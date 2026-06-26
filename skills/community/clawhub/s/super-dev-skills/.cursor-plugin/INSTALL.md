# 安装 Super-Dev Skills for Cursor

将全栈之神套件启用到 Cursor 中，通过克隆仓库并指向 skills 目录即可。

## 前置要求

- 已安装 Cursor
- Git

## 安装

### macOS / Linux

```bash
git clone https://github.com/WeedFire/super-dev-skills.git ~/.cursor/super-dev-skills
```

在 Cursor 设置中将 Skills 路径设为：

```text
~/.cursor/super-dev-skills/clawhub-plugin/skills/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/WeedFire/super-dev-skills.git "$env:USERPROFILE\.cursor\super-dev-skills"
```

在 Cursor 设置中将 Skills 路径设为：

```text
C:\Users\YOUR_USERNAME\.cursor\super-dev-skills\clawhub-plugin\skills\
```

> 将 `YOUR_USERNAME` 替换为你的 Windows 账户名。

保存路径后，重启 Cursor 或重新加载窗口以重新扫描本地 skills。

## 可用技能

| Skill | 职责 |
|-------|------|
| 🎯 super-dev-orchestrator | 总控调度、模式识别、任务委派、记忆存取 |
| 📋 super-dev-requirements | 需求深访、5W2H-D、用户故事、验收标准 |
| 🗣️ super-dev-shared-language | DDD 统一语言、术语表、消除翻译损耗 |
| 🏗️ super-dev-architect | 架构设计、技术选型、ADR 决策记录 |
| 🧪 super-dev-tdd | 测试驱动开发、Red→Green→Refactor |
| 🎨 super-dev-ux | 感官级 UI/UX 验证、AI 美学反模式检测 |
| 🔒 super-dev-security | Always/Ask/Never 安全边界、供应链门禁 |
| 🧠 super-dev-memory | 三层记忆系统（事实/过程/经验） |
| 🔄 super-dev-evolution | 技能自进化、Nudge Engine、经验归档 |
| 📦 super-dev-suite | 套件总览 |

## 兼容 agent-skills

本套件内化了 [agent-skills](https://github.com/addyosmani/agent-skills) 的核心工程原则，并支持以下 slash 命令桥接：

| agent-skills 命令 | super-dev 等效阶段 |
|-------------------|----------------------|
| `/spec` | 自动激活 super-dev-requirements |
| `/build` + `/test` | 自动激活 super-dev-tdd |
| `/review` | 对应 TDD 的五轴审查 |
| `/ship` | 对应 super-dev-security + super-dev-memory |

## 验证

确认 clone 存在且包含 `SKILL.md` 文件：

### macOS / Linux

```bash
find ~/.cursor/super-dev-skills/clawhub-plugin/skills -maxdepth 2 -name SKILL.md
```

### Windows (PowerShell)

```powershell
Get-ChildItem "$env:USERPROFILE\.cursor\super-dev-skills\clawhub-plugin\skills" -Directory | ForEach-Object {
    Get-ChildItem $_.FullName -Filter SKILL.md
}
```

## 更新

### macOS / Linux

```bash
cd ~/.cursor/super-dev-skills && git pull
```

### Windows (PowerShell)

```powershell
Set-Location "$env:USERPROFILE\.cursor\super-dev-skills"
git pull
```

## 卸载

### macOS / Linux

```bash
rm -rf ~/.cursor/super-dev-skills
```

### Windows (PowerShell)

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.cursor\super-dev-skills"
```
