# Hook 接入指南（yotta-learn）

Hook 是可选的自动提醒/自动捕获机制。核心能力（log/list/promote/review/stats/extract）不依赖 hook，
本目录提供各智能体的配置模板与 Linux-only 的 bash 辅助脚本。

| 文件 | 用途 | 平台 |
|---|---|---|
| claude-settings.json | Claude Code settings.json hook 配置模板 | 通用 |
| codex-settings.json | Codex settings.json hook 配置模板 | 通用 |
| openclaw-setup.md | OpenClaw 接入说明 | 通用 |
| activator.sh | 每次会话开始提醒 review 学习条目 | Linux-only |
| error-detector.sh | 命令失败时自动检测并提示记录 | Linux-only |

bash hook 依赖 Unix shell，Windows 请只用 JSON 模板中的 python 命令形式。
