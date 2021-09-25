# Not finished

import os
import sys
import json
import requests

def main():
    __from_terminal__ = not "idlelib" in sys.modules
    
    if not __from_terminal__:
        sys.stderr.write("MUST be ran from terminal")
	sys.stderr.flush()
        sys.exit(1)
    else:
	if sys.platform == "win32":
		INSTALLDIR = "C:\\PyGet\\"
	elif sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
		INSTALLDIR = "/home/$(whoami)/PyGet/"
	else:
		sys.stderr.write("Unsupported OS")
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

		PACKAGES_JSON_STRUCTURE = """{
	"pyget": {
		"version": 1.0
	}
}"""

		def installPackageFromManifest(manifest, installDir):
			sourceCode = requests.get(manifest["source"]).text
			with open(installDir + manifest["name"], "wb") as file:
				file.write(sourceCode)

		def searchForManifest(property, value):
			pass # For now

		def uninstallPackage(id):
			pass # For now

		if os.path.isfile("packages.json"):
			with open("packages.json", "r") as file:
				contents = file.read()
		elif not os.path.isfile("packages.json"):
			with open("packages.json", "w") as file:
				file.write(PACKAGES_JSON_STRUCTURE)

		try:
			if not sys.argv[1] or sys.argv[1] == "help":
				print(helpText)
			else:
				if sys.argv[1] == "install" or sys.argv[1] == "upgrade":
					installPackageFromManifest(searchForManifest("id", sys.argv[2]), INSTALLDIR)
				elif sys.argv == "remove" or sys.argv == "uninstall":
					uninstallPackage(sys.argv[2])
		except IndexError:
			print(helpText)

if __name__ == "__main__":
	main()
