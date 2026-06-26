# XMarkdown Markdown Renderer

`SlXMarkdown` 用于渲染 Markdown 内容，支持流式输出、代码高亮、`think` / `sources` 增强块，以及将指定 Markdown 节点映射成自定义元素。

## 特性概览

- **Markdown 渲染**：支持标题、段落、列表、表格、图片、链接、引用、代码块
- **流式输出**：通过 `streaming` 控制未完成节点占位符和 tail
- **聊天增强**：内置 `think`、`sources` 两种常见 AI 输出块
- **自定义节点映射**：支持 language、HTML tag、tail、incomplete-* 的映射
- **安全默认值**：`escapeRawHtml` 默认为 `true`
- **主题切换**：内置 `light` / `dark`，也可传自定义 class 名

## 核心约束

- 组件只读取 `content` 属性，不读取 children 里的 Markdown 文本。
- `components` 接受的是 **自定义元素标签名字符串**，不是 React 组件本身。
- `plugins` 与 `streaming` 都是对象/数组，直接通过 JSX prop 传入即可。
- `escapeRawHtml` 默认应该保持开启；只有完全可信的 HTML 内容才能关闭。
- 当前版本 **没有 `onSl*` 事件**，通常靠 React state 更新 `content`、`streaming`、`components` 触发重渲染。

## 基础用法

```jsx
import React from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function BasicDemo() {
  const content = `# Hello

这是 **XMarkdown** 的基础示例。`;

  return <SlXMarkdown content={content} />;
}
```

## 深色主题

```jsx
import React from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function DarkThemeDemo() {
  return (
    <SlXMarkdown
      theme="dark"
      content={`## Dark Theme

> 使用内置 dark 主题渲染 Markdown。`}
    />
  );
}
```

## 流式输出

流式聊天场景中，只要还有后续 chunk，就让 `streaming.hasNextChunk = true`。

```jsx
import React from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function StreamingDemo() {
  return (
    <SlXMarkdown
      content="[Shoelace 官网](https://shoelace.style"
      streaming={{
        hasNextChunk: true,
        tail: { content: '正在生成中...' },
        animationConfig: {
          fadeDuration: 480,
          easing: 'ease-out'
        }
      }}
    />
  );
}
```

## think 和 sources

```jsx
import React from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function ChatBlocksDemo() {
  const content = `\`\`\`think
先比较两个方案的复杂度，再决定最终实现。
\`\`\`

\`\`\`sources
https://shoelace.style
https://x.ant.design/x-markdowns/introduce
\`\`\``;

  return <SlXMarkdown content={content} />;
}
```

## 自定义节点映射

`components` 的 key 通常有这些来源：

- fenced code language，例如 `mermaid`
- 自定义 HTML 标签名，例如 `agent-card`
- 特殊节点，例如 `tail`、`incomplete-link`

被映射的自定义元素会收到这些 property 和 `data-*`：

- `nodeType`
- `streamStatus`
- `textContent`
- `attrs`
- `meta`
- `raw`

```jsx
import React, { useEffect } from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function MermaidDemo() {
  useEffect(() => {
    if (!customElements.get('md-mermaid-viewer')) {
      customElements.define(
        'md-mermaid-viewer',
        class extends HTMLElement {
          connectedCallback() {
            const source = this.textContent || this.dataset.textContent || '';
            this.innerHTML = `<pre>${source}</pre>`;
          }
        }
      );
    }
  }, []);

  return (
    <SlXMarkdown
      content={`\`\`\`mermaid
graph TD;
A-->B;
\`\`\``}
      components={{
        mermaid: 'md-mermaid-viewer'
      }}
    />
  );
}
```

## 自定义未完成节点

业务上需要替换 link / image / heading / table / xml 占位符时，优先使用 `streaming.incompleteMarkdownComponentMap`。

```jsx
import React, { useEffect } from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function IncompleteImageDemo() {
  useEffect(() => {
    if (!customElements.get('md-incomplete-image')) {
      customElements.define(
        'md-incomplete-image',
        class extends HTMLElement {
          connectedCallback() {
            this.textContent = '图片内容尚未生成完成';
          }
        }
      );
    }
  }, []);

  return (
    <SlXMarkdown
      content="![preview](https://static.example.com/demo"
      streaming={{
        hasNextChunk: true,
        incompleteMarkdownComponentMap: {
          image: 'md-incomplete-image'
        }
      }}
    />
  );
}
```

## 插件管线

```jsx
import React from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

const plugins = [
  {
    name: 'doc-link-replacer',
    preprocess(source) {
      return source.replaceAll('[doc:nav]', '[Nav 组件文档](/components/nav)');
    }
  }
];

export default function PluginsDemo() {
  return (
    <SlXMarkdown
      content="这里有一个 [doc:nav] 占位标记。"
      plugins={plugins}
    />
  );
}
```

## 原始 HTML 安全控制

```jsx
import React from 'react';
import SlXMarkdown from '@kdcloudjs/shoelace/dist/react/x-markdown/index.js';

export default function TrustedHtmlDemo() {
  return (
    <SlXMarkdown
      content={`<sl-tag variant="success">可信 HTML</sl-tag>`}
      escapeRawHtml={false}
    />
  );
}
```

## API 概览

### SlXMarkdown

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `content` | 要渲染的 Markdown 内容 | `string` | `''` |
| `components` | 节点映射表，value 必须是自定义元素标签名 | `Record<string, string>` | `{}` |
| `plugins` | Markdown 管线插件 | `SlXMarkdownPlugin[]` | `[]` |
| `theme` | 主题名，支持 `light`、`dark` 或自定义 class 名 | `string` | `'light'` |
| `openLinksInNewTab` | 链接是否新开标签页 | `boolean` | `false` |
| `escapeRawHtml` | 是否转义原始 HTML | `boolean` | `true` |
| `debug` | 本地开发环境下输出调试信息 | `boolean` | `false` |
| `streaming` | 流式渲染配置，传 `false` 表示关闭 | `SlXMarkdownStreamingConfig \| false` | `false` |

### SlXMarkdownStreamingConfig

| 属性 | 说明 | 类型 |
| --- | --- | --- |
| `hasNextChunk` | 后续是否还有流式内容 | `boolean` |
| `incompleteMarkdownComponentMap` | 自定义未完成节点映射，仅支持 `link`、`image`、`heading`、`table`、`xml` | `Partial<Record<...>>` |
| `enableAnimation` | 预留动画开关 | `boolean` |
| `animationConfig` | tail 动画配置 | `{ fadeDuration?: number; easing?: string }` |
| `tail` | tail 展示配置，`true` 使用默认文案，`false` 不展示 | `boolean \| { content?: string; component?: string }` |

## 使用建议

- React 里如果要做 Mermaid、图表、业务卡片渲染，不要把 React 组件直接塞进 `components`，而是注册一个 custom element 再映射过去。
- `components.tail` 与 `streaming.tail.component` 都能接管 tail，自定义 tail 时优先选一种即可，避免重复配置。
- 对话流结束时，把 `hasNextChunk` 切回 `false`，否则 incomplete placeholder 和 tail 会一直保留。
- 只有可信内容才关闭 `escapeRawHtml`；普通富文本需求优先走 Markdown 和 `components`。
- `debug` 只会在本地开发域名下显示，不要把它当作线上调试面板。
