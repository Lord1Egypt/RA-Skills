# Steps 步骤条

用于引导用户按照流程完成任务的导航条，显示当前所处步骤及状态。

## 特性概览

- **多种类型**：支持默认型 (`default`)、点状型 (`dot`)、导航型 (`navigation`)、面板型 (`panel`)、内联型 (`inline`)
- **双变体**：支持填充模式 (`filled`) 和描边模式 (`outlined`)
- **双尺寸**：支持标准尺寸 (`default`) 和迷你尺寸 (`small`)
- **方向切换**：支持水平模式 (`horizontal`) 和垂直模式 (`vertical`)
- **标签位置**：支持标签在图标右侧 (`horizontal`) 或下方 (`vertical`)
- **状态流转**：自动根据 `current` 计算各步骤状态（wait / process / finish / error）
- **进度百分比**：当前步骤支持显示进度环
- **自定义图标**：每个步骤支持自定义 sl-icon 图标
- **可点击切换**：传入 `onChange` 后步骤条变为可点击状态
- **响应式**：支持窄屏自动切换为垂直模式

## 基础用法

最简单的步骤条用法，通过 `items` 设置步骤数据，`current` 指定当前步骤（从 0 开始）。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    items={[
      { title: '已完成', content: '这是描述信息' },
      { title: '进行中', subTitle: '副标题', content: '这是描述信息' },
      { title: '待处理', content: '这是描述信息' }
    ]}
  />
);
```

## 描边模式

使用 `variant="outlined"` 切换为描边样式，当前步骤图标使用蓝色背景。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    variant="outlined"
    items={[
      { title: '已完成', content: '这是描述信息' },
      { title: '进行中', content: '这是描述信息' },
      { title: '待处理', content: '这是描述信息' }
    ]}
  />
);
```

## 迷你尺寸

使用 `size="small"` 启用迷你尺寸，图标 24px，文字更紧凑。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    size="small"
    items={[
      { title: '已完成', content: '这是描述信息' },
      { title: '进行中', content: '这是描述信息' },
      { title: '待处理', content: '这是描述信息' }
    ]}
  />
);
```

## 起始序号

使用 `initial` 修改起始序号（显示序号 = initial + index + 1）。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    initial={2}
    items={[
      { title: '步骤三', content: '这是描述信息' },
      { title: '步骤四', content: '这是描述信息' },
      { title: '步骤五', content: '这是描述信息' }
    ]}
  />
);
```

## 错误状态

使用 `status="error"` 设置当前步骤为错误状态，图标和文字变红。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    status="error"
    items={[
      { title: '已完成', content: '这是描述信息' },
      { title: '出错了', content: '请检查后重试' },
      { title: '待处理', content: '这是描述信息' }
    ]}
  />
);
```

## 进度百分比

当前步骤为 `process` 状态时，通过 `percent` 显示进度环。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    percent={60}
    items={[{ title: '已完成' }, { title: '进行中', content: '已完成 60%' }, { title: '待处理' }]}
  />
);
```

## 自定义图标

通过 item 的 `icon` 属性指定 sl-icon 图标名称，完全替换默认的序号/状态图标（无外圈）。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    items={[
      { title: '登录', icon: 'person', content: '账号验证' },
      { title: '付款', icon: 'credit-card', content: '确认支付信息' },
      { title: '完成', icon: 'check-circle', content: '订单完成' }
    ]}
  />
);
```

## 点状型

使用 `type="dot"` 用小圆点代替数字图标，视觉更简洁。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    type="dot"
    current={1}
    items={[
      { title: '已完成', content: '这是描述信息' },
      { title: '进行中', content: '这是描述信息' },
      { title: '待处理', content: '这是描述信息' }
    ]}
  />
);
```

## 导航型

使用 `type="navigation"` 呈现面包屑风格，适合顶部全局流程导航。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    type="navigation"
    current={1}
    items={[
      { title: '第一步', subTitle: '基本信息' },
      { title: '第二步', subTitle: '详细配置' },
      { title: '第三步', subTitle: '确认提交' }
    ]}
  />
);
```

## 面板型

使用 `type="panel"` 带有背景块的样式，适合在独立区域展示。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    type="panel"
    current={1}
    items={[
      { title: '已完成', content: '基本信息已填写' },
      { title: '进行中', content: '正在配置详细参数' },
      { title: '待处理', content: '等待确认提交' }
    ]}
  />
);
```

## 内联型

使用 `type="inline"` 嵌入在内容中展示流程状态，紧凑轻量。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <div
    style={{
      border: '1px solid var(--sl-color-neutral-200)',
      borderRadius: 'var(--sl-border-radius-medium)',
      overflow: 'hidden'
    }}
  >
    <div
      style={{
        padding: '16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid var(--sl-color-neutral-200)',
        background: 'var(--sl-color-neutral-50)'
      }}
    >
      <span style={{ fontWeight: 600 }}>订单 #2024001</span>
      <SlSteps
        type="inline"
        current={2}
        style={{ display: 'inline-flex', width: 'auto' }}
        items={[{ title: '下单' }, { title: '付款' }, { title: '发货' }, { title: '收货' }]}
      />
    </div>
    <div style={{ padding: '16px', fontSize: '14px', color: 'var(--sl-color-neutral-600)' }}>
      <div>商品：Shoelace 组件库企业版</div>
      <div>金额：¥ 12,800.00</div>
    </div>
  </div>
);
```

## 标签在下方

使用 `titlePlacement="vertical"` 将文字放在图标下方，通常配合水平布局使用。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    current={1}
    titlePlacement="vertical"
    items={[
      { title: '已完成', content: '这是描述信息' },
      { title: '进行中', content: '这是描述信息' },
      { title: '待处理', content: '这是描述信息' }
    ]}
  />
);
```

## 垂直模式

使用 `orientation="vertical"` 从上到下排列，适合侧边栏或手机端长页面。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <SlSteps
    orientation="vertical"
    current={1}
    items={[
      { title: '已完成', content: '这是步骤一的内容描述' },
      { title: '进行中', content: '这是步骤二的内容描述' },
      { title: '待处理', content: '这是步骤三的内容描述' }
    ]}
  />
);
```

## 响应式

设置 `responsive` 属性后，窄于 532px 时自动从水平模式切换为垂直模式。

```jsx
import React from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => (
  <div
    style={{
      resize: 'horizontal',
      overflow: 'auto',
      border: '1px dashed var(--sl-color-neutral-300)',
      padding: '16px',
      minWidth: '300px'
    }}
  >
    <SlSteps
      responsive
      current={1}
      items={[
        { title: '已完成', content: '这是描述信息' },
        { title: '进行中', content: '这是描述信息' },
        { title: '待处理', content: '这是描述信息' }
      ]}
    />
  </div>
);
```

## 可点击切换

传入 `onChange` 回调后，步骤条变为可点击状态，用户可以自由切换步骤。

```jsx
import React, { useState } from 'react';
import SlSteps from '@kdcloudjs/shoelace/dist/react/steps/index.js';

export default () => {
  const [current, setCurrent] = useState(0);

  return (
    <SlSteps
      current={current}
      onChange={c => setCurrent(c)}
      items={[
        { title: '步骤一', content: '填写基本信息' },
        { title: '步骤二', content: '配置详细参数' },
        { title: '步骤三', content: '确认并提交' }
      ]}
    />
  );
};
```

## Properties

| 属性           | 描述                                             | 类型                                                        | 默认值         |
| -------------- | ------------------------------------------------ | ----------------------------------------------------------- | -------------- |
| items          | 步骤条数据                                       | `StepItem[]`                                                | `[]`           |
| current        | 当前步骤（从 0 开始）                            | `number`                                                    | `0`            |
| status         | 当前步骤的状态                                   | `'wait' \| 'process' \| 'finish' \| 'error'`                | `'process'`    |
| `direction` | 步骤条方向 | `'ltr' \| 'rtl'` | `'ltr'` |
| initial        | 起始序号（显示序号 = initial + index + 1）       | `number`                                                    | `0`            |
| percent        | 当前步骤进度百分比（0-100），仅 process 状态生效 | `number`                                                    | -              |
| size           | 尺寸                                             | `'default' \| 'small'`                                      | `'default'`    |
| type           | 类型                                             | `'default' \| 'dot' \| 'navigation' \| 'panel' \| 'inline'` | `'default'`    |
| variant        | 样式变体                                         | `'filled' \| 'outlined'`                                    | `'filled'`     |
| orientation    | 方向                                             | `'horizontal' \| 'vertical'`                                | `'horizontal'` |
| titlePlacement | 标签位置                                         | `'horizontal' \| 'vertical'`                                | `'horizontal'` |
| responsive     | 是否开启响应式（窄于 532px 自动切换为垂直模式）  | `boolean`                                                   | `false`        |
| onChange       | 点击步骤切换的回调，传入后步骤条变为可点击状态   | `(current: number) => void`                                 | -              |

## StepItem

| 属性     | 描述                                         | 类型                                         | 默认值  |
| -------- | -------------------------------------------- | -------------------------------------------- | ------- |
| title    | 步骤标题                                     | `string`                                     | -       |
| content  | 步骤内容描述                                 | `string`                                     | -       |
| subTitle | 步骤副标题                                   | `string`                                     | -       |
| status   | 步骤状态，不设置时根据 current 自动生成      | `'wait' \| 'process' \| 'finish' \| 'error'` | -       |
| icon     | 自定义图标（sl-icon name），替换默认序号图标 | `string`                                     | -       |
| disabled | 是否禁用该步骤（可点击模式下不可点击）       | `boolean`                                    | `false` |

## 常见问题

### Q: 如何让步骤条可点击？

A: 传入 `onChange` 回调即可，例如：`<SlSteps onChange={(c) => setCurrent(c)} />`。步骤条会自动显示 cursor: pointer 和 hover 效果。

### Q: 如何设置某个步骤为禁用状态？

A: 在 `items` 数组中对应的 item 设置 `disabled: true`，可点击模式下该步骤不可点击。

### Q: 如何自定义步骤图标？

A: 在 item 中设置 `icon` 属性为 sl-icon 的 name 值，例如 `{ title: '登录', icon: 'person' }`。自定义图标会完全替换默认的序号/状态图标，不显示外圈。

### Q: 如何让标签显示在图标下方？

A: 设置 `titlePlacement="vertical"`，文字会显示在图标下方，连接线在图标行水平贯穿。

### Q: 各种 type 的适用场景？

A:

- **default**：最通用的数字/图标步骤条，适合表单向导。
- **dot**：用小圆点代替数字，视觉更简洁，适合非操作引导。
- **navigation**：自带面包屑感，常用于顶部全局流程导航。
- **panel**：带有背景块的样式，适合在独立区域展示。
- **inline**：嵌入在列表或详情内容中，展示对象当前的流程状态。
