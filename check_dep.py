#!/usr/bin/env python
'''
Written by George Kent-Scheller
last changed 5/31/2019

*This program attempts to do all of the clean up after a test and makes sure that the important folders and files exist
*it is not perfict and only will work under specific conditions. For this reason it may be nessisary to do many of the
*steps manually through bash

if it doesnt work or if you have any questions contact me at:
215-873-3999
Georgetks@gmail.com
'''
import os
import sys
import subprocess
import time
import datetime
import shutil
import random
TIME_S = 0.25
TIME = 1
TIME_L = 5
folders = ("logs","programs","programs/","fine_prog","fixed_prog","brok_prog")
files = ("readme","autoadd_sas.py","prog_find.py","Logfile.log","error.log")
#gets directory of the .py file
def getPyDir():
    return os.path.dirname(os.path.realpath(__file__))

DISP = False # a more convient way of implementing the display feature across multiple functions.

# this function is the main runner of the psudo class
def checkF(dispOn):
    DISP = dispOn # turns on display

    if not hasALLFolders(): addFolders()#checks to see if any folders are missing. If they are it adds them.
    
    code = hasALLFiles() #gets diagnositc code
    # codes are as follows
    #-1 = error whose fix is not implemented in the code
    # 1 = all files there and empty as well as all folders there and empty
    # 2 = all files there but some are filled with data
    #-3 = error in function execution
    #exits if it cant solve the problem
    
    if code == -1:
        if DISP:
            print("Error you are missing some important files")
            time.sleep(TIME_S)
        quit()
    
    #finishes if has correct code and files are empty
    elif code == 1 :
        if DISP:
            print("All files found")
            time.sleep(TIME)
        return True
    
    #attempts to finish by solving file storage
    elif code == 2 or not( progsAreEmpty()):
        inp =raw_input("looks like the program was already run. Do you want to save an archive and run again:(y) \n")
        #normalizes input and creates an archive folder
        if inp.lower() == 'y':
            cleanAndRun()

        #quits the program
        else:
            if DISP:
                print("You didnt hit y. Exiting... ")
                time.sleep(TIME)
            quit()
            
    #quits the program
    else:
        if DISP:
                print("Error: Bad error code check .py file")
                time.sleep(TIME)
        quit()
        
#functions checks to see that the folders are empty
def progsAreEmpty():
    areEmpty = True
    for i in folders: if not len(os.listdir(getPyDir()+ "/"+i)) == 0: areEmpty = False
    return areEmpty

#function creats a new folder with a certain name at the correct path
def addFolder(name):
    newDir = getPyDir()+"/"+name
    if DISP:  print("Made: " + newDir)
    os.makedirs(newDir)

# adds folders for each of the missing folders
def addFolders():
    #boolean creation for folder existance
    foldInDir = os.listdir(getPyDir())
    for x in folders
        if x not in foldInDir: addFolder(x)

#checks to see if all the files are in the directory
def hasALLFiles():
    fileInDir = os.listdir(getPyDir())
    if DISP:
        print(fileInDir)
    # boolean creation
    hasAutoadd_sas = "autoadd_sas.py" in fileInDir
    hasProg_find = "prog_find.py" in fileInDir
    hasLogfile = "Logfile.log" in fileInDir
    hasError = "error.log" in fileInDir
    hasReadme = "readme" in fileInDir

    if DISP:
        for x in files:
            print("Have " + x + ": " + str(x in fileInDir)
                  
    neededProgs = hasAutoadd_sas and hasProg_find and hasReadme
    oldRunProgs = hasError and hasLogfile
    badCase = (hasError != hasLogfile) or  (not neededProgs)

    

    #return based on bools
    if badCase:
        return -1
    elif neededProgs and not oldRunProgs and progsAreEmpty():
        return 1
    elif neededProgs and oldRunProgs:
        return 2
    else:
        return -3

#check to see if all the folders are in the directory
def hasALLFolders():
    foldInDir = os.listdir(getPyDir())
    hasTheFolders = True
    for n in folders:
        if not n in foldInDir:
            hasTheFolders = false
    if DISP:
        for f in folders:
            print("Have " + f +": "+str(f)
    return hasTheFolders

def moveLFiles(newDir):
    InDir = os.listdir(getPyDir())
    for files in InDir:
        if (not (files.endswith("error.log") or files.endswith("Logfile.log"))) and (files.endswith(".lst") or files.endswith(".log")) :
             shutil.move(getPyDir()+"/"+files,newDir+"/logs/"+files)
def cleanUp():
    moveLFiles(getPyDir())

#attempts to move all changed files into archive
def tryToMoveF(newDir,folder):
    try: shutil.move(getPyDir()+"/"+folder+"/",newDir+"/"+folder+"/")
    except: pass
def tryToMove(newDir,fileN):
    try: shutil.move(getPyDir()+"/"+fileN,newDir+"/"+fileN)
    except: pass
def moveOutFolder(path,name):
    InDir = os.listdir(getPyDir()+"/"+name+"/")
    for files in InDir: shutil.move(getPyDir()+"/"+name+"/"+files, path+"/"+name+"/"+files)
def moveEverythingout(path):
    for fld in folders:
        moveOutFolder(path,fld)
    
def tryToMoveAll(newDir):
    for k in folders:
        tryToMoveF(newDir,k)
    tryToMove(newDir,"takenFileLocations.txt")   
    tryToMove(newDir,"Logfile.log")
    tryToMove(newDir,"error.log")
    
    addFolders() # adds all of the folders back
    moveEverythingout(newDir)
    
def cleanAndRun():
    CDT = datetime.datetime.now()
    date = str(CDT.month)+"_"+str(CDT.day)+"_"+str(CDT.year)+"_ID:"+random.randint(1,10000)
    newDir = getPyDir()+"/Arc_"+date
    cleanUp()
    os.makedirs(newDir)
                    
    if DISP:
        print("Made: " + newDir)
        time.sleep(TIME)
                    
    tryToMoveAll(newDir)
    
    #checks to see if the program now works
    if hasALLFiles() == 1:
        if DISP:
            print("All files found")
            time.sleep(TIME)
        return True
    
    #quits the program
    else:
        if DISP:
            print(hasALLFiles())
            print("Unknown Error")
        quit() 

