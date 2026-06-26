# 🕷️ Solana Monitor

**实时监控 Solana 生态数据，追踪价格、巨鲸、流动性变化**

---

## ✨ 功能特点

- 📊 **实时价格监控** - 支持 SOL 及所有 SPL 代币
- 🔔 **价格警报** - Telegram/邮件即时通知
- 🐋 **巨鲸追踪** - 大额转账实时监控
- 💧 **流动性监控** - DEX 流动性池变化警报
- 🆕 **新代币发现** - 自动发现新上线代币
- ⚠️ **风险评估** - 智能识别高风险代币

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/vic-ai-company/solana-monitor.git
cd solana-monitor

# 安装依赖
pip install -r requirements.txt
```

### 配置

创建 `.env` 文件：

```bash
# Telegram 配置（可选）
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Email 配置（可选）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your@gmail.com
SENDER_PASSWORD=your_app_password
```

### 使用

```python
from scripts.price_monitor import PriceMonitor, PriceAlert

# 创建监控器
monitor = PriceMonitor()

# 获取 SOL 价格
sol_price = monitor.get_sol_price()
print(f"SOL 价格：${sol_price:.2f}")

# 设置价格警报
alert_manager = PriceAlert()
alert_manager.add_alert('solana', 90.0, 'above')  # SOL 涨到 $90 警报
alert_manager.add_alert('solana', 80.0, 'below')  # SOL 跌到 $80 警报

# 检查警报
triggered = alert_manager.check_all_alerts(monitor)
```

---

## 📋 命令行使用

### 价格查询

```bash
# 查询 SOL 价格
python scripts/price_monitor.py

# 查询多个代币
python scripts/price_monitor.py --tokens solana,bitcoin,ethereum
```

### 设置警报

```bash
# 设置价格警报
python scripts/alert_manager.py add --token solana --price 90 --condition above

# 列出所有警报
python scripts/alert_manager.py list

# 删除警报
python scripts/alert_manager.py remove --id 1
```

---

## 💰 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| **免费** | $0 | 3 代币 + 5 警报 + Telegram |
| **基础版** | $19/月 | 20 代币 + 20 警报 + 邮件 + 大额监控 |
| **专业版** | $49/月 | 无限 + 流动性监控 + API + Webhook |
| **企业版** | $199/月 | 定制 + SLA + 专属节点 |

---

## 🔧 API 使用

### 获取价格

```bash
curl http://localhost:8000/api/v1/price/solana
```

### 设置警报

```bash
curl -X POST http://localhost:8000/api/v1/alert \
  -H "Content-Type: application/json" \
  -d '{
    "token": "solana",
    "target_price": 90,
    "condition": "above"
  }'
```

---

## 📊 示例输出

```
🔍 Solana Monitor - 价格监控测试
==================================================

📊 获取 SOL 当前价格...
✅ SOL 价格：$87.62 USD

📊 获取多个代币价格...
  SOL: $87.62 (+7.27%)
  BTC: $61,234.50 (+2.15%)
  ETH: $3,456.78 (+3.42%)

🔔 测试价格警报...
✅ 警报已添加：1
   代币：solana
   条件：above $91.99
✅ 警报已添加：2
   代币：solana
   条件：below $83.24

📋 当前警报列表:
  [1] solana above $91.99
  [2] solana below $83.24

==================================================
✅ 测试完成！
```

---

## 🛡️ 安全说明

- ✅ 只读取公开数据
- ✅ 不存储用户私钥
- ✅ 所有 API 调用加密
- ⚠️ 不构成投资建议

---

## 📞 技术支持

- GitHub Issues: https://github.com/vic-ai-company/solana-monitor/issues
- Telegram: @Vicaiceo_bot
- Email: support@vic-ai-company.com

---

## 📄 许可

MIT License - 详见 LICENSE 文件

---

**开发者：** VIC ai-company  
**版本：** v0.1.0  
**更新时间：** 2026-03-01
