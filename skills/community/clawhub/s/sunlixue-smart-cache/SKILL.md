---
name: smart-cache
description: 本地智能缓存系统，为AI助手提供语义级别的请求缓存。当用户需要(1)减少重复API调用成本、(2)加速相似问题的响应、(3)创建本地缓存层来优化AI助手性能时使用此技能。支持精确匹配(L1)和语义相似匹配(L2)两种缓存模式。
---

# Smart Cache - 本地智能缓存系统

## 概述

Smart Cache 是一个为 OpenClaw/QClaw 设计的本地智能缓存系统，通过缓存 AI 响应来减少 API 调用成本和响应时间。

**核心功能：**
- L1 精确缓存：完全相同的请求直接返回缓存结果
- L2 语义缓存：语义相似的请求返回相似结果（基于向量嵌入）
- 缓存管理：自动过期、容量限制、手动清理
- 成本追踪：记录节省的 token 和费用
- MCP 协议接口：支持与其他 AI 工具集成

## 快速开始

### 检查缓存状态

```python
python scripts/cache_manager.py status
```

### 查询缓存

```python
# 精确查询
python scripts/cache_manager.py query "你好，今天天气怎么样？"

# 语义查询（返回相似度 > 0.85 的结果）
python scripts/cache_manager.py query-semantic "今天天气如何？" --threshold 0.85
```

### 添加缓存

```python
python scripts/cache_manager.py add "你好" "你好！有什么可以帮助你的吗？"
```

### 清理缓存

```python
# 清理过期缓存
python scripts/cache_manager.py clean --expired

# 清理全部
python scripts/cache_manager.py clean --all

# 清理特定时间范围
python scripts/cache_manager.py clean --before "2024-01-01"
```

## 缓存模式

### L1 精确缓存 (Exact Cache)

适用于完全相同的请求。使用 SHA256 哈希作为 key，O(1) 查找时间。

**特点：**
- 100% 准确率，零误判
- 适用于重复性问题

**示例：**
```
用户: "什么是Python？"
→ 缓存命中 → 直接返回缓存的回答
```

### L2 语义缓存 (Semantic Cache)

适用于语义相似但不完全相同的请求。**需要配置 embedding API** 才能启用。

**工作原理：**
1. 将查询文本转换为向量嵌入（需要 API Key）
2. 在缓存中查找与查询向量相似度最高的条目
3. 返回相似度超过阈值的缓存结果

**特点：**
- 支持 OpenAI、DashScope（阿里云）、本地模型三种 embedding 来源
- 基于余弦相似度匹配
- 可配置阈值（默认 0.85）

**示例：**
```
缓存: "今天天气怎么样？" → "今天晴天，气温25度..."
查询: "今天天气如何？"
→ 相似度 0.92 → 返回缓存的回答
```

**注意：** L2 语义匹配需要 embedding API 支持（详见配置说明）。

## 配置

配置文件位于 `~/.qclaw/smart-cache/config.json`：

```json
{
  "cache_dir": "~/.qclaw/smart-cache/data",
  "l1_max_size": 10000,
  "l2_max_size": 5000,
  "ttl_hours": 168,
  "similarity_threshold": 0.85,
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "api_key": "your-api-key",
  "enable_cost_tracking": true
}
```

**配置说明：**
| 参数 | 默认值 | 说明 |
|:---|:---|:---|
| `l1_max_size` | 10000 | L1 缓存最大条目数 |
| `l2_max_size` | 5000 | L2 缓存最大条目数 |
| `ttl_hours` | 168 | 缓存过期时间（小时），约 7 天 |
| `similarity_threshold` | 0.85 | L2 语义匹配阈值（0-1） |
| `embedding_provider` | openai | embedding 提供者：`openai`、`dashscope`、`local` |
| `embedding_model` | text-embedding-3-small | embedding 模型名称 |
| `api_key` | - | API Key（支持 OPENAI_API_KEY / DASHSCOPE_API_KEY 环境变量） |
| `enable_cost_tracking` | true | 是否启用成本追踪 |

### Embedding Provider 配置

**OpenAI（推荐）：**
```json
{
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "api_key": "sk-..."
}
```

**阿里云 DashScope：**
```json
{
  "embedding_provider": "dashscope",
  "embedding_model": "text-embedding-v1",
  "api_key": "your-dashscope-key"
}
```

**本地模型（无需 API Key）：**
```json
{
  "embedding_provider": "local",
  "embedding_model": "all-MiniLM-L6-v2"
}
```
本地模型需要安装：`pip install sentence-transformers`

## 成本追踪

查看节省的成本：

```python
python scripts/cache_manager.py stats
```

输出示例：
```
📊 缓存统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━
总请求数: 1,234
L1命中: 456 (37%)
L2命中: 189 (15%)
缓存未命中: 589 (48%)

💰 成本节省
━━━━━━━━━━━━━━━━━━━━━━━━━━━
节省Token: 89,234
估算节省: $0.27
```

## 集成到 OpenClaw

### 方法1：作为 MCP Server 运行

MCP Server 支持 stdio 和 HTTP 两种模式。

**stdio 模式（推荐，用于 OpenClaw）：**
```python
python scripts/mcp_server.py --mode stdio
```

**HTTP 模式（用于其他工具）：**
```python
python scripts/mcp_server.py --mode http --port 8080
```

### 方法2：直接 API 调用

```python
from scripts.cache_api import SmartCache

cache = SmartCache()

# 查询缓存
result = cache.query("用户的问题")
if result:
    print(f"缓存命中！相似度: {result.similarity}")
    print(f"回答: {result.response}")
else:
    # 调用实际API
    response = call_llm_api("用户的问题")
    # 存入缓存
    cache.store("用户的问题", response)
```

## 脚本说明

### scripts/cache_manager.py

主缓存管理工具，提供命令行接口：
- `status` - 查看缓存状态
- `query` - 精确查询
- `query-semantic` - 语义查询（L2，需要 embedding 配置）
- `add` - 添加缓存条目
- `clean` - 清理缓存
- `stats` - 查看统计信息

### scripts/cache_api.py

Python API 模块，提供编程接口：
- `SmartCache` - 主缓存类
- `CacheEntry` - 缓存条目类
- `CacheStats` - 统计信息类

### scripts/embeddings.py

向量嵌入工具，支持多种 embedding 来源：
- `OpenAIEmbeddings` - OpenAI Embedding API
- `DashScopeEmbeddings` - 阿里云 DashScope API
- `LocalEmbeddings` - 本地 sentence-transformers 模型

用法示例：
```python
from scripts.embeddings import get_text_embedding, compute_similarity

# 获取单条文本的嵌入向量
emb = get_text_embedding("你好")

# 计算两条文本的相似度
sim = compute_similarity("今天天气怎么样", "今天天气好吗")
```

### scripts/mcp_server.py

MCP 协议服务器，支持与其他 AI 工具集成：
- `stdio` 模式：用于 OpenClaw MCP 集成
- `http` 模式：用于其他支持 HTTP 的工具

## 最佳实践

1. **合理设置 TTL**：根据内容更新频率设置过期时间
   - 事实性内容：7 天
   - 时效性内容：1-24 小时
   - 永久性内容：30 天

2. **L2 语义缓存需要 API Key**：如果未配置 embedding，L2 查询会使用字符级 Jaccard 作为后备方案

3. **调整相似度阈值**：
   - 严格匹配：0.95
   - 常规使用：0.85
   - 宽松匹配：0.75

4. **定期清理**：
   ```bash
   # 每周清理一次过期缓存
   0 0 * * 0 python ~/.qclaw/smart-cache/scripts/cache_manager.py clean --expired
   ```

5. **监控缓存效果**：
   - 命中率 > 30% 表示缓存有效
   - 命中率 < 10% 考虑调整阈值或 TTL

## 故障排除

### 缓存未命中率高

1. 检查相似度阈值是否过高
2. 确认缓存容量是否足够
3. 检查 TTL 设置是否过短

### 语义匹配不准确

1. 确认已配置 embedding API（检查 config.json 中的 `api_key`）
2. 尝试不同的 embedding 模型
3. 调整相似度阈值

### API Key 相关错误

1. 确认在 `~/.qclaw/smart-cache/config.json` 中配置了 `api_key`
2. 或设置环境变量 `OPENAI_API_KEY` / `DASHSCOPE_API_KEY`
3. 检查 API Key 是否有效、未过期

### 磁盘空间问题

1. 减小缓存容量（`l1_max_size`、`l2_max_size`）
2. 缩短 TTL（`ttl_hours`）
3. 定期运行清理：`cache_manager.py clean --expired`

## 资源

### scripts/
- `cache_manager.py` - 命令行管理工具
- `cache_api.py` - Python API 模块
- `mcp_server.py` - MCP 协议服务器
- `embeddings.py` - 向量嵌入工具

### references/
- `api_reference.md` - API 详细文档

### assets/
- `config_template.json` - 配置文件模板
