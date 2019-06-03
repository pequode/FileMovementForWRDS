#!/usr/bin/env python
'''
Written by George Kent-Scheller
last changed 5/31/2019

*This program contains both the run program for the other two files and the code for the testing of sas files.
*The first thing  that this program does is to run the other two methods from the other programs(prog_find.py,checkF.py).
*The the program goes through the programs folder and edits all sas files with libname. It then runs all sas files and
*sorts them into working and broken.
*It also saves a log of the console errors and the internal errors of these programs.

if it doesnt work or if you have any questions contact me at:
215-873-3999
Georgetks@gmail.com
'''
import os
import shutil # used for file manipulation
import sys
import subprocess
import time
import threading
from prog_find import search
from check_dep import checkF
from check_dep import cleanUp
from check_dep import tryToMove

#creates global vars for disp
SLEEP_TIME_SHORT = 0.5
SLEEP_TIME = 1
SLEEP_TIME_LONG = 5
CURENTF = "none"
CHECKFILESDISP = True
SEARCHDISP = True
REMNAMEDISP = False
ERRORCHECKDISP = True
ERRORCHECKMAN = False
ERRORCHECKPATH = "none"
runCPRE = (1,1,1,1)
DispIsOn = False

def removeLibName(rootDir,DispIs):
    DispIsOn = DispIs
    # shows the sub files in the root dir
    filename=os.listdir(rootDir)
    #checks to see if running in Disp Mode then Prints if true. All other Disp methods look like this.
    if DispIsOn:
         print("Files to be read: \n")
         print(filename)# prints file name list
         time.sleep(SLEEP_TIME_LONG)

    #traverses the directory
    for infile in filename:
        
        #gets the full path of a certain file
        fullpath = rootDir +"/" + infile

        if DispIsOn:
                print("\nPath:~",fullpath)
                time.sleep(SLEEP_TIME)
        #opens it with read on
        f=open(fullpath,'r')
        #gets the full txt of the file
        text=f.readlines()
        text2 =""
        for lines in text:
            if "libname" in lines:
                text2= text2 + ""
            else
                text2 = text2 + lines
        
        f.close()
        #opens the full txt with write permissions
        f = open(fullpath,'w')

        if DispIsOn:
            print(text)
            time.sleep(SLEEP_TIME_LONG)
            print(text2)
            time.sleep(SLEEP_TIME_LONG)

        #writes new data to file
        f.write(text2)
        f.close()
        if DispIsOn:
            print("Done deleting for: ", fullpath)
            time.sleep(SLEEP_TIME)


def runFilesCatchErrors(rootDir,DispIs,Manual):
    DispIsOn = DispIs
    #gets the sub files in the root dir
    filename=os.listdir(rootDir)
    totalNum = len(filename)
    if Manual:
        disp = raw_input("\nDo you want to disp?(y): \n")
        if disp.lower() == "y" : DispIsOn = True
    if DispIsOn:
        print(filename)
        time.sleep(SLEEP_TIME_SHORT)
    #opens a log file and an error file write permissions on to name it
    logf=open((getPyDir()+"/Logfile.log"),'w+')
    #creates a header
    logf.write("                             LOG                             \n\n\n-------------------------------------------------------------")
    logf.close
    Errorf=open((getPyDir()+"/error.log"),'w+')
    Errorf.write("                          ERROR LOG              \n\n\n---------------------------------------------------")
    Errorf.close
    moveOrder = []
    #traverses the files in the directory
    count = 0
    for infile in filename:
            if infile.endswith(".sas"):
                count =float(count + 1)
                CURENTF = infile
                dontSkip = True
                if Manual:
                        skipAble = raw_input("\nDo you want to run "+infile+ " ?(y): \n")
                        dontSkip = skipAble.lower() == "y"
                dontSkip = doesntHavePhrase( getPyDir()+"/programs/"+infile,"username=_prompt_;")
                if dontSkip:
                    if DispIsOn:
                        print("\nWorking on " + infile + "\n")
                        time.sleep(SLEEP_TIME_SHORT)
                    #gets the full path of a certain file
                    fullpath = rootDir +"/"+ infile
                    
                    #makes a comand to exacute a sas file in bash
                    stringComand ="sas " + fullpath + " -log " + getPyDir()+"/logs"
                    output, error = runComand(stringComand)
                    addErrAndOut(infile,output,error,getPyDir())#saves the output

                    dotLogN = infile[:-3] + "log"
                    #checks to see where to move program
                    if str(error) =="None" and "ERROR" not in str(output) and doesntHavePhrase(getPyDir()+"/logs/"+ dotLogN,"ERROR"):
                        if DispIsOn: print("\nDone Checkinging for: " + infile + "-----GOOD------\n")
                        printProgress(count,totalNum,SLEEP_TIME)  
                        Comand = ("mv " + fullpath + " " + getPyDir()+"/" + "fixed_prog")
                        out, err = runComand(Comand)
                    else:
                        if DispIsOn: print("\nDone Checkinging for: " + infile + "------Had an Error------\n")
                        printProgress(count,totalNum,SLEEP_TIME)
                        Comand = ("mv " + fullpath + " " +getPyDir()+"/"+ "brok_prog")
                        out, err = runComand(Comand)
                        try: shutil.copyfile((getPyDir()+"/logs/"+ dotLogN),getPyDir()+"/"+ "brok_prog/"+dotLogN)
                        except: pass
                else:
                    try: shutil.move(getPyDir()+"/programs/"+CURENTF,getPyDir()+"/programs/manLogin/"+CURENTF)
                    except:
                        moveOrder.append(CURENTF)
                        pass
                    if DispIsOn: print("\nSkipping: " + infile)
                    printProgress(count,totalNum,SLEEP_TIME)
    moveToManual(moveOrder)
def runComand(Comand):
    #runs the command in bash
    process = subprocess.Popen(Comand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return outPut,error;
def addErrAndOut(inFile,Output,Error,Path):
    logf=open((Path+"/Logfile.log"),'a')
    Errorf=open((Path+"/error.log"),'a')
    logf.write("\n\nErrors for " + inFile +"  from internal file diagnostic.\n\n")
    logf.write(str(Output))
    logf.write("\n-----------------------------------------\n")
    logf.close
    Errorf.write("\n\n Error for " + inFile +": \n\n")
    Errorf.write(str(Error)+"\n-----------------------------------------\n")
    Errorf.close

def doesntHavePhrase(path,phrase):
    logFileOpen = open(path,'r')
    textToCheck = logFileOpen.read()
    logFileOpen.close()
    return (not phrase in  textToCheck)
    
def printProgress(current,Total,timeToWait):
    if DispIsOn:
        print("%.2f%% done!" %((current/Total)*100 ))
        time.sleep(timeToWait)
def moveToManual(Lisp):
    if DispIsOn:
        print(Lisp)
        time.sleep(SLEEP_TIME)
    for x in Lisp:
        try: shutil.move(getPyDir()+"/programs/"+Lisp[x],getPyDir()+"/programs/manLogin/"+Lisp[x])
        except:pass
        
#gets starting directory
def getPyDir():
    return os.path.dirname(os.path.realpath(__file__))

#runs designated functions
def run():
    print("Running program may take about 20 min")
    #the directory that you want the files to be sent to
    ERRORCHECKPATH = getPyDir()+"/programs"
    # the directory you are searching
    searchStartDir = "/PROD/wrds/"
    # this is the file extention that you are looking for
    fileEnd = ".sas"
    # this is the name of the folder that has what you want
    desFolderN = "samples"
    #checks to make sure all of the files are in order, if they are not prompts user for an abort
    if runCPRE[0]:
        checkF(CHECKFILESDISP)
        time.sleep(SLEEP_TIME)
    #this copies all of the files to programs
    if runCPRE[1]: search(searchStartDir,fileEnd,desFolderN,ERRORCHECKPATH,SEARCHDISP)
    #this removes the string "libname" from the files
    if runCPRE[2]: removeLibName(ERRORCHECKPATH,REMNAMEDISP)
    #this trys to run the files for errors
    if runCPRE[3]:
        runFilesCatchErrors(ERRORCHECKPATH,ERRORCHECKDISP,ERRORCHECKMAN)
        cleanUp()
run()
