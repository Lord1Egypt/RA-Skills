# Skills Auto Manager

🤖 **自动管理 OpenClaw skills 的智能助手**

---

## 📋 简介

Skills Auto Manager 是一个自动化的 skills 管理工具，帮助你：
- 🔍 定期检查 skills 更新
- 🛒 浏览 ClawHub 市场并推荐有用的 skills
- 🤖 安全地自动安装低风险 skills
- 📊 生成详细的管理报告

---

## 🚀 快速开始

### 1. 安装

```bash
# Skill 已经在你的 workspace 中
cd ~/.openclaw/workspace/skills/skills-auto-manager
```

### 2. 配置

编辑 `config.json` 文件，自定义你的设置：

```json
{
  "settings": {
    "frequency": "weekly",           // 检查频率
    "auto_install_low_risk": true,    // 自动安装低风险 skills
    "max_recommendations": 10         // 最大推荐数量
  },
  "user_profile": {
    "focus_areas": [
      "quantitative-trading",
      "stock-analysis",
      "data-analysis"
    ]
  }
}
```

### 3. 启动自动化

```bash
# Cron job 已经配置完成
# 每周日晚上 20:00 自动执行

# 查看 cron 状态
openclaw cron list

# 手动触发一次检查
openclaw cron run auto-skills-market-checker
```

---

## 🎯 核心功能

### 1. 智能检查

- ✅ 检查已安装 skills 的更新状态
- ✅ 扫描需要修复或过期的 skills
- ✅ 生成健康报告

### 2. 市场浏览

- ✅ 自动搜索 ClawHub 市场
- ✅ 基于用户画像智能筛选
- ✅ 评分和排序推荐 skills

### 3. 安全自动安装

- ✅ 低风险 skills 自动安装
- ✅ 高风险 skills 请求确认
- ✅ 完整的安装日志

### 4. 报告生成

- ✅ 详细的检查报告
- ✅ 推荐技能列表
- ✅ 安装历史记录

---

## 🛡️ 安全机制

### 自动安装（低风险）
- ✅ 官方维护的 skills
- ✅ 零外部依赖
- ✅ 纯功能性工具
- ✅ 社区高评分

### 需要确认（高风险）
- ⚠️ 涉及资金的 skills
- ⚠️ 需要 API tokens
- ⚠️ experimental/beta 版本
- ⚠️ 涉及隐私数据

### 保护措施
- ✅ 安装前备份当前 skills
- ✅ 完整的安装日志
- ✅ 一键回滚功能
- ✅ 冲突检测和解决

---

## 📊 使用示例

### 示例 1: 手动触发检查

```
调用 skills-auto-manager
→ 执行完整检查流程
→ 生成报告到 memory/skills-auto-2026-04-21.md
→ 通知用户推荐结果
```

### 示例 2: 自定义筛选

编辑 `config.json`，添加你的关注领域：

```json
{
  "user_profile": {
    "focus_areas": [
      "machine-learning",
      "data-science",
      "visualization"
    ]
  }
}
```

然后重新执行检查。

### 示例 3: 查看历史报告

```bash
# 查看所有报告
ls memory/skills-auto-*.md

# 查看最新报告
cat memory/skills-auto-2026-04-21.md
```

---

## 📁 文件结构

```
skills-auto-manager/
├── SKILL.md              # 主 skill 文件
├── README.md             # 本文件
├── config.json           # 配置文件
├── implementation.md     # 实现指南
├── logs/                 # 日志目录
│   ├── install-*.log     # 安装日志
│   └── error-*.log       # 错误日志
└── reports/              # 报告目录（自动生成到 memory/）
```

---

## 🔧 配置选项

### 执行频率

| 频率 | Cron 表达式 | 说明 |
|------|-----------|------|
| 每周 | `0 20 * * 0` | 每周日晚上 20:00 |
| 每两周 | `0 20 * * 0/2` | 每两周的周日晚上 20:00 |
| 每月 | `0 20 1 * *` | 每月 1 号晚上 20:00 |

### 筛选优先级

| 领域 | 优先级 | 说明 |
|------|--------|------|
| quantitative-trading | 5 | 量化交易 |
| stock-analysis | 5 | 股票分析 |
| data-analysis | 4 | 数据分析 |
| automation | 4 | 自动化 |
| general | 2 | 通用工具 |

### 安装策略

| 策略 | low_risk | high_risk | 说明 |
|------|----------|-----------|------|
| 保守 | false | false | 全手动确认 |
| 平衡 | true | false | 低风险自动（默认） |
| 激进 | true | true | 大部分自动 |

---

## 🐛 故障排除

### 检查失败

**问题**: `openclaw skills check` 失败

**解决方案**:
```bash
# 确认网络连接
ping clawhub.ai

# 检查 openclaw CLI
openclaw --version

# 查看日志
cat logs/error-*.log
```

### 安装失败

**问题**: skill 安装失败

**解决方案**:
```bash
# 检查权限
ls -la ~/.openclaw/skills/

# 查看 disk space
df -h

# 查看安装日志
cat logs/install-*.log
```

### Cron 不执行

**问题**: cron job 没有运行

**解决方案**:
```bash
# 确认 Gateway daemon 运行中
openclaw gateway status

# 检查 cron 状态
openclaw cron list

# 查看 Gateway 日志
openclaw gateway logs
```

---

## 📈 版本历史

### v1.0.0 (2026-04-21)
- ✅ 初始版本
- ✅ 完整的自动检查功能
- ✅ ClawHub 集成
- ✅ 安全安装机制
- ✅ 报告生成
- ✅ Cron job 自动化

---

## 🤝 贡献

如果你发现 bug 或有新功能建议，请：

1. 提交 issue
2. 描述问题或功能需求
3. 等待维护者回复

---

## 📄 许可证

MIT License

---

## 📞 支持

- 📧 Email: support@openclaw.ai
- 💬 Discord: https://discord.com/invite/clawd
- 📖 Docs: https://docs.openclaw.ai

---

**Made with ❤️ by OpenClaw Community**
