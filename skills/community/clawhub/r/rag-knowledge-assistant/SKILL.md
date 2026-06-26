---
name: rag-knowledge-assistant
description: 基于向量数据库的 RAG(检索增强生成) 知识库助手。支持语义检索、多格式文档 (PDF/Word/Excel/Markdown) 处理、智能问答。使用 Chroma 向量库 + BGE-M3 Embedding 模型。适用于从 knowledge 目录快速检索信息、回答基于文档的问题。触发词："从知识库查"、"检索文档"、"RAG 查询"、"向量搜索"、"语义检索"等。
---

# RAG 知识库检索助手 (rag-knowledge-assistant)

基于向量数据库的智能知识库检索系统，支持语义理解和多格式文档处理。

## 核心能力

| 特性 | 说明 |
|------|------|
| **语义检索** | 基于向量相似度，理解问题意图而非仅关键词匹配 |
| **多格式支持** | PDF、Word(.docx)、Excel(.xlsx)、Markdown、TXT |
| **智能分块** | 自动文本分割 (500 字/块，重叠 50 字) 保持上下文完整 |
| **溯源引用** | 回答标注来源文件和位置 |
| **多轮迭代** | 最多 5 轮检索，逐步缩小范围 |

## 快速开始

### 首次使用：构建索引

```bash
# 1. 安装依赖 (首次使用)
cd scripts
pip install -r requirements.txt

# 2. 创建知识库索引 (确保 knowledge 目录有文档)
python index_knowledge.py --knowledge-dir ../../knowledge --output-dir ../../vectorstore

# 3. 验证索引
python rag_query.py "测试问题" --interactive
```

### 日常使用

直接向 AI 提问，AI 会自动使用 RAG 检索：

```
问：公司的年假政策是怎么规定的？
问：帮我查一下产品 API 的认证方式
问：XSS 攻击有哪些防护措施？
```

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  用户提问   │ →  │  向量检索   │ →  │  智能回答   │
└─────────────┘    └─────────────┘    └─────────────┘
                          ↓
                   ┌─────────────┐
                   │  溯源引用   │
                   └─────────────┘
```

### 1. 理解用户需求

从问题中提取：
- **主题/领域**：如"年假政策"、"API 认证"、"安全防护"
- **限定条件**：如"2024 年"、"最新版本"、"技术部门"
- **期望输出**：解释、摘要、具体数值、操作步骤

### 2. 向量相似度检索

使用 Embedding 模型将问题转换为向量，在向量库中查找最相似的文档片段：

```python
# 内部执行逻辑
query_vector = embeddings.embed_query(user_question)
results = vectorstore.similarity_search_with_score(query_vector, k=5)
```

**检索参数**：
- `top_k`: 返回最相关的 5 个片段
- `score_threshold`: 相似度阈值 0.6 (60%)
- 低于阈值的片段会被过滤

### 3. 答案组织与溯源

综合检索结果，生成回答：

**回答结构**：
1. **直接回答** - 简洁明确的结论
2. **详细说明** - 基于文档的展开说明
3. **来源标注** - 引用文档名称和位置

**示例回答格式**：
```
根据公司《员工手册》第 3 章规定：

员工年假天数根据工龄计算：
- 工龄 1-3 年：5 天/年
- 工龄 3-5 年：7 天/年
- 工龄 5-10 年：10 天/年
- 工龄 10 年以上：15 天/年

📄 来源：hr-policies/员工手册.pdf - 第 12 页
```

## 知识库管理

### 目录结构

```
knowledge/                    # 知识库根目录
├── data_structure.md         # 目录索引 (可选)
├── company-policies/         # 公司制度
│   ├── 员工手册.pdf
│   ├── 考勤制度.docx
│   └── 薪酬福利.pdf
├── product-docs/             # 产品文档
│   ├── API 文档.md
│   └── 产品说明.pdf
└── technical/                # 技术资料
    ├── 架构设计.md
    └── 安全规范.pdf
```

### 添加新文档

```bash
# 1. 将文档放入 knowledge 目录
copy 新文档.pdf ./knowledge/company-policies/

# 2. 重新构建索引 (或使用增量索引)
python index_knowledge.py --knowledge-dir ./knowledge --rebuild

# 3. 验证
python rag_query.py "新文档相关内容"
```

### 索引配置

编辑 `rag-config.yaml` 调整参数：

```yaml
rag:
  vectorstore:
    persist_directory: ./vectorstore
  
  embedding:
    model: BAAI/bge-m3  # 中文推荐
    device: cpu
  
  retrieval:
    top_k: 5
    score_threshold: 0.6
  
  chunking:
    chunk_size: 500
    chunk_overlap: 50
```

## 高级用法

### 多知识库检索

配置多个知识库目录：

```yaml
knowledge_bases:
  - name: company
    path: ./knowledge/company
    description: 公司文档
  
  - name: personal
    path: ./knowledge/personal
    description: 个人笔记
  
  - name: project
    path: ./knowledge/project-alpha
    description: 项目 Alpha 文档
```

查询时指定知识库：
```
问：从公司知识库查一下报销流程
问：在 project 知识库里找 API 设计文档
```

### 调整检索精度

**提高精度** (减少误匹配)：
```yaml
retrieval:
  score_threshold: 0.75  # 提高阈值
  top_k: 3               # 减少返回数量
```

**提高召回** (减少遗漏)：
```yaml
retrieval:
  score_threshold: 0.5   # 降低阈值
  top_k: 10              # 增加返回数量
```

### 使用不同的 Embedding 模型

**中文场景推荐**：
```yaml
embedding:
  model: BAAI/bge-m3      # 中英双语，效果好
  # model: shibing624/text2vec-base-chinese  # 纯中文
```

**英文场景**：
```yaml
embedding:
  model: text-embedding-3-small  # OpenAI
  # model: all-MiniLM-L6-v2      # Sentence Transformers
```

## 故障排查

### 问题：检索结果为空

**可能原因**：
1. 向量库未创建或为空
2. 问题与文档内容差异太大
3. 阈值设置过高

**解决方案**：
```bash
# 检查向量库是否存在
dir ./vectorstore

# 降低阈值重试
python rag_query.py "问题" --score-threshold 0.4

# 查看已索引的文档
cat ./vectorstore/index_config.json
```

### 问题：回答不准确

**可能原因**：
1. 文档分块不合理
2. 检索到的片段不相关
3. 文档内容本身不准确

**解决方案**：
```yaml
# 调整分块参数
chunking:
  chunk_size: 300    # 减小分块
  chunk_overlap: 100 # 增加重叠

# 或更换 Embedding 模型
embedding:
  model: BAAI/bge-large-zh  # 更大的中文模型
```

### 问题：索引速度慢

**优化建议**：
1. 使用 GPU 加速 (如有)
2. 减少不必要的文档格式
3. 增量索引而非全量重建

```yaml
# 使用 GPU (如有 NVIDIA 显卡)
embedding:
  device: cuda

# 仅索引特定格式
# 在 index_knowledge.py 中注释掉不需要的加载器
```

## 与其他工具协同

### 保留关键词检索

对于精确匹配场景，仍可结合 grep：

```bash
# 向量检索 + 关键词验证
python rag_query.py "API 认证"
grep -r "authentication" ./knowledge/**/*.md
```

### PDF 处理增强

复杂 PDF (扫描件、图片) 需要 OCR：

```python
# 使用 pdfplumber 处理表格
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        text = page.extract_text()
```

## 最佳实践

### ✅ 推荐做法

1. **文档结构化** - 按主题分类存放，添加 data_structure.md 索引
2. **定期更新索引** - 新增文档后及时重建索引
3. **使用中文 Embedding** - BGE-M3 对中文理解更好
4. **标注来源** - 回答时始终注明文档来源
5. **多轮迭代** - 首次检索不足时，调整关键词再试

### ❌ 避免做法

1. ❌ 索引超大单文件 (建议拆分为主题文档)
2. ❌ 忽略阈值设置 (导致低质量匹配)
3. ❌ 混合多语言文档 without 多语言 Embedding
4. ❌ 直接检索扫描件 PDF (需先 OCR)

## 性能指标

基于典型知识库的测试数据：

| 指标 | 数值 |
|------|------|
| 索引速度 | ~10 文档/分钟 (CPU) |
| 检索延迟 | <1 秒 (5000+ 片段) |
| 准确率 | 85%+ (明确问题时) |
| Token 消耗 | 2K-5K/问答 |

## 命令参考

### 索引命令

```bash
# 基本用法
python index_knowledge.py

# 指定目录
python index_knowledge.py -k ./knowledge -o ./vectorstore

# 强制重建
python index_knowledge.py --rebuild

# 调整分块
python index_knowledge.py --chunk-size 300 --chunk-overlap 100
```

### 查询命令

```bash
# 单次查询
python rag_query.py "你的问题"

# 交互模式
python rag_query.py --interactive

# 调整参数
python rag_query.py "问题" -k 10 -t 0.5

# JSON 输出
python rag_query.py "问题" --json
```

## 配置示例

完整的 `rag-config.yaml`：

```yaml
rag:
  enabled: true
  
  vectorstore:
    type: chroma
    persist_directory: ./vectorstore
  
  embedding:
    type: huggingface
    model: BAAI/bge-m3
    device: cpu
  
  retrieval:
    top_k: 5
    score_threshold: 0.6
    include_metadata: true
  
  chunking:
    chunk_size: 500
    chunk_overlap: 50
  
  knowledge_bases:
    - name: default
      path: ./knowledge
      description: 默认知识库
      enabled: true

logging:
  level: INFO
  file: ./logs/rag.log
```

---

## 参考资料

- `scripts/index_knowledge.py` - 索引构建脚本
- `scripts/rag_query.py` - 向量检索脚本
- `scripts/requirements.txt` - Python 依赖
- `rag-config.yaml` - 配置文件模板
- `references/pdf_reading.md` - PDF 处理指南
- `references/excel_reading.md` - Excel 读取指南
