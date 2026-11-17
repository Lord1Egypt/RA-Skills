# 模板列表 · template

> a7w 插件 `smart_clip` 的接口 `template` · 平台官方文档

---

`POST /api/v1/apps/smart_clip/template`

# 智能剪辑 · 模板列表

查询智能剪辑可用模板列表。接口为同步免费查询。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `smart_clip` |
| API 编码 | `template` |
| 请求方式 | `GET` |
| 请求路径 | `/api/v1/apps/smart_clip/template` |
| 调用模式 | 同步 |
| 计费方式 | 免费查询 |

## 请求参数

| 参数 | 位置 | 类型 | 必填 | 默认值 | 可选值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `pageSize` | query | integer | 否 | `10` | - | 每页大小 |
| `sid` | query | string | 否 | - | - | 分页游标，当有值时代表存在下一页，继续查询下一页时需传入该值 |
| `scene` | query | string | 是 | - | `realMan` / `oralMixCutting` / `newsMixCutting` | 模板使用场景；返回的模板只能提交到对应接口 |
| `searchKey` | query | string | 否 | - | `name` / `id` | 搜索字段，`name` 按名称搜索，`id` 按模板 ID 搜索 |
| `searchValue` | query | string | 否 | - | - | 搜索值 |
| `sortBy` | query | string | 否 | `desc` | `desc` / `asc` | 排序方式，`desc` 按上架时间倒序，`asc` 按上架时间正序 |

## scene 枚举

| 值 | 说明 |
| --- | --- |
| `realMan` | 真人口播模板，对应提交接口 `realman_broadcast` |
| `oralMixCutting` | 素材混剪模板，对应提交接口 `broadcast_mixcut` |
| `newsMixCutting` | 新闻混剪模板，对应提交接口 `news_mixcut` |

## 请求示例

```http
GET /api/v1/apps/smart_clip/template?scene=realMan&pageSize=10&sortBy=desc
Authorization: Bearer <YOUR_API_KEY>
```

## 成功响应说明

| 字段 | 类型 | 必返 | 说明 |
| --- | --- | --- | --- |
| `code` | string | 是 | 表示本次请求的状态，值为成功状态时表示成功，其他均为失败 |
| `data` | object | 是 | 结果数据 |
| `data.results` | array | 是 | 模板列表 |
| `data.results[].id` | string | 是 | 模板id |
| `data.results[].name` | string | 是 | 模板名称 |
| `data.results[].coverUrl` | string | 是 | 封面url |
| `data.results[].scene` | string | 是 | 场景，枚举同请求参数 `scene` |
| `data.results[].demoUrl` | string | 是 | 使用该模板生成的视频样片 |
| `data.sid` | string | 否 | 分页游标，当有值时代表存在下一页，继续查询下一页时需传入该值 |
| `message` | string | 否 | 错误描述信息，失败时返回 |

## 参数（平台 schema 原文）

```json
{
  "sid": {
    "type": "string",
    "description": "分页游标，当有值时代表存在下一页，继续查询下一页时需传入该值"
  },
  "scene": {
    "enum": [
      "realMan",
      "oralMixCutting",
      "newsMixCutting"
    ],
    "type": "string",
    "example": "realMan",
    "options": "realMan / oralMixCutting / newsMixCutting",
    "description": "模板使用场景：真人口播 realMan（提交接口 realman_broadcast）、素材混剪 oralMixCutting（提交接口 broadcast_mixcut）、新闻体视频 newsMixCutting（提交接口 news_mixcut）"
  },
  "sortBy": {
    "enum": [
      "desc",
      "asc"
    ],
    "type": "string",
    "default": "desc",
    "example": "desc",
    "options": "desc / asc",
    "description": "排序方式，desc：按上架时间倒序排序，asc：按上架时间正序排序"
  },
  "pageSize": {
    "type": "integer",
    "default": 10,
    "example": 10,
    "description": "每页大小"
  },
  "searchKey": {
    "enum": [
      "name",
      "id"
    ],
    "type": "string",
    "example": "name",
    "options": "name / id",
    "description": "搜索字段"
  },
  "searchValue": {
    "type": "string",
    "example": "口播",
    "description": "搜索值"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
