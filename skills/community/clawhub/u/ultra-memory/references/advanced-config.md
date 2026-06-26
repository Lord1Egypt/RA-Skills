# Ultra Memory — 进阶配置参考

## 目录

1. [自定义记录过滤规则](#1-自定义记录过滤规则)
2. [记忆衰减策略](#2-记忆衰减策略)
3. [LanceDB 向量检索升级](#3-lancedb-向量检索升级)
4. [团队共享记忆配置](#4-团队共享记忆配置)
5. [OpenClaw 集成配置](#5-openclaw-集成配置)
6. [Claude Code 集成配置](#6-claude-code-集成配置)
7. [n8n / LangGraph 集成](#7-n8n--langgraph-集成)
8. [安全注意事项](#8-安全注意事项)
9. [存储维护](#9-存储维护)
10. [clawbot Auto-Hook 配置](#10-clawbot-auto-hook-配置)
11. [自我进化引擎配置](#11-自我进化引擎配置)

---

## 1. 自定义记录过滤规则

在 `~/.ultra-memory/config.json` 中配置：

```json
{
  "filters": {
    "sensitive_patterns": [
      "password\\s*=\\s*\\S+",
      "sk-[A-Za-z0-9]{32,}",
      "YOUR_CUSTOM_SECRET_PATTERN"
    ],
    "skip_op_types": [],
    "skip_paths": [
      "~/.ssh/",
      "/etc/passwd"
    ],
    "max_detail_bytes": 2048
  }
}
```

说明：
- `sensitive_patterns`：正则列表，匹配到的内容替换为 `[REDACTED]`
- `skip_op_types`：不记录的操作类型（例如 `["file_read"]` 可减少日志量）
- `skip_paths`：文件路径前缀，涉及这些路径的操作不记录 detail
- `max_detail_bytes`：单条 detail 最大字节数，超出截断

---

## 2. 记忆衰减策略

避免历史记忆无限增长、降低检索噪音：

```json
{
  "decay": {
    "session_ttl_days": 30,
    "auto_archive_after_days": 7,
    "knowledge_base_max_entries": 1000,
    "milestone_weight_boost": 2.0,
    "recency_weight": 0.3
  }
}
```

- `session_ttl_days`：超过 N 天的会话目录自动删除（但不删 semantic/）
- `auto_archive_after_days`：N 天未访问的会话移入 `.archive/`
- `milestone_weight_boost`：里程碑类记忆检索权重倍增
- `recency_weight`：检索评分中时间新近度的权重（0-1）

手动清理：
```bash
python3 scripts/cleanup.py --older-than 30  # 清理 30 天前会话
python3 scripts/cleanup.py --archive-only   # 只归档不删除
```

---

## 3. LanceDB 向量检索升级

安装依赖后自动启用：

```bash
pip install lancedb sentence-transformers --break-system-packages
python3 scripts/setup_vector.py
```

`setup_vector.py` 会：
1. 初始化 `~/.ultra-memory/semantic/lancedb/` 数据库
2. 将现有 `knowledge_base.jsonl` 导入向量库
3. 修改 `config.json` 中 `"mode": "enhanced"`

向量检索配置：

```json
{
  "vector": {
    "model": "paraphrase-multilingual-MiniLM-L12-v2",
    "index_type": "IVF_PQ",
    "top_k_candidates": 20,
    "rerank": true
  }
}
```

推荐模型（支持中文）：
- `paraphrase-multilingual-MiniLM-L12-v2`（小，快，多语言）
- `BAAI/bge-m3`（大，精度更高，支持中英文混合）

---

## 4. 团队共享记忆配置

在团队协作场景下，将 Layer 3 指向共享存储：

```json
{
  "semantic": {
    "shared_path": "/mnt/team-nas/ultra-memory/semantic/",
    "sync_mode": "read-write",
    "namespace": "team-ai-project"
  }
}
```

或使用 S3 兼容存储：

```json
{
  "semantic": {
    "backend": "s3",
    "s3_bucket": "my-team-memory",
    "s3_prefix": "ultra-memory/",
    "namespace": "team-ai-project"
  }
}
```

注意：Layer 1（操作日志）和 Layer 2（摘要）始终本地存储，只有 Layer 3 共享。

---

## 5. OpenClaw 集成配置

### 安装方式

```bash
# 方式 A：作为 Skill 安装
cp -r ultra-memory ~/.openclaw/workspace/skills/

# 方式 B：作为 MCP Plugin 安装（推荐，获得完整工具调用支持）
openclaw plugins install ultra-memory --local ./ultra-memory
```

### openclaw CLAUDE.md 配置

在项目 CLAUDE.md 顶部添加：

```markdown
## Memory
使用 ultra-memory skill 记录所有操作。
会话开始时运行 `python3 ~/.openclaw/workspace/skills/ultra-memory/scripts/init.py --project <project-name>`
每次工具调用后运行 `python3 ... log_op.py --session $SESSION_ID --type tool_call --summary "..."`
```

### 自动 Hook 配置（openclaw hooks）

在 `.openclaw/hooks.yaml` 中：

```yaml
hooks:
  post_tool_call:
    - command: python3
      args:
        - ~/.openclaw/workspace/skills/ultra-memory/scripts/log_op.py
        - --session
        - "{{session_id}}"
        - --type
        - tool_call
        - --summary
        - "{{tool_name}}: {{summary}}"
```

---

## 6. Claude Code 集成配置

### 安装

```bash
cp -r ultra-memory ~/.claude/skills/ultra-memory
```

### CLAUDE.md 集成

```markdown
# Ultra Memory
在会话开始时：
init: python3 ~/.claude/skills/ultra-memory/scripts/init.py --project <项目名> --resume

在每次操作后（可通过 hooks 自动化）：
log: python3 ~/.claude/skills/ultra-memory/scripts/log_op.py --session $SESSION_ID --type <type> --summary "<summary>"
```

### MCP 服务器模式（推荐）

在 `~/.claude/claude_code_config.json` 中添加：

```json
{
  "mcpServers": {
    "ultra-memory": {
      "command": "node",
      "args": ["~/.claude/skills/ultra-memory/scripts/mcp-server.js"]
    }
  }
}
```

---

## 7. n8n / LangGraph 集成

### n8n 集成

在 n8n workflow 中添加 Execute Command 节点：

```
命令: python3
参数: /path/to/ultra-memory/scripts/log_op.py --session {{$json.session_id}} --type tool_call --summary "{{$json.summary}}"
```

或通过 HTTP 调用 MCP 服务器（需先启动 `mcp-server.js`）。

### LangGraph 集成

```python
from langgraph.graph import StateGraph
import subprocess

def log_to_ultra_memory(state, op_type, summary):
    subprocess.run([
        "python3", "/path/to/scripts/log_op.py",
        "--session", state["session_id"],
        "--type", op_type,
        "--summary", summary
    ])

# 在节点函数中调用
def my_node(state):
    # ... 执行操作 ...
    log_to_ultra_memory(state, "tool_call", "执行了数据查询")
    return state
```

---

## 8. 安全注意事项

1. **不要记录凭证**：内置敏感词过滤，但请在 `sensitive_patterns` 中添加你的业务特定模式
2. **权限控制**：`~/.ultra-memory/` 目录建议设置 `chmod 700`
3. **共享模式**：团队共享时启用 `namespace` 隔离，避免不同项目记忆混淆
4. **MCP 服务安全**：MCP Server 默认仅监听 stdio，不暴露网络端口，如需网络模式请添加认证
5. **数据保留**：ops.jsonl 包含完整操作历史，注意合规要求（GDPR 等）

---

## 9. 存储维护

### 目录结构

```
~/.ultra-memory/
├── config.json              # 全局配置
├── sessions/                # 会话目录（Layer 1 + 2）
│   ├── sess_20260402_abc/
│   │   ├── meta.json
│   │   ├── ops.jsonl        # 操作日志（append-only）
│   │   └── summary.md       # 摘要（累积追加）
│   └── ...
├── semantic/                # 跨会话语义层（Layer 3）
│   ├── user_profile.json
│   ├── project_registry.json
│   ├── knowledge_base.jsonl
│   ├── session_index.json
│   └── lancedb/             # 向量库（增强模式）
└── archive/                 # 归档的旧会话
```

### 空间估算

| 场景 | 每会话大小 | 1个月估算 |
|------|-----------|---------|
| 轻度使用（<50次操作）| ~20KB | ~200KB |
| 中度使用（50-200次）| ~100KB | ~1MB |
| 重度使用（>200次）| ~500KB | ~5MB |
| 增强模式（含向量）| +LanceDB ~50MB | ~50MB（共享）|

### 清理命令

```bash
# 查看空间使用
du -sh ~/.ultra-memory/

# 清理 30 天前会话
python3 scripts/cleanup.py --older-than 30

# 导出所有记忆（备份）
python3 scripts/export.py --output ~/memory-backup.zip
```

---

## 10. clawbot Auto-Hook 配置

ultra-memory 已提供 `clawbot_hook.py`，可在 clawbot 对话循环中自动触发记录，不依赖模型主动调用。

### Python Hook（推荐）

在 clawbot 的 skill_runner 或对话循环中导入：

```python
from ultra_memory.scripts.clawbot_hook import UltraMemoryHook

hook = UltraMemoryHook()

def run_conversation_turn(user_message, session_context):
    response = call_model(user_message, session_context)

    # 自动记录（加在这里）
    hook.on_turn_end(
        session_id=session_context.get("ultra_memory_session_id"),
        model_name=session_context.get("model_name", "unknown"),
        user_msg=user_message,
        assistant_msg=response.text,
        project=extract_project_name(user_message),
    )

    return response
```

### YAML Hook（clawbot 支持 hooks.yaml 时）

```yaml
hooks:
  post_turn:
    - name: ultra-memory-auto-log
      enabled: true
      condition: "session.ultra_memory_session_id != null"
      command: python3
      args:
        - "${SKILL_DIR}/scripts/log_op.py"
        - "--session"
        - "${session.ultra_memory_session_id}"
        - "--type"
        - "tool_call"
        - "--summary"
        - "自动记录: ${user.message[:60]}"
        - "--tags"
        - "auto,model:${session.model_name}"
      timeout: 5
      on_failure: skip

  post_tool_call:
    - name: ultra-memory-tool-log
      enabled: true
      condition: "session.ultra_memory_session_id != null"
      command: python3
      args:
        - "${SKILL_DIR}/scripts/log_op.py"
        - "--session"
        - "${session.ultra_memory_session_id}"
        - "--type"
        - "tool_call"
        - "--summary"
        - "工具调用: ${tool.name}"
        - "--tags"
        - "auto,tool:${tool.name}"
      timeout: 5
      on_failure: skip
```

### 设计原则

1. **失败静默跳过**：所有 hook 加 try/except + timeout（5秒），失败不抛异常
2. **超时要短**：log_op.py 是文件追加，100ms 内完成，5秒足够
3. **不重复记录**：hook 记录加 `auto` tag，模型主动记录不加，后续可按 tag 过滤
4. **session_id 为空时跳过**：`session_context.get("ultra_memory_session_id")` 为 None 时什么都不做

---

## 11. 自我进化引擎配置

v3.2.0 新增进化引擎，提供自动事实提取、矛盾检测、遗忘三大能力。

### 存储结构

```
~/.ultra-memory/evolution/
├── facts.jsonl           # 结构化事实（append-only）
├── contradictions.jsonl  # 矛盾记录（append-only）
├── fact_metadata.json    # 置信度/TTL/衰减状态（可变更）
└── decay_log.jsonl      # 遗忘事件审计日志
```

### 配置项（config.json）

```json
{
  "evolution": {
    "enable_auto_extraction": true,
    "auto_extraction_on_log": true,
    "similarity_threshold": 0.72,
    "forget_threshold": 0.05,
    "half_life_days": 30,
    "auto_negation_resolution": true
  }
}
```

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| `enable_auto_extraction` | `true` | 启用自动事实提取 |
| `auto_extraction_on_log` | `true` | log_op 时自动触发提取 |
| `similarity_threshold` | `0.72` | 矛盾检测相似度阈值 |
| `forget_threshold` | `0.05` | 遗忘触发阈值（decay_score） |
| `half_life_days` | `30` | 记忆半衰期 |
| `auto_negation_resolution` | `true` | 自动消解低置信度矛盾 |

### 脚本清单

| 脚本 | 用途 | 调用方式 |
|-----|------|---------|
| `extract_facts.py` | 从 ops 提取事实三元组 | log_op.py 自动调用，或 `python3 scripts/extract_facts.py --session S --batch` |
| `detect_contradictions.py` | 矛盾检测与消解 | extract_facts.py 触发，或 `python3 scripts/detect_contradictions.py --session S --batch` |
| `auto_decay.py` | TTL 衰减与遗忘 | `python3 scripts/cleanup.py --run-decay` 或每日定时 |
| `evolve_profile.py` | 画像贝叶斯更新 | `python3 scripts/evolve_profile.py --field X --value Y` |
| `multimodal/extract_from_pdf.py` | PDF 文本提取 | 自动触发（依赖 pdfminer.six） |
| `multimodal/extract_from_image.py` | 图片 OCR | 自动触发（依赖 pytesseract） |
| `multimodal/transcribe_video.py` | 视频转录 | 自动触发（依赖 whisper） |

### 多模态依赖安装

```bash
# PDF 文本提取
pip install pdfminer.six

# 图片 OCR（需安装 Tesseract 引擎）
pip install pytesseract
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt install tesseract-ocr

# 视频转录（本地 Whisper，无需 API）
pip install openai-whisper
```

### LangChain 集成

```python
from ultra_memory.integrations.langchain_memory import UltraMemoryMemory

memory = UltraMemoryMemory(
    session_id="sess_langchain_proj",
    project="my-agent",
    top_k=5
)

# LangChain agent 中使用
agent = OpenAIAgent(..., memory=memory)
```

### LangGraph Checkpointer 集成

```python
from ultra_memory.integrations.langgraph_checkpointer import UltraMemoryCheckpointer

checkpointer = UltraMemoryCheckpointer(session_id="sess_langgraph_proj")

# 每个节点执行后自动保存状态
def my_node(state):
    checkpointer.save_checkpoint(state["step"], state)
    return state

graph = StateGraph(AgentState)
graph.add_node("agent", my_node)
compiled = graph.compile(checkpointer=checkpointer)
```

### n8n 集成

在 n8n "Execute Command" 节点中：

```
命令: python3
参数: /path/to/ultra-memory/integrations/n8n_nodes.py init --project=<项目名>
```

支持操作：`init`, `log`, `recall`, `profile`
