# 查询换装结果 · query

> a7w 插件 `dressing_diffusion` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/dressing_diffusion/query`

## 查询换装结果

`POST /api/v1/apps/dressing_diffusion/query`

根据 `submit` 返回的 `task_id` 查询换装任务状态和结果图片。
任务处理通常需要 10~30 秒，建议每 3~5 秒轮询一次。

### 返回示例（处理中）
```json
{"task_id": "7xxxxxxxxxxxxxx", "status": "processing"}
```

### 返回示例（完成）
```json
{
  "task_id": "7xxxxxxxxxxxxxx",
  "status": "done",
  "images": ["https://cdn.example.com/result_1.jpg"]
}
```

## 参数（平台 schema 原文）

```json
{
  "task_id": {
    "type": "string",
    "example": "7xxxxxxxxxxxxxx",
    "required": true,
    "description": "提交换装任务时返回的任务 ID"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
