# VOKO Subagent Skill

VOKO 子 Agent 处理 Skill，运行在 OpenClaw Gateway 内部，负责创建真正的子 Agent 处理访客消息。

## 架构设计

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
                                            │
                                            ▼
                                     ┌─────────────────┐
                                     │ 返回 JSON 结果   │
                                     └─────────────────┘
```

## 安装

```bash
# 复制 skill 到 openclaw skills 目录
cp -r voko-subagent ~/.openclaw/skills/

# 安装依赖
cd ~/.openclaw/skills/voko-subagent
npm install
```

## 使用方式

### 方式 1: CLI 调用（从 voko im-service）

```bash
# 基本调用
openclaw skill run voko-subagent --visitor-uid=did:wba:xxx

# 指定数据库路径
openclaw skill run voko-subagent \
  --visitor-uid=did:wba:xxx \
  --db-path=C:\Users\...\voko\data\voko.db

# 传入预组装的 Prompt（Base64 编码）
openclaw skill run voko-subagent \
  --visitor-uid=did:wba:xxx \
  --prompt=eyJ2aXNpdG9y...

# 指定超时时间
openclaw skill run voko-subagent \
  --visitor-uid=did:wba:xxx \
  --timeout=180
```

### 方式 2: 在 voko im-service 中调用

```javascript
const { callVokoSubagent } = require('./voko-cli-client');

// 调用 voko-subagent
const result = await callVokoSubagent({
  visitorUid: 'did:wba:xxx',
  dbPath: 'C:\\Users\\...\\voko\\data\\voko.db',
  timeout: 120
});

console.log(result.reply);  // 子 Agent 生成的回复
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--visitor-uid` | string | ✅ | 访客 UID |
| `--db-path` | string | ❌ | VOKO 数据库路径，默认 `./data/voko.db` |
| `--prompt` | string | ❌ | Base64 编码的 Prompt，不传则自动从数据库组装 |
| `--mode` | string | ❌ | `handle` (默认) 或 `build-and-handle` |
| `--timeout` | number | ❌ | 子 Agent 超时时间（秒），默认 120 |

## 返回格式

Skill 输出包含在 `===RESULT===` 和 `===END===` 标记之间：

```json
{
  "success": true,
  "reply": "回复内容",
  "to_uid": "did:wba:xxx",
  "intimacy_suggestion": 75,
  "need_owner_attention": false,
  "attention_reason": "",
  "tags_to_add": [],
  "tags_to_remove": [],
  "run_id": "agent-xxx",
  "status": "completed"
}
```

### 错误返回

```json
{
  "success": false,
  "error": "错误信息",
  "reply": "系统繁忙，请稍后再试",
  "need_owner_attention": true,
  "attention_reason": "错误原因"
}
```

## 文件结构

```
voko-subagent/
├── index.js                    # Skill 主入口
├── skill.json                  # Skill 配置
├── package.json                # 依赖
├── README.md                   # 说明文档
└── src/
    ├── args-parser.js          # 参数解析
    ├── handler.js              # 主处理器
    ├── prompt-builder.js       # Prompt 组装
    ├── subagent-creator.js     # 子 Agent 创建
    └── response-parser.js      # 响应解析
```

## 依赖

- `sqlite3`: 读取 VOKO 数据库
- `openclaw`: Gateway 内部运行时自动提供

## 注意事项

1. **必须在 Gateway 内部运行**: 此 Skill 依赖 `openclaw` 模块，只能在 Gateway 进程中运行
2. **数据库路径**: 确保 `--db-path` 指向正确的 VOKO 数据库文件
3. **超时时间**: 根据网络情况调整，建议 120-180 秒

## 调试

```bash
# 查看详细日志
openclaw skill run voko-subagent --visitor-uid=xxx --verbose

# 测试模式（不创建真实子 Agent）
DEBUG=voko-subagent openclaw skill run voko-subagent --visitor-uid=xxx
```
