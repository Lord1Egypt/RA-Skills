# 邮件任务列表 API 参考

## python脚本参数
- `--page_no`：页码（必填，默认1）
- `--page_size`：页大小（必填，默认10）
- `--start_time`：开始时间（非必填，秒级时间戳）
- `--end_time`：结束时间（非必填，秒级时间戳）
- `--status`：发送状态（非必填，0-待发送 1-发送中 2-发送完成）

## 响应数据

### 分页信息
- total：总记录数
- pageNo：当前页码
- pageSize：页大小
- list：任务列表

### 任务信息
- id：任务ID
- name：任务名称
- sendName：发送名称
- sendEmail：发送邮箱
- replyEmail：回复邮箱
- tos：收件人列表（JSON数组字符串）
- attachments：附件列表（JSON数组字符串）
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