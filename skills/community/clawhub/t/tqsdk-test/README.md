# 天勤量化 Skill

该 Skill 提供对天勤量化接口的访问，支持获取实时行情、实时K线序列和历史K线数据。

## 前置条件

- 在天勤官网注册账号并获取用户名/密码。
- 历史K线查询需要专业版账号权限。

## 安装

在 Clawdbot 中安装此 Skill 后，会自动安装依赖。

## 参数说明

| 参数名            | 类型    | 必填 | 说明                                                                 |
|-------------------|---------|------|----------------------------------------------------------------------|
| action            | string  | 是   | 操作类型：`get_quote`, `get_kline_serial`, `get_kline_data`          |
| symbol            | string  | 是   | 合约代码，多合约用逗号分隔，如 `SHFE.rb2410,DCE.m2409`               |
| username          | string  | 是   | 天勤用户名                                                           |
| password          | string  | 是   | 天勤密码                                                             |
| duration_seconds  | integer | 否   | K线周期（秒），默认 60。仅用于 K线相关操作                           |
| data_length       | integer | 否   | K线序列长度，默认 200。仅用于 `get_kline_serial`                     |
| start_dt          | string  | 否   | 起始时间（ISO 8601），如 `2024-01-01T09:00:00`。仅用于 `get_kline_data` |
| end_dt            | string  | 否   | 结束时间（ISO 8601）。仅用于 `get_kline_data`                        |

## 示例

### 获取螺纹钢实时行情

```json
{
  "action": "get_quote",
  "symbol": "SHFE.rb2410",
  "username": "your_username",
  "password": "your_password"
}
返回结果：

json
{
  "result": [
    {
      "symbol": "SHFE.rb2410",
      "last_price": 3825.0,
      "ask_price1": 3826.0,
      "bid_price1": 3824.0,
      "volume": 123456,
      "open_interest": 789012,
      "datetime": "2025-04-15 14:30:00"
    }
  ]
}
获取5分钟K线序列（最近200根）
json
{
  "action": "get_kline_serial",
  "symbol": "SHFE.rb2410",
  "duration_seconds": 300,
  "data_length": 200,
  "username": "your_username",
  "password": "your_password"
}
返回结果包含最新一根K线的完整信息。

获取历史1小时K线
json
{
  "action": "get_kline_data",
  "symbol": "SHFE.rb2410",
  "duration_seconds": 3600,
  "start_dt": "2024-01-01T09:00:00",
  "end_dt": "2024-01-31T15:00:00",
  "username": "your_username",
  "password": "your_password"
}
返回结果包含指定时间段内的所有K线数据（最多约5000条）。


注意事项
历史K线接口需要天勤专业版账号。

实时接口会等待第一次行情更新，可能会稍有延迟。

密码等敏感信息应妥善保管，避免明文存储。
