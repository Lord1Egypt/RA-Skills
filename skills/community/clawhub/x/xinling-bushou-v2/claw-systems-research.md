# 类CLAW系统适配调研报告

> 调研人：阿探 🔍  
> 日期：2026-04-09  
> 参考：心灵补手 v1.0（技能位置：~/.openclaw/workspace/skills/xinling-bushou/）

---

## 心灵补手现有架构回顾

在分析各系统之前，先梳理心灵补手（xinling-bushou）的现有设计作为参照基准：

| 维度 | 实现方式 |
|------|----------|
| **人格/角色系统** | 4种风格（太监/丫鬟/早喵/司机），通过INSERT_TO_SOUL.md注入SOUL.md |
| **配置文件格式** | JSON（~/.xinling-bushou/config.json） |
| **配置参数** | enabled/level/persona/gender/mode |
| **可插拔性** | 注入式设计，不影响原人格 |
| **安全机制** | 硬过滤/软转向/频率限制/防觉醒 |
| **API扩展** | 通过pickup_lines/lines.json种子库驱动 |
| **扩展方式** | 大模型智能扩展，而非硬编码 |

---

## 一、各系统调研

### 1. Claude Code（Anthropic官方CLI）

**人格/角色系统实现方式**

Claude Code 采用 **SKILL.md 技能系统**，遵循 [agentskills.io](https://agentskills.io) 开放标准。技能定义在 `SKILL.md` 文件中，通过 YAML frontmatter（description/name/tags）和 Markdown 内容组成。Claude 自主判断何时调用技能，也可通过 `/skill-name` 手动触发。

角色/人设通过 **CLAUDE.md** 文件实现（项目级 `CLAUDE.md` 或 `.claude/CLAUDE.md`，用户级 `~/.claude/CLAUDE.md`），以及 **Output Styles**（持久化配置，影响系统提示词语气/格式）。

**配置文件存储位置**

- 项目级：`{cwd}/CLAUDE.md` 或 `{cwd}/.claude/CLAUDE.md`
- 用户级：`~/.claude/CLAUDE.md`
- Skills：`.claude/skills/`（项目级）、`~/.claude/skills/`（用户级）
- 插件：`{plugin}/.claude-plugin/plugin.json`
- 输出样式：`~/.claude/settings.json`

**API扩展能力**

- **MCP（Model Context Protocol）**：标准协议，支持连接外部工具/数据库/API
- **Custom Tools**：通过 `@tool`（Python）或 `tool()`（TypeScript）装饰器定义工具，封装为 in-process MCP server
- **Hooks**：在关键执行节点拦截/定制 agent 行为
- **Plugins**：打包为本地目录，通过 `plugin.json` 声明 commands/skills/agents/hooks/MCP servers

**是否有类似"技能"/"人格"机制**

✅ **强支持**。Claude Code 是与 OpenClaw 亲缘最近的系统：
- Skills（技能）：SKILL.md 标准格式，与 OpenClaw 的 SKILL.md 高度相似
- Agents（子代理）：可定义专业子代理
- Output Styles（输出风格）：类似"人格"变体
- 插件机制：支持打包分发

---

### 2. Cursor（AI代码编辑器）

**人格/角色系统实现方式**

Cursor 通过 **.cursorrules** 文件（项目根目录）实现项目级规则，格式为 Markdown，定义代码风格/响应语气/工作流偏好。通过 VS Code 设置（`cursor.json`）配置全局偏好，如 AI 语气选项（Concise/Formal/Warm等）。Cursor 3.0 引入 **Agent Tab** 支持多聊天并行，**Composer** 支持多文件编辑。

**配置文件存储位置**

- 项目级：`.cursorrules`（项目根目录）
- 全局设置：`~/.config/Cursor/User/settings.json`（VS Code兼容路径）
- MCP配置：`cursor.json` 中的 `mcpServers` 字段
- 快捷指令：在 Cursor Settings 中管理

**API扩展能力**

- **MCP服务器**：通过 cursor.json 配置 MCP 服务器连接
- **Bugbot**：代码审查Bot，支持 learned rules（从PR反馈中学习规则）和 MCP 工具接入
- **Cloud Agents**：支持自托管云端 agent（企业级）
- **多模型支持**：OpenAI/Anthropic/Gemini/xAI 等

**是否有类似"技能"/"人格"机制**

⚠️ **弱支持**。Cursor 的 .cursorrules 主要面向**代码风格**，而非独立人格/角色。缺乏类似 SKILL.md 的模块化技能定义。没有明显的多风格人格切换机制，但支持多 agent 并行运行。

---

### 3. GitHub Copilot

**人格/角色系统实现方式**

GitHub Copilot 提供 **Copilot Instructions**（.github/copilot-instructions.md）作为项目级指令文件，定义项目上下文/代码约定/特定任务指导。Copilot 没有独立的人格系统，AI行为主要受提示词上下文和代码补全的驱动。**Copilot Spaces** 提供更结构化的上下文管理。

**配置文件存储位置**

- 项目级：`.github/copilot-instructions.md`
- Workspace设置：github.com 设置中的 Copilot 配置
- MCP配置：GitHub 开发者设置中配置 MCP 服务器
- Spaces：Copilot Dashboard 中的虚拟工作空间

**API扩展能力**

- **MCP（Model Context Protocol）**：Copilot 支持 MCP 服务器集成
- **Copilot Extensions**：通过 GitHub Marketplace 分发的扩展
- **API Integration**：可对接 GitHub API 获取仓库上下文
- **Copilot Voice**：语音交互（有限）

**是否有类似"技能"/"人格"机制**

❌ **不支持**。Copilot 定位为**代码补全工具**，而非 agent 系统。没有人格/角色机制，不支持技能定义文件。扩展能力主要通过 MCP 和官方 Extensions 实现。

---

### 4. Cline（VS Code AI扩展）

**人格/角色系统实现方式**

Cline 通过 **Custom Instructions**（VS Code设置中配置 systemPrompt）定制 AI 行为。支持**自定义命令**（在 `.cline/` 目录或 VS Code 设置中定义）。通过 VS Code 的 `cline.customInstructions` 设置注入系统级提示词。没有独立的角色/人格系统，但支持通过不同 systemPrompt 模拟不同角色。

**配置文件存储位置**

- 全局设置：`~/.config/Code/User/settings.json`（或 VS Code settings.json）
- Cline专属：`cline.*` 配置项
- MCP配置：VS Code settings 中的 `cline.mcpServers`
- API Key：`cline.apiKey` / `cline.openRouterApiKey` 等

**API扩展能力**

- **MCP（Model Context Protocol）**：Cline 是 MCP 的积极推动者，支持创建新工具和扩展自身能力
- **多API Provider**：OpenRouter/Anthropic/OpenAI/Gemini/AWS Bedrock/Azure/GCP Vertex/Cerebras/Groq
- **Browser Use**：可控制浏览器进行网页交互
- **Human-in-the-loop**：每步操作需用户批准（安全设计）

**是否有类似"技能"/"人格"机制**

⚠️ **弱支持**。Cline 通过 systemPrompt 注入人格，没有标准化技能文件。但其 MCP 支持意味着可以**通过 MCP 服务器实现扩展能力**，在某种程度上等效于"技能"。

---

### 5. Roo Code（VS Code AI扩展）

**人格/角色系统实现方式**

Roo Code 与 Cline 类似，基于自主编码 agent，支持 **systemPrompt 自定义**。通过 VS Code settings 配置指令和规则。功能集与 Cline 相近，主要差异在 UI/UX 和默认行为调教。

**配置文件存储位置**

- VS Code settings.json：`roo.*` 配置项
- MCP配置：同 Cline
- API Keys：VS Code 密钥存储

**API扩展能力**

- MCP支持（Model Context Protocol）
- 多Provider支持
- Human-in-the-loop 审批机制

**是否有类似"技能"/"人格"机制**

⚠️ **弱支持**，与 Cline 基本一致。

---

### 6. Custom GPTs（OpenAI）

**人格/角色系统实现方式**

Custom GPTs 是 OpenAI 的 GPT Builder 产品，通过 **Custom Instructions**（"Instructions"字段）定义GPT行为，通过"Conversation Starters"提供快速入口，通过 **Knowledge**（文件上传）提供上下文。没有独立的人格文件，但可通过 Instructions 模拟角色。

**配置文件存储位置**

- OpenAI 平台：保存在用户的 GPT 列表中（云端）
- API方式：通过 OpenAI Assistants API 的 instructions 参数定义
- 知识文件：上传到 OpenAI 服务器

**API扩展能力**

- **Actions（自定义动作）**：通过 OpenAPI Schema 定义外部 API 调用
- **Knowledge Retrieval**：上传文件作为知识库
- **Plugin生态**：接入第三方服务
- ** Assistants API**：通过 API 编程方式创建/管理 agent

**是否有类似"技能"/"人格"机制**

⚠️ **中等支持**。Custom GPTs 通过 Instructions 模拟人格，但缺乏独立的技能模块化机制。Actions 机制可以扩展工具能力，但并非以"技能"为单位。

---

## 二、适配可行性分析

| 系统 | 人格机制 | 配置文件格式 | API扩展 | 技能机制 | 适配难度 |
|------|---------|------------|---------|---------|---------|
| **Claude Code** | ✅ 强（SKILL.md/SOUL.md类比） | JSON/MD | ✅ MCP+Custom Tools | ✅ SKILL.md标准 | ⭐ 低 |
| **Cursor** | ⚠️ 弱（.cursorrules） | JSON/MD | ✅ MCP | ❌ 无 | ⭐⭐ 中 |
| **GitHub Copilot** | ❌ 无 | MD | ✅ MCP | ❌ 无 | ⭐⭐⭐ 高 |
| **Cline** | ⚠️ 弱（systemPrompt） | JSON | ✅ MCP | ❌ 无（但可MCP模拟） | ⭐⭐⭐ 高 |
| **Roo Code** | ⚠️ 弱（systemPrompt） | JSON | ✅ MCP | ❌ 无 | ⭐⭐⭐ 高 |
| **Custom GPTs** | ⚠️ 中（Instructions） | 云端 | ✅ Actions | ❌ 无 | ⭐⭐⭐ 高 |

### 关键发现

1. **Claude Code 是最佳适配目标**：SKILL.md 标准与 OpenClaw 高度兼容，MCP 支持完善，Output Styles 类比人格系统，Plugins 机制支持打包分发。

2. **MCP 是跨系统扩展的事实标准**：Cline/GitHub Copilot/Cursor/Claude Code 均支持 MCP。可通过 MCP 服务器将心灵补手封装为跨平台工具。

3. **配置文件格式的差异**：Claude Code 用 MD/JSON，OpenClaw 用 SOUL.md/JSON，适配层需要做格式转换。

4. **人格机制的差异**：OpenClaw 的"叠加层"设计（INSERT_TO_SOUL.md）是独特创新，其他系统多采用"整体替换"方式。

---

## 三、优先适配建议

### 🥇 第一优先级：Claude Code

**推荐理由**：
- SKILL.md 标准与 OpenClaw 技能格式高度相似
- 插件架构（Plugins）支持打包技能分发
- 输出样式（Output Styles）已有人格概念
- MCP 支持完善，可扩展工具能力
- Anthropic 官方维护，与 OpenClaw 同源

**适配方案**：
1. 将 `xinling-bushou/` skill 目录结构映射到 `.claude/skills/xinling-bushou/SKILL.md`
2. 将 SOUL.md 的 INSERT_TO_SOUL.md 内容适配为 SKILL.md 的 frontmatter description
3. 通过 MCP server 封装 pickup_lines 和 config 读写能力
4. 创建 Claude Code 专属的 output style 定义文件

### 🥈 第二优先级：Cursor

**推荐理由**：
- 最大的 AI 代码编辑器用户群（NVIDIA CEO 推荐）
- MCP 支持意味着可通过 MCP 协议扩展
- 多 agent 并行能力强

**适配方案**：
1. 通过 Cursor 的 MCP 配置接入心灵补手 MCP 服务器
2. 将 .cursorrules 扩展支持心灵补手指令
3. Bugbot 的 learned rules 机制可借鉴到心灵补手的安全层

### 🥉 第三优先级：MCP 通用封装

**推荐理由**：
- MCP 是跨所有主流系统的扩展协议
- 一次封装，可同时支持 Claude Code/Cursor/Cline/GitHub Copilot

**适配方案**：
1. 将心灵补手核心功能封装为 MCP 服务器（stdio 传输）
2. MCP 服务器注册为 tool，供各系统调用
3. 心灵补手的话术生成/配置管理通过 MCP 协议暴露

---

## 四、总结

| 结论 | 详情 |
|------|------|
| **最值得优先适配** | Claude Code（架构最接近OpenClaw） |
| **最快出成果** | MCP 封装（一套协议，多系统复用） |
| **最大用户群** | Cursor（企业用户50强）+ GitHub Copilot |
| **最独特的能力** | 心灵补手的"叠加层"设计——其他系统均无类似机制 |
| **技术壁垒** | 人格叠加层 + 智能话术扩展（其他系统难以复制） |

---

*阿探出品 🔍 | 筑星队架构组*
