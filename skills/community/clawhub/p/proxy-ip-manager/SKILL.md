---
name: proxy-ip-manager
description: '快代理(Kuaidaili)智能管理技能，专为快代理用户设计。支持API配置、订单信息获取、到期提醒、IP健康检测、智能并发调度、使用统计。触发场景：(1) 用户提及"快代理"、"kuaidaili"、"kdlapi"、"代理IP"；(2) 用户需要检查快代理订单状态、IP质量、并发设置；(3) 用户使用命令 set_config/show_config/get_order_info/check_expiry/check_ip_health/get_concurrency/stats。此技能仅支持快代理服务。'
---

# 快代理智能管理器

专为快代理(Kuaidaili)用户打造的代理IP智能管理技能。

## 快速开始

首次使用需要配置快代理API密钥：

```
用户: set_config secret_id=example_id123 secret_key=example_key456
```

⚠️ **安全提示**：
- **请在私聊中配置密钥**，不要在群聊中发送，避免泄露给他人
- 密钥仅保存在你的本地设备，不会上传或分享
- 配置后使用 `show_config` 查看的是脱敏后的信息

**密钥获取方式**：
1. 登录快代理会员中心：https://www.kuaidaili.com/uc/overview/
2. 进入「API密钥管理」页面
3. 获取订单的 `SecretId` 和 `SecretKey`

**认证流程**：
系统会自动调用 `https://auth.kdlapi.com/api/get_secret_token` 获取 `secret_token` 作为签名凭证。

配置成功后可使用所有功能。

---

## 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `set_config` | 配置API密钥 | `set_config secret_id=xxx secret_key=xxx` |
| `show_config` | 显示当前配置（脱敏） | `show_config` |
| `get_order_info` | 获取订单详情 | `get_order_info` |
| `get_ip` | 获取代理IP | `get_ip` 或 `get_ip num=5` |
| `check_expiry` | 检查到期时间 | `check_expiry` |
| `check_ip_health` | IP健康检测 | `check_ip_health` |
| `get_concurrency` | 智能并发推荐 | `get_concurrency` |
| `stats` | 使用统计报告 | `stats` |

---

## 获取代理IP

配置 secret_id 和 secret_key 后，可以获取对应订单的代理IP。

### 命令

```
get_ip          # 获取代理IP（默认1个）
get_ip num=5    # 指定获取数量
```

### 支持的产品类型

| 产品类型 | API接口 | 说明 |
|---------|---------|------|
| 隧道代理Pro | `https://tps.kdlapi.com/api/tpsprocurrentip` | 获取当前隧道IP |
| 隧道代理 | `https://tps.kdlapi.com/api/tpscurrentip` | 获取当前隧道IP |
| 私密代理 | `https://dps.kdlapi.com/api/getdps` | 提取IP，支持 `num` 参数 |
| 独享代理 | `https://kps.kdlapi.com/api/getkps` | 提取IP |
| 海外动态代理 | `https://fps.kdlapi.com/api/getfps` | 获取隧道IP |
| 海外静态住宅 | `https://dev.kdlapi.com/api/getsfps` | 获取静态住宅IP |

### 请求参数

| 参数 | 说明 |
|------|------|
| `secret_id` | 用户密钥ID（必填） |
| `signature` | 签名/令牌（必填，系统自动获取） |
| `num` | 提取数量（仅私密代理支持，默认1） |

### 调用示例

**隧道代理Pro当前IP**：
```
GET https://tps.kdlapi.com/api/tpsprocurrentip?secret_id=example_id&signature=xxx
```
⚠️ **限制**：仅支持换IP周期 >= 30秒的隧道订单，否则返回错误码 `-4`

**隧道代理当前IP**：
```
GET https://tps.kdlapi.com/api/tpscurrentip?secret_id=example_id&signature=xxx
```
⚠️ **限制**：仅支持换IP周期 >= 30秒的隧道订单，否则返回错误码 `-4`

**私密代理IP（支持数量）**：
```
GET https://dps.kdlapi.com/api/getdps?secret_id=example_id&num=5&signature=xxx
```

**独享代理IP**：
```
GET https://kps.kdlapi.com/api/getkps?secret_id=example_id&signature=xxx
```

**海外动态代理隧道IP**：
```
GET https://fps.kdlapi.com/api/getfps?secret_id=example_id&signature=xxx
```

**海外静态住宅IP**：
```
GET https://dev.kdlapi.com/api/getsfps?secret_id=example_id&signature=xxx
```

### 返回格式

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "ip_list": ["1.2.3.4:5678", "5.6.7.8:9012"]
  }
}
```

---

## 订单信息API

### 获取订单详情

**接口**：`GET https://dev.kdlapi.com/api/getorderinfo`

**返回字段**：

### 公共字段（所有产品）
| 字段 | 说明 |
|------|------|
| `orderid` | 订单ID |
| `product` | 产品类型 |
| `status` | 订单状态 |
| `pay_type` | 付费方式 |
| `expire_time` | 到期时间（仅包年包月订单） |

### 隧道代理 (TPS) 特有字段
| 字段 | 说明 |
|------|------|
| `tunnel_host` | 代理主机 |
| `tunnel_port_http` | HTTP端口 |
| `tunnel_username` | 认证用户名 |
| `tunnel_password` | 认证密码 |
| `tunnel_req` | 并发上限 |
| `tunnel_bandwidth` | 带宽（Mbps） |

### 私密代理 (DPS) 特有字段
| 字段 | 说明 |
|------|------|
| `proxy_username` | 认证用户名 |
| `proxy_password` | 认证密码 |

### 独享代理 (KPS) 特有字段
| 字段 | 说明 |
|------|------|
| `proxy_count` | 独享代理数量 |
| `proxy_username` | 认证用户名 |
| `proxy_password` | 认证密码 |

### 海外动态代理 (FPS) 特有字段
| 字段 | 说明 |
|------|------|
| `proxy_username` | 认证用户名 |
| `proxy_password` | 认证密码 |
| `transfer_area` | 转发地区（如 US、JP、UK） |
| `fps_host` | 隧道主机 |
| `fps_port_http` | HTTP端口 |
| `fps_port_socks` | SOCKS端口 |

### 海外静态代理 (FPS_STATIC) 特有字段
| 字段 | 说明 |
|------|------|
| `proxy_count` | 代理数量 |
| `proxy_username` | 认证用户名（包段订单返回） |
| `proxy_password` | 认证密码（包段订单返回） |

**注意**：不同产品返回的字段不同，带宽和并发仅隧道代理(TPS)返回。详见 [references/api_response.md](references/api_response.md)

### 获取到期时间

**接口**：`GET https://dev.kdlapi.com/api/getorderexpiretime`

**返回字段**：
| 字段 | 说明 |
|------|------|
| `expire_time` | 到期时间（格式：YYYY-MM-DD HH:MM:SS） |

详见 [references/api_response.md](references/api_response.md)

---

## 配置管理

### 初始化检查

运行 `scripts/config_manager.py` 检查配置状态：
- 未配置 → 提示用户使用 `set_config`
- 已配置 → 验证密钥有效性

### 配置存储

配置保存在 `~/.openclaw/skills/proxy-ip-manager/config.json`：
```json
{
  "secret_id": "example_id123",
  "secret_key": "example_key456",
  "secret_token": "自动获取的令牌",
  "token_expire_time": "令牌过期时间",
  "test_url": "https://httpbin.org/ip",
  "timeout": 5,
  "configured_at": "YYYY-MM-DDTHH:MM:SS"
}
```

### 认证流程

1. 用户提供 `secret_id` 和 `secret_key`
2. 系统调用 `https://auth.kdlapi.com/api/get_secret_token` 获取 `secret_token`
3. `secret_token` 作为 `signature` 参数调用各API

### 安全脱敏

日志和输出中自动脱敏：
- `secret_id=exam***d123`
- `secret_key=exa***y456`
- `secret_token=自动脱敏`

---

## API调用规范

使用 `scripts/api_client.py` 封装所有API调用：

```python
# 自动特性
- 超时控制（5秒）
- 自动重试（最多3次）
- 错误处理和脱敏日志
```

### 返回字段解析

详见 [references/api_response.md](references/api_response.md)

关键字段：
- `ip_list` → 代理IP列表
- `max_concurrency` → 并发上限
- `expire_time` → 订单到期时间
- `username/password/host/port` → 认证信息

---

## 订单到期模块

运行 `scripts/expiry_checker.py`：

### 提醒规则

| 剩余天数 | 状态 | 提示级别 |
|---------|------|---------|
| >5天 | 正常 | 无 |
| 3-5天 | 注意 | 5天提醒 |
| 1-3天 | 警告 | 3天提醒 |
| <1天 | 紧急 | 1天提醒 |
| ≤0天 | 已过期 | 停止服务 |

### 过期处理

订单过期后：
- 并发 = 0
- 停止健康检测
- 状态标记为 `expired`
- 提示续费链接：https://www.kuaidaili.com/uc/order-list/

---

## IP健康检测

运行 `scripts/health_checker.py`：

### 检测流程

1. 从API获取多个代理IP
2. 使用 test_url 发请求测试
3. 记录成功/失败、响应延迟、状态码

### 评分算法

详见 [references/scoring_rules.md](references/scoring_rules.md)

```
score = success_rate * 70 + latency_score * 30

latency评分：
- <1s → 100分
- 1~3s → 80分
- >3s → 50分
```

### 输出指标

- IP质量评分（0-100）
- 成功率（%）
- 平均延迟（ms）

---

## 智能并发调度

运行 `scripts/scheduler.py`：

### 动态调整策略

| success_rate | 并发调整 |
|-------------|---------|
| >95% | base * 1.0 |
| 80-95% | base * 0.7 |
| 60-80% | base * 0.5 |
| <60% | base * 0.3 |

base = max_concurrency * 0.8

### 失败保护

- 连续失败 > 10 → 并发降低50%
- success_rate < 50% → 并发降至最低

---

## 使用统计

运行 `scripts/stats_tracker.py`：

### 统计内容

- 每日请求数
- 成功数/失败数
- 成功率
- 最近7天趋势

### 状态评估

| 成功率趋势 | 状态 |
|-----------|------|
| 稳定在90%+ | 稳定 |
| 波动10%以内 | 波动 |
| 波动>10%或<70% | 风险 |

---

## 异常处理

### API错误码对照

**隧道代理 (TPS) 错误码**：

| 错误码 | 说明 |
|-------|------|
| `-4` | 换IP周期不足30秒（仅支持换IP周期>=30秒的订单） |

**私密代理 (DPS) 错误码**：

| 错误码 | 说明 |
|-------|------|
| `1` | 今日提取余额已用尽 |
| `2` | 订单提取余额已用尽 |
| `3` | 没有找到符合条件的代理 |
| `4` | 账号尚未通过实名认证 |
| `-1` | 无效请求 |
| `-2` | 订单无效（刚下单需等待1分钟生效） |
| `-3` | 参数错误 |
| `-4` | 提取失败 |
| `-5` | 此订单不能提取私密代理 |
| `-6` | 调用IP不在白名单内 |
| `-51` | 订单1分钟内调用IP超限 |
| `-16` | 订单已退款 |
| `-15/-13` | 订单已过期 |
| `-14` | 订单被封禁（联系客服） |
| `-12` | 订单无效 |
| `-11` | 订单尚未支付 |

**独享代理 (KPS) 错误码**：

| 错误码 | 说明 |
|-------|------|
| `2` | 订单已过期 |
| `3` | 没有找到符合条件的代理 |
| `4` | 账号尚未通过实名认证 |
| `-1` | 无效请求 |
| `-2` | 订单无效（刚下单需等待1分钟生效） |
| `-3` | 参数错误 |
| `-4` | 提取失败 |
| `-5` | 此订单不能提取独享代理 |
| `-51` | 订单1分钟内调用IP超限 |
| `-16/-15/-13` | 订单已过期/退款 |
| `-14` | 订单被封禁（联系客服） |
| `-12/-11` | 订单无效/未支付 |

**海外动态代理 (FPS) 错误码**：

| 错误码 | 说明 |
|-------|------|
| `2` | 订单已过期 |
| `3` | 暂无可用代理 |
| `4` | 账号尚未通过实名认证 |
| `-1/-2/-3/-4` | 无效请求/订单无效/参数错误/提取失败 |
| `-5` | 此订单不能提取海外代理动态住宅 |
| `-51` | 订单1分钟内调用IP超限 |
| `-16/-15/-13/-14/-12/-11` | 订单状态异常（过期/退款/封禁等） |

**海外静态住宅 (FPS_STATIC) 错误码**：

| 错误码 | 说明 |
|-------|------|
| `2` | 订单已过期 |
| `3` | 没有找到符合条件的代理 |
| `4` | 账号尚未通过实名认证 |
| `-1/-2/-3/-4` | 无效请求/订单无效/参数错误/提取失败 |
| `-5` | 此订单不能提取海外代理静态住宅 |
| `-51` | 订单1分钟内调用IP超限 |
| `-16/-15/-13/-14/-12/-11` | 订单状态异常（过期/退款/封禁等） |

**公共错误码**：

| 错误码 | 说明 | 通用解决方案 |
|-------|------|---------|
| `-2` | 订单无效（刚下单） | 等待1分钟自动生效 |
| `-5` | 产品类型不匹配 | 确认订单产品类型与API对应 |
| `-51` | 调用IP数量超限 | 控制调用频率 |
| `-15/-13` | 订单已过期 | 续费或重新下单 |
| `-14` | 订单被封禁 | 联系客服处理 |

**其他异常**：

| 异常类型 | 输出提示 |
|---------|---------|
| 未配置 | "请先配置代理API密钥（使用 set_config）" |
| API调用失败 | "代理API调用失败，请检查API密钥是否有效" |
| 数据异常 | "API返回数据异常，请联系服务提供方" |
| 网络错误 | "网络连接失败，请检查网络环境" |

---

## 订单到期提醒

### 命令

```
check_expiry      # 检查到期时间，输出提醒信息
```

### 输出格式

返回 JSON 格式，包含：
- `need_notify`: 是否需要提醒（true/false）
- `days_left`: 剩余天数
- `expire_time`: 到期时间
- `notification_text`: 格式化的提醒文本

### 提醒规则

| 剩余天数 | 级别 | 说明 |
|---------|------|------|
| 5天 | 📅 提醒 | 请安排续费 |
| 3天 | ⚠️ 警告 | 请尽快续费 |
| 1天 | 🚨 紧急 | 请立即续费 |
| 已过期 | 🚨 紧急 | 已过期，立即续费 |

### 配置定时提醒

用户可自行配置定时任务，调用脚本获取提醒信息后发送通知：

**脚本路径**（相对于 skill 目录）：
```
scripts/expiry_notify.py
```

或使用绝对路径（将 `<USER>` 替换为你的用户名）：
```
C:\Users\<USER>\.openclaw\skills\proxy-ip-manager\scripts\expiry_notify.py
```

**示例输出**（需要提醒时）：
```json
{
  "need_notify": true,
  "days_left": 3,
  "expire_time": "YYYY-MM-DD HH:MM:SS",
  "notification_text": "⚠️【快代理订单到期警告】\n\n快代理订单将在3天后到期，请尽快续费。\n\n到期时间：YYYY-MM-DD HH:MM:SS\n剩余天数：3 天\n续费链接：https://www.kuaidaili.com/uc/order-list/"
}
```

---

## 脚本文件

| 脚本 | 用途 |
|------|------|
| `scripts/config_manager.py` | 配置管理（存储、读取、验证） |
| `scripts/api_client.py` | 代理IP获取 |
| `scripts/order_info.py` | 订单信息查询 |
| `scripts/expiry_checker.py` | 订单到期检查 |
| `scripts/health_checker.py` | IP健康检测 |
| `scripts/scheduler.py` | 智能并发调度 |
| `scripts/stats_tracker.py` | 使用统计 |