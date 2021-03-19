set SCRIPT_DIR_PATH=C:\Users\Vulnerability\Desktop\AbstractFuzz\scripts
set LOG_FILE=%SCRIPT_DIR_PATH%\log_boot.txt
set SHARED_SCRIPTS=Z:\scripts

cd %SCRIPT_DIR_PATH%

:: timeout 30>nul
:: git pull
call:sleep10s

z:\\scripts\\clear_disk.bat

::start "closer" python64 CloseAcrobatAlert.py
::call:sleep5s
start "fuzzer" python64  vm_fuzz.py

:Loop
    del alive_flag\vm_fuzz.alive.flag
    call:sleep60s
    if exist repo_need_update.flag (
        del repo_need_update.flag
        call:updaterepo
    )
    call:sleep300s
    if not exist alive_flag\vm_fuzz.alive.flag (
        echo %date% %time%, the vm_fuzz.py maybe zobie, will restart vm. >> %LOG_FILE%
        goto :restart
    )
    goto :Loop

exit /b 0

:updaterepo
    taskkill /F /IM python64.exe
    taskkill /F /IM windbg.exe
    taskkill /F /IM python64.exe
    taskkill /F /IM windbg.exe
    copy /Y %SHARED_SCRIPTS%\* .\
    ::call:sleep5s
    ::start "closer" python64 CloseAcrobatAlert.py
    call:sleep5s
    start "fuzzer" python64 vm_fuzz.py
    goto:eof

:sleep5s
    python64 -c "import time;time.sleep(5);"
    goto:eof

:sleep10s
    python64 -c "import time;time.sleep(10);"
    goto:eof

:sleep60s
    python64 -c "import time;time.sleep(60);"
    goto:eof

:sleep300s
    python64 -c "import time;time.sleep(300);"
    goto:eof

:restart
    shutdown /r /t 2
    exit /b 0