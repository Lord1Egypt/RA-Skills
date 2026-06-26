# macOS API Reference

> macOS 下文件操作首选 **xlwings**（需安装 Excel for Mac），失败自动降级到 **openpyxl / python-docx**。
> `.numbers` 文件需先用 LibreOffice 或 Numbers 应用转换为 xlsx。

---

## 快速降级链

```
Excel (.xlsx/.xlsm)：  xlwings → openpyxl
Numbers (.numbers)：   LibreOffice 转换 → openpyxl
Word (.docx)：          python-docx
旧格式 (.doc/.wps)：   LibreOffice 转换 → python-docx
```

---

## xlwings — Excel for Mac

### 读取

```python
import xlwings as xw
from pathlib import Path

app = xw.App(visible=False)
try:
    wb = app.books.open(str(Path("data.xlsx").resolve()))

    # 按名称 / 索引（0-based）/ 活动表
    ws = wb.sheets["Sheet1"]
    ws = wb.sheets[0]
    ws = wb.sheets.active

    # 读取已用区域（返回 list of lists）
    data = ws.used_range.value
    # 注意：单行返回 list，多行返回 list of lists
    if data and not isinstance(data[0], list):
        data = [data]

    # 读取指定单元格 / 区域
    cell = ws["A1"].value
    rng  = ws["A1:D10"].value

    wb.close()
finally:
    app.quit()
```

### 写入

```python
app = xw.App(visible=False)
try:
    wb = app.books.open(str(Path("data.xlsx").resolve()))
    ws = wb.sheets[0]

    # 单元格写入
    ws["A1"].value = "标题"

    # 批量写入（传入 list of lists）
    ws["A2"].value = [["姓名", "分数"], ["Alice", 90], ["Bob", 85]]

    # DataFrame 写入
    import pandas as pd
    ws["A1"].options(pd.DataFrame, header=True, index=False).value = df

    wb.save()
    wb.close()
finally:
    app.quit()
```

### 安全封装（推荐用法）

```python
import contextlib
import xlwings as xw
from pathlib import Path

@contextlib.contextmanager
def xlwings_session(filepath: str):
    """xlwings 安全会话，退出时自动 quit。"""
    app = xw.App(visible=False)
    wb  = None
    try:
        wb = app.books.open(str(Path(filepath).resolve()))
        yield wb
    finally:
        if wb:
            wb.close()
        app.quit()

# 用法
with xlwings_session("data.xlsx") as wb:
    ws = wb.sheets[0]
    data = ws.used_range.value
```

### xlwings → openpyxl 自动降级

```python
from pathlib import Path

def read_excel_mac(filepath: str, sheet_name: str = None) -> dict:
    result = {}

    # 优先 xlwings
    try:
        import xlwings as xw
        app = xw.App(visible=False)
        try:
            wb = app.books.open(str(Path(filepath).resolve()))
            sheets = [wb.sheets[sheet_name]] if sheet_name else wb.sheets
            for ws in sheets:
                data = ws.used_range.value or []
                result[ws.name] = data if isinstance(data[0], list) else [data]
            wb.close()
            return result
        finally:
            app.quit()
    except Exception as e:
        print(f"xlwings 失败（{e}），切换 openpyxl")

    # 降级 openpyxl
    import openpyxl
    wb = openpyxl.load_workbook(filepath, data_only=True)
    sheets = [wb[sheet_name]] if sheet_name else wb.worksheets
    for ws in sheets:
        result[ws.title] = [list(row) for row in ws.iter_rows(values_only=True)]
    wb.close()
    return result
```

---

## AppleScript — 系统原生控制

```applescript
-- 读取 Excel 数据
tell application "Microsoft Excel"
    open "/Users/me/data.xlsx"
    set ws to sheet "Sheet1" of active workbook
    set rangeData to value of used range of ws
    close active workbook saving no
    return rangeData
end tell
```

### Python 调用 AppleScript

```python
import subprocess

def run_applescript(script: str, timeout: int = 60) -> str:
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(f"AppleScript 执行失败: {result.stderr.strip()}")
    return result.stdout.strip()

# 示例：获取活动工作表名称
sheet_name = run_applescript('''
    tell application "Microsoft Excel"
        return name of active sheet of active workbook
    end tell
''')
```

---

## JXA (JavaScript for Automation)

更现代的 macOS 自动化方式，语法接近 JavaScript：

```javascript
// 读取 Excel 数据
const excel = Application('Microsoft Excel');
excel.includeStandardAdditions = true;
const wb = excel.open(Path('/Users/me/data.xlsx'));
const ws = wb.sheets['Sheet1'];
const data = ws.usedRange.value();
excel.close(wb, { saving: 'no' });
```

```python
import subprocess

def run_jxa(script: str, timeout: int = 60) -> str:
    result = subprocess.run(
        ['osascript', '-l', 'JavaScript', '-e', script],
        capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(f"JXA 执行失败: {result.stderr.strip()}")
    return result.stdout.strip()
```

---

## Numbers / .numbers 文件处理

macOS Numbers 文件无法直接用 Python 读取，需先转换：

```bash
# 方案 A：LibreOffice 转换（推荐，无需 GUI）
libreoffice --headless --convert-to xlsx input.numbers --outdir /tmp/
```

```python
# 方案 B：AppleScript 通过 Numbers 应用导出
import subprocess

def numbers_to_xlsx(numbers_path: str, output_path: str):
    script = f'''
    tell application "Numbers"
        open POSIX file "{numbers_path}"
        set doc to front document
        export doc to POSIX file "{output_path}" as Microsoft Excel
        close doc
    end tell
    '''
    subprocess.run(['osascript', '-e', script], check=True, timeout=60)
```

---

## 权限处理

首次运行 xlwings / AppleScript 控制 Excel 时，macOS 会弹出权限请求：

**手动开启路径：**
```
系统设置 → 隐私与安全性 → 辅助功能    → 开启"终端"/ "Python"
系统设置 → 隐私与安全性 → 自动化      → 允许控制"Microsoft Excel"
```

**代码检测权限：**

```python
import subprocess

def check_accessibility_permission() -> bool:
    result = subprocess.run(
        ['osascript', '-e',
         'tell application "System Events" to return name of first process'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("⚠️  需要辅助功能权限：系统设置 → 隐私与安全性 → 辅助功能")
        return False
    return True
```

---

## 常见问题

| 问题 | 解决方案 |
|---|---|
| `xlwings` 启动后卡住 | 确认 Excel for Mac 已完整安装并至少运行过一次 |
| `xlwings` 报权限错误 | 系统设置 → 自动化 → 允许终端控制 Excel |
| AppleScript 超时 | 增加 `timeout` 参数；大文件改用 `openpyxl` 离线读取 |
| `.numbers` 无法读取 | 用 LibreOffice 或 Numbers 应用先导出为 xlsx |
| 返回数据为字符串而非数值 | xlwings 默认返回显示值，改用 `ws.range("A1").raw_value` |
| M1/M2 芯片 xlwings 报错 | 确认 xlwings 与 Excel 同为 ARM 或 x86 架构，或用 Rosetta 运行 |
