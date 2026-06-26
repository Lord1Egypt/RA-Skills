# Segmented 分段选择器

分段选择器用于在多个选项之间进行切换，类似于 Tab 切换，适用于视图切换、筛选模式等场景。

## 特性概览

- **多种选项格式**：支持字符串、数字、对象（含 label/value/icon/disabled/tooltip）三种选项格式
- **受控/非受控**：支持受控模式 (`value`) 和非受控模式 (`defaultValue`)
- **多种尺寸**：支持 `large`、`medium`（默认）、`small` 三种尺寸
- **多种形状**：支持默认形状和胶囊形 (`round`)
- **垂直布局**：支持水平（默认）和垂直 (`vertical`) 两种方向
- **Block 模式**：支持撑满父容器宽度
- **图标支持**：选项可配置 `sl-icon` 图标
- **自定义渲染**：通过 slot 自定义选项内容
- **禁用状态**：支持整体禁用和单个选项禁用
- **滑块动画**：选中项切换时带有平滑的滑块过渡动画

## 基础用法

最简单的分段选择器用法，传入字符串数组作为选项。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => <SlSegmented options={['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']} />;
```

## 数字选项

支持传入数字数组作为选项。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => <SlSegmented options={[1, 2, 3, 4, 5]} defaultValue={3} />;
```

## 带图标选项

通过对象格式的选项配置 `icon` 字段，显示 `sl-icon` 图标。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => (
  <SlSegmented
    options={[
      { label: '列表', value: 'list', icon: 'list' },
      { label: '看板', value: 'kanban', icon: 'kanban' },
      { label: '日历', value: 'calendar', icon: 'calendar3' }
    ]}
  />
);
```

## 设置默认值

使用 `defaultValue` 属性设置默认选中项（非受控模式）。如果不设置，默认选中第一个非禁用选项。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => <SlSegmented options={['Daily', 'Weekly', 'Monthly']} defaultValue="Monthly" />;
```

## 受控模式

使用 `value` 属性进行受控模式，选中值由外部状态管理。通过 `onChange` 回调监听值变化并更新状态。

```jsx
import React, { useState, useCallback } from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => {
  const [value, setValue] = useState('daily');

  const handleChange = useCallback(val => {
    setValue(val);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <p style={{ fontSize: '14px', color: '#666' }}>当前选中: {value}</p>
      <SlSegmented options={['daily', 'weekly', 'monthly']} value={value} onChange={handleChange} />
    </div>
  );
};
```

## 禁用某个选项

通过对象格式的选项设置 `disabled: true` 禁用单个选项。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => (
  <SlSegmented
    options={[
      { label: 'Daily', value: 'daily' },
      { label: 'Weekly', value: 'weekly', disabled: true },
      { label: 'Monthly', value: 'monthly' }
    ]}
  />
);
```

## 整体禁用

使用 `disabled` 属性禁用整个分段选择器。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => <SlSegmented options={['Daily', 'Weekly', 'Monthly']} disabled />;
```

## 三种尺寸

使用 `size` 属性设置尺寸，支持 `large`、`medium`（默认）、`small`。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => {
  const options = ['Daily', 'Weekly', 'Monthly'];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'flex-start' }}>
      <SlSegmented options={options} size="large" />
      <SlSegmented options={options} size="medium" />
      <SlSegmented options={options} size="small" />
    </div>
  );
};
```

## 胶囊形

使用 `shape="round"` 启用胶囊形外观。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => <SlSegmented options={['Daily', 'Weekly', 'Monthly']} shape="round" />;
```

## 垂直模式

使用 `orientation="vertical"` 启用垂直布局。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => (
  <SlSegmented
    orientation="vertical"
    options={[
      { value: 'list', icon: 'list' },
      { value: 'kanban', icon: 'kanban' },
      { value: 'calendar', icon: 'calendar3' }
    ]}
  />
);
```

## Block 模式

使用 `block` 属性使分段选择器撑满父容器宽度，每个选项等分宽度。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => <SlSegmented options={['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']} block />;
```

## 自定义渲染

通过 slot 自定义选项内容，slot name 对应 option 的 `value`。

```jsx
import React from 'react';
import SlSegmented from '@kdcloudjs/shoelace/dist/react/segmented/index.js';

export default () => (
  <SlSegmented
    options={[
      { value: 'user1', label: '', tooltip: 'User 1' },
      { value: 'user2', label: '', tooltip: 'User 2' },
      { value: 'user3', label: '', tooltip: 'User 3' }
    ]}
  >
    <div slot="user1" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '4px' }}>
      <img
        src="https://api.dicebear.com/7.x/miniavs/svg?seed=8"
        width="32"
        height="32"
        style={{ borderRadius: '50%' }}
      />
      <span>User 1</span>
    </div>
    <div slot="user2" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '4px' }}>
      <img
        src="https://api.dicebear.com/7.x/miniavs/svg?seed=3"
        width="32"
        height="32"
        style={{ borderRadius: '50%' }}
      />
      <span>User 2</span>
    </div>
    <div slot="user3" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '4px' }}>
      <img
        src="https://api.dicebear.com/7.x/miniavs/svg?seed=12"
        width="32"
        height="32"
        style={{ borderRadius: '50%' }}
      />
      <span>User 3</span>
    </div>
  </SlSegmented>
);
```

## Properties

| 属性         | 描述                     | 类型                                    | 默认值         |
| ------------ | ------------------------ | --------------------------------------- | -------------- |
| options      | 选项列表                 | `(string \| number \| SegmentedItem)[]` | `[]`           |
| value        | 当前选中值（受控模式）   | `string \| number`                      | -              |
| defaultValue | 默认选中值（非受控模式） | `string \| number`                      | -              |
| onChange     | 值变化时的回调函数       | `(value: string \| number) => void`     | -              |
| disabled     | 是否禁用整个分段选择器   | `boolean`                               | `false`        |
| orientation  | 布局方向                 | `'horizontal' \| 'vertical'`            | `'horizontal'` |
| shape        | 外观形状                 | `'default' \| 'round'`                  | `'default'`    |
| size         | 尺寸大小                 | `'large' \| 'medium' \| 'small'`        | `'medium'`     |
| block        | 是否撑满父容器宽度       | `boolean`                               | `false`        |
| name         | 原生 radio 分组名称      | `string`                                | `'segmented'`  |

## SegmentedItem 选项对象

| 属性     | 描述             | 类型                       | 必填 |
| -------- | ---------------- | -------------------------- | ---- |
| label    | 显示文本         | `string \| TemplateResult` | 否   |
| value    | 选项值           | `string \| number`         | 是   |
| disabled | 是否禁用该选项   | `boolean`                  | 否   |
| icon     | sl-icon 图标名称 | `string`                   | 否   |
| tooltip  | 悬停提示文本     | `string`                   | 否   |

## Slots

| 名称      | 描述                                                      |
| --------- | --------------------------------------------------------- |
| `[value]` | 以选项的 `value` 值作为 slot name，自定义该选项的渲染内容 |

## CSS Custom Properties

| CSS 属性                  | 描述               | 默认值 |
| ------------------------- | ------------------ | ------ |
| --sl-color-neutral-100    | 容器背景色         | 主题色 |
| --sl-color-neutral-700    | 选项文字颜色       | 主题色 |
| --sl-color-neutral-900    | 选中项文字颜色     | 主题色 |
| --sl-color-neutral-400    | 禁用项文字颜色     | 主题色 |
| --sl-color-neutral-0      | 滑块背景色         | 主题色 |
| --sl-border-radius-medium | 容器和选项圆角     | 主题色 |
| --sl-font-size-small      | 默认字体大小       | 主题色 |
| --sl-font-size-medium     | large 尺寸字体大小 | 主题色 |
| --sl-font-size-x-small    | small 尺寸字体大小 | 主题色 |

## 常见问题

### Q: 受控模式 vs 非受控模式有什么区别？

A:

- **非受控模式**：使用 `defaultValue`，组件内部管理选中状态。选项变化时会自动调整选中值。
- **受控模式**：使用 `value`，需要在 `onChange` 回调中手动更新状态。

### Q: 选项动态变化后，当前选中值会怎样？

A: 在非受控模式下，如果当前选中值不在新的选项列表中，组件会自动选中第一个非禁用选项。受控模式下需要自行处理。

### Q: 如何只显示图标不显示文字？

A: 在选项对象中只设置 `icon` 和 `value`，不设置 `label`（或设为空字符串），同时可以配合 `tooltip` 提供悬停提示：

```jsx
<SlSegmented
  options={[
    { value: 'list', icon: 'list', tooltip: '列表视图' },
    { value: 'grid', icon: 'grid', tooltip: '网格视图' }
  ]}
/>
```

### Q: 如何自定义选项的渲染内容？

A: 使用 slot 机制，slot name 对应选项的 `value` 值。在选项对象中将 `label` 设为空字符串，然后通过子元素的 `slot` 属性插入自定义内容。
