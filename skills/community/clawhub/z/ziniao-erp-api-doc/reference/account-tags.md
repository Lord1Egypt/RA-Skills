# 账号标签管理接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅标签的添加、删除、重命名、绑定、解绑、替换、移除、清空、列表接口时加载。

所有标签接口**权限点**均为 **账号标签管理权限**。标签操作路径统一为 `/superbrowser/rest/v1/store-tag/{action}`，方法均为 POST。每个账号最多绑定 5 个标签。

**操作模式**：绑定/解绑为增量操作；替换为全量覆盖；清空移除所有标签。

---

## 添加账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/add`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 否 | string |
| userId | 用户id | 否 | string |
| tagName | 标签名称 | 否 | string |

**响应 data**：对象，含 tag_id(string)。

---

## 删除账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/delete`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 否 | string |
| tagIds | 标签id列表 | 否 | string[] |
| userId | 用户id | 否 | string |

**响应**：ret / msg

---

## 重命名账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/rename`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 否 | string |
| tid | 标签id | 否 | string |
| userId | 用户id | 否 | string |
| name | 新标签名称 | 否 | string |

**响应**：ret / status / msg

---

## 绑定账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/bind`（增量追加）

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 否 | string |
| storeIds | 账号id列表 | 否 | string[] |
| tagIds | 标签id列表 | 否 | string[] |
| userId | 用户id | 否 | string |

**响应**：ret / msg

---

## 解绑账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/unbind`（增量移除）

请求参数同「绑定账号标签」。**响应**：ret / status / msg

---

## 替换账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/replace`（全量覆盖）

请求参数同「绑定账号标签」。**响应**：ret / msg / status

---

## 移除账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/remove`

请求参数同「绑定账号标签」。**响应**：ret / msg / status

---

## 清空账号标签

- **路径**：`/superbrowser/rest/v1/store-tag/clear`（移除账号所有标签）

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 否 | string |
| storeIds | 账号id列表 | 否 | string[] |
| userId | 用户id | 否 | string |

**响应**：ret / msg

---

## 账号的标签列表

- **路径**：`/superbrowser/rest/v1/store-tag/list`

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | string |
| storeId | 店铺id | 是 | string |
| userId | 用户id | 是 | string |
| withSystem | 1带系统标签 0不带（默认0） | 否 | string |

**响应 data**：含 id(string)、name(string)、is_system(string)、store_count(string)。
