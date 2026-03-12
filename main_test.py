#Make EXE:
#pip install pyinstaller
#pyinstaller --onefile -w main.py

# region imports
import os, time
from datetime import datetime
from ConfigParams import *

import sys
from VersionControl import *
from Logger import *
# endregion

# region Declarations

# endregion

log_file_cnt.append(f"Program start....... {datetime.fromtimestamp(time.time())} ")
print("Program started...", file=sys.stdout)
#command = 'echo "Hello, World!" 1> output.txt'
#command = 'echo "Hello, World!"'
#os.system(command)

# region reading config
config = Config(config_file)
# endregion

# region main
for folderPath in config.verified_report_folders:
    dir_list = os.listdir(folderPath)
    file_list = []

    if os.path.exists(folderPath):
        for elem in dir_list:
            file_list.append(f"{folderPath}\\{elem}")

        curyear = datetime.fromtimestamp(time.time()).year
        curmonth = datetime.fromtimestamp(time.time()).month
        filesToDelete = []

        Logger.writeLogTrace(config.trace, f"Searching for old files in {folderPath}...")
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
        Logger.writeLogWarn(f"Folder not found: {folderPath}")
    print("")
# endregion

log_file_cnt.append(f"Program end......... {datetime.fromtimestamp(time.time())}")
Logger.writeLog()


