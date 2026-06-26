# Sophie Mem0 - 智能记忆系统

> 企业级长期记忆系统，为OpenClaw Agent提供持久化语义记忆能力

## 概述

Sophie Mem0 是一款基于 mem0ai 的企业级记忆管理技能，为 Agent 提供：

- **语义记忆存储** - 自然语言描述的记忆，自动提取关键信息
- **跨会话持久化** - 记忆永不过期，支持长期上下文
- **智能检索** - 语义搜索，快速定位相关记忆
- **多级记忆** - 支持 User/Session/Agent 三级记忆体系
- **自我反思** - Agent 可评估自身表现并从经验中学习

## 前置要求

### 必需服务

| 服务 | 版本 | 说明 |
|------|------|------|
| Qdrant | ≥1.7 | 向量数据库，存储记忆向量 |
| Python | ≥3.10 | 运行 mem0ai |
| mem0ai | ≥0.1.x | 记忆框架核心 |

### 依赖安装

```bash
pip install mem0ai qdrant-client
```

## 配置

### 1. 服务启动

```bash
# 启动 Qdrant (Docker)
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant

# 验证 Qdrant 运行
curl http://localhost:6333/readyz
```

### 2. 环境配置

技能读取配置文件：`~/.openclaw/workspace/mem0_config.json`

```json
{
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "sophie_memory"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": "YOUR_API_KEY",
            "openai_base_url": "https://open.bigmodel.cn/api/paas/v4",
            "model": "glm-4"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": "YOUR_API_KEY",
            "openai_base_url": "https://open.bigmodel.cn/api/paas/v4",
            "model": "embedding-3"
        }
    }
}
```

### 3. API配置说明

#### LLM 模型（必须）

支持以下兼容 OpenAI 接口的模型：

| 模型 | 提供商 | 说明 |
|------|--------|------|
| `glm-4` | 智谱AI | 推荐，支持中文 |
| `gpt-4o` | OpenAI | 需要海外环境 |
| `gpt-4` | OpenAI | 需要海外环境 |

#### Embedder 模型（必须）

| 模型 | 提供商 | 说明 |
|------|--------|------|
| `embedding-3` | 智谱AI | 推荐，支持中文 |
| `text-embedding-3-small` | OpenAI | 需要海外环境 |

#### 向量数据库

| 数据库 | Provider | 说明 |
|--------|----------|------|
| Qdrant | `qdrant` | 推荐，已验证 |
| Chroma | `chroma` | 需额外配置 |
| PGVector | `pgvector` | 需PostgreSQL |

## 使用方法

### 全自动模式（推荐）

Sophie可以**全自动**识别和存储重要记忆，无需手动触发：

```bash
# 自动监控模式 - 分析文本并自动存储
/tmp/mem0-env/bin/python3 ~/.openclaw/workspace/skills/sophie-mem0/scripts/auto_memory.py auto -t "文本内容"
```

#### 自动触发场景

| 场景 | 关键词/模式 | 优先级 |
|------|-------------|--------|
| 用户自我介绍 | "我叫..."、"我是..."、"我的名字叫..." | 高 |
| 职业/工作 | "在...工作"、"做...工程师" | 高 |
| 用户偏好 | "我喜欢..."、"我更偏好..." | 中 |
| 习惯 | "我通常..."、"我习惯..." | 中 |
| 待办/承诺 | "记得..."、"别忘了..." | 高 |
| 用户纠正 | "不对"、"错了"、"应该..." | 中 |
| 情感状态 | "今天有点累"、"最近很烦" | 低 |

#### 使用示例

```bash
# 自动存储用户自我介绍
auto -t "我叫张三，在厦门工作，做应用开发"

# 自动存储用户偏好
auto -t "我喜欢喝咖啡，尤其是拿铁"

# 自动存储待办
auto -t "记得周五提醒我买火车票"

# 自动识别用户纠正
auto -t "不对，我之前说的是美式咖啡"
```

### 手动命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `add` | 添加新记忆 | `mem0 add -t "记忆内容"` |
| `search` | 搜索记忆 | `mem0 search -q "关键词"` |
| `list` | 列出所有记忆 | `mem0 list` |
| `delete` | 删除记忆 | `mem0 delete -i "记忆ID"` |
| `health` | 健康检查 | `mem0 health` |

### 响应格式

#### 添加记忆成功
```
✅ 已记住："[记忆内容]"
   记忆ID: xxx-xxx
   创建时间: YYYY-MM-DD HH:mm:ss
```

#### 搜索记忆结果
```
🔍 找到 X 条相关记忆：

1. [记忆内容] (相关度: 85%)
   ID: xxx | 添加于: YYYY-MM-DD

2. [记忆内容] (相关度: 72%)
   ID: xxx | 添加于: YYYY-MM-DD
```

#### 无记忆结果
```
🔍 没有找到与"[关键词]"相关的记忆
```

## API 参考

### Python SDK

```python
from mem0.memory.main import Memory

# 初始化
memory = Memory.from_config(config)

# 添加记忆
result = memory.add(
    text="用户喜欢喝拿铁咖啡",
    user_id="sophie"
)

# 搜索记忆
results = memory.search(
    query="用户的咖啡偏好是什么？",
    user_id="sophie"
)

# 获取所有记忆
all_memories = memory.get_all(user_id="sophie")

# 删除记忆
memory.delete(memory_id="xxx-xxx", user_id="sophie")
```

## 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                     OpenClaw Agent                      │
├─────────────────────────────────────────────────────────┤
│  Sophie Mem0 Skill                                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Memory Manager                                  │   │
│  │  - 自动记忆提取                                  │   │
│  │  - 语义压缩                                     │   │
│  │  - 冲突检测                                     │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                              │
│                         ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  mem0ai Core                                    │   │
│  │  - 自然语言理解                                  │   │
│  │  - 记忆组织                                    │   │
│  │  - 上下文管理                                   │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                              │
│           ┌─────────────┴─────────────┐              │
│           ▼                           ▼              │
│  ┌─────────────────┐     ┌─────────────────┐        │
│  │   LLM (glm-4)   │     │ Embedder        │        │
│  │   智谱AI API    │     │ (embedding-3)  │        │
│  └─────────────────┘     └─────────────────┘        │
│                         │                              │
│                         ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Qdrant Vector Store                             │   │
│  │  - 向量存储 & 相似度检索                         │   │
│  │  - 元数据管理                                   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 安全与隐私

### 数据安全

- ✅ 所有数据存储在本地 Qdrant 实例
- ✅ API Key 通过配置文件管理，不硬编码
- ✅ 支持私有化部署
- ✅ 无第三方数据传输

### 隐私保护

- 用户可随时删除记忆
- 支持按记忆ID精确删除
- 支持清空所有记忆

## 故障排除

### Qdrant 连接失败

```bash
# 检查容器状态
docker ps | grep qdrant

# 重启 Qdrant
docker restart qdrant

# 检查端口
curl http://localhost:6333
```

### API Key 无效

```bash
# 验证 API Key
curl -H "Authorization: Bearer YOUR_KEY" \
     https://open.bigmodel.cn/api/paas/v4/models
```

### 模型不支持

确保使用的模型名称与提供商文档一致：
- 智谱AI: `glm-4`, `embedding-3`
- OpenAI: `gpt-4o`, `text-embedding-3-small`

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-25 | 初始版本，支持 Qdrant + 智谱AI |

## 许可证

MIT License - 可自由使用、修改和分发

## 作者

Sophie AI - 为 Master (Ding Dangmao) 服务 🎀
