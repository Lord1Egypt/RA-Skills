# 查询图片任务 · query

> a7w 插件 `nano_banana` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/nano_banana/query`

# nano-banana · 查询图片任务

按平台 `task_id` 查询任务状态与图片结果。本接口只读取平台任务，不产生新的扣点。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `nano_banana` |
| API 编码 | `query` |
| 请求方式 | `GET` |
| 请求路径 | `/api/v1/apps/nano_banana/query` |
| 调用模式 | 同步 |
| 是否计费 | 否 |

## 鉴权

```http
GET /api/v1/apps/nano_banana/query?task_id=task_xxxxxxxxxxxx
Authorization: Bearer <YOUR_API_KEY>
```

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `task_id` | string | 是 | 创建图片任务接口返回的平台任务 ID |

## 处理中响应

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "result": {
      "status": "processing"
    },
    "usage": {
      "points_cost": 0,
      "actual_points": 0
    }
  }
}
```

## 完成响应

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "result": {
      "status": "completed",
      "task_id": "task_xxxxxxxxxxxx",
      "image_url": "https://example.com/output.png",
      "actual_points": 24
    },
    "usage": {
      "points_cost": 24,
      "actual_points": 24
    }
  }
}
```

## 失败响应

```json
{
  "code": 0,
  "msg": "任务不存在或不属于当前租户",
  "data": [],
  "show": 1
}
```

任务失败时，接口会返回平台清洗后的错误信息；不会暴露底层服务地址、密钥或原始内部异常。

## 轮询建议

建议每 3 到 5 秒查询一次任务状态。任务成功后响应中会包含 `image_url`、`actual_points` 等字段；如提交时传入 `callback_url`，平台也会在任务终态时主动通知该地址。

## 参数（平台 schema 原文）

```json
{
  "task_id": {
    "type": "string",
    "example": "task_xxxxxxxxxxxx",
    "description": "创建任务后返回的平台任务 ID。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
