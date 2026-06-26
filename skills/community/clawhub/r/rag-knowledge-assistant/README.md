# RAG 知识库助手 (rag-knowledge-assistant)

基于向量数据库的智能知识库检索系统，支持语义理解和多格式文档处理。

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **语义检索** | 基于向量相似度，理解问题意图而非仅关键词匹配 |
| **多格式支持** | PDF、Word(.docx)、Excel(.xlsx)、Markdown、TXT |
| **智能分块** | 自动文本分割 (500 字/块，重叠 50 字) 保持上下文完整 |
| **溯源引用** | 回答标注来源文件和位置 |
| **本地部署** | 使用 Ollama + Chroma，无需云服务 |

## 🚀 快速开始

### 1. 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 2. 准备知识库

将文档放入 `knowledge` 目录：

```
knowledge/
├── company-policies/
│   ├── 员工手册.pdf
│   ├── 考勤制度.docx
│   └── 报销流程.pdf
└── product-docs/
    ├── API 文档.md
    └── 产品说明.pdf
```

### 3. 构建索引

```bash
# 使用 Ollama Embedding (推荐)
python index_knowledge_ollama.py --knowledge-dir ./knowledge --output-dir ./vectorstore

# 或使用 HuggingFace 模型
python index_knowledge.py --knowledge-dir ./knowledge --output-dir ./vectorstore
```

### 4. 测试检索

```bash
# 交互模式
python rag_query_ollama.py --interactive --vectorstore ./vectorstore

# 单次查询
python rag_query_ollama.py "公司年假是怎么规定的？" --vectorstore ./vectorstore
```

## 📁 目录结构

```
rag-knowledge-assistant/
├── scripts/                    # 核心脚本
│   ├── index_knowledge.py      # 索引构建 (HuggingFace)
│   ├── index_knowledge_ollama.py  # 索引构建 (Ollama)
│   ├── rag_query.py            # 向量检索 (HuggingFace)
│   ├── rag_query_ollama.py     # 向量检索 (Ollama)
│   ├── requirements.txt        # Python 依赖
│   └── setup.bat               # Windows 安装脚本
├── references/                 # 参考文档
│   ├── pdf_reading.md
│   ├── excel_reading.md
│   └── excel_analysis.md
├── rag-config.yaml             # 配置文件模板
├── SKILL.md                    # OpenClaw 技能定义
└── README.md                   # 本文件
```

## 🔧 配置

编辑 `rag-config.yaml` 调整参数：

```yaml
rag:
  vectorstore:
    type: chroma
    persist_directory: ./vectorstore
  
  embedding:
    type: ollama
    model: nomic-embed-text-v2-moe  # 或 BAAI/bge-m3
  
  retrieval:
    top_k: 5
    distance_threshold: 200.0  # L2 距离阈值
  
  chunking:
    chunk_size: 500
    chunk_overlap: 50
```

## 📊 支持的 Embedding 模型

### 本地模型 (Ollama)

```bash
# 安装模型
ollama pull nomic-embed-text-v2-moe
ollama pull mxbai-embed-large
```

### HuggingFace 模型

- `BAAI/bge-m3` - 中英双语，推荐
- `shibing624/text2vec-base-chinese` - 纯中文
- `all-MiniLM-L6-v2` - 英文

## 💡 使用示例

### 企业制度问答

```python
# 查询考勤制度
python rag_query_ollama.py "上班时间是几点？" --vectorstore ./vectorstore

# 查询车辆管理
python rag_query_ollama.py "公车怎么申请？" --vectorstore ./vectorstore

# 查询报销流程
python rag_query_ollama.py "出差报销需要什么材料？" --vectorstore ./vectorstore
```

### 回答格式

```
根据公司《考勤管理制度》规定：

工作时间：周一至周五
- 上午 8:00-12:00
- 下午 13:00-17:00

打卡制度：一日两次指纹打卡

📄 来源：公司考勤管理制度.docx - 第 3 章
```

## 🔗 OpenClaw 集成

将此技能安装到 OpenClaw：

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/AIxbinge/rag-knowledge-assistant.git ~/.openclaw/skills/rag-knowledge-assistant

# 或在 OpenClaw 中
openclaw skills install rag-knowledge-assistant
```

然后在对话中使用：
```
从知识库查一下公司年假规定
检索文档：车辆管理制度
```

## 🛠️ 故障排查

### 检索结果为空

1. 检查向量库是否存在：`dir ./vectorstore`
2. 降低阈值重试：`python rag_query_ollama.py "问题" -t 300`
3. 重新构建索引：`python index_knowledge_ollama.py --rebuild`

### Ollama 连接失败

```bash
# 启动 Ollama 服务
ollama serve

# 检查模型
ollama list
```

### 依赖问题

```bash
# 重新安装依赖
pip install -r requirements.txt --upgrade
```

## 📝 最佳实践

### ✅ 推荐

1. 文档按主题分类存放
2. 使用中文 Embedding 模型（BGE-M3 或 nomic-embed-text-v2-moe）
3. 定期更新索引（新增文档后）
4. 回答时始终标注来源

### ❌ 避免

1. 索引超大单文件（建议拆分为主题文档）
2. 忽略阈值设置（导致低质量匹配）
3. 直接检索扫描件 PDF（需先 OCR）

## 📄 许可证

MIT License

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain)
- [Chroma](https://github.com/chroma-core/chroma)
- [Ollama](https://github.com/ollama/ollama)
- [BGE-M3](https://huggingface.co/BAAI/bge-m3)
