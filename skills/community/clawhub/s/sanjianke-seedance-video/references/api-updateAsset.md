# 更新素材 · updateAsset

> a7w 插件 `seedance` 的接口 `updateAsset` · 平台官方文档

---

`POST /api/v1/apps/seedance/updateAsset`

## 更新素材（UpdateAsset）

`POST /api/v1/apps/seedance/updateAsset`

Content-Type: `multipart/form-data`

## 参数（平台 schema 原文）

```json
{
  "Id": {
    "type": "string",
    "example": "asset-20260402224305-54j64",
    "required": "1",
    "description": "Asset Id"
  },
  "Name": {
    "type": "string",
    "description": "新的素材名称，上限 64 字符"
  },
  "ProjectName": {
    "type": "string",
    "default": "default",
    "description": "项目名称，默认 default"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
