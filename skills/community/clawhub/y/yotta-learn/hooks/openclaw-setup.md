# OpenClaw Hook 接入

OpenClaw 使用 workspace 级提示注入 + 会话工具。接入方式：

1. 安装技能到 OpenClaw 技能目录。
2. 在 OpenClaw 配置中为「会话开始」事件挂载 yotta-learn 的 review 命令。
3. 可选：把 .learnings/ 目录加入 workspace，让各会话共享同一份学习库。

bash 辅助脚本（activator.sh / error-detector.sh）仅在 Linux 主机可用。
