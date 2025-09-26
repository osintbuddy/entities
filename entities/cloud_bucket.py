import osintbuddy as ob
from osintbuddy.elements import TextInput


class CloudBucket(ob.Plugin):
    label = "Cloud Bucket"
    color = "#10B98199"
    icon = "bucket"
    author = "OSIB"
    description = "Represent a cloud storage bucket (S3/GCS/Azure)."

    elements = [
        TextInput(label="Provider", icon="cloud"),
        TextInput(label="Bucket", icon="bucket"),
        TextInput(label="Region", icon="map-pin"),
    ]
