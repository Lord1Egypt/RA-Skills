# Grid 栅格布局

基于 24 栅格系统的布局组件，包含 `SlRow`（行）和 `SlCol`（列）两个组件，用于创建灵活的响应式布局。

## 特性概览

- **24 栅格系统**：将页面划分为 24 等份，通过 `span` 属性控制列宽
- **响应式布局**：支持 `xs`、`sm`、`md`、`lg`、`xl`、`xxl` 六个断点
- **灵活间距**：通过 `gutter` 属性设置水平和垂直间距
- **对齐方式**：支持水平对齐（`justify`）和垂直对齐（`align`）
- **列偏移**：通过 `offset`、`push`、`pull` 控制列的位置
- **Flex 布局**：支持 `flex` 属性实现弹性布局

## 基础用法

最简单的栅格布局，使用 `SlRow` 包裹 `SlCol`，通过 `span` 属性指定列宽。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-content {
    padding: 16px;
    text-align: center;
    color: white;
    border-radius: 4px;
  }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <SlRow>
      <SlCol span={12}><div className="grid-content bg-blue">col-12</div></SlCol>
      <SlCol span={12}><div className="grid-content bg-green">col-12</div></SlCol>
    </SlRow>
    <style>{css}</style>
  </>
);
```

## 栅格比例

24 栅格系统支持任意比例的列宽组合。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-demo { display: flex; flex-direction: column; gap: 16px; }
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <div className="grid-demo">
      <SlRow>
        <SlCol span={24}><div className="grid-content bg-blue">col-24</div></SlCol>
      </SlRow>
      <SlRow>
        <SlCol span={12}><div className="grid-content bg-blue">col-12</div></SlCol>
        <SlCol span={12}><div className="grid-content bg-green">col-12</div></SlCol>
      </SlRow>
      <SlRow>
        <SlCol span={8}><div className="grid-content bg-blue">col-8</div></SlCol>
        <SlCol span={8}><div className="grid-content bg-green">col-8</div></SlCol>
        <SlCol span={8}><div className="grid-content bg-blue">col-8</div></SlCol>
      </SlRow>
      <SlRow>
        <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
        <SlCol span={6}><div className="grid-content bg-green">col-6</div></SlCol>
        <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
        <SlCol span={6}><div className="grid-content bg-green">col-6</div></SlCol>
      </SlRow>
    </div>
    <style>{css}</style>
  </>
);
```

## 区块间隔（Gutter）

使用 `gutter` 属性设置列之间的间距。可以是数字（水平间距）或数组 `[水平, 垂直]`。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
`;

export default () => (
  <>
    <SlRow gutter={16}>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
    </SlRow>
    <style>{css}</style>
  </>
);
```

## 垂直间隔

使用数组格式 `[水平间距, 垂直间距]` 同时设置水平和垂直间距。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
`;

export default () => (
  <>
    <SlRow gutter={[16, 24]}>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
      <SlCol span={6}><div className="grid-content bg-blue">col-6</div></SlCol>
    </SlRow>
    <style>{css}</style>
  </>
);
```


## 列偏移（Offset）

使用 `offset` 属性将列向右偏移指定的栅格数。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-demo { display: flex; flex-direction: column; gap: 16px; }
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
`;

export default () => (
  <>
    <div className="grid-demo">
      <SlRow>
        <SlCol span={8}><div className="grid-content bg-blue">col-8</div></SlCol>
        <SlCol span={8} offset={8}><div className="grid-content bg-blue">col-8 offset-8</div></SlCol>
      </SlRow>
      <SlRow>
        <SlCol span={6} offset={6}><div className="grid-content bg-blue">col-6 offset-6</div></SlCol>
        <SlCol span={6} offset={6}><div className="grid-content bg-blue">col-6 offset-6</div></SlCol>
      </SlRow>
    </div>
    <style>{css}</style>
  </>
);
```

## 水平对齐

使用 `justify` 属性设置列的水平对齐方式。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-demo { display: flex; flex-direction: column; gap: 8px; }
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <div className="grid-demo">
      <p>start</p>
      <SlRow justify="start" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
      </SlRow>
      <p>center</p>
      <SlRow justify="center" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
      </SlRow>
      <p>end</p>
      <SlRow justify="end" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
      </SlRow>
      <p>space-between</p>
      <SlRow justify="space-between" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green">col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue">col-4</div></SlCol>
      </SlRow>
    </div>
    <style>{css}</style>
  </>
);
```

## 垂直对齐

使用 `align` 属性设置列的垂直对齐方式。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-demo { display: flex; flex-direction: column; gap: 8px; }
  .grid-content { text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <div className="grid-demo">
      <p>top</p>
      <SlRow justify="center" align="top" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue" style={{ padding: '40px 16px' }}>col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green" style={{ padding: '60px 16px' }}>col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue" style={{ padding: '30px 16px' }}>col-4</div></SlCol>
      </SlRow>
      <p>middle</p>
      <SlRow justify="center" align="middle" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue" style={{ padding: '40px 16px' }}>col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green" style={{ padding: '60px 16px' }}>col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue" style={{ padding: '30px 16px' }}>col-4</div></SlCol>
      </SlRow>
      <p>bottom</p>
      <SlRow justify="center" align="bottom" style={{ background: 'rgba(128,128,128,0.08)' }}>
        <SlCol span={4}><div className="grid-content bg-blue" style={{ padding: '40px 16px' }}>col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-green" style={{ padding: '60px 16px' }}>col-4</div></SlCol>
        <SlCol span={4}><div className="grid-content bg-blue" style={{ padding: '30px 16px' }}>col-4</div></SlCol>
      </SlRow>
    </div>
    <style>{css}</style>
  </>
);
```

## 列排序（Order）

使用 `order` 属性改变列的显示顺序。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <SlRow>
      <SlCol span={6} order={4}><div className="grid-content bg-blue">1 order-4</div></SlCol>
      <SlCol span={6} order={3}><div className="grid-content bg-green">2 order-3</div></SlCol>
      <SlCol span={6} order={2}><div className="grid-content bg-blue">3 order-2</div></SlCol>
      <SlCol span={6} order={1}><div className="grid-content bg-green">4 order-1</div></SlCol>
    </SlRow>
    <style>{css}</style>
  </>
);
```

## Flex 弹性布局

使用 `flex` 属性实现弹性布局。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-demo { display: flex; flex-direction: column; gap: 16px; }
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <div className="grid-demo">
      <SlRow>
        <SlCol flex="100px"><div className="grid-content bg-blue">100px</div></SlCol>
        <SlCol flex="auto"><div className="grid-content bg-green">auto</div></SlCol>
      </SlRow>
      <SlRow>
        <SlCol flex={1}><div className="grid-content bg-blue">1</div></SlCol>
        <SlCol flex={2}><div className="grid-content bg-green">2</div></SlCol>
        <SlCol flex={1}><div className="grid-content bg-blue">1</div></SlCol>
      </SlRow>
    </div>
    <style>{css}</style>
  </>
);
```

## 响应式布局

使用 `xs`、`sm`、`md`、`lg`、`xl`、`xxl` 属性实现响应式布局。

断点说明：
- `xs`: < 576px
- `sm`: ≥ 576px
- `md`: ≥ 768px
- `lg`: ≥ 992px
- `xl`: ≥ 1200px
- `xxl`: ≥ 1600px

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <SlRow>
      <SlCol xs={24} sm={12} md={8} lg={6}><div className="grid-content bg-blue">Col</div></SlCol>
      <SlCol xs={24} sm={12} md={8} lg={6}><div className="grid-content bg-green">Col</div></SlCol>
      <SlCol xs={24} sm={12} md={8} lg={6}><div className="grid-content bg-blue">Col</div></SlCol>
      <SlCol xs={24} sm={12} md={8} lg={6}><div className="grid-content bg-green">Col</div></SlCol>
    </SlRow>
    <style>{css}</style>
  </>
);
```

## 响应式对象配置

响应式属性也可以传入对象，包含 `span`、`offset` 等属性。

```jsx
import React from "react";
import SlRow from '@kdcloudjs/shoelace/dist/react/row/index.js';
import SlCol from '@kdcloudjs/shoelace/dist/react/col/index.js';

const css = `
  .grid-content { padding: 16px; text-align: center; color: white; border-radius: 4px; }
  .bg-blue { background: #0092ff; }
  .bg-green { background: #00a854; }
`;

export default () => (
  <>
    <SlRow>
      <SlCol xs={{ span: 24 }} md={{ span: 12 }} lg={{ span: 8, offset: 4 }}>
        <div className="grid-content bg-blue">Col</div>
      </SlCol>
      <SlCol xs={{ span: 24 }} md={{ span: 12 }} lg={{ span: 8 }}>
        <div className="grid-content bg-green">Col</div>
      </SlCol>
    </SlRow>
    <style>{css}</style>
  </>
);
```

## Row Properties

| 属性    | 描述                                                                 | 类型                                                                           | 默认值    |
| ------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------- |
| gutter  | 栅格间隔，可以是数字或数组 `[水平间距, 垂直间距]`，支持响应式对象    | `number \| [number, number] \| object`                                         | `0`       |
| justify | 水平排列方式                                                         | `'start' \| 'end' \| 'center' \| 'space-around' \| 'space-between' \| 'space-evenly'` | `'start'` |
| align   | 垂直对齐方式                                                         | `'top' \| 'middle' \| 'bottom' \| 'stretch'`                                   | `'top'`   |
| wrap    | 是否自动换行                                                         | `boolean`                                                                      | `true`    |

## Col Properties

| 属性   | 描述                                                       | 类型                        | 默认值      |
| ------ | ---------------------------------------------------------- | --------------------------- | ----------- |
| span   | 栅格占位格数（0-24）                                       | `number`                    | -           |
| offset | 栅格左侧偏移格数                                           | `number`                    | `0`         |
| order  | 栅格顺序                                                   | `number`                    | `0`         |
| push   | 栅格向右移动格数                                           | `number`                    | `0`         |
| pull   | 栅格向左移动格数                                           | `number`                    | `0`         |
| flex   | flex 布局属性                                              | `string \| number`          | -           |
| xs     | `< 576px` 响应式栅格，可为数字或包含其他属性的对象         | `number \| object`          | -           |
| sm     | `≥ 576px` 响应式栅格                                       | `number \| object`          | -           |
| md     | `≥ 768px` 响应式栅格                                       | `number \| object`          | -           |
| lg     | `≥ 992px` 响应式栅格                                       | `number \| object`          | -           |
| xl     | `≥ 1200px` 响应式栅格                                      | `number \| object`          | -           |
| xxl    | `≥ 1600px` 响应式栅格                                      | `number \| object`          | -           |

## 常见问题

### Q: 为什么列没有按预期宽度显示？

A: 确保 `span` 属性值正确（0-24），且所有列的 `span` 之和不超过 24。如果超过 24，多余的列会换行显示。

### Q: 如何实现响应式布局？

A: 使用 `xs`、`sm`、`md`、`lg`、`xl`、`xxl` 属性，可以传入数字或对象：
```jsx
<SlCol xs={24} sm={12} md={8} lg={6} />
// 或
<SlCol xs={{ span: 24 }} md={{ span: 12, offset: 6 }} />
```

### Q: gutter 间距没有生效？

A: 确保 `gutter` 属性设置在 `SlRow` 上，而不是 `SlCol` 上。
