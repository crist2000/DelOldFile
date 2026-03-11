#Make EXE:
#pip install pyinstaller
#pyinstaller --onefile -w main.py

# region imports
import os, time
from datetime import datetime
import socket
import sys
# endregion

# region Declarations
hostname = socket.gethostname()
cls = lambda: os.system('cls')

version = "1.0"
DelFilePath = r"DeletedFiles.txt" # list of deleted files
config_file = r"config.ini"
log_file = f"{hostname}_log.txt"
tester = None
trace = 0  #trace data to log
log_file_cnt = [] # log file content
repor_folders = [] # folder list in ini file
verified_repor_folders = [] # folder list that actually present

def writeLog():
    with open(log_file, 'a') as file:
        for f in log_file_cnt:
            file.write(f"{f}\n")

def writeLogErr(msg):
    log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} ERR: {msg}")

def writeLogInfo(msg):
    log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} INFO: {msg}")

def writeLogWarn(msg):
    log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} WARN: {msg}")

def writeLogTrace(isTrue, msg):
    if isTrue:
        log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} TRACE: {msg}")
# endregion


log_file_cnt.append(f"Program start....... {datetime.fromtimestamp(time.time())} ")
print("HELLO")
#print("Program started...", file=sys.stdout)
#command = 'echo "Hello, World!" 1> output.txt'
#command = 'echo "Hello, World!"'
#os.system(command)

# region reading config
try:
    if not os.path.exists(config_file):
        raise FileNotFoundError(None)
except FileNotFoundError:
    writeLogErr(f"{hostname} config.ini not found")
    writeLog()

with open(config_file) as f:
    config_lines = f.read().splitlines()

for line in config_lines:
    if line.startswith("#"):
        continue

    split_line = line.split("=")
    match split_line[0]:
        case "Tester": tester = split_line[1]
        case "ReportFolder": repor_folders.append(split_line[1])
        case "Trace":
            if(split_line[1] == "True"):
                trace = 1
        case _: writeLogErr(f"Unknow config parameter {split_line[0]}")

writeLogTrace(trace, f"Version: {version}")
writeLogTrace(trace, f"Tester: {tester}")

if tester is None:
    tester = hostname

for line in repor_folders:
    if os.path.exists(line):
        writeLogTrace(trace, f"Config path found: {line}")
        verified_repor_folders.append(line)
    else:
        writeLogErr(f"Config path not found {line}")
# endregion

# region main
for folderPath in verified_repor_folders:
    dir_list = os.listdir(folderPath)
    file_list = []

    if os.path.exists(folderPath):
        for elem in dir_list:
            file_list.append(f"{folderPath}\\{elem}")

        curyear = datetime.fromtimestamp(time.time()).year
        curmonth = datetime.fromtimestamp(time.time()).month
        filesToDelete = []

        writeLogTrace(trace, f"Searching for old files in {folderPath}...")
        cnt = 0
        for f in file_list:
            t_mod = os.path.getmtime(f)
            fyear = datetime.fromtimestamp(t_mod).year
            fmonth = datetime.fromtimestamp(t_mod).month

            cnt += 1
            pcnt = int(cnt / len(file_list) * 100)
            sys.stdout.write(f"\r")
            sys.stdout.write(f"{folderPath} {pcnt}%")
            sys.stdout.flush()
    else:
        writeLogWarn(f"Folder not found: {folderPath}")
    print("")
# endregion

log_file_cnt.append(f"Program end......... {datetime.fromtimestamp(time.time())}")
writeLog()


