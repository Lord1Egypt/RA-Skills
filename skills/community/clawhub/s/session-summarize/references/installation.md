# 安装方式与平台前置条件

## 一键安装（全平台通用，自动检测目标平台）

```bash
curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-error-skill/master/scripts/install.sh | bash
```

Windows PowerShell:

```powershell
iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-error-skill/master/scripts/install.ps1 | iex
```

安装脚本会自动检测当前平台（ZCode / CodeBuddy / Claude Code / Codex / Reasonix）并安装到对应目录。如果检测不到，会回退到 `~/.agent-skills/summarize`。

## 手动安装

```bash
# ZCode
git clone git@github.com:gtbwpkwjnb-alt/summarize-error-skill.git ~/.agents/skills/summarize

# CodeBuddy
git clone git@github.com:gtbwpkwjnb-alt/summarize-error-skill.git ~/.codebuddy/skills/summarize

# Claude Code
git clone git@github.com:gtbwpkwjnb-alt/summarize-error-skill.git ~/.claude/skills/summarize

# Codex
git clone git@github.com:gtbwpkwjnb-alt/summarize-error-skill.git ~/.codex/skills/summarize

# Reasonix
git clone git@github.com:gtbwpkwjnb-alt/summarize-error-skill.git ~/.reasonix/skills/summarize
```

## 更新

```bash
cd ~/.agent-skills/summarize && git pull
```

安装后输入 `总结` 或 `summarize` 即可触发。

## 平台前置条件

| 能力 | 是否必需 | 说明 |
|------|---------|------|
| 自定义技能/命令注入 | ✅ 必需 | 用于注入触发方式 |
| 文件系统读写 | ✅ 必需 | 存储收割数据和规则文件 |
| 会话历史访问 | ✅ 必需 | 模块1/2/3/4都需要读取当前会话 |
| 上下文使用率数据 | 🟡 可选 | 模块4 token统计；无数据时自动降级为字符估算 |

如果平台不支持某些能力，对应模块会自动降级。
