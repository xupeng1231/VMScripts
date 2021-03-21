import os
import time
import random
import sys
import traceback
import shutil

from CloseAcrobatAlert import close_acrobat_alert


base_dir = 'C:\\Users\\Vulnerability\\Desktop\\AbstractFuzz\\'
script_dir_path = os.path.join(base_dir, 'scripts')
flag_dir = os.path.join(base_dir, 'scripts', 'alive_flag')
if not os.path.exists(flag_dir):
    os.mkdir(flag_dir)
fuzz_alive_flag_path = os.path.join(base_dir, 'scripts', 'alive_flag', 'vm_fuzz.alive.flag')


sample_dir = 'Z:\\samples'
crash_dir = 'Z:\\crashes'



base_dir = 'C:\\Users\\Vulnerability\\Desktop\\AbstractFuzz\\'

windbg_path = 'C:\\Program Files (x86)\\Windows Kits\\10\\Debuggers\\x86\\windbg.exe'
acrord32_exe_path = 'C:\\\\Program Files (x86)\\\\Adobe\\\\Acrobat Reader DC\\\\Reader\\\\Acrord32.exe'
foxit_exe_path = 'C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe'
wps_exe_path = 'C:\Users\Vulnerability\AppData\Local\kingsoft\WPS Office\ksolaunch.exe'
windbg_script_path = os.path.join(base_dir, 'scripts', 'windbg.py')
windbg_all_process_script_path = os.path.join(base_dir, 'scripts', 'windbg_all_process.py')
flag_path = os.path.join(base_dir, 'crash.flag')
tmp_sample_path = os.path.join(base_dir, 'tmp_sample.pdf')

# tmp_dir = 'C:\\Users\\Vulnerability\\Desktop\\AbstractFuzz\\tmp'

min_wait_secs = 40
max_wait_secs = 120


def log(s):
    with open('log_fuzz.txt', 'ab') as out_fd:
        out_str = time.strftime('%y_%m_%d %H:%M:%S : ')+s
        out_fd.write(out_str)
        print out_str


def main():
    while True:
        try:
            sample_test()
        except Exception as e:
            log(str(e)+'\n'+traceback.format_exc())
            time.sleep(5)


def sample_test():
    # create alive flag file
    if not os.path.exists(fuzz_alive_flag_path):
        for _ in range(3):
            try:
                with open(fuzz_alive_flag_path, 'wb') as alive_fd:
                    pass
            except:
                log('ERROR, %dst time(all: 3) create alive_flag failed.'%_)
                time.sleep(_+1)
            else:
                break
    sys.stdout.flush()
    # exam sample dir and crash dir
    if not os.path.exists(sample_dir) or not os.path.exists(crash_dir):
        log('WARNING, samples dir or crashes dir don\'t found, will sleep 20 seconds.')
        time.sleep(20)
        return
    # get all valid samples
    samples = [c for c in os.listdir(sample_dir) if c.endswith('.pdf') and time.time()-os.path.getmtime(os.path.join(sample_dir, c))>30 and os.path.getsize(os.path.join(sample_dir, c))>1]
    if len(samples) == 0:
        log('sample dir is empty, will sleep 3 minute.')
        time.sleep(180)
        log('awake.')
        return

    # delete crash flag file
    if os.path.exists(flag_path):
        for _ in range(3):
            try:
                os.remove(flag_path)
            except:
                log('ERROR, %dst time(all:3) remove flag file failed.'%_)
                time.sleep(2)
            else:
                break

    # random choose one sample to test
    samplename = random.choice(samples)
    sample_path = os.path.join(sample_dir, samplename)
    for _ in range(3):
        try:
            if os.path.exists(tmp_sample_path):
                os.remove(tmp_sample_path)
            shutil.copy(sample_path, tmp_sample_path)
            break
        except Exception as excep:
            print 'Exception:', excep
            log('{}st time ERROR, remove and copy tmp_sample failed'.format(str(_)))
            print '{}st time ERROR, remove and copy tmp_sample failed'.format(str(_))
            if _ == 2:
                return
            time.sleep(2*(_+1))
    log('testing ' + sample_path)
    exist_log_paths = []
    adobe_log_path = os.path.join(os.path.dirname(sample_path), '{sample_name}.adobe.log.txt'.format(sample_name=samplename))
    foxit_log_path = os.path.join(os.path.dirname(sample_path), '{sample_name}.foxit.log.txt'.format(sample_name=samplename))
    wps_log_path = os.path.join(os.path.dirname(sample_path), '{sample_name}.wps.log.txt'.format(sample_name=samplename))
    adobe_cmd = 'start "" "{windbg_path}"  -c ".load pykd;!py ' \
          '{windbg_script_path} {flag_path} {log_path}" -o' \
          ' "{acrord32_exe_path}" "{pdf_path}"'.format(
            windbg_path=windbg_path, windbg_script_path=windbg_script_path,
            flag_path=flag_path, log_path=adobe_log_path, acrord32_exe_path=acrord32_exe_path,
            pdf_path=tmp_sample_path)
    foxit_cmd = 'start "" "{windbg_path}"  -c ".load pykd;!py ' \
          '{windbg_all_process_script_path} {flag_path} {log_path}" -o' \
          ' "{foxit_exe_path}" "{pdf_path}"'.format(
             windbg_path=windbg_path, windbg_all_process_script_path=windbg_script_path,
            flag_path=flag_path, log_path=foxit_log_path, foxit_exe_path=foxit_exe_path,
            pdf_path=tmp_sample_path)
    wps_cmd = 'start "" "{windbg_path}"  -c ".load pykd;!py ' \
                '{windbg_all_process_script_path} {flag_path} {log_path}" -o' \
                ' "{wps_exe_path}" "{pdf_path}"'.format(
        windbg_path=windbg_path, windbg_all_process_script_path=windbg_script_path,
        flag_path=flag_path, log_path=wps_log_path, wps_exe_path=wps_exe_path,
        pdf_path=tmp_sample_path)
    # cmds = (adobe_cmd, foxit_cmd, wps_cmd)
    # cmd_names = ('adobe', 'foxit', 'wps')
    # cmds = (adobe_cmd, )
    # cmd_names = ('adobe', )
    # for i in range(len(cmds)):
    #     cmd, cmdname = cmds[i], cmd_names[i]
    for _ in range(3):
        res = os.system(adobe_cmd)
        # res = os.system(foxit_cmd)
        if 0 == res:
            time.sleep(1)
            break
        else:
            log('ERROR, %dst time(all:3) start %s failed.'%(_, 'adobe'))
            time.sleep(2*(_+1))
    # sleep wait_secs seconds
    wait_start_time = time.time()
    while True:
        jswindow_exist = close_acrobat_alert()
        if time.time()-wait_start_time > max_wait_secs:
            break
        time.sleep(0.1)
    # kill windbg process
    for _ in range(3):
        res = os.system('taskkill /F /IM windbg.exe')
        if 0 == res:
            break
        else:
            log('ERROR, %dst time(all:3) stop windbg process failed.')
            time.sleep(2*(_+1))

    time.sleep(2)
    # exam all the log files.
    log_paths = (adobe_log_path, foxit_log_path, wps_log_path)
    for log_path in log_paths:
        if os.path.exists(log_path):
            exist_log_paths.append(log_path)

    # test if the sample crash the application
    if os.path.exists(flag_path) or len(exist_log_paths)>0:
        for _ in range(3):
            try:
                shutil.move(sample_path, os.path.join(crash_dir, samplename))
                time.sleep(1)
            except:
                log('ERROR, %d time(all:3) move sample to crash dir failed.%s,%s'%(_, sample_path, os.path.join(crash_dir, samplename)))
                time.sleep(2*(_+1))
            else:
                break
        for log_path in exist_log_paths:
            for _ in range(3):
                try:
                    shutil.move(log_path, os.path.join(crash_dir, os.path.basename(log_path)))
                    time.sleep(1)
                except:
                    log('ERROR, %d time(all:3) move log(%s) to crash dir failed.' % (_, log_path))
                    time.sleep(2*(_+1))
                else:
                    break

    # remove the sample
    if os.path.exists(sample_path):
        for _ in range(3):
            try:
                os.remove(sample_path)
            except:
                log('ERROR, %d time(all:3) remove %s failed.'%(_, sample_path))
                time.sleep(2*(_+1))
            else:
                break


if __name__ == '__main__':
    main()
