# Changelog

## 1.0.0 - 2026-04-15

- 清理发布包中的隐私与运行时文件（`.env`、`.session`、日志、锁文件、本地虚拟环境、测试脚本）。
- 统一默认会话名为 `tg_monitor_session`，移除个人路径示例。
- 重写根目录 `SKILL.md` 为可发布格式（frontmatter + instructions/rules/examples）。
- 新增 `clawhub.json`，补充 ClawHub 发布元数据。
- 更新 `.clawignore`，保留 `.env.example` 并强化敏感文件排除策略。
