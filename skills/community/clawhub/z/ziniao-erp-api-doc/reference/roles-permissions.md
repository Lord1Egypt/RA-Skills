# 角色和权限管理接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅角色增改查、权限列表、用户角色调整接口的详细参数时加载。

所有接口方法均为 POST。

---

## ERP-添加角色

- **路径**：`/superbrowser/rest/v1/erp/per/role/add`　**权限点**：ERP-角色添加、修改权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| roleName | 角色名称 | 是 | string |
| identityId | 角色身份id（1管理员/2普通成员/3超级管理员） | 是 | number |
| desc | 描述 | 否 | string |
| permissionIds | 权限id列表 | 是 | number[] |

**响应**：ret / status / msg

---

## ERP-修改角色

- **路径**：`/superbrowser/rest/v1/erp/per/role/edit`　**权限点**：ERP-角色添加、修改权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| roleId | 角色id | 是 | string |
| roleName | 角色名称 | 是 | string |
| identityId | 角色身份id | 是 | number |
| desc | 描述 | 否 | string |
| permissionIds | 权限id列表 | 是 | number[] |

**响应**：ret / status / msg

---

## ERP-角色列表查询

- **路径**：`/superbrowser/rest/v1/erp/per/role/list`　**权限点**：ERP-角色列表查询

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| page | 页码 | 否 | number |
| limit | 每页条数 | 否 | number |
| filterKeyword | 搜索关键字 | 否 | string |

**响应 data**：含角色信息 id、name、desc、identityType(1管理/2员工/3超管)、allPermission、users[{userId,name,username}]、permissions[{id,name,groupId,groupName,dependOn[],requiredBy[]}]。另有 count。

---

## ERP-角色详情

- **路径**：`/superbrowser/rest/v1/erp/per/role/detail`　**权限点**：ERP-角色详情

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| roleId | 角色id | 是 | number |

**响应 data**：含 id、companyId、name、desc、permissionList[{id,name,groupId,groupName}] (均 string)。

---

## ERP-权限列表

- **路径**：`/superbrowser/rest/v1/erp/per/permission/list`　**权限点**：ERP-权限列表

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| identityId | 角色身份id（1管理员/2普通成员/3超级管理员） | 是 | number |

**响应 data**：数组，每项含 id(number)、name(string)、desc(string)、order(number)、groupId(number)、groupName(string)、groupOrder(number)、dependOn(number[])、requiredBy(number[])。

---

## ERP-调整角色

- **路径**：`/superbrowser/rest/v1/erp/staff/change/role`　**权限点**：ERP-角色添加、修改权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| roleId | 角色id | 是 | number |
| staffIds | 用户id列表 | 是 | number[] |

**响应**：ret / status / msg

---

## ERP-用户角色列表

- **路径**：`/superbrowser/rest/v1/erp/staff/role/list`　**权限点**：ERP-角色列表查询

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| staffId | 用户id | 是 | number |

**响应 data**：对象含 roleList 数组，每项含 id(string)、name(string)。
