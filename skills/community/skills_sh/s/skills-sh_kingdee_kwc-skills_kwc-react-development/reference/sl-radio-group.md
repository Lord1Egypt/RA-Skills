# Radio Group 单选框组

用于将多个单选框或单选按钮组合在一起，作为单个表单控件使用。

## 特性概览

- **布局控制**：支持 `horizontal`（水平）和 `vertical`（垂直）两种排列方式
- **尺寸控制**：支持 `small`、`medium`、`large` 三种尺寸
- **表单集成**：支持表单验证和自定义校验
- **两种样式**：支持普通单选框（SlRadio）和按钮式单选框（SlRadioButton）

## 基础用法

最简单的用法，将多个 `SlRadio` 放入 `SlRadioGroup` 中。

```jsx
import { useState } from 'react';
import SlRadioGroup from '@shoelace-style/shoelace/dist/react/radio-group';
import SlRadio from '@shoelace-style/shoelace/dist/react/radio';

function App() {
  const [value, setValue] = useState('1');

  return (
    <SlRadioGroup 
      label="选择一个选项" 
      name="option" 
      value={value}
      onSlChange={e => setValue(e.target.value)}
    >
      <SlRadio value="1">选项 1</SlRadio>
      <SlRadio value="2">选项 2</SlRadio>
      <SlRadio value="3">选项 3</SlRadio>
    </SlRadioGroup>
  );
}
```

## 布局方向

使用 `layout` 属性控制单选框的排列方向。默认为 `vertical`（垂直排列），设置为 `horizontal` 可实现水平排列。

```jsx
import SlRadioGroup from '@shoelace-style/shoelace/dist/react/radio-group';
import SlRadio from '@shoelace-style/shoelace/dist/react/radio';

function App() {
  return (
    <>
      <SlRadioGroup label="垂直排列（默认）" name="a" value="1" layout="vertical">
        <SlRadio value="1">选项 1</SlRadio>
        <SlRadio value="2">选项 2</SlRadio>
        <SlRadio value="3">选项 3</SlRadio>
      </SlRadioGroup>

      <br /><br />

      <SlRadioGroup label="水平排列" name="b" value="1" layout="horizontal">
        <SlRadio value="1">选项 1</SlRadio>
        <SlRadio value="2">选项 2</SlRadio>
        <SlRadio value="3">选项 3</SlRadio>
      </SlRadioGroup>
    </>
  );
}
```

## 按钮式单选框布局

`layout` 属性同样适用于按钮式单选框（SlRadioButton）。

```jsx
import SlRadioGroup from '@shoelace-style/shoelace/dist/react/radio-group';
import SlRadioButton from '@shoelace-style/shoelace/dist/react/radio-button';

function App() {
  return (
    <>
      <SlRadioGroup label="水平按钮" name="c" value="1" layout="horizontal">
        <SlRadioButton value="1">选项 1</SlRadioButton>
        <SlRadioButton value="2">选项 2</SlRadioButton>
        <SlRadioButton value="3">选项 3</SlRadioButton>
      </SlRadioGroup>

      <br /><br />

      <SlRadioGroup label="垂直按钮" name="d" value="1" layout="vertical">
        <SlRadioButton value="1">选项 1</SlRadioButton>
        <SlRadioButton value="2">选项 2</SlRadioButton>
        <SlRadioButton value="3">选项 3</SlRadioButton>
      </SlRadioGroup>
    </>
  );
}
```

## 帮助文本

使用 `helpText` 属性添加描述性帮助文本。

```jsx
import SlRadioGroup from '@shoelace-style/shoelace/dist/react/radio-group';
import SlRadio from '@shoelace-style/shoelace/dist/react/radio';

function App() {
  return (
    <SlRadioGroup 
      label="选择一个选项" 
      helpText="请选择最合适的选项" 
      name="option" 
      value="1"
    >
      <SlRadio value="1">选项 1</SlRadio>
      <SlRadio value="2">选项 2</SlRadio>
      <SlRadio value="3">选项 3</SlRadio>
    </SlRadioGroup>
  );
}
```

## 尺寸

使用 `size` 属性设置单选框组的尺寸，会应用到所有子单选框。

```jsx
import SlRadioGroup from '@shoelace-style/shoelace/dist/react/radio-group';
import SlRadio from '@shoelace-style/shoelace/dist/react/radio';

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <SlRadioGroup label="小尺寸" size="small" name="s" value="1">
        <SlRadio value="1">选项 1</SlRadio>
        <SlRadio value="2">选项 2</SlRadio>
      </SlRadioGroup>

      <SlRadioGroup label="中等尺寸" size="medium" name="m" value="1">
        <SlRadio value="1">选项 1</SlRadio>
        <SlRadio value="2">选项 2</SlRadio>
      </SlRadioGroup>

      <SlRadioGroup label="大尺寸" size="large" name="l" value="1">
        <SlRadio value="1">选项 1</SlRadio>
        <SlRadio value="2">选项 2</SlRadio>
      </SlRadioGroup>
    </div>
  );
}
```

## Properties

| 属性 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| label | 单选框组的标签 | `string` | `''` |
| helpText | 帮助文本 | `string` | `''` |
| name | 表单提交时的字段名 | `string` | `'option'` |
| value | 当前选中的值 | `string` | `''` |
| size | 尺寸大小 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| layout | 排列方向 | `'horizontal' \| 'vertical'` | `'vertical'` |
| form | 关联的表单 ID | `string` | `''` |
| required | 是否必填 | `boolean` | `false` |

## Events

| 事件名称 | React 绑定 | 描述 |
| --- | --- | --- |
| sl-change | `onSlChange` | 选中值变化时触发 |
| sl-input | `onSlInput` | 用户输入时触发 |
| sl-invalid | `onSlInvalid` | 表单验证失败时触发 |

## Slots

| 插槽名称 | 描述 |
| --- | --- |
| (default) | 放置 SlRadio 或 SlRadioButton 元素 |
| label | 自定义标签内容 |
| help-text | 自定义帮助文本内容 |

## CSS Parts

| Part 名称 | 描述 |
| --- | --- |
| form-control | 表单控件容器 |
| form-control-label | 标签容器 |
| form-control-input | 输入区域容器 |
| form-control-help-text | 帮助文本容器 |
| button-group | 按钮组容器（使用 radio-button 时） |
| radios | 单选框容器（使用 radio 时） |

## 导入说明

```jsx
import SlRadioGroup from '@shoelace-style/shoelace/dist/react/radio-group';
import SlRadio from '@shoelace-style/shoelace/dist/react/radio';
// 如果使用按钮式单选框
import SlRadioButton from '@shoelace-style/shoelace/dist/react/radio-button';
```
