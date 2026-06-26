# 平台/分支 (Branch) API 文档

## 概述
产品平台/分支管理相关的API接口。

## API 列表

### 管理分支

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/branch-manage-[productID].json` |
| 描述 | 管理产品的分支 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 排序分支

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/branch-sort.json` |
| 描述 | 对分支进行排序 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 获取下拉菜单

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/branch-ajaxGetDropMenu-[productID]-[module]-[method]-[extra].json` |
| 描述 | AJAX获取下拉菜单 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| module | string | 否 | 模块 |
| method | string | 否 | 方法 |
| extra | string | 否 | 额外参数 |

---

### 删除分支

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/branch-delete-[branchID]-[confirm].json` |
| 描述 | 删除分支 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| branchID | int | 否 | 分支ID |
| confirm | string | 否 | 确认 |

---

### 获取分支列表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/branch-ajaxGetBranches-[productID]-[oldBranch].json` |
| 描述 | AJAX获取分支列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| oldBranch | int | 否 | 旧分支ID |