# VOKO Subagent Skill

VOKO 子 Agent 处理 Skill，运行在 OpenClaw Gateway 内部，负责创建真正的子 Agent 处理访客消息。

## 架构

```
┌─────────────────┐     CLI 调用      ┌─────────────────┐
│  voko (im-service) │ ───────────────► │ voko-subagent   │
│  (独立运行)        │   传递参数       │ (Gateway Skill) │
└─────────────────┘                  └─────────────────┘
                                            │
                                            ▼
                                     ┌─────────────────┐
                                     │ OpenClaw        │
                                     │ (创建真子Agent)  │
                                     └─────────────────┘
```

## 使用方式

### 1. 直接调用（Gateway 内部）

```javascript
const result = await sessions_spawn({
  runtime: 'subagent',
  task: '处理访客消息',
  agentId: 'voko-subagent',
  // 参数通过 task 传递
});
```

### 2. CLI 调用（从 voko im-service）

```bash
# 处理访客消息
openclaw skill run voko-subagent --visitor-uid=<uid> --db-path=<path> --prompt=<base64>

# 或者使用简化模式
openclaw skill run voko-subagent --mode=handle --visitor-uid=<uid>
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--visitor-uid` | 访客 UID | `did:wba:...` |
| `--db-path` | VOKO 数据库路径 | `C:\...\voko\data\voko.db` |
| `--prompt` | Base64 编码的 Prompt | `eyJ2aXNpdG9y...` |
| `--mode` | 运行模式 | `handle` / `build-and-handle` |

## 返回格式

```json
{
  "success": true,
  "reply": "回复内容",
  "to_uid": "访客UID",
  "intimacy_suggestion": 75,
  "need_owner_attention": false,
  "attention_reason": "",
  "tags_to_add": [],
  "tags_to_remove": [],
  "run_id": "子Agent运行ID"
}
```
