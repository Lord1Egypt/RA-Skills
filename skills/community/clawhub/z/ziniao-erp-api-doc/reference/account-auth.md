# 账号授权管理接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅账号授权新增、删除、查询、清除、授权用户列表接口的详细参数时加载。

---

## ERP-账号授权新增

- **路径**：`/superbrowser/rest/v1/erp/store/auth/add`　**方法**：POST　**权限点**：ERP-账号授权权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeIdList | 账号id列表 | 是 | string[] |
| staffId | 授权用户id | 是 | string |
| isAuthAddtion | 是否授权附加账号（默认授权）0否 1是 | 否 | number |

**响应**：ret / status / msg

---

## ERP-账号授权删除

- **路径**：`/superbrowser/rest/v1/erp/store/auth/delete`　**方法**：POST　**权限点**：ERP-账号授权权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeIdList | 账号id列表 | 是 | string[] |
| staffId | 授权用户id | 是 | string |

**响应**：ret / status / msg

---

## ERP-账号授权查询

- **路径**：`/superbrowser/rest/v1/erp/store/auth/query`　**方法**：POST　**权限点**：ERP-账号查看权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| userId | 用户id | 是 | number |

**响应 data**：数组，每项含 storeId(number)、storeName(string)。

---

## ERP-清除账号授权

- **路径**：`/superbrowser/rest/v1/erp/store/auth/clean`　**方法**：POST　**权限点**：ERP-清除账号授权

> 清除指定账号上的所有授权关系（不指定用户）。

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeIdList | 账号id数组 | 是 | string[] |

**响应**：ret / msg

---

## ERP-账号授权用户列表查询

- **路径**：`/superbrowser/rest/v1/erp/store/user/list`　**方法**：POST　**权限点**：ERP-账号查看权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeIdList | 账号id列表 | 否 | string[] |
| page | 页码 | 否 | string |
| limit | 每页条数 | 否 | string |

**响应 data**：数组，每项含 storeId(number)、userId(number)、username(string)。另有 count。
