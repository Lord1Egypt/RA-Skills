---
name: pyautogui-controller
description: Advanced Windows desktop/browser automation via a local Python controller project. Use when the user wants natural-language UI automation on this machine: screenshots, opening apps, browser navigation, clicking inputs/buttons, typing text, and simple multi-step desktop workflows. Prefer built-in browser/web tools for normal web tasks; use this skill when direct screen/desktop control is required.
metadata: { "openclaw": { "emoji": "🤖", "os": ["win32"], "requires": { "anyBins": ["python", "python3"] } } }
---

# PyAutoGUI Controller

Use this skill when the user needs **local desktop automation on this Windows machine** and normal browser tools are not enough.

## Use for

- Open desktop apps and interact with their windows
- Take screenshots
- Type Chinese/English text into native apps
- Click buttons/inputs on screen
- Run short natural-language automation commands through the local controller
- Browser actions that require screen-based control instead of DOM/web APIs

## Avoid for

- Normal web reading/searching → use `web_fetch`, `browser`, or search skills
- Mobile automation
- High-assurance unattended long workflows

## Project location

The controller project lives at:

`C:\Users\dev\Desktop\昱昱\skills\pyautogui-controller`

## Primary invocation

Run the local controller through the wrapper script:

```powershell
python {baseDir}\scripts\run_controller.py "打开记事本，然后输入 '你好'"
```

The wrapper calls the real project entrypoint:

`C:\Users\dev\Desktop\昱昱\skills\pyautogui-controller\main.py`

## Recommended workflow

1. Prefer a **single compound command** over multiple split commands
2. Start with simple actions
3. Inspect returned JSON for `success`, `results`, `runtime`, and `warnings`
4. If the command fails, simplify the wording and retry

## Good command examples

```powershell
python {baseDir}\scripts\run_controller.py "截图"
python {baseDir}\scripts\run_controller.py "打开记事本"
python {baseDir}\scripts\run_controller.py "打开浏览器访问 https://example.com"
python {baseDir}\scripts\run_controller.py "打开浏览器访问 file:///C:/path/test.html，然后在搜索框输入 'abc'，再点击发送按钮"
```

## Practical notes

- Compound commands are more reliable than split follow-ups
- OCR / DOM readiness may affect accuracy; check `warnings`
- Move the mouse to the top-left corner if PyAutoGUI fail-safe is triggered
- This skill is local-machine specific; it assumes the project path above exists
