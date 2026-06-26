# skill-evolver

[English](README.md) | [中文](README.zh-CN.md)

> 先解决问题，再决定是否沉淀成 skill。

`skill-evolver` 是一个面向 Claude Code、Codex 和 OpenClaw 风格运行时的、以规范驱动的 skill 全生命周期管理器。它帮助代理找到合适的 skill、判断是否安全、决定该直接编排还是深度融合，并在工作流被验证有效后，把它沉淀为可复用能力。

## Problem

大多数 AI coding workflow 在真正执行前就已经开始失控：

- **Skill 很难找**：可用能力分散在本地目录、公开 registry 和个人仓库里。
- **信任边界不清晰**：直接安装公开来源的 skill，往往缺少必要的安全审计。
- **组合方式不明确**：有时单个 skill 足够，有时需要编排，有时只能做深度融合。
- **复用机制不稳定**：很多高价值的一次性流程最后没有沉淀成可复用 skill。

## Solution

`skill-evolver` 把 skill 使用过程变成一套明确工作流，而不是临时试错：

- **先分析任务意图**，确认真正要解决的问题。
- **统一搜索本地和远程来源**，包括已安装 skill、`skills.sh` 和 ClawHub。
- **先检查再使用**，对候选 skill 做深入分析与安全审计。
- **让 LLM 负责路径判断**：原生执行、skill 编排，还是 skill 融合。
- **在人机协作节点设置检查点**，把高风险决策留给用户确认。
- **只在验证成功后再沉淀**，把真正值得复用的流程物化为 skill。

## What You Get

- **更安全的 skill 引入流程**，安装和使用前就完成验证与审计。
- **更清晰的决策路径**，明确什么时候该用原生能力、编排或融合。
- **完整的生命周期管理**，从发现到执行再到可选沉淀，一条链走通。
- **跨生态兼容性**，覆盖 Claude Code、Codex 与 OpenClaw 风格运行时。
- **可复现的输出结构**，通过模板、脚本和阶段产物固定工作过程。

## How It Works

```text
Phase 0: Setup Output Directory
Phase 1: Intent Analysis
Phase 2: Skill Search (local + skills.sh + ClawHub)
Phase 3: Deep Inspection
Checkpoint: Approach Decision
Phase 3.5: Skill Fusion (conditional)
Phase 4: Orchestration
Checkpoint: Plan Confirmation
Phase 5: Execution
Checkpoint: Materialization Decision
```

## Core Capabilities

- **双轨搜索**：一次流程同时覆盖本地 skill 和远程 registry。
- **安全审计**：识别破坏性命令、远程执行、凭据外传、权限提升等高风险模式。
- **LLM 路径决策**：评估任务匹配度，并给出原生执行、编排或融合建议。
- **Skill 融合**：把多个部分匹配的 skill 深度整合成新的能力。
- **工作流沉淀**：在流程被证明有复用价值后，再转成新的 skill。

## 安装

**推荐方式 (via skills.sh):**
```bash
npx skills add ClawSkill/skill-evolver -g -y
```

**手动安装:**
```bash
# 克隆仓库
git clone https://github.com/ClawSkill/skill-evolver.git

# 复制到 skills 目录
# macOS / Linux
cp -r skill-evolver/* ~/.claude/skills/skill-evolver/

# Windows (PowerShell)
Copy-Item -Recurse skill-evolver/* $env:USERPROFILE\.claude\skills\skill-evolver\
```

### 可选前置依赖

如果你要启用远程 registry 搜索，请安装对应 CLI：

```bash
# Skills.sh (Vercel) - 无需安装 通过npx直接启动
# Usage: npx skills find <query>
#        npx skills add <source> -g -y
# Docs: https://github.com/vercel-labs/skills

# ClawHub (OpenClaw) - 需要全局安装
npm i -g clawhub
# Usage: clawhub search "<query>"
#        clawhub install <slug>
# Docs: https://docs.openclaw.ai/zh-CN/tools/clawhub
```

## Repository Structure

```text
skill-evolver/
|-- SKILL.md
|-- scripts/
|   |-- search_skills.py
|   |-- audit_skill.py
|   `-- verify_skill.py
`-- references/
    |-- skill-search.md
    |-- skill-fusion.md
    |-- skill-inspector.md
    `-- templates/
        |-- 01-intent.md
        |-- 02-candidates.md
        |-- 03-inspection.md
        |-- 03b-fusion-spec.md
        `-- 04-orchestration.md
```

## License

本项目采用 [MIT License](LICENSE)。
