# Task Tracker - OpenClaw Skill

持久化任务管理 Skill，解决 AI Agent "断电丢活"问题。

## 功能

- 📋 收到任务自动拆解步骤，建档追踪
- ✅ 做一步打一个勾，进度实时可见
- 🔄 对话中断后自动恢复，接着干
- 👥 支持多 Agent 协作，谁做的谁打勾
- 📦 完成后自动检查 + 归档

## 核心理念

> 不信任对话记忆，只信任文件。状态全部落盘，断电不丢活。

## 安装

```bash
# ClawHub
clawhub install task-tracker

# 手动安装
# 将 SKILL.md 放到 OpenClaw workspace 的 skills/task-tracker/ 目录下
```

## 使用

给你的 Agent 一个多步骤任务，它会自动建档追踪。任务文件在 `tasks/` 目录下，Markdown 格式，人机都能一眼看懂。

## License

MIT
