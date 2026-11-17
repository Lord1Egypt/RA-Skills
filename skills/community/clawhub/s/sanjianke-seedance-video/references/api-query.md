# 查询任务 · query

> a7w 插件 `seedance` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/seedance/query`

## 查询服务任务（可选）

`GET /api/v1/tasks/{task_id}`

直接查询 maplego 网关任务状态；不计费或按 0 点固定价。
常规集成更推荐使用开放平台统一任务接口：`GET /api/v1/tasks/{task_id}`（使用本平台的 task_id）。

## 参数（平台 schema 原文）

```json
{
  "task_id": {
    "type": "string",
    "example": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "description": "上游返回的任务 ID（与创建接口响应 data.id 一致）。也可使用查询参数 id。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
