# Survival Manager 技能

[![ClawHub](https://img.shields.io/badge/ClawHub-survival--manager-blue)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://clawhub.com)

> 🌑 自主运行 + 人类授权的生存管理系统  
> Inspired by Automaton (Conway Research)

---

## 📋 功能特性

- **生存等级评估** - 根据余额自动调整运行模式（thriving/normal/lowCompute/critical）
- **心跳守护** - 定期检查网关/浏览器/技能/Fiverr/邮箱/日历状态
- **授权队列** - 高风险操作需用户授权，自动记录决策
- **财务追踪** - 收入/支出自动记录，成本估算
- **Agent 通信** - 子代理协调 + 优先级通知系统

---

## 🚀 安装

```bash
# 通过 ClawHub CLI 安装
clawhub install survival-manager

# 或手动安装
git clone https://github.com/openclaw_ceo/skills/survival-manager
# 复制到 OpenClaw skills 目录
```

---

## 📖 使用说明

### 检查生存状态

```bash
# PowerShell
.\scripts\check-survival.ps1
```

输出示例：
```
【生存状态】2026-03-01 05:30

等级：normal (→ thriving in ¥1000)
余额：¥0
今日收入：¥0 / 目标¥100 (0%)
今日支出：¥0 / 预算¥50 (0%)

下次检查：2026-03-01 06:30
```

### 记录收入

```powershell
.\scripts\log-income.ps1 -Amount 500 -Source "Fiverr Order #12345" -Channel "fiverr"
```

### 请求授权

```powershell
.\scripts\request-auth.ps1 `
  -Operation "file_write" `
  -Description "更新 Fiverr 服务页面" `
  -Cost 0.01 `
  -Priority "normal"
```

---

## ⚙️ 配置

### 生存等级配置

编辑 `survival-config.json`：

```json
{
  "survival": {
    "balance": 0,
    "currentTier": "normal",
    "tiers": {
      "thriving": { "minBalance": 5000, "model": "qwen3.5-397b", "heartbeatMinutes": 30, "maxSubagents": 8 },
      "normal": { "minBalance": 1000, "model": "qwen3.5-plus", "heartbeatMinutes": 60, "maxSubagents": 4 },
      "lowCompute": { "minBalance": 100, "model": "qwen3.5-flash", "heartbeatMinutes": 120, "maxSubagents": 2 },
      "critical": { "minBalance": 0, "model": "qwen3.5-flash", "heartbeatMinutes": 240, "maxSubagents": 1 }
    }
  }
}
```

### 心跳检查配置

编辑 `HEARTBEAT.md` 添加检查任务：

```markdown
## 🔄 心跳任务清单

### 每 30 分钟
- [ ] Fiverr 订单/消息检查

### 每小时
- [ ] 余额检查（生存等级评估）
- [ ] 邮箱检查（紧急未读）
- [ ] 日历检查（24h 内事件）
```

---

## 🔒 安全说明

### 自主执行操作（无需授权）
- ✅ 读取文件
- ✅ 网络搜索
- ✅ 浏览器快照
- ✅ 成本 < ¥10 的 API 调用

### 需授权操作
- ⚠️ 文件写入/删除
- ⚠️ 发送外部消息
- ⚠️ 创建子代理
- ⚠️ 配置修改

### 禁止操作（需明确命令）
- ❌ 支付/转账
- ❌ 删除系统文件
- ❌ 修改保护文件

---

## 📊 输出格式

### 生存状态报告

```
【生存状态】2026-03-01 05:30

等级：normal
余额：¥0
今日收入：¥0 / 目标¥100 (0%)
今日支出：¥0 / 预算¥50 (0%)
```

### 授权请求

```
【授权请求】AUTH-20260301-053000

操作：file_write
描述：更新 Fiverr 服务页面
成本：¥0.01
紧急：normal

请在 1 小时内回复：
- "批准" 执行
- "拒绝" 取消
- "修改：[内容]" 修改后执行
```

---

## 🎯 价值创造策略

### 短期 (7 天)
1. Fiverr 首单突破
2. 优化服务页面
3. 主动营销

### 中期 (30 天)
1. 建立 3+ 收入渠道
2. 自动化交付流程
3. 客户 CRM 系统

### 长期 (90 天)
1. 被动收入 > 主动收入
2. 多代理协作系统
3. 产品化服务

---

## 📝 更新日志

### v1.0.0 (2026-03-01)
- 初始发布
- 生存等级系统
- 心跳守护
- 授权队列
- 财务追踪
- Agent 通信

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🔗 链接

- [ClawHub](https://clawhub.com)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub Repo](https://github.com/openclaw_ceo/skills/survival-manager)
