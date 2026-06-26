# sl-think 思考组件

Think 组件用于展示 AI 模型的思考过程，支持可展开/折叠的内容区域，适用于展示推理、分析等思维链内容。

## 特性概览

| 特性 | 说明 |
|------|------|
| **可展开/折叠** | 点击状态栏可展开或收起内容区域，支持平滑动画过渡 |
| **加载状态** | 支持 `loading` 属性，状态图标替换为加载动画 |
| **闪烁效果** | 支持 `blink` 属性，标题文字添加脉冲动画效果 |
| **受控/非受控** | 支持 `expanded` 属性控制展开状态，或通过事件监听实现受控模式 |
| **自定义图标** | 通过 `icon` 和 `loading-icon` 插槽自定义状态栏图标 |
| **自定义标题** | 通过 `title` 插槽实现富文本标题内容 |
| **CSS 自定义** | 支持 CSS Parts 和 Design Token 自定义样式 |

---

## 基础用法

最简单的思考组件，显示一个可展开/折叠的内容区域。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';

export default () => (
  <SlThink className="basic-think" title="深度思考">
    让我分析一下这个问题... 首先，我们需要考虑几个关键因素。
    基于以上分析，我认为最佳方案是...
  </SlThink>
);
```

---

## 加载状态

使用 `loading` 属性来显示加载状态，状态图标会替换为加载动画。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';

export default () => (
  <SlThink className="loading-think" title="正在思考中..." loading>
    AI 正在分析您的问题...
  </SlThink>
);
```

---

## 闪烁效果

使用 `blink` 属性为标题文字添加闪烁动画效果，用于表示正在进行中的状态。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';

export default () => (
  <SlThink className="blink-think" title="思考中" loading blink>
    正在进行深度分析...
  </SlThink>
);
```

---

## 默认折叠

通过设置 `expanded` 属性为 `false`，可以让内容默认处于折叠状态。

```jsx
import React, { useState } from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';

export default () => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <SlThink 
      className="collapsed-think" 
      title="点击展开查看思考过程" 
      expanded={isExpanded}
    >
      这是折叠状态下的内容，点击状态栏可以展开。
    </SlThink>
  );
};
```

---

## 受控模式

通过监听 `sl-expand` 和 `sl-collapse` 事件来控制展开/折叠状态。

```jsx
import React, { useState, useCallback } from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';

export default () => {
  const [isExpanded, setIsExpanded] = useState(true);

  const statusText = isExpanded ? '已展开' : '已折叠';

  const handleExpand = useCallback(() => {
    setIsExpanded(true);
  }, []);

  const handleCollapse = useCallback(() => {
    setIsExpanded(false);
  }, []);

  return (
    <div>
      <SlThink
        className="controlled-think"
        title="受控模式示例"
        expanded={isExpanded}
        onSlExpand={handleExpand as any}
        onSlCollapse={handleCollapse as any}
      >
        这是一个受控模式的示例，展开状态由父组件管理。
      </SlThink>
      <div 
        style={{ 
          marginTop: 'var(--sl-spacing-medium)', 
          fontSize: 'var(--sl-font-size-small)', 
          color: 'var(--sl-color-neutral-600)' 
        }}
      >
        当前状态: {statusText}
      </div>
    </div>
  );
};
```

---

## 自定义图标

使用 `icon` 插槽来自定义状态栏图标，使用 `loading-icon` 插槽来自定义加载图标。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';
import SlSpinner from '@kdcloudjs/shoelace/dist/react/spinner/index.js';

export default () => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sl-spacing-medium)' }}>
    <SlThink className="custom-icon-think" title="自定义图标">
      <SlIcon slot="icon" name="lightbulb" />
      使用灯泡图标表示思考...
    </SlThink>

    <SlThink className="custom-loading-think" title="自定义加载图标" loading>
      <SlSpinner slot="loading-icon" style={{ fontSize: 'var(--sl-font-size-medium)' }} />
      正在加载中...
    </SlThink>
  </div>
);
```

---

## 自定义标题

使用 `title` 插槽来自定义富文本标题内容。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';
import SlBadge from '@kdcloudjs/shoelace/dist/react/badge/index.js';

export default () => (
  <SlThink className="custom-title-think">
    <span 
      slot="title" 
      style={{ display: 'flex', alignItems: 'center', gap: 'var(--sl-spacing-small)' }}
    >
      深度分析
      <SlBadge variant="primary" pill>AI</SlBadge>
    </span>
    这是使用富文本标题的示例。
  </SlThink>
);
```

---

## 自定义样式

通过 CSS 自定义属性来定制闪烁动画的颜色。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';

const css = `
  .custom-blink-think {
    --sl-c-think-TitleTextBlink-color-default: var(--sl-color-primary-500);
    --sl-c-think-TitleTextBlink-color: var(--sl-color-primary-700);
  }
`;

export default () => (
  <>
    <SlThink className="custom-blink-think" title="自定义闪烁颜色" loading blink>
      使用主题色的闪烁效果。
    </SlThink>
    <style>{css}</style>
  </>
);
```

---

## 程序化控制展开/折叠

通过状态变量程序化控制展开和折叠状态。

```jsx
import React, { useState, useCallback } from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const [isExpanded, setIsExpanded] = useState(true);

  const handleExpand = useCallback(() => {
    setIsExpanded(true);
  }, []);

  const handleCollapse = useCallback(() => {
    setIsExpanded(false);
  }, []);

  return (
    <div>
      <div 
        style={{ 
          marginBottom: 'var(--sl-spacing-medium)', 
          display: 'flex', 
          gap: 'var(--sl-spacing-small)' 
        }}
      >
        <SlButton size="small" onClick={handleExpand}>展开</SlButton>
        <SlButton size="small" onClick={handleCollapse}>折叠</SlButton>
      </div>
      <SlThink
        className="programmatic-think"
        title="程序化控制示例"
        expanded={isExpanded}
      >
        通过按钮修改 isExpanded 状态来控制展开/折叠状态。
      </SlThink>
    </div>
  );
};
```

---

## 完整示例

综合使用各种功能的完整示例。

```jsx
import React from "react";
import SlThink from '@kdcloudjs/shoelace/dist/react/think/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

const css = `
  .think-container {
    display: flex;
    flex-direction: column;
    gap: var(--sl-spacing-medium);
  }
`;

export default () => (
  <>
    <div className="think-container">
      {/* 基础用法 */}
      <SlThink className="think-basic" title="基础思考">
        这是一个基础的思考过程展示。
      </SlThink>

      {/* 加载中 */}
      <SlThink className="think-loading" title="AI 正在思考..." loading blink>
        正在分析您的问题，请稍候...
      </SlThink>

      {/* 带自定义图标 */}
      <SlThink className="think-custom" title="深度推理">
        <SlIcon slot="icon" name="cpu" />
        使用自定义图标展示思考过程。
      </SlThink>
    </div>
    <style>{css}</style>
  </>
);
```

---

## API 参考

### `SlThink` 属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | `string` | `''` | 状态栏中显示的标题文本。如需显示 HTML 内容，请使用 `title` 插槽。 |
| `loading` | `boolean` | `false` | 为 `true` 时，状态图标替换为加载动画（或 `loading-icon` 插槽中的自定义内容）。 |
| `expanded` | `boolean` | `true` | 内容区域是否展开。可通过此属性控制展开/折叠状态。 |
| `defaultExpanded` | `boolean` | `true` | 组件首次渲染时的初始展开状态。仅当 `expanded` 属性未设置时生效。 |
| `blink` | `boolean` | `false` | 为 `true` 时，标题文字应用闪烁动画效果，用于表示正在进行中的活动状态。 |

### `SlThink` 插槽

| 插槽 | 说明 |
|------|------|
| _(默认)_ | 思考内容的主体区域。 |
| `title` | 状态栏的标题内容（富文本）。如果只需要纯文本，可使用 `title` 属性。 |
| `icon` | 未加载时显示的自定义图标，默认为思考图标。 |
| `loading-icon` | 加载状态时显示的自定义图标，默认为 Spinner 加载动画。 |

### `SlThink` 事件

| 事件 | React 属性 | 说明 | 事件详情 |
|------|------------|------|----------|
| `sl-expand` | `onSlExpand` | 当内容区域开始展开时触发（动画前）。 | - |
| `sl-collapse` | `onSlCollapse` | 当内容区域开始折叠时触发（动画前）。 | - |

### `SlThink` CSS Parts

| Part | 说明 |
|------|------|
| `base` | 组件的基础包装器。 |
| `status` | 可点击的状态栏（图标 + 标题 + 箭头）。 |
| `status-icon` | 状态栏中的图标容器。 |
| `status-text` | 状态栏中的标题文本区域。 |
| `chevron` | 展开/折叠的箭头指示器。 |
| `body` | 可折叠的内容容器。 |
| `content` | body 内部的内容区域。 |

### `SlThink` CSS 自定义属性

| 属性 | 说明 | 默认值 |
|------|------|--------|
| `--sl-c-think-TitleTextBlink-color-default` | 闪烁动画期间的基础文本颜色。 | `rgba(0, 0, 0, 0.45)` |
| `--sl-c-think-TitleTextBlink-color` | 闪烁高亮（光束）颜色。 | `#000` |

---

## 交互行为说明

1. **展开/折叠**：点击状态栏可切换内容的展开/折叠状态，带有平滑的高度过渡动画。
2. **受控 vs 非受控**：
   - 非受控模式：使用 `defaultExpanded` 设置初始展开状态，组件内部管理后续状态变化。
   - 受控模式：使用 `expanded` 属性，需在 `onSlExpand` 和 `onSlCollapse` 事件回调中手动更新该属性。
3. **加载状态**：`loading` 为 `true` 时，状态图标替换为加载动画（或 `loading-icon` 插槽中的自定义内容）。
4. **闪烁动画**：`blink` 属性在标题上产生脉冲动画效果，适合标记正在进行的思考过程。

---

## 最佳实践

1. **合理使用加载状态**：用 `loading` 表示思考进行中，配合 `blink` 可以更明显地指示当前状态。
2. **事件处理**：在 React 中使用 `onSlExpand` 和 `onSlCollapse` 属性绑定事件处理函数。
3. **CSS 使用 Design Token**：样式必须使用 Shoelace Design Token，禁止硬编码 hex 色值或 px 数值。

---

## 常见问题

### Q: 如何自定义闪烁动画颜色？

通过 CSS 自定义属性设置：

```jsx
const css = `
  .my-think {
    --sl-c-think-TitleTextBlink-color-default: var(--sl-color-primary-500);
    --sl-c-think-TitleTextBlink-color: var(--sl-color-primary-700);
  }
`;
```

### Q: 如何在 React 中监听展开/折叠事件？

使用 `onSlExpand` 和 `onSlCollapse` 属性：

```jsx
<SlThink
  expanded={isExpanded}
  onSlExpand={() => setIsExpanded(true)}
  onSlCollapse={() => setIsExpanded(false)}
>
  内容
</SlThink>
```

### Q: 受控模式 vs 非受控模式有什么区别？

- **非受控模式**：使用 `defaultExpanded`，组件内部管理状态。
- **受控模式**：使用 `expanded` 属性，需要在 `onSlExpand` 和 `onSlCollapse` 回调中更新状态。
