# 插件 (Extension) API 文档

## 概述
插件管理相关的API接口。

## API 列表

### 插件首页

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/extension.json` |
| 描述 | 插件首页 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |

---

### 浏览插件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/extension-browse-[type]-[recTotal]-[recPerPage]-[pageID].json` |
| 描述 | 浏览已安装的插件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| type | string | 否 | 插件类型 |
| recTotal | int | 否 | 总记录数 |
| recPerPage | int | 否 | 每页记录数 |
| pageID | int | 否 | 页码 |

---

### 安装插件

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/extension-install-[extensionID].json` |
| 描述 | 安装插件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| extensionID | string | 否 | 插件ID |

---

### 卸载插件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/extension-uninstall-[extensionID]-[confirm].json` |
| 描述 | 卸载插件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| extensionID | string | 否 | 插件ID |
| confirm | string | 否 | 确认 |

---

### 启用插件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/extension-enable-[extensionID].json` |
| 描述 | 启用插件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| extensionID | string | 否 | 插件ID |

---

### 禁用插件

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/extension-disable-[extensionID].json` |
| 描述 | 禁用插件 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| extensionID | string | 否 | 插件ID |

---

### 插件设置

| 属性 | 值 |
|------|-----|
| 方法 | GET/POST |
| 路径 | `/extension-setting-[extensionID].json` |
| 描述 | 插件设置 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| extensionID | string | 否 | 插件ID |

---

### 插件市场

| 属性 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/extension-market.json` |
| 描述 | 插件市场 |

**参数列表**

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| 无参数 | - | - | - |