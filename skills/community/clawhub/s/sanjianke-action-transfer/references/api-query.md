# 查询任务 · query

> a7w 插件 `action_transfer` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/action_transfer/query`

# 动作迁移 · 查询任务

根据提交接口返回的 `task_id` 查询动作迁移任务状态、生成结果与计费信息。查询接口不重复计费。

## 接口地址

```http
POST /api/v1/apps/action_transfer/query
```

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `task_id` | string | 是 | 提交任务接口返回的平台任务 ID，例如 `task_xxxxxxxxxxxxxxxx`。 |

## 请求示例

```json
{
  "task_id": "task_xxxxxxxxxxxxxxxx"
}
```

## cURL 示例

```bash
curl -X POST "https://你的域名/api/v1/apps/action_transfer/query" \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task_xxxxxxxxxxxxxxxx"
  }'
```

## 成功响应

处理中：

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "result": {
      "task_id": "task_xxxxxxxxxxxxxxxx",
      "status": "running",
      "duration": 0
    },
    "usage": {
      "points_cost": 0,
      "actual_points": 0
    }
  }
}
```

完成后：

任务完成后，`result` 中会返回生成结果地址。不同上游可能返回 `video_url`、`output_url`、`url` 或 `results` 数组；平台会尽量归一化为可直接访问的视频地址。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "result": {
      "task_id": "task_xxxxxxxxxxxxxxxx",
      "status": "done",
      "duration": 15.695,
      "data": {
        "status": "completed",
        "video_url": "https://example.com/output.mp4",
        "duration": 15.695
      }
    },
    "usage": {
      "points_cost": 31.39,
      "actual_points": 31.39
    }
  }
}
```

| 字段 | 说明 |
| --- | --- |
| `result.status` | 任务状态，常见值：`running`、`done`、`failed`。 |
| `result.duration` | 平台识别到的视频时长，单位秒。 |
| `result.data.video_url` | 生成后的视频地址；实际字段以返回结果为准。 |
| `usage.actual_points` | 任务实际扣费点数。 |

## 失败响应

```json
{
  "code": 0,
  "msg": "任务不存在",
  "data": []
}
```

常见错误：

| HTTP | code | 说明 |
| --- | --- | --- |
| 400 | `invalid_request` | `task_id` 缺失或格式错误。 |
| 401 | `auth_failed` | API Key 缺失或无效。 |
| 403 | `permission_denied` | 当前 API Key 无权查询该任务。 |
| 404 | `not_found` | 任务不存在或不属于当前租户。 |
| 5xx | `server_error` | 服务异常，请稍后重试。 |

## 参数（平台 schema 原文）

```json
{
  "task_id": {
    "type": "string",
    "required": true,
    "description": "平台任务 ID"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
