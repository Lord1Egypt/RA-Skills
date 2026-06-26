---
name: Skill Manager All In One | 一站式技能管理器
description: Manage OpenClaw skills end-to-end. 一站式管理 OpenClaw 技能的创建、修改、发布、更新、升版与审计。
license: MIT-0
---

# Skill Manager All In One | 一站式技能管理器

本技能可能指导 agent 检查、创建、编辑、移动、发布或审计 OpenClaw 技能文件；它不是只读文档型技能。

**所需工具**：clawhub / git / gh
**授权**：ClawHub 发布需要已登录会话；GitHub 发布需要 Git/GitHub 授权。执行发布类命令前必须展示精确命令并等待「确认-<username>」电子签名。

---

## 模式 | Mode

> 读取本 SKILL.md 后，先确认当前任务属于哪种模式，再跳转对应章节执行。

| 模式 | 说明 |
|------|------|
| **create** | 从零创建新技能 |
| **modify** | 修改已发布技能（升版/功能调整） |
| **audit** | 审计本地或已发布技能的质量、逻辑、声明完整性 |
| **local-test** | 仅本地测试，不发布 |

---

## 核心原则 | Core Rules

1. **Local first, network second** — 先检查本地已安装技能，再搜索网络。
2. **Be concrete** — 汇报时写清楚准确路径、准确命令、准确版本变化。
3. **One by one, confirm one by one** — 涉及多个文件/版本/技能时，必须逐个处理、逐个确认。每项确认都必须获得「确认-<username>」格式的电子签名授权，禁止批量操作。
4. **Publish like a product** — 发布文本应像正式发布说明，而非聊天记录。
5. **For AI and humans** — 技能正文应兼顾 agent 与人类可读性。
6. **English first, Chinese second** — 对外展示文本统一先英文后中文；包括 `name`、SKILL.md frontmatter `description`（发布到 ClawHub 后显示为 registry `summary` / CLI `Summary:`）、Changelog、README 关键标题与核心段落。中文不能因英文过长而被预览截断。
7. **Learn from release evidence** — 发布流程规则来自真实发布证据；新增检查项前先确认它能防止具体失误，而不是堆砌流程。

---

## 技能制作流程 | Phase 1: Create / Modify

> 按顺序执行，边做边对照第 6 章「统一检查清单」的【通用质量基线】。

### 步骤 1：明确需求

确定以下四项，作为后续所有操作的依据：

- **目标平台**：ClawHub / GitHub / 其他
- **版本号**：首次发布为 `1.0.0`

> ⚠️ Display name 和 Skill slug 是 ClawHub 专属概念，若目标平台为 ClawHub，请在 Phase 2 步骤 1 确认。

### 步骤 2：创建技能（参考 skill-creator）

**创建或修改技能内容前，先读 skill-creator 的完整流程。**

skill-creator 是创建技能的唯一权威参考，包含：
- SKILL.md 写法（Anatomy of a Skill）
- 目录结构规范（Skill folder layout）
- 编写技巧（Concise is Key / Set Appropriate Degrees of Freedom）
- 打包与发布流程

```
~/.openclaw/workspace/skills/<slug>/
```

### 步骤 3：边做边查——对照清单

每完成一个文件或代码块，立即对照第 6 章【通用质量基线】逐项打勾。

**目标平台已确定时，附加对应平台专项（ClawHub → CH01-CH11，GitHub → GH01-GH06）。**

### 步骤 4：修改项目的渠道核查

修改已发布技能时（如升版、功能调整、名称/slug 变更），必须核查以下渠道：

| 渠道 | 说明 |
|------|------|
| 本地文件系统 | 项目目录、技能目录、模型缓存（如有）、项目内所有引用旧名称的文件 |
| Git remote | `git remote -v` 中的仓库名 |
| Memory 文件 | MEMORY.md、memory/*.md、TOOLS.md 等中的名称 |
| GitHub repo | repo slug + description |
| ClawHub | slug + display name（通过重新发布更新） |

**如涉及名称或 slug 变更（改名 = 全量替换）：**

1. **审计**：搜索所有渠道中的旧名称
   ```bash
   # 搜索项目内所有旧名称
   grep -rn "<old-slug>\|<old-display-name>" \
     ~/.openclaw/workspace/projects/<slug>/ \
     --include="*.md" --include="*.html" --include="*.js" --include="*.json"
   # 搜索 memory 文件
   grep -rn "<old-slug>\|<old-display-name>" \
     ~/.openclaw/workspace/MEMORY.md \
     ~/.openclaw/workspace/memory/
   # 检查 GitHub
   gh repo view <owner>/<repo> --json name,description
   ```

2. **改文件内容**（先文字，后目录名，否则路径会断）

3. **改本地目录名 + git remote**
   ```bash
   mv ~/.openclaw/workspace/projects/<old-slug>/ ~/.openclaw/workspace/projects/<new-slug>/
   mv ~/.openclaw/workspace/skills/<old-slug>/ ~/.openclaw/workspace/skills/<new-slug>/
   git remote set-url origin <new-url>
   ```

4. **改线上平台**：GitHub（`gh repo rename`）→ ClawHub（重新发布）

5. **改 Memory**：MEMORY.md + memory/*.md

6. **验证**：全渠道搜索旧名称，确认零残留

**两步验证**：改名涉及多处写入，必须走两步验证。先汇报变更清单（渠道+位置+旧值+新值），等「确认-<username>」后再执行。

> 如 Phase 1 已逐项打勾通用基线，Phase 2 只需复核 + 补充平台专项，不必重复全量检查。

---

## 技能发布验证流程 | Phase 2: Publish

> 必须完成 Phase 1 后才能执行本阶段。

### 步骤 1：确认基本信息 & 复查清单

**ClawHub 目标时，先确认以下两项：**
- **Display name**：`EN Title | CN Title` 双语格式（对应 CH01）
- **Skill slug**：小写字母 + 连字符，如 `speech-synthesizer`

**然后复查清单：**
- 对照第 6 章【通用质量基线】全部项（G01-G06）
- 根据目标平台，额外核对【平台专项】（ClawHub → CH01-CH11，GitHub → GH01-GH06）
- 逐项标注 ✅ / ⚠️，有问题的立即修复

### 步骤 2：⚠️ 两步验证（强制，必须执行）

**无论改动多小、无论第几次修改，两步验证不可跳过。**

> 详细操作步骤见对应 reference：ClawHub → `references/clawhub-publish.md`；GitHub → `references/github-publish.md`；推广 → `references/promotion.md`

两步验证核心原则：
- **第一步**（AI 内部执行，不输出给用户）：清单核对 + 文件大小 + 对外表述检查 + 拟定 changelog
- **第二步**：向用户输出完整汇报模板（第 9 章），等待「确认-<username>」后才执行发布

**确认标志**：用户必须回复「确认-<username>」，不得用「好」「确认」「上传」「发吧」等语义模糊的词汇替代。

**⚠️ 两步验证适用于所有发布类操作**：clawhub publish / git push / gh release create / 推广发帖 / 社交平台发帖等。

### 步骤 3：执行发布

获得用户确认后，执行对应平台的发布命令。
> ClawHub 上传详见 `references/clawhub-publish.md`；GitHub 上传详见 `references/github-publish.md`。

**若用户拒绝发布**：回到 Phase 1 修改流程，递增修订版本号（如 1.2.1 → 1.2.2-dev），不得直接重复尝试发布相同内容。

---

## 发布后维护 | Phase 3: Maintain

参考 Phase 1 修改流程 + 版本号递增 → 回到 Phase 2 两步验证。

- **升版/更新**：ClawHub → `references/clawhub-publish.md`；GitHub → `references/github-publish.md`
- **宣传/推广**：读 `references/promotion.md`（Moltbook 格式、AI心理学、去标识化）
- **查看详情**：ClawHub → `clawhub inspect <slug>`（详情见 `references/clawhub-publish.md` 中的 Inspect 命令参考）
- **GitHub**：`git log` 验证
- **回滚**：clawhub → `clawhub delete <slug> --yes`（软删除）；GitHub → `git revert`
- **隐藏/恢复/删除**：执行前报告 + 执行后验证

---

## 安全扫描说明 | Security Scans（仅限 ClawHub）

ClawHub 发布后会自动进行三项安全扫描（GitHub 发布无此流程）。

### 三项扫描介绍

| 扫描 | 扫描对象 | 判定方式 | 误报率 |
|------|---------|---------|--------|
| VirusTotal | 整个发布包（zip） | 外部引擎 + Code Insight LLM | 高（敏感能力类技能常见 Review） |
| ClawScan | SKILL.md + metadata | OpenClaw 自有 LLM 分析 | 中（可通过声明优化） |
| Static Analysis | 代码模式 | 静态规则匹配 | 低 |

### VirusTotal 常见结果

| 结果 | 含义 | 处理方式 |
|------|------|----------|
| Benign | ✅ 通过 | 无需处理 |
| Review | 平台标记了敏感能力（如私信读写、浏览器自动化） | 功能性质决定，无法消除，接受（需向用户说明原因） |
| Suspicious | 检测到可疑模式（非功能性质） | ❌ 必须修复，向用户汇报具体可疑内容 |

### ClawScan 常见 findings 类型

- Tool Misuse and Exploitation（工具滥用）
- Agentic Supply Chain Vulnerabilities（供应链风险）
- Identity and Privilege Abuse（身份权限滥用）
- Memory and Context Poisoning（上下文泄露）

| 结果 | 含义 | 处理方式 |
|------|------|----------|
| Benign | ✅ 通过 | 无需处理 |
| Review | 检测到敏感能力，但有缓解措施 | 优化 SKILL.md 声明（加两步验证、数据披露、凭据声明）降低 severity |

### Static Analysis 常见结果

| 结果 | 含义 | 处理方式 |
|------|------|----------|
| Benign | ✅ 通过 | 无需处理 |
| 非 Benign | 命中注入/路径风险等规则 | ❌ 列出具体命中规则，修复代码 |

### 发布后汇报流程（ClawHub 专有）

> 发布后必须汇报 ClawHub 平台的安全扫描结果。扫描结果可能需要数分钟到数小时才全部完成。

**发布后汇报时机：**
- 如果发布后立即能看到结果（数分钟内），当场汇报
- 如果发布后结果尚未完成，告知用户稍后查看 `https://clawhub.ai/<username>/<slug>/security`（`<username>` 为你的 ClawHub 用户名）

**汇报格式（SOP）：**
```markdown
## 🔍 技能安全扫描汇报 | <slug> v<version>

**技能：** <Display name>
**slug：** <slug>
**版本：** <version>
**复查时间：** <YYYY-MM-DD HH:MM>

### 安全扫描结果

| 扫描项 | 结果 | 处理 |
|--------|------|------|
| VirusTotal | Benign / ⚠️ Review / ❌ Suspicious | <处理方式> |
| ClawScan | Benign / ⚠️ Review | <处理方式> |
| Static analysis | Benign / ❌ 非 Benign | <处理方式> |

### 问题与修复（如有）
- <扫描项>: <具体问题描述> → <修复方案>（需用户「确认-<username>」后执行）
```

**处理原则：**
- Benign → 无需处理
- 非 Benign → 逐项列出问题，向用户说明，寻求「确认-<username>」授权后修复

---

## 统一检查清单 | Checklist（制作与发布共享）

**上游参考技能保护**：不要直接修改上游/参考技能，尤其是 `skill-creator`。它会随 OpenClaw 或上游版本更新而变化；本技能只能把本地经验沉淀到 `skill-manager-all-in-one` 自己的 SKILL.md / references 中。若确实需要修改上游技能，必须先向用户说明原因、影响和恢复方案，等待明确授权。

| # | 检查项 | 说明 |
|---|---------|------|
| G01 | 去标识化 | 无个人信息、内部路径、私有凭证 |
| G02 | 安全性 | 无注入风险（Shell注入/Python注入/路径注入）、无过度权限、无数据外传 |
| G03 | 逻辑科学性 | 结构清晰、路径准确、模块化、**同名规范** |
| G04 | AI 可读性 | agent 可理解、上下文连贯、无歧义指令 |
| G05 | 易维护性 | 代码整洁、注释到位、变量命名清晰、模块化 |
| G06 | 依赖/凭据声明 | 外部 Python 包、命令行工具、API、模型、账号权限、凭据来源、文件系统写入范围必须明确声明；不得硬编码密钥。发布类技能需声明 `clawhub`/`git`/`gh` 等工具及验证命令。

### ClawHub 专项（附加于通用基线之后）

| # | 检查项 | 说明 |
|---|---------|------|
| CH01 | Display Name 双保险 | **ClawHub 页面展示名必须双保险**：`SKILL.md` frontmatter 的 `name:` 填 `EN Title | CN Title`，发布命令也必须显式传 `--name "EN Title | CN Title"`。实测仅改 `name:` / `_meta.displayName` 更新版本时，ClawHub 顶部展示名可能不会同步中文。例：`clawhub publish <path> --slug speech-synthesizer --name "TTS Speaker | TTS 朗读器" --version 1.0.1 ...` |
| CH02 | Skill slug | 技能唯一标识符，小写字母 + 连字符（例：`speech-synthesizer`）；在 `~/.openclaw/workspace/skills/<slug>/` 目录名和 `clawhub publish` 命令中使用 |
| CH03 | SKILL.md description 双语且≤150字符 | SKILL.md frontmatter `description` 是发布到 ClawHub 后的 registry `summary`（CLI 显示为 `Summary:`）。要求：先英文后中文，总字符数控制在 150 以内（含中英文、标点、空格），英文部分优先短句，确保中文在卡片预览可见、不被截断。 |
| CH04 | Changelog 格式 | 英文在前（面向用户描述功能变化，而非开发者心理活动）、双语数字列表。**禁止提及安全扫描结果或扫描器名称**（如 ClawScan、VirusTotal、SUSPICIOUS、Benign 等），changelog 只描述功能改动本身，不得暗示意图影响扫描判定。 |
| CH05 | Embedding 500 应急 | 当 SKILL.md 或引用的 reference 文件超过 500 行时，自动拆分或提供摘要版本 |
| CH06 | 文件/模型分离 | 技能文件夹（`~/.openclaw/workspace/skills/<slug>/`）**严禁存放任何模型文件、运行产物、结果文件**。模型文件统一放 `~/.cache/huggingface/modules/<slug>/`；运行文件与结果文件统一放 `~/.openclaw/workspace/projects/<slug>/`。技能文件夹本身仅含技能代码（SKILL.md、脚本、配置文件等），大小应控制在 50MB 以内。发布前 `du -sh <skill-dir>` 超过 50MB 需立即处理。 |
| CH07 | 版本号一致性 | `_meta.json` version、changelog 版本号、发布命令版本号三者必须一致 |
| CH08 | 对外表述顺序统一 | 所有面向用户的双语表述统一先英文后中文：Display name、SKILL.md `description` / ClawHub `Summary:`、Changelog、README 关键标题、核心说明、示例说明。避免一处中文在前、一处英文在前造成发布页风格不一致。 |
| CH09 | 坏符号链接 | 无失效符号链接 |
| CH10 | 运行时产物 | 无 `.pyc`、`.pyo`、`__pycache__`、`.log` 等运行时产物 |
| CH11 | 目录隔离 | 确保技能文件夹内无 `.git/`、`.DS_Store`、`Thumbs.db` 等无关元数据 |
| CH12 | 英中文顺序检测 | 关键信息先英文后中文：① Display name 用 `|` 分隔（如 `EN Title | CN Title`）；② description 不用 `|`，英文句在前、中文句在后，≤150字符；③ Changelog 英文在前、中文在后；④ SKILL.md 正文关键标题/说明、references 关键内容均为先英文后中文。不因顺序检查影响技能高效与稳定。 |

### GitHub 专项（附加于通用基线之后）

> ⚠️ 必须先通过通用质量基线 G01-G06。

| # | 检查项 | 说明 |
|---|---------|------|
| GH01 | git status | 无未提交变更（`git status` 干净） |
| GH02 | 分支规范 | main/master 分支干净，commit 原子化 |
| GH03 | commit 规范 | commit message 简洁、描述性、一行概括 + 详细说明 |
| GH04 | Release Notes | 格式规范，与 changelog 内容一致 |
| GH05 | 文件完整性 | 无多余临时文件 |
| GH06 | License 检查 | 发布前确认包含合适开源许可证文件（如 MIT），或明确声明无许可证 |

---

## 技能目录体系 | Directory System

| 目录 | 路径 |
|------|------|
| 正式技能 | `~/.openclaw/workspace/skills/<slug>/` |
| 插件技能 | `~/.openclaw/extensions/` |
| 临时草稿 | `~/.openclaw/workspace/temp-skills/<slug>/` |
| 工作区资源（项目） | `~/.openclaw/workspace/projects/<slug>/` |
| 模型缓存 | `~/.cache/huggingface/modules/<slug>/` |
| **项目总规范** | `~/.openclaw/workspace/projects/README.md` |

### 项目 SOP（强制）

所有 `projects/` 下的项目均遵循 **项目 README** 规范（分项目可选）：

| 层级 | 何时需要 | 内容 |
|------|---------|------|
| **项目 README** | 必须 | 项目目标、结构、所有分项目入口（如有）、关键产出索引、进展日志（**若无分项目，日志直接写在这里**） |
| **分项目 README** | 可选（当项目有多个独立方向或体量较大时） | 该分项目目标、结构、核心产出清单、Agent Handoff Log |
| **总规范** | 只在 `projects/README.md` 存在一份 | 通用 SOP（不含具体项目名） |

> **渐进披露原则**：MEMORY.md 不重复项目内容，项目详情查 `projects/README.md` 指引。

### 各目录职责（强制分离）

> **技能文件夹 = 纯技能代码**。禁止放入任何模型、运行产物、结果文件。

| 目录 | 职责 | 禁止放入 |
|------|------|---------|
| `~/.openclaw/workspace/skills/<slug>/` | 技能代码（SKILL.md、脚本、配置） | 模型文件、运行结果、输出文件 |
| `~/.openclaw/workspace/projects/<slug>/` | 运行文件、结果输出、数据文件 | 技能源代码 |
| `~/.cache/huggingface/modules/<slug>/` | 所有模型文件（.pt/.onnx 等） | 非模型文件 |

**示例（speech-transcriber 技能）：**
```
~/.openclaw/workspace/skills/speech-transcriber/     # ✅ 技能代码（SKILL.md、scripts/、requirements.txt）
~/.openclaw/workspace/projects/speech-transcriber/   # ✅ 运行文件与结果（transcriptions/、recordings/、outputs/）
~/.cache/huggingface/modules/speech-transcriber/     # ✅ 模型文件（small/、medium/）
```

### 命名规范 | Naming Convention

**⚠️ 重要：项目目录和模型缓存必须与技能名（slug）保持一致。**

---


## 汇报模板 | Report Template

汇报时必须包含以下全部内容。SOP 格式：逐项列表格，逐项打 ✅ / ⚠️。

### 汇报格式

```markdown
## 🔍 技能发布汇报 | <Display name> v<version>

**Display name：** <EN Title | CN Title>
**Skill slug：** <slug>
**目标平台：** clawhub / github
**SKILL.md description：** <English sentence. 中文句子。>（<N> 字符）
**当前版本：** <old> → **新版本：** <new>
**Changelog：**
1. <English update>. <中文更新>。

**文件大小：** <N>KB

---

### 核对清单

> 汇报时逐项标注 ✅ / ⚠️，有问题的在「问题与修复」中说明。

**通用质量基线（G01-G06，所有技能必检）：**

| # | 检查项 | 状态 | 备注 |
|---|--------|------|------|
| G01 | 去标识化 | ✅/⚠️ | 无个人信息、内部路径、私有凭证 |
| G02 | 安全性 | ✅/⚠️ | 无注入风险、无过度权限、无数据外传 |
| G03 | 逻辑科学性 | ✅/⚠️ | 结构清晰、路径准确、模块化、同名规范 |
| G04 | AI 可读性 | ✅/⚠️ | agent 可理解、上下文连贯、无歧义指令 |
| G05 | 易维护性 | ✅/⚠️ | 代码整洁、注释到位、变量命名清晰 |
| G06 | 依赖/凭据声明 | ✅/⚠️ | 外部包/工具/密钥已声明，无硬编码 |

**平台专项（根据目标平台二选一）：**

**→ ClawHub 目标时（CH01-CH12）：**

| # | 检查项 | 状态 | 备注 |
|---|--------|------|------|
| CH01 | Display Name 双保险 | ✅/⚠️ | `name:` = `EN Title | CN Title`；`--name` 参数一致 |
| CH02 | Skill slug | ✅/⚠️ | 小写字母 + 连字符 |
| CH03 | description ≤150字符 | ✅/⚠️ | 英文在前、中文在后，总字符 ≤150，不用 `\|` 分隔 |
| CH04 | Changelog 格式 | ✅/⚠️ | 英文在前、中文在后，数字列表，正式语气 |
| CH05 | Embedding 500 应急 | ✅/⚠️ | SKILL.md + references 均 ≤500 行，否则拆分 |
| CH06 | 文件/模型分离 | ✅/⚠️ | 技能文件夹 ≤50MB，无模型/结果文件 |
| CH07 | 版本号一致性 | ✅/⚠️ | `_meta.json` / changelog / 发布命令三处一致 |
| CH08 | 对外表述顺序统一 | ✅/⚠️ | 所有双语表述均先英文后中文 |
| CH09 | 坏符号链接 | ✅/⚠️ | 无失效符号链接 |
| CH10 | 运行时产物 | ✅/⚠️ | 无 .pyc / .pyo / __pycache__ / .log |
| CH11 | 目录隔离 | ✅/⚠️ | 无 .git / .DS_Store / Thumbs.db 等无关文件 |
| CH12 | 英中文顺序检测 | ✅/⚠️ | display name 用 `\|`、description 不用 `\|`、changelog 先英后中 |

**→ GitHub 目标时（GH01-GH06）：**

| # | 检查项 | 状态 | 备注 |
|---|--------|------|------|
| GH01 | git status | ✅/⚠️ | 无未提交变更 |
| GH02 | 分支规范 | ✅/⚠️ | main/master 干净，commit 原子化 |
| GH03 | commit 规范 | ✅/⚠️ | 英文在前、中文在后，简洁描述性 |
| GH04 | Release Notes | ✅/⚠️ | 与 changelog 内容一致 |
| GH05 | 文件完整性 | ✅/⚠️ | 无多余临时文件 |
| GH06 | License | ✅/⚠️ | 含合适开源许可证或声明无许可证 |

---

### 发布命令

```bash
clawhub publish <path> --slug <slug> --name "<EN Title | CN Title>" --version <version> --changelog "<text>"
```

### 问题与修复（如有）

- <检查项>: <具体问题> → <修复方案>（需用户「确认-<username>」后执行）
```

---

## 文件归属原则 | File Ownership

> 项目文件遵循 `~/.openclaw/workspace/projects/README.md` 中定义的 SOP。

| 文件类型 | 归属 |
|---------|------|
| 搜索 JSON / 索引文件 | paper-searcher-manager 项目 |
| 文献全文 / PDF | 各自项目/分项目的 `literature/` 或 `papers/` |
| 分析报告 / 结论性文档 | 分项目 `reports/` |
| 原始数据 / 清洗后数据 | 分项目 `data/` |
| 脚本 / 处理代码 | 分项目 `scripts/` |
| Zotero 文献库 | paper-searcher-manager 项目 |

**新建技能时**：同步在 `~/.openclaw/workspace/projects/` 下创建同名项目目录（遵循 projects/README.md 的三层 README 规范）：
- **项目 README**（`projects/<slug>/README.md`）：项目目标、结构、关键产出索引
- **分项目 README**（如需要）：在项目下再建子目录 + 对应 README
- **总项目 README**（`projects/README.md`）：通用规范，不含具体项目名称（仅在 projects 文件夹根目录存在一份）

> 不制造孤岛：不要让文件躲在 README 解释不到的地方。

---

## 实用说明 | Practical Notes

### 执行提示

- 执行敏感操作前，用 `clawhub --help` 核对当前 CLI 行为
- `skill-creator` 是底层规则权威来源
