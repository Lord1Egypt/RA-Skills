---
name: stock-price-alert
description: 股价异动实时提醒，支持行情接口、邮件和Sonos语音播报
author: OpenClaw User
license: LICENSE-CC-BY-NC-SA 4.0 in LICENSE.txt
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "jq"] },
        "install":
          [
            {
              "id": "jq",
              "kind": "apt",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (apt)",
            },
          ],
      },
  }
---

# Stock Price Alert

监控股票持仓价格异动，当涨跌幅、成交量或价格突破阈值时，通过邮件和/或 Sonos 语音播报发出实时提醒。

## 使用场景

- 持仓股票涨跌幅超过设定阈值时需要即时通知
- 关键价格位突破（支撑/阻力）时需要提醒
- 需要语音播报以便不在屏幕前时也能获知异动
- 定时轮询行情并按规则触发告警

## 前置条件

- `curl`、`jq` 已安装
- 行情 API Key（默认支持 Alpha Vantage 免费接口，可替换为其他数据源）
- 邮件提醒需配置 SMTP 环境变量：`SMTP_HOST`、`SMTP_PORT`、SMTP_USER`、`SMTP_PASS`、`ALERT_EMAIL_TO`
- Sonos 播报需本地网络有 Sonos 设备且 `sonos` CLI 可用

## 配置

在 `scripts/config.json` 中设定持仓和规则：

```json
{
  "watchlist": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "alert_pct": 3.0,
      "alert_price_above": null,
      "alert_price_below": 170.0
    }
  ],
  "poll_interval_sec": 300,
  "notify": {
    "email": true,
    "sonos": true,
    "sonos_speaker": "Kitchen"
  },
  "api": {
    "provider": "alphavantage",
    "apikey_env": "ALPHAVANTAGE_API_KEY"
  }
}
```

| 字段 | 说明 |
|------|------|
| `watchlist[].alert_pct` | 涨跌幅超此值触发（百分比，如 3.0 表示 ±3%） |
| `watchlist[].alert_price_above` | 价格上穿此值触发（null 不启用） |
| `watchlist[].alert_price_below` | 价格下穿此值触发（null 不启用） |
| `poll_interval_sec` | 轮询间隔秒数 |
| `notify.email` | 是否启用邮件提醒 |
| `notify.sonos` | 是否启用 Sonos 语音播报 |
| `notify.sonos_speaker` | Sonos 设备名称 |

## 工作流

1. **读取配置** — 加载 `config.json`，获取持仓列表和告警规则
2. **拉取行情** — 调用行情接口获取最新报价和前日收盘价
3. **计算异动** — 对比涨跌幅、价格突破阈值
4. **触发提醒** — 命中规则时执行邮件和/或 Sonos 播报
5. **循环轮询** — 按 `poll_interval_sec` 间隔持续监控

## 运行

```bash
# 单次检查
bash scripts/stock_alert.sh --once

# 持续轮询
bash scripts/stock_alert.sh

# 指定自定义配置
bash scripts/stock_alert.sh --config /path/to/config.json
```

## 输出格式

标准输出打印检查结果，告警信息同时发送到配置的通知渠道：

```
[2026-05-12 08:00:01] AAPL $182.50 +4.2% ⚠️ 涨幅超阈值(3.0%)
[2026-05-12 08:00:01] → 邮件已发送至 user@example.com
[2026-05-12 08:00:01] → Sonos 播报: Kitchen
```

## 邮件提醒

脚本使用 `curl` 调用 SMTP 发送邮件，需配置环境变量：

| 变量 | 说明 |
|------|------|
| `SMTP_HOST` | SMTP 服务器地址 |
| `SMTP_PORT` | SMTP 端口（如 587） |
| `SMTP_USER` | 发件邮箱 |
| `SMTP_PASS` | 邮箱密码/应用专用密码 |
| `ALERT_EMAIL_TO` | 收件邮箱 |

## Sonos 语音播报

依赖 `sonos` CLI（参见 sonoscli 技能），播报内容示例：

> "AAPL 当前价格 182.50 美元，涨幅 4.2%，超过阈值 3%"

## 错误处理

| 错误 | 处理 |
|------|------|
| API 限流 (429) | 等待后重试，最多 3 次 |
| API Key 缺失 | 打印警告并跳过行情拉取 |
| SMTP 连接失败 | 降级为仅控制台输出 |
| Sonos 设备不可达 | 降级为仅控制台输出，不阻断其他通知 |

## 注意事项

- Alpha Vantage 免费版限 25 次/天，建议 `poll_interval_sec` 不低于 300
- 可替换 `api.provider` 为其他数据源，只需修改 `fetch_quote` 函数
- 邮件发送也可替换为 SendGrid/Mailgun 等 HTTP API
