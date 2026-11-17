# 查询任务 · query

> a7w 插件 `happy_horse` 的接口 `query` · 平台官方文档

---

`POST /api/v1/apps/happy_horse/query`

## 查询任务

`POST /api/v1/apps/happy_horse/query`

按平台 `task_id` 拉取处理状态与结果。接口 **同步调用**，可与异步 submit 配合。
**内测期未放通时，会返回与 submit 一致的内测提示。**

## 参数（平台 schema 原文）

```json
{
  "task_id": {
    "type": "string",
    "example": "task_xxxxxxxxxxxxxxxx",
    "required": true,
    "description": "submit 返回的平台任务 id"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
