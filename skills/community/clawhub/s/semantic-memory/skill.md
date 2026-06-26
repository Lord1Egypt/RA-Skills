---
name: semantic-memory
description: "OpenClaw Agent 中文长期记忆系统。jieba TF-IDF + 向量检索三轨混合，中文语义优先，支持多Agent记忆协同。触发词：向量数据库、记忆检索、长期记忆、语义搜索、vector search、memory retrieval"
---

# Semantic Memory — 中文语义记忆系统

> OpenClaw Agent 中文长期记忆基础设施 | v1.0.0

## 技能概述

为 OpenClaw Agent 打造的中文长期记忆检索系统。三大核心创新：

1. **中文语义优先**：jieba TF-IDF 替代纯向量检索，中文理解大幅提升
2. **混合三轨**：TF-IDF × 向量 × 关键词加权，实测 100% 命中率
3. **Agent 自动路由**：自动识别意图路由到对应 memory collection

## 核心文件

| 文件 | 用途 |
|------|------|
| `scripts/vector_search.py` | ⭐ 核心检索脚本 |
| `scripts/import_memory.py` | ⭐ 记忆导入脚本 |
| `scripts/start_chroma.sh` | ChromaDB 服务启动脚本 |
| `README.md` | 完整项目文档 |

## 快速开始

### 1. 安装依赖

```bash
pip install chromadb jieba
```

### 2. 启动 ChromaDB

```bash
chroma run --path ./vector_db --host 0.0.0.0 --port 8000 &
```

### 3. 导入记忆

```bash
python3 scripts/import_memory.py
```

### 4. 检索

```bash
python3 scripts/vector_search.py "你的查询"
```

## 工作流程

```
用户查询
    │
    ▼
Agent 自动路由（关键词匹配 collection）
    │
    ▼
TF-IDF 预计算索引（jieba 分词）
    ├─→ 中文语义相似度（主要）
    │
ChromaDB 向量检索
    ├─→ 语义扩展（补充）
    │
关键词命中加权（source 标题匹配）
    │
    ▼
综合评分 = 0.45×向量 + 0.55×TF-IDF + boost
    │
    ▼
输出 Top 6 结果
```

## API 用法

```python
import sys
sys.path.insert(0, 'scripts')
from vector_search import search

results = search("跌倒检测老人", topk=6)
for r in results:
    print(r['source'], r['combined'], r['doc'][:100])
```

## 配置

### Agent 路由规则

修改 `scripts/vector_search.py` 中的：

```python
AGENT_KEYWORDS = {
    '你的Agent': ['关键词1', '关键词2'],
}
AGENT_COLLECTION = {'你的Agent': 'projects'}
```

### 权重调整

```python
combined = 0.45 * vec_sim + 0.55 * tfidf_norm + boost
# 调高 0.55 → 更注重中文关键词精确匹配
# 调高 0.45 → 更注重语义扩展
```

## 性能基准

| 指标 | 数值 |
|------|------|
| 中文查询命中率 | **100%**（10/10） |
| 平均响应速度 | **0.8 秒/次** |
| 支持中文 | ✅ jieba 分词 |
| 多 Agent 支持 | ✅ 自动路由 |
| 无 Docker/GPU | ✅ 纯 pip |

## 技术栈

- ChromaDB 1.0（向量数据库）
- jieba 0.42（中文分词）
- Python 3.10+

## 已知限制

- embedding 模型为英文（all-MiniLM-L6-v2），中文语义主要靠 TF-IDF 弥补
- ChromaDB 跨机器文件共享需配置 API 认证
- 缓存基于文件路径，Windows 兼容性未测试

## License

MIT — 署名即可，欢迎使用和二次开发。
