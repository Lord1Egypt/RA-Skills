# TG 消息助手 多平台适配调研

调研日期：2026-06-05

## 目标

tg-message-assistant 目前仅在 telyclaw 环境中可用，需要适配 codex、openclaw 等主流平台。

## 当前平台绑定点（5 处）

| # | 绑定点 | 位置 | 具体内容 |
|---|--------|------|----------|
| 1 | 工具引用 | Step 2 | `telegram_get_messages` — telyclaw MCP 工具 |
| 2 | 工具引用 | Step 4 | `telegram_send_message` — telyclaw MCP 工具 |
| 3 | 工具引用 | Step 4 | `gmail_message_send`, `gmail_authorize` — telyclaw MCP 工具 |
| 4 | 插件检测 | Step 4 | "telyclaw plugin marketplace" — 平台专属分发渠道 |
| 5 | Cron 调度 | Step 5 | "OpenClaw's built-in cron functionality" — 平台专属调度引用 |

核心工作流（收集配置 → 拉取消息 → 生成简报 → 投递 → 定时调度）本身是**平台无关的**。

---

## 行业现状

### SKILL.md 已成为跨平台标准

- 2025-10：Anthropic 推出 Claude Code Skills
- 2025-11：OpenAI Codex CLI 实验性支持 Skills；OpenClaw 发布
- 2025-12：Anthropic 将 Agent Skills 发布为开放标准（agentskills.io）
- 2026 初：Codex CLI 将 Skills 设为默认；Claude Code、Codex、OpenClaw、Cursor、Copilot 等均支持 SKILL.md 格式

### 平台差异速查

| 维度 | Telyclaw (Claude Code) | Codex CLI | OpenClaw |
|------|----------------------|-----------|----------|
| 项目指令文件 | `CLAUDE.md` | `AGENTS.md` | `openclaw.json` |
| Skill 存储路径 | `.claude/skills/` | `.agents/skills/` | `~/.openclaw/skills/` |
| Skill 调用语法 | `/skill-name` | `$skill-name` | `/skill-name` |
| 隐式调用控制 | `disable-model-invocation` | `allow_implicit_invocation` | `disable-model-invocation` |
| 依赖声明 | 无 | MCP deps in `openai.yaml` | `bins`/`env`/`os`/`config` |
| Skill 分发 | Plugin marketplace + GitHub | `github.com/openai/skills` | ClawHub |

---

## 三种跨平台适配模式

### 模式 A：单一 SKILL.md + 平台专属段

**代表**：OpenClaw 官方 `coding-agent/SKILL.md`

一个文件内用条件块区分平台：

```yaml
# frontmatter
config:
  node-claude:
    kind: package
    package: "@anthropic-ai/claude-code"
    bin: claude
  node-codex:
    kind: package
    package: "@openai/codex"
    bin: codex
```

正文用平台专属区块描述不同平台的执行方式：
```markdown
**Claude Code:** `claude --permission-mode bypassPermissions --print < "$PROMPT"`
**Codex:** `codex exec - < "$PROMPT"`
**OpenCode:** `opencode run < "$PROMPT"`
```

- 优点：单文件维护
- 缺点：平台越多越臃肿，工具映射混在指令中

### 模式 B：core + 统一 SKILL.md（已采用）

实际落地结构（平台安装直接指向 skill 二级目录）：

```
tg-message-assistant/
├── SKILL.md                    # 统一入口：含三平台工具速查表 + 平台专属 setup 段
├── core/
│   └── prompt.md               # 共享的 5 步工作流 + 交互原则
├── assets/templates/           # 共享模板
├── references/
└── scripts/
```

设计要点：
- `SKILL.md` 引用 `./core/prompt.md`，三平台共用同一份工作流
- 工具映射通过平台速查表（3 列：Telyclaw / Codex CLI / OpenClaw）呈现
- 平台专属 setup（MCP 配置、OAuth 流程、Bot Token 等）放在各自 section

- 优点：单目录简洁，各平台直接 symlink 无需额外操作，核心逻辑只写一次
- 缺点：SKILL.md 随平台增加会变长（目前 3 个平台可控）

### 模式 C：PlatformAdapter 抽象层

**代表**：`dnviti/codeclaw` 项目

```python
class PlatformAdapter(ABC):
    discover_skills()    # 发现可用 skill
    invoke_tool()        # 统一工具调用
    ask_user()           # 统一用户交互
    get_config()         # 统一配置读取
    get_project_root()   # 统一项目根目录
    run_command()        # 统一命令执行
```

每个平台实现具体适配器：`claude_code.py`, `codex.py`, `openclaw.py`, `generic.py`

- 优点：最完整、最灵活，支持 8+ 平台
- 缺点：需要额外的脚本运行时，对纯 SKILL.md repo 来说过重

---

## 可参考的开源项目

| 项目 | 地址 | 说明 |
|------|------|------|
| ok-skills | `github.com/mxyhi/ok-skills` | 40+ 跨平台 skill，标准 SKILL.md 格式 |
| codeclaw | `github.com/dnviti/codeclaw` | PlatformAdapter 抽象层 + 多平台适配器实现 |
| openclaw/agent-skills | `github.com/openclaw/agent-skills` | OpenClaw 官方跨平台 skill 仓库 |
| tycho/agent-skills | `github.com/tychohq/agent-skills` | 18+ 平台兼容的 skill 集合 |
| cc-harness-skills | `github.com/LearnPrompt/cc-harness-skills` | 便携式跨平台 skills（memory/verification/coordination） |
| agent-skills-cli | npm: `agent-skills-cli` | 一键安装 skill 到 37+ agent 平台 |
| agentshift | PyPI: `agentshift` | Skill 平台间转译 CLI 工具 |

---

## 各平台 Telegram / Gmail 工具生态调研

### Codex CLI

#### Telegram

Codex CLI 通过 MCP 协议集成 Telegram 能力，主要方案：

| 方案 | 类型 | 能力 | 安装方式 |
|------|------|------|----------|
| **mcp-telegram** (`beautyfree/mcp-telegram`) | MCP Server (MTProto) | 102 个工具：读/搜/发消息、管理频道、联系人、语音转写，可直接调用原始 MTProto API | `npx -y mcp-telegram` |
| **TeleCodex** (`benedict2310/telecodex`) | Telegram Bot 桥接 | Telegram Bot → Codex CLI 双向桥接，手机上控制 Codex，streaming 响应 | 自部署 Docker |
| **CodexClaw** | Telegram Bot + MCP | 远程 Codex 访问，零信任访问控制，cron 调度器，多 agent 编排 | `mcpmarket.com` 下载 |

推荐使用 **mcp-telegram**：它是目前最完整的 MCP 方案，直接连接用户真实 Telegram 账号（非 Bot），工具覆盖全面。

**Codex CLI 配置** (`~/.codex/config.toml`):
```toml
[mcp_servers.telegram]
command = "npx"
args = ["-y", "mcp-telegram"]
env = { TELEGRAM_API_ID = "your_api_id", TELEGRAM_API_HASH = "your_api_hash" }
enabled = true
```

#### Gmail / Email

| 方案 | 类型 | 能力 | 安装方式 |
|------|------|------|----------|
| **@kembec/email-mcp** | MCP Server (Rust) | 支持 Gmail (OAuth2)、Outlook、iCloud，`list_messages`/`get_message`/`send_message`/`search_messages` | `npx -y @kembec/email-mcp` |
| **Composio Gmail MCP** | 托管 MCP | 托管的 Gmail MCP，高级搜索、自动草稿+发送、标签管理、联系人管理 | `composio.dev` 注册 |
| **Codex Official Gmail Plugin** | 官方插件 (2026.04) | `/plugins` 安装，内置 OAuth，与 Codex App/CLI/VS Code 统一体验 | `/plugins install gmail` |

推荐使用 **Codex Official Gmail Plugin**（最简）或 **@kembec/email-mcp**（功能最全）。

**Codex CLI 配置** (`~/.codex/config.toml`):
```toml
[mcp_servers.email]
command = "npx"
args = ["-y", "@kembec/email-mcp"]
enabled = true
```

#### Cron / 调度

- **CodexClaw**：内置 cron 调度器，支持主动式自动化（如每日摘要）
- **Codex Plugins**：部分插件自带 scheduling 能力
- **外部方案**：组合系统 cron + `codex exec` 命令

### OpenClaw

#### Telegram

OpenClaw 原生支持 Telegram 作为 **first-class channel**，无需额外 MCP Server：

- 在 `openclaw.json` 中配置 Telegram Bot Token（通过 @BotFather 获取）
- OpenClaw 直接连接 Telegram Bot API，可读/发消息
- 支持通过 Telegram 向自己的 AI 发指令

备选 MCP 方案：

| 方案 | 类型 | 能力 |
|------|------|------|
| **Telebiz MCP Skill** | ClawHub Skill | 通过浏览器执行器控制 Telegram，`clawhub install telebiz-mcp-skill` |
| **mcp-telegram** (`beautyfree/mcp-telegram`) | MCP Server | 同上表所述，OpenClaw 也可通过 MCP 协议连接 |

#### Gmail / Email

| 方案 | 类型 | 能力 | 安装方式 |
|------|------|------|----------|
| **AgentMail** | ClawHub Skill | 发送/阅读/回复/搜索/整理邮件 | `clawhub install agentmail` |
| **MCP Bundles Gmail** | MCP 服务 | 从任意渠道（Telegram/WhatsApp 等）通过 Gmail 发送摘要邮件 | `mcpbundles.com` 配置 OAuth |

**OpenClaw MCP 配置** (`openclaw.json`):
```json
{
  "mcp": {
    "servers": {
      "mcpbundles": {
        "url": "https://mcp.mcpbundles.com/hub/mcp",
        "headers": {
          "Authorization": "Bearer your_key_here"
        }
      }
    }
  }
}
```

#### Cron / 调度

OpenClaw 内置 cron 功能，直接在 skill 配置中使用，无需额外工具。

---

## 平台能力映射表（完整）

| 功能 | Telyclaw | Codex CLI | OpenClaw |
|------|----------|-----------|----------|
| Telegram 拉取消息 | `telegram_get_messages` | `mcp-telegram`（102 tools，含读/搜） | 原生 Telegram channel + `telebiz-mcp-skill` |
| Telegram 发送消息 | `telegram_send_message` | `mcp-telegram` | 原生 Telegram channel |
| Telegram 账号方式 | telyclaw 内置 | 真实用户账号 (MTProto) | Bot API (BotFather token) |
| Gmail 发送 | `gmail_message_send` + `gmail_authorize` | `@kembec/email-mcp` 或 Codex Official Gmail Plugin | `agentmail` (ClawHub) 或 MCP Bundles Gmail |
| Gmail 授权方式 | OAuth (telyclaw 内置) | OAuth2 (email-mcp) 或 Codex Plugin OAuth | OAuth (MCP Bundles) |
| Cron 调度 | `CronCreate` 工具 | CodexClaw cron / 系统 cron + `codex exec` | 内置 cron |
| 插件/Skill 安装 | telyclaw plugin marketplace | `/plugins install` 或 `~/.codex/config.toml` | `clawhub install` |
| Skill 发现路径 | `.claude/skills/` | `.agents/skills/` | `~/.openclaw/skills/` |

---

## 推荐方案：模式 B（core + adapters）

### 理由

- 适配目标明确（telyclaw → codex, openclaw），不需要模式 C 的完整抽象层
- 模式 A 在工具名完全不同时难以维护
- 模式 B 是社区验证的主流方案，适合 SKILL.md 仓库的纯配置特性

### 改造步骤

1. **提取 core/prompt.md** — 平台无关的工作流、模板选择规则、交互原则
2. **定义工具接口抽象** — 不硬编码工具名，用语义描述，各 adapter 自行映射到平台工具
3. **编写 adapters/** — 为 telyclaw、codex、openclaw 各写薄 SKILL.md
4. **平台 adapter 关键差异**：

#### Telyclaw adapter
- 工具：`telegram_get_messages`, `telegram_send_message`, `gmail_message_send`, `gmail_authorize`
- 插件检测：指向 telyclaw plugin marketplace
- Cron：`CronCreate` 工具
- 目标路径：`.claude/skills/tg-message-assistant/`

#### Codex adapter
- 工具：`mcp-telegram` 提供的 Telegram 工具 + `@kembec/email-mcp` 或 Codex Official Gmail Plugin 提供的 Gmail 工具
- 前置依赖声明：需在 `openai.yaml` 或 `~/.codex/config.toml` 中配置 MCP servers
- Cron：引导用户使用 CodexClaw cron 或系统 cron
- 目标路径：`.agents/skills/tg-message-assistant/`

#### OpenClaw adapter
- 工具：原生 Telegram channel 能力 + AgentMail (ClawHub) 提供的 Gmail 工具
- 前置依赖：需在 `openclaw.json` 中配置 Telegram Bot Token，安装 `agentmail` skill
- Cron：OpenClaw 内置 cron
- 目标路径：`.openclaw/skills/tg-message-assistant/`

### 实施 Plan（建议顺序）

1. 创建 `core/prompt.md`，从当前 SKILL.md 中提取平台无关的 5 步工作流和交互原则
2. 重构当前 SKILL.md → `adapters/telyclaw/SKILL.md`（薄包装，指向 core）
3. 编写 `adapters/codex/SKILL.md`（含 MCP 配置引导）
4. 编写 `adapters/openclaw/SKILL.md`（含 openclaw.json 配置引导）
5. 更新根目录 README 说明多平台安装方式
