# Solana Monitor - OpenClaw 技能

**版本：** v0.1.0  
**状态：** 开发中  
**作者：** VIC ai-company

---

## 📋 技能说明

实时监控 Solana 生态数据，包括：

- 📊 代币价格（CoinGecko API）
- 🔔 价格警报（Telegram/邮件）
- 🐋 大额转账追踪
- 💧 流动性池监控
- 🆕 新代币发现

---

## 🎯 使用场景

### DeFi 交易者
- 设置价格警报，不错过买卖点
- 监控巨鲸动向，跟随聪明钱
- 追踪流动性变化，避免 Rug Pull

### NFT 交易者
- 监控地板价变化
- 追踪大额 NFT 交易
- 发现新上线项目

### 项目方
- 监控竞争对手数据
- 追踪代币持有者分布
- 市场情绪分析

---

## 📦 安装

```bash
# 在 OpenClaw 中
openclaw skills install solana-monitor
```

或手动安装：

```bash
cd /workspace/skills/solana-monitor
pip install -r requirements.txt
```

---

## 🔧 配置

创建配置文件 `config/config.yaml`：

```yaml
# 监控设置
monitoring:
  check_interval: 60  # 检查间隔（秒）
  price_delay: 5      # 价格延迟（秒）

# 警报设置
alerts:
  enabled: true
  channels:
    - telegram
    - email

# Telegram 配置
telegram:
  bot_token: YOUR_BOT_TOKEN
  chat_id: YOUR_CHAT_ID

# Email 配置
email:
  smtp_server: smtp.gmail.com
  smtp_port: 587
  sender_email: your@gmail.com
  sender_password: YOUR_APP_PASSWORD
```

---

## 💻 使用示例

### Python 调用

```python
from scripts.price_monitor import PriceMonitor
from scripts.notifier import NotificationManager

# 初始化
monitor = PriceMonitor()
notifier = NotificationManager()

# 获取价格
sol_price = monitor.get_sol_price()
print(f"SOL: ${sol_price:.2f}")

# 设置警报
monitor.check_price_alert('solana', 90.0, 'above')
```

### 命令行

```bash
# 运行监控
python scripts/price_monitor.py

# 测试通知
python scripts/notifier.py
```

---

## 📊 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费 | $0 | 3 代币 + 5 警报 |
| 基础版 | $19/月 | 20 代币 + 20 警报 |
| 专业版 | $49/月 | 无限 + API |
| 企业版 | $199/月 | 定制 + SLA |

---

## 🚧 开发路线图

- [x] 价格监控模块
- [x] 通知系统
- [ ] 大额转账监控
- [ ] 流动性监控
- [ ] Web 仪表板
- [ ] API 开放

---

**最后更新：** 2026-03-01  
**状态：** 开发中（MVP 阶段）
