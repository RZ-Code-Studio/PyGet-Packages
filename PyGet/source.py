# Not finished

import os
import sys
import json
import requests
import shutil


def main():
    __from_terminal__ = not "idlelib" in sys.modules

    if not __from_terminal__:
        sys.stderr.write("MUST be ran from terminal\n")
        sys.stderr.flush()
        sys.exit(1)
    else:
        if sys.platform == "win32":
            INSTALLDIR = f"{os.environ['USERPROFILE']}\\PyGet-Packages\\"
        elif sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
            INSTALLDIR = "/home/$(whoami)/PyGet-Packages/"
        else:
            sys.stderr.write("Unsupported OS\n")
            sys.stderr.flush()
            sys.exit(1)

        helpText = """
Arguments|Parameters|Description
---------------------------------
upgrade   <package>    Upgrades <package>
install   <package>    Installs <package>
uninstall <package>    Uninstalls <package>
remove    <package>    Alias for uninstall
add       <package>    Alias for install
help                   Displays this message
"""

        def printHelpText(header):
            print(header)
            print(helpText)

        def installPackageFromManifest(manifest, installPath):
            if not os.path.isdir(installPath + manifest["name"]):
                os.system(f"mkdir {installPath + manifest['name']}")

            sourceCode = requests.get(manifest["source"]).text

            for dependencyManifestURL in manifest["dependencies"]:
                installPackageFromManifest(getManifest(dependencyManifestURL), installPath)

            with open(f"{INSTALLDIR}packages.json", "r") as file:
                try:
                    data = json.load(file)
                except:
                    with open(f"{INSTALLDIR}packages.json", "w") as file2:
                        file2.writelines([
                            "{\n",
                            "    \"pyget\": { \n",
                            "        \"version\": 1.0,\n",
                            "        \"source\": \"https://raw.githubusercontent.com/RZ-Code-Studio/Pyget-Packages/main/PyGet/source.py\",\n",
                            "        \"name\": \"PyGet\",\n", 
                            "        \"dependencies\": []\n", 
                            "    }\n", 
                            "}"
                        ])
                    
                        with open(f"{INSTALLDIR}packages.json", "r") as file3:
                            data = json.load(file3)

            with open(f"{INSTALLDIR}packages.json", "w") as file:
                isManifestInData = data | manifest == data

                if not isManifestInData:
                    data[manifest["name"]] = manifest

                json.dump(data, file)

            try:
                with open(installPath + manifest["name"] + "\\" + manifest["source"].split("/")[len(manifest["source"].split("/")) - 1], "wb") as file:
                    file.write(sourceCode)
            except:
                with open(installPath + manifest["name"] + "\\" + manifest["source"].split("/")[len(manifest["source"].split("/")) - 1], "w") as file:
                    file.write(sourceCode)

        def getManifest(url):
            manifest = requests.get(url).json()
            return manifest

        def uninstallPackage(theName):
            try:
                shutil.rmtree(INSTALLDIR + theName)
            except:
                sys.stderr.write("The package isn't even installed\n")
                sys.stderr.flush()
                sys.exit(1)
            
            with open(f"{INSTALLDIR}packages.json", "r") as file:
                data = json.load(file)
            
            for key in data:
                if key == theName:
                    del theName[key]

            with open(f"{INSTALLDIR}packages.json", "w") as file:
                file.write(json.dumps(str(data)))

        if not os.path.isfile(f"{INSTALLDIR}packages.json"):
            if not os.path.isdir(INSTALLDIR):
                os.system(f"mkdir {INSTALLDIR}")

            with open(f"{INSTALLDIR}packages.json", "w") as file:
                print(f"{INSTALLDIR}packages.json")
                file.writelines([
                    "{\n",
                    "    \"pyget\": { \n",
                    "        \"version\": 1.0,\n",
                    "        \"source\": \"https://raw.githubusercontent.com/RZ-Code-Studio/Pyget-Packages/main/PyGet/source.py\",\n",
                    "        \"name\": \"PyGet\",\n", 
                    "        \"dependencies\": []\n", 
                    "    }\n", 
                    "}"
                ])

        try:
            if sys.argv[1] == "help":
                printHelpText("Command Help")
            elif not sys.argv[1]:
                printHelpText("Must be supplied by arguments")
            else:
                if sys.argv[1] == "install" or sys.argv[1] == "upgrade" or sys.argv[1] == "add":
                    installPackageFromManifest(getManifest(
                        f"https://raw.githubusercontent.com/RZ-Code-Studio/Pyget-Packages/main/{sys.argv[2]}/manifest.json"), INSTALLDIR)
                elif sys.argv[1] == "remove" or sys.argv[1] == "uninstall":
                    uninstallPackage(sys.argv[2])
        except IndexError:
            printHelpText("Must be supplied by arguments")

if __name__ == "__main__":
    main()
