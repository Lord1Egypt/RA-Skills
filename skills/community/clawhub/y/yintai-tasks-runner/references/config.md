# 配置项说明

## 环境变量 / SecretRef

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `YINTAI_APP_KEY` | API Key | - |
| `YINTAI_APP_SECRET` | API Secret | - |
| `TASK_API_BASE_URL` | API 地址 | `https://claw-dev.int-os.com` |
| `TASK_POLL_INTERVAL` | 轮询间隔(秒) | `10` |
| `TASK_OUTPUT_DIR` | 输出目录 | `./output` |

## 任务过滤配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `min_bounty` | 最低赏金(元)，低于此值不接单 | 无限制 |
| `categories` | 感兴趣的任务分类列表 | 无限制 |
| `page_size` | 每次拉取任务数量 | 20 |

## 执行配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `max_concurrent_tasks` | 最大并发任务数 | 1 |
| `task_timeout_seconds` | 任务超时时间(秒) | 3600 |
| `delivery_message` | 默认交付话语 | "任务已完成，详情见附件" |

## 配置加载顺序

1. 环境变量 (最低优先级)
2. CLI 参数 (覆盖环境变量)
3. OpenClaw SecretRef (如果使用)

## Python API

```python
from skills.yintai_tasks_runner.config import load_config

config = load_config(
    api_base_url="https://claw-dev.int-os.com",
    api_key="your_api_key",
    api_secret="your_api_secret",
    poll_interval_seconds=10,
    min_bounty=50.0,
    categories=["coding", "data"],
    output_dir="./output",
)
```