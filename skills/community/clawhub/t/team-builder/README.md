# team-builder

多 Agent 团队工作区生成工具。一条命令搭起完整的团队骨架，包含角色、信箱、看板、产品知识目录、cron 巡检、双开发轨模板。

---

## 🚀 首次使用：完整安装流程

### 第一步：确认前置条件

```bash
node -v        # 需要 Node.js 16+
openclaw status  # 确认 OpenClaw 已运行
```

### 第二步：运行生成脚本（交互式）

```bash
node ~/.openclaw/skills/team-builder/scripts/deploy.js
```

脚本会依次询问：
- 团队名称（如 `Alpha Team`）
- 工作区路径（默认 `~/.openclaw/workspace-team`）
- 时区（默认 `Asia/Shanghai`）
- 晨报/晚报时间（默认 8 / 18）
- 思考型模型（用于 chief-of-staff / product-lead / growth-lead）
- 执行型模型（用于 devops / fullstack-dev 等）
- CEO 称呼（如 `老板` / `Boss`）
- 各角色名称（可直接回车用默认值）

> 💡 不想交互？用 `--config`，见下方「非交互部署」。

### 第三步：应用配置（写入 openclaw.json）

```bash
node <工作区路径>/apply-config.js
```

这一步把生成的 Agent 写入 OpenClaw 配置，**必须执行**。

### 第四步：创建定时任务

**Windows（PowerShell）：**
```powershell
powershell <工作区路径>/create-crons.ps1
```

**macOS / Linux（Bash）：**
```bash
bash <工作区路径>/create-crons.sh
```

### 第五步：重启 Gateway

```bash
openclaw gateway restart
```

### 第六步：CEO 填写项目上下文 ⚠️ 重要

打开工作区里的 `shared/onboarding.md`，**填写以下内容**：

```markdown
## 当前项目/产品
（是什么产品，目标用户，核心功能一句话）

## 现在进展到哪步
（已完成什么，当前在做什么）

## 最近完成的里程碑
（近期上线/交付了什么，时间）

## 当前最大阻塞
（卡在哪里，需要什么才能继续）

## 技术栈/代码目录
（主要技术栈，代码在哪个路径）
```

> ⚠️ **这一步非常重要**：所有 Agent 启动时会先读这个文件。不填的话 Agent 不知道你在做什么项目，会从零开始问你。
> 填完后告知 chief-of-staff（直接在群里说一声），它会开始正式工作。

### 第七步：验证（可选但推荐）

```bash
node ~/.openclaw/skills/team-builder/scripts/deploy.js --verify --config <配置文件路径>
```

输出结构化 JSON 检查报告，覆盖 `core / roles / fallback / workflow / hygiene / cron`。

---

## ⚙️ 非交互部署（推荐用于重复/CI 场景）

准备配置文件 `team-builder.json`：

```json
{
  "teamName": "Alpha Team",
  "workspaceDir": "~/.openclaw/workspace-team",
  "timezone": "Asia/Shanghai",
  "morningHour": 8,
  "eveningHour": 18,
  "thinkingModel": "claude-sonnet-4-5",
  "executionModel": "claude-sonnet-4-5",
  "ceoTitle": "老板",
  "roles": ["chief-of-staff", "product-lead", "devops", "fullstack-dev", "growth-lead", "content-chief", "intel-analyst", "data-analyst"],
  "roleNames": {
    "chief-of-staff": "参谋长",
    "product-lead": "产品总监",
    "devops": "交付总监",
    "fullstack-dev": "全栈工程师",
    "growth-lead": "增长总监",
    "content-chief": "内容主编",
    "intel-analyst": "情报分析师",
    "data-analyst": "数据分析师"
  }
}
```

运行：
```bash
node ~/.openclaw/skills/team-builder/scripts/deploy.js --config team-builder.json
```

---

## 📁 生成物说明

| 文件/目录 | 说明 |
|-----------|------|
| `AGENTS.md` | 启动引导 + 角色对照表 |
| `SOUL.md` | 团队价值观（可自定义） |
| `USER.md` | CEO 信息 |
| `shared/onboarding.md` | **CEO 填写项目背景**（新增，首次必填） |
| `shared/status/team-dashboard.md` | 团队状态面板（chief-of-staff 维护） |
| `shared/decisions/active.md` | CEO 决策与指令 |
| `shared/products/_index.md` | 产品矩阵目录 |
| `shared/inbox/to-[role].md` | 各角色信箱 |
| `shared/knowledge/team-workflow.md` | 团队工作流规范 |
| `agents/[role]/SOUL.md` | 各角色身份与职责 |
| `agents/[role]/MEMORY.md` | 各角色长期记忆 |
| `apply-config.js` | 写入 openclaw.json（手动执行） |
| `create-crons.ps1 / .sh` | 创建 cron 定时任务（手动执行） |
| `references/coding-behavior-fallback.md` | fullstack-dev 编码行为兜底 |

---

## 🧠 Agent 启动顺序（已内置于 AGENTS.md）

每个 Agent 启动时自动按此顺序读文件：

1. 确认自己的角色身份
2. 读 `agents/[role]/SOUL.md`
3. **读 `shared/onboarding.md`**（项目背景，CEO 填写）
4. **读 `shared/status/team-dashboard.md`**（当前状态）
5. 读 `shared/decisions/active.md`（仅当涉及策略/决策时）
6. 读 `shared/inbox/to-[role].md`（自己的收件箱）
7. 读 `agents/[role]/MEMORY.md`（仅当需要历史上下文时）

---

## 🔄 双开发轨模型

```
product-lead  ←→  需求澄清 / PRD / 验收标准 / 路由
     ↓
devops           ←→  部署 / 环境 / QA gate / 发布
fullstack-dev    ←→  项目内实现 / 模块深挖 / 连续编码
```

编码执行分层：
- 简单任务 → 直接执行
- 中等任务 → ACP run / direct acpx
- 复杂任务 → 现有 ACP session 连续性 + context file

---

## 📋 可选角色说明

| 角色 ID | 职责 | 模型类型 |
|---------|------|---------|
| `chief-of-staff` | 路由器 + 调度 + 策略（**必选**） | 思考型 |
| `product-lead` | 产品管理 + 需求澄清 + 验收 | 思考型 |
| `devops` | 交付 + 部署 + QA | 执行型 |
| `fullstack-dev` | 代码实现 + 模块深挖 | 执行型 |
| `growth-lead` | GEO + SEO + 社区 + 社媒 | 思考型 |
| `content-chief` | 内容策略 + 写作 + 本地化 | 思考型 |
| `intel-analyst` | 竞品情报 + 市场趋势 | 执行型 |
| `data-analyst` | 数据分析 + 用户研究 | 执行型 |

---

## 🔧 常用命令速查

```bash
# 交互式生成
node ~/.openclaw/skills/team-builder/scripts/deploy.js

# 非交互生成
node ~/.openclaw/skills/team-builder/scripts/deploy.js --config team-builder.json

# 验证生成结果
node ~/.openclaw/skills/team-builder/scripts/deploy.js --verify --config team-builder.json

# 应用配置
node <工作区>/apply-config.js

# 重启 gateway
openclaw gateway restart
```

---

## ✅ 安装后检查清单

- [ ] `apply-config.js` 已执行，openclaw.json 已更新
- [ ] `create-crons.ps1 / .sh` 已执行，定时任务已创建
- [ ] `openclaw gateway restart` 已执行
- [ ] `shared/onboarding.md` 已填写项目背景
- [ ] `shared/products/_index.md` 已填写产品信息
- [ ] `shared/decisions/active.md` 已填写 CEO 指令
- [ ] 已在群里告知 chief-of-staff 开始工作

---

## 相关文件

- `SKILL.md` — Agent 技能描述
- `scripts/deploy.js` — 核心生成脚本
- `references/shared-templates.md` — 共享文件模板
- `references/soul-templates.md` — 角色 SOUL 模板
- `references/coding-behavior-fallback.md` — 编码行为兜底规则
- `references/agent-refs/` — 各角色方法论参考文件

---

## 最近更新

- **2026-04-02**：新增 `shared/onboarding.md` 项目背景引导文件；`AGENTS.md` 启动顺序加入读 onboarding 步骤；README 重写为中文完整安装指引
- **2026-03-29**：`deploy.js --verify` 扩展为结构化 JSON 检查报告；生成物自动带 `team-workflow.md`
