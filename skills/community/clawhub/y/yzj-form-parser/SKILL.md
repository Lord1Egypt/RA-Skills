---
name: yzj-form-parser
description: 云之家(YunZhijia)表单数据解析与构建技能。用于解析云之家表单JSON结构，支持双向转换：推送数据解析和审批发起数据构建。触发场景：(1) 解析云之家审批推送数据 (2) 构建发起审批接口的表单数据 (3) 理解云之家表单widgetMap和detailMap结构 (4) 处理各类控件：文本、单选、多选、日期、人员、部门、明细表等。
---

# 云之家表单数据解析与构建

## 概述

云之家表单结构在推送数据和发起审批接口中是**完全一致**的，只是数据流向不同：
- **推送解析**: `widgetMap` → 业务字段（读取数据）
- **发起审批**: 业务字段 → `widgetMap`（写入数据）

## 表单整体结构

```json
{
  "formInfo": {
    "widgetMap": { /* 主表单控件 */ },
    "detailMap": { /* 明细表控件 */ }
  },
  "basicInfo": { /* 基本信息 */ }
}
```

### basicInfo 字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| `eventId` | String | 推送事件ID，全局唯一 |
| `formInstId` | String | 表单实例ID |
| `flowInstId` | String | 流程实例ID |
| `formDefId` | String | 表单模版ID |
| `formCodeId` | String | 表单模版codeId |
| `dataType` | Integer | 0=测试数据，1=正式数据 |
| `actionType` | String | reach/agree/submit/delete/abandon/withdraw/disagree |
| `title` | String | 表单标题 |
| `eventTime` | Long | 时间戳(毫秒) |

## 主表单控件 (widgetMap)

`widgetMap` 是一个 Map，key 为控件的 `codeId`。

### 通用字段

每个控件都包含：
- `codeId`: 控件唯一标识
- `title`: 控件标题
- `type`: 控件类型
- `value`: 控件值
- `extendFieldMap`: 扩展配置

---

## 控件类型详解

详见 [references/widget-types.md](references/widget-types.md)

### 1. 文本控件

| type | 说明 | value类型 | 示例 |
|------|------|----------|------|
| `textWidget` | 单行文本 | String | `"一行文字"` |
| `textAreaWidget` | 多行文本 | String | `"多行文字"` |

**解析**: 直接读取 `value`
**构建**: 直接设置 `value`

```java
// 解析
String text = widget.getValue().toString();
// 构建
widget.setValue("文本内容");
```

### 2. 日期控件

| type | 说明 | value类型 |
|------|------|----------|
| `dateWidget` | 日期 | Long (毫秒时间戳) |
| `dateRangeWidget` | 日期区间 | Long[] [开始,结束] |

**解析**: 时间戳转Date
**构建**: Date转时间戳

```java
// 解析
Long timestamp = (Long) widget.getValue();
Date date = new Date(timestamp);

// 构建
widget.setValue(date.getTime());
```

### 3. 数字/金额控件

| type | 说明 | value类型 |
|------|------|----------|
| `numberWidget` | 数字 | String |
| `moneyWidget` | 金额 | String |
| `arithmeticWidget` | 运算 | String |

**注意**: value 是字符串类型！

```java
// 解析
BigDecimal amount = new BigDecimal(widget.getValue().toString());
// 构建
widget.setValue("100.50");
```

### 4. 单选控件 (radioWidget)

**数据结构**:
```json
{
  "type": "radioWidget",
  "value": "AaBaCcDd",  // 选中的key
  "options": [
    { "key": "AaBaCcDd", "value": "选项1", "checked": true },
    { "key": "EeFfGgHh", "value": "选项2", "checked": false }
  ]
}
```

**解析流程**:
```
value(key) → options匹配 → value(显示文本) → 字典匹配 → 业务值
```

**构建流程**:
```
业务值 → 字典匹配 → 显示文本 → options匹配 → key → 设置value
```

### 5. 多选控件 (checkboxWidget)

**数据结构**:
```json
{
  "type": "checkboxWidget",
  "value": ["AaBaCcDd", "EeFfGgHh"],  // 选中的key数组
  "options": [
    { "key": "AaBaCcDd", "value": "选项1", "checked": true },
    { "key": "EeFfGgHh", "value": "选项2", "checked": true }
  ]
}
```

**解析**: value 是 key 数组，遍历匹配
**构建**: 设置 key 数组

### 6. 人员选择控件 (personSelectWidget)

**数据结构**:
```json
{
  "type": "personSelectWidget",
  "option": "single",  // single或multi
  "personInfo": [
    {
      "name": "张三",
      "userId": "xxx",
      "oid": "xxx",
      "image": "头像URL"
    }
  ],
  "value": ["xxx"]  // oid数组
}
```

**解析**: 从 `personInfo` 获取详细信息
**构建**: 设置 `value` 为 oid 数组，同时填充 `personInfo`

### 7. 部门选择控件 (departmentSelectWidget)

**数据结构**:
```json
{
  "type": "departmentSelectWidget",
  "option": "single",
  "deptInfo": [
    {
      "name": "财务部",
      "orgId": "xxx",
      "longName": "公司/中心/部门"
    }
  ],
  "value": ["xxx"]  // orgId数组
}
```

### 8. 附件控件 (attachmentWidget)

详见 [references/file-widget.md](references/file-widget.md)

**数据结构**:
```json
{
  "type": "attachmentWidget",
  "maximum": 200,
  "value": [
    {
      "fileId": "69f06679d0c3b700014ec175",
      "fileName": "document.pdf",
      "fileSize": "482",
      "fileExt": "pdf",
      "fileType": "application/pdf"
    }
  ]
}
```

### 9. 图片控件 (imageWidget)

```json
{
  "type": "imageWidget",
  "maximum": 12,
  "value": ["fileId1", "fileId2"]
}
```

**注意**: 图片控件的 `value` 是文件ID数组。

### 10. 关联审批控件 (relatedWidget)

```json
{
  "type": "relatedWidget",
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

### 11. 流水号控件 (serialNumWidget)

```json
{
  "type": "serialNumWidget",
  "value": "1-20171023-002"  // 系统自动生成
}
```

---

## 明细表控件 (detailMap)

详见 [references/detail-widget.md](references/detail-widget.md)

**数据结构**:
```json
{
  "Dd_0": {
    "codeId": "Dd_0",
    "title": "明细表名称",
    "type": "detailedWidget",
    "buttonName": "添加明细",
    "widgetVos": { /* 列定义 */ },
    "widgetValue": [ /* 行数据 */ ]
  }
}
```

### widgetVos (列定义)

定义明细表中每列的控件结构，与主表控件结构相同：
```json
{
  "Te_1": {
    "codeId": "Te_1",
    "type": "textWidget",
    "title": "姓名"
  }
}
```

### widgetValue (行数据)

数组，每行是一个对象，key 为控件的 codeId：
```json
[
  {
    "_id_": "1",          // 行ID
    "Te_1": "张三",       // 文本值
    "Ra_0": "AaBaCcDd",   // 单选key
    "Da_0": 1508688000000 // 日期时间戳
  }
]
```

---

## 数据解析示例

### 解析推送数据

```java
// 1. 解析主表
Map<String, WidgetInfo> widgetMap = formInfo.getWidgetMap();

// 文本
String title = (String) widgetMap.get("_S_TITLE").getValue();

// 日期
Long timestamp = (Long) widgetMap.get("Da_0").getValue();
Date date = new Date(timestamp);

// 单选
WidgetInfo radio = widgetMap.get("Ra_0");
String key = (String) radio.getValue();
String label = getOptionLabel(radio.getOptions(), key);

// 人员
WidgetInfo person = widgetMap.get("Ps_0");
String name = person.getPersonInfo().get(0).getName();

// 2. 解析明细表
DetailWidget detail = detailMap.get("Dd_0");
Map<String, WidgetInfo> widgetVos = detail.getWidgetVos(); // 列定义
List<Map<String, Object>> rows = detail.getWidgetValue();  // 行数据

for (Map<String, Object> row : rows) {
    String name = (String) row.get("Te_1");
    String radioKey = (String) row.get("Ra_0");
    // 从widgetVos获取options进行匹配
}
```

### 构建发起审批数据

```java
// 1. 构建主表
Map<String, Object> widgetMap = new HashMap<>();

// 文本
widgetMap.put("_S_TITLE", createTextWidget("标题内容"));

// 日期
widgetMap.put("Da_0", createDateWidget(System.currentTimeMillis()));

// 单选
widgetMap.put("Ra_0", createRadioWidget("AaBaCcDd", options));

// 人员
widgetMap.put("Ps_0", createPersonWidget(oid, name));

// 2. 构建明细表
List<Map<String, Object>> rows = new ArrayList<>();
for (Item item : items) {
    Map<String, Object> row = new HashMap<>();
    row.put("Te_1", item.getName());
    row.put("Ra_0", item.getRadioKey());
    rows.add(row);
}
```

---

## 注意事项

1. **数字类型**: `numberWidget`、`moneyWidget` 的 value 是**字符串**
2. **时间戳**: 日期控件的 value 是**毫秒级时间戳**
3. **选项key**: 单选/多选的 value 是选项的 **key**，不是显示文本
4. **明细表行ID**: 每行有 `_id_` 字段，构建时可不设置
5. **数组类型**: 多选、人员、部门、附件的 value 都是数组