---
name: tqsdk-read
description: 天勤量化 - 期货实时行情与历史数据接口，提供国内期货、期权的实时报价、K线序列与历史数据查询。
version: 1.0.0
author: 真圆氦狗
homepage: https://www.shinnytech.com/tqsdk/
runtime: python3
entrypoint: __init__.py:handler
parameters:
  - name: action
    type: string
    required: true
    enum:
      - get_quote
      - get_kline_serial
      - get_kline_data
    description: 要执行的操作类型
  - name: symbol
    type: string
    required: true
    description: 合约代码，格式如 "SHFE.rb2410"。多合约用逗号分隔，如 "SHFE.rb2410,DCE.m2409"
  - name: duration_seconds
    type: integer
    required: false
    default: 60
    description: K线周期（秒），仅用于 get_kline_serial 或 get_kline_data
  - name: data_length
    type: integer
    required: false
    default: 200
    description: K线序列长度，仅用于 get_kline_serial
  - name: start_dt
    type: string
    required: false
    description: 历史数据起始时间（ISO 8601），仅用于 get_kline_data
  - name: end_dt
    type: string
    required: false
    description: 历史数据结束时间（ISO 8601），仅用于 get_kline_data
---

# 天勤量化技能

该技能提供天勤量化接口的访问，支持获取期货实时行情、K线序列及历史数据。

## 使用示例
/tqsdk-read get_quote SHFE.rb2410
/tqsdk-read get_kline_serial SHFE.rb2410 --duration_seconds 300 --data_length 50
/tqsdk-read get_kline_data SHFE.rb2410 --duration_seconds 3600 --start_dt 2024-01-01T09:00:00 --end_dt 2024-01-31T15:00:00


## 环境变量配置

本技能通过环境变量读取天勤账号，请在使用前设置：

- `TQ_USERNAME`：天勤用户名（注册于官网）
- `TQ_PASSWORD`：天勤密码

在 ClawHub 中，可在技能设置页面或通过环境变量文件配置。

## 注意事项

- 历史K线查询（`get_kline_data`）需要天勤**专业版账号**权限。
- 实时行情和K线序列（`get_quote`, `get_kline_serial`）基础版账号即可使用。
- 合约代码格式：交易所.合约代码，如 `SHFE.rb2410`、`DCE.m2409`、`CFFEX.IF2406`。
- 多合约操作时，`symbol` 参数用逗号分隔（仅支持 `get_quote` 和 `get_kline_serial`）。
- K线周期常用值：60（1分钟）、300（5分钟）、900（15分钟）、3600（1小时）、86400（日线）。

## 常见问题

**Q: 提示“天勤认证失败”怎么办？**  
A: 请检查环境变量 `TQ_USERNAME` 和 `TQ_PASSWORD` 是否正确，并确保账户已激活。

**Q: 历史K线接口报错？**  
A: 确认您拥有天勤专业版账号，且时间范围有效（K线数量不超过限制）。