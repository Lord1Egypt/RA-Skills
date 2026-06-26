# 安装 Super-Dev Skills for OpenCode

## 前置要求

- 已安装 [OpenCode.ai](https://opencode.ai)
- Git

## 安装

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

> **注意：** 在 Windows 上创建符号链接可能需要管理员权限或启用开发者模式。

重启 OpenCode 以发现技能。
验证方法：询问"列出可用技能"

## 可用技能

- **super-dev-orchestrator** — 🎯 总控调度：模式识别、任务委派、记忆存取
- **super-dev-requirements** — 📋 需求深访：5W2H-D 框架、用户故事、验收标准
- **super-dev-shared-language** — 🗣️ 统一语言：DDD 术语表、消除翻译损耗
- **super-dev-architect** — 🏗️ 架构设计：技术选型、数据库 DDL、ADR
- **super-dev-tdd** — 🧪 TDD 驱动：Red→Green→Refactor、测试金字塔
- **super-dev-ux** — 🎨 体验审计：AI 美学反模式 A1-A11、感官级验证
- **super-dev-security** — 🔒 安全门禁：Always/Ask/Never、四级扫描
- **super-dev-memory** — 🧠 分层记忆：三层记忆加载/写回/压缩
- **super-dev-evolution** — 🔄 自进化：Skill 提炼、Nudge Engine
- **super-dev-suite** — 📦 套件总览

### Agent-Skills 桥接

本套件内化 [agent-skills](https://github.com/addyosmani/agent-skills) 原则，支持 `/spec` `/build` `/test` `/review` `/ship` 桥接。

## 更新

```bash
cd ~/.super-dev-skills && git pull
```

符号链接将自动指向更新后的内容，无需重新链接。

## 卸载

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

## 故障排除

### 找不到技能

1. 验证符号链接是否存在：`ls -la ~/.config/opencode/skills/`
2. 每个技能文件夹应包含 `SKILL.md` 文件
3. 安装后重启 OpenCode

## 获取帮助

- 问题反馈：https://github.com/WeedFire/super-dev-skills/issues
