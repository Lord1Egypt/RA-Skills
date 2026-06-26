# 访问策略 - 网页与分组管理接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅网页增删改查、网页分组管理接口的详细参数时加载。

所有接口**权限点**均为 **ERP-网页访问权限**，方法均为 POST。

---

## ERP-添加网页

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url/add`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| name | 网页名称 | 是 | string |
| groupId | 分组ID | 是 | number |
| desc | 描述 | 否 | string |
| urlPattern | URL | 是 | string |

**响应 data**：含 id(number)。

---

## ERP-编辑网页

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url/edit`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| urlId | 网页ID | 是 | number |
| name | 网页名称 | 是 | string |
| groupId | 分组ID | 是 | number |
| desc | 描述 | 否 | string |
| urlPattern | URL | 是 | string |

**响应**：ret / msg

---

## ERP-删除网页

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url/delete`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| urlIds | 网页ID列表 | 是 | number[] |

**响应**：ret / msg

---

## ERP-网页列表

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url/list`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| search | 搜索关键字 | 否 | string |
| groupIds | 筛选分组ID | 否 | number[] |
| tType | 1系统预置 2自定义 | 否 | number |
| page | 页码 | 是 | number |
| limit | 每页条数 | 是 | number |

**响应 data**：含 list 数组（每项含 id、name、groupId、groupName、tType、urlPattern、description）和 count(number)。

---

## ERP-网页详情

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url/detail`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| urlId | 网页ID | 是 | number |
| urlPattern | 网页url（按url查详情） | 否 | string |

**响应 data**：含 id、name、groupId、groupName、tType、urlPattern、description。

---

## ERP-网页修改分组

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url/change_group`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| groupId | 目标分组ID | 是 | number |
| urlIds | 网页ID列表 | 是 | number[] |

**响应**：ret / msg

---

## ERP-添加网页分组

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url_group/add`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| name | 分组名称 | 是 | string |
| groupIdParent | 父级分组ID（0为顶级，默认0） | 否 | number |

**响应 data**：含 id(number)。

---

## ERP-编辑网页分组

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url_group/edit`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| groupId | 分组ID | 是 | number |
| name | 分组名称 | 是 | string |

**响应**：ret / msg

---

## ERP-删除网页分组

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url_group/delete`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| groupId | 分组ID | 是 | number |

**响应**：ret / msg

---

## ERP-网页分组列表

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule_url_group/list`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| groupIdParent | 父级id（0为顶级，默认0） | 否 | number |
| isAll | 是否返回全部数据（默认false） | 否 | boolean |

**响应 data**：含 list 数组，每项含 id(number)、name(string)、tType(1系统/2自定义)、urlCount(number)、childrenCount(number)、groupIdParent(number)、children(array，isAll=true 时返回，结构同父节点)。
