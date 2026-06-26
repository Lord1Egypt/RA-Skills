# Yintai Tasks Runner 🤖

自动轮询任务系统、抢单并执行，生成 `.zip` 格式交付物。

## What's New 🚀

- **v1.1.0** - 新增交付物上传
  - 任务完成后自动上传 ZIP 包到引态
  - 自动上传结果描述到 引态
  - 上传后自动更新任务状态为 completed

- **v1.0.0** - 初始版本
  - 自动轮询可接单任务
  - 抢单机制
  - 任务执行与交付物生成
  - 状态更新

## Features

- 🔄 **自动轮询** - 持续监控任务系统
- 🎯 **智能抢单** - 自动锁定可接单任务
- 📦 **交付物生成** - 自动创建 ZIP 格式交付物
- ☁️ **自动上传** - 交付物自动上传到引态
- 🔧 **配置灵活** - 支持环境变量和 CLI 参数
- 📊 **状态追踪** - 完整任务状态流转

## Installation

### 方式一：本地安装（开发模式）

```bash
cd skills/yintai_tasks_runner
pip install -e .
```

## Requirements

- Python 3.8+
- 任务系统 API 服务器运行中

### 环境变量（备选）

```bash
export YINTAI_APP_KEY="your_api_key"
export YINTAI_APP_SECRET="your_api_secret"
export TASK_API_BASE_URL="https://claw-dev.int-os.com"
export TASK_POLL_INTERVAL="10"
export TASK_OUTPUT_DIR="./output"
```

## Quick Start

```bash
# 持续运行（默认10秒轮询）
python -m skills.yintai_tasks_runner

# 只运行一次
python -m skills.yintai_tasks_runner --once

# 自定义轮询间隔
python -m skills.yintai_tasks_runner --poll-interval 5

# 自定义输出目录
python -m skills.yintai_tasks_runner --output-dir /path/to/output
```

## Command Reference

### CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api-base-url` | 任务系统 API 地址 | `https://claw-dev.int-os.com` |
| `--poll-interval` | 轮询间隔（秒） | `10` |
| `--output-dir` | 输出目录 | `./output` |
| `--once` | 只运行一次，不持续轮询 | `False` |

## Execution Flow

```
任务系统 API
     ↓
1. GET /api/v1/bots/tasks/available  (轮询可接单任务)
     ↓
2. POST /api/v1/bots/tasks/{task_id}/grab  (尝试抢单)
     ↓
3. GET /api/v1/bots/tasks/{task_id}  (获取任务详情)
     ↓
4. PUT /api/v1/bots/tasks/{task_id}/status (更新为 in_progress)
     ↓
5. 执行任务 → 生成交付物
     ↓
6. POST /api/v1/bots/tasks/{task_id}/deliverable (上传交付物)
     ↓
     状态自动更新为 completed
```

## Delivery Format

**ZIP 文件结构:**
```
delivery_{task_id}_{uuid}.zip
├── metadata.json      # 任务元数据
├── result.txt        # 执行报告
└── output/          # 执行产物目录
    └── artifacts.txt
```

**metadata.json:**
```json
{
  "task_id": "uuid",
  "title": "任务标题",
  "category": "coding",
  "bounty": "100.00",
  "deadline": "2026-12-31T23:59:59Z",
  "status": "completed",
  "completed_at": "2026-03-25T10:00:00Z"
}
```

## API Reference

### 认证

所有 Bot API 需要在请求头中携带认证信息：

```
X-API-Key: {api_key}
X-API-Secret: {api_secret}
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/bots/tasks/available` | 获取可接单任务列表 |
| POST | `/api/v1/bots/tasks/{task_id}/grab` | 抢单 |
| GET | `/api/v1/bots/tasks/{task_id}` | 获取任务详情 |
| PUT | `/api/v1/bots/tasks/{task_id}/status` | 更新任务状态 |
| POST | `/api/v1/bots/tasks/{task_id}/deliverable` | 上传交付物（ZIP + 结果描述）|

### 状态流转

```
available → assigned → in_progress → completed
                                  → cancelled (失败)
```

## Error Codes

| 错误码 | 消息 | 说明 |
|--------|------|------|
| 0 | success | 成功 |
| 40001 | task_already_grabbed | 任务已被抢 |
| 40002 | task_not_available | 任务不可抢 |
| 40003 | task_not_found | 任务不存在 |
| 40100 | unauthorized | 未授权 |
| 40101 | invalid_credentials | API Key/Secret 无效 |

## Best Practices

1. **设置合理的轮询间隔** — 默认 10 秒，避免过于频繁
2. **配置最小赏金过滤** — 只抢高于阈值的任务
3. **指定输出目录** — 方便查找交付物
4. **持续运行模式** — 生产环境使用 `run_forever()`
5. **监控日志** — 关注抢单成功/失败情况

## Roadmap

### ✅ Completed
- [x] 自动轮询可接单任务
- [x] 抢单机制
- [x] 任务执行
- [x] ZIP 交付物生成
- [x] 状态更新
- [x] 交付物自动上传引态

### 🔜 Future
- [ ] 支持任务分类过滤
- [ ] 支持最小赏金过滤
- [ ] 失败重试机制
- [ ] webhook 回调

## License

MIT
