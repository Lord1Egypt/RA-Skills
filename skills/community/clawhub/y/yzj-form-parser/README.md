# 云之家表单数据解析器 (yzj-form-parser)

[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/code)
[![Language](https://img.shields.io/badge/Language-中文-green)]()

> Claude Code 技能：用于解析和构建云之家(YunZhijia)表单数据

## 📖 简介

`yzj-form-parser` 是一个专为处理云之家表单 JSON 数据而设计的 Claude Code 技能。它支持**双向转换**：

- **推送数据解析**：从 `widgetMap` 提取业务字段（读取数据）
- **审批发起构建**：将业务字段转换为 `widgetMap`（写入数据）

## 🚀 快速开始

### 安装

将本技能放置在 Claude Code 的 skills 目录下：

```
~/.claude/skills/yzj-form-parser/
├── SKILL.md
├── README.md
└── references/
    ├── widget-types.md
    ├── detail-widget.md
    └── file-widget.md
```

### 使用方式

在 Claude Code 中直接描述你的需求，技能会自动触发：

```
# 解析推送数据
"帮我解析这个云之家审批推送数据..."

# 构建审批数据
"帮我构建发起审批接口的表单数据..."
```

## 🎯 触发场景

| 场景 | 说明 |
|------|------|
| 解析推送数据 | 处理云之家审批回调的 JSON 数据 |
| 构建审批数据 | 组装发起审批接口的请求参数 |
| 理解表单结构 | 分析 `widgetMap` 和 `detailMap` 的数据结构 |
| 控件数据处理 | 处理文本、单选、多选、日期、人员、部门、明细表等各类控件 |

## 📋 支持的控件类型

### 基础控件

| 控件类型 | type | 说明 |
|---------|------|------|
| 文本 | `textWidget` / `textAreaWidget` | 单行/多行文本 |
| 日期 | `dateWidget` / `dateRangeWidget` | 日期/日期区间 |
| 数字 | `numberWidget` | 数字输入 |
| 金额 | `moneyWidget` | 金额输入 |
| 运算 | `arithmeticWidget` | 公式运算 |

### 选择控件

| 控件类型 | type | 说明 |
|---------|------|------|
| 单选 | `radioWidget` | 单选按钮 |
| 多选 | `checkboxWidget` | 复选框 |

### 组织架构控件

| 控件类型 | type | 说明 |
|---------|------|------|
| 人员 | `personSelectWidget` | 人员选择器 |
| 部门 | `departmentSelectWidget` | 部门选择器 |

### 附件控件

| 控件类型 | type | 说明 |
|---------|------|------|
| 附件 | `attachmentWidget` | 文件上传 |
| 图片 | `imageWidget` | 图片上传 |

### 特殊控件

| 控件类型 | type | 说明 |
|---------|------|------|
| 关联审批 | `relatedWidget` | 关联其他审批单据 |
| 流水号 | `serialNumWidget` | 系统自动生成编号 |
| 明细表 | `detailedWidget` | 子表/明细数据 |

## 📚 数据结构概览

### 表单整体结构

```json
{
  "formInfo": {
    "widgetMap": { /* 主表单控件 */ },
    "detailMap": { /* 明细表控件 */ }
  },
  "basicInfo": {
    "eventId": "事件ID",
    "formInstId": "表单实例ID",
    "flowInstId": "流程实例ID",
    "formDefId": "表单模版ID",
    "actionType": "reach/agree/submit/...",
    "title": "表单标题"
  }
}
```

### 控件通用字段

```json
{
  "codeId": "控件唯一标识",
  "title": "控件标题",
  "type": "控件类型",
  "value": "控件值",
  "extendFieldMap": { /* 扩展配置 */ }
}
```

## 💡 使用示例

### 解析推送数据

```java
// 解析主表单
Map<String, WidgetInfo> widgetMap = formInfo.getWidgetMap();

// 获取文本
String title = (String) widgetMap.get("_S_TITLE").getValue();

// 获取日期
Long timestamp = (Long) widgetMap.get("Da_0").getValue();
Date date = new Date(timestamp);

// 获取单选项
WidgetInfo radio = widgetMap.get("Ra_0");
String selectedKey = (String) radio.getValue();
String label = getOptionLabel(radio.getOptions(), selectedKey);

// 获取人员信息
WidgetInfo person = widgetMap.get("Ps_0");
String name = person.getPersonInfo().get(0).getName();
```

### 构建审批数据

```java
// 构建主表单
Map<String, Object> widgetMap = new HashMap<>();

widgetMap.put("_S_TITLE", createTextWidget("标题内容"));
widgetMap.put("Da_0", createDateWidget(System.currentTimeMillis()));
widgetMap.put("Ra_0", createRadioWidget("AaBaCcDd", options));
widgetMap.put("Ps_0", createPersonWidget(oid, name));

// 构建明细表
List<Map<String, Object>> rows = new ArrayList<>();
for (Item item : items) {
    Map<String, Object> row = new HashMap<>();
    row.put("Te_1", item.getName());
    row.put("Ra_0", item.getRadioKey());
    rows.add(row);
}
```

## ⚠️ 注意事项

1. **数字类型**：`numberWidget`、`moneyWidget` 的 value 是**字符串**类型
2. **时间戳**：日期控件的 value 是**毫秒级时间戳**（Long）
3. **选项 key**：单选/多选的 value 是选项的 **key**，不是显示文本
4. **明细表行 ID**：每行有 `_id_` 字段，构建新数据时可不设置
5. **数组类型**：多选、人员、部门、附件的 value 都是数组

## 📁 参考文档

- [控件类型详解](references/widget-types.md)
- [明细表控件](references/detail-widget.md)
- [附件控件](references/file-widget.md)

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License
