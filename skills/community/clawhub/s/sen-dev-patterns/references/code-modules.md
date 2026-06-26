# 代码模块库

本文档沉淀常用的代码模块，便于复用。

---

## 1. 日志模块

### Tkinter日志处理器

```python
import tkinter as tk
import logging

class TextHandler(logging.Handler):
    """自定义日志处理器，将日志输出到Tkinter文本框"""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    
    def emit(self, record):
        msg = self.formatter.format(record)
        
        def append():
            if record.levelno >= logging.ERROR:
                self.text_widget.insert(tk.END, msg + '\n', 'error')
            elif record.levelno >= logging.WARNING:
                self.text_widget.insert(tk.END, msg + '\n', 'warning')
            elif record.levelno >= logging.INFO:
                self.text_widget.insert(tk.END, msg + '\n', 'info')
            else:
                self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        
        try:
            self.text_widget.after(0, append)
        except Exception:
            pass

class Logger:
    """日志管理器"""
    
    def __init__(self, name='App'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []
    
    def setup_gui_logger(self, text_widget):
        """设置GUI日志处理器"""
        self.logger.handlers = []
        handler = TextHandler(text_widget)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        text_widget.tag_config('info', foreground='#000000')
        text_widget.tag_config('warning', foreground='#FF8C00')
        text_widget.tag_config('error', foreground='#DC143C')
    
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)
```

---

## 2. 文件工具类

### FileUtil 文件操作类

```python
import os
import csv
from tkinter import filedialog
import openpyxl

class FileUtil:
    """文件操作工具类"""
    
    ALLOWED_EXTENSIONS = [
        ('Excel 文件', '*.xlsx *.xls'),
        ('CSV 文件', '*.csv'),
        ('所有支持的文件', '*.xlsx *.xls *.csv')
    ]
    
    @staticmethod
    def select_files(title="选择数据文件"):
        """选择多个原始数据文件"""
        filepaths = filedialog.askopenfilenames(
            title=title,
            filetypes=FileUtil.ALLOWED_EXTENSIONS
        )
        return list(filepaths) if filepaths else []
    
    @staticmethod
    def select_file(title="选择数据文件"):
        """选择单个原始数据文件"""
        filepath = filedialog.askopenfilename(
            title=title,
            filetypes=FileUtil.ALLOWED_EXTENSIONS
        )
        return filepath if filepath else None
    
    @staticmethod
    def validate_file(filepath):
        """验证文件格式"""
        if not filepath:
            return False, "文件路径为空"
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ['.xlsx', '.xls', '.csv']:
            return False, f"不支持的文件格式: {ext}"
        if not os.path.exists(filepath):
            return False, "文件不存在"
        return True, "验证通过"
    
    @staticmethod
    def read_excel(filepath, sheet_name=None):
        """读取Excel文件"""
        wb = openpyxl.load_workbook(filepath, data_only=False)
        ws = wb[sheet_name] if sheet_name else wb.active
        return wb, ws
    
    @staticmethod
    def get_output_path(base_dir, folder_name, filename):
        """获取输出路径，自动创建目录"""
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return os.path.join(folder_path, filename)
```

---

## 3. 配置管理模块

### ConfigManager 配置管理

```python
import json
import os

class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load()
    
    def _load(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {e}")
        return {}
    
    def save(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
```

---

## 4. 常量与工具函数

### 常用工具函数

```python
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

def get_script_dir() -> str:
    """获取脚本所在目录"""
    return os.path.dirname(os.path.abspath(__file__))

def safe_str(v) -> str:
    """安全转换为字符串"""
    if v is None:
        return ""
    return str(v).strip()

def parse_float(v) -> float:
    """安全转换为浮点数，转换失败返回0.0"""
    s = safe_str(v)
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0

def col_letter_to_index(letter: str) -> int:
    """将Excel列字母转换为1-based索引"""
    letter = letter.strip().upper()
    n = 0
    for ch in letter:
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n

def contains_any(hay: str, needles: List[str]) -> bool:
    """检查hay是否包含任何needle"""
    if not hay:
        return False
    for kw in needles:
        if kw and kw in hay:
            return True
    return False

def exact_match(hay: str, needles: List[str]) -> bool:
    """检查hay是否精确匹配任何needle"""
    if not hay:
        return False
    return hay in needles

def extract_month_day_from_yyyymmdd(v) -> Tuple[str, str]:
    """从日期值中提取月和日"""
    s = safe_str(v)
    if not s:
        return ("", "")
    digits = re.sub(r"\D+", "", s)
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", digits)
    if not m:
        return ("", "")
    return m.group(2), m.group(3)

@dataclass
class MetricCounters:
    """指标计数器"""
    count_pos: int = 0
    sum_pos: float = 0.0
    count_pos_x_yes: int = 0
    count_pos_t_len: int = 0
    count_z_ge1: int = 0

    def update(self, calc_val: float, x_yes: bool, t_len_ge10: bool, z_ge1: bool) -> None:
        """更新计数器"""
        self.count_pos += 1
        self.sum_pos += calc_val
        if x_yes:
            self.count_pos_x_yes += 1
        if t_len_ge10:
            self.count_pos_t_len += 1
        if z_ge1:
            self.count_z_ge1 += 1

    def avg_pos(self) -> Optional[float]:
        if self.count_pos <= 0:
            return None
        return self.sum_pos / float(self.count_pos)

    def is_empty(self) -> bool:
        return self.count_pos == 0
```

---

## 5. Excel操作模块

### 读取Excel数据的标准模式

```python
import openpyxl
from openpyxl.utils import get_column_letter

def read_excel_data(filepath, sheet_name=None, header_row=1, 
                    min_col=None, max_col=None, read_only=True):
    """
    读取Excel数据
    
    Args:
        filepath: 文件路径
        sheet_name: 工作表名称，默认读取active sheet
        header_row: 表头行号
        min_col: 最小列
        max_col: 最大列
        read_only: 是否只读模式（节省内存）
    
    Returns:
        (headers, data): 表头列表和数据行列表
    """
    wb = openpyxl.load_workbook(filepath, data_only=read_only, read_only=read_only)
    ws = wb[sheet_name] if sheet_name else wb.active
    
    headers = []
    data = []
    
    # 读取表头
    row_iter = ws.iter_rows(min_row=header_row, max_row=header_row, 
                           min_col=min_col, max_col=max_col, values_only=True)
    for row in row_iter:
        headers = list(row)
    
    # 读取数据
    data_iter = ws.iter_rows(min_row=header_row + 1, 
                            min_col=min_col, max_col=max_col, values_only=True)
    for row in data_iter:
        if any(cell is not None for cell in row):
            data.append(list(row))
    
    wb.close()
    return headers, data
```

### 写入Excel数据的标准模式

```python
def write_excel_data(filepath, data, sheet_name="Sheet1", headers=None):
    """
    写入Excel数据
    
    Args:
        filepath: 输出文件路径
        data: 数据列表 [[row1], [row2], ...]
        sheet_name: 工作表名称
        headers: 表头列表
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name
    
    start_row = 1
    if headers:
        for col_idx, header in enumerate(headers, start=1):
            ws.cell(row=1, column=col_idx, value=header)
        start_row = 2
    
    for row_idx, row_data in enumerate(data, start=start_row):
        for col_idx, value in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    wb.save(filepath)
    wb.close()
```

### 复制Sheet样式

```python
import tempfile
import shutil

def copy_sheet_with_styles(source_wb, source_sheet_name, target_wb, target_sheet_name):
    """
    复制Sheet及其样式（通过临时文件方法）
    """
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    
    # 保存源工作簿到临时文件
    source_wb.save(tmp_path)
    
    # 从临时文件读取目标Sheet
    tmp_wb = openpyxl.load_workbook(tmp_path)
    if source_sheet_name in tmp_wb.sheetnames:
        source_ws = tmp_wb[source_sheet_name]
        target_ws = target_wb.create_sheet(target_sheet_name)
        
        # 复制单元格值和样式
        for row in source_ws.iter_rows():
            for cell in row:
                new_cell = target_ws[cell.coordinate]
                new_cell.value = cell.value
                if cell.has_style:
                    new_cell.font = cell.font.copy()
                    new_cell.fill = cell.fill.copy()
                    new_cell.border = cell.border.copy()
                    new_cell.alignment = cell.alignment.copy()
                    new_cell.number_format = cell.number_format
        
        # 复制列宽
        for col in source_ws.column_dimensions:
            target_ws.column_dimensions[col].width = source_ws.column_dimensions[col].width
    
    tmp_wb.close()
    os.unlink(tmp_path)
```

---

## 6. GUI组件模板

### 设置对话框模板（QTabWidget布局）

```python
from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QTabWidget, QWidget,
    QVBoxLayout, QFormLayout, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    """设置对话框模板"""
    
    def __init__(self, parent, config):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setModal(True)
        self.setMinimumSize(650, 550)
        self.config = config
        
        outer = QVBoxLayout(self)
        outer.setSpacing(12)
        outer.setContentsMargins(12, 12, 12, 12)
        
        # 标签页控件
        self.tabs = QTabWidget()
        self._build_tab1()
        self._build_tab2()
        outer.addWidget(self.tabs, 1)
        
        # 底部按钮
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._apply_and_accept)
        btns.rejected.connect(self.reject)
        outer.addWidget(btns)
    
    def _build_tab1(self):
        """构建Tab1"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        # ... 添加控件
        self.tabs.addTab(tab, "页面1")
    
    def _build_tab2(self):
        """构建Tab2"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        # ... 添加控件
        self.tabs.addTab(tab, "页面2")
    
    def _apply_and_accept(self):
        """应用并保存"""
        self.accept()
    
    def get_config(self):
        return self.config
```

### 表单行布局模板

```python
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLineEdit, QPushButton

def create_form_row(label_text, default_value="", browse=False):
    """
    创建标准表单行
    
    Returns:
        (form_row, line_edit, browse_btn or None)
    """
    form_row = QHBoxLayout()
    line_edit = QLineEdit(default_value)
    line_edit.setMinimumWidth(300)
    
    if browse:
        browse_btn = QPushButton("浏览...")
        browse_btn.setFixedSize(70, 28)
        form_row.addWidget(line_edit, 1)
        form_row.addWidget(browse_btn)
        return form_row, line_edit, browse_btn
    else:
        form_row.addWidget(line_edit, 1)
        return form_row, line_edit, None
```

---

## 7. 数据处理模板

### 按日期分组汇总

```python
from collections import defaultdict

def aggregate_by_date(data, date_col_idx, value_col_indices):
    """
    按日期分组汇总数据
    
    Args:
        data: [[date, val1, val2, ...], ...]
        date_col_idx: 日期列索引
        value_col_indices: 需要汇总的数值列索引列表
    
    Returns:
        {date: {'count': n, 'sums': [s1, s2, ...], ...}}
    """
    result = defaultdict(lambda: {'count': 0, 'sums': defaultdict(float)})
    
    for row in data:
        date_val = row[date_col_idx]
        if not date_val:
            continue
        
        result[date_val]['count'] += 1
        for col_idx in value_col_indices:
            val = row[col_idx]
            if isinstance(val, (int, float)):
                result[date_val]['sums'][col_idx] += val
    
    return dict(result)
```

### 条件筛选器

```python
class DataFilter:
    """数据筛选器"""
    
    def __init__(self):
        self.conditions = []
    
    def add_condition(self, col_idx, operator, value):
        """添加筛选条件"""
        self.conditions.append((col_idx, operator, value))
        return self
    
    def apply(self, data):
        """应用筛选"""
        result = []
        for row in data:
            if all(self._check_condition(row, cond) for cond in self.conditions):
                result.append(row)
        return result
    
    def _check_condition(self, row, condition):
        col_idx, operator, value = condition
        val = row[col_idx]
        
        if operator == '==':
            return val == value
        elif operator == '!=':
            return val != value
        elif operator == '>=':
            return val >= value
        elif operator == '<=':
            return val <= value
        elif operator == '>':
            return val > value
        elif operator == '<':
            return val < value
        elif operator == 'contains':
            return value in str(val) if val else False
        elif operator == 'is_empty':
            return val is None or val == ''
        
        return True
```

---

## 8. 常用样式片段

### 水晶质感按钮样式

```python
CRYSTAL_BUTTON_STYLE = """
    QPushButton {
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
        border-radius: 16px;
        padding: 12px 20px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #667eea, stop:0.5 #764ba2, stop:1 #667eea);
        border-top: 1px solid #ffffff;
        border-left: 1px solid #ffffff;
        border-right: 1px solid #000000;
        border-bottom: 2px solid #000000;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #7c8ff0, stop:0.5 #8a5db3, stop:1 #7c8ff0);
    }
    QPushButton:pressed {
        border-bottom: 1px solid #000000;
        padding-top: 14px;
    }
    QPushButton:disabled {
        color: #cccccc;
        background: #a0aec0;
        border-color: #718096;
    }
"""
```

### 标签页样式

```python
TAB_STYLE = """
    QTabWidget::pane {
        border: 1px solid #4ebaff;
        border-radius: 8px;
        background: #ffffff;
        padding: 12px;
    }
    QTabBar::tab {
        background: #e8f4ff;
        border: 1px solid #4ebaff;
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        padding: 10px 24px;
        margin-right: 4px;
        font-weight: 700;
        color: #0b3d91;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        border-bottom: 2px solid #ffffff;
    }
    QTabBar::tab:hover {
        background: #d4ebff;
    }
"""
```

### 日志区域样式

```python
LOG_TEXT_STYLE = """
    QTextEdit {
        background: #1a202c;
        color: #e2e8f0;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        border-radius: 6px;
        padding: 8px;
    }
"""
```

### 输入框样式

```python
LINE_EDIT_STYLE = """
    QLineEdit {
        background: #ffffff;
        border: 1px solid #d0d0d0;
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QLineEdit:focus {
        border: 2px solid #667eea;
        background: #f8f9ff;
    }
"""
```

---

## 9. 进度条与状态指示

### 进度条模板

```python
def create_progress_dialog(parent, title="处理中", max_steps=100):
    """创建进度对话框"""
    from PySide6.QtWidgets import QProgressDialog
    
    dialog = QProgressDialog(title, "取消", 0, max_steps, parent)
    dialog.setWindowTitle(title)
    dialog.setWindowModality(Qt.WindowModal)
    dialog.setMinimumDuration(0)
    dialog.setValue(0)
    return dialog

# 使用示例
def process_with_progress(data, callback):
    dialog = create_progress_dialog(len(data))
    results = []
    
    for i, item in enumerate(data):
        if dialog.wasCanceled():
            break
        results.append(callback(item))
        dialog.setValue(i + 1)
    
    dialog.close()
    return results
```

### 状态指示灯

```python
STATUS_INDICATOR_STYLE = """
    QLabel#status_indicator {
        border-radius: 8px;
        min-width: 16px;
        max-width: 16px;
        min-height: 16px;
        max-height: 16px;
    }
    QLabel#status_indicator.success {
        background-color: #48bb78;
    }
    QLabel#status_indicator.warning {
        background-color: #f6ad55;
    }
    QLabel#status_indicator.error {
        background-color: #fc8181;
    }
    QLabel#status_indicator.idle {
        background-color: #a0aec0;
    }
"""
```

---

## 10. 异常处理模板

### 标准异常处理

```python
import traceback
import sys

def safe_execute(func, *args, default=None, log_error=True, **kwargs):
    """
    安全执行函数，捕获异常
    
    Args:
        func: 要执行的函数
        *args: 位置参数
        default: 异常时返回的默认值
        log_error: 是否记录错误日志
        **kwargs: 关键字参数
    
    Returns:
        函数返回值或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_error:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"执行失败: {error_msg}")
            traceback.print_exc()
        return default

class AppError(Exception):
    """应用自定义异常"""
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)

def handle_app_error(e: AppError):
    """处理应用异常"""
    error_msg = f"[{e.code}] {e.message}" if e.code else e.message
    # 根据错误类型执行不同操作
    if e.code == 'FILE_NOT_FOUND':
        # 文件未找到处理
        pass
    elif e.code == 'DATA_INVALID':
        # 数据无效处理
        pass
    return error_msg
```
