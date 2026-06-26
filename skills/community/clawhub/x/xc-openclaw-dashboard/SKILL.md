# OpenClaw Dashboard

> 🤖 你的 AI Agent 团队实时监控面板 — 一眼看穿所有 Agent 的运行状态

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)

## 功能特性

- **📊 Token 消耗监控** — 实时统计所有 Session 的 Token 总消耗
- **📚 多 Agent 支持** — 同时监控多个 Agent 的运行状态
- **🖥️ 系统信息概览** — 节点、Channel、模型版本一目了然
- **📱 飞书卡片推送** — 漂亮的富文本卡片，直接推送到群聊

## 解决的问题

- ✅ 想知道 Agent 消耗了多少 Token？
- ✅ 想知道哪个 Agent 最吃资源？
- ✅ 想知道有多少个活跃 Session？
- ✅ 想快速查看所有 Agent 的健康状态？

## 触发命令

| 命令 | 说明 |
|------|------|
| `/status-card` | 向当前飞书会话推送状态卡片（推荐） |
| `/sessions` | 列出当前所有活跃 session |
| `/status` | 快速查看简要状态信息 |

## 使用前提

- OpenClaw 版本 ≥ 3.8
- 飞书 Channel 已正确配置（如需卡片推送功能）
- `openclaw status` 命令可正常执行

## 技术原理

通过调用 `openclaw status` 命令解析输出，获取：
- 所有活跃 Session 的 Token 消耗
- Agent 类型和活跃时间
- 系统配置信息

## 文件结构

```
openclaw-dashboard/
├── SKILL.md           # 本文件
├── README.md          # 详细文档
├── index.js           # 命令入口
├── scripts/
│   └── collector.js   # 数据采集
├── dashboard.html     # 可视化网页（可选）
└── config.json        # 配置
```

## 作者

[Xu Chenglin](https://github.com/xc66o)

**如果你觉得有用，请给个 ⭐️！**
