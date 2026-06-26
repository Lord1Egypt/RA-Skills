# 离线部署指南

## 概述

Agent Memory 系统支持在无网络连接的环境中运行。核心功能（记忆写入、关键词检索、上下文构建、结构化编码、去重过滤、情感分析、时间旅行、因果链）不依赖任何外部服务。

## 环境变量配置

```bash
# 禁用需要网络/模型的功能
export AGENT_MEMORY_DISABLE_SEMANTIC=true
export AGENT_MEMORY_DISABLE_DISTILLATION=true

# API 密钥（从环境变量读取，不再硬编码）
export SILICONFLOW_API_KEY=""           # 留空表示不使用 LLM
export AGENT_MEMORY_ADMIN_PASSWORD="your-secure-password"  # 管理员密码
```

## 离线功能对照

| 功能 | 在线模式 | 离线模式 | 替代方案 |
|------|---------|---------|----------|
| 语义搜索 | sqlite-vec 向量检索 | 关键词搜索 (LIKE) | 结构化检索 |
| 向量相似度 | 余弦相似度 | 不可用 | FTS5 / LIKE |
| LLM 蒸馏 | LLM 生成摘要 | 不可用 | 启发式摘要 |
| Reranker | 交叉编码器精排 | 不可用 | 分数排序 |
| 情感分析 | 规则 + LLM | 纯规则模式 | 词典匹配 |
| 元认知 | 规则 + LLM | 纯规则模式 | 关键词扩展 |

## 保留的核心功能

- 记忆写入（过滤 → 清洗 → 去重 → 编码 → 存储）
- 关键词检索（FTS5 / LIKE 降级）
- 上下文构建
- 结构化 6 维编码
- 去重过滤
- 情感分析（纯规则）
- 时间旅行（快照/Diff/Blame）
- 因果链（规则层）
- 记忆衰减与归档
- 自我修复

## 离线依赖安装

在离线环境中，需要提前准备以下依赖包：

```bash
# 在有网络的机器上下载
pip download sqlite-vec -d ./offline_packages/
pip download sentence-transformers -d ./offline_packages/

# 传输到离线服务器后安装
pip install --no-index --find-links=./offline_packages/ sqlite-vec
```

## Embedding 模型离线部署

sentence-transformers 模型需要从 HuggingFace 预下载：

```bash
# 在有网络的机器上下载模型
python3 -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
model.save('./offline_model/')
"

# 将 offline_model/ 目录传输到离线服务器
# 设置模型路径
export AGENT_MEMORY_EMBEDDING_MODEL_PATH="./offline_model/"
```

## 在 OpenClaw 中使用

```python
import sys
from pathlib import Path

plugin_dir = Path("/home/admin/.openclaw/plugins/agent_memory")
sys.path.insert(0, str(plugin_dir))

from memory_bridge import get_memory_bridge

memory = get_memory_bridge()
memory.remember("这是测试内容")
results = memory.recall("测试")
context = memory.build_context("用户的问题")
```

## 验证离线模式

```bash
cd /path/to/agent_memory
python3 -c "
from memory_system import AgentMemory
mem = AgentMemory(db_path='test.db', enable_semantic=False)
result = mem.remember('测试记忆')
print('写入:', result.get('written', False))
results = mem.recall('测试')
print('检索:', len(results.get('primary', [])), '条')
"
```
