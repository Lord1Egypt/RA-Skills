# macOS API Reference

## xlwings — Excel for Mac

```python
import xlwings as xw

# 打开工作簿
app = xw.App(visible=False)
wb = app.books.open("/path/to/file.xlsx")
ws = wb.sheets.active              # 活动工作表
ws = wb.sheets["Sheet1"]           # 按名称
ws = wb.sheets[0]                  # 按索引（0-based）

# 读取数据
data = ws.used_range.value         # list of lists
cell = ws["A1"].value
range_data = ws["A1:D10"].value

# 写入
ws["A1"].value = "Hello"
ws["A1:B2"].value = [[1, 2], [3, 4]]

# 关闭
wb.save()
wb.close()
app.quit()
```

---

## AppleScript — 系统原生控制

```applescript
-- 读取 Excel 数据
tell application "Microsoft Excel"
    open "/path/to/file.xlsx"
    set ws to sheet "Sheet1" of active workbook
    set cellValue to value of cell "A1" of ws
    set rangeData to value of used range of ws
    close active workbook saving no
    return rangeData
end tell
```

### Python 调用 AppleScript

```python
import subprocess

def run_applescript(script: str) -> str:
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"AppleScript error: {result.stderr}")
    return result.stdout.strip()
```

---

## JXA (JavaScript for Automation)

```javascript
// 更现代的 macOS 自动化方式
const excel = Application('Microsoft Excel');
excel.includeStandardAdditions = true;

const wb = excel.open(Path('/path/to/file.xlsx'));
const ws = wb.sheets['Sheet1'];
const data = ws.usedRange.value();
excel.close(wb, {saving: 'no'});
```

```python
import subprocess, json

def run_jxa(script: str):
    result = subprocess.run(
        ['osascript', '-l', 'JavaScript', '-e', script],
        capture_output=True, text=True
    )
    return result.stdout.strip()
```

---

## 权限处理

首次运行 AppleScript/xlwings 控制 Excel 时，macOS 会弹出权限请求。

**手动开启：**
- 系统设置 → 隐私与安全性 → 辅助功能 → 开启终端/Python
- 系统设置 → 隐私与安全性 → 自动化 → 允许控制 Microsoft Excel

**检测是否有权限：**
```python
import subprocess
result = subprocess.run(
    ['osascript', '-e', 'tell application "System Events" to return name of first process'],
    capture_output=True, text=True
)
if result.returncode != 0:
    print("⚠️ 需要辅助功能权限，请在系统设置中开启")
```

---

## 常见问题

| 问题 | 解决方案 |
|---|---|
| `xlwings` 无法连接 Excel | 确认 Excel for Mac 已安装并运行过一次 |
| AppleScript 超时 | 增加 `timeout` 参数，大文件使用 `openpyxl` 离线读取 |
| 权限拒绝 | 在「隐私与安全性」中手动授权 |
| `.numbers` 文件 | 使用 `libreoffice --convert-to xlsx` 先转换 |
