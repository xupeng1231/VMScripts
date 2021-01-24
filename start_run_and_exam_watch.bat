set SCRIPT_DIR_PATH=C:\Users\Vulnerability\Desktop\AbstractFuzz\scripts
set LOG_FILE=%SCRIPT_DIR_PATH%\log_boot.txt

cd %SCRIPT_DIR_PATH%

:: timeout 30>nul
:: git pull
timeout 10>nul

start "fuzzer" python64  vm_fuzz.py

:Loop
    del alive_flag\vm_fuzz.alive.flag
    timeout 30>nul
    if exist repo_need_update.flag (
        del repo_need_update.flag
        goto :updaterepo
    )
    timeout 300>nul
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
    git pull
    timeout 5>nul
    start "fuzzer" python64 vm_fuzz.py
    exit /b /0

:restart
    shutdown /r /t 2
    exit /b 0