---
name: "qdrant-db"
description: "Search and manage a Qdrant vector knowledge base via local CLI helper"
---

# qdrant-db

OpenClaw 外部向量知识库（Qdrant）。**不替代** `memory_search`：  
- 日常偏好/会话笔记 → 继续 `memory_*`  
- 项目文档/运维手册/可共享知识 → 用本 skill

示例配置（代码不内置默认值，模板见 `env.example`；本机 `.env` 当前指向内网 Qdrant `172.26.25.136`）：  
- Qdrant：`http://127.0.0.1:6333`，collection `openclaw`  
- Embedding：`Qwen3-Embedding-0.6B`（1024 维）

## 何时用

- 用户要查/写入「知识库」「Qdrant」「向量库」「kb」
- 需要跨项目检索已入库文档
- 明确说不要写进 MEMORY.md，而要进 Qdrant

## 命令

脚本：

```bash
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py <cmd>
```

### 检索

```bash
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py search "查询内容"
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py search "DPV2 升级" --top-k 8
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py search "队列名" --collection openclaw
```

### 写入

```bash
# 单条文本
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py upsert --text "事实或段落" --source note

# 带元数据
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py upsert --text "..." --source manual --tags "dpv2,ops"

# 从文件入库（按段落/块切分）
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py upsert-file /path/to/doc.md --source doc.md
```

### 管理

```bash
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py ensure      # 确保 collection 存在
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py collections
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py info
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py delete --id <point_id>
```

### 从 OpenClaw SQLite 记忆迁移

```bash
# 复用 sqlite 里已有向量（默认，不重新 embed）
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py migrate-sqlite

# 指定库路径
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py migrate-sqlite \
  --db /root/.openclaw/agents/main/agent/openclaw-agent.sqlite

# 强制按当前 embedding 接口重算向量
python3 /root/.openclaw/workspace/skills/qdrant-db/scripts/kb.py migrate-sqlite --reembed
```

迁移会写入 payload：`path/start_line/end_line/origin=openclaw-sqlite/tags=[migrated,sqlite,memory]`。  
**不会删除** 原 sqlite；内置 `memory_search` 仍可用。

## 工作流

1. 首次或 collection 不存在：先 `ensure`
2. 用户给文档/要点：`upsert` / `upsert-file`
3. 用户要查知识：`search`，把命中的 text + source + score 整理进回复
4. 不要把 Qdrant 检索结果默默写进 MEMORY.md，除非用户要求“记住”

## 环境变量（可选覆盖）

配置来源优先级：**真实环境变量 > `<skill根>/.env`**（代码不内置默认值；缺必填项会报错，按 `env.example` 补全 `.env` 即可）

所有配置统一从环境变量读取；`.env` 为 shell 风格 `KEY=VALUE`（支持 `export` 前缀、单/双引号、`#` 注释、空行，不支持变量展开）。

统一配置文件 `<skill根目录>/.env`（与 kb.py 同随 skill 走，权限 600）；目录下附脱敏模板 `env.example`，复制即可开始：

```bash
cp env.example .env && chmod 600 .env
```

```bash
# --- Qdrant 向量库 ---
QDRANT_URL=http://172.26.25.136:6333
QDRANT_COLLECTION=openclaw
QDRANT_API_KEY=

# --- Embedding 服务（全量配置已在此，不再依赖 openclaw.json） ---
EMBEDDING_BASE_URL=http://apiproxy.jq.datagrand.cn/v1
EMBEDDING_API_KEY=<真实key>
EMBEDDING_MODEL=Qwen3-Embedding-0.6B
EMBEDDING_DIMS=1024
```

可覆盖的环境变量：`QDRANT_URL` / `QDRANT_COLLECTION` / `QDRANT_API_KEY` / `EMBEDDING_BASE_URL` / `EMBEDDING_API_KEY` / `EMBEDDING_MODEL` / `EMBEDDING_DIMS`。

注意：
- 不能把自定义键塞进 `openclaw.json`（schema 白名单，额外字段会导致 gateway 拒绝启动）。
- openclaw.json 的 `agents.defaults.memorySearch` 已清理，只剩 `enabled:false`（关闭内置 memory search），不再作为 embedding 配置来源。
- 密钥只走 .env 或环境变量，不要打印到聊天。

## 规则

- 写入与检索必须用同一 embedding 模型/维度，禁止混用 MiniLM 等其它模型写同一 collection
- 大文件先 `upsert-file`，不要一次性把整本塞进单点
- 失败时展示脚本 stderr，不要假装写入成功
- 密钥只走环境变量或 .env，不要打印到聊天

## 与 memory 的分工

| 内容 | 去哪 |
|---|---|
| 用户偏好、口头约定、日常笔记 | `MEMORY.md` / `memory_search` |
| 可复用文档、方案、手册、接口说明 | 本 Qdrant KB |
| 两者都要 | 先 KB 检索，重要结论再按需记 memory |
