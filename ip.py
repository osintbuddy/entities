import socket
import httpx
from selenium.webdriver.common.by import By
from osintbuddy.elements import TextInput
from osintbuddy.errors import OBPluginError
from osintbuddy.utils import to_camel_case
import httpx
import osintbuddy as ob


class IP(ob.Plugin):
    label = "IP"
    color = "#F47C00"
    entity = [TextInput(label="IP Address", icon="map-pin")]
    icon = "building-broadcast-tower"
    author = "OSIB"
    description = "Internet Protocol address"

    @ob.transform(label="To website", icon="world")
    async def transform_to_website(self, node, use):
        website_entity = await ob.Registry.get_plugin('website')
        try:
            resolved = socket.gethostbyaddr(node.ip_address)
            if len(resolved) >= 1:
                blueprint = website_entity.create(domain=resolved[0])
                return blueprint
            else:
                raise OBPluginError("No results found")
        except (socket.gaierror, socket.herror):
            raise OBPluginError("We ran into a socket error. Please try again")

    @ob.transform(label="To subdomains", icon="world")
    async def transform_to_subdomains(self, node, use):
        nodes = []
        params = {
            "q": node.ip_address,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://api.hackertarget.com/reverseiplookup',
                    params=params,
                    timeout=None
                )
                data = response.content.decode("utf8").split("\n")
        except Exception as e:
            raise OBPluginError(e)
        subdomain_entity = await ob.Registry.get_plugin('subdomain')
        for subdomain in data:
            blueprint = subdomain_entity.create(subdomain=subdomain)
            nodes.append(blueprint)
        return nodes

    @ob.transform(label="To geolocation", icon="map-pin")
    async def transform_to_geolocation(self, node, use):
        summary_rows = [
            "ASN",
            "Hostname",
            "Range",
            "Company",
            "Hosted domains",
            "Privacy",
            "Anycast",
            "ASN type",
            "Abuse contact",
        ]
        geo_rows = [
            "City",
            "State",
            "Country",
            "Postal",
            "Timezone",
            "Coordinates",
        ]
        if len(node.ip_address) == 0:
            raise OBPluginError(
                "A valid IP Address is a required field for this transform"
            )

        geolocation = {}
        summary = {}
        with use.get_driver() as driver:
            driver.get(f'https://ipinfo.io/{node.ip_address}')
            for row in summary_rows:
                summary[to_camel_case(row)] = driver.find_element(
                    by=By.XPATH, value=self.get_summary_xpath(row)
                ).text
            for row in geo_rows:
                geolocation[to_camel_case(row)] = driver.find_element(
                    by=By.XPATH, value=self.get_geo_xpath(row)
                ).text
        IPGeolocationPlugin = await ob.Registry.get_plugin('ip_geolocation')
        blueprint = IPGeolocationPlugin.create(
            city=geolocation.get("city"),
            state=geolocation.get("state"),
            country=geolocation.get("country"),
            postal=geolocation.get("postal"),
            timezone=geolocation.get("timezone"),
            coordinates=geolocation.get("coordinates"),
            asn=summary.get("asn"),
            hostname=summary.get("hostname"),
            range=summary.get("range"),
            company=summary.get("company"),
            hosted_domains=summary.get("hostedDomains"),
            privacy=summary.get("privacy"),
            anycast=summary.get("anycast"),
            asn_type=summary.get("asnType"),
            abuse_contact=summary.get("abuseContact"),
        )
        return blueprint

    @staticmethod
    def get_summary_xpath(value: str):
        return (
            f"//td//span[contains(text(),'{value}')]"
            "/ancestor::td/following-sibling::td"
        )

    @staticmethod
    def get_geo_xpath(value: str):
        return f"//td[contains(text(),'{value}')]/following-sibling::td"
