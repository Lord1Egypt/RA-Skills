# 邮件任务明细列表 API 参考

## python脚本参数
- `--task_id`：任务ID（必填）
- `--page_no`：页码（必填，默认1）
- `--page_size`：页大小（必填，默认10）
- `--start_time`：开始时间（非必填，秒级时间戳）
- `--end_time`：结束时间（非必填，秒级时间戳）
- `--status`：发送状态（非必填，1发送中 2发送成功 3发送失败 4对方已读）

## 响应数据

### 分页信息
- total：总记录数
- pageNo：当前页码
- pageSize：页大小
- list：明细列表

### 明细信息
- id：明细ID
- taskId：任务ID
- email：收件人邮箱
- numbSend：发送数
- numbSuccess：成功数
- numbFail：失败数
- numbOpen：打开数
- numbClick：点击数
- status：状态（1发送中 2发送成功 3发送失败 4对方已读）
- retryStatus：重试状态
- subject：邮件主题
- sendTime：发送时间（秒级时间戳）