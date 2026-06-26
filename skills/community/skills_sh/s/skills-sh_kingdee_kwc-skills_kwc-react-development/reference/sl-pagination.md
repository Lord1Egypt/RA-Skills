# Pagination 分页器

用于数据分页展示的控件，支持页码跳转和每页条数设置。

## 特性概览

- **双模式切换**：支持标准模式和简洁模式 (`simpleMode`)
- **页码跳转**：支持输入页码快速跳转（标准模式）
- **每页条数**：支持自定义每页显示条数选项
- **受控/非受控**：支持受控模式 (`currentPage`) 和非受控模式 (`defaultCurrentPage`)
- **禁用状态**：支持整体禁用交互

## 基础用法

最简单的分页器用法，使用默认配置。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => <SlPagination />;
```

## 设置总数据量

使用 `total` 属性设置总数据量，组件会自动计算总页数。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => <SlPagination total={1000} />;
```

## 设置每页条数

使用 `pageSize` 属性设置每页显示的条数，默认为 20。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => <SlPagination total={500} pageSize={50} />;
```

## 自定义每页条数选项

使用 `pageSizeOpts` 属性（传入数组）自定义下拉菜单中的每页条数选项。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => (
  <SlPagination total={1000} pageSize={25} pageSizeOpts={[25, 50, 100, 200]} />
);
```

## 设置默认页码

使用 `defaultCurrentPage` 属性设置默认显示的页码（非受控模式）。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => <SlPagination total={500} defaultCurrentPage={5} />;
```

## 受控模式

使用 `currentPage` 属性进行受控模式，页码由外部状态管理。通过 `onSlPageChange` 监听页码变化并更新状态。

```jsx
import React, { useState, useCallback } from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => {
  const [currentPage, setCurrentPage] = useState(1);

  const handlePageChange = useCallback((event) => {
    const { pageNumber } = event.detail;
    setCurrentPage(pageNumber);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
      <p style={{ fontSize: "14px", color: "#666" }}>当前页码: {currentPage}</p>
      <SlPagination
        total={500}
        currentPage={currentPage}
        onSlPageChange={handlePageChange}
      />
    </div>
  );
};
```

## 简洁模式

使用 `simpleMode` 属性启用简洁模式，只显示上一页/下一页按钮和每页条数选择器，不显示页码输入框和总页数信息。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => <SlPagination total={500} simpleMode />;
```

## 禁用状态

使用 `disabled` 属性禁用分页器的所有交互。

```jsx
import React from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => <SlPagination total={500} disabled />;
```

## 监听分页事件

使用 `onSlPageChange` 属性监听 `sl-page-change` 事件，获取页码变化和每页条数变化。事件的 `detail` 对象包含 `pageNumber`（当前页码）和 `pageSize`（每页条数）。

```jsx
import React, { useState, useCallback } from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

export default () => {
  const [pageNumber, setPageNumber] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const handlePageChange = useCallback((event) => {
    const { pageNumber, pageSize } = event.detail;
    setPageNumber(pageNumber);
    setPageSize(pageSize);
    console.log(`请求第 ${pageNumber} 页数据，每页 ${pageSize} 条`);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
      <div style={{ padding: "8px", background: "#f5f5f5", borderRadius: "4px", fontSize: "14px" }}>
        <p style={{ margin: "4px 0" }}>当前页码: {pageNumber}</p>
        <p style={{ margin: "4px 0" }}>每页条数: {pageSize}</p>
      </div>
      <SlPagination total={1000} onSlPageChange={handlePageChange} />
    </div>
  );
};
```

## 动态更新分页器

通过 `ref` 动态更新分页器的属性。

```jsx
import React, { useRef } from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const paginationRef = useRef(null);

  const handleSetPage = () => {
    if (paginationRef.current) {
      paginationRef.current.currentPage = 5;
    }
  };

  const handleSetSize = () => {
    if (paginationRef.current) {
      paginationRef.current.pageSize = 50;
    }
  };

  const handleReset = () => {
    if (paginationRef.current) {
      paginationRef.current.currentPage = 1;
      paginationRef.current.pageSize = 20;
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton size="small" onClick={handleSetPage}>跳转到第5页</SlButton>
        <SlButton size="small" onClick={handleSetSize}>设置每页50条</SlButton>
        <SlButton size="small" onClick={handleReset}>重置</SlButton>
      </div>
      <SlPagination ref={paginationRef} total={500} />
    </div>
  );
};
```

## 事件处理最佳实践

`sl-page-change` 事件在 React 中使用 `onSlPageChange` 属性绑定（遵循 `onSl*` 命名规范）：

```jsx
import React, { useCallback } from "react";
import SlPagination from '@kdcloudjs/shoelace/dist/react/pagination/index.js';

const handlePageChange = useCallback((event) => {
  const { pageNumber, pageSize } = event.detail;
  console.log('当前页:', pageNumber);
  console.log('每页条数:', pageSize);
}, []);

<SlPagination total={500} onSlPageChange={handlePageChange} />
```

## Properties

| 属性               | 描述                                     | 类型       | 默认值              |
| ------------------ | ---------------------------------------- | ---------- | ------------------- |
| currentPage        | 当前页码（受控模式）                     | `number`   | -                   |
| defaultCurrentPage | 默认页码（非受控模式）                   | `number`   | `1`                 |
| pageSize           | 每页显示条数                             | `number`   | `20`                |
| pageSizeOpts       | 每页条数选项                             | `number[]` | `[10, 20, 50, 100]` |
| total              | 数据总条数                               | `number`   | `5000`              |
| disabled           | 是否禁用分页器                           | `boolean`  | `false`             |
| simpleMode         | 是否使用简洁模式（隐藏页码输入和总页数） | `boolean`  | `false`             |
| className          | 自定义 CSS 类名                          | `string`   | `''`                |

## Events

| 事件名称       | JSX 属性          | 描述                       | 事件详情                                        |
| -------------- | ----------------- | -------------------------- | ----------------------------------------------- |
| sl-page-change | `onSlPageChange`  | 页码或每页条数变化时触发   | `{ pageNumber: number, pageSize: number }`      |

## CSS Custom Properties

| CSS 属性                                         | 描述                   | 默认值                                          |
| ------------------------------------------------ | ---------------------- | ----------------------------------------------- |
| --sl-pagination-text-color                       | 文字颜色               | `var(--sl-color-neutral-600)`                   |
| --sl-pagination-current-page-color               | 当前页码颜色           | `var(--sl-color-neutral-900)`                   |
| --sl-pagination-font-size                        | 字体大小               | `var(--sl-font-size-small)`                     |
| --sl-pagination-current-page-border-width        | 页码输入框边框宽度     | `var(--sl-input-border-width)`                  |
| --sl-pagination-current-page-border-radius       | 页码输入框圆角         | `var(--sl-input-border-radius-small)`           |
| --sl-pagination-current-page-sizing-width        | 页码输入框宽度         | `3rem`                                          |
| --sl-pagination-current-page-background          | 页码输入框背景色       | `var(--sl-input-background-color)`              |
| --sl-pagination-current-page-background-disabled | 禁用时背景色           | `var(--sl-input-background-color-disabled)`     |
| --sl-pagination-current-page-border              | 页码输入框边框颜色     | `var(--sl-input-border-color)`                  |
| --sl-pagination-current-page-border-hover        | 悬停时边框颜色         | `var(--sl-input-border-color-focus)`            |
| --sl-pagination-current-page-border-active       | 激活时边框颜色         | `var(--sl-input-border-color-focus)`            |
| --sl-pagination-icon-font-size                   | 图标大小               | `1rem`                                          |
| --sl-pagination-icon-font                        | 图标颜色               | `var(--sl-color-neutral-600)`                   |
| --sl-pagination-icon-font-hover                  | 悬停时图标颜色         | `var(--sl-color-primary-600)`                   |
| --sl-pagination-icon-font-disabled               | 禁用时图标颜色         | `var(--sl-color-neutral-400)`                   |

## 常见问题

### Q: 为什么页码切换后没有触发事件？

A: 请确保使用 `onSlPageChange` 属性绑定事件处理函数，例如：`<SlPagination onSlPageChange={handlePageChange} />`。

### Q: 如何在简洁模式下显示当前页码？

A: 简洁模式不显示页码输入框。如需显示当前页码，可以监听 `sl-page-change` 事件并在自定义元素中显示。

### Q: 如何动态更新总数据量？

A: 通过 `ref` 直接设置 `pagination.total = newTotal`，组件会自动重新计算总页数。如果当前页码超出新的总页数，会自动调整到最后一页。

### Q: 受控模式 vs 非受控模式有什么区别？

A: 
- **非受控模式**：使用 `defaultCurrentPage`，组件内部管理状态。
- **受控模式**：使用 `currentPage`，需要在 `onSlPageChange` 回调中更新状态。
