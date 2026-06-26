# 明细表控件详解

## 整体结构

明细表使用 `detailedWidget` 类型，存储在 `detailMap` 中：

```json
{
  "detailMap": {
    "Dd_0": {
      "codeId": "Dd_0",
      "title": "明细表标题",
      "type": "detailedWidget",
      "buttonName": "添加明细",
      "openErpLink": false,
      "advancedMode": false,
      "widgetVos": { /* 列定义 */ },
      "widgetValue": [ /* 行数据 */ ],
      "extendFieldMap": {
        "showSerialNum": false,
        "editRow": true,
        "delRow": true,
        "addRow": true
      }
    }
  }
}
```

## 核心字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| `codeId` | String | 明细表控件ID，如 `Dd_0`, `Dd_1` |
| `title` | String | 明细表标题 |
| `type` | String | 固定为 `detailedWidget` |
| `buttonName` | String | 添加按钮文本 |
| `widgetVos` | Map | 列定义（控件描述） |
| `widgetValue` | Array | 行数据数组 |
| `extendFieldMap` | Object | 扩展配置 |

---

## widgetVos (列定义)

定义明细表中每一列的控件结构，与主表控件结构相同。

**结构**:
```json
{
  "widgetVos": {
    "Te_1": {
      "codeId": "Te_1",
      "type": "textWidget",
      "title": "姓名",
      "value": null
    },
    "Ra_0": {
      "codeId": "Ra_0",
      "type": "radioWidget",
      "title": "性别",
      "options": [
        { "key": "AaBaCcDd", "value": "男" },
        { "key": "EeFfGgHh", "value": "女" }
      ]
    },
    "Da_1": {
      "codeId": "Da_1",
      "type": "dateWidget",
      "title": "入职日期",
      "dateFormat": "yyyy-MM-dd"
    }
  }
}
```

**关键作用**:
1. 定义每列的控件类型
2. 提供 `options` 用于单选/多选的 key→label 转换
3. 解析行数据时需要参考此结构

---

## widgetValue (行数据)

数组，每个元素代表一行数据。

**结构**:
```json
{
  "widgetValue": [
    {
      "_id_": "1",
      "Te_1": "张三",
      "Ra_0": "AaBaCcDd",
      "Da_1": 1508688000000
    },
    {
      "_id_": "2",
      "Te_1": "李四",
      "Ra_0": "EeFfGgHh",
      "Da_1": 1508774400000
    }
  ]
}
```

**行数据字段**:
| 字段 | 说明 |
|-----|------|
| `_id_` | 行ID（系统生成） |
| 其他字段 | key 为控件 codeId，value 为控件值 |

**value 类型规则**:
与主表控件相同：
- 文本: String
- 日期: Long (时间戳)
- 单选: String (key)
- 多选: String[] (keys)
- 数字: String
- 人员: String[] (oids)

---

## 解析明细表数据

### 解析流程

```java
// 1. 获取明细表控件
DetailWidget detailWidget = detailMap.get("Dd_0");

// 2. 获取列定义（包含options）
Map<String, WidgetInfo> widgetVos = detailWidget.getWidgetVos();

// 3. 获取行数据
List<Map<String, Object>> rows = detailWidget.getWidgetValue();

// 4. 遍历解析每行
for (Map<String, Object> row : rows) {
    // 文本字段
    String name = (String) row.get("Te_1");
    
    // 日期字段
    Long date = (Long) row.get("Da_1");
    
    // 单选字段：需要从widgetVos获取options进行转换
    String radioKey = (String) row.get("Ra_0");
    WidgetInfo radioDef = widgetVos.get("Ra_0");
    String label = getOptionLabel(radioDef.getOptions(), radioKey);
}
```

### 单选/多选转换

明细表行数据中只存储 key，需要从 `widgetVos` 获取 options 进行转换：

```java
/**
 * 根据key获取选项显示文本
 */
private String getOptionLabel(List<OptionInfo> options, String key) {
    return options.stream()
        .filter(opt -> key.equals(opt.getKey()))
        .findFirst()
        .map(OptionInfo::getValue)
        .orElse(null);
}

/**
 * 多选：获取多个选项的显示文本
 */
private List<String> getOptionLabels(List<OptionInfo> options, List<String> keys) {
    return keys.stream()
        .map(key -> getOptionLabel(options, key))
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
}
```

---

## 构建明细表数据

### 构建流程

```java
// 1. 构建列定义 (widgetVos)
Map<String, Object> widgetVos = new HashMap<>();
widgetVos.put("Te_1", createTextWidgetDef("姓名"));
widgetVos.put("Ra_0", createRadioWidgetDef("性别", genderOptions));

// 2. 构建行数据 (widgetValue)
List<Map<String, Object>> widgetValue = new ArrayList<>();
for (Item item : items) {
    Map<String, Object> row = new HashMap<>();
    row.put("Te_1", item.getName());
    row.put("Ra_0", item.getGenderKey()); // 设置key，不是label
    widgetValue.add(row);
}

// 3. 组装明细表
Map<String, Object> detailMap = new HashMap<>();
detailMap.put("Dd_0", Map.of(
    "codeId", "Dd_0",
    "type", "detailedWidget",
    "title", "明细表",
    "widgetVos", widgetVos,
    "widgetValue", widgetValue
));
```

### 创建列定义

```java
// 文本列
private Map<String, Object> createTextWidgetDef(String title) {
    Map<String, Object> widget = new HashMap<>();
    widget.put("type", "textWidget");
    widget.put("title", title);
    widget.put("extendFieldMap", new HashMap<>());
    return widget;
}

// 单选列
private Map<String, Object> createRadioWidgetDef(String title, List<Map<String, String>> options) {
    Map<String, Object> widget = new HashMap<>();
    widget.put("type", "radioWidget");
    widget.put("title", title);
    widget.put("options", options);
    widget.put("extendFieldMap", new HashMap<>());
    return widget;
}
```

---

## 多个明细表

一个表单可以有多个明细表，通过不同的 `codeId` 区分：

```json
{
  "detailMap": {
    "Dd_0": {
      "codeId": "Dd_0",
      "title": "人伤明细",
      "type": "detailedWidget",
      "widgetVos": { /* 人伤字段定义 */ },
      "widgetValue": [ /* 人伤数据 */ ]
    },
    "Dd_1": {
      "codeId": "Dd_1",
      "title": "车辆明细",
      "type": "detailedWidget",
      "widgetVos": { /* 车辆字段定义 */ },
      "widgetValue": [ /* 车辆数据 */ ]
    }
  }
}
```

---

## 完整示例

### 推送数据解析

```json
{
  "Dd_0": {
    "codeId": "Dd_0",
    "title": "人伤事故情况",
    "type": "detailedWidget",
    "widgetVos": {
      "Te_1": { "codeId": "Te_1", "type": "textWidget", "title": "姓名" },
      "Ra_0": {
        "codeId": "Ra_0",
        "type": "radioWidget",
        "title": "性别",
        "options": [
          { "key": "AaBaCcDd", "value": "男" },
          { "key": "EeFfGgHh", "value": "女" }
        ]
      },
      "Te_2": { "codeId": "Te_2", "type": "textWidget", "title": "身份证号" }
    },
    "widgetValue": [
      { "_id_": "1", "Te_1": "张三", "Ra_0": "AaBaCcDd", "Te_2": "310..." },
      { "_id_": "2", "Te_1": "李四", "Ra_0": "EeFfGgHh", "Te_2": "320..." }
    ]
  }
}
```

### 解析结果

| 姓名 | 性别 | 身份证号 |
|-----|------|---------|
| 张三 | 男 | 310... |
| 李四 | 女 | 320... |

---

## 注意事项

1. **行ID `_id_`**: 构建数据时可不设置，系统会自动生成
2. **单选/多选**: 行数据中存储的是 key，需要通过 `widgetVos` 中的 options 转换
3. **空值处理**: 行数据中可能缺少某些字段，需要做空值判断
4. **列定义**: `widgetVos` 中的控件结构与主表控件相同，但没有 `value` 字段（或为 null）
5. **明细表嵌套**: 不支持明细表嵌套明细表