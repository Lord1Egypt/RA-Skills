# Datepicker 日期选择器组件 Skill

## 组件概述

`SlDatepicker` 是一个日期/日期时间选择器组件，支持日期选择（`date`）和日期时间选择（`datetime`）两种模式。在桌面端以弹出面板形式展示日历，在移动端（屏幕宽度 ≤ 500px）自动切换为底部抽屉面板。

## 功能列表

| 功能 | 说明 | 详细文档 |
|------|------|----------|
| 基础用法 | 日期选择、占位符、默认值、尺寸、清除等基础功能 | [basic-usage.md](./features/basic-usage.md) |
| 日期时间模式 | datetime 模式选择日期和时间 | [datetime-mode.md](./features/datetime-mode.md) |
| 日期格式化 | 通过 format 自定义日期显示格式（基于 dayjs） | [format.md](./features/format.md) |
| 日期范围限制 | 通过 min/max 限制可选日期范围 | [date-range.md](./features/date-range.md) |
| 表单集成 | 表单关联、必填校验 | [form-integration.md](./features/form-integration.md) |
| 事件处理 | sl-change、sl-input 事件监听与处理 | [events.md](./features/events.md) |
| 样式定制 | CSS Parts、Slots、尺寸、filled/pill 等外观定制 | [styling.md](./features/styling.md) |
| 校验 | 内置校验、自定义校验、校验消息 | [validation.md](./features/validation.md) |

## 核心约束

### 必须遵守的规则

1. **值格式要求**
   - `date` 模式：值格式为 `yyyy-MM-dd`（如 `2024-01-15`）
   - `datetime` 模式：值格式为 `yyyy-MM-dd HH:mm:ss`（如 `2024-01-15 14:30:00`）
   - 支持 `-`、`/`、`.` 作为日期分隔符输入，但输出统一为 `-` 分隔

2. **React 框架规范**
   - 导入必须从 `@kdcloudjs/shoelace/dist/react/datepicker/index.js` 默认导入
   - 类型导入使用 `import type SlDatepickerElement from '@kdcloudjs/shoelace/dist/components/datepicker/datepicker.js'`
   - **事件绑定**：在 JSX 中使用 `onSlChange`、`onSlInput` 等 `onSl*` 前缀属性绑定事件

3. **组件标签名**
   - React 组件名为 `SlDatepicker`，HTML 标签名为 `sl-datepicker`

## 快速开始

### 组件导入

```jsx
// 默认导入 React 包装组件
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

// 类型导入（TypeScript）
import type SlDatepickerElement from '@kdcloudjs/shoelace/dist/components/datepicker/datepicker.js';
```

### 最简示例

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => <SlDatepicker style={{ width: "230px" }} />;
```

### 事件监听示例

在 JSX 中直接使用 `onSlChange`、`onSlInput` 等 `onSl*` 属性绑定事件：

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [value, setValue] = useState("");

  const handleChange = useCallback((event) => {
    setValue(event.target.value);
  }, []);

  return (
    <SlDatepicker
      placeholder="选择日期"
      onSlChange={handleChange}
    />
  );
};
```

## API 概览

### 主要属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `value` | 当前日期值 | `string` | `''` |
| `type` | 选择器类型 | `'date' \| 'datetime'` | `'date'` |
| `placeholder` | 占位提示文本 | `string` | `''` |
| `label` | 标签文本 | `string` | `''` |
| `name` | 表单字段名 | `string` | `''` |
| `disabled` | 是否禁用 | `boolean` | `false` |
| `readonly` | 是否只读 | `boolean` | `false` |
| `clearable` | 是否可清除 | `boolean` | `false` |
| `required` | 是否必填 | `boolean` | `false` |
| `size` | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| `min` | 最小可选日期 | `string` | `'0001-01-01'` |
| `max` | 最大可选日期 | `string` | `'9999-12-31'` |
| `pattern` | 输入格式正则 | `string` | - |
| `format` | 日期显示格式（dayjs） | `string` | `'YYYY-MM-DD'` / `'YYYY-MM-DD HH:mm:ss'` |
| `hoist` | 弹出层提升到固定定位 | `boolean` | `false` |
| `filled` | 填充样式 | `boolean` | `false` |
| `pill` | 圆角药丸样式 | `boolean` | `false` |
| `help-text` | 帮助提示文本 | `string` | `''` |
| `form` | 关联的表单 ID | `string` | `''` |

### 主要事件

**注意**：以下事件通过 `onSl*` JSX 属性绑定。

| 事件 | 说明 | 触发时机 |
|------|------|----------|
| `sl-change` | 值确认变更 | 选择日期并确认、输入框失焦提交、清除值时触发 |
| `sl-input` | 输入过程变化 | 输入框键入、日历面板选择日期时触发 |
| `sl-focus` | 获取焦点 | 控件获取焦点时触发 |
| `sl-blur` | 失去焦点 | 控件失去焦点时触发 |
| `sl-clear` | 清除值 | 清除按钮被激活时触发 |
| `sl-invalid` | 校验失败 | 表单校验失败时触发 |

### 主要方法

| 方法 | 说明 | 参数 |
|------|------|------|
| `focus(options?)` | 聚焦并打开面板 | `FocusOptions` |
| `blur()` | 失焦并关闭面板 | - |
| `checkValidity()` | 检查表单校验 | - |
| `reportValidity()` | 报告校验结果 | - |
| `setCustomValidity(message)` | 设置自定义校验消息 | `string` |
| `getForm()` | 获取关联的表单元素 | - |

### Slots（插槽）

| Slot | 说明 |
|------|------|
| `label` | 自定义标签内容 |
| `prefix` | 输入框前缀 |
| `suffix` | 输入框后缀（默认为日历图标） |
| `clear-icon` | 自定义清除按钮图标 |
| `help-text` | 自定义帮助提示内容 |

### CSS Parts

| Part 名称 | 说明 |
|-----------|------|
| `input` | 输入框 |
| `popup` | 弹出面板容器 |
| `calendar` | 日历组件 |
| `calendar-base` | 日历基础容器 |
| `calendar-header` | 日历头部 |
| `calendar-nav-button` | 日历导航按钮 |
| `calendar-title` | 日历标题 |
| `calendar-title-year` | 日历标题年份 |
| `calendar-title-month` | 日历标题月份 |
| `calendar-body` | 日历主体 |
| `calendar-date-panel` | 日期选择视图的容器 |
| `calendar-day-header` | 星期标题栏 |
| `calendar-day` | 日期网格中的每一天 |
| `calendar-day-footer` | 日期视图底部的操作区 |
| `calendar-month-grid` | 月份选择视图的网格容器 |
| `calendar-month-item` | 月份网格中的每一个月份项 |
| `calendar-year-grid` | 年份选择视图的网格容器 |
| `calendar-year-item` | 年份网格中的每一个年份项 |
| `calendar-time-footer` | 时间选择底部（datetime 模式） |
| `time-panel-base` | 时间面板基础容器 |
| `time-panel-header` | 时间面板头部 |
| `time-panel-columns` | 时间面板列容器 |
| `time-panel-column` | 时间面板单列 |
| `time-panel-hour` | 小时列 |
| `time-panel-minute` | 分钟列 |
| `time-panel-second` | 秒列 |
| `time-panel-item` | 时间选择项 |
| `time-panel-footer` | 时间面板底部 |

## 使用建议

1. **日期选择**：仅需选择日期时使用默认 `type="date"`，选择后自动关闭弹窗
2. **日期时间选择**：需要精确到时分秒时设置 `type="datetime"`，需点击确定按钮确认
3. **日期范围限制**：通过 `min` 和 `max` 属性限制可选范围，超出范围的日期会被禁用
4. **事件绑定**：React 中直接在 JSX 使用 `onSlChange`、`onSlInput` 等属性绑定事件（遵循 `onSl*` 命名规范）
5. **移动端适配**：组件自动检测屏幕宽度，≤ 500px 时切换为移动端底部抽屉面板
