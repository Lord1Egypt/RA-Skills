---
name: safe-config
description: 安全修改 OpenClaw 配置文件。用于任何需要修改 ~/.openclaw/openclaw.json 的场景，包括：模型切换、channel 配置、tools 配置、skill 安装等。确保修改前备份、预览（脱敏 key）、并获得用户确认。
---

# 🛡️ Safe Config Modifier

安全修改 OpenClaw 配置文件的标准化流程，防止配置损坏导致服务故障。

## ⚡ 快速开始

```bash
# 1. 预览当前配置（脱敏）
~/.openclaw/skills/safe-config/scripts/preview.sh

# 2. 验证配置合法性
~/.openclaw/skills/safe-config/scripts/validate.sh

# 3. 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d-%H%M%S)
```

## 📋 完整流程

### 步骤 1: 读取当前配置

```bash
# 查看完整配置
cat ~/.openclaw/openclaw.json | jq '.'

# 查看特定字段
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model'
cat ~/.openclaw/openclaw.json | jq '.channels'
cat ~/.openclaw/openclaw.json | jq '.plugins'
```

### 步骤 2: 脱敏预览

使用内置脚本生成安全的预览：

```bash
# 完整预览（自动脱敏）
~/.openclaw/skills/safe-config/scripts/preview.sh

# 或手动脱敏
~/.openclaw/skills/safe-config/scripts/sanitize.sh < ~/.openclaw/openclaw.json
```

**脱敏字段**: `apiKey`, `token`, `password`, `secret`, `botToken`

### 步骤 2.5: 本地验证

```bash
# JSON 语法检查
jq '.' ~/.openclaw/openclaw.json

# 使用验证脚本
~/.openclaw/skills/safe-config/scripts/validate.sh

# 测试 API 连通性（如适用）
curl -s https://api.siliconflow.cn/v1/models -H "Authorization: Bearer test" | jq .
```

### 步骤 3: 请求用户确认

⚠️ **关键规则**:
- 展示脱敏后的配置变更
- 告知验证结果
- **必须收到确认语才能执行**
- 确认语只认: **`ojbk可以改了`**
- ❌ 其他任何同意（"好的/可以/OK/收到"）都不执行！

### 步骤 4: 执行修改

```bash
# 1. 备份（必需）
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d-%H%M%S)

# 2. 写入新配置（使用 jq 或直接写入）
jq '.新字段 = "新值"' ~/.openclaw/openclaw.json > /tmp/openclaw.json
mv /tmp/openclaw.json ~/.openclaw/openclaw.json

# 3. 重启 Gateway（如需要）
openclaw gateway restart
```

### 步骤 5: 验证

```bash
# 检查配置写入
jq '.新字段' ~/.openclaw/openclaw.json

# 验证 JSON 合法
jq empty ~/.openclaw/openclaw.json && echo "✅ JSON 合法"

# 检查 Gateway 状态
openclaw gateway status
```

## 📖 常用配置示例

### 模型切换

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "siliconflow/Pro/MiniMaxAI/MiniMax-M2.5"
      }
    }
  }
}
```

### 添加新模型提供商

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "baseUrl": "https://api.anthropic.com/v1",
        "apiKey": "sk-ant-***",
        "models": [
          {
            "id": "claude-sonnet-4-20250514",
            "name": "Claude Sonnet 4",
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### Channel 配置

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "123456:ABC-DEF***",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist"
    }
  }
}
```

### 启用 Telegram 贴纸

```json
{
  "channels": {
    "telegram": {
      "actions": {
        "sticker": true
      }
    }
  }
}
```

### Tools 配置

```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "kimi",
        "kimi": {
          "apiKey": "sk-***"
        }
      }
    }
  }
}
```

## 🚫 禁止事项

| 规则 | 说明 |
|------|------|
| ❌ 禁止不备份 | 每次修改必须先备份 |
| ❌ 禁止不脱敏 | 展示给用户前必须脱敏 |
| ❌ 禁止不验证 | 修改前必须验证 JSON 格式 |
| ❌ 禁止口语确认 | 只认"ojbk可以改了" |
| ❌ 禁止忽略错误 | JSON 错误必须修复 |

## ✅ 正确流程检查清单

- [ ] 读取当前配置
- [ ] 生成脱敏预览
- [ ] 验证 JSON 格式
- [ ] 展示给用户
- [ ] 等待"ojbk可以改了"
- [ ] 备份当前配置
- [ ] 执行修改
- [ ] 验证写入结果

## 📂 文件结构

```
safe-config/
├── SKILL.md           # 本文档
├── _meta.json         # 元数据（ClawHub）
├── references/
│   └── examples.md    # 配置示例
└── scripts/
    ├── sanitize.sh    # 脱敏脚本
    ├── validate.sh    # 验证脚本
    └── preview.sh     # 预览脚本
```

## 🔗 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub 市场](https://clawhub.com)
