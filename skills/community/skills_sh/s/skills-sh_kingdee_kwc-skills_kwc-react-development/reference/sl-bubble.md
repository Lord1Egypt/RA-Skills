# Bubble 气泡对话

聊天气泡组件，常用于对话式 UI，支持打字动画、流式输出、编辑模式等特性。

## 特性概览

- **位置控制**：支持 `start`（左对齐）和 `end`（右对齐）两种位置（`placement`）
- **外观变体**：支持 `filled`、`outlined`、`shadow`、`borderless` 四种视觉风格（`variant`）
- **形状样式**：支持 `default`、`round`、`corner` 三种气泡形状（`shape`）
- **加载状态**：支持 `loading` 属性显示加载动画
- **打字动画**：支持逐字显示内容的打字动画效果（`typing`）
- **流式输出**：支持内容流式到达时的持续打字动画（`streaming`）
- **编辑模式**：支持对气泡内容进行编辑（`editable`）
- **丰富插槽**：支持头像、头部、底部、额外内容和自定义加载指示器
- **底部位置**：支持自定义 footer 在内容区域内外的不同位置（`footerPlacement`）
- **CSS 自定义属性**：支持通过 CSS 变量自定义各变体的颜色和样式

## 基础用法

最简单的用法，显示一条聊天气泡消息。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => <SlBubble content="你好，有什么可以帮助你的吗？" />;
```

## 位置

设置 `placement` 属性控制气泡位置，`start` 为左对齐（他人消息），`end` 为右对齐（自己消息）。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => (
  <>
    <SlBubble content="你好，我是助手" placement="start" />
    <SlBubble content="你好！" placement="end" />
  </>
);
```

## 外观变体

通过 `variant` 属性设置气泡外观，支持 `filled`（默认）、`outlined`、`shadow`、`borderless`。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => (
  <>
    <SlBubble content="Filled（默认）" variant="filled" />
    <SlBubble content="Outlined" variant="outlined" />
    <SlBubble content="Shadow" variant="shadow" />
    <SlBubble content="Borderless" variant="borderless" />
  </>
);
```

## 形状

通过 `shape` 属性设置气泡形状，支持 `default`（默认圆角）、`round`（药丸形）、`corner`（聊天缺角）。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => (
  <>
    <SlBubble content="Default" shape="default" />
    <SlBubble content="Round" shape="round" />
    <SlBubble content="Corner" shape="corner" />
  </>
);
```

## 加载状态

设置 `loading` 属性显示加载指示器（三个跳动的点），常用于等待回复。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => <SlBubble loading />;
```

## 打字动画

设置 `typing` 属性启用逐字打字动画，可通过 `typingStep` 和 `typingInterval` 控制速度。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => (
  <SlBubble
    content="这是一段带有打字动画效果的文本内容，逐字显示给用户看。"
    typing
    typingStep={2}
    typingInterval={50}
  />
);
```

## 流式输出

结合 `typing` 和 `streaming` 属性，支持内容流式到达时的持续打字动画。

```jsx
import React, { useState, useEffect, useRef } from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => {
  const [content, setContent] = useState('');
  const [streaming, setStreaming] = useState(true);

  useEffect(() => {
    const chunks = ['你好，', '我正在', '思考你的', '问题...', '这是答案。'];
    let i = 0;
    const timer = setInterval(() => {
      if (i < chunks.length) {
        setContent(prev => prev + chunks[i]);
        i++;
      } else {
        setStreaming(false);
        clearInterval(timer);
      }
    }, 500);
    return () => clearInterval(timer);
  }, []);

  return <SlBubble content={content} typing streaming={streaming} />;
};
```

## 头像插槽

通过 `avatar` 插槽在气泡旁边显示头像，常与 `<SlAvatar>` 组件配合使用。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';
import SlAvatar from '@kdcloudjs/shoelace/dist/react/avatar/index.js';

export default () => (
  <SlBubble content="你好，我是助手">
    <SlAvatar slot="avatar" initials="AI" shape="circle" />
  </SlBubble>
);
```

## 头部和底部插槽

通过 `header` 和 `footer` 插槽添加头部和底部内容。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => (
  <SlBubble content="这是消息内容">
    <span slot="header">助手 · 10:30</span>
    <span slot="footer">已读</span>
  </SlBubble>
);
```

## 底部位置

通过 `footerPlacement` 属性控制底部内容在气泡内外的位置。

```jsx
import React from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => (
  <>
    <SlBubble content="外部底部（左对齐）" footerPlacement="outer-start">
      <span slot="footer">底部内容</span>
    </SlBubble>
    <SlBubble content="内部底部（右对齐）" footerPlacement="inner-end">
      <span slot="footer">底部内容</span>
    </SlBubble>
  </>
);
```

## 编辑模式

设置 `editable` 属性进入编辑模式，内容区域变为可编辑区域，显示确认和取消按钮。

```jsx
import React, { useCallback } from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => {
  const handleEditConfirm = useCallback(event => {
    console.log('编辑确认:', event.detail.content);
  }, []);

  const handleEditCancel = useCallback(() => {
    console.log('编辑取消');
  }, []);

  return (
    <SlBubble
      content="这段内容可以编辑"
      editable
      okText="确认"
      cancelText="取消"
      onSlEditConfirm={handleEditConfirm}
      onSlEditCancel={handleEditCancel}
    />
  );
};
```

## 监听事件

使用 `onSl*` 属性绑定事件处理函数。

```jsx
import React, { useCallback } from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

export default () => {
  const handleTypingComplete = useCallback(() => {
    console.log('打字动画完成');
  }, []);

  const handleEditConfirm = useCallback(event => {
    console.log('编辑确认:', event.detail.content);
  }, []);

  const handleEditCancel = useCallback(() => {
    console.log('编辑取消');
  }, []);

  return (
    <SlBubble
      content="带打字动画的内容"
      typing
      onSlTypingComplete={handleTypingComplete}
      onSlEditConfirm={handleEditConfirm}
      onSlEditCancel={handleEditCancel}
    />
  );
};
```

## Properties

| 属性            | 描述                                             | 类型                                                           | 默认值      |
| --------------- | ------------------------------------------------ | -------------------------------------------------------------- | ----------- |
| placement       | 气泡位置，`start` 左对齐，`end` 右对齐          | `'start' \| 'end'`                                            | `'start'`   |
| content         | 气泡文本内容                                     | `string`                                                       | `''`        |
| variant         | 外观变体                                         | `'filled' \| 'outlined' \| 'shadow' \| 'borderless'`          | `'filled'`  |
| shape           | 气泡形状                                         | `'default' \| 'round' \| 'corner'`                            | `'default'` |
| loading         | 是否显示加载状态                                 | `boolean`                                                      | `false`     |
| typing          | 是否启用打字动画                                 | `boolean`                                                      | `false`     |
| typingStep      | 每步打字显示的字符数                             | `number`                                                       | `2`         |
| typingInterval  | 打字动画每步间隔（毫秒）                         | `number`                                                       | `50`        |
| streaming       | 是否正在流式输出                                 | `boolean`                                                      | `false`     |
| footerPlacement | 底部内容位置                                     | `'outer-start' \| 'outer-end' \| 'inner-start' \| 'inner-end'` | -           |
| editable        | 是否启用编辑模式                                 | `boolean`                                                      | `false`     |
| okText          | 编辑确认按钮文本                                 | `string`                                                       | `'OK'`      |
| cancelText      | 编辑取消按钮文本                                 | `string`                                                       | `'Cancel'`  |

## Events

| 事件名称           | JSX 属性              | 描述                     | 事件详情                  |
| ------------------ | --------------------- | ------------------------ | ------------------------- |
| sl-typing-complete | `onSlTypingComplete`  | 打字动画完成时触发       | -                         |
| sl-edit-confirm    | `onSlEditConfirm`     | 用户确认编辑时触发       | `{ content: string }`     |
| sl-edit-cancel     | `onSlEditCancel`      | 用户取消编辑时触发       | -                         |

## Slots

| 插槽名   | 描述                                              |
| -------- | ------------------------------------------------- |
| (默认)   | 气泡内容的默认插槽，当未设置 `content` 属性时使用 |
| avatar   | 头像区域，配合 `<SlAvatar>` 使用                 |
| header   | 头部内容，显示在气泡内容上方                      |
| footer   | 底部内容，显示在气泡内容下方                      |
| extra    | 额外内容，显示在头像对侧                          |
| loading  | 自定义加载指示器，覆盖默认加载动画                |

## CSS Parts

| Part 名称 | 描述                   |
| --------- | ---------------------- |
| base      | 组件最外层包装器       |
| avatar    | 头像容器               |
| body      | 主体包装器（头部+内容+底部） |
| header    | 头部容器               |
| content   | 主内容气泡区域         |
| footer    | 底部容器               |
| extra     | 额外内容容器           |
| loading   | 默认加载指示器容器     |

## CSS 自定义属性

| 属性名                              | 描述                                     |
| ------------------------------------ | ---------------------------------------- |
| --sl-bubble-filled-background        | `filled` 变体背景色（start 位置）        |
| --sl-bubble-filled-color             | `filled` 变体文字色                      |
| --sl-bubble-filled-background-end    | `filled` 变体背景色（end 位置）          |
| --sl-bubble-filled-color-end         | `filled` 变体文字色（end 位置）          |
| --sl-bubble-outlined-background      | `outlined` 变体背景色                    |
| --sl-bubble-outlined-border-color    | `outlined` 变体边框色                    |
| --sl-bubble-outlined-color           | `outlined` 变体文字色                    |
| --sl-bubble-shadow-background        | `shadow` 变体背景色                      |
| --sl-bubble-shadow-box-shadow        | `shadow` 变体阴影                        |
| --sl-bubble-shadow-color             | `shadow` 变体文字色                      |
| --sl-bubble-borderless-color         | `borderless` 变体文字色                  |
| --sl-bubble-loading-dot-color        | 加载指示器圆点颜色                       |
| --sl-bubble-cursor-color             | 打字光标颜色                             |

## 事件处理最佳实践

`sl-typing-complete` 等事件在 React 中使用 `onSlTypingComplete` 属性绑定（遵循 `onSl*` 命名规范）：

```jsx
import React, { useCallback } from 'react';
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';

const handleTypingComplete = useCallback(() => {
  console.log('打字动画完成');
}, []);

const handleEditConfirm = useCallback(event => {
  console.log('编辑确认:', event.detail.content);
}, []);

<SlBubble onSlTypingComplete={handleTypingComplete} onSlEditConfirm={handleEditConfirm} />;
```

## 最佳实践

### 1. 正确导入组件

```javascript
import SlBubble from '@kdcloudjs/shoelace/dist/react/bubble/index.js';
```

### 2. 属性直接通过 JSX 属性传入

`@lit/react` 的 `createComponent` 会将所有 Lit `@property()` 声明的属性映射为 React props，因此所有属性可以直接传入：

```jsx
<SlBubble
  content="你好"
  variant="outlined"
  shape="round"
  typing
  typingStep={3}
/>
```

### 3. 使用 useCallback 包裹事件处理函数

```jsx
const handleTypingComplete = useCallback(() => {
  console.log('打字完成');
}, []);

<SlBubble onSlTypingComplete={handleTypingComplete} />;
```

### 4. 通过 ref 操作组件

```jsx
const ref = useRef(null);

// 动态更新内容
const appendContent = (text) => {
  if (ref.current) {
    ref.current.content += text;
  }
};

<SlBubble ref={ref} typing streaming />;
```

## 常见问题

### Q: 为什么打字动画没有效果？

A: 打字动画只在通过 `content` 属性设置文本内容时生效，不支持默认插槽内容。请确保同时设置了 `typing` 属性和 `content` 属性。

### Q: 流式输出时何时触发 sl-typing-complete？

A: 当 `streaming` 属性为 `true` 时，即使内容已全部打完，打字动画也会持续等待新内容。只有在 `streaming` 设为 `false` 后，剩余内容输出完毕才会触发 `sl-typing-complete` 事件。

### Q: footerPlacement 的默认值是什么？

A: `footerPlacement` 未设置时，默认根据 `placement` 决定：`placement="start"` 时为 `outer-start`，`placement="end"` 时为 `outer-end`。

### Q: 编辑模式如何获取编辑后的内容？

A: 监听 `onSlEditConfirm` 事件，通过 `event.detail.content` 获取编辑后的文本内容。

### Q: 受控模式 vs 非受控模式有什么区别？

A:

- **非受控模式**：设置初始 `content`，组件内部管理打字状态。
- **受控模式**：使用 `content` 属性 + `streaming`，在回调中动态更新内容（常用于流式输出场景）。
