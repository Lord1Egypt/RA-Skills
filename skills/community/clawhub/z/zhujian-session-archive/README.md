# Session Archive Plugin

OpenClaw 插件：实时将对话消息存档到 SQLite 数据库。

## 功能特性

### 1. 对话消息存档 (messages 表)
- **实时写入**：每次对话完成后立即触发，自动保存到 SQLite
- **完整记录**：保存角色、内容、模型、时间戳
- **元数据**：支持 channel、message_type、tool_name、media_path 等

### 2. 操作记录 (operations 表)
支持手动调用记录以下操作：
- 文件操作：write/edit/delete
- 命令执行：exec/process
- 配置变更：config_change
- Gateway 操作：gateway_restart/start/stop
- 登录/登出：login/logout

## 安装

```bash
openclaw plugins install @zhuJian/session-archive
# 或
npm install @zhuJian/session-archive
```

## 配置

### 默认配置
- 数据库路径：`~/.openclaw/session-archive.db`

### 自定义配置
在 `openclaw.json` 中添加：

```json
{
  "plugins": {
    "entries": {
      "session-archive": {
        "enabled": true,
        "config": {
          "dbPath": "/自定义/路径/session.db"
        }
      }
    }
  }
}
```

## 数据库表结构

### messages 表
```sql
CREATE TABLE messages (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  session_key  TEXT NOT NULL,
  session_id   TEXT NOT NULL,
  role         TEXT NOT NULL,
  content      TEXT NOT NULL DEFAULT '',
  model        TEXT,
  tokens       INTEGER,
  created_at   INTEGER NOT NULL,
  channel      TEXT,
  account_id   TEXT,
  message_id   TEXT,
  message_type TEXT,
  tool_name    TEXT,
  media_path   TEXT,
  tokens_input INTEGER,
  tokens_output INTEGER,
  cost_usd     REAL
);
```

### operations 表
```sql
CREATE TABLE operations (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  session_key     TEXT,
  operation_type  TEXT NOT NULL,
  target          TEXT NOT NULL,
  details         TEXT,
  result          TEXT,
  operator        TEXT,
  created_at      INTEGER NOT NULL
);
```

## 使用示例

### 查询对话消息
```sql
SELECT * FROM messages WHERE session_key = 'agent:main:main' ORDER BY created_at DESC LIMIT 20;
```

### 查询某渠道的消息
```sql
SELECT * FROM messages WHERE channel = 'wecom' ORDER BY created_at DESC LIMIT 10;
```

### 查询工具调用
```sql
SELECT * FROM messages WHERE message_type = 'tool' ORDER BY created_at DESC LIMIT 10;
```

## 开发者接口

### 记录操作
```typescript
// 在其他插件中调用
const engine = api.getContextEngine('session-archive');
engine.recordOperation({
  operationType: 'exec',
  target: 'ls -la',
  details: { cwd: '/home' },
  result: 'success',
  operator: 'agent:devagent'
});
```

## 与 LCM 插件对比

| 特性 | session-archive | lossless-claw (LCM) |
|------|------------------|---------------------|
| 存储方式 | SQLite | LSM 压缩存储 |
| 压缩 | 无 | 有 |
| 查询性能 | 快 | 较慢 |
| 用途 | 原始消息存档 | 上下文压缩 |
| 互补 | ✅ 可一起使用 | ✅ 可一起使用 |

## 注意事项

1. **数据安全**：数据库文件包含完整对话内容，请妥善保管
2. **磁盘空间**：根据对话量预估存储需求（参考：500条消息/天 ≈ 250KB/天）
3. **兼容性**：需要 OpenClaw >= 2026.3.0

## 版本历史

- **0.4.0**：新增元数据字段（channel、message_type、tool_name、media_path 等）
- **0.3.0**：新增 operations 表支持操作记录
- **0.2.0**：新增元数据字段
- **0.1.0**：初始版本，只记录对话消息

## 作者

- 作者：ZhuJian
- 许可证：MIT
