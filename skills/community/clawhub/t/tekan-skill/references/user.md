# User 模块

查询积分余额（tekan-video 配额）和查看权益消费记录。

## 使用场景

- 在运行生成任务前，确认积分余额是否充足。
- 在运行任务后，查看使用记录和费用。

## API 端点

| 端点 | 方法 | 说明 |
|----------|--------|-------------|
| `/user/benefit/tekan-video/quota` | GET | 查询积分余额（返回数字） |
| `/user/benefit/list` | POST | 查询权益消费记录（分页） |

## 用法

```bash
python {baseDir}/scripts/user.py <command> [options]
```

## 命令

### `credit` — 查询余额

调用 `GET /user/benefit/tekan-video/quota`。返回当前 tekan-video 积分配额（数字）。

```bash
python {baseDir}/scripts/user.py credit
```

输出：

```
Credit balance: 1000
```

配合 `--json`：

```bash
python {baseDir}/scripts/user.py credit --json
```

### `logs` — 权益消费记录

调用 `POST /user/benefit/list`，传入 JSON 请求体。支持按权益类型、权益 ID、权益组 ID 和时间范围筛选。

```bash
python {baseDir}/scripts/user.py logs
```

带筛选条件：

```bash
python {baseDir}/scripts/user.py logs \
  --type video_avatar \
  --benefit-ids 1,2,3 \
  --benefit-group-ids 10,20 \
  --start "2024-01-01 00:00:00" \
  --end "2024-12-31 23:59:59" \
  --page 1 \
  --size 50
```

## 选项

### 全局

| 选项 | 说明 |
|--------|-------------|
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制状态消息 |

### `logs`

| 选项 | 说明 |
|--------|-------------|
| `--type TYPE` | 按权益类型筛选 |
| `--benefit-ids IDS` | 按权益 ID 筛选，逗号分隔 |
| `--benefit-group-ids IDS` | 按权益组 ID 筛选，逗号分隔 |
| `--start TIME` | 开始时间（`yyyy-MM-dd HH:mm:ss`） |
| `--end TIME` | 结束时间（`yyyy-MM-dd HH:mm:ss`） |
| `--page N` | 页码（默认：1） |
| `--size N` | 每页条数（默认：20） |
