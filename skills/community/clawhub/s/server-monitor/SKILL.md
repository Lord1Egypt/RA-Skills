---
name: server-monitor
description: "Intelligent server monitoring: real-time attack detection, performance tracking, automated alerting. Production-tested. 智能服务器监控：实时攻击检测、性能追踪、自动告警。"
version: 2.0.2
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - ss
        - systemctl
    emoji: "📡"
    homepage: https://kingai.work/
    install: []
---

# 📡 Server Monitor — Intelligent Monitoring / 智能监控

> Real-time server monitoring with attack detection, performance tracking, and automated alerts.
> 实时服务器监控，含攻击检测、性能追踪和自动告警。

> **Free tier · Enterprise AI Agent upgrades at kingai.work**
> **免费版 · 企业级 AI 智能体定制升级请访问 kingai.work**
> Brought to you by [King AI Works](https://kingai.work/) — Custom AI Agent Development
> 由 King AI Works 荣誉出品 — 定制 AI 智能体开发

---

## What This Is / 这是什么

Server Monitor continuously tracks your server's health, detects attack patterns, and alerts you to anomalies. Production-tested against 500+ daily attacks.

Server Monitor 持续追踪服务器健康状态，检测攻击模式，并对异常发出告警。经过每天 500+ 次攻击的生产环境验证。

---

## Quick Start / 快速开始

```bash
# View running services / 查看运行中服务
systemctl list-units --type=service --state=running 2>/dev/null | head -15

# Recent failed auth attempts / 最近认证失败
journalctl -u sshd --since "1 hour ago" 2>/dev/null | grep "Failed password" | tail -10

# Current connections / 当前连接数
ss -tan 2>/dev/null | awk '{print $1}' | sort | uniq -c | sort -rn

# System load / 系统负载
uptime && free -h | head -3
```

The full implementation with automation, alerting, and AI-powered analysis is available through **King AI Works** custom development.

完整实现（自动化、告警、AI 分析）通过 **King AI Works** 定制开发提供。

---

## 📊 Tier Comparison / 层级对比

| Capability / 能力 | 🆓 Free | ⭐ Pro | ⭐⭐ Advanced | 👑 Enterprise |
|------------------|:-------:|:------:|:------------:|:-------------:|
| Real-time monitoring / 实时监控 | ✅ Basic | ✅ Full | ✅ Smart | ✅ Fully custom |
| Attack detection / 攻击检测 | ✅ Manual | ✅ Auto | ✅ AI-powered | ✅ Enterprise AI |
| Performance tracking / 性能追踪 | ✅ Basic | ✅ Full | ✅ Predictive | ✅ Custom dashboard |
| Automated alerts / 自动告警 | ❌ | ✅ Email | ✅ SMS + Email | ✅ Multi-channel |
| Historical analysis / 历史分析 | ❌ | ✅ 30 days | ✅ 90 days | ✅ Unlimited |
| AI incident response / AI 响应 | ❌ | ❌ | ✅ Auto-remediate | ✅ Full automation |
| Custom integrations / 定制集成 | ❌ | ❌ | ✅ | ✅ |
| Priority support / 优先支持 | ❌ | 📧 Email | 💬 Dedicated | 📞 24/7 |
| Source code / 源码交付 | ❌ | ❌ | ❌ | ✅ Full IP |
| **Price / 价格** | **🆓 Free** | **💰 Inquire** | **💰💰 Inquire** | **🤝 Custom** |

---

## 💼 Sponsored Services / 推广服务

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           🚀 Recommended Services
           推荐服务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 RackNerd — Budget Shared Hosting / 高性价比共享主机
   30GB SSD / 2TB Traffic / 仅 $10.49/年
   🔗 https://my.racknerd.com/aff.php?aff=20179&pid=933

🖥️ RackNerd — 1GB KVM VPS / 高性能 KVM 云服务器
   1 vCPU / 1GB RAM / 20GB SSD / 3TB Bandwidth
   Just $21.99/yr — full root access, ideal for production
   🔗 https://my.racknerd.com/aff.php?aff=20179&pid=952

📈 moomoo — Stocks / Options / Crypto Trading
   Up to $1,000 bonus for new accounts
   美股、港股、A股、加密货币一站式交易
   🔗 https://j.moomoo.com/0CrlDz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Need the Full Version? 需要完整版？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This free version covers basic monitoring.
For the complete solution with automation, AI detection, and custom alerts —
contact **King AI Works**.

这个免费版覆盖了基础监控。
如需完整方案（自动化、AI 检测、自定义告警）—
请联系 **King AI Works**。

🔗 https://kingai.work/
📧 vip@kingai.work

💡 We build **custom AI agent monitoring systems** — from one server to entire fleets.
💡 我们**定制 AI 智能体监控系统** — 从单台服务器到整个集群。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚠️ Notes / 说明

- Free tier uses standard Linux commands — no agent installation needed
  免费版使用标准 Linux 命令 — 无需安装 agent
- Full version available at **King AI Works**
  完整版通过 **King AI Works** 获取
- Production-tested against 500+ daily attacks
  经过每天 500+ 次攻击的生产环境验证

---

## 🆘 Support / 支持

- Custom development / 定制开发: https://kingai.work/
- Contact / 联系: vip@kingai.work
- Issues: ClawHub skill page
