# 编译 (Compile) API 文档

## 概述
编译管理相关的API接口。

## API 列表

### 浏览Jenkins构建

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-browse-[jobID]-[orderBy]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览指定Jenkins job的构建历史 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| jobID | int | 否 | Jenkins job ID |
| orderBy | string | 否 | 排序方式 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 查看Jenkins构建日志

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-logs-[buildID].json` |
| 描述 | 查看指定Jenkins构建的详细日志 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | Jenkins构建ID |

---

### 触发构建

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/compile-trigger-[jobID].json` |
| 描述 | 触发Jenkins job开始构建 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| jobID | int | 否 | Jenkins job ID |

---

### 获取构建状态

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-status-[buildID].json` |
| 描述 | 获取Jenkins构建的当前状态 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|-----|------|------|
| buildID | int | 否 | Jenkins构建ID |

---

### 取消构建

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-cancel-[buildID].json` |
| 描述 | 取消正在进行的Jenkins构建 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | Jenkins构建ID |

---

### 重试构建

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/compile-retry-[buildID].json` |
| 描述 | 重试失败的Jenkins构建 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | Jenkins构建ID |

---

### 获取构建产物

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-artifacts-[buildID].json` |
| 描述 | 获取Jenkins构建的产物列表 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | Jenkins构建ID |

---

### 下载构建产物

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-download-[buildID]-[artifact].json` |
| 描述 | 下载指定的构建产物 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| buildID | int | 否 | Jenkins构建ID |
| artifact | string | 否 | 产物名称 |

---

### 构建统计

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-statistic-[jobID].json` |
| 描述 | 获取Jenkins job的构建统计信息 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| jobID | int | 否 | Jenkins job ID |

---

### 配置构建参数

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/config-params-[jobID].json` |
| 描述 | 配置Jenkins job的构建参数 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| jobID | int | 否 | Jenkins job ID |

---

### 获取构建历史图表

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/compile-chart-[jobID].json` |
| 描述 | 获取Jenkins构建历史的图表数据 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| jobID | int | 否 | Jenkins job ID |

---

### 构建通知设置

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/compile-notify-[jobID].json` |
| 描述 | 设置构建完成的通知方式 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| jobID | int | 否 | Jenkins job ID |