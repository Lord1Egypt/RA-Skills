# 短信任务明细列表 API 参考

## python脚本参数
- `--task_id`：任务ID（必填）
- `--page_no`：页码（必填，默认1）
- `--page_size`：页大小（必填，默认10）
- `--start_time`：开始时间（非必填，秒级时间戳）
- `--end_time`：结束时间（非必填，秒级时间戳）
- `--status`：发送状态（非必填，0-待发送 1-发送中 2-成功 3-失败）
- `--api_key`：API密钥（可选，默认从环境变量获取）

## 响应数据

### 分页信息
- total：总记录数
- pageNo：当前页码
- pageSize：页大小
- list：明细列表

### 明细信息
- id：明细ID
- taskId：任务ID
- phone：手机号
- channelType：渠道类型（0-普通 1-双向）
- status：发送状态（0-待发送 1-发送中 2-成功 3-失败）
- sendTime：发送时间（秒级时间戳）