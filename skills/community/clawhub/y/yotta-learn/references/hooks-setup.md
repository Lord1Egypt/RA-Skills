# Hook 详细接入步骤

## Claude Code

把 hooks/claude-settings.json 内容合并到 ~/.claude/settings.json（或项目 .claude/settings.json），
并把 PATH_TO_SKILL 替换为技能实际路径。

## Codex

把 hooks/codex-settings.json 内容合并到 ~/.codex/settings.json（或项目 .codex/settings.json），
并把 PATH_TO_SKILL 替换为技能实际路径。

## OpenClaw

按 hooks/openclaw-setup.md 接入；bash 辅助脚本仅 Linux 可用。

## 关闭 hook

删除对应配置段即可；不影响 yotta-learn 手动使用。
