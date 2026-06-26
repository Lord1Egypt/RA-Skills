---
name: pushplus
slug: pushplus
description: PushPlus(推送加)消息推送服务，支持微信、邮件、短信、企业微信、钉钉、飞书等多种渠道。使用场景：(1) 系统监控告警通知 (2) 定时任务执行结果通知 (3) 业务异常告警 (4) 日常消息提醒。当用户需要发送推送消息、配置消息通知、查询推送结果时使用此 Skill。
author: luch
version: 1.1.0
category: notification
changelog: 升级API至v1.13，新增clawbot渠道和36个OpenAPI接口（群组用户/渠道配置/ClawBot/功能设置/好友/预处理）
tags: [pushplus, notification, wechat, email, webhook, dingtalk, feishu, sms, clawbot]
env:
  - name: PUSHPLUS_TOKEN
    description: PushPlus 用户 Token/消息 Token（用于基础推送功能）
    required: true
  - name: PUSHPLUS_USER_TOKEN
    description: PushPlus 用户 Token（用于 OpenAPI 功能）
    required: false
  - name: PUSHPLUS_SECRET_KEY
    description: PushPlus SecretKey（用于 OpenAPI 功能）
    required: false
credentials:
  - name: PUSHPLUS_TOKEN
    type: api_key
    description: PushPlus API Token
---

# PushPlus 消息推送服务

## 功能概述

PushPlus(推送加)是一个集成了微信、短信、邮件、企业微信、钉钉、飞书等多种渠道的实时消息推送平台。

本 Skill 的能力设计是平台无关的，可用于支持 Skill 安装能力的各类 agent/runtime。当前仓库示例以 Python 脚本为主实现，不绑定单一 agent 平台。

### 核心功能

- **多渠道推送**：支持微信公众号、邮件、短信、企业微信、钉钉、飞书、语音、App、插件等
- **多消息类型**：支持文本、HTML、Markdown、JSON 等格式
- **一对多推送**：支持群组消息，一次推送给多人
- **多渠道同时发送**：支持一次请求同时发送到多个渠道
- **好友消息**：支持向指定好友发送消息
- **模板消息**：内置多种消息模板，如阿里云监控、Jenkins、支付通知等

## 使用时机

当用户需要以下功能时，使用此 Skill：

1. **发送推送消息**到微信、邮件、钉钉、飞书等渠道
2. **配置消息通知**用于系统监控、定时任务通知
3. **查询推送结果**或管理消息历史
4. **管理群组**或消息 Token

## Agent 调用规则

### 默认入口

- 普通消息通知：优先使用 `scripts/pushplus.py` 中的 `send_message()`
- 多渠道同时通知：明确要求多渠道时再使用 `send_batch_message()`
- OpenAPI 管理能力：仅当用户明确要求查询管理信息或执行管理操作时使用 `scripts/pushplus_openapi.py`

### 默认行为

- 默认渠道：`wechat`
- 默认模板：`html`
- 未显式指定多渠道时，不调用 `batchSend`
- 未明确要求收费渠道时，不自动使用 `sms`、`voice`

### 环境变量缺失时的处理

- 缺少 `PUSHPLUS_TOKEN`：不能执行基础消息发送
- 缺少 `PUSHPLUS_USER_TOKEN` 或 `PUSHPLUS_SECRET_KEY`：不能执行 OpenAPI 相关能力
- 若凭据不足，应直接提示缺少的环境变量，不自动降级到高风险或收费能力

### 副作用与确认规则

- 发送消息、查询结果、查询用户信息：可直接执行
- 新增 Token、新增群组、修改 Token：执行前应确认用户明确有管理意图
- 删除消息、删除 Token、删除群组、退出群组：属于高风险操作，执行前应获得用户明确确认

## 环境变量配置

| 环境变量名 | 说明 | 必须 |
|-----------|------|------|
| `PUSHPLUS_TOKEN` | 用户 Token/消息 Token | 使用推送消息，必须配置 |
| `PUSHPLUS_USER_TOKEN` | 用户 Token（用于 OpenAPI,不支持使用消息token） | 使用OpenAPI相关功能，必须配置 |
| `PUSHPLUS_SECRET_KEY` | 用户 SecretKey（用于 OpenAPI） | 使用OpenAPI相关功能，必须配置 |

Token 获取地址：[https://www.pushplus.plus/uc-dev.html](https://www.pushplus.plus/uc-dev.html)

如果使用OpenAPI相关功能，需要配置`安全IP地址`、`开放接口`设置

### 凭据使用边界

| 场景 | 需要的凭据 |
|------|-----------|
| 仅发送普通消息 | `PUSHPLUS_TOKEN` |
| 发送群组消息/多渠道消息 | `PUSHPLUS_TOKEN` |
| 调用 OpenAPI 查询或管理能力 | `PUSHPLUS_USER_TOKEN` + `PUSHPLUS_SECRET_KEY` |

说明：
- `PUSHPLUS_TOKEN` 用于基础推送能力，可为用户 Token 或消息 Token
- `PUSHPLUS_USER_TOKEN` 仅用于 OpenAPI AccessKey 获取，不支持使用消息 Token 替代
- 使用 OpenAPI 时，必须同时提供 `PUSHPLUS_USER_TOKEN` 和 `PUSHPLUS_SECRET_KEY`

## 快速开始

### 1. 发送消息

使用脚本发送简单消息：

```bash
python3 scripts/pushplus.py -t YOUR_TOKEN -c "消息内容" --title "消息标题"
```

或使用环境变量：

```bash
export PUSHPLUS_TOKEN="your_token"
python3 scripts/pushplus.py -c "消息内容"
```

### 2. 使用 Python 函数

```python
from scripts.pushplus import send_message, send_wechat_message, send_email_message

# 发送微信消息
result = send_wechat_message(
    token="YOUR_TOKEN",
    title="系统告警",
    content="CPU 使用率超过 90%"
)

# 发送邮件
result = send_email_message(
    token="YOUR_TOKEN",
    title="日报",
    content="今日数据统计..."
)
```

## 脚本使用说明

### 能力分层

#### 默认安全能力

- 发送普通消息、多渠道消息
- 查询消息发送结果、消息列表、消息详情
- 查询用户信息、请求次数、解封时间等只读信息
- 查询群组列表、群组详情、群组用户列表、群组二维码
- 查询消息 Token 列表、下拉选择列表
- 查询渠道配置（webhook/公众号/企业微信/邮箱列表及详情）
- 查询默认配置列表及详情
- 查询好友列表、个人二维码
- 查询预处理信息列表及详情
- ClawBot 二维码获取、扫码状态查询、绑定详情、消息获取

#### 谨慎能力

- 新增/修改消息 Token
- 新增/修改群组、上下架积分群组、修改订阅人备注
- 新增/修改 webhook 渠道
- 新增/修改默认配置
- 新增/修改预处理信息
- 修改接收消息限制、开启/关闭发送、修改打开消息方式、修改插件转发
- 修改好友备注
- 测试预处理代码

#### 高风险能力

- 删除消息、删除消息 Token
- 删除群组、退出群组、删除群组内用户
- 删除默认配置
- 删除好友
- 删除预处理信息
- 解绑 ClawBot

对高风险能力，建议仅在用户明确要求时调用。

### 命令行参数

```
python3 scripts/pushplus.py [选项]

必填参数:
  -t, --token     PushPlus Token（也可通过环境变量 PUSHPLUS_TOKEN 设置）
  -c, --content   消息内容

可选参数:
  --title         消息标题
  --topic         群组编码（一对多消息）
  --template      消息模板 (html/txt/json/markdown/cloudMonitor/jenkins/route/pay)
  --channel       推送渠道 (wechat/webhook/cp/mail/sms/extension/voice/app/clawbot)
  --channels      多渠道发送，逗号分隔，如 "wechat,webhook,extension"
  --webhook       Webhook 编码（已废弃，请使用 --option）
  --option        渠道配置参数（原 webhook 参数，多个渠道用逗号分隔）
  --options       多渠道配置参数，逗号分隔
  --callback-url  回调地址
  --timestamp     时间戳（毫秒）
  --to            好友令牌，支持多人（逗号分隔）
  --pre           预处理编码
  -v, --verbose   显示详细信息
```

### 使用示例

#### 1. 发送简单微信消息

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一条测试消息"
```

#### 2. 发送带标题的消息

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "服务器 CPU 使用率达到 95%" \
    --title "系统告警"
```

#### 3. 发送 Markdown 格式消息

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "# 今日日报
## 数据统计
- 新增用户: 100
- 活跃用户数: 1000" \
    --template markdown \
    --title "日报"
```

#### 4. 发送邮件

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一封测试邮件" \
    --title "邮件标题" \
    --channel mail
```

#### 5. 发送一对多消息（群组消息）

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一条群组消息" \
    --title "群组通知" \
    --topic "GROUP_CODE"
```

#### 6. 发送钉钉消息

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一条钉钉消息" \
    --title "钉钉通知" \
    --channel webhook \
    --option "DINGTALK_WEBHOOK_CODE"
```

#### 7. 多渠道同时发送

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一条多渠道消息" \
    --title "多渠道通知" \
    --channels "wechat,webhook,extension" \
    --options ",webhook_code,"
```

#### 8. 发送语音消息

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一条语音消息" \
    --title "语音通知" \
    --channel voice
```

#### 9. 发送 App 消息

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "这是一条 App 推送消息" \
    --title "App通知" \
    --channel app
```

#### 10. 调试模式

```bash
python3 scripts/pushplus.py \
    -t "YOUR_TOKEN" \
    -c "测试消息" \
    -v
```

## Python API 函数说明

### 核心函数

#### `send_message()`

通用消息发送函数，支持所有参数。

```python
def send_message(
    token: str,
    content: str,
    title: Optional[str] = None,
    topic: Optional[str] = None,
    template: str = "html",
    channel: str = "wechat",
    webhook: Optional[str] = None,  # 已废弃，请使用 option
    option: Optional[str] = None,
    callback_url: Optional[str] = None,
    timestamp: Optional[int] = None,
    to: Optional[str] = None,
    pre: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]
```

#### `send_batch_message()`

多渠道同时发送消息。

```python
def send_batch_message(
    token: str,
    content: str,
    channels: List[str],
    title: Optional[str] = None,
    topic: Optional[str] = None,
    template: str = "html",
    options: Optional[List[str]] = None,
    callback_url: Optional[str] = None,
    timestamp: Optional[int] = None,
    to: Optional[str] = None,
    pre: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]
```

### 便捷函数

#### 微信消息

```python
send_wechat_message(
    token: str,
    content: str,
    title: str = "通知",
    topic: str = None
) -> Dict[str, Any]
```

#### 邮件消息

```python
send_email_message(
    token: str,
    content: str,
    title: str,
    topic: str = None
) -> Dict[str, Any]
```

#### Markdown 消息

```python
send_markdown_message(
    token: str,
    content: str,
    title: str = "通知",
    topic: str = None
) -> Dict[str, Any]
```

#### JSON 消息

```python
send_json_message(
    token: str,
    data: dict,
    title: str = "JSON通知",
    topic: str = None
) -> Dict[str, Any]
```

#### 钉钉/飞书/企业微信消息

```python
send_dingtalk_message(
    token: str,
    content: str,
    title: str = "通知",
    webhook: str = None
) -> Dict[str, Any]

send_feishu_message(
    token: str,
    content: str,
    title: str = "通知",
    webhook: str = None
) -> Dict[str, Any]

send_work_wechat_message(
    token: str,
    content: str,
    title: str = "通知",
    webhook: str = None
) -> Dict[str, Any]
```

#### 短信消息

```python
send_sms_message(
    token: str,
    content: str,
    title: str = "短信通知"
) -> Dict[str, Any]
```

#### 语音消息

```python
send_voice_message(
    token: str,
    content: str,
    title: str = "语音通知"
) -> Dict[str, Any]
```

#### App 消息

```python
send_app_message(
    token: str,
    content: str,
    title: str = "通知"
) -> Dict[str, Any]
```

#### 插件消息

```python
send_extension_message(
    token: str,
    content: str,
    title: str = "通知"
) -> Dict[str, Any]
```

#### 模板消息

```python
send_template_message(
    token: str,
    content: str,
    title: str,
    template: str,
    **kwargs
) -> Dict[str, Any]
```

## 参数说明

### 参数校验规则

- `channels` 不能为空列表
- 使用 `--channels` 时，`--options` 的数量应与渠道数量一致；若某个渠道无需配置参数，应保留空位
- OpenAPI 分页参数 `page_size` 最大为 `50`
- 删除类接口属于高风险操作，调用前应先确认用户意图
- 未显式指定收费渠道时，不应默认切换到 `sms` 或 `voice`

### 模板类型

| 模板名称 | 描述 |
|---------|------|
| html | 默认模板，支持 HTML 文本 |
| txt | 纯文本展示，不转义 HTML |
| json | 内容基于 JSON 格式展示 |
| markdown | 内容基于 Markdown 格式展示 |
| cloudMonitor | 阿里云监控报警定制模板 |
| jenkins | Jenkins 插件定制模板 |
| route | 路由器插件定制模板 |
| pay | 支付成功通知模板 |

### 推送渠道

| 渠道 | 是否免费 | 描述 |
|-----|---------|------|
| wechat | 免费 | 微信公众号 |
| webhook | 免费 | 第三方 webhook 渠道（企业微信、钉钉、飞书等） |
| cp | 免费 | 企业微信应用 |
| mail | 免费 | 邮件 |
| sms | 收费 | 短信（10 积分/条，0.1 元） |
| voice | 收费 | 语音（30 积分/条，0.3 元） |
| extension | 免费 | 浏览器插件、桌面应用程序 |
| app | 免费 | App 渠道（支持安卓、鸿蒙、iOS） |
| clawbot | 免费 | 微信 ClawBot |

### 返回码

| 返回码 | 说明 |
|-------|------|
| 200 | 执行成功 |
| 302 | 未登录 |
| 401 | 请求未授权 |
| 403 | 请求 IP 未授权 |
| 500 | 系统异常 |
| 600 | 数据异常 |
| 888 | 积分不足 |
| 900 | 用户账号使用受限（请求次数过多） |
| 903 | 无效的用户令牌 |
| 905 | 账户未进行实名认证 |
| 999 | 服务端验证错误 |

## 使用限制

### 请求频率限制

| 限制类型 | 实名用户 | 会员用户 |
|---------|---------|---------|
| 微信渠道日请求次数 | 200 次 | 2,000 次 |
| 请求频率 | 1 分钟 5 次 | 10 秒 5 次 |
| 相同内容 | 1 小时 3 条 | 1 小时 3 条 |

### 内容长度限制

| 限制类型 | 实名用户 | 会员用户 |
|---------|---------|---------|
| 标题长度 | 100 字 | 200 字 |
| 内容长度 | 2 万字 | 10 万字 |

## OpenAPI 扩展功能

本 Skill 还提供了 `pushplus_openapi.py` 脚本，支持通过 AccessKey 调用 PushPlus OpenAPI，包括：

### 功能模块

1. **AccessKey 管理**
   - `get_access_key()` - 获取 AccessKey（有效期2小时）

2. **消息接口**
   - `list_messages()` - 消息列表
   - `get_message_result()` - 查询发送结果
   - `delete_message()` - 删除消息
   - `get_message_detail()` - 消息详情（HTML）

3. **用户接口**
   - `get_user_token()` - 获取用户 Token
   - `get_user_info()` - 个人资料详情
   - `get_limit_time()` - 解封剩余时间
   - `get_send_count()` - 当日请求次数

4. **消息 Token 接口**
   - `list_tokens()` - 消息 Token 列表
   - `select_token_list()` - Token 下拉选择列表
   - `add_token()` - 新增消息 Token
   - `edit_token()` - 修改消息 Token
   - `delete_token()` - 删除消息 Token

5. **群组接口**
   - `list_topics()` - 群组列表
   - `get_topic_detail()` - 我创建的群组详情
   - `get_join_topic_detail()` - 我加入的群组详情
   - `add_topic()` - 新增群组
   - `edit_topic()` - 修改群组
   - `get_topic_qrcode()` - 群组二维码
   - `exit_topic()` - 退出群组
   - `delete_topic()` - 删除群组
   - `set_topic_is_open()` - 上下架积分群组

6. **群组用户接口**
   - `list_topic_subscribers()` - 群组内用户列表
   - `delete_topic_user()` - 删除群组内用户
   - `edit_topic_user_remark()` - 修改订阅人备注

7. **渠道配置接口**
   - `list_webhooks()` / `get_webhook_detail()` / `add_webhook()` / `edit_webhook()` - Webhook CRUD
   - `list_mp_channels()` - 微信公众号渠道列表
   - `list_cp_channels()` - 企业微信应用渠道列表
   - `list_mail_channels()` / `get_mail_channel_detail()` - 邮箱渠道列表/详情

8. **微信 ClawBot 接口**
   - `get_clawbot_qrcode()` / `get_clawbot_qrcode_status()` - 二维码获取/扫码查询
   - `get_clawbot_bind_info()` / `unbind_clawbot()` - 绑定详情/解绑
   - `get_clawbot_messages()` - 获取发送消息

9. **功能设置接口**
   - `list_default_settings()` / `get_default_setting_detail()` - 默认配置列表/详情
   - `add_default_setting()` / `edit_default_setting()` / `delete_default_setting()` - 默认配置 CRUD
   - `set_receive_limit()` - 接收消息限制
   - `set_send_enabled()` - 发送消息开关
   - `set_open_message_type()` - 消息打开方式
   - `set_extension_forward()` - 插件渠道转发

10. **好友功能接口**
    - `get_personal_qrcode()` - 个人二维码
    - `list_friends()` - 好友列表
    - `delete_friend()` - 删除好友
    - `edit_friend_remark()` - 修改好友备注

11. **预处理信息接口**
    - `list_pre_info()` / `get_pre_info_detail()` - 预处理列表/详情
    - `add_pre_info()` / `edit_pre_info()` / `delete_pre_info()` - 预处理 CRUD
    - `test_pre_code()` - 测试预处理代码

### OpenAPI 使用示例

```python
from scripts.pushplus_openapi import (
    get_access_key,
    list_messages,
    get_user_info,
    list_tokens
)

# 1. 获取 AccessKey（有效期2小时）
result = get_access_key(
    user_token="your_user_token",
    secret_key="your_secret_key"
)
access_key = result["data"]["accessKey"]

# 2. 使用 AccessKey 调用其他接口
messages = list_messages(access_key, current=1, page_size=20)
user_info = get_user_info(access_key)
tokens = list_tokens(access_key)
```

## 更多资源

- 完整 API 文档：[PushPlus 文档中心](https://www.pushplus.plus/doc/)
- 在线测试：[Apifox 接口文档](https://pushplus.apifox.cn/)
- 官网：[www.pushplus.plus](https://www.pushplus.plus)
