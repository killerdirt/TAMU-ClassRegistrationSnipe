from ClassObj import TAMUClass
from ClassManipulator import Classer
from ConfigReader import ConfigReader
import time

# Opens configuration file
configs = ConfigReader("config_angelo.ini")
# Make sure to change this to whatever your cofig file is


# Opens the browser
classBrowser = Classer(configs.user, configs.password)

# Gets classes from the config reader
classes = configs.classes

# Initialization step.
for classItem in classes:
    print("Initializing: " + classItem.subjectAbbr, classItem.courseNumber)
    # Initializing CRNs
    if(classItem.sectionNumbers[0] == "ALL"):
        crns, courses, openSpots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber)        
        classItem.setSectionNums(courses)
        classItem.setCRNs(crns)
        classItem.setRemainingSpots(openSpots)
    else:
        crns, crsNums, openSpots = classBrowser.getData(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.setSectionNums(crsNums)   # Might have been reordered
        classItem.setCRNs(crns)
        classItem.setRemainingSpots(openSpots)

print("INITIALIZED!")
    


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
        print("Checking: " + classItem.subjectAbbr, classItem.courseNumber)

        spots = classBrowser.checkSpots(classItem.subjectAbbr, classItem.courseNumber, classItem.sectionNumbers)
        classItem.setRemainingSpots(spots)
        message = classItem.checkOpenSpotMessage()

        # If theres an open
        if not message == "":
            print(message)
            classBrowser.emailNotif(message, configs.emailTo, configs.emailFrom, configs.emailPass)
            
            # If the user wanted a class to be auto added
            if(classItem.addClass):
                # Gets list of good CRNs
                toBeAdded = classItem.checkAutoAdd()
                tries = 0
                success = False

                # If theres a class that needs to be dropped.
                if(classItem.needDrop):
                    while(not success and tries < len(toBeAdded)):
                        # dropThenAddClass returns 0 if it was successful
                        success = classBrowser.dropThenAddClass(classItem.conflictCRN, toBeAdded[tries]) ==0
                        tries += 1
                else:
                    while(not success and tries < len(toBeAdded)):
                        # addClass returns 0 if it was successful
                        success = classBrowser.addClass(toBeAdded[tries]) ==0
                        tries += 1
                
                # just feedback for user
                if(success):
                    print("SUCCESS CONFIRMED BOIS")
                else:
                    print("Failure.")



    runs=runs+1
    print("Completed " + str(runs) + " runs!")
    # sleep configured in config.ini
    time.sleep(configs.pollingRate) 