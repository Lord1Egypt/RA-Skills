# 短信任务列表 API 参考

## python脚本参数
- `--page_no`：页码（必填，默认1）
- `--page_size`：页大小（必填，默认10）
- `--start_time`：开始时间（非必填，秒级时间戳）
- `--end_time`：结束时间（非必填，秒级时间戳）
- `--status`：发送状态（非必填，0-待发送 1-发送中 2-发送完成）
- `--api_key`：API密钥（可选，默认从环境变量获取）

## 响应数据

### 分页信息
- total：总记录数
- pageNo：当前页码
- pageSize：页大小
- list：任务列表

### 任务信息
- id：任务ID
- name：任务名称
- channelType：渠道类型（0普通，1双向）
- tos：收件人（JSON数组字符串）
- numb：数量
- numbSend：发送数量
- numbSuccess：成功数量
- numbFail：失败数量
- status：状态（0-待发送 1-发送中 2-发送完成）
- priceTotal：实际扣费（单位：分钱(RMB)）
- priceRebate：返回金额（单位：分钱(RMB)）
- priceReal：预扣费（单位：分钱(RMB)）
- content：短信内容
- sendTime：发送时间（秒级时间戳）