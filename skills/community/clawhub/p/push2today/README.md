# Push2Today Skill

将任务执行结果推送到负一屏显示的 OpenClaw Skill。

## 功能特性

- 支持普通对话结果推送
- 支持定时任务执行结果自动推送
- 通过 `tools.json` 定义 CLI 工具
- 完整的参数验证和错误处理
- 环境变量配置管理

## 目录结构

```
push2today/
├── SKILL.md       # Skill 核心定义文件
├── tools.json     # 工具定义（CLI 命令）
├── README.md      # 使用文档
└── scripts/
    ├── cli.ts     # TypeScript CLI 源码
    └── cli.js     # 编译后的 JavaScript
```

## 快速开始

### 1. 编译 CLI

```bash
cd scripts
npx tsc cli.ts --esModuleInterop --target ES2020 --module CommonJS --moduleResolution node --skipLibCheck
```

ln -s /Users/pingjiang/coding/gitcode/ai/clawhome/skills/push2today ~/.openclaw/skills/push2today

### 2. 配置环境变量

使用 OpenClaw 配置认证令牌：

```bash
openclaw config set skills.entries.push2today.env.AS_TODAY_AUTH_CODE "your_actual_token_here"
```

### 3. 使用 Skill

当用户说以下任一短语时，Agent 会自动调用此 Skill：

- "推送到负一屏"
- "帮我推送到负一屏"
- "推送到手机"
- "帮我推送到手机"
- "帮我推送到手机负一屏"
- "push to Today"

## CLI 使用方法

### 基本用法

```bash
node scripts/cli.js push2today \
  --msgId "msg-123456" \
  --summary "任务完成" \
  --result "任务执行成功" \
  --content "任务已成功完成，所有检查通过"
```

### 定时任务推送

```bash
node scripts/cli.js push2today \
  --msgId "msg-cron-001" \
  --summary "晨间摘要完成" \
  --result "任务执行成功" \
  --content "今日摘要内容..." \
  --scheduleTaskId "morning-brief" \
  --scheduleTaskName "晨间摘要任务" \
  --source "openclaw"
```

### 查看帮助

```bash
node scripts/cli.js --help
node scripts/cli.js push2today --help
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--msgId` | **是** | 消息 ID |
| `--summary` | **是** | 任务摘要（64 字符以内） |
| `--result` | **是** | 执行结果：`任务执行成功` 或 `任务执行失败` |
| `--content` | **是** | 详细内容（长度限制 30717 字符） |
| `--scheduleTaskId` | 否 | 定时任务 ID |
| `--scheduleTaskName` | 否 | 定时任务名称 |
| `--source` | 否 | 来源类型（默认：`openclaw`） |
| `--taskFinishTime` | 否 | 任务完成时间戳（单位：秒） |

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `AS_TODAY_AUTH_CODE` | **是** | 接口鉴权令牌 |
| `AS_TODAY_API_URL` | 否 | API 端点（可选） |
| `DEBUG` | 否 | 设置为 `true` 显示调试信息 |

### 配置示例

```bash
# 配置认证令牌
openclaw config set skills.entries.push2today.env.AS_TODAY_AUTH_CODE "your_actual_token_here"

# 调试模式（可选）
openclaw config set skills.entries.push2today.env.DEBUG "true"
```

## API 数据格式

CLI 工具内部发送的数据格式：

```json
{
  "data": {
    "authCode": "<AS_TODAY_AUTH_CODE>",
    "msgContent": [
      {
        "msgId": "msg-123456",
        "scheduleTaskId": "task-001",
        "scheduleTaskName": "定时任务",
        "taskFinishTime": 1711800000,
        "source": "openclaw",
        "summary": "任务完成",
        "result": "任务执行成功",
        "content": "详细内容..."
      }
    ]
  }
}
```

## 常见问题

### Q: 提示 "未设置环境变量 AS_TODAY_AUTH_CODE"

需要先配置认证令牌：

```bash
openclaw config set skills.entries.push2today.env.AS_TODAY_AUTH_CODE "your_token"
```

### Q: 推送失败

1. 检查 `AS_TODAY_AUTH_CODE` 是否正确配置
2. 检查网络连接
3. 使用 `DEBUG=true` 查看详细错误信息：

```bash
DEBUG=true node scripts/cli.js push2today --msgId "test" --summary "test" --result "任务执行成功" --content "test"
```

### Q: 参数长度超限

- `summary` 长度不能超过 64 字符
- `content` 长度不能超过 30717 字符

## 开发

### 编译 CLI

```bash
cd scripts
npx tsc cli.ts --esModuleInterop --target ES2020 --module CommonJS --moduleResolution node --skipLibCheck
```

### 本地测试

```bash
# 测试推送
node scripts/cli.js push2today \
  --msgId "test-$(date +%s)" \
  --summary "测试推送" \
  --result "任务执行成功" \
  --content "这是一条测试消息"
```

### 类型检查

```bash
npx tsc --noEmit cli.ts
```

## License

MIT
