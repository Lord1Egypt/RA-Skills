# 提交任务 · submit

> a7w 插件 `flashvsr` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/flashvsr/submit`

## 提交弹性任务

`POST /api/v1/apps/flashvsr/submit`

在平台「弹性部署」对应应用中配置默认策略后，调用本接口创建 `ai_elastic_task`。

返回示例：`{ "task_id": 123, "status": "pending" }`（task_id 为弹性任务主键）

## 参数（平台 schema 原文）

```json
{
  "mode": {
    "type": "string",
    "default": "async_query",
    "required": false,
    "description": "任务模式，默认 async_query"
  },
  "duration": {
    "type": "number",
    "example": 15.695,
    "required": false,
    "description": "输入视频时长，单位秒；未传时平台从 input_url 探测"
  },
  "input_url": {
    "type": "string",
    "example": "https://example.com/low_res_video.mp4",
    "required": true,
    "description": "输入视频文件 URL，待超分辨率处理的视频"
  }
}
```

## 计费

- 结算口径：按用量 3 点/单位；另有固定 0.1 点
- 标准价：`fixed_price=0.0000` / `input_price=3.000000`
- 租户价：`tenant_fixed_points=0.10` / `tenant_points_per_1k_input=0.0000`
