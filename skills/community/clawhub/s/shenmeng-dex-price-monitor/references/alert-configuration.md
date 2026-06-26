# 预警配置指南

## 预警类型

### 1. 价格阈值预警

**目标价突破**：
```python
alert_config = {
    'type': 'price_threshold',
    'token': 'ETH/USDC',
    'condition': 'above',  # above / below
    'price': 4000,
    'message': 'ETH突破$4000！'
}
```

**使用场景**：
- 达到目标买入价
- 达到目标卖出价
- 突破关键支撑/阻力位

### 2. 价差预警

**DEX价差**：
```python
alert_config = {
    'type': 'spread_threshold',
    'token': 'ETH/USDC',
    'dex1': 'Uniswap V3',
    'dex2': 'SushiSwap',
    'threshold': 0.8,  # 0.8%
    'message': '发现套利机会！'
}
```

**使用场景**：
- 搬砖套利
- 发现定价错误
- 流动性异常

### 3. 波动率预警

**价格剧烈波动**：
```python
alert_config = {
    'type': 'volatility',
    'token': 'ETH/USDC',
    'timeframe': '1h',  # 1h / 24h
    'threshold': 5,  # 5%
    'message': 'ETH剧烈波动！'
}
```

**使用场景**：
- 市场异常
- 重大新闻
- 风险提示

### 4. 异常检测预警

**价格偏离**：
```python
alert_config = {
    'type': 'anomaly',
    'token': 'ETH/USDC',
    'baseline': 'median',  # median / mean / vwap
    'deviation': 3,  # 3%
    'message': 'ETH价格异常！'
}
```

**使用场景**：
- 数据源错误
- 合约被攻击
- 大额操纵

## 通知渠道配置

### Telegram

**创建Bot**：
1. 找 @BotFather
2. 发送 `/newbot`
3. 命名你的bot
4. 获取token

**获取Chat ID**：
```python
# 给bot发消息后访问
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
response = requests.get(url)
chat_id = response.json()['result'][0]['message']['chat']['id']
```

**发送消息**：
```python
import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    response = requests.post(url, json=payload)
    return response.json()

# 使用
token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
message = '''
🚨 *价格预警*

ETH突破 $4,000!
当前价格: $4,050
24h涨幅: +5.2%

[查看图表](https://dexscreener.com/ethereum/0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8)
'''
send_telegram_message(token, chat_id, message)
```

### Discord

**创建Webhook**：
1. 进入Discord服务器设置
2. 集成 → Webhook
3. 创建Webhook
4. 复制URL

**发送消息**：
```python
import requests

def send_discord_webhook(webhook_url, content, embeds=None):
    payload = {
        'content': content,
        'username': 'DEX Monitor',
        'avatar_url': 'https://example.com/icon.png'
    }
    if embeds:
        payload['embeds'] = embeds
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 204

# 使用
webhook_url = 'YOUR_WEBHOOK_URL'

embed = {
    'title': '价格预警',
    'description': 'ETH突破$4000',
    'color': 0x00ff00,
    'fields': [
        {'name': '当前价格', 'value': '$4,050', 'inline': True},
        {'name': '24h涨幅', 'value': '+5.2%', 'inline': True}
    ],
    'timestamp': datetime.utcnow().isoformat()
}

send_discord_webhook(webhook_url, '@everyone 价格预警！', [embed])
```

### 邮件通知

```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(smtp_server, port, username, password, to_email, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = to_email
    
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

# 使用
send_email_alert(
    'smtp.gmail.com',
    587,
    'your_email@gmail.com',
    'your_password',
    'alert@example.com',
    'DEX价格预警',
    '<h1>ETH突破$4000</h1><p>当前价格: $4,050</p>'
)
```

### Webhook

**通用Webhook**：
```python
import requests

def send_webhook(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response.status_code

# 使用
data = {
    'event': 'price_alert',
    'token': 'ETH/USDC',
    'price': 4050,
    'timestamp': datetime.utcnow().isoformat()
}
send_webhook('https://your-app.com/webhook', data)
```

## 预警级别

### 级别定义

```python
ALERT_LEVELS = {
    'info': {
        'color': '🟢',
        'notify': ['console', 'log'],
        'description': '一般信息'
    },
    'warning': {
        'color': '🟡',
        'notify': ['console', 'log', 'telegram'],
        'description': '需要注意'
    },
    'critical': {
        'color': '🔴',
        'notify': ['console', 'log', 'telegram', 'discord', 'email'],
        'description': '立即处理'
    }
}
```

### 使用示例

```python
def send_alert(level, message, data=None):
    config = ALERT_LEVELS[level]
    
    formatted_message = f"{config['color']} [{level.upper()}] {message}"
    
    # 控制台
    if 'console' in config['notify']:
        print(formatted_message)
    
    # Telegram
    if 'telegram' in config['notify']:
        send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, formatted_message)
    
    # Discord
    if 'discord' in config['notify']:
        send_discord_webhook(DISCORD_WEBHOOK, formatted_message)
    
    # 邮件
    if 'email' in config['notify']:
        send_email_alert(...)
    
    # 日志
    if 'log' in config['notify']:
        logger.log(getattr(logging, level), message)

# 使用
send_alert('warning', 'ETH价差超过0.5%', {'spread': 0.52})
send_alert('critical', 'ETH价格异常偏离！', {'deviation': 5.3})
```

## 预警去重

### 去重策略

```python
from datetime import datetime, timedelta

class AlertDeduplicator:
    def __init__(self, cooldown_minutes=5):
        self.recent_alerts = {}
        self.cooldown = timedelta(minutes=cooldown_minutes)
    
    def should_send(self, alert_key):
        """检查是否应该发送预警"""
        now = datetime.now()
        
        if alert_key in self.recent_alerts:
            last_sent = self.recent_alerts[alert_key]
            if now - last_sent < self.cooldown:
                return False
        
        self.recent_alerts[alert_key] = now
        return True
    
    def clean_old(self):
        """清理过期记录"""
        now = datetime.now()
        self.recent_alerts = {
            k: v for k, v in self.recent_alerts.items()
            if now - v < self.cooldown * 2
        }

# 使用
deduplicator = AlertDeduplicator(cooldown_minutes=10)

if deduplicator.should_send('ETH_above_4000'):
    send_alert('warning', 'ETH突破$4000')
```

## 配置文件示例

### YAML配置

```yaml
# config/alerts.yaml
alerts:
  - name: ETH价格预警
    type: price_threshold
    token: ETH/USDC
    condition: above
    price: 4000
    level: warning
    cooldown: 30  # 分钟
    notify:
      - telegram
      - discord
    
  - name: 套利机会
    type: spread_threshold
    token: ETH/USDC
    dex1: Uniswap V3
    dex2: SushiSwap
    threshold: 0.8
    level: info
    cooldown: 5
    notify:
      - telegram
    
  - name: 异常波动
    type: volatility
    token: ETH/USDC
    timeframe: 1h
    threshold: 5
    level: critical
    cooldown: 60
    notify:
      - telegram
      - discord
      - email

notifications:
  telegram:
    enabled: true
    bot_token: ${TELEGRAM_BOT_TOKEN}
    chat_id: ${TELEGRAM_CHAT_ID}
    
  discord:
    enabled: true
    webhook_url: ${DISCORD_WEBHOOK_URL}
    
  email:
    enabled: false
    smtp_server: smtp.gmail.com
    port: 587
    username: ${EMAIL_USERNAME}
    password: ${EMAIL_PASSWORD}
    to_email: alerts@example.com
```

### 加载配置

```python
import yaml
import os

def load_alert_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # 环境变量替换
    def replace_env_vars(obj):
        if isinstance(obj, dict):
            return {k: replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_env_vars(i) for i in obj]
        elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
            env_var = obj[2:-1]
            return os.getenv(env_var, obj)
        return obj
    
    return replace_env_vars(config)

# 使用
config = load_alert_config('config/alerts.yaml')
```

---

*好的预警配置能及时捕捉机会，同时避免信息过载。*
