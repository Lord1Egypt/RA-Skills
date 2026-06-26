# 访问策略 - 访问规则与账号策略接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅访问规则的新建、编辑、删除、启禁用、详情，以及规则成员/账号设置、账号策略绑定接口时加载。

所有接口**权限点**均为 **ERP-网页访问权限**，方法均为 POST。

---

## ERP-访问规则新建

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/add`

> addIds 与 addNames 可任传其一，都传取并集。

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| name | 规则名称 | 是 | string |
| desc | 规则描述 | 是 | string |
| activeUser | 生效成员（1除boss外所有/2指定成员/3指定部门/4指定角色） | 是 | number |
| userChange | 指定成员对象 | 是 | object |
| userChange.addIds | 新增成员id列表（空值传[]） | 否 | string[] |
| userChange.addNames | 新增成员用户名列表 | 否 | string[] |
| userChange.departmentIds | 指定部门列表 | 否 | number[] |
| userChange.roleIds | 指定角色列表 | 否 | number[] |
| activeAccount | 生效账号（0所有/1指定） | 是 | number |
| accountChange | 指定账号对象 | 是 | object |
| accountChange.addIds | 账号id列表 | 否 | string[] |
| activeRange | 生效范围（1所有网站/2黑名单/3白名单） | 是 | string |
| configs | 配置详情数组 | 是 | array |
| configs[].urlId | 网页ID（activeRange=1时传0） | 是 | number |
| configs[].isAccessible | 是否可访问 | 是 | boolean |
| configs[].isLog | 是否记录日志 | 是 | boolean |
| configs[].functions | 操作控制配置数组 | 是 | array |
| configs[].functions[].function | clipboard/file_upload/file_download/print/console/password/mouse_click/keyboard_input | 是 | string |
| configs[].functions[].permission | 1允许/2允许且记录/3限制且记录/6限制 | 是 | number |
| isSkipRuleConflictCheck | 是否跳过冲突检测 | 是 | boolean |
| effectiveTime | 生效时间（可选） | 否 | object |
| effectiveTime.timeType | 0永久 1限制时间 | 是 | string |
| effectiveTime.startTime | 开始时间戳（秒），永久填0 | 是 | number |
| effectiveTime.endTime | 结束时间戳（秒），永久填0 | 是 | number |
| isAllowRequest | 是否允许申请访问（默认true） | 否 | boolean |
| shareCompanyIds | 合作公司id列表 | 否 | number[] |
| domIds | dom列表 | 否 | number[] |

**响应 data**：含 id(number)。

---

## ERP-访问规则编辑

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/edit`

> addIds/addNames 可任传其一取并集；deleteIds/deleteNames 不能与 add 重复。

参数结构与「规则新建」基本一致，差异：
- 新增 `ruleId`(number, 必须) — 规则ID
- `userChange` / `accountChange` 增加 `deleteIds`(string[]) 和 `deleteNames`(string[]) 用于删除成员
- 无 `activeRange`、`isSkipRuleConflictCheck` 参数

**响应**：ret / msg

---

## ERP-访问规则删除

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/delete`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ruleIds | 规则ID列表 | 是 | number[] |

**响应**：ret / msg

---

## ERP-访问规则启用禁用

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/active`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ruleIds | 规则ID列表 | 是 | number[] |
| isActive | 0禁用 1启用 | 是 | string |

**响应**：ret / msg

---

## ERP-访问规则列表

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/list`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| search | 搜索关键字 | 否 | string |
| activeRange | 1所有网站/2黑名单/3白名单 | 否 | number |
| isActive | 0禁用 1启用 | 否 | number |
| ruleListType | 0全部 1账号可绑定 | 否 | number |
| accountId | 账号id（获取可绑定规则时传） | 否 | number |
| page | 页码 | 是 | number |
| limit | 每页条数 | 是 | number |

**响应 data**：含 list 数组（每项含 id、name、activeUser、activeRange、isActive、description、users[]、roles[]、departments[]、accounts[]、presetType、canChangeUser/Account/Url/Active/canDelete/canCopy）和 count。

---

## ERP-访问规则详情

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/detail`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ruleId | 规则ID | 是 | number |

**响应 data**：含 id、name、description、activeUser、activeRange、activeAccount、users[{id,name,username}]、roles[{id,name}]、departments[{id,name}]、accounts[{id,name}]、configs[{urlId,urlName,groupId,groupName,tType,isAccessible,isLog,urlPattern,functions[{function,permission}]}]、effectiveTime{timeType,startTime,endTime}、shareCompanys[{id,name}]、domList[]、domIds[]。

---

## ERP-访问规则设置生效成员

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/change_user`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ruleId | 规则ID | 是 | number |
| activeUser | 1所有/2指定成员/3指定部门/4指定角色 | 是 | number |
| userChange.addIds | 新增成员id（空传[]） | 是 | string[] |
| userChange.addNames | 新增成员用户名 | 否 | string[] |
| userChange.deleteIds | 删除成员id（空传[]） | 是 | string[] |
| userChange.deleteNames | 删除成员用户名 | 否 | string[] |
| userChange.departmentIds | 指定部门 | 是 | number[] |
| userChange.roleIds | 指定角色 | 是 | number[] |

**响应**：ret / msg

---

## ERP-访问规则设置生效账号

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/change_account`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ruleId | 规则ID | 是 | number |
| activeAccount | 0所有 1指定 | 是 | number |
| accountChange.addIds | 新增账号id | 是 | string[] |
| accountChange.deleteIds | 删除账号id | 是 | string[] |

**响应**：ret / msg

---

## ERP-规则可绑定的账号列表

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/account/bindable_list`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| page | 页码 | 是 | number |
| limit | 每页条数 | 是 | number |
| ruleId | 规则id | 否 | number |
| platformIds | 平台id列表 | 否 | number[] |
| tagIds | 标签id列表 | 否 | number[] |
| accountName | 账号名称 | 否 | string |

**响应 data**：含 list（每项含 id、name、collocationRelation、sitePlatformName、storePlatformId、tags[{id,name}]）、count(number)、bindAccountIds(number[])。

---

## ERP-账号添加访问策略

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/account_ref/add_to_account`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| accountId | 账号id | 是 | string |
| ruleIds | 访问策略id列表 | 是 | number[] |
| isSkipRuleConflictCheck | 是否跳过冲突检测 | 是 | boolean |

**响应**：ret / msg

---

## ERP-账号移除访问策略

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/account_ref/remove_from_account`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| accountId | 账号id | 是 | string |
| ruleIds | 访问策略id列表 | 是 | number[] |

**响应**：ret / msg

---

## ERP-账号绑定的访问策略列表

- **路径**：`/superbrowser/rest/v1/erp/security/access_rule/list/one_account`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| accountId | 账号id | 是 | string |
| page | 页码 | 是 | number |
| limit | 每页条数 | 是 | number |

**响应 data**：含 list 数组（每项含 id、name、activeRange、activeUser、isActive、users[{id,name,username}]、urlCount、isInvalid、canDelete）和 count。
