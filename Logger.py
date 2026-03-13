from Constants import *
from datetime import datetime
import time
import socket

log_file_cnt = [] # log file content

class Logger:

    @staticmethod
    def writeLog():
        with open(log_file, 'a') as file:
            for f in log_file_cnt:
                file.write(f"{f}\n")

    @staticmethod
    def writeLogErr(msg):
        log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} ERR: {msg}")

    @staticmethod
    def writeLogInfo(msg):
        log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} INFO: {msg}")

    @staticmethod
    def writeLogWarn(msg):
        log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} WARN: {msg}")

    @staticmethod
    def writeLogTrace(isTrue, msg):
        if isTrue:
            log_file_cnt.append(f"{datetime.fromtimestamp(time.time())} TRACE: {msg}")

    @staticmethod
    def clearLog():
        log_file_cnt.clear()