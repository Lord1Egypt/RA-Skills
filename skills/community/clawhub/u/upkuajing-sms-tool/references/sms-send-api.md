# 短信发送 API 参考

## python脚本参数
- `--content`：短信内容, 最少10个字符（必填）
- `--phones`：手机号列表（必填，JSON数组格式，如 '["13800138000","13800138001"]'）
- `--channel_type`：发送类型（非必填，0-单向发送 1-双向，支持接收回复消息）
- `--api_key`：API密钥（可选，默认从环境变量获取）

## 响应数据

### 任务信息
- id：任务ID
- name：任务名称
- channelType：渠道类型（0-普通 1-双向）
- tos：收件人（JSON数组字符串）
- numb：总数量
- numbSend：发送数
- numbSuccess：成功数
- numbFail：失败数
- status：状态（1发送中 2发送成功 3失败 4部分成功）
- priceTotal：实际费用（单位：分）
- priceRebate：退回费用（单位：分）
- priceReal：预扣费用（单位：分）
- content：短信内容
- sendTime：发送时间（秒级时间戳）