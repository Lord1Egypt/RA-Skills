# 测试用例 (Testcase) API 文档

## 概述
测试用例管理相关的API接口。

## API 列表

### 测试用例首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase.json` |
| 描述 | 测试用例首页 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 浏览测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase-browse-[productID]-[branch]-[browseType]-[param]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览测试用例列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |
| browseType | string | 否 | 浏览类型 |
| param | - | 否 | 参数 |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 创建测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-create-[productID]-[branch]-[moduleID]-[storyID].json` |
| 描述 | 创建测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |
| branch | int | 否 | 分支ID |
| moduleID | int | 否 | 模块ID |
| storyID | int | 否 | 需求ID |

---

### 编辑测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-edit-[caseID].json` |
| 描述 | 编辑测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| caseID | int | 否 | 测试用例ID |

---

### 查看测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase-view-[caseID]-[version].json` |
| 描述 | 查看测试用例详情 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| caseID | int | 否 | 测试用例ID |
| version | string | 否 | 版本号 |

---

### 删除测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase-delete-[caseID]-[confirm].json` |
| 描述 | 删除测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| caseID | int | 否 | 测试用例ID |
| confirm | string | 否 | 确认删除 |

---

### 批量创建测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-batchCreate-[productID].json` |
| 描述 | 批量创建测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 批量编辑测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-batchEdit.json` |
| 描述 | 批量编辑测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 导入测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-import-[productID].json` |
| 描述 | 从文件导入测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 导出测试用例

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-export-[productID].json` |
| 描述 | 导出测试用例到文件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| productID | int | 否 | 产品ID |

---

### 关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/testcase-linkStory-[caseID]-[storyID].json` |
| 描述 | 关联需求到测试用例 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| caseID | int | 否 | 测试用例ID |
| storyID | int | 否 | 需求ID |

---

### 取消关联需求

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase-unlinkStory-[caseID]-[storyID].json` |
| 描述 | 取消需求与测试用例的关联 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| caseID | int | 否 | 测试用例ID |
| storyID | int | 否 | 需求ID |

---

### 测试用例版本

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase-version-[caseID].json` |
| 描述 | 查看测试用例版本历史 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| caseID | int | 否 | 测试用例ID |

---

### 测试用例模板

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/testcase-template-[type].json` |
| 描述 | 获取测试用例模板 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| type | string | 否 | 模板类型 |