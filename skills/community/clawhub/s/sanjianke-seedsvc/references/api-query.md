# 查询任务 · query

> a7w 插件 `seedsvc` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/seedsvc/query`

## 查询弹性任务

`POST /api/v1/apps/seedsvc/query`

根据 `submit` 返回的 `task_id` 查询执行状态与结果。

## 参数（平台 schema 原文）

```json
{
  "task_id": {
    "type": "integer",
    "required": "",
    "description": "同 elastic_task_id"
  },
  "elastic_task_id": {
    "type": "integer",
    "required": "",
    "description": "弹性任务 id（与 task_id 二选一）"
  }
}
```

## 计费

- 结算口径：按次固定价 0.1 点（租户价）
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.10` / `tenant_points_per_1k_input=0.0000`
