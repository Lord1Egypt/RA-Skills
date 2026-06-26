# 🤖 OpenClaw Dashboard

> 你的 AI Agent 团队实时监控面板 — 一眼看穿所有 Agent 的运行状态

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![OpenClaw](https://img.shields.io/badge/OpenClaw-3.8+-orange)

---

## 🎯 这个 Skill 解决什么问题？

**当你运行多个 AI Agent 时，是否遇到过这些困扰？**

- ❓ "我的 Agent 现在消耗了多少 Token？还剩多少？"
- ❓ "哪个 Agent 最吃资源？需要清理了吗？"
- ❓ "现在有多少个活跃 Session？都是哪些？"
- ❓ "每次想看状态都要敲命令，还不好记"

**OpenClaw Dashboard 就是答案！** 一条命令，所有 Agent 的状态一目了然。

---

## ✨ 核心功能

### 📊 Token 消耗监控
- 实时统计所有 Session 的 Token 总消耗
- 按 Agent 排序，快速定位资源大户
- 显示每个 Session 的 Context 使用百分比

### 📚 多 Agent 支持
- 同时监控多个 Agent（recruit-director、zero、bianju、jia_baili 等）
- 区分 Session 类型（direct / group / cron）
- 显示每个 Agent 的活跃状态

### 🖥️ 系统信息概览
- 节点名称、Channel、模型版本
- Agent 数量统计
- 一目了然的健康状态

### 📱 多种输出格式
- **飞书卡片**：漂亮的富文本卡片，直接推送到群聊
- **简洁文字**：快速文字输出，适合终端
- **网页仪表盘**：可视化大屏，实时刷新（可选）

---

## 🚀 快速开始

### 安装

```bash
clawhub install openclaw-dashboard
```

### 使用

**发送状态卡片到飞书：**
```
/status-card
```

**查看所有活跃 Session：**
```
/sessions
```

**快速状态概览：**
```
/status
```

---

## 📖 详细功能说明

### Token 监控

| 指标 | 说明 |
|------|------|
| 总消耗 | 所有 Session 的 Token 消耗总和 |
| Session 数 | 当前活跃的会话数量 |
| Context 上限 | 200K / session（MiniMax 模型） |

### Session 列表

每个 Session 显示：
- **Agent 名称** — 哪个 Agent
- **类型** — direct（私聊）/ group（群聊）/ cron（定时任务）
- **活跃时间** — 最后活跃是多久前
- **Token 消耗** — 消耗了多少 tokens

### Agent 数量统计

自动识别你运行的所有 Agent：
- `recruit-director` — 主控 Agent
- `zero` — 零号 Agent
- `bianju` — 编剧 Agent
- `jia_baili` — 甲贝利 Agent
- 以及更多...

---

## 🎨 输出示例

### 飞书卡片

```
┌─────────────────────────────────┐
│  🤖 OpenClaw 多 Agent 状态       │
├─────────────────────────────────┤
│  📊 Token 使用情况               │
│  总消耗: 559K tokens            │
│  会话数: 10 个活跃               │
│  Context 上限: 200K/session     │
├─────────────────────────────────┤
│  📚 活跃 Sessions                │
│  • jia_baili/feishu: 129K      │
│  • zero/feishu: 117K           │
│  • bianju/main: 109K           │
│  • ...还有 7 个 session        │
├─────────────────────────────────┤
│  🖥️ 系统信息                    │
│  节点: DESKTOP-XXX             │
│  Channel: feishu               │
│  Agent 数: 4                   │
└─────────────────────────────────┘
```

### 文字输出

```
📊 Token 总消耗: 559K tokens
📚 活跃 Sessions: 10 个
🖥️ 模型: MiniMax-M2.5-highspeed
```

---

## 🔧 配置

编辑 `config.json` 自定义行为：

```json
{
  "tokenLimit": 200000,
  "maxSessions": 50,
  "sessionTimeoutHours": 24
}
```

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `tokenLimit` | 200000 | Context 上限（根据模型调整） |
| `maxSessions` | 50 | 最多显示的 Session 数 |
| `sessionTimeoutHours` | 24 | 多久前的 Session 算活跃 |

---

## 💡 适用场景

### 1. 资源管理
当你想知道 Token 消耗情况，决定是否需要清理 Session 时。

### 2. 多 Agent 协作
同时运行多个 Agent 时，监控每个 Agent 的负载。

### 3. 定时汇报
结合 OpenClaw Cron，每小时自动推送状态报告。

### 4. 故障排查
当 Agent 响应变慢时，检查是否是 Context 快满了。

---

## 📂 文件结构

```
openclaw-dashboard/
├── SKILL.md           # 技能定义
├── README.md          # 本文档
├── index.js           # 命令入口
├── scripts/
│   ├── collector.js   # 数据采集（调用 openclaw status）
│   └── renderer.js    # 网页版渲染
├── dashboard.html     # 可视化网页（可选）
└── config.json        # 配置文件
```

---

## 🔒 安全说明

- 数据来源：`openclaw status` 命令（本地执行）
- 无外部 API 调用
- 不收集任何敏感信息
- 完全开源，可审查代码

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📝 更新日志

### v1.0.0 (2026-03-20)
- 初始版本发布
- 支持 Token 监控、多 Agent 列表
- 支持飞书卡片推送
- 支持网页可视化仪表盘（可选）

---

## 👨‍💻 作者

由 [Xu Chenglin](https://github.com/xc66o) 开发

**如果你觉得有用，请给个 ⭐️！**

---

## 许可证

MIT License — 可以自由使用、修改、分发。
