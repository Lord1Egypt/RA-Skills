# FloatButton 悬浮按钮

悬浮按钮固定在页面上，用于全局性的常用操作。

## 特性概览

- **双类型切换**：支持 `default` 和 `primary` 两种按钮类型
- **多形状**：支持 `circle` 圆形和 `square` 方形
- **多尺寸**：支持 `small`、`medium`、`large` 三种尺寸
- **按钮组**：通过 `SlFloatButtonGroup` 组合多个悬浮按钮
- **菜单模式**：支持 `click` 和 `hover` 触发展开菜单
- **受控模式**：通过 `open` 属性手动控制菜单展开/收起
- **链接按钮**：设置 `href` 后渲染为 `<a>` 标签
- **Tooltip**：支持悬浮提示文字
- **禁用状态**：支持整体禁用交互

## 基础用法

最基本的悬浮按钮。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="question-lg" style={{ position: 'absolute', right: 24, bottom: 24 }} />
  </div>
);
```

## 类型

通过 `type` 属性切换按钮类型，支持 `default` 和 `primary`。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="question-lg" type="default" style={{ position: 'absolute', right: 80, bottom: 24 }} />
    <SlFloatButton icon="pencil" type="primary" style={{ position: 'absolute', right: 24, bottom: 24 }} />
  </div>
);
```

## 形状

通过 `shape` 属性设置按钮形状，支持 `circle`（默认）和 `square`。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="chat-dots" shape="circle" style={{ position: 'absolute', right: 80, bottom: 24 }} />
    <SlFloatButton icon="chat-dots" shape="square" style={{ position: 'absolute', right: 24, bottom: 24 }} />
  </div>
);
```

## 尺寸

通过 `size` 属性设置按钮尺寸，支持 `small`、`medium`（默认）和 `large`。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 120,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="star" size="small" style={{ position: 'absolute', right: 140, bottom: 24 }} />
    <SlFloatButton icon="star" size="medium" style={{ position: 'absolute', right: 80, bottom: 24 }} />
    <SlFloatButton icon="star" size="large" style={{ position: 'absolute', right: 12, bottom: 24 }} />
  </div>
);
```

## 带文字描述

当 `shape="square"` 时，可以通过 `content` 插槽添加文字描述。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="chat-dots" shape="square" style={{ position: 'absolute', right: 24, bottom: 24 }}>
      <span slot="content">帮助</span>
    </SlFloatButton>
  </div>
);
```

## Tooltip

通过 `tooltip` 属性设置悬浮提示文字。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="question-lg" tooltip="帮助信息" style={{ position: 'absolute', right: 24, bottom: 24 }} />
  </div>
);
```

## 链接按钮

通过 `href` 属性将悬浮按钮渲染为链接。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton
      icon="github"
      href="https://github.com"
      target="_blank"
      tooltip="GitHub"
      style={{ position: 'absolute', right: 24, bottom: 24 }}
    />
  </div>
);
```

## 禁用状态

通过 `disabled` 属性禁用按钮。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 100,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButton icon="pencil" disabled style={{ position: 'absolute', right: 80, bottom: 24 }} />
    <SlFloatButton icon="pencil" type="primary" disabled style={{ position: 'absolute', right: 24, bottom: 24 }} />
  </div>
);
```

## 按钮组

使用 `SlFloatButtonGroup` 将多个悬浮按钮组合在一起。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';
import SlFloatButtonGroup from '@kdcloudjs/shoelace/dist/react/float-button-group/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 200,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden'
    }}
  >
    <SlFloatButtonGroup style={{ position: 'absolute', right: 24, top: 24 }}>
      <SlFloatButton icon="chat-dots" tooltip="评论" />
      <SlFloatButton icon="person" tooltip="用户" />
      <SlFloatButton icon="gear" tooltip="设置" />
    </SlFloatButtonGroup>
  </div>
);
```

## 菜单模式

通过 `trigger` 属性开启菜单模式，支持 `click` 和 `hover` 两种触发方式。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';
import SlFloatButtonGroup from '@kdcloudjs/shoelace/dist/react/float-button-group/index.js';

export default () => (
  <div
    style={{
      position: 'relative',
      height: 260,
      border: '1px dashed var(--sl-color-neutral-300)',
      borderRadius: 8,
      overflow: 'hidden',
      display: 'flex',
      gap: 200
    }}
  >
    <div style={{ position: 'relative', flex: 1 }}>
      <SlFloatButtonGroup trigger="click" style={{ position: 'absolute', right: 24, bottom: 24 }}>
        <SlFloatButton icon="chat-dots" />
        <SlFloatButton icon="person" />
        <SlFloatButton icon="gear" />
      </SlFloatButtonGroup>
      <div style={{ position: 'absolute', bottom: 4, right: 16, fontSize: 12, color: 'var(--sl-color-neutral-500)' }}>
        click 触发
      </div>
    </div>
    <div style={{ position: 'relative', flex: 1 }}>
      <SlFloatButtonGroup trigger="hover" style={{ position: 'absolute', right: 24, bottom: 24 }}>
        <SlFloatButton icon="chat-dots" />
        <SlFloatButton icon="person" />
        <SlFloatButton icon="gear" />
      </SlFloatButtonGroup>
      <div style={{ position: 'absolute', bottom: 4, right: 16, fontSize: 12, color: 'var(--sl-color-neutral-500)' }}>
        hover 触发
      </div>
    </div>
  </div>
);
```

## 展开方向

通过 `placement` 属性设置菜单展开方向，支持 `top`（默认）、`right`、`bottom`、`left`。

```jsx
import React from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';
import SlFloatButtonGroup from '@kdcloudjs/shoelace/dist/react/float-button-group/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

export default () => (
  <div style={{ position: 'relative', height: 300, border: '1px dashed var(--sl-color-neutral-300)', borderRadius: 8 }}>
    <SlFloatButtonGroup
      trigger="click"
      placement="top"
      style={{ position: 'absolute', left: '50%', top: 80, transform: 'translateX(-50%)' }}
    >
      <SlIcon slot="trigger-icon" name="chevron-up" />
      <SlFloatButton icon="chat-dots" />
      <SlFloatButton icon="person" />
    </SlFloatButtonGroup>

    <SlFloatButtonGroup
      trigger="click"
      placement="bottom"
      style={{ position: 'absolute', left: '50%', bottom: 80, transform: 'translateX(-50%)' }}
    >
      <SlIcon slot="trigger-icon" name="chevron-down" />
      <SlFloatButton icon="chat-dots" />
      <SlFloatButton icon="person" />
    </SlFloatButtonGroup>

    <SlFloatButtonGroup
      trigger="click"
      placement="left"
      style={{ position: 'absolute', right: '50%', top: '50%', transform: 'translate(-24px, -50%)' }}
    >
      <SlIcon slot="trigger-icon" name="chevron-left" />
      <SlFloatButton icon="chat-dots" />
      <SlFloatButton icon="person" />
    </SlFloatButtonGroup>

    <SlFloatButtonGroup
      trigger="click"
      placement="right"
      style={{ position: 'absolute', left: '50%', top: '50%', transform: 'translate(24px, -50%)' }}
    >
      <SlIcon slot="trigger-icon" name="chevron-right" />
      <SlFloatButton icon="chat-dots" />
      <SlFloatButton icon="person" />
    </SlFloatButtonGroup>
  </div>
);
```

## 返回顶部

利用悬浮按钮实现"返回顶部"功能。滚动下方区域查看效果。

```jsx
import React, { useRef, useState, useCallback } from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => {
  const scrollerRef = useRef(null);
  const [visible, setVisible] = useState(false);

  const handleScroll = useCallback(() => {
    setVisible(scrollerRef.current.scrollTop > 100);
  }, []);

  const handleBackTop = useCallback(() => {
    scrollerRef.current.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  return (
    <div
      style={{
        position: 'relative',
        height: 200,
        border: '1px dashed var(--sl-color-neutral-300)',
        borderRadius: 8,
        overflow: 'hidden'
      }}
    >
      <div ref={scrollerRef} onScroll={handleScroll} style={{ height: '100%', overflowY: 'auto', padding: 16 }}>
        <p>向下滚动查看返回顶部按钮 ↓</p>
        <div
          style={{
            height: 600,
            background: 'linear-gradient(to bottom, var(--sl-color-neutral-100), var(--sl-color-neutral-300))',
            borderRadius: 4,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--sl-color-neutral-500)'
          }}
        >
          滚动区域
        </div>
      </div>
      {visible && (
        <SlFloatButton
          icon="arrow-up"
          type="primary"
          tooltip="返回顶部"
          style={{ position: 'absolute', right: 24, bottom: 24 }}
          onSlClick={handleBackTop}
        />
      )}
    </div>
  );
};
```

## 受控模式

通过 `open` 属性手动控制菜单的展开与收起。通过 `onSlShow` 和 `onSlHide` 监听菜单状态变化并更新状态。

```jsx
import React, { useState, useCallback } from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';
import SlFloatButtonGroup from '@kdcloudjs/shoelace/dist/react/float-button-group/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const [open, setOpen] = useState(false);

  const handleShow = useCallback(() => {
    setOpen(true);
  }, []);

  const handleHide = useCallback(() => {
    setOpen(false);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div
        style={{
          position: 'relative',
          height: 200,
          border: '1px dashed var(--sl-color-neutral-300)',
          borderRadius: 8,
          overflow: 'hidden'
        }}
      >
        <SlFloatButtonGroup
          trigger="click"
          open={open}
          onSlShow={handleShow}
          onSlHide={handleHide}
          style={{ position: 'absolute', right: 24, bottom: 24 }}
        >
          <SlFloatButton icon="chat-dots" />
          <SlFloatButton icon="person" />
          <SlFloatButton icon="gear" />
        </SlFloatButtonGroup>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <SlButton size="small" onClick={() => setOpen(true)}>
          展开
        </SlButton>
        <SlButton size="small" onClick={() => setOpen(false)}>
          收起
        </SlButton>
        <SlButton size="small" variant="primary" onClick={() => setOpen(o => !o)}>
          切换
        </SlButton>
      </div>
    </div>
  );
};
```

## 监听点击事件

使用 `onSlClick` 属性监听 `sl-click` 事件，响应按钮点击。事件在 React 中使用 `onSlClick` 属性绑定（遵循 `onSl*` 命名规范）。

```jsx
import React, { useState, useCallback } from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';

export default () => {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div
        style={{
          position: 'relative',
          height: 100,
          border: '1px dashed var(--sl-color-neutral-300)',
          borderRadius: 8,
          overflow: 'hidden'
        }}
      >
        <SlFloatButton
          icon="bell"
          type="primary"
          style={{ position: 'absolute', right: 24, bottom: 24 }}
          onSlClick={handleClick}
        />
      </div>
      <div
        style={{
          padding: '8px 12px',
          fontSize: 14,
          borderRadius: 4,
          background: 'var(--sl-color-neutral-100)',
          color: 'var(--sl-color-neutral-700)'
        }}
      >
        {count > 0 ? `🔔 点击了 ${count} 次` : '点击悬浮按钮试试'}
      </div>
    </div>
  );
};
```

## 动态更新悬浮按钮

通过 `ref` 动态更新悬浮按钮的属性。

```jsx
import React, { useRef, useCallback } from 'react';
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const floatBtnRef = useRef(null);

  const handleSetPrimary = useCallback(() => {
    if (floatBtnRef.current) {
      floatBtnRef.current.type = 'primary';
    }
  }, []);

  const handleSetDefault = useCallback(() => {
    if (floatBtnRef.current) {
      floatBtnRef.current.type = 'default';
    }
  }, []);

  const handleToggleDisabled = useCallback(() => {
    if (floatBtnRef.current) {
      floatBtnRef.current.disabled = !floatBtnRef.current.disabled;
    }
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ display: 'flex', gap: 8 }}>
        <SlButton size="small" onClick={handleSetPrimary}>
          设为 Primary
        </SlButton>
        <SlButton size="small" onClick={handleSetDefault}>
          设为 Default
        </SlButton>
        <SlButton size="small" onClick={handleToggleDisabled}>
          切换禁用
        </SlButton>
      </div>
      <div
        style={{
          position: 'relative',
          height: 100,
          border: '1px dashed var(--sl-color-neutral-300)',
          borderRadius: 8,
          overflow: 'hidden'
        }}
      >
        <SlFloatButton ref={floatBtnRef} icon="star" style={{ position: 'absolute', right: 24, bottom: 24 }} />
      </div>
    </div>
  );
};
```

## 事件处理最佳实践

`sl-click` 事件在 React 中使用 `onSlClick` 属性绑定（遵循 `onSl*` 命名规范）；`sl-show` 和 `sl-hide` 事件分别使用 `onSlShow` 和 `onSlHide`：

```jsx
import React, { useCallback } from "react";
import SlFloatButton from '@kdcloudjs/shoelace/dist/react/float-button/index.js';
import SlFloatButtonGroup from '@kdcloudjs/shoelace/dist/react/float-button-group/index.js';

const handleClick = useCallback(() => {
  console.log('悬浮按钮被点击');
}, []);

const handleShow = useCallback(() => {
  console.log('菜单展开');
}, []);

const handleHide = useCallback(() => {
  console.log('菜单收起');
}, []);

<SlFloatButton icon="star" onSlClick={handleClick} />

<SlFloatButtonGroup trigger="click" onSlShow={handleShow} onSlHide={handleHide}>
  <SlFloatButton icon="chat-dots" />
  <SlFloatButton icon="person" />
</SlFloatButtonGroup>
```

## Properties

### sl-float-button

| 属性             | 描述                                | 类型                                     | 默认值      |
| ---------------- | ----------------------------------- | ---------------------------------------- | ----------- |
| type             | 按钮类型                            | `'default' \| 'primary'`                 | `'default'` |
| shape            | 按钮形状                            | `'circle' \| 'square'`                   | `'circle'`  |
| size             | 按钮尺寸                            | `'small' \| 'medium' \| 'large'`         | `'medium'`  |
| icon             | 图标名称（来自注册的图标库）        | `string`                                 | `''`        |
| tooltip          | 悬浮提示文字                        | `string`                                 | `''`        |
| tooltipPlacement | 提示文字方向                        | `'top' \| 'right' \| 'bottom' \| 'left'` | `'left'`    |
| disabled         | 是否禁用                            | `boolean`                                | `false`     |
| href             | 链接地址（设置后渲染为 `<a>` 标签） | `string`                                 | `''`        |
| target           | 链接打开方式（仅 href 设置时有效）  | `string`                                 | `''`        |

### sl-float-button-group

| 属性      | 描述                               | 类型                                     | 默认值     |
| --------- | ---------------------------------- | ---------------------------------------- | ---------- |
| shape     | 子按钮形状                         | `'circle' \| 'square'`                   | `'circle'` |
| trigger   | 菜单触发方式（设置后启用菜单模式） | `'click' \| 'hover' \| ''`               | `''`       |
| open      | 菜单是否展开（受控模式）           | `boolean`                                | `false`    |
| placement | 菜单展开方向                       | `'top' \| 'right' \| 'bottom' \| 'left'` | `'top'`    |

## Events

### sl-float-button

| 事件名称 | JSX 属性    | 描述             | 事件详情 |
| -------- | ----------- | ---------------- | -------- |
| sl-click | `onSlClick` | 按钮被点击时触发 | -        |

### sl-float-button-group

| 事件名称 | JSX 属性   | 描述           | 事件详情 |
| -------- | ---------- | -------------- | -------- |
| sl-show  | `onSlShow` | 菜单展开时触发 | -        |
| sl-hide  | `onSlHide` | 菜单收起时触发 | -        |

## Slots

### sl-float-button

| 插槽名    | 描述                                   |
| --------- | -------------------------------------- |
| (default) | 按钮图标内容                           |
| content   | 文字描述（仅 `shape="square"` 时可见） |

### sl-float-button-group

| 插槽名       | 描述               |
| ------------ | ------------------ |
| (default)    | 悬浮按钮列表       |
| trigger-icon | 自定义触发按钮图标 |
| close-icon   | 自定义关闭图标     |

## CSS Parts

### sl-float-button

| Part    | 描述           |
| ------- | -------------- |
| base    | 按钮的基础容器 |
| icon    | 图标容器       |
| content | 文字内容容器   |

### sl-float-button-group

| Part         | 描述                 |
| ------------ | -------------------- |
| base         | 组的基础容器         |
| list         | 按钮列表容器         |
| trigger      | 触发按钮（菜单模式） |
| trigger-icon | 触发按钮图标         |

## 常见问题

### Q: 为什么点击悬浮按钮后没有触发事件？

A: 请确保使用 `onSlClick` 属性绑定事件处理函数，例如：`<SlFloatButton onSlClick={handleClick} />`。

### Q: 如何在菜单模式下监听展开/收起？

A: 使用 `onSlShow` 和 `onSlHide` 属性监听菜单状态变化，例如：`<SlFloatButtonGroup trigger="click" onSlShow={handleShow} onSlHide={handleHide} />`。

### Q: 受控模式 vs 非受控模式有什么区别？

A:

- **非受控模式**：不设置 `open` 属性，组件内部管理菜单展开状态。
- **受控模式**：使用 `open` 属性，需要在 `onSlShow` / `onSlHide` 回调中更新状态。

### Q: 如何动态更新悬浮按钮属性？

A: 通过 `ref` 直接设置属性，如 `floatBtnRef.current.type = 'primary'`，组件会自动更新渲染。
