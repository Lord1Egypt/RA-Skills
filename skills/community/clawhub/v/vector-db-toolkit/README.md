# Vector Database Toolkit

Vector database operations toolkit for AI/RAG applications.

## 功能 | Features

- 统一的向量数据库客户端 | Unified vector DB client
- 支持 Qdrant、Chroma、内存存储 | Supports Qdrant, Chroma, InMemory
- 嵌入向量工具 | Embedding utilities
- 语义搜索 | Semantic search
- 批量操作 | Batch operations

## 安装 | Installation

```bash
pip install -r requirements.txt
```

## 快速开始 | Quick Start

```python
from scripts.vector_client import VectorClient

# Qdrant
client = VectorClient(backend="qdrant", url="http://localhost:6333")
client.create_collection("articles", dimension=768)
client.upsert("articles", ids=["1"], vectors=[[0.1]*768], payloads=[{"title": "Hello"}])
results = client.search("articles", vector=[0.1]*768, top_k=5)
```

## 目录结构 | Structure

```
vector-db-toolkit/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── vector_client.py
│   ├── qdrant_client.py
│   ├── chroma_client.py
│   └── embedding_utils.py
├── examples/
│   └── basic_usage.py
└── tests/
    └── test_vector_client.py
```
