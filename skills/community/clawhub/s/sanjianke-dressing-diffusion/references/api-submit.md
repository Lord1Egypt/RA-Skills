# 提交换装任务 · submit

> a7w 插件 `dressing_diffusion` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/dressing_diffusion/submit`

## 提交换装任务

`POST /api/v1/apps/dressing_diffusion/submit`

上传模特图和服装图，AI 自动生成试穿效果。
支持单件上衣、单件下装、上下套装、连衣裙/全身装四种模式。

### 图片要求
- 格式：JPG / JPEG / PNG，建议 JPG
- 模特图：主体清晰、光线均匀
- 服装图：白底或纯色背景、平铺展示

### 请求示例
```json
{
  "model_url": "https://example.com/model.jpg",
  "garment": {
    "data": [
      {"category": "upper", "url": "https://example.com/shirt.jpg"},
      {"category": "bottom", "url": "https://example.com/pants.jpg"}
    ]
  }
}
```

### 返回示例
```json
{"task_id": "7xxxxxxxxxxxxxx", "status": "pending"}
```

提交成功后使用 `query` 接口轮询结果。

## 参数（平台 schema 原文）

```json
{
  "garment": {
    "type": "object",
    "required": true,
    "description": "服装配置。格式：{\"data\": [{\"category\": \"upper\", \"url\": \"服装图URL\"}, ...]}。category 可选值：upper（上衣）、bottom（下装）、full（连衣裙/全身装）。支持单件或上下套装组合，服装图建议白底平铺。"
  },
  "model_url": {
    "type": "string",
    "example": "https://example.com/model.jpg",
    "required": true,
    "description": "模特图片 URL，建议主体清晰、光线均匀的正面或半身模特图。格式：JPG/PNG"
  }
}
```

## 计费

- 结算口径：按次固定价 0.1 点（租户价）
- 标准价：`fixed_price=0.1000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.10` / `tenant_points_per_1k_input=0.0000`
