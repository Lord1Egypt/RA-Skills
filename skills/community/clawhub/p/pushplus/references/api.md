# PushPlus API 参考文档

> 对应 PushPlus API v1.13 (2026-03-27)，新增 clawbot 渠道

## 接口地址

```
https://www.pushplus.plus/send
```

## 请求方式

- GET, POST, PUT, DELETE
- Content-Type: `application/json`

## 请求参数

| 参数名称 | 是否必填 | 默认值 | 说明 |
|---------|---------|-------|------|
| token | 是 | 无 | 用户 Token 或消息 Token |
| content | 是 | 无 | 具体消息内容 |
| title | 否 | 无 | 消息标题 |
| topic | 否 | 无 | 群组编码（一对多消息） |
| template | 否 | html | 消息模板类型 |
| channel | 否 | wechat | 推送渠道 |
| webhook | 否 | 无 | Webhook 编码 |
| callbackUrl | 否 | 无 | 回调地址 |
| timestamp | 否 | 无 | 时间戳（毫秒） |
| to | 否 | 无 | 好友令牌 |
| pre | 否 | 无 | 预处理编码 |

## 模板类型

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

## 推送渠道

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

## 返回码

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

## 更多资源

- 完整 API 文档：[PushPlus 文档中心](https://www.pushplus.plus/doc/)
- 在线测试：[Apifox 接口文档](https://pushplus.apifox.cn/)
- 官网：[www.pushplus.plus](https://www.pushplus.plus)
