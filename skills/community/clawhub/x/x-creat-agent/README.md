# x-create-agent

> **作者：少年李迟迟**
> 一键创建 OpenClaw Agent，支持飞书机器人自动配对

## 功能特性

- ✅ 自动发现 `OPENCLAW_HOME`（跨平台：Linux / macOS / Windows）
- ✅ 创建标准化 Agent 工作区（目录结构 + 空占位文件）
- ✅ 注册 Agent 到 `openclaw.json`
- ✅ 支持飞书机器人 `--feishu-appid` + `--feishu-appsecret` 自动配对
- ✅ 工作区文件**不写死用户名**，内容由调用方动态渲染
- ✅ 创建前展示汇总，用户确认后再动手

##快速开始
##安装
安装在系统共享skill目录，即~/.openclaw/skills
### 使用

```bash
cd ~/.openclaw/skills/x-create-agent
python3 scripts/create_agent.py <agent_id> <name> "<description>" \
  --user-name "你的名字" \
  --feishu-appid "cli_xxxxxxxx" \
  --feishu-appsecret "<secret>"
```

### 最小用法（跳过飞书配对）

```bash
python3 scripts/create_agent.py my-agent "我的助手" "帮我处理事务"
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `agent_id` | ✅ | 唯一标识，字母开头，只含字母/数字/连字符 |
| `name` | ✅ | 中文名称，1-20字 |
| `description` | ✅ | 一句话职能描述 |
| `--user-name` | ❌ | 用户名称（写入 USER.md 占位符） |
| `--feishu-appid` | ❌ | 飞书机器人 AppID |
| `--feishu-appsecret` | ❌ | 飞书机器人 AppSecret |
| `--openclaw-home` | ❌ | 手动指定配置目录路径 |
| `--workspace` | ❌ | 自定义工作区路径 |

## 工作原理

```
触发 skill → 收集信息 → 执行脚本 → 自动发现 OPENCLAW_HOME
  → 用户确认 → 创建目录结构 + 占位文件 → 注册到 openclaw.json
  → 自动配对飞书（可选）→ 完成
```

## 开源协议

MIT License
