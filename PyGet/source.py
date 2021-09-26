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
            INSTALLDIR = f"{os.environ['USERPRoFILE']}\\PyGet-Packages\\"
        elif sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
            INSTALLDIR = "/home/$(whoami)/PyGet-Packages/"
        else:
            sys.stderr.write("Unsupported OS\n")
            sys.stderr.flush()
            sys.exit(1)
		
        contents = ""
        helpText = """Must be supplied with arguments.
Arguments  Parameters Description
---------------------------------
upgrade   <package>    Upgrades <package>
install   <package>    Installs <package>		
uninstall <package>    Uninstalls <package>
help                   Displays this message
"""
            
        def installPackageFromManifest(manifest, installPath):
            if not os.path.isdir(installPath + manifest["name"]):
                os.system(f"mkdir {installPath + manifest['name']}")
            
            sourceCode = requests.get(manifest["source"]).text
                
            try:
			    with open(installPath + manifest["name"] + "\\" + manifest["source"].split("/")[len(manifest["source"].split("/")) - 1], "wb") as file:
                    file.write(sourceCode)
            except:
                with open(installPath + manifest["name"] + "\\" + manifest["source"].split("/")[len(manifest["source"].split("/")) - 1], "w") as file:
                    file.write(sourceCode)
                    
        def searchForManifest():
            manifest = requests.get(f"https://raw.githubusercontent.com/RZ-Code-Studio/Pyget-Packages/main/{sys.argv[2]}/manifest.json").json()
            return manifest

        def uninstallPackage(theName):
            try:
                shutil.rmtree(INSTALLDIR + theName)
            except:
                print("The package isn't even installed")
                        
        if os.path.isfile(f"{INSTALLDIR}packages.json"):
            with open(f"{INSTALLDIR}packages.json", "r") as file:
            contents = file.read()
        elif not os.path.isfile(f"{INSTALLDIR}packages.json"):
            print(os.path.isdir(INSTALLDIR))
                
            if not os.path.isdir(INSTALLDIR):
                os.system(f"mkdir {INSTALLDIR}")
                
            with open(f"{INSTALLDIR}packages.json", "w") as file:
                file.write("{\n    \"PyGet\"{\n        \"version\": 1.0\n    }\n}")

        try:
            if not sys.argv[1] or sys.argv[1] == "help":
                print(helpText)
            else:
                if sys.argv[1] == "install" or sys.argv[1] == "upgrade":
                    installPackageFromManifest(searchForManifest(), INSTALLDIR)
                elif sys.argv[1] == "remove" or sys.argv[1] == "uninstall":
                    uninstallPackage(sys.argv[2])
                                
        except IndexError:
            print(helpText)

if __name__ == "__main__":
    main()
