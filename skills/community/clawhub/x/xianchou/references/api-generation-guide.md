# AI 生成指南

本文档说明 `xianchou` CLI 如何通过 `/api/cli` 完成模型发现、生图、轮询和 settle。

## 核心规则

> 模型 ID 必须动态获取，严禁猜测或硬编码。

```bash
xianchou models image --project-id <PROJECT_ID>
```

## 生图流程

1. `GET /api/cli/models/image` 获取模型和默认参数。
2. `POST /api/cli/images/generate` 提交生图任务。
3. `GET /api/cli/tasks/{task_id}` 轮询任务状态。
4. `POST /api/cli/tasks/{task_id}/settle` 结算任务。

CLI 命令：

```bash
xianchou generate image --prompt "描述" --project-id <PROJECT_ID> --poll
```

## 任务状态

| 状态 | 含义 | Agent 行为 |
|------|------|------------|
| `PENDING` | 排队中 | 按 `poll_interval` 继续轮询 |
| `PROGRESS` | 生成中 | 按 `poll_interval` 继续轮询 |
| `SUCCESS` | 成功 | 读取 `image_urls`，然后 settle |
| `FAILURE` | 失败 | 展示 `detail` 和 `error_code` |
| `REVOKED` | 已取消 | 停止轮询 |
| `EXPIRED` | 已过期 | 提示重新提交 |

## 输出字段

`/api/cli/tasks/{task_id}` 返回标准字段：

```json
{
  "success": true,
  "task_id": "xxx",
  "state": "SUCCESS",
  "image_urls": ["https://..."],
  "poll_interval": 3000,
  "detail": ""
}
```

不要依赖 `/run` 的原始结果结构。
