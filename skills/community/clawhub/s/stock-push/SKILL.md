---
name: stock-push
description: A股股票定时推送系统。管理盘前推荐（09:20）、收盘复盘（15:05）、次日关注（20:00）三个推送任务，每交易日晚自动发送持仓股行情到微信。当用户提到：股票推送、持仓监控、定时提醒、A股行情，或者需要查询持仓盈亏、复盘信息、次日建议时触发。also triggers when user says "推送" or "股票" or asks to check their holdings.
---

# Stock Push — A股持仓定时推送

## 系统架构

```
东方财富 API  →  Python 脚本  →  openclaw message send  →  微信
（数据源）        （处理逻辑）          （Gateway转发）
```

**关键约束：**
- 不依赖 Gateway 会话/cron run，完全系统 cron 独立运行
- 发送走 `openclaw message send`（非 direct ilink API）
- 数据源：东方财富 `push2.eastmoney.com`

## 三推送任务

| 脚本 | cron | 触发 | 功能 |
|------|------|------|------|
| `stock_pre.py` | `20 9 * * 1-5` | 09:20 | 大盘指数 + 自选股 |
| `stock_after.py` | `5 15 * * 1-5` | 15:05 | 持仓收盘行情 + 统计 |
| `stock_next.py` | `0 20 * * 1-4` | 20:00 | 收盘概况 + 明日建议 |

## 数据源

**东方财富行情 API：**
```
GET https://push2.eastmoney.com/api/qt/stock/get
  ?secid=<market>.<code>
    &fields=f43,f44,f47,f57,f58,f60
    &ut=bd1d9ddb04089700cf9c27f4f4961f5b&fltt=2&invt=2
```

**secid：** `1.沪股代码`（如 `1.600490`） / `0.深股代码`（如 `0.300269`）

**已验证字段：**

| 字段 | 含义 | 特殊情况 |
|------|------|---------|
| `f43` | 最新价（收盘/当前） | — |
| `f44` | 昨收价 | 竞价阶段返回 `'-'`，自动改用 f60 |
| `f47` | 成交量（手） | 竞价阶段可能返回 `'-'` |
| `f57` | 股票代码 | — |
| `f58` | 股票名称 | — |
| `f60` | 备用昨收 | f44='-' 时自动使用 |

**涨跌幅计算：** `(f43 - f44) / f44 × 100`

⚠️ **不要用 `f3` 字段**（非交易时段返回0，不可靠）

## 发送方式

```bash
openclaw message send \
  --channel openclaw-weixin \
  --target YOUR_WECHAT_USER_ID \
  --message "<text>"
```

## 可靠性机制

- **有效数据校验**：`price ≤ 0 or yclose ≤ 0` → `valid=False`，不参与统计
- **零数据跳过**：全部无效时不发送，避免假数据
- **发送重试**：失败最多3次，每次间隔3秒
- **异常隔离**：单只股票失败不影响其他
- **日志文件**：`/tmp/stock_pre.log` / `stock_after.log` / `stock_next.log`

## 持仓配置

持仓列表在脚本顶部 `HOLDINGS` / `WATCH_LIST` 列表中修改。

格式：`(secid, code, name)`

```
HOLDINGS = [
    ("1.600490", "600490", "鹏欣资源"),
    ("0.300269", "300269", "联建光电"),
    ("0.002138", "002138", "顺络电子"),
    ("0.300444", "300444", "双杰电气"),
]
```

## 手动测试

```bash
python3 /root/.openclaw/workspace/stock_pre.py
python3 /root/.openclaw/workspace/stock_after.py
python3 /root/.openclaw/workspace/stock_next.py

# 查看日志
tail -f /tmp/stock_pre.log
tail -f /tmp/stock_after.log
tail -f /tmp/stock_next.log
```

## 日志轮转

配置：`/etc/logrotate.d/stock-monitor`，保留7天。

## 详细文档

- **字段验证数据** → `references/field-verification.md`
- **推送历史/变更记录** → `references/history.md`
- **已知问题排查** → `references/troubleshooting.md`
