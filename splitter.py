from lxml import etree
from datetime import datetime
import os, glob

# Note: PEPFAR is already in a single file
departments = {
    "US-GOV-7": "unitedstates",
    "US-GOV-11": "unitedstates",
    "XM-DAC-5-2": "bmz",
    "XM-DAC-5-52": "bmz",
}

for code, department in departments.items():

    if not os.path.exists("output/" + code):
        os.mkdir("output/" + code)
    activityFiles = glob.glob(os.path.join("data/"+ department +"/*.xml"))

    for iatifile in activityFiles:

        # Some files are empty
        try:
            root = etree.parse(iatifile)
        except:
            continue

        print("Extracting " + code + " from: " + os.path.basename(iatifile))
        
        for activity in root.iterfind("iati-activity"):
            matchingOrg = False
            participatingOrgs = activity.findall("participating-org")
            for participatingOrg in participatingOrgs:
                try:
                    if participatingOrg.attrib["role"] == "2" and participatingOrg.attrib["ref"] == code:
                        matchingOrg = True
                except:
                    matchingOrg = False
        
                
            if matchingOrg == False:
                activity.getparent().remove(activity)

        with open("output/" + code +"/" + os.path.basename(iatifile) + ".xml", "wb+") as out_file:
            out_file.write(etree.tostring(root, encoding="utf8", pretty_print=True))