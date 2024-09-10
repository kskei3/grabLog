#Call: python3 main.py <outputFile> <startTime> <endTime> logDir logsName
#Call: python3 main.py output/kk01.txt 2024.08.28D06:16:52.000 2024.08.28D06:17:06.000 ./logdir/ ds_gw_actiontracker_a,ds_action_tracker_a
import sys
import os
import re
import datetime


def findFilesByRegex(logDirPath, logFile, logNameRegex):
    logNameRegex = ["(^" + item +".*)" for item in logNameRegex]
    logNameRegex = "|".join(logNameRegex)
    # regex = "(^ds_gw_actiontracker_a\.1.*)|(^ds_action_tracker_a\.1.*)"
    for filename in os.listdir(logDirPath):
        if bool(re.search(logNameRegex, filename)): #re.IGNORECASE
            logFile.append(filename)
    return logFile

def timestampToDatetime(timestamp):
    timestamp = timestamp[0:10] + "D" + timestamp[11:22]
    format = "%Y.%m.%dD%H:%M:%S.%f"
    try:
        d = datetime.datetime.strptime(timestamp,format)
    except ValueError:
        d = datetime.datetime.now()
    return d


def grabFileContent(logDirPath, logFile,startTime,endTime ):        #<time> | <filename> | <logFile Msg> |
    output = []
    for f in logFile:
        print(f"Reading this file: {f}")
        try:
            openFile = reversed(list(open(f"{logDirPath}"+f"{f}","r")))
            for logLine in openFile:
                if len(logLine) > 31 or logLine[0]=="'":           #<->2024.08.28D06:16:55.579 ###
                    print(logLine)
                    if logLine[0] =="'":
                        logTime= timestampToDatetime(logLine[1:logLine.find(" ")])
                    else:
                        logTime= timestampToDatetime(logLine[3:logLine.find(" ### ")])
                    if startTime <= logTime <= endTime:
                        print(f"Output: {logLine}")
                        output.append((logTime, f , logLine))
                    if logTime < startTime:
                        break
        except:
            pass
    return output

def writeFile(outputFile, result):
    f= open(outputFile,'w+')
    l = " ".join(sys.argv) + " \n\n"
    for r in result:
        line = r[1] + "\n" + r[2]
        f.write(line + "\n")
    f.close()

def main():
    outputFile, startTime, endTime, logDirPath = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    startTime = timestampToDatetime(startTime)
    endTime = timestampToDatetime(endTime)
    logNameRegex = sys.argv[5].split(",")
    logFile = []
    logFile = findFilesByRegex(logDirPath, logFile, logNameRegex)
    print(f"Readning the following files: {logFile} \n")
    output = grabFileContent(logDirPath, logFile, startTime, endTime)
    result = sorted(output,key = lambda x:x[0])
    writeFile(outputFile,result)
main()