# Runbook

## Minimal working Android path
1. Confirm `adb version`
2. Confirm `adb devices` shows a `device`
3. Install ADB Keyboard APK
4. Enable it:
   - `adb shell ime enable com.android.adbkeyboard/.AdbIME`
   - `adb shell ime set com.android.adbkeyboard/.AdbIME`
5. Create and activate a repo-local virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
6. Install project deps inside `.venv`:
   - `pip install -r requirements.txt`
   - `pip install -e .`
7. Start or point to a model server
8. Run from `.venv`:
   - `python main.py --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" "打开美团搜索附近的火锅店"`
9. If it fails, run deployment check script and inspect the error

## What to tell the user when something fails
- Device missing: check cable, authorization prompt, USB debugging, restart adb
- Text input broken: re-enable ADB Keyboard
- Model failing: confirm endpoint, model name, API key, server health
- Command waiting forever: use a direct task string or a TTY
- Sensitive screen reached: request takeover
