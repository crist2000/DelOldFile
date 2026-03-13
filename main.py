#Make EXE:
#pip install pyinstaller
#pyinstaller main.py --onefile

# region imports
import sys
from ConfigParams import *
# endregion

# region Declarations
# endregion

log_file_cnt.append(f"Program start....... {datetime.fromtimestamp(time.time())} ")
print("Reading configuration.......", file=sys.stdout)

# region reading config
config = Config(config_file)
# endregion

# region main
print("Checking folders.......", file=sys.stdout)

for folderPath in config.verified_report_folders:
    dir_list = os.listdir(folderPath)
    file_list = []

    for elem in dir_list:
        if ext_mask in elem.upper():
            file_list.append(f"{folderPath}\\{elem.upper()}")

    ttime = time.time()
    curyear = datetime.fromtimestamp(ttime).year
    curmonth = datetime.fromtimestamp(ttime).month

    Logger.writeLogTrace(config.trace, f"Searching for old files in {folderPath}...")
    filesToDelete = []
    cnt = 0

    for f in file_list:
        t_mod = os.path.getmtime(f)
        fyear = datetime.fromtimestamp(t_mod).year
        fmonth = datetime.fromtimestamp(t_mod).month

        if(curyear - fyear > 10):
            filesToDelete.append(f)
        elif(curyear - fyear == 10):
            if (fmonth <= curmonth):
                filesToDelete.append(f)
        else:
            "Do nothing"

        cnt += 1
        pcnt = int(cnt / len(file_list) * 100)
        sys.stdout.write(f"\r")
        sys.stdout.write(f"{folderPath} {pcnt}% of {len(file_list)}")
        sys.stdout.flush()

    if len(filesToDelete) > 0:
        Logger.writeLogInfo("Deleting old files...")

        with open(DelFilePath, 'a') as file:

            for f in filesToDelete:
                if ext_mask in f:
                    time_now = datetime.fromtimestamp(time.time())
                    file.write(f"{time_now} {f} {datetime.fromtimestamp(os.path.getmtime(f)).month} {datetime.fromtimestamp(os.path.getmtime(f)).year}\n")
                    os.remove(f)

        Logger.writeLogInfo(f"Deleted {len(filesToDelete)} files")
    else:
        Logger.writeLogInfo(f"{len(file_list)} files checked. No files to delete in {folderPath}")
    print("")
# endregion

log_file_cnt.append(f"Program end......... {datetime.fromtimestamp(time.time())}")
Logger.writeLog()


