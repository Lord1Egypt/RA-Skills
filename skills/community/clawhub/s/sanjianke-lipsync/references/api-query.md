# 查询任务 · query

> a7w 插件 `lipsync` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/lipsync/query`

## 查询任务

`POST /api/v1/apps/lipsync/query`

根据 `submit` 返回的 `task_id` 查询执行状态与结果。

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
