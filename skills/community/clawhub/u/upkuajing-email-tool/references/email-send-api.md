# 邮件发送 API 参考

## python脚本参数
- `--subject`：邮件主题（必填，最长250字符）
- `--content`：邮件内容（必填）
- `--emails`：收件人邮箱列表（必填，JSON数组格式）
- `--send_name`：发送名称（非必填，默认 service，最长50字符）
- `--email_name`：邮件名（非必填，默认 service，最长50字符）
- `--reply_email`：回复邮箱（非必填）

## 响应数据

### 任务信息
- id：任务ID
- name：任务名称
- sendName：发送名称
- sendEmail：发送邮箱
- replyEmail：回复邮箱
- tos：收件人列表（JSON数组字符串）
- numbTos：收件人总数
- numbSend：已发送数
- numbSuccess：成功数
- numbFail：失败数
- numbOpen：打开数
- numbClick：点击数
- status：状态（0-待发送 1-发送中 2-发送完成）
- priceTotal：总费用（单位：分钱(RMB)）
- priceRebate：退回费用（单位：分钱(RMB)）
- priceReal：实际费用（单位：分钱(RMB)）
- content：邮件内容
- subject：邮件主题