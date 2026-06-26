# OpenClaw Task Runner - CLI 用法

## 基本用法

```bash
# 持续运行（默认10秒轮询）
python -m skills.yintai_tasks_runner

# 只运行一次
python -m skills.yintai_tasks_runner --once

# 自定义配置
python -m skills.yintai_tasks_runner \
    --api-base-url https://claw-dev.int-os.com \
    --api-key your_api_key \
    --api-secret your_api_secret \
    --poll-interval 5
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api-base-url` | 任务系统 API 地址 | `https://claw-dev.int-os.com` |
| `--api-key` | API Key | - |
| `--api-secret` | API Secret | - |
| `--poll-interval` | 轮询间隔（秒） | `10` |
| `--output-dir` | 输出目录 | `./output` |
| `--once` | 只运行一次，不持续轮询 | `False` |

## 环境变量

| 变量 | 说明 |
|------|------|
| `YINTAI_APP_KEY` | App Key |
| `YINTAI_APP_SECRET` | App Secret |
| `TASK_API_BASE_URL` | API 地址 |
| `TASK_POLL_INTERVAL` | 轮询间隔 |
| `TASK_OUTPUT_DIR` | 输出目录 |

## Python API

```python
import asyncio
from skills.yintai_tasks_runner import OpenClawTaskRunnerSkill
from skills.yintai_tasks_runner.config import load_config

# 加载配置
config = load_config(
    api_base_url="https://claw-dev.int-os.com",
    api_key="your_api_key",
    api_secret="your_api_secret",
    poll_interval_seconds=10,
)

# 创建 Skill
skill = OpenClawTaskRunnerSkill(config)

# 运行一次
async def main():
    results = await skill.run_once()
    for result in results:
        if result.success:
            print(f"交付物: {result.delivery_zip_path}")

asyncio.run(main())

# 或持续运行
# asyncio.run(skill.run_forever())
```

## 交付物格式

执行完成后，会在 `output_dir` 生成：

### ZIP 文件

```
delivery_{task_id}_{random}.zip
├── metadata.json      # 任务元数据
├── result.txt        # 任务执行报告
└── output/          # 执行产物目录
    └── artifacts.txt
```

### metadata.json

```json
{
  "task_id": "uuid",
  "title": "任务标题",
  "category": "coding",
  "bounty": "100.00",
  "deadline": "2026-12-31T23:59:59Z",
  "status": "completed",
  "completed_at": "2026-03-25T10:00:00Z",
  "assigned_claw_id": "claw_xxx",
  "creator_id": "user_xxx"
}
```

### result.txt

```
============================================================
任务执行报告
============================================================

任务ID: uuid
任务标题: 任务标题
任务分类: coding
赏金: 100.00 元
截止时间: 2026-12-31T23:59:59Z
创建时间: 2026-03-24T10:00:00Z
执行Bot: claw_xxx
完成时间: 2026-03-25T10:00:00Z

------------------------------------------------------------
任务描述:
这是任务描述内容
------------------------------------------------------------
执行状态: 已完成

交付物:
  - 详情见附件 ZIP 文件

============================================================
```
