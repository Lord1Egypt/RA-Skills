# 编程规范

## 核心原则

### 1. 最小改动原则
- **只改需要改的地方**：需求变更时，只修改与当前问题相关的最少代码行
- **禁止重构**：不主动重构已验证正确的代码
- **禁止优化无关代码**：不要借机优化其他代码
- **禁止覆盖源文件和模板文件**：绝对不能修改源数据和模板文件

### 2. 已正确部分绝对不动
- 若明确说明某部分逻辑正确，必须严格保护
- 不得修改变量名、结构、顺序、注释和格式

### 3. 修改必须透明
- 每次修改后说明：修改了哪几行、修改原因、对原有逻辑的影响

### 4. 先定位问题，再动手修改
- 优先帮用户定位错误位置
- 不直接大面积改写代码

### 5. 计算逻辑优先保证正确性
- 数值计算、表格列计算必须严格按输入输出样例对齐
- 不自行简化逻辑

### 6. 避免连锁改错
- 改某一列/某一段逻辑时，不得影响其他已验证正确的部分

## Excel处理规范

### 列保护规则

**绝对禁止覆盖的列**：
- H列：公式列，禁止代码覆盖
- J列：公式列，禁止代码覆盖
- E到K列（及新增L/M列）：无明确要求不改动

**保护实现**：
```python
# 动态检测需要跳过的行
skip_rows = set()
for r in range(row_start, row_end + 1):
    key_val = template_sheet.cell(row=r, column=match_t_col).value
    key_str = safe_str(key_val)
    if "小计" in key_str or "合计" in key_str or "汇总" in key_str:
        skip_rows.add(r)

# 跳过合并单元格行
merged_rows = set()
for merge_range in template_sheet.merged_cells.ranges:
    if merge_range.min_col <= 3 and merge_range.max_col >= 3:
        for row_num in range(merge_range.min_row, merge_range.max_row + 1):
            merged_rows.add(row_num)
```

### 大数据量优化

```python
# 1. 使用read_only模式读取大文件
source_wb = load_workbook(source_path, data_only=True, read_only=True)
source_ws = source_wb.active

# 2. 限制读取列范围
min_col = min(all_needed_columns)
max_col = max(all_needed_columns)
for row in source_ws.iter_rows(min_row=min_row, min_col=min_col, max_col=max_col):
    # 处理数据

# 3. 进度提示
if idx % 800 == 0:
    self.progress.emit(f"统计进度：已处理约 {idx} 行...")

# 4. 关闭工作簿释放内存
source_wb.close()
```

### 样式复制（完整版）

```python
def _copy_sheet_from_template(self, template_wb, sheet_name: str, target_ws: Worksheet) -> None:
    """
    正确复制工作表样式：
    1. 保存模板到临时文件
    2. 从临时文件加载获取完整的样式
    3. 遍历复制每个单元格的值和完整样式
    """
    import tempfile
    from copy import copy
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # 保存模板到临时文件
        template_wb.save(tmp_path)
        # 重新加载获取完整样式
        tmp_wb = load_workbook(tmp_path, data_only=False)
        tmp_sheet = tmp_wb[sheet_name]
        
        # 复制列宽
        for col_letter, dim in tmp_sheet.column_dimensions.items():
            target_ws.column_dimensions[col_letter].width = dim.width
        
        # 复制合并单元格
        for merge_range in tmp_sheet.merged_cells.ranges:
            target_ws.merge_cells(str(merge_range))
        
        # 复制单元格样式
        for r in range(1, tmp_sheet.max_row + 1):
            for c in range(1, tmp_sheet.max_column + 1):
                src_cell = tmp_sheet.cell(row=r, column=c)
                tgt_cell = target_ws.cell(row=r, column=c)
                tgt_cell.value = src_cell.value
                
                # 完整样式复制
                tgt_cell.font = copy(src_cell.font)
                tgt_cell.fill = copy(src_cell.fill)
                tgt_cell.border = copy(src_cell.border)
                tgt_cell.alignment = copy(src_cell.alignment)
                tgt_cell.number_format = src_cell.number_format
        
        tmp_wb.close()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
```

## 线程安全

### Qt Worker模式

```python
from PySide6.QtCore import QObject, Signal, QThread

class ExcelWorker(QObject):
    """Excel数据处理工作器"""
    progress = Signal(str)
    finished = Signal(str)
    failed = Signal(str)
    request_sheet_name = Signal(str, object)
    request_sheet_overwrite = Signal(str, object)
    
    def __init__(self, config, source_path, output_dir):
        super().__init__()
        self.config = config
        self.source_path = source_path
        self.output_dir = output_dir
        # 用于线程间通信
        self._sheet_name_event = threading.Event()
        self._sheet_name_value = None
    
    def run(self):
        try:
            self._run_impl()
        except Exception as e:
            self.failed.emit(f"发生异常：{e}\n\n{traceback.format_exc()}")
    
    def set_sheet_name(self, name, request_id):
        self._sheet_name_value = name
        self._sheet_name_event.set()
```

### Tkinter 线程安全

```python
class TextHandler(logging.Handler):
    """将日志输出到Tkinter ScrolledText"""
    def emit(self, record):
        def append():
            if record.levelno >= logging.ERROR:
                self.text_widget.insert(tk.END, msg + '\n', 'error')
            # ...
            self.text_widget.see(tk.END)
        try:
            # 使用after()线程安全更新UI
            self.text_widget.after(0, append)
        except Exception:
            pass
```

## 日志规范

### 日志格式

```python
# 分隔线
app_logger.info("=" * 50)
app_logger.info("开始执行：功能名称")
app_logger.info("=" * 50)

# 步骤日志
app_logger.info("-" * 40)
app_logger.info("步骤1: 操作描述")

# 进度日志（带颜色）
app_logger.info(f"处理文件 {i+1}/{total}: {filename}")
app_logger.info(f"写入进度：{pct}%")

# 完成日志
app_logger.info("=" * 50)
app_logger.info("✓ 完成！已生成：路径")
app_logger.info("=" * 50)
```

### 日志颜色语义

| 关键词 | 颜色 | 含义 |
|--------|------|------|
| 完成、成功 | #68d391/#48bb78 | 成功完成 |
| 开始、统计、处理 | #63b3ed | 进度信息 |
| 错误、失败 | #fc8181 | 错误信息 |
| 跳过 | #a0aec0 | 跳过/忽略 |
| 警告 | #f6ad55 | 警告信息 |

## 配置管理

### JSON配置结构

```json
{
    "schema_version": 2,
    "source": {
        "default_paths": ["path1.xlsx", "path2.xlsx"],
        "sheet_index": 0
    },
    "target": {
        "workbook_relative_path": "数据模板.xlsx",
        "sheet_name": "关键数据",
        "match_key_target_column": "C",
        "match_key_source_column": "G",
        "target_row_start": 3,
        "target_row_end": 88
    },
    "output": {
        "summary_filename": "汇总.xlsx"
    },
    "source_columns": {
        "l": "L",
        "z": "Z",
        "aa": "AA"
    },
    "base_columns": {
        "count": "E",
        "sum": "G",
        "target_l_avg": "K"
    },
    "groups": [
        {
            "group_name": "分中心名称",
            "keywords": ["关键词1", "关键词2"]
        }
    ]
}
```

### 配置管理器

```python
DEFAULT_CONFIG = {
    "schema_version": 3,
    "source": {"default_paths": [], "sheet_index": 0},
    "target": {...},
    "output": {...},
}

def ensure_config_exists(config_path):
    if os.path.exists(config_path):
        return
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        ensure_config_exists(config_path)
        self.data = self.load()
    
    def load(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
```

## 工具函数

### 列字母转换

```python
def col_letter_to_index(letter: str) -> int:
    """将Excel列字母（如 'G', 'AK'）转换为1-based索引"""
    letter = letter.strip().upper()
    n = 0
    for ch in letter:
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n
```

### 安全类型转换

```python
def safe_str(v) -> str:
    """安全转换为字符串"""
    if v is None:
        return ""
    return str(v).strip()

def parse_float(v) -> float:
    """安全转换为浮点数，失败返回0.0"""
    s = safe_str(v)
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0
```

### 日期解析

```python
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
```

### 跨平台打开文件

```python
def open_file(filepath):
    if sys.platform == 'darwin':
        subprocess.run(['open', filepath])
    elif sys.platform == 'win32':
        os.startfile(filepath)
    else:
        subprocess.run(['xdg-open', filepath])
```

## 模块化设计

### 按职责分离

| 模块 | 职责 | 公共API |
|------|------|---------|
| `constants.py` | 常量、工具函数 | `safe_str`, `parse_float`, `col_letter_to_index` |
| `config_manager.py` | 配置读写 | `ConfigManager` |
| `file_util.py` | 文件操作 | `FileUtil.select_files()`, `FileUtil.read_excel()` |
| `logger.py` | 日志处理 | `TextHandler`, `app_logger` |
| `date_splitter.py` | 日期拆分 | `DateSplitter.split_by_date()` |
| `monthly_agg.py` | 月度聚合 | `MonthlyAggregator.aggregate_all_months()` |
| `template_mapper.py` | 模板映射 | `TemplateMapper.map_and_fill()` |
| `data_processor.py` | 数据处理 | `ExcelWorker`, `SplitWorker` |

### 导入规范

```python
# 标准库
import os
import sys
import json
import re
import shutil
import threading
import time
import traceback
from datetime import datetime

# 第三方库
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

# 本地模块
from constants import safe_str, parse_float, col_letter_to_index
from logger import app_logger, TextHandler
```
