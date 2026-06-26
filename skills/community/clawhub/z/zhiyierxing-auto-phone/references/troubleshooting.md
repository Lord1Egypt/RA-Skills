# Troubleshooting

## If the repo won't clone or update
- confirm `git` is installed
- confirm network access to GitHub
- if the local repo already exists and contains the required files, continue from the local repo when the failure is only a transient network/update issue
- otherwise retry the repo command after the network issue is resolved

## If adb sees no device
Tell the user to:
1. use a data-capable cable
2. unlock the phone
3. accept the USB debugging popup
4. restart adb

macOS / Linux:
```bash
adb kill-server
adb start-server
adb devices
```

Windows PowerShell:
```powershell
adb kill-server
adb start-server
adb devices
```

## If typing fails on Android
Tell the user to:
1. install ADB Keyboard
2. enable it in system input settings
3. run:
```bash
adb shell ime enable com.android.adbkeyboard/.AdbIME
adb shell ime set com.android.adbkeyboard/.AdbIME
```
4. retry the task

## If dependency installation fails
Tell the user to verify:
- the selected Python runtime is at least 3.10
- `.venv` was created with that suitable Python runtime
- the repo requirements are compatible with the selected interpreter

## If the model check fails
Tell the user to verify:
- `.venv` is activated
- `base-url`
- `model`
- API key
- server is running
- endpoint is OpenAI-compatible

## If the agent gets stuck on login, captcha, or payment
Stop and request takeover.
Do not try to bypass the step.

## If screenshots are black
Treat it as a sensitive screen and request takeover.

## If interactive mode errors with EOF
Tell the user to activate `.venv` first, then run with a direct task string or use a real TTY terminal.
Use the host-appropriate activation command on Windows vs macOS/Linux.

## Response pattern
When a problem appears, answer with:
- the likely cause
- whether `.venv` is involved
- the exact fix
- the exact command if one exists
