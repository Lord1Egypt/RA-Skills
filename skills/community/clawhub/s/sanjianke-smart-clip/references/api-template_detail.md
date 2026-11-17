# 模板详情 · template_detail

> a7w 插件 `smart_clip` 的接口 `template_detail` · 平台官方文档

---

`POST /api/v1/apps/smart_clip/template_detail`

# 智能剪辑 · 模板详情

按模板 ID 获取模板结构详情。接口为同步免费查询。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `smart_clip` |
| API 编码 | `template_detail` |
| 请求方式 | `GET` |
| 请求路径 | `/api/v1/apps/smart_clip/template_detail?id={id}` |
| 调用模式 | 同步 |
| 计费方式 | 免费查询 |

## 请求参数

| 参数 | 位置 | 类型 | 必填 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `id` | query | string | 是 | `67b7ee802b2beb0030cdeaaf` | 模板id |

## 请求示例

```http
GET /api/v1/apps/smart_clip/template_detail?id=67b7ee802b2beb0030cdeaaf
Authorization: Bearer <YOUR_API_KEY>
```

## 成功响应说明

| 字段 | 类型 | 必返 | 说明 |
| --- | --- | --- | --- |
| `code` | string | 是 | 表示本次请求的状态，值为成功状态时表示成功，其他均为失败 |
| `data` | object | 是 | 结果数据 |
| `data.id` | string | 是 | 模板id |
| `data.name` | string | 是 | 模板名称 |
| `data.coverUrl` | string | 是 | 封面url |
| `data.scene` | string | 是 | 应用场景，同模板列表接口的 `scene` |
| `data.videoStructInfo` | object | 是 | 模板结构详情 |
| `data.videoStructInfo.editInfo` | object | 是 | 编辑结构信息 |
| `data.videoStructInfo.editInfo.canvas.width` | integer | 是 | 模板画布尺寸宽 |
| `data.videoStructInfo.editInfo.canvas.height` | integer | 是 | 模板画布尺寸高 |
| `data.videoStructInfo.editInfo.headerLayer` | object | 是 | 标题图层，返回 `{}` 表示没有相关图层 |
| `data.videoStructInfo.editInfo.subtitleLayer` | object | 是 | 字幕图层，返回 `{}` 表示没有相关图层 |
| `data.videoStructInfo.editInfo.ipLayer` | object | 是 | 身份栏图层，返回 `{}` 表示没有相关图层 |
| `data.videoStructInfo.editInfo.figureLayer` | object | 是 | 数字人图层，返回 `{}` 表示没有相关图层 |
| `data.videoStructInfo.editInfo.backgroundLayer` | object | 是 | 背景图层，返回 `{}` 表示没有相关图层 |
| `requestId` | string | 是 | 本次请求的唯一标识id |
| `message` | string | 否 | 错误描述信息，失败时返回 |

## 图层数据结构

| 字段 | 类型 | 必返 | 说明 |
| --- | --- | --- | --- |
| `width` | integer | 是 | 图层宽 |
| `height` | integer | 是 | 图层高 |
| `transform` | object | 否 | 图层位置数据 |
| `transform.anchor` | integer[] | 是 | 锚点，辅助定位，不支持修改 |
| `transform.scalar` | integer[] | 是 | 缩放，单位：%，不支持修改 |
| `transform.position` | integer[] | 是 | 锚点定位 |
| `uri` | string | 否 | 背景资源图片，仅背景图层返回 |

## 参数（平台 schema 原文）

```json
{
  "id": {
    "type": "string",
    "example": "67b7ee802b2beb0030cdeaaf",
    "description": "模板id"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
