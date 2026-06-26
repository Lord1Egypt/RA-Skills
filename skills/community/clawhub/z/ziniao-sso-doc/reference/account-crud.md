# 企业信息与员工/账号查询接口

> 本文件是 ziniao-sso-doc 的 Level 2 参考文档。
> 仅在需要查阅企业信息、员工查询或账号查询接口的详细参数时加载。

> **响应说明**：以下各接口的"响应参数"均为业务层字段，实际位于网关响应的 `data` 内部。完整响应结构见 `api-guide.md` 公共响应参数。

## 获取当前自建应用的公司信息

### 基本信息

| 项目 | 值 |
|------|------|
| 路径 | `/app/builtin/company` |
| 方法 | GET |
| Content-Type | application/json |

### 请求 Headers

| 参数名称 | 参数值 | 是否必须 |
|----------|--------|----------|
| Content-Type | application/json | true |
| Authorization | Bearer {API_Key} | true |

### 请求 Body

无。

### 响应参数

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| companyId | 企业 ID（固定值，获取一次后复用） | integer |

### 请求示例

```bash
curl --location 'https://sbappstoreapi.ziniao.com/openapi-router/app/builtin/company' \
--header 'Authorization: Bearer {API_Key}'
```

### 响应示例

```json
{
  "companyId": 15393571083459
}
```

> companyId 为固定值，也可在开放平台首页右侧直接获取。

---

## ERP-员工查询

### 基本信息

| 项目 | 值 |
|------|------|
| 路径 | `/superbrowser/rest/v1/erp/staff/list` |
| 方法 | POST |
| Content-Type | application/json |

### 请求 Headers

| 参数名称 | 参数值 | 是否必须 |
|----------|--------|----------|
| Content-Type | application/json | true |
| Authorization | Bearer {API_Key} | true |

### 请求 Body

| 参数名称 | 参数说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| companyId | 公司 ID | true | number |
| page | 页码 | true | number |
| limit | 每页条数 | true | number |
| username | 用户账号 | false | string |
| name | 用户真实姓名 | false | string |
| departmentIds | 部门 ID 数组 | false | array\<number\> |
| level | 角色类型：0=Boss，1=经理，2=员工，3=超级管理员 | false | string |
| delflag | 删除标志：0=正常，1=禁用，2=删除（不传返回全部） | false | string |
| isAccurate | 查询模式：0=模糊查询，1=精确查询（默认 0） | false | number |

### 响应参数

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| ret | 状态码，0=成功 | number |
| status | success / faile | string |
| data | 员工列表 | array |
| data[].username | 用户名 | string |
| data[].userId | 用户 ID | number |
| data[].name | 联系人姓名 | string |
| data[].level | 角色类型：0=Boss，1=经理，2=员工，3=超级管理员 | string |
| data[].mobile | 手机号 | string |
| data[].delflag | 状态：0=正常，1=禁用，2=删除 | string |
| data[].authPhone | 登录手机号 | string |
| msg | 错误信息 | string |
| count | 总条数 | string |

### 请求示例

```bash
curl --location 'https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/staff/list' \
--header 'Authorization: Bearer {API_Key}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "companyId": "15393571083459",
  "page": "1",
  "limit": "10",
  "level": "",
  "isAccurate": "",
  "departmentIds": [],
  "delflag": "",
  "name": "",
  "username": ""
}'
```

---

## ERP-账号列表查询

### 基本信息

| 项目 | 值 |
|------|------|
| 路径 | `/superbrowser/rest/v1/erp/store/list` |
| 方法 | POST |
| Content-Type | application/json |

### 请求 Headers

| 参数名称 | 参数值 | 是否必须 |
|----------|--------|----------|
| Content-Type | application/json | true |
| Authorization | Bearer {API_Key} | true |

### 请求 Body

| 参数名称 | 参数说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| companyId | 公司 ID | true | number |
| storeName | 账号名称 | false | string |
| ip | 设备 IP | false | string |
| page | 页码 | false | number |
| limit | 每页条数（私有化账号建议传 20） | false | number |

### 响应参数

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| ret | 状态码，0=成功 | number |
| status | success / faile | string |
| data | 账号列表 | array |
| data[].id | 账号 ID（即 storeId） | number |
| data[].ip | 设备 IP | string |
| data[].lastuserId | 最后登录用户 ID | number |
| data[].lastusetime | 最后登录时间 | string |
| data[].name | 账号名 | string |
| data[].platform | 账号所属平台（如"美国亚马逊"） | string |
| data[].proxyId | 设备 ID | string |
| data[].siteId | 平台 ID | string |
| data[].username | 平台登录账号 | string |
| data[].createtime | 账号创建时间 | string |
| data[].siteName | 站点名称 | string |
| data[].packageName | 套餐名称 | string |
| data[].platformName | 平台名称 | string |
| msg | 错误信息 | string |
| count | 总条数 | string |

### 请求示例

```bash
curl --location 'https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/store/list' \
--header 'Authorization: Bearer {API_Key}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "companyId": "15393571083459",
  "storeName": "",
  "ip": "",
  "page": "1",
  "limit": "10"
}'
```

---

## ERP-查询某用户有权限的账号列表

### 基本信息

| 项目 | 值 |
|------|------|
| 路径 | `/superbrowser/rest/v1/erp/user/stores` |
| 方法 | POST |
| Content-Type | application/json |

### 请求 Headers

| 参数名称 | 参数值 | 是否必须 |
|----------|--------|----------|
| Content-Type | application/json | true |
| Authorization | Bearer {API_Key} | true |

### 请求 Body

| 参数名称 | 参数说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| companyId | 公司 ID | true | number |
| userId | 用户 ID | true | number |
| storeName | 账号名称 | false | string |
| isAccurate | 查询模式：0=模糊，1=精确（默认精确） | false | number |
| page | 页码 | false | number |
| limit | 每页条数 | false | number |

### 响应参数

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| ret | 状态码，0=成功 | number |
| status | success / faile | string |
| data | 账号列表 | array |
| data[].id | 账号 ID（即 storeId） | number |
| data[].ipId | 设备 ID | number |
| data[].ip | 设备 IP | string |
| data[].platform | 账号所属平台 | string |
| data[].name | 账号名 | string |
| data[].lastUserId | 最后登录用户 ID | string |
| data[].lastUserName | 最后登录用户姓名 | string |
| data[].lastOpenUsername | 最后登录用户名称 | string |
| data[].lastUsetime | 最后登录时间 | string |
| data[].ipExpiryTime | 设备到期时间 | string |
| data[].tags | 账号标签列表 | array\<string\> |
| data[].regionInfo | 套餐信息 | string |
| data[].platformCategory | 平台类目 | string |
| data[].userName | 登录凭证 | string |
| msg | 错误信息 | string |
| count | 总条数 | number |

### 请求示例

```bash
curl --location 'https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/user/stores' \
--header 'Authorization: Bearer {API_Key}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "companyId": "15393571083459",
  "userId": "15393571087094",
  "storeName": "",
  "isAccurate": "",
  "page": "1",
  "limit": "10"
}'
```
