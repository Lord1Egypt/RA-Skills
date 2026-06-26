# 踩坑记录

本文档记录开发过程中遇到的坑和解决方案，防止重复踩坑。

---

## 1. Excel样式复制问题

### 问题描述
使用openpyxl复制工作表时，样式（如字体颜色、背景色、对齐方式等）丢失或不完整。

### 原因分析
openpyxl的`copy()`方法对样式对象的复制不完整，特别是跨工作簿复制时。

### 解决方案
使用**临时文件法**：

```python
def _copy_sheet_from_template(self, template_wb, sheet_name: str, target_ws: Worksheet) -> None:
    import tempfile
    from copy import copy
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # 1. 保存模板到临时文件
        template_wb.save(tmp_path)
        
        # 2. 从临时文件重新加载（完整保留样式）
        tmp_wb = load_workbook(tmp_path, data_only=False)
        tmp_sheet = tmp_wb[sheet_name]
        
        # 3. 复制列宽
        for col_letter, dim in tmp_sheet.column_dimensions.items():
            target_ws.column_dimensions[col_letter].width = dim.width
            target_ws.column_dimensions[col_letter].hidden = dim.hidden
        
        # 4. 复制行高
        for row_num, dim in tmp_sheet.row_dimensions.items():
            target_ws.row_dimensions[row_num].height = dim.height
        
        # 5. 复制合并单元格
        for merge_range in tmp_sheet.merged_cells.ranges:
            target_ws.merge_cells(str(merge_range))
        
        # 6. 复制单元格样式
        for r in range(1, tmp_sheet.max_row + 1):
            for c in range(1, tmp_sheet.max_column + 1):
                src_cell = tmp_sheet.cell(row=r, column=c)
                
                # 跳过合并单元格
                if isinstance(src_cell, MergedCell):
                    continue
                
                tgt_cell = target_ws.cell(row=r, column=c)
                tgt_cell.value = src_cell.value
                
                # 完整样式复制
                tgt_cell.font = copy(src_cell.font)
                tgt_cell.fill = copy(src_cell.fill)
                tgt_cell.border = copy(src_cell.border)
                tgt_cell.alignment = copy(src_cell.alignment)
                tgt_cell.number_format = src_cell.number_format
                
                # protection属性
                if hasattr(src_cell, 'protection'):
                    tgt_cell.protection = copy(src_cell.protection)
        
        tmp_wb.close()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
```

### 关键点
- **必须通过临时文件**：直接复制的样式会丢失
- **逐个属性复制**：font, fill, border, alignment, number_format
- **处理MergedCell**：合并单元格区域内的子单元格需要跳过

---

## 2. 公式列被覆盖

### 问题描述
代码写入数据时，不小心覆盖了模板中的公式列（如H列、J列）。

### 原因分析
写入前没有明确哪些列是需要保留公式的，遍历时无差别写入。

### 解决方案
**方案1：固定禁止列表**
```python
# 禁止覆盖的列（公式列）
PROTECTED_COLUMNS = {'H', 'J'}

# 写入前检查
for col_letter in PROTECTED_COLUMNS:
    col_idx = col_letter_to_index(col_letter)
    if target_col == col_idx:
        continue  # 跳过受保护的列
```

**方案2：动态检测（推荐）**
```python
# 检测合并单元格行（C列参与合并的行，通常是小计/合计行）
merged_rows = set()
for merge_range in template_sheet.merged_cells.ranges:
    if merge_range.min_col <= 3 and merge_range.max_col >= 3:  # C列参与合并
        for row_num in range(merge_range.min_row, merge_range.max_row + 1):
            merged_rows.add(row_num)

# 跳过小计/合计/汇总行
for r in range(row_start, row_end + 1):
    if r in merged_rows:
        continue
    key_val = template_sheet.cell(row=r, column=match_t_col).value
    key_str = safe_str(key_val)
    if "小计" in key_str or "合计" in key_str or "汇总" in key_str:
        continue
    # 正常写入...
```

---

## 3. 大文件内存溢出

### 问题描述
处理几十MB甚至上百MB的Excel文件时，Python进程内存占用飙升，甚至崩溃。

### 原因分析
- 未使用`read_only`模式读取
- 一次加载整个工作簿到内存
- 未及时关闭工作簿

### 解决方案

**1. 使用只读模式**
```python
# 普通模式：读写混合，适合小文件
wb = load_workbook(filepath)

# 只读模式：适合大文件，只读的内存占用更低
wb = load_workbook(filepath, read_only=True, data_only=True)
```

**2. 限制读取范围**
```python
# 只读取需要的列
min_col = min(needed_columns)
max_col = max(needed_columns)

for row in source_ws.iter_rows(min_row=3, min_col=min_col, max_col=max_col):
    # 处理行
    pass
```

**3. 及时关闭**
```python
source_wb = load_workbook(source_path, read_only=True)
try:
    # 处理数据
    pass
finally:
    source_wb.close()  # 显式关闭释放内存
```

**4. 分批处理**
```python
# 按日期分割大文件为小文件
for date_key, rows in date_groups.items():
    # 每批只处理一个日期的数据
    self._create_new_file(output_path, header_row, rows)
```

---

## 4. 跨平台文件路径

### 问题描述
代码在Windows上正常，在Mac上无法找到文件，或者路径分隔符错误。

### 解决方案

**1. 使用os.path**
```python
import os

# 路径拼接
config_path = os.path.join(get_script_dir(), 'config.json')

# 检查存在
if os.path.exists(config_path):
    pass

# 获取目录
output_dir = os.path.dirname(filepath)
```

**2. 跨平台打开文件**
```python
import subprocess

def open_file(filepath):
    if sys.platform == 'darwin':
        subprocess.run(['open', filepath])
    elif sys.platform == 'win32':
        os.startfile(filepath)
    else:  # Linux
        subprocess.run(['xdg-open', filepath])
```

**3. 获取脚本目录**
```python
def get_script_dir() -> str:
    """获取脚本所在目录（跨平台）"""
    return os.path.dirname(os.path.abspath(__file__))
```

---

## 5. 线程安全问题

### 问题描述
- 在后台线程中直接更新GUI导致崩溃
- Tkinter不允许非主线程更新UI
- 日志输出不显示或显示乱序

### 解决方案

**Tkinter：使用after()**
```python
class TextHandler(logging.Handler):
    def emit(self, record):
        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        
        # 通过after()在主线程执行
        self.text_widget.after(0, append)
```

**Qt：使用Signal**
```python
class ExcelWorker(QObject):
    progress = Signal(str)  # 定义信号
    
    def run(self):
        # 在后台线程中发射信号
        self.progress.emit("处理中...")
```

**Tkinter：异步执行**
```python
def run_async(self, func):
    """异步执行耗时函数"""
    def wrapper():
        thread = threading.Thread(target=self._run_with_error_handler, args=(func,))
        thread.daemon = True
        thread.start()
    wrapper()

def _run_with_error_handler(self, func):
    try:
        func()
    except Exception as e:
        # 通过after更新UI
        self.root.after(0, lambda: messagebox.showerror("错误", str(e)))
```

---

## 6. 日期格式不一致

### 问题描述
- 源表日期格式多种多样：YYYYMMDD、YYYY-MM-DD、datetime对象、Excel序列号
- 代码只处理了其中一种格式，其他格式解析失败

### 解决方案

**统一日期解析**
```python
def convert_to_month_day(val) -> str:
    """将各种日期格式统一转换为X月X日"""
    if val is None:
        return ""
    
    # datetime对象
    if isinstance(val, datetime.datetime):
        return f"{val.month}月{val.day}日"
    if isinstance(val, datetime.date):
        return f"{val.month}月{val.day}日"
    
    # Excel序列号
    if isinstance(val, (int, float)):
        try:
            dt = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=val)
            return f"{dt.month}月{dt.day}日"
        except Exception:
            pass
    
    # 字符串解析
    digits = re.sub(r"\D+", "", safe_str(val))
    if len(digits) >= 8:
        m = re.match(r"^(\d{4})(\d{2})(\d{2})", digits)
        if m:
            month_int, day_int = int(m.group(2)), int(m.group(3))
            if 1 <= month_int <= 12 and 1 <= day_int <= 31:
                return f"{month_int}月{day_int}日"
    
    return ""
```

---

## 7. 配置文件损坏

### 问题描述
配置文件被意外修改、格式错误或损坏，导致程序无法启动。

### 解决方案

**1. 默认配置**
```python
DEFAULT_CONFIG = {
    "schema_version": 2,
    "source": {"default_paths": [], "sheet_index": 0},
    "target": {...},
}

def ensure_config_exists(config_path):
    """配置文件不存在则创建默认配置"""
    if os.path.exists(config_path):
        return
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
```

**2. 读取失败时备份重建**
```python
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception:
    # 备份旧文件
    backup_path = f"{config_path}.bak_{int(time.time())}"
    try:
        os.replace(config_path, backup_path)
    except Exception:
        pass
    # 使用默认配置
    config = DEFAULT_CONFIG.copy()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
```

---

## 8. Sheet名称重复

### 问题描述
创建结果sheet时，如果名称已存在，会抛出异常。

### 解决方案

**1. 询问用户**
```python
def create_sheet_with_confirm(wb, sheet_name, overwrite_callback=None):
    if sheet_name in wb.sheetnames:
        reply = QMessageBox.question(
            None, "Sheet已存在",
            f"Sheet「{sheet_name}」已存在，是否覆盖？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return None
        
        # 删除旧sheet
        del wb[sheet_name]
    
    return wb.create_sheet(title=sheet_name)
```

**2. 自动加序号**
```python
def get_unique_sheet_name(wb, base_name):
    """获取不重复的sheet名称"""
    if base_name not in wb.sheetnames:
        return base_name
    
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}"
        if new_name not in wb.sheetnames:
            return new_name
        counter += 1
```

---

## 9. 循环变量捕获

### 问题描述
在循环中创建lambda/回调时，使用了循环变量而非其当前值，导致所有回调执行时都使用最后一个值。

### 问题代码
```python
for i, cmd in enumerate(btn_configs):
    btn = ttk.Button(frame, text=text, command=lambda: self.run_async(cmd))  # 错误！
```

### 解决方案
```python
for i, cmd in enumerate(btn_configs):
    # 方法1：默认参数捕获
    btn = ttk.Button(frame, text=text, command=lambda c=cmd: self.run_async(c))
    
    # 方法2：闭包
    def make_callback(cmd):
        return lambda: self.run_async(cmd)
    btn = ttk.Button(frame, text=text, command=make_callback(cmd))
```

---

## 10. PyInstaller打包问题

### 问题描述
打包后的exe找不到配置文件、无法打开文件、界面显示异常。

### 解决方案

**1. 包含数据文件**
```python
# spec_file.spec
a = Analysis(['main.py'],
    ...
    datas=[('settings.json', '.'), ('数据模板.xlsx', '.')],
    ...
)
```

**2. 获取资源路径**
```python
import sys

def resource_path(relative_path):
    """获取资源文件的绝对路径（兼容开发环境和打包后）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller创建的临时文件夹
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)
```

**3. 隐藏控制台窗口**
```python
# spec_file.spec
a = Analysis(['main.py'],
    console=False,  # Windows下隐藏控制台
    ...
)
```

---

## 11. 持续更新

### 添加新坑的模板

```markdown
## N. 坑的名称

### 问题描述
问题是什么？

### 原因分析
为什么会出问题？

### 解决方案
如何解决？

### 预防措施
如何避免再次踩坑？
```
