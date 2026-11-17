# 上传素材 · createAsset

> a7w 插件 `seedance` 的接口 `createAsset` · 平台官方文档

---

`POST /api/v1/apps/seedance/createAsset`

## 上传素材（CreateAsset）

`POST /api/v1/apps/seedance/createAsset`

Content-Type: `multipart/form-data`

上游会异步处理素材，调用 `getAsset` 查询 `Status` 为 `Active` 后即可在创建任务中以 `asset://<ASSET_ID>` 引用。

## 参数（平台 schema 原文）

```json
{
  "URL": {
    "type": "string",
    "example": "https://your-domain.com/uploads/image.png",
    "required": "1",
    "description": "素材公网可访问 URL；将由上游拉取并入库"
  },
  "Name": {
    "type": "string",
    "description": "素材名称，上限 64 字符"
  },
  "GroupId": {
    "type": "string",
    "example": "group-20260402173639-97brg",
    "required": "1",
    "description": "Asset 所属的 Asset Group Id（来自 createGroup 返回的 Result.Id）"
  },
  "AssetType": {
    "type": "string",
    "example": "Image",
    "options": "Image / Video / Audio",
    "required": "1",
    "description": "素材类型：Image / Video / Audio"
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
