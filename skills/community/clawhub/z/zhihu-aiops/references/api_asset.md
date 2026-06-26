# 资产中心 API 详细参数

## 资产类型管理

### 资产类型列表

**URL**: `/cqt/asset-type/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| typeName | string | 否 | 类型名称(搜索) |

### 创建资产类型

**URL**: `/cqt/asset-type/create`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| typeName | string | 是 | 类型名称 |
| typeCode | string | 是 | 类型编码 |
| description | string | 否 | 描述 |

### 更新资产类型

**URL**: `/cqt/asset-type/update`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 类型ID |
| typeName | string | 否 | 类型名称 |
| typeCode | string | 否 | 类型编码 |
| description | string | 否 | 描述 |

### 删除资产类型

**URL**: `/cqt/asset-type/delete`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 类型ID |

---

## 资产模型管理

### 资产模型列表

**URL**: `/cqt/asset-model/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| modelName | string | 否 | 模型名称(搜索) |

---

## 资产信息管理

### 资产信息列表

**URL**: `/cqt/asset-info/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| assetName | string | 否 | 资产名称(搜索) |
| modelId | int | 否 | 模型ID |

### 创建资产

**URL**: `/cqt/asset-info/create`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| modelId | int | 是 | 模型ID |
| assetName | string | 是 | 资产名称 |
| ... | ... | 否 | 模型定义的其他属性 |

### 更新资产

**URL**: `/cqt/asset-info/update`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 资产ID |
| ... | ... | 否 | 要更新的属性 |

### 删除资产

**URL**: `/cqt/asset-info/delete`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 资产ID |

### 导出导入模板

**URL**: `/cqt/asset-info/export-template`

**请求方式**: POST

**说明**: 下载资产导入模板

### 导入资产

**URL**: `/cqt/asset-info/import/{modelId}`

**请求方式**: POST

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| modelId | int | 模型ID |

### 导出资产

**URL**: `/cqt/asset-info/export`

**请求方式**: POST
