# Windows API Reference

## COM 应用调用手册

### Excel / WPS Spreadsheet (KET)

```python
import win32com.client

# Excel
excel = win32com.client.Dispatch("Excel.Application")
# WPS 表格
wps = win32com.client.Dispatch("KET.Application")

# 通用设置
app.Visible = False
app.DisplayAlerts = False

# 打开工作簿
wb = app.Workbooks.Open(r"C:\path\to\file.xlsx")
ws = wb.Sheets("Sheet1")       # 按名称
ws = wb.Sheets(1)              # 按索引（1-based）
ws = wb.ActiveSheet            # 活动工作表

# 读取数据
data = ws.UsedRange.Value      # 返回 tuple of tuples
cell_val = ws.Cells(1, 1).Value
range_val = ws.Range("A1:D10").Value

# 写入数据
ws.Cells(1, 1).Value = "Hello"
ws.Range("A1:B2").Value = ((1, 2), (3, 4))

# 保存与关闭
wb.Save()
wb.SaveAs(r"C:\output.xlsx")
wb.Close(False)                # False = 不保存
app.Quit()
```

### Word / WPS Writer (KWPS)

```python
# Word
word = win32com.client.Dispatch("Word.Application")
# WPS 文字
kwps = win32com.client.Dispatch("KWPS.Application")

doc = app.Documents.Open(filepath)

# 提取正文
full_text = doc.Content.Text

# 段落遍历
for para in doc.Paragraphs:
    style = para.Style.NameLocal
    text = para.Range.Text

# 表格提取
for table in doc.Tables:
    for i in range(1, table.Rows.Count + 1):
        for j in range(1, table.Columns.Count + 1):
            cell = table.Cell(i, j).Range.Text.rstrip('\r\x07')

# 内置属性
author = doc.BuiltInDocumentProperties("Author").Value
pages = doc.ComputeStatistics(2)   # wdStatisticPages = 2
words = doc.ComputeStatistics(0)   # wdStatisticWords = 0

doc.Close(False)
app.Quit()
```

### PowerShell COM 方式（无 Python 环境）

```powershell
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Open("C:\data.xlsx")
$ws = $wb.Sheets.Item(1)
$used = $ws.UsedRange
$data = $used.Value2
$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel)
```

---

## 安全上下文管理器

```python
import contextlib
import win32com.client

@contextlib.contextmanager
def safe_com_session(app_name: str):
    app = None
    try:
        app = win32com.client.Dispatch(app_name)
        app.Visible = False
        app.DisplayAlerts = False
        yield app
    except Exception as e:
        raise RuntimeError(f"COM 调用失败 [{app_name}]: {e}") from e
    finally:
        if app:
            try:
                app.Quit()
            except Exception:
                pass
```

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|---|---|---|
| `pywintypes.com_error` | Office 未安装或版本不匹配 | 改用 `openpyxl` |
| Excel 进程残留 | 未调用 `Quit()` | 使用 `safe_com_session` |
| 读取公式而非值 | 未设置计算 | 调用 `wb.Application.Calculate()` |
| 中文乱码 | 编码问题 | 保存时指定 `encoding='utf-8-sig'` |
| WPS COM 报错 | COM 名称不同 | 用 `KET.Application` / `KWPS.Application` |
