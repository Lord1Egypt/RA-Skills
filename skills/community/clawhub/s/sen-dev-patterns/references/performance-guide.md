# 性能优化指南

本文档沉淀大数据处理和性能优化经验。

---

## 1. Excel读取优化

### read_only模式

```python
import openpyxl

# ❌ 错误：大文件慢，占用内存多
wb = openpyxl.load_workbook('large_file.xlsx')
ws = wb.active

# ✅ 正确：使用read_only模式，速度快3-5倍
wb = openpyxl.load_workbook('large_file.xlsx', read_only=True, data_only=True)
ws = wb.active
```

### 限制列范围

```python
# ❌ 错误：读取整张表
for row in ws.iter_rows(values_only=True):
    process(row)

# ✅ 正确：只读取需要的列
needed_cols = [1, 2, 5, 8, 12]  # A, B, E, H, L列
for row in ws.iter_rows(min_col=1, max_col=12, values_only=True):
    # 只处理需要的列
    selected = [row[i-1] for i in needed_cols if i <= len(row)]
    process(selected)
```

### 及时关闭

```python
import openpyxl

# ✅ 正确：使用完立即关闭
try:
    wb = openpyxl.load_workbook('file.xlsx', read_only=True)
    ws = wb.active
    # 处理数据...
finally:
    wb.close()
```

---

## 2. 分批处理大数据

### 批量处理模式

```python
def process_large_file(filepath, batch_size=1000, callback=None):
    """
    分批处理大文件
    
    Args:
        filepath: 文件路径
        batch_size: 每批处理行数
        callback: 每批处理完成后的回调函数
    """
    wb = openpyxl.load_workbook(filepath, read_only=True)
    ws = wb.active
    
    batch = []
    total_rows = 0
    
    for row in ws.iter_rows(values_only=True):
        batch.append(row)
        total_rows += 1
        
        if len(batch) >= batch_size:
            # 处理这一批数据
            process_batch(batch)
            
            # 回调通知进度
            if callback:
                callback(total_rows)
            
            # 清空批次，准备下一批
            batch = []
    
    # 处理剩余数据
    if batch:
        process_batch(batch)
        if callback:
            callback(total_rows)
    
    wb.close()
    return total_rows

def process_batch(batch):
    """处理单批数据"""
    for row in batch:
        # 处理逻辑
        pass
```

### 带进度条的批量处理

```python
from PySide6.QtCore import QThread, Signal

class BatchProcessor(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)
    
    def __init__(self, filepath, batch_size=1000):
        super().__init__()
        self.filepath = filepath
        self.batch_size = batch_size
    
    def run(self):
        try:
            total = process_large_file(
                self.filepath,
                self.batch_size,
                callback=lambda count: self.progress.emit(count)
            )
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
```

---

## 3. 内存优化

### 避免重复读取

```python
# ❌ 错误：多次读取同一文件
data1 = read_file('source.xlsx')
process1(data1)
data2 = read_file('source.xlsx')  # 重复读取
process2(data2)

# ✅ 正确：一次性读取，多次使用
data = read_file('source.xlsx')
process1(data)
process2(data)
```

### 使用生成器

```python
# ❌ 错误：一次性加载所有数据
def get_all_rows(filepath):
    wb = openpyxl.load_workbook(filepath, read_only=True)
    ws = wb.active
    return list(ws.iter_rows(values_only=True))

# ✅ 正确：使用生成器，按需加载
def iter_rows(filepath):
    wb = openpyxl.load_workbook(filepath, read_only=True)
    ws = wb.active
    try:
        for row in ws.iter_rows(values_only=True):
            yield row
    finally:
        wb.close()
```

### 及时释放大对象

```python
def process_with_cleanup(filepath):
    wb = None
    try:
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        # 处理...
    finally:
        if wb:
            wb.close()  # 确保释放
    # 此时wb已关闭，不再占用内存
```

---

## 4. 数据结构优化

### 使用dict而非list查找

```python
# ❌ 错误：O(n) 查找
for item in large_list:
    if item['id'] == target_id:
        return item

# ✅ 正确：O(1) 查找
lookup_dict = {item['id']: item for item in large_list}
return lookup_dict.get(target_id)
```

### 使用defaultdict聚合

```python
from collections import defaultdict

# ✅ 正确：使用defaultdict简化聚合
def aggregate_by_category(data):
    result = defaultdict(list)
    for item in data:
        result[item['category']].append(item)
    return dict(result)

# 而不是：
def aggregate_by_category(data):
    result = {}
    for item in data:
        if item['category'] not in result:
            result[item['category']] = []
        result[item['category']].append(item)
    return result
```

---

## 5. 跨平台路径处理

### 使用pathlib

```python
from pathlib import Path

# ✅ 正确：跨平台路径处理
script_dir = Path(__file__).parent
data_file = script_dir / 'data' / 'input.xlsx'

# 自动处理不同平台的斜杠
output_file = script_dir / 'output' / 'result.xlsx'

# 检查文件存在
if data_file.exists():
    print(f"文件存在: {data_file}")

# 获取绝对路径
abs_path = data_file.resolve()
```

### 路径工具函数

```python
import os
from pathlib import Path

def ensure_dir_exists(filepath):
    """确保目录存在"""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def get_safe_filename(filename):
    """生成安全的文件名"""
    # 移除不合法字符
    import re
    safe = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe

def get_file_size_mb(filepath):
    """获取文件大小（MB）"""
    size_bytes = os.path.getsize(filepath)
    return size_bytes / (1024 * 1024)
```

---

## 6. GUI性能优化

### 使用线程处理耗时任务

```python
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(int)
    
    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.task_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# 使用
worker = Worker(process_file, filepath)
worker.progress.connect(lambda p: progress_bar.setValue(p))
worker.finished.connect(lambda r: print(f"完成: {r}"))
worker.start()
```

### 批量更新UI

```python
# ❌ 错误：频繁更新UI
for item in large_list:
    update_ui(item)  # 每次都触发UI重绘

# ✅ 正确：批量更新
updates = []
for item in large_list:
    updates.append(prepare_update(item))

# 一次性应用所有更新
apply_all_updates(updates)
```

---

## 7. 性能监控

### 计时装饰器

```python
import time
from functools import wraps

def timing(func):
    """性能计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} 耗时: {end - start:.3f}秒")
        return result
    return wrapper

@timing
def process_data(data):
    """处理数据"""
    # ...
    pass
```

### 内存监控

```python
import psutil
import os

def get_memory_usage_mb():
    """获取当前进程内存使用（MB）"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def log_memory_usage():
    """记录内存使用"""
    mem_mb = get_memory_usage_mb()
    print(f"当前内存使用: {mem_mb:.2f} MB")
```

---

## 8. 常见性能问题速查

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| Excel读取慢 | 3秒以上 | 使用read_only=True |
| 内存占用高 | 1GB+ | 分批处理，及时close() |
| UI卡顿 | 点击无响应 | 使用QThread后台处理 |
| 查找慢 | O(n)遍历 | 用dict替代list |
| 重复读取 | 多次加载同一文件 | 一次性读取，缓存结果 |
| 字符串拼接慢 | 大量+=操作 | 使用join()或list append |
| 正则重复编译 | 每次调用都编译 | 使用re.compile()预编译 |
