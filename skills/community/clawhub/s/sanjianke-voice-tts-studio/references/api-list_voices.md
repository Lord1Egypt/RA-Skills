# 音色列表 · list_voices

> a7w 插件 `voice_tts` 的接口 `list_voices` · 平台官方文档

---

`POST /api/v1/apps/voice_tts/list_voices`

## 音色列表

### 接口地址
`GET /api/v1/apps/voice_tts/list_voices`

### 功能说明
分页查询已创建的语音音色模型，可按名称、语言筛选。

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page_size | integer | 否 | 每页数量，默认20，最大100 |
| page_number | integer | 否 | 页码，从1开始 |
| title | string | 否 | 按名称模糊搜索 |
| self | boolean | 否 | 仅查询自己创建的音色，默认true |
| language | string | 否 | 按语言筛选 |

### 响应示例
```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "total": 5,
    "items": [
      {
        "id": "model_xxxxxxxxxxxx",
        "title": "我的音色",
        "type": "tts",
        "created_at": "2026-04-01T12:00:00Z"
      }
    ]
  }
}
```

## 参数（平台 schema 原文）

```json
{
  "tag": {
    "type": "string",
    "required": "",
    "description": "按标签筛选"
  },
  "title": {
    "type": "string",
    "required": "",
    "description": "按音色名称搜索"
  },
  "sort_by": {
    "type": "string",
    "required": "",
    "description": "排序：score / task_count / created_at"
  },
  "language": {
    "type": "string",
    "required": "",
    "description": "按语言筛选"
  },
  "page_size": {
    "type": "integer",
    "required": "",
    "description": "每页数量，官方默认 10"
  },
  "page_number": {
    "type": "integer",
    "required": "",
    "description": "页码，默认 1"
  },
  "title_language": {
    "type": "string",
    "required": "",
    "description": "按标题语言筛选"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
