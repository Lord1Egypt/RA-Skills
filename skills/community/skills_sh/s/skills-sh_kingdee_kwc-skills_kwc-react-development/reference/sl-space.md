# Space 间距

用于设置组件之间的间距，避免组件紧贴在一起，适合行内元素的水平或垂直间距布局。

## 特性概览

- **灵活间距**：支持 `small`、`medium`、`large` 预设大小或自定义数值
- **方向控制**：支持水平（`horizontal`）和垂直（`vertical`）两种排列方向
- **对齐方式**：支持 `start`、`end`、`center`、`baseline` 四种对齐方式
- **自动换行**：支持 `wrap` 属性实现空间不足时自动换行
- **CSS 变量**：支持通过 `--gap` 自定义间距

## 基础用法

最简单的用法，在一行内排列多个元素并设置间距。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => (
  <SlSpace>
    <SlButton>按钮1</SlButton>
    <SlButton>按钮2</SlButton>
    <SlButton>按钮3</SlButton>
  </SlSpace>
);
```

## 垂直间距

使用 `orientation="vertical"` 可以设置垂直方向排列。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => (
  <SlSpace orientation="vertical">
    <SlButton>按钮1</SlButton>
    <SlButton>按钮2</SlButton>
    <SlButton>按钮3</SlButton>
  </SlSpace>
);
```

## 间距大小

通过 `size` 属性设置间距大小，可选值为 `small`、`medium`、`large`，默认为 `small`。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const css = `
  .space-demo { display: flex; flex-direction: column; gap: 16px; }
`;

export default () => (
  <>
    <div className="space-demo">
      <SlSpace size="small">
        <SlButton>Small</SlButton>
        <SlButton>Small</SlButton>
        <SlButton>Small</SlButton>
      </SlSpace>
      
      <SlSpace size="medium">
        <SlButton>Medium</SlButton>
        <SlButton>Medium</SlButton>
        <SlButton>Medium</SlButton>
      </SlSpace>
      
      <SlSpace size="large">
        <SlButton>Large</SlButton>
        <SlButton>Large</SlButton>
        <SlButton>Large</SlButton>
      </SlSpace>
    </div>
    <style>{css}</style>
  </>
);
```

## 自定义间距

`size` 也可以设置为具体的数值（单位为 px）。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => (
  <SlSpace size={24}>
    <SlButton>按钮1</SlButton>
    <SlButton>按钮2</SlButton>
    <SlButton>按钮3</SlButton>
  </SlSpace>
);
```

## 数组形式间距

`size` 可以传入数组 `[水平间距, 垂直间距]` 分别设置水平和垂直方向的间距。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => (
  <SlSpace size={[16, 24]} wrap style={{ width: '300px' }}>
    <SlButton>按钮1</SlButton>
    <SlButton>按钮2</SlButton>
    <SlButton>按钮3</SlButton>
    <SlButton>按钮4</SlButton>
    <SlButton>按钮5</SlButton>
  </SlSpace>
);
```

## 对齐方式

通过 `align` 属性设置对齐方式，可选值为 `start`、`end`、`center`、`baseline`。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const css = `
  .space-demo { display: flex; flex-direction: column; gap: 16px; }
  .demo-box { padding: 16px; background: var(--sl-color-neutral-100); }
`;

export default () => (
  <>
    <div className="space-demo">
      <SlSpace align="start">
        <span className="demo-box">Start</span>
        <SlButton size="small">小按钮</SlButton>
        <SlButton size="large">大按钮</SlButton>
      </SlSpace>
      
      <SlSpace align="center">
        <span className="demo-box">Center</span>
        <SlButton size="small">小按钮</SlButton>
        <SlButton size="large">大按钮</SlButton>
      </SlSpace>
      
      <SlSpace align="end">
        <span className="demo-box">End</span>
        <SlButton size="small">小按钮</SlButton>
        <SlButton size="large">大按钮</SlButton>
      </SlSpace>
      
      <SlSpace align="baseline">
        <span className="demo-box">Baseline</span>
        <SlButton size="small">小按钮</SlButton>
        <SlButton size="large">大按钮</SlButton>
      </SlSpace>
    </div>
    <style>{css}</style>
  </>
);
```

## 自动换行

使用 `wrap` 属性可以让元素在空间不足时自动换行。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const css = `
  .wrap-container {
    width: 300px;
    border: 1px dashed var(--sl-color-neutral-300);
    padding: 8px;
  }
`;

export default () => (
  <>
    <SlSpace wrap className="wrap-container">
      <SlButton>按钮1</SlButton>
      <SlButton>按钮2</SlButton>
      <SlButton>按钮3</SlButton>
      <SlButton>按钮4</SlButton>
      <SlButton>按钮5</SlButton>
      <SlButton>按钮6</SlButton>
      <SlButton>按钮7</SlButton>
      <SlButton>按钮8</SlButton>
    </SlSpace>
    <style>{css}</style>
  </>
);
```

## 使用 CSS 变量自定义间距

可以通过 `--gap` CSS 变量来自定义间距。

```jsx
import React from "react";
import SlSpace from '@kdcloudjs/shoelace/dist/react/space/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => (
  <SlSpace style={{ '--gap': '32px' }}>
    <SlButton>按钮1</SlButton>
    <SlButton>按钮2</SlButton>
    <SlButton>按钮3</SlButton>
  </SlSpace>
);
```

## Properties

| 属性        | 描述                                                                 | 类型                                                    | 默认值         |
| ----------- | -------------------------------------------------------------------- | ------------------------------------------------------- | -------------- |
| orientation | 间距方向                                                             | `'horizontal' \| 'vertical'`                            | `'horizontal'` |
| size        | 间距大小，可选预设值或自定义数值（px），支持数组形式 `[水平, 垂直]` | `'small' \| 'medium' \| 'large' \| number \| [SpaceSize, SpaceSize]` | `'small'`      |
| align       | 对齐方式                                                             | `'start' \| 'end' \| 'center' \| 'baseline'`            | -              |
| wrap        | 是否自动换行，仅在 horizontal 方向时有效                             | `boolean`                                               | `false`        |

## CSS Parts

| Part      | 描述               |
| --------- | ------------------ |
| base      | 组件的基础容器     |
| item      | 每个子元素的包装容器 |
| separator | 分隔符容器         |

## CSS Custom Properties

| 属性   | 描述           | 默认值                    |
| ------ | -------------- | ------------------------- |
| --gap  | 自定义间距大小 | `var(--sl-spacing-small)` |

## 常见问题

### Q: 如何设置不同方向的间距？

A: 使用数组形式的 `size` 属性：
```jsx
<SlSpace size={[16, 24]} wrap>
  {/* 水平间距 16px，垂直间距 24px */}
</SlSpace>
```

### Q: wrap 属性不生效？

A: 确保 `orientation` 为 `horizontal`（默认值），`wrap` 仅在水平方向时有效。同时需要给容器设置一个固定宽度。

### Q: 如何让 Space 组件占满整行？

A: Space 组件默认是 `inline-block`，可以通过样式设置为 `block`：
```jsx
<SlSpace style={{ display: 'block', width: '100%' }}>
  {/* 内容 */}
</SlSpace>
```
