# 反模式示例（避免这样写）

## 1. 逐条翻译而非批量

```python
# ❌ 错误：逐条翻译，效率低下
for paragraph in doc.paragraphs:
    if paragraph.text.strip():
        translated = translator.translate_text(paragraph.text)
        paragraph.text = translated

# ✅ 正确：收集后批量翻译
all_texts = [p.text for p in doc.paragraphs if p.text.strip()]
translated_list = translator.translate_list(all_texts)
for p, t in zip(doc.paragraphs, translated_list):
    p.text = t
```

## 2. 硬编码配置

```python
# ❌ 错误：硬编码参数
MAX_LEN = 1500
MAX_COUNT = 10

# ✅ 正确：从配置读取
engine_cfg = CONFIG.get("BATCH_CONFIG", {}).get(self.engine, {})
MAX_LEN = engine_cfg.get("max_len", 1000)
MAX_COUNT = engine_cfg.get("max_count", 10)
```

## 3. 忽略错误处理

```python
# ❌ 错误：无错误处理
def read_docx(file_path):
    doc = Document(file_path)
    return [p.text for p in doc.paragraphs]

# ✅ 正确：添加异常处理
def read_docx(file_path):
    try:
        doc = Document(file_path)
        return [p.text for p in doc.paragraphs if p.text.strip()]
    except Exception as e:
        print(f"[错误] 读取文件失败: {e}")
        return []
```

## 4. 明文存储敏感信息

```python
# ❌ 错误：明文存储 API Key
CONFIG = {
    "API_KEY": "sk-xxx123456"
}

# ✅ 正确：加密存储
from crypto_utils import crypto
CONFIG = {
    "API_KEY": crypto.encrypt("sk-xxx123456")  # 存储密文
}
# 使用时解密
api_key = crypto.decrypt(CONFIG["API_KEY"])
```

## 5. 混合 UI 和业务逻辑

```python
# ❌ 错误：GUI 中直接处理文件
def start_translation(self):
    for file_path in self.files:
        doc = Document(file_path)
        # ... 翻译逻辑
        doc.save(output_path)

# ✅ 正确：调用独立模块
def start_translation(self):
    from main import process_file
    for file_path in self.files:
        success, result = process_file(file_path, engine_type=engine)
```

## 6. 不保留原文档结构

```python
# ❌ 错误：只提取纯文本，丢失格式
text = "\n".join([p.text for p in doc.paragraphs])
translated = translator.translate(text)
new_doc.add_paragraph(translated)

# ✅ 正确：逐元素翻译，保留格式
for p in doc.paragraphs:
    p.text = translator.translate_text(p.text)
```
