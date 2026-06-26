# WeChat Mini Program Automation Testing API Reference

## Table of Contents

1. [Launcher API](#launcher-api)
2. [Automation API](#automation-api)
3. [Console Reader API](#console-reader-api)
4. [Test Scenarios API](#test-scenarios-api)

---

## Launcher API

### WeappLauncher Class

Used to launch and control the WeChat Developer Tools.

#### Initialization

```python
from weapp_launcher import WeappLauncher

# macOS
launcher = WeappLauncher(cli_path="/Applications/wechatwebdevtools.app/Contents/MacOS/cli")

# Windows
launcher = WeappLauncher(cli_path=r"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat")
```

#### Methods

##### open_project(project_path, auto_preview=False)

Open a mini program project.

**Parameters:**
- `project_path` (str): Root directory path of the mini program project
- `auto_preview` (bool): Whether to automatically open preview

**Returns:**
```python
{
    "success": True,
    "stdout": "...",
    "stderr": "..."
}
```

##### close_project(project_path)

Close a mini program project.

##### quit_wechatdevtools()

Quit the WeChat Developer Tools.

##### auto_test(project_path, test_script_path)

Execute an automation test script.

##### is_running()

Check if the Developer Tools are running.

---

## Automation API

### AutomationConfig Configuration Class

```python
from weapp_automation import AutomationConfig

config = AutomationConfig(
    project_path="/path/to/miniprogram",
    cli_path="/Applications/wechatwebdevtools.app/Contents/MacOS/cli",
    screenshot_dir="./screenshots",
    timeout=30,
    ws_endpoint="ws://localhost:9420"  # Optional: custom WebSocket port
)
```

### WeappAutomation Class

Core automation control class.

#### navigate_to(page_path)

Navigate to a specified page.

```python
automation = WeappAutomation(config)
result = automation.navigate_to("pages/index/index")
```

#### click(selector, page="pages/index/index")

Click an element.

```python
result = automation.click(".button-class")
result = automation.click("#submit-btn", "pages/form/form")
```

#### input_text(selector, text, page="pages/index/index")

Enter text in an input field.

```python
result = automation.input_text("input[name='username']", "testuser")
```

#### screenshot(filename=None, page="pages/index/index")

Take a screenshot.

```python
result = automation.screenshot("home.png")
# Or auto-generate filename
result = automation.screenshot()
```

#### get_element_text(selector, page="pages/index/index")

Get element text.

```python
result = automation.get_element_text(".title")
print(result["data"]["text"])
```

#### scroll(selector, direction="down", distance=300, page="pages/index/index")

Scroll an element.

```python
result = automation.scroll(".scroll-view", "down", 500)
```

### WeappTestRunner Class

Chainable test runner.

```python
from weapp_automation import WeappTestRunner

runner = WeappTestRunner(config)

result = (runner
    .navigate("pages/index/index")
    .click(".button")
    .input("input[name='search']", "keyword")
    .screenshot("search_result.png")
    .get_results())

summary = runner.get_summary()
print(f"Pass rate: {summary['success_rate'] * 100}%")
```

---

## Console Reader API

### ConsoleReader Class

Read and analyze console logs.

```python
from console_reader import ConsoleReader, LogLevel

reader = ConsoleReader("/path/to/project")

# Read logs
logs = reader.read_logs_from_script()

# Filter errors
errors = reader.filter_logs(LogLevel.ERROR)

# Export report
reader.export_to_markdown("logs_report.md")
```

#### Methods

##### filter_logs(level=LogLevel.ALL, pattern=None)

Filter logs.

```python
# Get errors only
errors = reader.filter_logs(LogLevel.ERROR)

# Search for specific content
logs = reader.filter_logs(pattern="network")
```

##### get_errors()

Get all error logs.

##### get_warnings()

Get all warning logs.

##### export_to_json(filepath, level=LogLevel.ALL)

Export to JSON format.

##### export_to_markdown(filepath, level=LogLevel.ALL)

Export to Markdown format.

### PerformanceMonitor Class

Performance monitoring.

```python
from console_reader import PerformanceMonitor

monitor = PerformanceMonitor("/path/to/project")
metrics = monitor.collect_metrics()
monitor.export_report("performance_report.json")
```

---

## Test Scenarios API

### TestScenarios Class

Predefined test scenarios.

```python
from test_scenarios import TestScenarios

scenarios = TestScenarios("/path/to/project")
```

#### smoke_test()

Smoke test.

```python
result = scenarios.smoke_test()
```

#### navigation_flow_test(pages)

Navigation flow test.

```python
result = scenarios.navigation_flow_test([
    "pages/index/index",
    "pages/category/category",
    "pages/detail/detail"
])
```

#### form_submission_test(form_data)

Form submission test.

```python
result = scenarios.form_submission_test({
    "input[name='username']": "testuser",
    "input[name='password']": "testpass"
})
```

#### ui_regression_test(pages, baseline_dir="./baseline")

UI regression test.

```python
result = scenarios.ui_regression_test([
    "pages/index/index",
    "pages/profile/profile"
])
```

#### scroll_performance_test(page, scroll_element, scrolls=5)

Scroll performance test.

```python
result = scenarios.scroll_performance_test(
    "pages/list/list",
    ".scroll-view",
    scrolls=10
)
```

#### user_journey_test(steps)

User journey test.

```python
steps = [
    {"action": "navigate", "page": "pages/index/index"},
    {"action": "click", "selector": ".product"},
    {"action": "click", "selector": ".add-to-cart"},
    {"action": "navigate", "page": "pages/cart/cart"},
    {"action": "screenshot", "filename": "cart.png"}
]
result = scenarios.user_journey_test(steps)
```

---

## Command Line Usage

### Launcher

```bash
python weapp_launcher.py --project /path/to/miniprogram --action open
python weapp_launcher.py --project /path/to/miniprogram --action close
python weapp_launcher.py --project /path/to/miniprogram --action quit
```

### Automation

```bash
# Navigate
python weapp_automation.py --project /path/to/miniprogram --action navigate --page pages/index/index

# Click
python weapp_automation.py --project /path/to/miniprogram --action click --selector ".button"

# Input
python weapp_automation.py --project /path/to/miniprogram --action input --selector "input" --text "hello"

# Screenshot
python weapp_automation.py --project /path/to/miniprogram --action screenshot --filename test.png

# Scroll
python weapp_automation.py --project /path/to/miniprogram --action scroll --selector ".scroll-view" --direction down --distance 500
```

### Console Reader

```bash
# Read logs
python console_reader.py --project /path/to/miniprogram --action read

# View errors
python console_reader.py --project /path/to/miniprogram --action errors

# Export report
python console_reader.py --project /path/to/miniprogram --action export --format markdown --output report.md
```

### Test Scenarios

```bash
# Smoke test
python test_scenarios.py --project /path/to/miniprogram --scenario smoke

# Navigation test
python test_scenarios.py --project /path/to/miniprogram --scenario navigation --pages "pages/index/index,pages/about/about"

# UI regression test
python test_scenarios.py --project /path/to/miniprogram --scenario ui --pages "pages/index/index,pages/profile/profile"
```

---

## Notes

1. **Dependency Installation**: Install `miniprogram-automator` before use
   ```bash
   npm install miniprogram-automator
   ```

2. **Developer Tools Settings**:
   - Enable "Service Port": Settings -> Security Settings -> Service Port
   - Ensure the project has been imported into the Developer Tools

3. **Selector Syntax**:
   - `.class` - Class selector
   - `#id` - ID selector
   - `tag` - Tag selector
   - `[attr=value]` - Attribute selector

4. **Screenshot Directory**: Saved to `./screenshots` by default, configurable

---

## Troubleshooting

### Connection refused (`ECONNREFUSED`)

1. Confirm DevTools is open and the project is loaded
2. Check that "Service Port" is enabled in Security Settings
3. Verify the WebSocket port matches (default: 9420)

### Element not found

1. Add `.wait(2)` before interacting with elements to ensure the page is loaded
2. Verify the selector is correct (use `.get_wxml("page")` to inspect DOM)
3. Confirm the element is visible on the current page

### Screenshot is empty or missing

1. Ensure `screenshot_dir` exists and is writable
2. Add `.wait(1)` before screenshot to ensure rendering is complete
