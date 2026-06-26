# Scheduled Tasks Skill | 定时任务技能

> **OpenClaw + 飞书定时任务解决方案**  
> **Version | 版本**: 2.1.7  
> **Author | 作者**: 9527  
> **License | 许可证**: MIT  

---

## 🎯 功能特性

- ✅ 两种定时方式（OpenClaw Cron + 系统 Crontab）
- ✅ 一次性提醒和周期性任务
- ✅ 详细的故障排查指南
- ✅ 安全审查通过（无敏感信息）

---

## 📦 安装

```bash
clawhub install scheduled-tasks
```

---

## 🚀 快速开始

### 创建一次性提醒

```bash
openclaw cron add \
  --name "喝水提醒" \
  --at "20m" \
  --session main \
  --system-event "主人，该喝水了 💧" \
  --wake now \
  --delete-after-run
```

### 创建每日定时任务

```bash
openclaw cron add \
  --name "每日新闻" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent <agent-id> \
  --message "搜索今日新闻并推送" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

---

## 📁 目录结构

```
scheduled-tasks/
├── SKILL.md                          # 技能文档
├── README.md                         # 使用说明
├── LICENSE.md                        # MIT 许可证
├── scripts/
│   ├── task-manager.sh               # 任务管理工具
│   └── maintenance-reminder.sh       # 维护提醒脚本
└── references/
    └── troubleshooting.md            # 故障排查指南
```

**文件总数**: 6 个核心文件

---

## 📚 文档说明

| 文件 | 说明 |
|------|------|
| **SKILL.md** | 完整技能文档（双语） |
| **README.md** | 快速开始指南 |
| **scripts/** | 脚本工具 |
| **references/** | 故障排查指南 |

---

## 🛠️ 故障排查

遇到问题？查看 [references/troubleshooting.md](references/troubleshooting.md)

---

## 📋 更新日志

### Version 2.1.7 (2026-03-27)

**精简优化**：
- 🎯 只包含 6 个核心文件
- 🗑️ 移除 tests 目录（开发测试用）
- 🗑️ 移除模板文件（参考用）
- 🗑️ 移除所有内部文档
- ✅ 修复 Security Scan 问题
- ✅ 修复 frontmatter 格式
- ✅ 修复路径引用问题

**文件**：
- SKILL.md - 技能文档
- README.md - 使用说明
- LICENSE.md - MIT 许可证
- scripts/task-manager.sh - 任务管理
- scripts/maintenance-reminder.sh - 维护提醒
- references/troubleshooting.md - 故障排查

---

### Version 2.1.6 (2026-03-26)

**安全修复**：
- 🔒 移除敏感路径引用
- 🔒 添加安全声明
- 🔒 改进示例代码

---

### Version 2.1.0 (2026-03-26)

**初始合并版本**：
- 🎉 合并 scheduled-tasks 和 openclaw-scheduler
- 📚 完整双语文档
- 🧪 完整测试套件
- 🔒 安全审查通过

---

## 🙏 致谢

感谢所有贡献者！

---

## 📧 支持

- **文档**: https://docs.openclaw.ai
- **社区**: https://discord.com/invite/clawd
- **技能市场**: https://clawhub.com

---

*Made with 💙 by 9527*
