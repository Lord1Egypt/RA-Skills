# 优秀代码示例

## 1. 批量翻译处理

```python
# translator.py - 智能批处理实现
def translate_list(self, text_list):
    """批量翻译文本列表"""
    # 过滤空行并记录原始索引
    indexed_texts = [(i, text) for i, text in enumerate(text_list) if text.strip()]
    
    results = [""] * len(text_list)
    
    # 批处理逻辑仅适用于 AI 模型
    if self.engine in ["cloud", "ollama"]:
        batches = []
        batch = []
        batch_indices = []
        current_len = 0
        
        # 从配置中获取对应引擎的批处理参数
        engine_cfg = CONFIG.get("BATCH_CONFIG", {}).get(self.engine, {"max_len": 1000, "max_count": 10})
        MAX_LEN = engine_cfg.get("max_len", 1000)
        MAX_COUNT = engine_cfg.get("max_count", 10)
        
        # 智能分批：同时满足长度和数量限制
        for idx, text in indexed_texts:
            text_len = len(text)
            if current_len + text_len > MAX_LEN or len(batch) >= MAX_COUNT:
                batches.append((batch, batch_indices))
                batch = []
                batch_indices = []
                current_len = 0
            
            batch.append(text)
            batch_indices.append(idx)
            current_len += text_len + 20
        
        if batch:
            batches.append((batch, batch_indices))
        
        # 批量翻译
        total_batches = len(batches)
        for i, (b, b_idx) in enumerate(batches):
            process_batch(b, b_idx, i + 1, total_batches)
    
    return results
```

**优点**:
- 智能分批策略，平衡效率和质量
- 从配置动态读取参数，不同引擎不同策略
- 保留原始索引，确保结果顺序正确

## 2. 格式保留翻译

```python
# file_handler.py - Word 翻译保留格式
def translate_docx_in_place(file_path, translator, output_path):
    """翻译 docx 文件并保留原格式"""
    doc = Document(file_path)
    
    # 1. 收集所有需要翻译的文本对象
    all_elements = []
    
    # 处理正文段落
    for p in doc.paragraphs:
        if p.text.strip():
            all_elements.append(p)
    
    # 处理表格内容
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text.strip():
                        all_elements.append(p)
    
    # 2. 提取文本并批量翻译
    texts_to_translate = [e.text for e in all_elements]
    translated_texts = translator.translate_list(texts_to_translate)
    
    # 3. 将翻译后的文本写回
    for element, translated_text in zip(all_elements, translated_texts):
        element.text = translated_text
    
    # 4. 保存
    doc.save(output_path)
    return output_path
```

**优点**:
- 统一收集所有文本元素，确保不遗漏
- 批量翻译提高效率
- 直接修改元素 text 属性，保留所有格式

## 3. 关键词引导翻译

```python
# analyzer.py - 专业术语提取
class TextAnalyzer:
    @staticmethod
    def extract_keywords(text, top_k=50):
        """提取文本中的前 K 个关键名词"""
        if not text:
            return []
        
        # 预处理：移除多余空白和非文字字符
        clean_text = re.sub(r'[^\w\s]', ' ', text)
        
        # 使用 jieba 提取名词相关词性
        allow_pos = ('n', 'nr', 'nz', 'nt', 'nw', 'v')
        keywords = jieba.analyse.extract_tags(
            text, 
            topK=top_k, 
            withWeight=False, 
            allowPOS=allow_pos
        )
        return keywords
```

**优点**:
- 使用 jieba 进行中文分词和词性标注
- 提取名词和专业术语，过滤无意义词汇
- 将关键词注入翻译 prompt，提升专业翻译质量
