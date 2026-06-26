# 部门员工管理接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅部门增删改查移动、员工新增/修改/查询/启禁用、部门变更接口时加载。

所有接口方法均为 POST。

---

## ERP-部门查询

- **路径**：`/superbrowser/rest/v1/erp/department/list`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |

**响应 data**：数组，每项含 id(number)、name(string)、hierarchy(number 层级)、parentId(number)、ordering(number)。另有 count。

---

## ERP-部门新增

- **路径**：`/superbrowser/rest/v1/erp/department/add`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| name | 部门名称 | 是 | string |
| hierarchy | 部门级别 | 是 | string |
| parentId | 父级部门id | 是 | string |

**响应 data**：含 id(string 部门id)。

---

## ERP-部门修改

- **路径**：`/superbrowser/rest/v1/erp/department/update`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| id | 部门id | 是 | number |
| name | 部门新名称 | 否 | string |
| parentId | 父部门id | 否 | number |

**响应**：ret / status / msg

---

## ERP-部门删除

- **路径**：`/superbrowser/rest/v1/erp/department/delete`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | string |
| id | 部门id | 是 | string |

**响应**：ret / status / msg

---

## ERP-部门移动

- **路径**：`/superbrowser/rest/v1/erp/department/order`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| parentId | 父部门id | 是 | string |
| order | 更新后的部门顺序（部门id数组） | 是 | string[] |

**响应**：ret / status / msg

---

## ERP-员工查询

- **路径**：`/superbrowser/rest/v1/erp/staff/list`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| page | 页码 | 是 | number |
| limit | 每页条数 | 是 | number |
| username | 用户账号 | 否 | string |
| name | 真实姓名 | 否 | string |
| departmentIds | 部门id数组 | 否 | number[] |
| level | 角色类型（0boss/1经理/2员工/3超管） | 否 | string |
| delflag | 0正常 1禁用 2删除（不传全部） | 否 | string |
| isAccurate | 0模糊 1精确（默认0） | 否 | number |

**响应 data**：含 username、userId、name、level、mobile、delflag、authPhone (均 string)。另有 count。

---

## ERP-员工新增v2

- **路径**：`/superbrowser/rest/v2/erp/staff/add`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | string |
| nickname | 用户账号 | 是 | string |
| name | 真实姓名 | 是 | string |
| password | 密码 | 是 | string |
| mobile | 手机号 | 否 | string |
| departmentIds | 部门id数组 | 是 | string[] |
| roleId | 角色id | 是 | number |
| authDevide | 设备授权方式（1/2/3/4） | 是 | number |
| isUpdatePersonInfo | 1允许修改个人信息 0不允许 | 是 | number |
| isLimitLogin | 0否 1是 | 是 | number |
| isTwoStepVerify | 0否 1是 | 是 | number |
| authClient | 登录终端控制对象 | 是 | object |
| authClient.allowLoginWindows | 1允许 0不允许 | 是 | string |
| authClient.allowLoginMac | 1允许 0不允许 | 是 | string |
| authClient.allowLoginAndroid | 1允许 0不允许 | 是 | string |
| authClient.allowLoginWeb | 1允许 0不允许 | 是 | string |
| authClient.allowLoginIos | 1允许 0不允许 | 是 | string |
| authClient.allowLoginMiniprog | 1允许 0不允许 | 是 | string |
| authClient.allowLoginLinux | 1允许 0不允许 | 否 | string |
| loginLimitStartTime | HH:mm（分钟仅00或30） | 否 | string |
| loginLimitEndTime | HH:mm | 否 | string |
| loginLimitStartDate | yyyy-MM-dd | 否 | string |
| loginLimitEndDate | yyyy-MM-dd | 否 | string |
| enablePhoneLogin | 0否 1是 | 否 | number |

**响应**：含 id(用户id)、password(string)。

---

## ERP-员工修改v2

- **路径**：`/superbrowser/rest/v2/erp/staff/modify`　**权限点**：ERP-部门与员工接口

参数结构与「员工新增v2」基本一致，差异：
- 新增 `id`(string, 必须) — 用户id
- 多数字段变为非必须（不传不更新）
- 新增 `isResetAuthPhone`(number) — 1重置登录手机号 0不重置
- `areaCode` 和 `authPhone` 已废弃

**响应**：ret / status / msg

---

## ERP-员工启用禁用接口

- **路径**：`/superbrowser/rest/v1/erp/staff/status`　**权限点**：ERP-部门与员工接口

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| staffIds | 用户id数组 | 是 | string[] |
| status | 0启用 1禁用 2删除 | 是 | string |

**响应**：ret / status / msg

---

## ERP-用户的部门变更

- **路径**：`/superbrowser/rest/v1/erp/staff/department`　**权限点**：ERP-用户的部门变更

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | string |
| staffIds | 用户id列表 | 是 | number[] |
| departmentIds | 部门id列表 | 是 | number[] |

**响应**：ret / msg / status
