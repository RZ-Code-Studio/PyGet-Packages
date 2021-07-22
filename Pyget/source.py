# Not finished

import os
import json
import requests

contents = ""

if os.path.isfile("packages.json"):
    with open("packages.json". "r") as file:
        contents = file.read()
else:
    contents = """{
    "pyget": {
        "version": 1.0,
        "installed": true
    }
}"""
