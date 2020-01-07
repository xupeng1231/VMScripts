import pykd
import os
import time
import shutil
import sys
import datetime
from subprocess import Popen,call
import traceback
import re

def log(log_str):
    with open("p.log", "at") as log:
        log.write("{}\t{}\n\n".format(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"), log_str))

# !py windbg.py file_name base_dir

# this script run most 20 seconds
enter_time = time.time()
expire_time = enter_time + 30

flag_path = sys.argv[1]
log_path = sys.argv[2]

e = pykd.dbgCommand


def save_sample(who_find):
    global flag_path
    # saving crash flag.
    for _ in range(3):
        try:
            with open(flag_path, 'wb') as flag_fd:
                pass
        except:
            log("ERROE:create flag error!")
            pass
        else:
            break

    # log
    for _ in range(3):
        try:
            log( str(who_find)+" FIND VULNERABILITY!!!"+"#"*64+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
            log(log_path)
        except:
            pass
        else:
            break


    # save a log file about this crash sample
    try:
        logf=open(log_path, "wt")
        logf.write("*"*40+".lastevent"+"*"*40+"\n"*2)
        logf.write(e(".lastevent")+"\n"*4)
        logf.write("*"*40+"r"+"*"*40+"\n"*2)
        logf.write(e("r")+"\n"*4)
        logf.write("*"*40+"u "+"*"*40+"\n"*2)
        logf.write(e("u")+"\n"*4)
        logf.write("*"*40+"ub"+"*"*40+"\n"*2)
        logf.write(e("ub eip")+"\n"*4)
        logf.write("*"*40+"callstack"+"*"*40+"\n"*2)
        logf.write(e("kv")+"\n"*4)
        logf.write("*" * 40 + "lm" + "*" * 40 + "\n" * 2)
        logf.write(e("lm") + "\n" * 4)
        logf.close()
    except:
        log("ERROE:crashlog create error!")
        pass

while True:
    # check if expiration time arrived.
    if time.time() > expire_time:
        break

    try:
        # only fuzz 1 process
        # if 1 != pykd.getCurrentProcessId():
        #     e("g")
        #     continue

        # sxd some breakpoint, and go;
        res_g=e("sxd cpr;sxd ld;sxd ct;sxd et;g")

        # get some information
        lastevent = e(".lastevent")
        r = e("r")
        kl2 = e("k L2")

        # see if any crash
        # if break at verifier!VerifierStopMessage, maybe a page heap crash occur.
        if kl2.find("verifier!VerifierStopMessage") >= 0:
            save_sample(lastevent)
            break
        # filter some normal breakpoint, otherwise will be treated as a crash.
        if lastevent.find("Break instruction exception") > 0 or lastevent.find("Exit process") > 0 or r.find("ntdll!KiFastSystemCallRet") > 0:
            continue
        elif lastevent.find("Unknown exception") > 0:
            continue
        else:
            save_sample(lastevent)
            break
    except :
        pass