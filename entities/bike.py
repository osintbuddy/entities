import osintbuddy as ob
from osintbuddy.elements import TextInput


class Bike(ob.Plugin):
    label = "Bike"
    color = "#22C55E99"
    icon = "bike"
    author = "OSIB"
    description = "Represent a bicycle with make/model."

    elements = [
        TextInput(label="Make", icon="tool"),
        TextInput(label="Model", icon="tools"),
        TextInput(label="Serial Number", icon="hash"),
    ]

