'''
Written by George Kent-Scheller
last changed 5/31/2019
* This program fetches files with a specifc ending
* from the WRDS server in a directory and copies
* them to another.
if it doesnt work or if you have any questions contact me at:
215-873-3999
Georgetks@gmail.com
'''
# import statements
import os
import sys
import subprocess
import time
TIME_L = 5
TIME_S = 0.1
TIME_MS = 0.05

#fetches the starting directory of the .py file. This is used extensively throughout the 3 programs.
def getPyDir():
    return os.path.dirname(os.path.realpath(__file__))


# this function finds the file with a specific extention that is in a specific diriectory and folder
def search(searchS,fileE,foldN,Dest,dispOn):
    # dispOn is the printing function
    if dispOn:
        print(searchS)
        
    
    badDir = getTupsFromFile("badDirs.txt") #("sec","nyse","nas99axs","nas00axs","nas01axs","nas02axs","nas03axs","nas04axs","nas05axs","nas06axs","nas07axs","nas08axs","hfrsamp" )
    dirs = os.listdir(searchS)
    f = open(getPtDir()+"/takenFileLocations.txt",'w')
    for folders in dirs:

        if dispOn:
            print("\tChecking: "+folders+"\n")
            time.sleep(TIME_S)
        # this pauses over directories which have been flaged and then skips them.
        if folders.endswith(badDir):
            if dispOn:
                print(folders + " is a \'badDir\'")
                time.sleep(TIME_S)
        else:
            hasSASFiles = False # this is used to check to see if it has any sas folders to improve future searches
            
            for dirName, subdirList, fileList in os.walk(searchS+folders):# this is a depth first search alg

                if dispOn:
                    print('\nFound directory: %s' % dirName)
                    time.sleep(TIME_MS)

                if dirName.lower().endswith(foldN) or dirName.lower().endswith(foldN + "/"): #checks for folder
                    for fname in fileList:
                        if fname.endswith(fileE): #checks for file in folder ending with X
                            if dispOn:
                                print("\t\t-Copying "+fname+ "....")
                                time.sleep(TIME_MS)
                            try:# attempts to copy the file
                                copyTo(dirName+"/"+fname,Dest)
                                f.write(fname+":\t"dirName+"/"+fname+"/")
                                hasSASFiles = True
                            except:
                                print ("something bad happend... \n ",sys.exc_info()[0])
                                raise
    f.close()


# currently this uses bash to accomplish its task
# this is to avoid importing another lib
def copyTo(fileN,Destination):
    stringComand ="cp " + str(fileN) + " " +str(Destination)
    process = subprocess.Popen(stringComand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
def getTupsFromFile(name):
    f = open((getPyDir()+"/"+name),'r')
    lisp = []
    for l in f:
        lisp.append(l.replace("\n",''))
    f.close()
    tupy = tuple(lisp)
    return tupy
