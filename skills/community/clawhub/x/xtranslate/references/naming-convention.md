# 命名规范

## 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| Python 模块 | 全小写，下划线分隔 | `file_handler.py`, `cad_handler.py` |
| 类文件 | PascalCase | `SKILL.md` |
| 配置文件 | 全小写 | `config.py`, `requirements.txt` |

## 代码命名

### 类名 - PascalCase
```python
class FileHandler:      # ✅
class CADHandler:       # ✅
class word_formatter:   # ❌
```

### 函数/方法 - snake_case
```python
def translate_text():           # ✅
def extract_keywords():         # ✅
def translateText():            # ❌
```

### 变量 - snake_case
```python
output_path = "output"          # ✅
file_handler = FileHandler()    # ✅
outputPath = "output"           # ❌
```

### 常量 - 全大写
```python
MAX_BATCH_SIZE = 10             # ✅
DEFAULT_ENGINE = "cloud"        # ✅
maxBatchSize = 10               # ❌
```

### 私有方法/变量 - 下划线前缀
```python
def _internal_method():         # 模块内部使用
self._private_var = value       # 类私有变量
```

## 命名建议

1. **描述性**: 名称应清晰表达用途
   - ✅ `extract_keywords()` 
   - ❌ `process()`

2. **避免缩写**: 除非是通用缩写
   - ✅ `configuration`
   - ❌ `cfg` (除非作为局部变量)

3. **动词开头**: 方法名使用动词
   - ✅ `get_output_dir()`, `translate_text()`
   - ❌ `output_dir()`, `text_translation()`
