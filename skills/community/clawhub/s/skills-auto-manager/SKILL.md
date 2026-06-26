---
name: skills-auto-manager
description: '自动管理 OpenClaw skills 的智能助手：定期检查更新、浏览 ClawHub 市场、智能推荐并安全安装有用的 skills'
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": {},
        "tags": ["skills", "automation", "clawhub", "quantitative-trading"]
      },
  }
---

# Skills Auto Manager

自动管理 OpenClaw skills 的智能助手：
- 定期检查 skills 更新
- 浏览 ClawHub 市场
- 筛选并推荐有用的 skills
- 安全自动安装低风险 skills

---

## 功能特性

### 🔍 智能检查
- 检查已安装 skills 的更新状态
- 扫描需要修复或过期的 skills
- 生成健康报告

### 🛒 市场浏览
- 自动搜索 ClawHub 市场
- 基于用户画像智能筛选
- 评分和排序推荐 skills

### 🤖 自动安装（安全）
- 低风险 skills 自动安装
- 高风险 skills 请求确认
- 完整的安装日志

---

## 使用方法

### 1. 手动触发检查

```
执行完整检查流程：
- 检查当前 skills 状态
- 浏览市场推荐
- 生成报告
- 请求确认安装
```

### 2. 设置自动化

```
配置自动检查任务：
- 每周/每两周自动执行
- 自动通知你推荐结果
- 自动处理低风险 skills
```

### 3. 筛选配置

```
基于你的使用场景定制：
- 量化交易相关
- 数据分析工具
- 自动化脚本
- 其他特定领域
```

---

## 安全机制

### ✅ 自动安装（低风险）
- 官方维护的 skills
- 零外部依赖
- 纯功能性工具
- 社区高评分

### ⚠️ 需要确认（高风险）
- 涉及资金的 skills
- 需要 API tokens
- experimental/beta 版本
- 涉及隐私数据

### 🛡️ 保护措施
- 安装前备份当前 skills
- 完整的安装日志
- 一键回滚功能
- 冲突检测和解决

---

## 输出报告

检查完成后会生成详细报告：

```
# Skills Auto Manager Report

## 🔍 当前状态
- 已安装: X个
- 有更新: Y个
- 需修复: Z个

## 📦 推荐安装 (Top 10)
1. [skill-name] - ⭐⭐⭐⭐⭐
   - 分类: XXX
   - 理由: XXX
   - 风险: 低/中/高

## ✅ 已自动安装
- skill-1
- skill-2

## ⚠️ 等待确认
- skill-3 (高风险)
```

---

## 配置选项

### 执行频率
- 每周日 (默认)
- 每两周
- 每月
- 手动触发

### 筛选优先级
- 股票/量化相关
- 数据分析
- 自动化
- 通用工具

### 安装策略
- 保守 (全手动确认)
- 平衡 (低风险自动)
- 激进 (大部分自动)

---

## 技术细节

### Cron Job 配置
- 自动化任务通过 OpenClaw cron 管理
- Isolated session 执行
- 结果通知到当前会话

### 数据存储
- 报告保存到: `memory/skills-auto-YYYY-MM-DD.md`
- 配置保存到: `skills-auto-manager-config.json`
- 历史记录可追溯

### 依赖工具
- `openclaw` CLI
- ClawHub API (web_fetch)
- 本地文件系统 (read/write)

---

## 故障排除

### 检查失败
- 确认网络连接
- 检查 `openclaw` CLI 是否可用
- 查看日志文件

### 安装失败
- 检查权限
- 确认 disk space
- 查看冲突检测日志

### Cron 不执行
- 确认 Gateway daemon 运行中
- 检查 cron 状态: `openclaw cron list`
- 查看 Gateway 日志

---

## 维护建议

### 定期检查
- 每周自动检查 (默认)
- 手动触发: 随时运行

### 备份策略
- 每次安装前自动备份
- 保留最近 3 次备份
- 可配置保留策略

### 清理优化
- 定期清理旧报告
- 移除未使用的 skills
- 优化存储空间

---

## 版本信息

- **Version**: 1.0.0
- **Created**: 2026-04-21
- **Maintainer**: Auto-generated skill
- **Dependencies**: OpenClaw CLI, ClawHub

---

## 更新日志

### v1.0.0 (2026-04-21)
- 初始版本
- 完整的自动检查功能
- ClawHub 集成
- 安全安装机制
- 报告生成
