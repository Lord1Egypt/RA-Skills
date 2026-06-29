---
name: x-create-agent
version: 1.2.14
author: 少年李迟迟
description: 规范化创建 OpenClaw Agent 的完整工作流。当用户说"创建 agent"、"新建 agent"、"添加 agent"、"new agent"时触发。执行三步流程：(1) 收集 agent_id/中文名/职能描述；(2) 执行脚本创建 agent 和工作区文件（--user-name 防硬编码）；(3) 引导用户创建飞书机器人并提交 AppID/AppSecret 完成配对。
---

# x-create-agent — OpenClaw Agent 标准化创建流程

> 作者：少年李迟迟
> 工作区文件（USER.md 等）**不写死任何用户名**，参考模板结合用户信息动态生成。
> 飞书配对**自动化**（脚本直接写入 openclaw.json），无需主 agent 介入。

## 工作流程

### Step 1：收集信息

向用户收集以下信息（逐项询问，不要一次性问完）：

| 信息 | 说明 | 验证规则 |
|------|------|---------|
| `agent_id` | 唯一标识，英文字母/数字/连字符 | 必须是合法标识符（字母开头） |
| `name` | 中文名称 | 1-20字 |
| `description` | 职能描述 | 一句话说明这个 agent 是做什么的 |
| `feishu_appid` | 飞书 AppID | 格式：`cli_xxxxxxxx` |
| `feishu_appsecret` | 飞书 AppSecret | 非空字符串 |

> ⚠️ 如果用户跳过飞书信息，创建完成后仍需引导填写。
>
> **路径说明：** `~/.openclaw/skills/x-create-agent` 是默认安装路径示例，实际路径因用户环境而异。脚本支持**自动搜索**，搜不到时会交互式询问，用户只需输入自己的 `OPENCLAW_HOME` 绝对路径即可，开源分享无障碍。

### Step 2：执行创建脚本

**路径确认制**：脚本发现路径后，先展示汇总信息，用户确认（输入 y）后再创建。

```bash
cd ~/.openclaw/skills/x-create-agent
python3 scripts/create_agent.py "<agent_id>" "<name>" "<description>" \
  [--openclaw-home <path>] \
  [--workspace <path>] \
  [--user-name <name>] \
  [--feishu-appid <appid>] \
  [--feishu-appsecret <secret>]
```

**展示内容（等用户确认）：**
- Agent ID / 名称 / 职能描述
- 发现的配置目录路径
- 将创建的 Agent 目录路径
- 将创建的工作区路径

**路径发现优先级（自动搜索，无需手动指定）：**
1. `OPENCLAW_HOME` 环境变量（如已设置）
2. 脚本自身目录向上持续搜索（无层级限制，直到根目录）
3. `openclaw` 二进制所在目录向上搜索
4. 常见安装路径（`~/.openclaw/` 等 Linux/macOS/Windows 平台覆盖）

**手动指定（可选）：**
- `--openclaw-home <path>` — 显式指定配置目录路径
- `--workspace <path>` — 自定义工作区路径（相对路径基于脚本目录 resolve）

**如全部搜索失败**：脚本进入交互模式，提示用户输入配置目录路径并验证 `openclaw.json` 存在。

**用户输入非 y**：脚本立即退出，不创建任何文件。

### Step 2.1：飞书配对（可选，命令行直接传入）

创建时直接传入 AppID 和 AppSecret，自动完成飞书机器人配对：

```bash
python3 scripts/create_agent.py "<agent_id>" "<name>" "<description>" \
  --feishu-appid "cli_xxxxxxxx" \
  --feishu-appsecret "<secret>"
```

这会在 `openclaw.json` 中自动写入：
- `channels.feishu.accounts[<agent_id>]`：机器人凭证
- `bindings`：路由绑定

如未传入，脚本会在创建完成后打印操作指引。**无需主 agent 介入，skill 调用者自己引导用户完成即可。**

**飞书机器人创建链接：**
- [智能体](https://open.feishu.cn/page/launcher?from=backend_oneclick)
- [机器人](https://open.feishu.cn/page/openclaw?form=multiAgent)

### Step 3：确认完成

创建完成后，报告：
- Agent 目录路径
- 工作区路径
- 飞书绑定状态（如已传入凭证，则自动完成）

---

## 脚本详情：`scripts/create_agent.py`

### 功能

- 创建 `agents/<agent_id>/agent/` 目录
- 创建工作区目录及标准文件（SOUL.md / AGENTS.md / USER.md 等）
- 将新 agent 注册到 `openclaw.json`
- **自动完成飞书机器人配对**（写入 accounts + bindings）

### 关键实现细节

**路径发现逻辑**（按优先级）：
1. `OPENCLAW_HOME` 环境变量
2. `~/.openclaw/`
3. 常见安装路径（如 `~/.openclaw/`）

**openclaw.json 注册**：
- 在 `agents.list` 中添加新条目（含 `id`、`name`、`workspace`、`agentDir`）
- 在 `tools.agentToAgent.allow` 中添加新 agent_id

**飞书配对自动写入**：
- `channels.feishu.accounts[<agent_id>]`：机器人凭证（appId + appSecret）
- `bindings`：路由绑定（channel=feishu, accountId=<agent_id>）

**工作区文件**：
- 脚本**参考内置模板**，结合用户提供的 `agent_id`、`name`、`description`、`user_name` 动态渲染生成各文件
- `SOUL.md` → 填入 agent 名称和职能描述（专属内容）
- `USER.md` → 填入 user_name（主人名）
- `IDENTITY.md` → 填入 agent 名称
- `AGENTS.md` / `HEARTBEAT.md` / `TOOLS.md` / `MEMORY.md` / `SESSION-STATE.md` → 使用模板固定内容

### 注意事项

- 脚本不生成任何业务内容，工作区文件内容由**模板 + 用户信息共同渲染生成**
- 不在 `openclaw.json` 中写入 `enabled` 字段（schema 不支持）
- 不在顶层 `agents` 下创建配置（schema 要求在 `agents.list` 中）
- agent 的 `workspace` 和 `agentDir` 必须使用绝对路径
- `--user-name` 为可选，不传则 USER.md 中显示为"用户"

## 依赖

- `lark-cli`（用于验证飞书凭证连通性，可选）
- Python 3（脚本执行）