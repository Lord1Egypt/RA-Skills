# 云之家控件类型详解

## 控件类型速查表

| type | 控件名称 | value类型 | 特殊字段 |
|------|---------|----------|---------|
| `textWidget` | 单行文本 | String | - |
| `textAreaWidget` | 多行文本 | String | - |
| `dateWidget` | 日期 | Long (毫秒) | `dateFormat` |
| `dateRangeWidget` | 日期区间 | Long[] | `dateFormat`, `title2` |
| `numberWidget` | 数字 | String | `decimalDigit`, `detailCount` |
| `moneyWidget` | 金额 | String | `decimalDigit`, `displayAmountWords` |
| `arithmeticWidget` | 运算 | String | `expression`, `expressionReality` |
| `radioWidget` | 单选 | String (key) | `options` |
| `checkboxWidget` | 多选 | String[] (keys) | `options` |
| `personSelectWidget` | 人员选择 | String[] (oids) | `personInfo`, `option` |
| `departmentSelectWidget` | 部门选择 | String[] (orgIds) | `deptInfo`, `option` |
| `attachmentWidget` | 附件 | Object[] | `maximum` |
| `imageWidget` | 图片 | String[] (fileIds) | `maximum` |
| `relatedWidget` | 关联审批 | Object[] | `singleSelect` |
| `serialNumWidget` | 流水号 | String | 自动生成 |
| `describeWidget` | 说明文字 | null | 只读 |
| `detailedWidget` | 明细表 | - | `widgetVos`, `widgetValue` |
| `kingGridWidget` | 政务发文 | Object | `parentCodeId` |

---

## 文本类控件

### textWidget (单行文本)

```json
{
  "codeId": "Te_0",
  "type": "textWidget",
  "title": "单行文本框",
  "value": "一行文字",
  "extendFieldMap": { "wordLimit": 200 }
}
```

### textAreaWidget (多行文本)

```json
{
  "codeId": "Ta_0",
  "type": "textAreaWidget",
  "title": "多行文本框",
  "value": "多行\n文字",
  "extendFieldMap": { "wordLimit": 5000 }
}
```

---

## 日期类控件

### dateWidget (日期)

```json
{
  "codeId": "Da_0",
  "type": "dateWidget",
  "title": "日期",
  "dateFormat": "yyyy-MM-dd",
  "value": 1508688000000,
  "extendFieldMap": {}
}
```

**注意事项**:
- `value` 是毫秒级时间戳（数字类型）
- `dateFormat` 指定显示格式

### dateRangeWidget (日期区间)

```json
{
  "codeId": "Dr_1",
  "type": "dateRangeWidget",
  "title": "开始日期",
  "title2": "结束日期",
  "dateFormat": "yyyy-MM-dd",
  "value": [1508688000000, 1508860800000]
}
```

**注意事项**:
- `value` 是包含两个时间戳的数组 [开始时间, 结束时间]
- `title` 是开始日期标题，`title2` 是结束日期标题

---

## 数字类控件

### numberWidget (数字输入框)

```json
{
  "codeId": "Nu_0",
  "type": "numberWidget",
  "title": "数量",
  "value": "10",
  "decimalDigit": 5,
  "detailCount": false,
  "detailCountName": "总数量",
  "extendFieldMap": {}
}
```

**注意事项**:
- `value` 是**字符串**类型，不是数字！
- `decimalDigit` 是小数精度
- `detailCount` 为 true 时表示是明细表合计列

### moneyWidget (金额)

```json
{
  "codeId": "Mo_0",
  "type": "moneyWidget",
  "title": "金额(元)",
  "value": "10.23456",
  "decimalDigit": 5,
  "displayThousand": true,
  "displayAmountWords": true,
  "moneyWords": null,
  "detailCount": false,
  "detailCountName": "总金额(元)"
}
```

**注意事项**:
- `value` 是**字符串**类型
- `displayThousand` 是否千分位显示
- `displayAmountWords` 是否显示大写金额

### arithmeticWidget (运算控件)

```json
{
  "codeId": "Ac_0",
  "type": "arithmeticWidget",
  "title": "运算控件",
  "value": "20.23456",
  "expression": "",
  "expressionReality": [
    { "type": "widget", "value": "Nu_0" },
    { "type": "operator", "value": "+" },
    { "type": "widget", "value": "Mo_0" }
  ],
  "decimalDigit": 5,
  "displayThousand": true,
  "displayAmountWords": true,
  "detailCount": false
}
```

**注意事项**:
- `expressionReality` 定义运算表达式
- `type` 为 `widget` 时引用其他控件，`operator` 为运算符

---

## 选择类控件

### radioWidget (单选框)

```json
{
  "codeId": "Ra_0",
  "type": "radioWidget",
  "title": "单选框",
  "value": "AaBaCcDd",
  "options": [
    { "key": "AaBaCcDd", "value": "选项1", "checked": true, "enable": true },
    { "key": "EeFfGgHh", "value": "选项2", "checked": false, "enable": true }
  ],
  "extendFieldMap": {}
}
```

**核心字段**:
- `value`: 选中的选项的 `key`
- `options`: 所有选项列表
  - `key`: 选项唯一标识
  - `value`: 选项显示文本
  - `checked`: 是否选中（推送时通常全为 false）
  - `enable`: 是否启用

**解析流程**: `value(key)` → `options` 匹配 → `value(显示文本)`

### checkboxWidget (多选框)

```json
{
  "codeId": "Cb_0",
  "type": "checkboxWidget",
  "title": "多选框",
  "value": ["AaBaCcDd", "EeFfGgHh"],
  "options": [
    { "key": "AaBaCcDd", "value": "选项1", "checked": true },
    { "key": "EeFfGgHh", "value": "选项2", "checked": true },
    { "key": "IiJjKkLl", "value": "选项3", "checked": false }
  ]
}
```

**核心字段**:
- `value`: 选中的 key 数组
- `options`: 所有选项

---

## 人员/部门控件

### personSelectWidget (人员选择)

```json
{
  "codeId": "Ps_0",
  "type": "personSelectWidget",
  "title": "人员选择",
  "option": "single",
  "personInfo": [
    {
      "name": "张三",
      "userId": "6358ce8ee4b0f4b16a9bb66f",
      "oid": "637af892e4b054bb75e18764",
      "image": "头像URL",
      "deptLongName": "公司/中心/部门"
    }
  ],
  "value": ["637af892e4b054bb75e18764"]
}
```

**核心字段**:
- `option`: `single`(单选) 或 `multi`(多选)
- `personInfo`: 选中人员的详细信息列表
- `value`: 选中人员的 `oid` 数组

**人员信息字段**:
| 字段 | 说明 |
|-----|------|
| `name` | 姓名 |
| `userId` | 用户ID |
| `oid` | 用户OID（value使用此字段） |
| `image` | 头像URL |
| `deptLongName` | 部门全路径 |
| `phone` | 手机号 |

### departmentSelectWidget (部门选择)

```json
{
  "codeId": "Ds_0",
  "type": "departmentSelectWidget",
  "title": "部门选择",
  "option": "single",
  "deptInfo": [
    {
      "name": "财务部",
      "orgId": "91612e89-ab0e-43df-9c57-8161c6bb99ce",
      "longName": "财务部(财务中心)",
      "realLongName": "公司!中心!部门"
    }
  ],
  "value": ["91612e89-ab0e-43df-9c57-8161c6bb99ce"]
}
```

**核心字段**:
- `option`: `single`(单选) 或 `multi`(多选)
- `deptInfo`: 选中部门的详细信息列表
- `value`: 选中部门的 `orgId` 数组

**部门信息字段**:
| 字段 | 说明 |
|-----|------|
| `name` | 部门名称 |
| `orgId` | 部门ID（value使用此字段） |
| `longName` | 部门路径（带父部门简称） |
| `realLongName` | 部门路径（`!`分隔） |

---

## 文件类控件

### attachmentWidget (附件)

```json
{
  "codeId": "At_0",
  "type": "attachmentWidget",
  "title": "附件",
  "maximum": 12,
  "value": [
    {
      "fileName": "document.pdf",
      "fileSize": "1024",
      "fileExt": "pdf",
      "fileType": "application/pdf",
      "fileId": "xxx"
    }
  ]
}
```

**附件信息字段**:
| 字段 | 说明 |
|-----|------|
| `fileName` | 文件名 |
| `fileSize` | 文件大小（字节） |
| `fileExt` | 文件扩展名 |
| `fileType` | MIME类型 |
| `fileId` | 文件ID |

### imageWidget (图片)

```json
{
  "codeId": "Im_0",
  "type": "imageWidget",
  "title": "图片",
  "maximum": 12,
  "value": ["fileId1", "fileId2"]
}
```

**注意事项**:
- `value` 是图片文件ID的数组
- 比 `attachmentWidget` 简单，只有ID

---

## 特殊控件

### relatedWidget (关联审批)

```json
{
  "codeId": "Rd_0",
  "type": "relatedWidget",
  "title": "关联审批单",
  "singleSelect": false,
  "value": [
    {
      "flowInstId": "xxx",
      "formInstId": "xxx",
      "formDefId": "xxx",
      "formCodeId": "xxx",
      "title": "关联单据标题"
    }
  ]
}
```

**用途**: 获取关联的其他表单实例ID

### serialNumWidget (流水号)

```json
{
  "codeId": "_S_SERIAL",
  "type": "serialNumWidget",
  "title": "流水号",
  "value": "1-20171023-002"
}
```

**注意事项**: 系统自动生成，构建时可不设置

### describeWidget (说明文字)

```json
{
  "codeId": "De_0",
  "type": "describeWidget",
  "title": "说明文字"
}
```

**注意事项**: 只读控件，无 `value` 字段

### kingGridWidget (政务发文)

```json
{
  "codeId": "Kg_0",
  "type": "kingGridWidget",
  "title": "正文",
  "parentCodeId": "",
  "value": {
    "fileId": "xxx",
    "fileName": "xxx.docx",
    "kingGridWidgetFileId": "xxx",
    "pdfFileId": "xxx",
    "updateTime": 1620355780322,
    "historyVersions": []
  }
}
```