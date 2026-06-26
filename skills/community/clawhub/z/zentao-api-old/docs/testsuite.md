# 测试套件 (Testsuite) API 文档

## 概述
测试套件管理相关的API接口。

## API 列表

### 测试套件首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testsuite.json` |
| 描述 | 测试套件首页，跳转到浏览页面 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 浏览测试套件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testsuite-browse-[productID]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览产品下的测试套件列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建测试套件

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testsuite-create-[productID].json` |
| 描述 | 为产品创建测试套件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 查看测试套件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testsuite-view-[suiteID]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 查看测试套件详情及关联的测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| suiteID | int | 否 | 测试套件ID |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 编辑测试套件

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testsuite-edit-[suiteID].json` |
| 描述 | 编辑测试套件信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| suiteID | int | 否 | 测试套件ID |

---

### 删除测试套件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testsuite-delete-[suiteID]-[confirm].json` |
| 描述 | 删除测试套件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| suiteID | int | 否 | 测试套件ID |
| confirm | string | 否 | 确认删除 |

---

### 关联测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testsuite-linkCase-[suiteID]-[param]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 向测试套件中关联测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| suiteID | int | 否 | 测试套件ID |
| param | int | 否 | 参数 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 移除测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testsuite-unlinkCase-[suiteID]-[rowID]-[confirm].json` |
| 描述 | 从测试套件中移除测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| suiteID | int | 否 | 测试套件ID |
| rowID | int | 否 | 行ID |
| confirm | string | 否 | 确认删除 |

---

### 批量移除测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testsuite-batchUnlinkCases-[suiteID].json` |
| 描述 | 批量从测试套件中移除测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| suiteID | int | 否 | 测试套件ID |