# 快代理 API 响应字段说明

## 密钥令牌接口

**接口**：`POST https://auth.kdlapi.com/api/get_secret_token`

**Content-Type**：`application/x-www-form-urlencoded`

**参数**：
- `secret_id` - 用户密钥ID
- `secret_key` - 用户密钥Key

**请求示例**：
```
POST https://auth.kdlapi.com/api/get_secret_token
Content-Type: application/x-www-form-urlencoded

secret_id=example_secret_id_123&secret_key=example_secret_key_abc
```

**返回示例**：
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "secret_token": "获得的令牌字符串",
    "expire_time": "YYYY-MM-DD HH:MM:SS"
  }
}
```

**说明**：
- `secret_token` 作为其他API的 `signature` 参数使用
- Token 有效期通常为1小时，过期需重新获取

---

## 获取代理IP接口

### 隧道代理Pro当前IP

**接口**：`GET https://tps.kdlapi.com/api/tpsprocurrentip`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）

**请求示例**：
```
GET https://tps.kdlapi.com/api/tpsprocurrentip?secret_id=example_id&signature=xxx
```

**返回示例**：
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "ip": "1.2.3.4"
  }
}
```

**⚠️ 错误码说明**：

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `-4` | 换IP周期不足30秒 | 此API仅支持**换IP周期 >= 30秒**的隧道订单，请在订单管理中确认换IP周期设置 |

---

### 隧道代理当前IP

**接口**：`GET https://tps.kdlapi.com/api/tpscurrentip`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）

**请求示例**：
```
GET https://tps.kdlapi.com/api/tpscurrentip?secret_id=example_id&signature=xxx
```

**⚠️ 错误码说明**：

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `-4` | 换IP周期不足30秒 | 此API仅支持**换IP周期 >= 30秒**的隧道订单，请在订单管理中确认换IP周期设置 |

---

### 私密代理IP

**接口**：`GET https://dps.kdlapi.com/api/getdps`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）
- `num` - 提取数量（可选，默认1）

**请求示例**：
```
GET https://dps.kdlapi.com/api/getdps?secret_id=example_id&num=5&signature=xxx
```

**返回示例**：
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "proxy_list": [
      {"ip": "1.2.3.4", "port": 5678},
      {"ip": "5.6.7.8", "port": 9012}
    ]
  }
}
```

**⚠️ 错误码说明**：

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `1` | 今日提取余额已用尽 | 等待次日自动恢复，或充值增加配额 |
| `2` | 订单提取余额已用尽 | 订单配额耗尽，需续费或升级套餐 |
| `3` | 没有找到符合条件的代理 | 调整筛选条件，如地区、协议等 |
| `4` | 账号尚未通过实名认证 | 完成实名认证后再使用 |
| `-1` | 无效请求 | 检查请求格式是否正确 |
| `-2` | 订单无效（刚下单需等待） | 下单后1分钟内订单自动生效，请稍候 |
| `-3` | 参数错误 | 检查参数是否完整且格式正确 |
| `-4` | 提取失败: $err_msg | 查看具体错误信息处理 |
| `-5` | 此订单不能提取私密代理 | 确认订单产品类型是否为私密代理 |
| `-6` | 调用IP不在白名单内 | 在订单设置中添加调用IP到白名单 |
| `-51` | 订单1分钟内允许最多$ip_number个IP调用 | 控制调用IP数量，避免超限 |
| `-16` | 订单已退款 | 无法使用，需重新下单 |
| `-15` | 订单已过期 | 续费或重新下单 |
| `-14` | 订单被封禁 | 联系客服处理 |
| `-13` | 订单已过期 | 续费或重新下单 |
| `-12` | 订单无效 | 检查订单状态 |
| `-11` | 订单尚未支付 | 完成支付后再使用 |

---

### 独享代理IP

**接口**：`GET https://kps.kdlapi.com/api/getkps`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）

**请求示例**：
```
GET https://kps.kdlapi.com/api/getkps?secret_id=example_id&signature=xxx
```

**⚠️ 错误码说明**：

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `2` | 订单已过期 | 续费或重新下单 |
| `3` | 没有找到符合条件的代理 | 调整筛选条件 |
| `4` | 账号尚未通过实名认证 | 完成实名认证后再使用 |
| `-1` | 无效请求 | 检查请求格式是否正确 |
| `-2` | 订单无效（刚下单需等待） | 下单后1分钟内订单自动生效，请稍候 |
| `-3` | 参数错误 | 检查参数是否完整且格式正确 |
| `-4` | 提取失败: $err_msg | 查看具体错误信息处理 |
| `-5` | 此订单不能提取独享代理 | 确认订单产品类型是否为独享代理 |
| `-51` | 订单1分钟内允许最多$ip_number个IP调用 | 控制调用IP数量，避免超限 |
| `-16` | 订单已退款 | 无法使用，需重新下单 |
| `-15/-13` | 订单已过期 | 续费或重新下单 |
| `-14` | 订单被封禁 | 联系客服处理 |
| `-12` | 订单无效 | 检查订单状态 |
| `-11` | 订单尚未支付 | 完成支付后再使用 |

---

### 海外动态代理隧道IP

**接口**：`GET https://fps.kdlapi.com/api/getfps`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）

**请求示例**：
```
GET https://fps.kdlapi.com/api/getfps?secret_id=example_id&signature=xxx
```

**⚠️ 错误码说明**：

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `2` | 订单已过期 | 续费或重新下单 |
| `3` | 暂无可用代理 | 等待或联系客服 |
| `4` | 账号尚未通过实名认证 | 完成实名认证后再使用 |
| `-1` | 无效请求 | 检查请求格式是否正确 |
| `-2` | 订单无效（刚下单需等待） | 下单后1分钟内订单自动生效，请稍候 |
| `-3` | 参数错误 | 检查参数是否完整且格式正确 |
| `-4` | 提取失败: $err_msg | 查看具体错误信息处理 |
| `-5` | 此订单不能提取海外代理动态住宅 | 确认订单产品类型是否为海外动态代理 |
| `-51` | 订单1分钟内允许最多$ip_number个IP调用 | 控制调用IP数量，避免超限 |
| `-16` | 订单已退款 | 无法使用，需重新下单 |
| `-15/-13` | 订单已过期 | 续费或重新下单 |
| `-14` | 订单被封禁 | 联系客服处理 |
| `-12` | 订单无效 | 检查订单状态 |
| `-11` | 订单尚未支付 | 完成支付后再使用 |

---

### 海外静态住宅IP

**接口**：`GET https://dev.kdlapi.com/api/getsfps`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）

**请求示例**：
```
GET https://dev.kdlapi.com/api/getsfps?secret_id=example_id&signature=xxx
```

**⚠️ 错误码说明**：

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `2` | 订单已过期 | 续费或重新下单 |
| `3` | 没有找到符合条件的代理 | 调整筛选条件 |
| `4` | 账号尚未通过实名认证 | 完成实名认证后再使用 |
| `-1` | 无效请求 | 检查请求格式是否正确 |
| `-2` | 订单无效（刚下单需等待） | 下单后1分钟内订单自动生效，请稍候 |
| `-3` | 参数错误 | 检查参数是否完整且格式正确 |
| `-4` | 提取失败: $err_msg | 查看具体错误信息处理 |
| `-5` | 此订单不能提取海外代理静态住宅 | 确认订单产品类型是否为海外静态代理 |
| `-51` | 订单1分钟内允许最多$ip_number个IP调用 | 控制调用IP数量，避免超限 |
| `-16` | 订单已退款 | 无法使用，需重新下单 |
| `-15/-13` | 订单已过期 | 续费或重新下单 |
| `-14` | 订单被封禁 | 联系客服处理 |
| `-12` | 订单无效 | 检查订单状态 |
| `-11` | 订单尚未支付 | 完成支付后再使用 |

---

## 订单信息接口

**接口**：`GET https://dev.kdlapi.com/api/getorderinfo`

**参数**：
- `secret_id` - 用户密钥ID
- `signature` - 签名（密钥令牌）

---

## 公共字段（所有产品类型）

| 字段 | 说明 | 取值 |
|------|------|------|
| `orderid` | 订单号 | |
| `pay_type` | 付费方式 | `PRE_PAY`: 包年包月(预付费)<br>`PRE_PAY_IP`: 按IP付费(预付费)<br>`POST_PAY`: 按量付费(后付费) |
| `product` | 产品类型 | 见下表 |
| `status` | 订单状态 | `VALID`: 有效<br>`WAIT_PAY`: 待支付<br>`OPENING`: 开通中<br>`EXPIRED`: 已过期<br>`OWING`: 欠费暂停<br>`CLOSED`: 已关闭<br>`FORBIDDEN`: 被封禁 |
| `expire_time` | 订单到期时间（仅包年包月订单返回） | 格式：`2021-08-18 12:01:43` |
| `is_auto_renew` | 是否开启自动续费（仅包年包月订单返回） | `true` / `false` |
| `auto_renew_time_type` | 自动续费时长（仅 `is_auto_renew=true` 时返回） | `DAY`: 按天<br>`WEEK`: 按周<br>`MONTH`: 按月<br>`YEAR`: 按年 |
| `freeze_amount` | 订单冻结金额（仅按量付费订单返回） | 单位：元，如 `36.28` |
| `unit_price` | 计费单价（仅按量付费订单返回） | 单位：元，如 `1.95` |

---

## 产品类型对照表

| product值 | 产品名称 | 特有字段 |
|-----------|----------|----------|
| `TPS` | 隧道代理 | tunnel_* 系列 |
| `DPS` | 私密代理 | proxy_username, proxy_password |
| `KPS` | 独享代理 | proxy_count, proxy_username, proxy_password |
| `FPS` | 海外动态代理 | fps_* 系列, transfer_area |
| `FPS_STATIC` | 海外静态代理 | proxy_count, proxy_username, proxy_password |

---

## 隧道代理 (TPS) 响应示例

```json
{
  "msg": "",
  "code": 0,
  "data": {
    "orderid": "123456789012345",
    "pay_type": "POST_PAY",
    "product": "TPS",
    "status": "VALID",
    "freeze_amount": "2.68",
    "unit_price": "2.68",
    "tunnel_password": "example_password",
    "tunnel_username": "t12345678901234",
    "tunnel_host": "tps123.kdlapi.com",
    "tunnel_port_http": "12345",
    "tunnel_port_socks": "20806",
    "tunnel_bandwidth": 10,
    "tunnel_req": 20
  }
}
```

### 隧道代理特有字段

| 字段 | 说明 |
|------|------|
| `tunnel_host` | 隧道host |
| `tunnel_port_http` | 隧道HTTP端口 |
| `tunnel_port_socks` | 隧道SOCKS端口 |
| `tunnel_username` | 隧道用户名 |
| `tunnel_password` | 隧道密码 |
| `tunnel_period` | 隧道换IP周期（秒） |
| `tunnel_bandwidth` | 隧道带宽（Mbps） |
| `tunnel_req` | 隧道并发上限 |

---

## 私密代理 (DPS) 响应示例

```json
{
  "msg": "",
  "code": 0,
  "data": {
    "orderid": "123456789012346",
    "pay_type": "PRE_PAY_IP",
    "product": "DPS",
    "status": "VALID",
    "expire_time": "2026-05-01 12:00:00",
    "proxy_username": "dps_user_example",
    "proxy_password": "dps_pass_example"
  }
}
```

### 私密代理特有字段

| 字段 | 说明 |
|------|------|
| `proxy_username` | 私密代理用户名 |
| `proxy_password` | 私密代理密码 |

---

## 独享代理 (KPS) 响应示例

```json
{
  "msg": "",
  "code": 0,
  "data": {
    "orderid": "123456789012347",
    "pay_type": "PRE_PAY",
    "product": "KPS",
    "status": "VALID",
    "expire_time": "2026-06-01 12:00:00",
    "proxy_count": 5,
    "proxy_username": "kps_user_example",
    "proxy_password": "kps_pass_example"
  }
}
```

### 独享代理特有字段

| 字段 | 说明 |
|------|------|
| `proxy_count` | 此订单下的独享代理数量 |
| `proxy_username` | 独享代理用户名 |
| `proxy_password` | 独享代理密码 |

---

## 海外动态代理 (FPS) 响应示例

```json
{
  "msg": "",
  "code": 0,
  "data": {
    "orderid": "123456789012348",
    "pay_type": "POST_PAY",
    "product": "FPS",
    "status": "VALID",
    "freeze_amount": "5.00",
    "unit_price": "5.00",
    "proxy_username": "fps_user_example",
    "proxy_password": "fps_pass_example",
    "transfer_area": "US",
    "fps_host": "fps123.kdlapi.com",
    "fps_port_http": "12400",
    "fps_port_socks": "12401"
  }
}
```

### 海外动态代理特有字段

| 字段 | 说明 |
|------|------|
| `proxy_username` | 海外动态代理用户名 |
| `proxy_password` | 海外动态代理密码 |
| `transfer_area` | 转发地区（如 US、JP、UK 等） |
| `fps_host` | 隧道host |
| `fps_port_http` | 隧道HTTP端口 |
| `fps_port_socks` | 隧道SOCKS端口 |

---

## 海外静态代理 (FPS_STATIC) 响应示例

```json
{
  "msg": "",
  "code": 0,
  "data": {
    "orderid": "123456789012349",
    "pay_type": "PRE_PAY",
    "product": "FPS_STATIC",
    "status": "VALID",
    "expire_time": "2026-12-01 12:00:00",
    "proxy_count": 10,
    "proxy_username": "fps_static_user_example",
    "proxy_password": "fps_static_pass_example"
  }
}
```

### 海外静态代理特有字段

| 字段 | 说明 |
|------|------|
| `proxy_count` | 此订单下的海外静态代理数量 |
| `proxy_username` | 海外静态代理用户名（包段订单返回此字段） |
| `proxy_password` | 海外静态代理密码（包段订单返回此字段） |

---

## 代理地址格式

### 隧道代理/海外动态代理
```
http://username:password@host:port
```

示例：
```
http://t12345678901234:example_password@tps123.kdlapi.com:12345
```

### 私密代理/独享代理/海外静态代理
需要通过API获取具体IP列表，认证方式为用户名密码。

---

## 快代理 API 类型

| API | 用途 | URL格式 |
|-----|------|---------|
| TPS隧道代理 | 获取隧道代理IP | `https://tps.kdlapi.com/api/gettps` |
| DPS私密代理 | 获取私密代理IP | `https://dps.kdlapi.com/api/getdps` |
| KPS独享代理 | 获取独享代理IP | `https://kps.kdlapi.com/api/getkps` |
| FPS海外动态 | 获取海外动态代理IP | `https://fps.kdlapi.com/api/getfps` |

## 官方文档

- 订单信息API：https://www.kuaidaili.com/doc/api/getorderinfo/
- 用户中心：https://www.kuaidaili.com/uc/overview/
- 订单管理：https://www.kuaidaili.com/uc/order-list/