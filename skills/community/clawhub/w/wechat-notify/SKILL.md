---
name: wechat-notify
description: >
  微信（WeChat Work / 企业微信）消息通知 Skill。
  通过企业微信群机器人的 Webhook 接口向微信群/微信用户发送消息通知。
  支持：文本消息、Markdown、卡片消息、图片。
  适用场景：定时报告、报警通知、交易信号推送、自动化工作流通知。
---

# WeChat Work 消息通知

> 通过企业微信 Webhook 向微信群/用户发送消息

## 支持功能

- ✅ 文本消息
- ✅ Markdown 消息（企业微信格式）
- ✅ 图文卡片消息
- ✅ 定时推送（结合 OpenClaw Cron）
- ✅ 多群/多用户推送

## 环境要求

- 企业微信账号（需开通「群机器人」功能）
- Python 3.10+
- `requests` 库（`pip install requests`）

## 快速安装

```bash
clawhub install wechat-notify
```

## 配置

### Step 1：获取 Webhook 地址

1. 打开企业微信 PC 版
2. 进入任意群聊 → 点击右上角「群机器人」→「添加机器人」
3. 复制生成的 Webhook URL，格式如：
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXXXXXXX-XX
   ```

### Step 2：配置环境变量

```bash
export WECHAT_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```

或在 `.env` 文件中：
```bash
WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY
```

## 使用方法

### Python API

```python
import sys
sys.path.insert(0, "/home/user/.openclaw/workspace")

from skills.wechat_notify import WeChatNotifier

# 初始化（默认使用 WECHAT_WEBHOOK_URL 环境变量）
notifier = WeChatNotifier()

# ─── 发送文本消息 ───────────────────────────
notifier.send_text("BTC 价格跌破 60000，建议关注！")

# ─── 发送 Markdown（企业微信格式）────────────
notifier.send_markdown("""
## 📊 交易信号报告

**BTC/USDT**: 买入信号
- RSI: 32（超卖）
- MACD: 金叉

> 时间：2026-03-25 17:30
""")

# ─── 发送图文卡片 ───────────────────────────
notifier.send_news(
    title="交易信号提醒",
    description="BTC 出现买入信号",
    url="https://www.binance.com",
    picurl="https://example.com/btc.png"
)

# ─── 多个 Webhook（多群推送）─────────────────
notifier2 = WeChatNotifier(
    webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YYY"
)
notifier2.send_text("通知到第二个群")
```

### 命令行

```bash
# 发送文本
python -m skills.wechat_notify --text "测试消息"

# 发送 Markdown
python -m skills.wechat_notify --markdown "**粗体** 和 _斜体_"

# 发送图文
python -m skills.wechat_notify --news "标题" "描述" "URL" "图片URL"
```

### 配合 Cron 定时推送

```python
from skills.wechat_notify import WeChatNotifier
from datetime import datetime

notifier = WeChatNotifier()

def send_daily_report():
    notifier.send_markdown(f"""
## 📅 每日报告 - {datetime.now().strftime('%Y-%m-%d')}
- 系统运行正常
- 策略收益：+2.3%
    """)

# 在 OpenClaw Cron 中设置定时任务
```

## 故障排除

| 问题 | 解决方法 |
|------|----------|
| `40014` 错误 | Webhook URL 不正确或已失效，重新获取 |
| `40003` 错误 | 指定的用户/群不存在，检查 key |
| 消息发送成功但群里看不到 | 检查企业微信版本是否支持群机器人 |
| `curl` 失败 | 确认网络能访问 `qyapi.weixin.qq.com` |

## 安全提示

- Webhook URL 不要提交到 Git（包含 key）
- 每个群的 Webhook 只在该群有效
- Webhook 可以@群里所有人

## Webhook 限制

- 每个 webhook 每分钟最多发送 20 条消息
- 消息内容大小限制：Markdown 不超过 2048 字节
- 建议结合 OpenClaw Cron 使用时，最小间隔 3 分钟以上
