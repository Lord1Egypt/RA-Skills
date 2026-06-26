---
name: weapp-automatd-testing
description: WeChat Mini Program automation testing toolkit. Supports launching DevTools, page navigation, element interaction, screenshots, console log reading, and more. Use when the user needs to automate mini program testing, control WeChat DevTools, read console logs, or perform UI screenshot comparison.
---

# WeChat Mini Program Automation Testing

## CRITICAL: Batch Execution Rule

**ALWAYS write a single Python script that uses `WeappTestRunner` to batch ALL operations, then execute it with ONE `python` call.**

Each tool call costs ~30-60s overhead. A test with 10 individual CLI calls takes 5-15 minutes; the same 10 operations batched into one script take ~5 seconds.

### Execution pattern

1. **Plan** all operations the user needs
2. **Write** a single Python script using `WeappTestRunner`
3. **Run** with one `python` command
4. **Read** output and report results

### Example

```python
import sys
sys.path.insert(0, r"path_to_weapp-automation_skill\scripts")
from weapp_automation import AutomationConfig, WeappTestRunner

config = AutomationConfig(
    project_path=r"path_to_your_miniapp\my_mini_app",
    ws_endpoint="ws://localhost:9420"
)

runner = WeappTestRunner(config)
results = (runner
    .navigate("pages/index/index")
    .wait(2)
    .screenshot("home.png")
    .click(".category-item")
    .wait(1)
    .screenshot("after_click.png")
    .get_results())

print(runner.get_summary())
for r in results:
    print(r)
```

Save as a `.py` file and run with `python script.py`.

---

## Prerequisites

1. Install: `npm install -g miniprogram-automator`
2. Open WeChat DevTools -> Settings -> Security Settings -> Enable "Service Port"
3. Ensure the project is imported into DevTools

CLI paths:
- **macOS**: `/Applications/wechatwebdevtools.app/Contents/MacOS/cli`
- **Windows**: `C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat`

---

## WeappTestRunner Chainable Methods

| Method | Description |
|--------|-------------|
| `.navigate(page_path)` | Navigate to a page |
| `.click(selector)` | Tap an element |
| `.input(selector, text)` | Type text into an input field |
| `.screenshot(filename)` | Take a screenshot |
| `.scroll(selector, direction, distance)` | Scroll an element |
| `.get_wxml(selector)` | Extract WXML DOM structure |
| `.get_data(path)` | Read page data |
| `.wait(seconds)` | Wait for a duration |
| `.run()` | Execute all queued steps |
| `.get_results()` | Execute and return results list |
| `.get_summary()` | Return pass/fail summary dict |

---

## Other APIs

- **WeappAutomation** - Single-step API for one-off operations
- **WeappLauncher** - Launch/close WeChat DevTools
- **ConsoleReader** - Read and analyze console logs
- **PerformanceMonitor** - Collect performance metrics
- **TestScenarios** - Pre-built test scenario templates (smoke, navigation, form, UI regression, user journey)

For detailed usage, parameters, and examples of all APIs, see [references/api_reference.md](references/api_reference.md).

---

## Script Inventory

| Script | Purpose |
|--------|---------|
| `scripts/weapp_launcher.py` | Launch/close WeChat DevTools |
| `scripts/weapp_automation.py` | Core automation engine (batch + single-step) |
| `scripts/console_reader.py` | Console log reading and analysis |
| `scripts/test_scenarios.py` | Pre-defined test scenario templates |
