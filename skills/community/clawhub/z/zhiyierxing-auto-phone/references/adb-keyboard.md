# ADB Keyboard

## Why it is needed
Android `adb shell input text` is poor for Unicode and Chinese text input. ADB Keyboard solves that by receiving broadcast intents.

## Repo
- `https://github.com/senzhk/ADBKeyBoard`

## Install options
### Use APK
- Stable release example: `https://github.com/senzhk/ADBKeyBoard/releases/download/v2.4-dev/keyboardservice-debug.apk`
- Newer A16-fix example: `https://github.com/senzhk/ADBKeyBoard/releases/download/v2.5-dev/keyboardservice-debug.apk`
- Older APK path: `https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk`

### Build from source
```bash
git clone https://github.com/senzhk/ADBKeyBoard.git
cd ADBKeyBoard
export ANDROID_HOME=$HOME/Android/Sdk
./gradlew installDebug
```

## Enable it
```bash
adb shell ime enable com.android.adbkeyboard/.AdbIME
adb shell ime set com.android.adbkeyboard/.AdbIME
```

## Check available IMEs
```bash
adb shell ime list -a
```

## Reset to default keyboard
```bash
adb shell ime reset
```

## Common fix
If typing does not work, re-run enable + set commands, then retry the task.
