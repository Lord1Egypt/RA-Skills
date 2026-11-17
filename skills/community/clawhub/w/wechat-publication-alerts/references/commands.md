# 命令与渠道

所有命令前缀：`python scripts/publication_alerts.py`。只查询不扣订阅费：options、accounts、events、channels、deliveries、orders、stats、status。分页筛选参数可写 JSON 文件，通过 --params 读取，例如 events 的 `{"page":1,"pageSize":100,"subscriptionId":"订阅ID"}`。

账号识别：`resolve --account gh_xxx --account https://mp.weixin.qq.com/s/短码`。

报价：`quote --account gh_xxx --plan-id 实际套餐ID`。套餐实时读取；按号套餐的标价是每号单价，打包套餐是总价。不要沿用文档中的历史金额。

首次订阅示例（金额和 ID 都须来自本次报价）：

```text
python scripts/publication_alerts.py setup --account gh_xxx --plan-id 套餐ID --channel-id 渠道ID --budget 1.50 --yes --workspace ./提醒工作区
```

不传 channel-id 则只保留站内动态，必须向用户说明没有启用外部通知。多个渠道重复传 --channel-id。`--wait-seconds` 最多 60，默认 20；超时仅结束本次查看，云端继续准备，不能将其视为购买失败。

创建渠道：在本机配置环境变量 `WM_NOTIFICATION_DESTINATION`（邮箱或机器人 HTTPS 地址）、可选 `WM_NOTIFICATION_SECRET`。非敏感参数存到 channel.json：`{"name":"运营群","kind":"feishu","enabled":true}`，再运行 `channel-save --params channel.json --yes`。邮箱 kind=email，企业微信 wecom，钉钉 dingtalk，通用回调 webhook。

更新渠道提供 --id；地址为空表示沿用，但改变地址时不能继承旧签名密钥。密钥不进入参数文件、日志、报告或发布包。确认渠道成功后再将返回 ID 绑定订阅。

测试消息：`channel-test --id 渠道ID --yes`。这是对外发送消息的操作，须有用户针对该接收目标的授权。邮件测试另需 --params 中的 captchaId、captchaCode；使用平台现有验证码页面完成，不尝试绕过。验证码未完成只表示渠道未验证，不伪称发送成功。

单项修改：`update --id 订阅ID --params changes.json` 预览；--yes 执行。changes.json 只填需要变化的设置，例如 `{"includeDigest":false}`。暂停、恢复、取消分别用 pause/resume/cancel，其余字段自动保留。

续费示例：`renew --operation-id renewal-202611 --account gh_xxx --plan-id 套餐ID --budget 1.50 --yes --workspace ./提醒工作区`。未指定的渠道、摘要、自动续费和摘要扣费 Key 自动沿用原设置；不同设置的账号分组续费。明确取消外部通知用 --station-only，关闭摘要或自动续费用 --no-include-digest / --no-auto-renew。

网络结果不明时订阅购买复用原工作区和 operation-id。渠道创建和测试通知不自动重发，先通过 channels/deliveries 核实，避免重复渠道或重复通知。已明确失败的采集请求不会在原任务中无限重试；保留成功数据和错误后，确认范围与费用再建立新任务。

状态口径：monitorStatus 关注监听，deliveries.status 关注投递；lastConfirmedAt 是最近成功确认时间。succeeded 仅表示接收服务接受，不表示用户已读。首次监听只提醒生效后发现的新文；暂停/过期恢复的基线按服务规则重新建立。

当前 Webhook HMAC 验签使用时间戳 + 点号 + 原始 Body；外层 id 是投递 ID，event.id 是发文事件 ID。通用 webhook 的自动重试有限，unknown 不自动重发。完整协议以平台发文提醒“API 接入”文档为准。
