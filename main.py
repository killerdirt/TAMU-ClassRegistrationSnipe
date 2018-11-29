from ClassObj import TAMUClass
from ClassManipulator import Classer
from ConfigReader import ConfigReader
import time

# Opens configuration file
configs = ConfigReader("config.ini")

# Opens the browser
classBrowser = Classer(configs.user, configs.password)

classes = configs.classes

# Initialization step.
for classItem in classes:
    print(classItem.subjectAbbr)

    # Initializing CRNs
    if(classItem.sectionNumbers[0] == "ALL"):
        crns, courses, openSpots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber)
        
        # print(crns, courses, openSpots)
        # print(len(crns), len(courses), len(openSpots))
        
        classItem.setSectionNums(courses)
        classItem.setCRNs(crns)
        classItem.setRemainingSpots(openSpots)
    else:
        crns, crsNums, openSpots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        
        # print(crns, crsNums, openSpots)

        classItem.setSectionNums(crsNums)   # Might have been reordered
        classItem.setCRNs(crns)
        classItem.setRemainingSpots(openSpots)
    


runs = 0

# Objs are now setup and stuff.
# TODO: Add caching so that this step only has to be run when ini file is changed.

# This is the big while loop daddy
# All it does is:
#                   1.) Check for open spots for all classes and stuff
#                   2.) Updates the variables of the classes
#                   3.) Checks to see if any of the classes specified has an open spot.
while(True):

    for classItem in classes:
        spots = classBrowser.checkSpots(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.setRemainingSpots(spots)
        message = classItem.checkOpenSpots()
        if not message == "":
            print(message)
            classBrowser.emailNotif(message, configs.emailTo, configs.emailFrom, configs.emailPass)


    runs=runs+1
    print("Completed " + str(runs) + " runs!")
    # sleep configured in config.ini
    time.sleep(configs.pollingRate) 
    


