from Logger import *
import os
from VersionControl import *

class Config:

    def __init__(self, cfg_file):
        self.tester = None
        self.trace = 0
        self.verified_report_folders = []  # folder list that actually present
        self.__report_folders = []  # folder list in ini file

        try:
            if not os.path.exists(cfg_file):
                raise FileNotFoundError(None)
        except FileNotFoundError:
            Logger.writeLogErr(f"config.ini not found")
            Logger.writeLog()

        with open(cfg_file) as f:
         config_lines = f.read().splitlines()

        for line in config_lines:
            if line.startswith("#"):
                continue

            split_line = line.split("=")
            match split_line[0]:
                case "Tester": self.tester = split_line[1]
                case "ReportFolder": self.__report_folders.append(split_line[1])
                case "Trace":
                    if(split_line[1] == "True"):
                        self.trace = 1
                case _: Logger.writeLogErr(f"Unknow config parameter {split_line[0]}")

        Logger.writeLogTrace(self.trace, f"Version: {version}")
        Logger.writeLogTrace(self.trace, f"Tester: {self.tester}")

        for line in self.__report_folders:
            if os.path.exists(line):
                Logger.writeLogTrace(self.trace, f"Config path found: {line}")
                self.verified_report_folders.append(line)
            else:
                Logger.writeLogErr(f"Config path not found {line}")
