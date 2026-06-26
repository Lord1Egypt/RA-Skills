# 账号增删改查与状态接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅账号创建、删除、编辑、列表查询、标签列表、缓存清除接口的详细参数时加载。

---

## ERP-创建账号

- **路径**：`/superbrowser/rest/v1/erp/store/create`　**方法**：POST　**权限点**：ERP-创建与删除账号权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeData | 账号数据数组 | 是 | array |
| storeData[].name | 账号名 | 是 | string |
| storeData[].username | 平台登录账号 | 否 | string |
| storeData[].password | 平台登录密码 | 否 | string |
| storeData[].siteId | 站点id | 否 | string |
| storeData[].tagIds | 标签列表（不超过5个） | 否 | number[] |
| proxyId | 设备id | 否 | number |
| enterpriseName | 企业简称 | 否 | string |
| defyWarning | 是否无视风险添加：1是 0否（默认1） | 否 | string |

**响应 data**：数组，每项含 storeId(string)、name(string)、siteId(string)、msg(string)、riskMsgList(string[])

---

## ERP-删除账号

- **路径**：`/superbrowser/rest/v1/erp/store/delete`　**方法**：POST　**权限点**：ERP-创建与删除账号权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeIds | 账号id数组 | 是 | number[] |

**响应**：ret / status / msg

---

## ERP-编辑账号基础信息

- **路径**：`/superbrowser/rest/v1/erp/store/update/base`　**方法**：POST　**权限点**：ERP-编辑账号基础信息

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| id | 账号id | 是 | number |
| name | 账号名（≤64位，不传不更新） | 否 | string |
| siteId | 平台id（不传不更新） | 否 | number |
| tagIds | 标签id列表（不传不更新，传空清空，≤5个） | 否 | number[] |
| defyWarning | 是否无视风险：1是 0否（默认1） | 否 | integer |
| customerUrl | 自定义平台站点url | 否 | string |

**响应**：ret / msg / status

---

## ERP-账号列表查询

- **路径**：`/superbrowser/rest/v1/erp/store/list`　**方法**：POST　**权限点**：ERP-账号查看权限

> 私有化账号建议一次最多查询 20 条。

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeName | 账号名称 | 否 | string |
| ip | 设备ip | 否 | string |
| page | 页码 | 否 | number |
| limit | 每页条数 | 否 | number |

**响应 data**：数组，每项含 id、name、ip、proxyId、siteId、siteName、platform、platformName、username、createtime、lastuserId、lastusetime、packageName (均 string)。另有 count。

---

## ERP-用户的账号列表查询

- **路径**：`/superbrowser/rest/v1/erp/store/list/by/user`　**方法**：POST　**权限点**：ERP-账号查看权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| userId | 用户id | 是 | number |
| storeName | 账号名称 | 否 | string |
| page | 页码 | 否 | number |
| limit | 每页条数 | 否 | number |

**响应 data**：数组，每项含 storeId、storeName、proxyId、ipExpiryTime、platformName (均 string)。另有 count。

---

## ERP-查询某用户有权限的账号列表

- **路径**：`/superbrowser/rest/v1/erp/user/stores`　**方法**：POST　**权限点**：ERP-查询某用户有权限的账号列表

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| userId | 用户id | 是 | number |
| storeName | 账号名称 | 否 | string |
| isAccurate | 0模糊 1精确（默认精确） | 否 | number |
| page | 页码 | 否 | number |
| limit | 每页条数 | 否 | number |

**响应 data**：数组，每项含 id(number)、name、ipId(number)、ip、platform、platformCategory、userName、lastUserId、lastUserName、lastOpenUsername、lastUsetime、ipExpiryTime、tags(string[])、regionInfo。另有 count。

---

## ERP-标签列表

- **路径**：`/superbrowser/rest/v1/erp/tag/list`　**方法**：POST　**权限点**：ERP-标签列表

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |

**响应 data**：对象，含 list 数组，每项含 id(string)、name(string)。

---

## ERP-清除账号缓存

- **路径**：`/superbrowser/rest/v1/erp/store/deletecookie`　**方法**：POST　**权限点**：ERP-清除账号缓存

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| userId | 用户id | 是 | string |
| removeStoreId | 账号id | 是 | number |
| removeType | 1清除所有 2仅保留cookie 3仅保留二步验证状态 | 是 | number |

**响应**：ret / msg / status
