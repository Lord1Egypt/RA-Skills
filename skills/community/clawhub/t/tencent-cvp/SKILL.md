---
name: tencent-cvp
description: "All-in-one Android phone automation via ADB: screen analysis, touch/input, foreground app detection, app install. Use for any task that involves operating the Android device."
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "os": ["linux", "darwin"],
        "requires": { "bins": ["adb"] },
      },
  }
---

# Tencent CVP — Cloud Virtual Phone Automation

Operate the Tencent Cloud Virtual Phone: observe the screen, interact with it, detect apps, and install new ones.

**Core loop: Observe -> Act -> Verify.** Always check the screen before and after actions.

---

## 1. Screen Analysis

### UI Layout Dump (preferred)

Structured XML with every element's text, coordinates, and properties. **Always try this first.**

```bash
adb shell uiautomator dump && adb shell cat /sdcard/window_dump.xml
```

Each XML `node` has:
- `text` — visible text
- `resource-id` — element identifier
- `class` — widget type (e.g. `android.widget.TextView`)
- `bounds` — coordinates as `[left,top][right,bottom]`
- `clickable`, `enabled`, `focused` — interaction state

Compute tap target from bounds: `x = (left + right) / 2`, `y = (top + bottom) / 2`.

### Screenshot (fallback only)

Use **only when uiautomator returns empty or partial XML** — common with games, video players, WebView, or custom-rendered surfaces.

```bash
adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png /tmp/screen.png
```

Then read `/tmp/screen.png` for visual analysis.

### Tips

- Wake screen first: `adb shell input keyevent KEYCODE_WAKEUP`
- Get resolution: `adb shell wm size`
- uiautomator dump takes ~1-2s; don't spam it.

---

## 2. Input and Interaction

### Touch

```bash
# Tap
adb shell input tap <x> <y>

# Long press (~1s)
adb shell input swipe <x> <y> <x> <y> 1000

# Swipe
adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms>
```

### Text Input

```bash
# ASCII only
adb shell input text "hello"
```

**CJK / Non-ASCII** — `input text` does not support Chinese. Use clipboard:

```bash
adb shell am broadcast -a clipper.set -e text "中文内容"
adb shell input keyevent KEYCODE_PASTE
```

### Key Events

```bash
adb shell input keyevent KEYCODE_HOME
adb shell input keyevent KEYCODE_BACK
adb shell input keyevent KEYCODE_ENTER
adb shell input keyevent KEYCODE_WAKEUP
adb shell input keyevent KEYCODE_POWER
adb shell input keyevent KEYCODE_APP_SWITCH
adb shell input keyevent KEYCODE_VOLUME_UP
adb shell input keyevent KEYCODE_VOLUME_DOWN
```

### Launch Apps

```bash
# By package + activity
adb shell am start -n <package>/<activity>

# By intent (open URL)
adb shell am start -a android.intent.action.VIEW -d "https://example.com"

# From launcher (package only)
adb shell monkey -p <package> -c android.intent.category.LAUNCHER 1
```

---

## 3. Foreground App Detection

```bash
adb shell dumpsys window | grep mCurrentFocus | grep -v null
```

Output example:

```
  mCurrentFocus=Window{abcdef0 u0 com.tencent.mm/com.tencent.mm.ui.LauncherUI}
```

**Output may be empty** — this happens when:
- Screen is off or locked
- System transition in progress
- No focused window (e.g. during boot)

When empty: wake screen (`KEYCODE_WAKEUP`), wait, retry. If still empty, use uiautomator dump.

### Common Package Names

| App | Package |
|-----|---------|
| Home/Launcher | `com.android.launcher` or vendor variant |
| Settings | `com.android.settings` |
| Chrome | `com.android.chrome` |
| WeChat | `com.tencent.mm` |
| Alipay | `com.eg.android.AlipayGphone` |
| Douyin | `com.ss.android.ugc.aweme` |
| Bilibili | `tv.danmaku.bili` |

---

## 4. App Install

**Priority: MyApp (应用宝) first**, then browser, then web search.

### Via MyApp (应用宝)

```bash
adb shell am start -a android.intent.action.VIEW -d "market://details?id=<package_name>" -p com.tencent.android.qqdownloader
```

Examples:

```bash
# WeChat
adb shell am start -a android.intent.action.VIEW -d "market://details?id=com.tencent.mm" -p com.tencent.android.qqdownloader

# Alipay
adb shell am start -a android.intent.action.VIEW -d "market://details?id=com.eg.android.AlipayGphone" -p com.tencent.android.qqdownloader
```

After opening:
1. Use uiautomator dump to verify the page loaded
2. Find and tap the install/download button
3. Wait for install, then verify

### Finding Package Names

If unknown, search the web for `<app name> android package name`. Common pattern: reverse domain (`com.company.appname`).

### When MyApp Fails

- Try browser: `adb shell am start -a android.intent.action.VIEW -d "https://official-site.com"`
- Last resort: web search for APK download
