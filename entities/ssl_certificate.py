import osintbuddy as ob
from osintbuddy.elements import TextInput


class SSLCertificate(ob.Plugin):
    label = "SSL Certificate"
    color = "#0EA5E999"
    icon = "certificate-2"
    author = "OSIB"
    description = "Represent details from an SSL/TLS certificate."

    elements = [
        TextInput(label="Common Name", icon="certificate-2"),
        TextInput(label="Issuer", icon="shield"),
        TextInput(label="Fingerprint", icon="fingerprint"),
    ]

