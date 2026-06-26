# Windows API Reference

> Windows 下文件操作首选 **Python + win32com**，失败自动降级到 **openpyxl / python-docx**。
> 所有 COM 操作已封装到 `safe_com_session` 上下文管理器，无需手动调用 `Quit()`。

---

## 快速降级链

```
Excel / WPS 表格：  win32com → openpyxl
Word / WPS 文字：   win32com → python-docx
旧格式 .xls/.doc：  win32com → xlrd/openpyxl
```

---

## Excel COM 操作（win32com）

### 读取

```python
import win32com.client
from pathlib import Path

# 推荐：使用安全上下文管理器（见下方）
with safe_com_session("Excel.Application") as app:
    wb = app.Workbooks.Open(str(Path("data.xlsx").resolve()))

    # 按名称 / 索引（1-based）/ 活动表
    ws = wb.Sheets("Sheet1")
    ws = wb.Sheets(1)

    # 读取已用区域（返回 tuple of tuples）
    raw = ws.UsedRange.Value
    if raw:
        rows = [list(row) for row in raw] if isinstance(raw[0], tuple) else [list(raw)]

    # 读取指定区域
    cell_val   = ws.Cells(1, 1).Value
    range_val  = ws.Range("A1:D10").Value

    # 读取前确保公式已计算
    app.Calculate()

    wb.Close(False)   # False = 不保存
```

### 写入

```python
with safe_com_session("Excel.Application") as app:
    wb = app.Workbooks.Open(str(Path("data.xlsx").resolve()))
    ws = wb.Sheets(1)

    # 单元格写入
    ws.Cells(1, 1).Value = "标题"
    ws.Range("A2:C2").Value = (("姓名", "分数", "等级"),)

    # 批量写入（二维 tuple，性能最优）
    data = tuple(tuple(row) for row in df.values.tolist())
    ws.Range(f"A2:C{len(data)+1}").Value = data

    # 设置格式
    ws.Cells(1, 1).Font.Bold = True
    ws.Columns("A:C").AutoFit()

    wb.Save()
```

### 新建工作簿

```python
with safe_com_session("Excel.Application") as app:
    wb = app.Workbooks.Add()
    ws = wb.ActiveSheet
    ws.Name = "销售报告"
    ws.Range("A1").Value = "月份"
    wb.SaveAs(str(Path("output.xlsx").resolve()))
```

### 格式转换（xlsx / csv / pdf）

```python
with safe_com_session("Excel.Application") as app:
    wb = app.Workbooks.Open(str(Path("data.xls").resolve()))

    # 另存为 xlsx
    wb.SaveAs(r"C:\output.xlsx", FileFormat=51)   # 51 = xlOpenXMLWorkbook

    # 另存为 CSV
    wb.SaveAs(r"C:\output.csv", FileFormat=6)     # 6 = xlCSV

    # 导出 PDF
    wb.ExportAsFixedFormat(0, r"C:\output.pdf")   # 0 = xlTypePDF
```

---

## WPS 表格 COM（KET.Application）

```python
# WPS 表格 COM 名称与 Excel 不同
with safe_com_session("KET.Application") as app:
    wb = app.Workbooks.Open(str(Path("data.et").resolve()))
    for ws in wb.Sheets:
        raw = ws.UsedRange.Value
        print(ws.Name, len(raw) if raw else 0)
    wb.Close(False)
```

---

## Word / WPS Writer COM

### 读取

```python
with safe_com_session("Word.Application") as app:    # WPS 用 "KWPS.Application"
    doc = app.Documents.Open(str(Path("doc.docx").resolve()))

    # 正文文本
    full_text = doc.Content.Text

    # 段落遍历
    for para in doc.Paragraphs:
        style = para.Style.NameLocal
        text  = para.Range.Text.rstrip('\r\n')

    # 表格提取
    tables = []
    for table in doc.Tables:
        tbl = []
        for i in range(1, table.Rows.Count + 1):
            row = []
            for j in range(1, table.Columns.Count + 1):
                try:
                    row.append(table.Cell(i, j).Range.Text.rstrip('\r\x07'))
                except Exception:
                    row.append("")
            tbl.append(row)
        tables.append(tbl)

    # 文档属性
    author = doc.BuiltInDocumentProperties("Author").Value
    pages  = doc.ComputeStatistics(2)   # wdStatisticPages
    words  = doc.ComputeStatistics(0)   # wdStatisticWords

    doc.Close(False)
```

### 写入

```python
with safe_com_session("Word.Application") as app:
    doc = app.Documents.Add()
    rng = doc.Content

    rng.Text = "这是新增的段落内容。"
    rng.InsertParagraphAfter()

    # 设置样式
    para = doc.Paragraphs(1)
    para.Style = doc.Styles("Heading 1")

    doc.SaveAs(str(Path("output.docx").resolve()), FileFormat=16)  # 16 = docx
```

---

## 安全上下文管理器

```python
import contextlib
import win32com.client

@contextlib.contextmanager
def safe_com_session(app_name: str):
    """
    安全 COM 会话：自动隐藏窗口，异常或正常退出时都调用 Quit()，防止进程残留。
    用法：with safe_com_session("Excel.Application") as app: ...
    """
    app = None
    try:
        app = win32com.client.Dispatch(app_name)
        app.Visible = False
        if hasattr(app, 'DisplayAlerts'):
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

## PowerShell 备用方案（无 Python 环境）

```powershell
# 读取 Excel 数据
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Open("C:\data.xlsx")
$ws = $wb.Sheets.Item(1)
$data = $ws.UsedRange.Value2      # Value2 不含货币/日期格式
$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

# 导出为 CSV（无需 Python）
$ws.UsedRange.Value2 | Export-Csv "C:\output.csv" -Encoding UTF8 -NoTypeInformation
```

---

## openpyxl 降级方案

当 win32com 不可用时（未安装 Office / 权限不足），自动切换：

```python
import openpyxl
from pathlib import Path

def read_excel_offline(filepath: str, sheet_name: str = None) -> dict:
    file_mb = Path(filepath).stat().st_size / 1e6
    read_only = file_mb > 50   # 大文件自动只读

    wb = openpyxl.load_workbook(filepath, data_only=True, read_only=read_only)
    result = {}
    sheets = [wb[sheet_name]] if sheet_name else wb.worksheets
    for ws in sheets:
        result[ws.title] = [list(row) for row in ws.iter_rows(values_only=True)]
    wb.close()
    return result
```

---

## 常见问题

| 错误 / 现象 | 原因 | 解决方案 |
|---|---|---|
| `pywintypes.com_error: -2147221005` | Office 未安装或注册表损坏 | 降级用 `openpyxl` |
| Excel 进程残留（任务管理器可见） | 未调用 `Quit()` | 使用 `safe_com_session` |
| 读到公式文本而非计算值 | 未触发重算 | 调用 `app.Calculate()` 后再读 |
| `UsedRange.Value` 返回单值而非元组 | 只有一行/一列数据 | 判断类型：`isinstance(raw, tuple)` |
| 中文路径报错 | COM 不接受相对路径 | 用 `Path(fp).resolve()` 转绝对路径 |
| WPS COM 名称找不到 | WPS 未安装或版本不同 | 表格用 `KET.Application`，文字用 `KWPS.Application` |
| 写入后数字格式异常 | COM 自动推断类型 | 写入前将数字转 `float`：`ws.Cells(r,c).Value = float(val)` |
