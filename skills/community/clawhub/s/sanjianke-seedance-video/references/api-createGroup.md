# 创建素材资产组合 · createGroup

> a7w 插件 `seedance` 的接口 `createGroup` · 平台官方文档

---

`POST /api/v1/apps/seedance/createGroup`

## 创建素材资产组合（Asset Group）

`POST /api/v1/apps/seedance/createGroup`

Content-Type: `multipart/form-data`

同步接口；调用成功后返回上游 `Result.Id`，用于后续上传素材时填入 `GroupId`。

## 参数（平台 schema 原文）

```json
{
  "Name": {
    "type": "string",
    "example": "demo-group",
    "required": "1",
    "description": "Asset Group 名称，上限 64 字符"
  },
  "GroupType": {
    "type": "string",
    "example": "AIGC",
    "options": "AIGC",
    "description": "分组类型；AIGC 表示虚拟人像分组"
  },
  "Description": {
    "type": "string",
    "description": "分组描述，上限 300 字符"
  },
  "ProjectName": {
    "type": "string",
    "default": "default",
    "description": "项目名称，默认 default；非默认项目需填写正确名称"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
