---
name: workflow-automation-cn
version: 1.0.0
description: 自动化工作流生成器 - 用自然语言描述需求，自动生成 OpenClaw 心跳脚本。适合：想自动化日常任务的开发者。
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["python3", "node"]
---

# 自动化工作流生成器 Skill

用自然语言描述需求，自动生成可执行的自动化脚本。

## 支持的自动化类型

| 类型 | 示例 | 复杂度 |
|------|------|--------|
| 定时任务 | 每天发送日报 | ⭐ |
| 数据监控 | 价格变动提醒 | ⭐⭐ |
| 内容发布 | 自动发文章 | ⭐⭐ |
| API 调用 | 定时调用接口 | ⭐⭐ |
| 多步骤工作流 | 监控→分析→通知 | ⭐⭐⭐ |

## 使用方法

### 创建自动化

```
帮我创建一个自动化：每天早上 9 点检查 BTC 价格，如果涨跌超过 5% 就通知我
```

Agent 会：
1. 理解需求
2. 生成 Python 脚本
3. 配置心跳触发
4. 提供使用说明

### 修改自动化

```
把 BTC 价格监控改成每 4 小时检查一次
```

### 列出所有自动化

```
显示我所有的自动化任务
```

## 生成模板

### 定时通知脚本

```python
#!/usr/bin/env python3
"""
自动化：每日日报
触发：每天 09:00
"""
import requests
from datetime import datetime

def run():
    """执行自动化任务"""
    # 1. 收集数据
    today = datetime.now().strftime("%Y-%m-%d")

    # 2. 生成报告
    report = f"""
📊 每日报告 - {today}
━━━━━━━━━━━━━━
✅ 任务完成：X 个
❌ 任务失败：Y 个
💰 今日收益：¥Z
"""

    # 3. 发送通知
    send_notification(report)
    return True

def send_notification(message):
    """发送通知到 Telegram"""
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, data={
        "chat_id": chat_id,
        "text": message
    })

if __name__ == "__main__":
    run()
```

### 价格监控脚本

```python
#!/usr/bin/env python3
"""
自动化：价格监控
触发：每 10 分钟
"""
import requests
import json

# 配置
ALERT_THRESHOLD = 5.0  # 涨跌 5% 预警
LAST_PRICE_FILE = "/tmp/last_price.json"

def get_price():
    """获取当前价格"""
    resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    return float(resp.json()["price"])

def get_last_price():
    """获取上次价格"""
    try:
        with open(LAST_PRICE_FILE) as f:
            return json.load(f)["price"]
    except:
        return None

def save_price(price):
    """保存价格"""
    with open(LAST_PRICE_FILE, "w") as f:
        json.dump({"price": price}, f)

def check_alert(current, last):
    """检查是否需要预警"""
    if last is None:
        return None
    change = (current - last) / last * 100
    if abs(change) >= ALERT_THRESHOLD:
        return change
    return None

def run():
    current = get_price()
    last = get_last_price()
    alert = check_alert(current, last)

    if alert:
        direction = "📈 上涨" if alert > 0 else "📉 下跌"
        message = f"""
⚠️ BTC 价格预警
━━━━━━━━━━━━━━
{direction} {abs(alert):.2f}%
当前价格：${current:,.2f}
"""
        send_notification(message)

    save_price(current)
    return True

if __name__ == "__main__":
    run()
```

### 内容发布脚本

```python
#!/usr/bin/env python3
"""
自动化：内容发布
触发：每天 08:00
"""
import os
import glob
from datetime import datetime

CONTENT_DIR = os.path.expanduser("~/.openclaw/workspace/memory/content-queue")
PUBLISHED_DIR = os.path.join(CONTENT_DIR, "published")

def get_pending_content():
    """获取待发布内容"""
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    return [f for f in files if "published" not in f]

def publish_content(filepath):
    """发布内容到平台"""
    # 读取内容
    with open(filepath) as f:
        content = f.read()

    # 调用发布 API（示例）
    # result = publish_to_juejin(content)

    # 移动到已发布目录
    os.makedirs(PUBLISHED_DIR, exist_ok=True)
    new_path = os.path.join(PUBLISHED_DIR, os.path.basename(filepath))
    os.rename(filepath, new_path)

    return True

def run():
    pending = get_pending_content()
    if not pending:
        print("没有待发布内容")
        return False

    # 发布第一篇
    published = publish_content(pending[0])
    if published:
        print(f"已发布：{os.path.basename(pending[0])}")
        send_notification(f"✅ 已发布文章：{os.path.basename(pending[0])}")

    return True

if __name__ == "__main__":
    run()
```

### API 调用脚本

```python
#!/usr/bin/env python3
"""
自动化：API 定时调用
触发：每 4 小时
"""
import requests
import json

API_URL = "https://api.example.com/endpoint"
RESULT_FILE = "/tmp/api_result.json"

def call_api():
    """调用 API"""
    resp = requests.get(API_URL, timeout=30)
    return resp.json()

def process_result(data):
    """处理结果"""
    # 自定义处理逻辑
    return data

def save_result(data):
    """保存结果"""
    with open(RESULT_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run():
    data = call_api()
    processed = process_result(data)
    save_result(processed)
    return True

if __name__ == "__main__":
    run()
```

## 心跳配置

### HEARTBEAT.md 示例

```markdown
# 心跳触发规则

## 定时任务
- 09:00 → 日报发送
- */4h → API 调用
- */10m → 价格监控

## 脚本路径
- 日报：~/.openclaw/workspace/custom/daily_report.py
- 监控：~/.openclaw/workspace/custom/price_monitor.py
- 发布：~/.openclaw/workspace/custom/auto_publish.py
```

## 快速命令

### 测试脚本

```bash
python3 ~/.openclaw/workspace/custom/your_script.py
```

### 添加到心跳

```bash
# 编辑心跳配置
vim ~/.openclaw/workspace/HEARTBEAT.md
```

### 查看日志

```bash
tail -f ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

## 注意事项

- 脚本需要可执行权限：`chmod +x script.py`
- 敏感信息使用环境变量
- 添加错误处理和日志
- 测试后再部署到心跳

---

创建：2026-03-12
版本：1.0