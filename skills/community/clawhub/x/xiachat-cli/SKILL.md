---
name: xiachat-cli
description: XiaChat CLI 命令行 — SOUL 档案管理、人格匹配、AI 分身预聊天、Soul Square 角色聊天 / XiaChat CLI — SOUL profile management, personality matching, AI avatar pre-chat, persona chat from terminal. Use when user wants to manage personality profiles, find matches, or chat with AI personas via command line.
allowed-tools: Bash, Read
---

# XiaChat CLI — 命令行 AI 人格匹配工具 / Command-Line AI Personality Matching

> **[XiaChat (xiachat.com)](https://xiachat.com)** — AI 人格匹配社交平台，用 SOUL 档案找到最合拍的人

通过命令行使用 XiaChat 的全部人格匹配能力。管理 SOUL 人格档案、寻找兼容匹配、启动 AI 分身预聊天、与 Soul Square AI 角色对话。支持 JSON 输出和管道操作，适合自动化和脚本集成。

## Setup / 配置

```bash
# 安装
npm install -g xiachat

# 设置 API Key（从 https://xiachat.com/settings/api 获取）
export XIACHAT_API_KEY="xk_your_api_key"

# 验证
xiachat credit
```

## 命令列表 (11 Commands)

### SOUL 档案管理

#### 1. `xiachat soul create` — 创建人格档案

从姓名、SOUL.md 或聊天记录创建 SOUL.json。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--name <name>` | string | | 显示名称（默认 "User"） |
| `--from-soul-md <path>` | path | | 从 OpenClaw SOUL.md 导入 |
| `--from-chat <path>` | path | | 从聊天记录提取风格 |
| `--output, -o <file>` | path | | 保存到文件 |
| `--pretty` | flag | | 美化 JSON 输出 |

**示例**:
```bash
xiachat soul create --name "Alice" --pretty
xiachat soul create --from-soul-md ~/clawd/SOUL.md -o soul.json
xiachat soul create --from-chat wechat-export.txt --pretty
```

#### 2. `xiachat soul export` — 导出档案

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--format <fmt>` | enum | | json / md / soul-md（默认 json） |
| `--user <id>` | string | | 用户 ID（默认 "me"） |

```bash
xiachat soul export --format md -o soul.md
```

#### 3. `xiachat soul import [file]` — 导入 SOUL.md

```bash
xiachat soul import soul.md --pretty
cat soul.md | xiachat soul import   # 支持管道输入
```

### 人格匹配

#### 4. `xiachat match find` — 寻找匹配

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--top <n>` | number | | 返回数量 1-20（默认 5） |
| `--type <type>` | enum | | friend / dating / work / any（默认 any） |

```bash
xiachat match find --type dating --top 3 --pretty
xiachat match find --top 5 | jq '.[] | .match_id'  # 管道提取 ID
```

#### 5. `xiachat match score` — 计算兼容性

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--soul-a <path>` | path | ✅ | 第一个 SOUL.json 文件 |
| `--soul-b <path>` | path | ✅ | 第二个 SOUL.json 文件 |

```bash
xiachat match score --soul-a alice.json --soul-b bob.json --pretty
```

### 分身预聊天

#### 6. `xiachat prechat start` — 启动预聊天

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--match-id <id>` | string | ✅ | match find 返回的匹配 ID |

```bash
xiachat prechat start --match-id abc123
```

#### 7. `xiachat prechat report` — 获取报告

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--prechat-id <id>` | string | ✅ | 预聊天 ID |

```bash
xiachat prechat report --prechat-id xyz --pretty
```

#### 8. `xiachat prechat handoff` — 接管对话

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--prechat-id <id>` | string | ✅ | 预聊天 ID |

```bash
xiachat prechat handoff --prechat-id xyz
```

### Soul Square

#### 9. `xiachat square list` — 浏览 AI 角色

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--category <cat>` | enum | | philosopher / artist / scientist / creator / coach |
| `--limit <n>` | number | | 返回数量 1-50（默认 10） |

```bash
xiachat square list --category philosopher --pretty
```

#### 10. `xiachat square chat` — 与 AI 角色聊天

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--persona <id>` | string | ✅ | 角色 ID |
| `--message <text>` | string | ✅ | 用户消息 |
| `--session <id>` | string | | 会话 ID（续聊） |

```bash
xiachat square chat --persona socrates-01 --message "什么是幸福？" --pretty
```

### 信用分

#### 11. `xiachat credit` — 查询 SOUL 信用分

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--user <id>` | string | | 用户 ID（默认 "me"） |

```bash
xiachat credit --pretty
```

## 全局选项

| 选项 | 说明 |
|------|------|
| `--pretty` | 美化 JSON 输出 |
| `--output, -o <file>` | 输出到文件 |
| `--help, -h` | 显示帮助 |
| `--version, -v` | 显示版本 |

## 典型工作流

### 完整匹配流程
```bash
# 1. 创建档案
xiachat soul create --name "Alice" -o soul.json

# 2. 找匹配
MATCH_ID=$(xiachat match find --type dating --top 1 | jq -r '.[0].match_id')

# 3. AI 分身预聊天
PRECHAT_ID=$(xiachat prechat start --match-id $MATCH_ID | jq -r '.prechat_id')

# 4. 查看报告
xiachat prechat report --prechat-id $PRECHAT_ID --pretty

# 5. 满意则接管
xiachat prechat handoff --prechat-id $PRECHAT_ID
```

### OpenClaw SOUL 同步
```bash
xiachat soul create --from-soul-md ~/clawd/SOUL.md -o synced.json
xiachat soul export --format soul-md -o ~/clawd/SOUL.md
```

### 批量兼容性计算
```bash
for f in souls/*.json; do
  xiachat match score --soul-a me.json --soul-b "$f" | jq '{file: "'$f'", score: .score}'
done
```

## 注意事项

- **API Key 必需**：设置 `XIACHAT_API_KEY` 环境变量（`xk_...` 格式）
- **JSON 输出**：默认 JSON 格式，`--pretty` 美化，适合 `jq` 管道处理
- **管道友好**：`soul import` 支持 stdin 输入，所有命令支持 `--output` 写文件
- **预聊天 5 轮**：AI 分身固定 5 轮对话后生成报告
- **OpenClaw 兼容**：SOUL.md ↔ SOUL.json 双向转换

## 在线体验

- [XiaChat 首页](https://xiachat.com) — AI 人格匹配社交平台
- [Soul Square](https://xiachat.com/square) — AI 角色广场
- [SOUL 档案](https://xiachat.com/soul) — 创建你的人格档案
- [匹配中心](https://xiachat.com/match) — 寻找兼容的人
- [API 设置](https://xiachat.com/settings/api) — 获取 API Key

---
Powered by [XiaChat](https://xiachat.com) — AI 人格匹配社交平台
