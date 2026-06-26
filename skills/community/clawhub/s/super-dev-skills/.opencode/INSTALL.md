# Installing Super-Dev Skills for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- Git

## Installation

### macOS / Linux

```bash
git clone https://github.com/WeedFire/super-dev-skills.git ~/.super-dev-skills

mkdir -p ~/.config/opencode/skills
for skill in ~/.super-dev-skills/clawhub-plugin/skills/*/; do
    skill_name=$(basename "$skill")
    ln -s "$skill" ~/.config/opencode/skills/"$skill_name"
done
```

### Windows (PowerShell)

```powershell
git clone https://github.com/WeedFire/super-dev-skills.git "$env:USERPROFILE\.super-dev-skills"

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\skills"
Get-ChildItem "$env:USERPROFILE\.super-dev-skills\clawhub-plugin\skills" -Directory | ForEach-Object {
    New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\skills\$($_.Name)" -Target $_.FullName
}
```

> **Note:** Creating symbolic links on Windows may require administrator privileges or Developer Mode enabled.

Restart OpenCode to discover the skills.
Verify by asking: "List available skills"

## Available Skills

- **super-dev-orchestrator** — 🎯 总控调度：模式识别、任务委派、记忆存取，桥接 agent-skills
- **super-dev-requirements** — 📋 需求深访：5W2H-D 框架、用户故事、验收标准
- **super-dev-shared-language** — 🗣️ 统一语言：DDD 术语表、消除翻译损耗
- **super-dev-architect** — 🏗️ 架构设计：技术选型、数据库 DDL、ADR 决策记录
- **super-dev-tdd** — 🧪 TDD 驱动：Red→Green→Refactor、测试金字塔、五轴审查
- **super-dev-ux** — 🎨 体验审计：AI 美学反模式检测（A1-A11）、感官级四维验证
- **super-dev-security** — 🔒 安全门禁：Always/Ask/Never、四级供应链扫描
- **super-dev-memory** — 🧠 分层记忆：事实/过程/经验三层记忆加载与压缩
- **super-dev-evolution** — 🔄 自进化：Skill 提炼、Nudge Engine、经验归档
- **super-dev-suite** — 📦 套件总览：架构说明与使用方式

### Agent-Skills Bridge

本套件内化 [agent-skills](https://github.com/addyosmani/agent-skills) 原则，支持 `/spec` `/build` `/test` `/review` `/ship` 桥接。

## Updating

```bash
cd ~/.super-dev-skills && git pull
```

Symlinks will automatically point to the updated content — no need to re-link.

## Uninstalling

### macOS / Linux

```bash
rm -f ~/.config/opencode/skills/super-dev-*
rm -rf ~/.super-dev-skills
```

### Windows (PowerShell)

```powershell
Get-ChildItem "$env:USERPROFILE\.config\opencode\skills\super-dev-*" | Remove-Item -Force
Remove-Item -Recurse -Force "$env:USERPROFILE\.super-dev-skills"
```

## Troubleshooting

### Skills not found

1. Verify symlinks exist: `ls -la ~/.config/opencode/skills/`
2. Each skill folder should contain a `SKILL.md` file
3. Restart OpenCode after installation

## Getting Help

- Report issues: https://github.com/WeedFire/super-dev-skills/issues
