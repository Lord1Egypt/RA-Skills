# 🧠 Self-Improving Agent v2.0

> **自我反思 + 自我学习 + 自我改进** 的 AI 代理系统

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://clawhub.com/skills/self-improving)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-published-orange.svg)](https://clawhub.com/skills/self-improving)

---

## ✨ 功能亮点

### 🔄 每日自动反思（3 次/天）
- **09:00** 早晨反思 - 回顾昨天，规划今天
- **14:00** 下午反思 - 上午复盘，调整下午
- **21:00** 晚上反思 - 全天总结，整理记忆

### 💾 对话记录全量保存
- ✅ 文字对话 - 永久保存
- ✅ 图片 - 永久保存
- ✅ 重要决策 - 提取到长期记忆
- 🔄 视频/大文件 - 月度清理

### 📚 智能记忆管理
- 每天小整理（21:00）
- 每周大整理（周日）
- 每月深度整理（月末）

---

## 🚀 快速开始

### 安装

```bash
# 从 ClawHub 安装
clawhub install self-improving

# 或从 GitHub 克隆
git clone https://github.com/openclaw/skills.git
cd skills/self-improving
```

### 配置

```bash
# 查看 Cron 任务
openclaw cron list

# 启用定时任务（已自动启用）
openclaw cron update <jobId> --enabled true
```

### 使用

```bash
# 手动反思
python scripts/memory_manager.py reflect evening

# 保存对话
python scripts/memory_manager.py save "主题" "要点 1" "要点 2"

# 整理记忆
python scripts/memory_manager.py organize

# 清理大型文件
python scripts/memory_manager.py cleanup 30
```

---

## 📋 Cron 定时任务

| 任务 | 时间 | 说明 |
|------|------|------|
| 记忆反思 - 早晨 | 每天 09:00 | 回顾昨天，规划今天 |
| 记忆反思 - 下午 | 每天 14:00 | 上午复盘，调整下午 |
| 记忆反思 - 晚上 | 每天 21:00 | 全天总结，整理记忆 |
| 记忆清理 - 月度 | 每月 1 号 09:00 | 清理>30 天的视频和大文件 |

---

## 📁 项目结构

```
self-improving/
├── SKILL.md              # OpenClaw 技能说明
├── README.md             # 本项目说明
├── CHANGELOG.md          # 更新日志
├── package.json          # 项目配置
├── LICENSE               # MIT 许可证
├── scripts/
│   └── memory_manager.py # 记忆管理主脚本
├── cron/
│   └── reflection_jobs.json # Cron 配置
└── tests/
    └── test_memory.py    # 测试脚本
```

---

## 🆚 v2.0 更新内容

### 新增功能

- ✅ 每日自动反思 3 次（Cron 定时）
- ✅ 对话记录全量保存
- ✅ 图片永久保存
- ✅ 视频月度清理
- ✅ MEMORY.md 自动整理
- ✅ 4 个 Cron 定时任务

### 核心改动

| 功能 | v1.0 | v2.0 |
|------|------|------|
| 反思频率 | 手动 | 自动 3 次/天 |
| 对话保存 | ❌ | ✅ 全量 |
| 图片保存 | ❌ | ✅ 永久 |
| 视频清理 | ❌ | ✅ 月清理 |
| 记忆整理 | ❌ | ✅ 自动 |

---

## 💡 使用示例

### 保存重要对话

```bash
python scripts/memory_manager.py save "职业讨论" "优先畅联达" "ToAPIs 不错" "薪资 18-30K"
```

### 手动反思

```bash
# 早晨反思
python scripts/memory_manager.py reflect morning

# 下午反思
python scripts/memory_manager.py reflect afternoon

# 晚上反思
python scripts/memory_manager.py reflect evening
```

### 整理记忆

```bash
# 整理到 MEMORY.md
python scripts/memory_manager.py organize
```

---

## 📊 记忆存储策略

### 永久保存（不清理）

```
✅ 所有文字对话
✅ 所有图片
✅ 重要决策
✅ 用户偏好
✅ 代码/脚本
✅ MEMORY.md
✅ memory/YYYY-MM-DD.md
```

### 月度清理（>30 天）

```
🔄 视频文件
🔄 大型附件
🔄 临时文件
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

```bash
# Fork 项目
git fork https://github.com/openclaw/skills.git

# 创建分支
git checkout -b feature/your-feature

# 提交更改
git commit -m "feat: add your feature"

# 推送分支
git push origin feature/your-feature

# 创建 PR
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 👥 作者

- **Jarvis** - Initial work

---

## 🙏 致谢

- OpenClaw 团队
- ClawHub 社区
- 所有贡献者

---

## 📞 联系方式

- **ClawHub**: https://clawhub.com/skills/self-improving
- **GitHub**: https://github.com/openclaw/skills
- **Issues**: https://github.com/openclaw/skills/issues

---

*Made with ❤️ by Jarvis*
*Version: 2.0.0 | Last Updated: 2026-03-20*
