# feishu_robot_creater（飞书机器人创建）

快速创建飞书机器人并连接到 OpenClaw，绑定专属 Agent。

---

## 适用环境

- 操作系统：Windows（当前机器）
- OpenClaw 版本：`2026.4.26`
- 当前工作区：`C:\Users\26462\.openclaw\workspace`
- OpenClaw 文档目录：`C:\Users\26462\AppData\Roaming\npm\node_modules\openclaw\docs`
- 主人称呼偏好：对用户统一称“主人”
- 当前主代理身份：皇帝（总后台 / 主代理）

> 本技能已按主人当前机器环境改写：路径、命令风格、Gateway 操作方式均以这台 Windows + OpenClaw 环境为准。

---

## 这个技能是做什么的

这个技能用于指导或协助创建一个新的飞书机器人，并把它接到 OpenClaw，让该机器人绑定到一个独立 Agent。

适合的场景：
- 想给不同用途创建不同飞书机器人
- 想把“工程师 / 客服 / 运营 / 设计师”等角色拆成独立 Agent
- 想让新的飞书机器人直接接入当前 OpenClaw 环境

---

## 命名规则

| 输入（中文） | Agent ID（英文） | Agent Name（中文） |
|--------------|------------------|-------------------|
| 工程师 | engineer | 工程师 |
| 测试机器人 | test-bot | 测试机器人 |
| 客服 | customer-service | 客服 |
| 运营 | operator | 运营 |
| 设计师 | visual-designer | 设计师 |

建议：
- `Agent ID` 使用小写英文或连字符
- 尽量避免空格、中文、特殊符号
- 飞书机器人中文名可按业务用途命名

---

## 完整流程

| 步骤 | 说明 |
|------|------|
| 1 | 访问创建链接 → 填名称+头像 |
| 2 | 获取 App ID + App Secret |
| 3 | 检查飞书事件与权限配置 |
| 4 | 创建 Agent 工作区结构 |
| 5 | 配置 OpenClaw |
| 6 | 重启 / 检查 Gateway |
| 7 | 验证连接 |

---

## 第 1 步：创建飞书应用

**访问链接**：https://open.feishu.cn/page/openclaw?form=multiAgent

**操作步骤**：
1. 打开链接后，点击「创建应用」
2. 输入机器人名称（如：工程师、客服、运营）
3. 选择一个头像（可选）
4. 点击「确定」或「创建」按钮
5. 记住创建的机器人名称，后续配置需要

---

## 第 2 步：获取凭证

**进入应用后台**：
1. 回到应用列表，点击刚创建的应用
2. 点击左侧菜单「凭证与基础信息」
3. 复制以下信息：
   - **App ID**（格式：`cli_xxxxxx`）
   - **App Secret**（点击「获取」按钮后复制）

**请保存好这两个凭证，后续配置必须用到。**

---

## 第 3 步：检查飞书事件与权限

在飞书开放平台中确认：

1. **事件订阅** 已开启
2. 已配置接收消息相关事件（至少确认私聊消息接收能力）
3. 应用处于可用状态
4. 如果平台要求补充权限，按飞书控制台提示完成

> 不同版本的飞书后台 UI 会变化，若字段名称略有不同，以当前控制台实际显示为准。

---

## 第 4 步：创建 Agent 工作区结构

建议在当前用户目录下为新 Agent 建立独立工作区。当前机器可参考：

- OpenClaw 主目录：`C:\Users\26462\.openclaw`
- Agent 工作区建议路径：`C:\Users\26462\.openclaw\agents\<agent-id>`

### 4.1 创建目录结构（PowerShell）

将 `<agent-id>` 替换为实际 Agent ID：

```powershell
$agentId = "<agent-id>"
$base = "C:\Users\26462\.openclaw\agents\$agentId"
New-Item -ItemType Directory -Force -Path "$base\agent" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\.learnings" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\memory" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\skills" | Out-Null
```

### 4.2 创建 MEMORY.md（重要）

建议初始化记忆文件：

```powershell
$agentId = "<agent-id>"
$botName = "<机器人名称>"
$memoryPath = "C:\Users\26462\.openclaw\agents\$agentId\memory\MEMORY.md"
@"
# MEMORY.md - $botName

## 基础信息
- 名称：$botName
- Agent ID：$agentId
- 创建时间：$(Get-Date -Format 'yyyy-MM-dd')

## 用户信息
（待填写）

## 偏好习惯
（待填写）

## 工作状态
- 状态：已配置，待首次对话
- 技能：无
"@ | Set-Content -Path $memoryPath -Encoding UTF8
```

> 是否“必须”创建该文件，取决于 Agent 设计；但实际使用中，提前建好 `memory\MEMORY.md` 更稳妥。

---

## 第 5 步：配置 OpenClaw

### 推荐原则

- 优先参考本机 OpenClaw 文档与当前版本行为
- 不使用旧教程里的 macOS/Linux 路径
- 不使用手工 `kill` 进程替代 Gateway 重启

### 5.1 Agent 配置思路

需要让 OpenClaw 知道这个新 Agent 的：
- `id`
- `name`
- `workspace`
- （如有需要）对应的 agent 目录

当前机器推荐工作区路径形态：

```text
C:\Users\26462\.openclaw\agents\<agent-id>
```

### 5.2 Feishu 账号配置思路

需要为飞书渠道补充：
- `appId`
- `appSecret`
- `botName`
- `enabled`
- 该机器人与 Agent 的绑定关系

### 5.3 绑定配置思路

目标是让：
- 飞书账号 `<agent-id>`
- 路由到 Agent `<agent-id>`

> 由于不同 OpenClaw 版本的配置结构可能存在扩展字段，实际填写时建议以当前本机文档和现有配置格式为准。

---

## 第 6 步：检查并重启 Gateway

当前环境下，优先使用 OpenClaw 官方子命令：

```powershell
openclaw gateway status
openclaw gateway restart
```

如果只是检查状态：

```powershell
openclaw status
```

> 不推荐使用旧文档中的 `ps | grep | kill` 流程；那套做法属于旧环境思路，在当前 Windows + OpenClaw 场景下并不合适。

---

## 第 7 步：验证连接

**测试方法**：
1. 打开飞书，搜索机器人名称
2. 给机器人发送一条消息（如：`你好`）
3. 如果收到回复，说明连接成功

**常见问题**：
- 如果没有回复，先检查 `openclaw gateway status`
- 检查 App ID 和 App Secret 是否正确
- 检查飞书后台事件订阅与权限
- 检查 Agent 与飞书账号的绑定是否一致

---

## 快速检查清单

- [ ] 访问创建链接并创建应用
- [ ] 获取并保存 App ID
- [ ] 获取并保存 App Secret
- [ ] 检查飞书事件与权限
- [ ] 创建 Agent 目录结构
- [ ] 初始化 `memory\MEMORY.md`
- [ ] 配置 Agent 信息
- [ ] 配置 Feishu 账号信息
- [ ] 配置绑定关系
- [ ] 执行 `openclaw gateway restart`
- [ ] 测试发送消息验证连接

---

## 命名参考

| 用途 | Agent ID | 中文名 |
|------|----------|--------|
| 代码开发 | engineer | 工程师 |
| 内容创作 | content-helper | 内容助手 |
| 热点追踪 | hot-tracker | 热点追踪 |
| 数据采集 | collector | 采集员 |
| 视觉设计 | visual-designer | 设计师 |
| 平台运营 | operator | 运营 |
| 客服 | customer-service | 客服 |
| 审核 | reviewer | 审核员 |
| 知识库 | knowledge-integrator | 知识库 |
