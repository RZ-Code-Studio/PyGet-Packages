# Not finished

import os
import sys
import json
import requests

INSTALLDIR = "C:\\PyGet\\"

contents = ""
helpText = """
Must be supplied with arguments.

Arguments  Parameters Description
---------------------------------
upgrade   <package>    Upgrades <package>
install   <package>    Installs <package>
uninstall <package>    Uninstalls <package>
help                   Displays this message
"""

PACKAGES_JSON_STRUCTURE = """{
    "pyget": {
        "version": 1.0,
    }
"""

def installPackagesFromManifest(manifest, installDir):
    sourceCode = requests.get(manifest["source"]).text
    with open(installDir + manifest["name"], "wb") as file:
        file.write(sourceCode)

def searchForManifest(property, value):
    pass # For now
        
if os.path.isfile("packages.json"):
    with open("packages.json", "r") as file:
        contents = file.read()
elif not os.path.isfile("packages.json"):
    with open("packages.json", "w") as file:
        file.write(PACKAGES_JSON_STRUCTURE)

if not sys.argv[1] or sys.argv[1] == "help":
    print(helpText)
else:
    if sys.argv[1] == "install":
        installPackageFromManifest(searchForManifest("id", sys.argv[2]), INSTALLDIR)
    elif sys.argv[1] == "upgrade":
        installPackageFromManifest(searchForManifest("id", sys.argv[2]), INSTALLDIR)
    else:
        uninstallPackage(sys.argv[2])
