# sl-thought-chain 思维链组件 React 使用指南

## 概述

ThoughtChain（思维链）用于可视化和追踪 Agent 的调用链路，以垂直连接的节点列表展示 AI 推理或执行过程中的每一步。

组件套件包含三个元素：

- `SlThoughtChain` — 容器，管理链路布局、连接线和展开/折叠状态
- `SlThoughtChainNode` — 链路中的单个节点，包含图标、标题、描述、可折叠内容和底部区域
- `SlThoughtChainItem` — 独立的标签/徽章，用于在完整链路之外展示单个动作条目

---

## 基础用法

最简单的思维链，展示几个步骤节点。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <SlThoughtChain>
    <SlThoughtChainNode title="分析用户意图" description="解析用户输入的自然语言" />
    <SlThoughtChainNode title="检索知识库" description="从向量数据库中查找相关文档" />
    <SlThoughtChainNode title="生成回答" description="基于检索结果生成最终回答" />
  </SlThoughtChain>
);
```

---

## 节点状态

通过 `status` 属性设置节点的状态：`loading`、`success`、`error`、`abort`。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <SlThoughtChain>
    <SlThoughtChainNode title="解析输入" status="success" description="已完成" />
    <SlThoughtChainNode title="调用工具" status="loading" description="正在执行中..." />
    <SlThoughtChainNode title="生成结果" status="error" description="执行失败" />
    <SlThoughtChainNode title="已中止" status="abort" description="用户取消了操作" />
  </SlThoughtChain>
);
```

---

## 可折叠内容

设置 `collapsible` 属性使节点内容可折叠，需要配合 `nodeKey` 使用。通过 `defaultExpandedKeys` 设置默认展开的节点。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <SlThoughtChain defaultExpandedKeys={['step1']}>
    <SlThoughtChainNode nodeKey="step1" title="第一步：分析" collapsible description="点击展开查看详情">
      <div>这里是第一步的详细分析内容，包括对用户输入的语义解析结果。</div>
    </SlThoughtChainNode>
    <SlThoughtChainNode nodeKey="step2" title="第二步：检索" collapsible description="点击展开查看详情">
      <div>检索到 3 条相关文档，相似度分别为 0.95、0.87、0.82。</div>
    </SlThoughtChainNode>
    <SlThoughtChainNode nodeKey="step3" title="第三步：生成" collapsible description="点击展开查看详情">
      <div>基于检索结果，使用 LLM 生成最终回答。</div>
    </SlThoughtChainNode>
  </SlThoughtChain>
);
```

---

## 受控展开

通过 `expandedKeys` 属性控制展开状态，监听 `onSlExpand` 事件更新。

```tsx
import React, { useState } from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => {
  const [expandedKeys, setExpandedKeys] = useState<string[]>(['step1']);

  return (
    <>
      <SlThoughtChain expandedKeys={expandedKeys} onSlExpand={(e: any) => setExpandedKeys(e.detail.expandedKeys)}>
        <SlThoughtChainNode nodeKey="step1" title="意图识别" collapsible>
          <div>识别到用户意图：查询天气信息</div>
        </SlThoughtChainNode>
        <SlThoughtChainNode nodeKey="step2" title="API 调用" collapsible>
          <div>调用天气 API 获取数据</div>
        </SlThoughtChainNode>
        <SlThoughtChainNode nodeKey="step3" title="结果整理" collapsible>
          <div>将 API 返回的数据格式化为自然语言</div>
        </SlThoughtChainNode>
      </SlThoughtChain>
      <div style={{ marginTop: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>
        当前展开: {expandedKeys.join(', ') || '无'}
      </div>
    </>
  );
};
```

---

## 闪烁动画

设置 `blink` 属性使节点标题产生闪烁/脉冲动画，通常用于表示正在活跃的步骤。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <SlThoughtChain>
    <SlThoughtChainNode title="已完成" status="success" />
    <SlThoughtChainNode title="正在思考..." blink status="loading" />
    <SlThoughtChainNode title="等待中" />
  </SlThoughtChain>
);
```

---

## 自定义图标

通过 `icon` 插槽自定义节点图标，或使用 `noIcon` 属性隐藏图标区域。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon';

export default () => (
  <SlThoughtChain>
    <SlThoughtChainNode title="搜索">
      <SlIcon slot="icon" name="search" />
    </SlThoughtChainNode>
    <SlThoughtChainNode title="代码生成">
      <SlIcon slot="icon" name="code-slash" />
    </SlThoughtChainNode>
    <SlThoughtChainNode title="无图标节点" noIcon />
  </SlThoughtChain>
);
```

---

## 自定义插槽内容

使用 `title`、`description`、`footer` 插槽自定义富文本内容。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <SlThoughtChain>
    <SlThoughtChainNode collapsible nodeKey="rich">
      <span slot="title" style={{ color: 'var(--sl-color-primary-600)', fontWeight: 600 }}>
        自定义标题
      </span>
      <span slot="description">
        带有 <strong>富文本</strong> 的描述
      </span>
      <div>这是可折叠的主体内容区域。</div>
      <div slot="footer" style={{ fontSize: 12, color: 'var(--sl-color-neutral-500)' }}>
        底部信息 · 耗时 1.2s
      </div>
    </SlThoughtChainNode>
  </SlThoughtChain>
);
```

---

## 连接线样式

通过 `line` 属性控制节点之间的连接线样式，支持 `true`（默认实线）、`'solid'`、`'dashed'`、`'dotted'` 和 `false`（无连接线）。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <div style={{ display: 'flex', gap: 40 }}>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>solid（默认）</div>
      <SlThoughtChain line="solid">
        <SlThoughtChainNode title="步骤 1" />
        <SlThoughtChainNode title="步骤 2" />
        <SlThoughtChainNode title="步骤 3" />
      </SlThoughtChain>
    </div>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>dashed</div>
      <SlThoughtChain line="dashed">
        <SlThoughtChainNode title="步骤 1" />
        <SlThoughtChainNode title="步骤 2" />
        <SlThoughtChainNode title="步骤 3" />
      </SlThoughtChain>
    </div>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>dotted</div>
      <SlThoughtChain line="dotted">
        <SlThoughtChainNode title="步骤 1" />
        <SlThoughtChainNode title="步骤 2" />
        <SlThoughtChainNode title="步骤 3" />
      </SlThoughtChain>
    </div>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>无连接线</div>
      <SlThoughtChain line={false}>
        <SlThoughtChainNode title="步骤 1" />
        <SlThoughtChainNode title="步骤 2" />
        <SlThoughtChainNode title="步骤 3" />
      </SlThoughtChain>
    </div>
  </div>
);
```

---

## 尺寸

通过 `size` 属性调整思维链的尺寸，支持 `'small'`、`'middle'`（默认）、`'large'`。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <div style={{ display: 'flex', gap: 40 }}>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>small</div>
      <SlThoughtChain size="small">
        <SlThoughtChainNode title="步骤 1" description="描述" />
        <SlThoughtChainNode title="步骤 2" description="描述" />
      </SlThoughtChain>
    </div>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>middle</div>
      <SlThoughtChain size="middle">
        <SlThoughtChainNode title="步骤 1" description="描述" />
        <SlThoughtChainNode title="步骤 2" description="描述" />
      </SlThoughtChain>
    </div>
    <div>
      <div style={{ marginBottom: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>large</div>
      <SlThoughtChain size="large">
        <SlThoughtChainNode title="步骤 1" description="描述" />
        <SlThoughtChainNode title="步骤 2" description="描述" />
      </SlThoughtChain>
    </div>
  </div>
);
```

---

## ThoughtChainItem 独立标签

`SlThoughtChainItem` 可以独立使用，作为标签/徽章展示单个动作条目。

```tsx
import React from 'react';
import SlThoughtChainItem from '@shoelace-style/shoelace/dist/react/thought-chain-item';

export default () => (
  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
    <SlThoughtChainItem title="默认" />
    <SlThoughtChainItem title="成功" status="success" />
    <SlThoughtChainItem title="加载中" status="loading" />
    <SlThoughtChainItem title="错误" status="error" />
    <SlThoughtChainItem title="已中止" status="abort" />
  </div>
);
```

---

## ThoughtChainItem 变体

通过 `variant` 属性设置不同的视觉变体：`'solid'`（默认）、`'outlined'`、`'text'`。

```tsx
import React from 'react';
import SlThoughtChainItem from '@shoelace-style/shoelace/dist/react/thought-chain-item';

export default () => (
  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
    <SlThoughtChainItem title="Solid" variant="solid" />
    <SlThoughtChainItem title="Outlined" variant="outlined" />
    <SlThoughtChainItem title="Text" variant="text" />
  </div>
);
```

---

## 可点击的 ThoughtChainItem

设置 `clickable` 属性使 Item 可点击，监听 `onSlClick` 事件。

```tsx
import React, { useState } from 'react';
import SlThoughtChainItem from '@shoelace-style/shoelace/dist/react/thought-chain-item';

export default () => {
  const [log, setLog] = useState('');

  return (
    <>
      <div style={{ display: 'flex', gap: 8 }}>
        <SlThoughtChainItem title="可点击" clickable onSlClick={() => setLog('点击了「可点击」')} />
        <SlThoughtChainItem title="禁用" clickable disabled onSlClick={() => setLog('不应触发')} />
      </div>
      <div style={{ marginTop: 8, fontSize: 13, color: 'var(--sl-color-neutral-600)' }}>
        {log || '点击上方标签试试'}
      </div>
    </>
  );
};
```

---

## 动态添加节点

通过状态管理动态添加思维链节点。

```tsx
import React, { useState } from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

interface StepNode {
  key: string;
  title: string;
  description: string;
  status: 'loading' | 'success' | 'error' | 'abort' | '';
}

export default () => {
  const [nodes, setNodes] = useState<StepNode[]>([
    { key: 's1', title: '初始节点', description: '已完成', status: 'success' }
  ]);

  const addNode = () => {
    const idx = nodes.length + 1;
    const newNode: StepNode = {
      key: `s${idx}`,
      title: `动态节点 ${idx}`,
      description: '正在执行...',
      status: 'loading'
    };
    setNodes(prev => [...prev, newNode]);

    // 模拟异步完成
    setTimeout(() => {
      setNodes(prev => prev.map(n => (n.key === newNode.key ? { ...n, status: 'success', description: '已完成' } : n)));
    }, 2000);
  };

  return (
    <>
      <button onClick={addNode} style={{ marginBottom: 12 }}>
        添加节点
      </button>
      <SlThoughtChain>
        {nodes.map(n => (
          <SlThoughtChainNode key={n.key} title={n.title} description={n.description} status={n.status} />
        ))}
      </SlThoughtChain>
    </>
  );
};
```

---

## 完整示例

模拟一个 AI Agent 的完整调用链路，综合使用自定义图标、可折叠内容、状态、底部信息等功能。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon';

export default () => (
  <SlThoughtChain defaultExpandedKeys={['search', 'generate']}>
    <SlThoughtChainNode nodeKey="parse" title="解析用户意图" status="success" description="耗时 0.3s" collapsible>
      <SlIcon slot="icon" name="chat-dots" />
      <div>用户输入: "帮我查一下北京明天的天气"</div>
      <div>识别意图: 天气查询</div>
      <div>提取实体: 城市=北京, 时间=明天</div>
    </SlThoughtChainNode>

    <SlThoughtChainNode nodeKey="search" title="调用天气 API" status="success" description="耗时 1.2s" collapsible>
      <SlIcon slot="icon" name="cloud" />
      <div>请求: GET /api/weather?city=beijing&date=tomorrow</div>
      <div>响应: 200 OK</div>
      <div>数据: 晴, 最高 28°C, 最低 18°C</div>
    </SlThoughtChainNode>

    <SlThoughtChainNode nodeKey="generate" title="生成回答" status="success" description="耗时 0.8s" collapsible>
      <SlIcon slot="icon" name="stars" />
      <div>北京明天天气晴朗，最高温度 28°C，最低温度 18°C，适合户外活动。</div>
      <div slot="footer" style={{ fontSize: 12, color: 'var(--sl-color-neutral-500)' }}>
        总耗时 2.3s · Token 消耗 156
      </div>
    </SlThoughtChainNode>
  </SlThoughtChain>
);
```

---

## CSS 自定义样式

通过 CSS 自定义属性和 `::part()` 选择器自定义思维链样式。

```tsx
import React from 'react';
import SlThoughtChain from '@shoelace-style/shoelace/dist/react/thought-chain';
import SlThoughtChainNode from '@shoelace-style/shoelace/dist/react/thought-chain-node';

export default () => (
  <>
    <style>{`
      .styled-chain {
        --sl-thought-chain-gap: var(--sl-spacing-medium);
        --sl-thought-chain-connector-color: var(--sl-color-primary-300);
        --sl-thought-chain-icon-size: var(--sl-font-size-large);
      }
      .styled-chain sl-thought-chain-node::part(title) {
        color: var(--sl-color-primary-700);
        font-weight: 600;
      }
      .styled-chain sl-thought-chain-node::part(description) {
        font-style: italic;
      }
      .styled-chain sl-thought-chain-node::part(content) {
        background: var(--sl-color-neutral-50);
        border-radius: var(--sl-border-radius-medium);
        padding: var(--sl-spacing-small);
      }
    `}</style>
    <SlThoughtChain className="styled-chain" defaultExpandedKeys={['s1']}>
      <SlThoughtChainNode nodeKey="s1" title="自定义样式" description="通过 CSS 变量和 ::part 自定义" collapsible>
        <div>自定义背景和间距的内容区域。</div>
      </SlThoughtChainNode>
      <SlThoughtChainNode title="第二步" description="继承自定义样式" />
    </SlThoughtChain>
  </>
);
```

---

## API 参考

### SlThoughtChain 属性

| 属性                  | 类型                                         | 默认值      | 说明                         |
| --------------------- | -------------------------------------------- | ----------- | ---------------------------- |
| `size`                | `'small' \| 'middle' \| 'large'`             | `'middle'`  | 节点尺寸                     |
| `line`                | `boolean \| 'solid' \| 'dashed' \| 'dotted'` | `true`      | 连接线样式                   |
| `defaultExpandedKeys` | `string[]`                                   | `[]`        | 默认展开的节点 key（非受控） |
| `expandedKeys`        | `string[]`                                   | `undefined` | 当前展开的节点 key（受控）   |

### SlThoughtChain 事件

| 事件         | 回调参数                                  | 说明                |
| ------------ | ----------------------------------------- | ------------------- |
| `onSlExpand` | `{ key: string, expandedKeys: string[] }` | 折叠/展开节点时触发 |

### SlThoughtChain CSS Parts

| Part   | 说明           |
| ------ | -------------- |
| `base` | 组件基础包装器 |

### SlThoughtChain CSS 自定义属性

| 属性                                 | 说明                 | 默认值                        |
| ------------------------------------ | -------------------- | ----------------------------- |
| `--sl-thought-chain-gap`             | 图标与节点主体的间距 | `var(--sl-spacing-small)`     |
| `--sl-thought-chain-connector-color` | 连接线颜色           | `var(--sl-color-neutral-300)` |
| `--sl-thought-chain-icon-size`       | 节点图标尺寸         | `var(--sl-font-size-medium)`  |

---

### SlThoughtChainNode 属性

| 属性          | 类型                                                 | 默认值  | 说明                                  |
| ------------- | ---------------------------------------------------- | ------- | ------------------------------------- |
| `nodeKey`     | `string`                                             | `''`    | 唯一标识（折叠功能必需）              |
| `title`       | `string`                                             | `''`    | 标题文本（或使用 `title` 插槽）       |
| `description` | `string`                                             | `''`    | 描述文本（或使用 `description` 插槽） |
| `status`      | `'loading' \| 'success' \| 'error' \| 'abort' \| ''` | `''`    | 状态指示                              |
| `collapsible` | `boolean`                                            | `false` | 内容是否可折叠                        |
| `blink`       | `boolean`                                            | `false` | 标题闪烁动画                          |
| `noIcon`      | `boolean`                                            | `false` | 隐藏图标区域                          |

### SlThoughtChainNode 插槽

| 插槽          | 说明                       |
| ------------- | -------------------------- |
| _(默认)_      | 节点主体内容（可折叠区域） |
| `icon`        | 自定义图标                 |
| `title`       | 富文本标题                 |
| `description` | 富文本描述                 |
| `footer`      | 底部内容                   |

### SlThoughtChainNode CSS Parts

| Part            | 说明                    |
| --------------- | ----------------------- |
| `base`          | 节点基础包装器          |
| `icon`          | 图标容器                |
| `header`        | 头部区域（标题 + 描述） |
| `title`         | 标题区域                |
| `description`   | 描述区域                |
| `content`       | 可折叠内容包装器        |
| `content-inner` | 内容内层包装器          |
| `footer`        | 底部区域                |
| `collapse-icon` | 折叠箭头图标            |

---

### SlThoughtChainItem 属性

| 属性          | 类型                                                 | 默认值    | 说明                                  |
| ------------- | ---------------------------------------------------- | --------- | ------------------------------------- |
| `title`       | `string`                                             | `''`      | 标题文本（或使用 `title` 插槽）       |
| `description` | `string`                                             | `''`      | 描述文本（或使用 `description` 插槽） |
| `status`      | `'loading' \| 'success' \| 'error' \| 'abort' \| ''` | `''`      | 状态指示                              |
| `variant`     | `'solid' \| 'outlined' \| 'text'`                    | `'solid'` | 视觉变体                              |
| `blink`       | `boolean`                                            | `false`   | 闪烁动画                              |
| `disabled`    | `boolean`                                            | `false`   | 禁用状态                              |
| `clickable`   | `boolean`                                            | `false`   | 是否可点击                            |

### SlThoughtChainItem 插槽

| 插槽          | 说明       |
| ------------- | ---------- |
| `icon`        | 自定义图标 |
| `title`       | 富文本标题 |
| `description` | 富文本描述 |

### SlThoughtChainItem 事件

| 事件        | 说明                                         |
| ----------- | -------------------------------------------- |
| `onSlClick` | 点击时触发（需 `clickable` 且非 `disabled`） |

### SlThoughtChainItem CSS Parts

| Part          | 说明       |
| ------------- | ---------- |
| `base`        | 基础包装器 |
| `icon`        | 图标容器   |
| `content`     | 内容包装器 |
| `title`       | 标题区域   |
| `description` | 描述区域   |

---

## 交互行为说明

1. **折叠/展开**：点击设置了 `collapsible` 属性的节点标题区域可切换内容的展开/折叠状态，带有平滑的高度过渡动画（250ms ease）。
2. **键盘支持**：可折叠节点的标题支持 `Enter` 和 `Space` 键触发展开/折叠。
3. **受控 vs 非受控**：
   - 非受控模式：使用 `defaultExpandedKeys` 设置初始展开状态，组件内部管理后续状态变化。
   - 受控模式：使用 `expandedKeys` 属性，需在 `onSlExpand` 事件回调中调用 `setExpandedKeys(e.detail.expandedKeys)` 更新状态。
4. **状态图标**：`loading` 状态显示旋转加载器，`success`/`error`/`abort` 显示对应的图标。无状态时显示序号。
5. **闪烁动画**：`blink` 属性在标题上产生脉冲动画效果，适合标记当前活跃步骤。
6. **ThoughtChainItem 点击**：设置 `clickable` 后，Item 会显示悬停样式和指针光标。`disabled` 状态下点击事件不会触发。

---

## 最佳实践

1. **始终为可折叠节点设置 `nodeKey`**：`nodeKey` 是折叠功能的必要标识，确保每个可折叠节点有唯一的 key。
2. **使用按需引入**：始终使用 `import SlXxx from '@shoelace-style/shoelace/dist/react/xxx'` 按需引入组件，避免使用桶导入。
3. **合理使用状态**：用 `loading` 表示进行中，`success` 表示完成，`error` 表示失败，`abort` 表示中止。
4. **使用 `blink` 标记活跃步骤**：配合 `loading` 状态使用 `blink` 可以更明显地指示当前正在执行的步骤。
5. **连接线样式选择**：默认实线适合大多数场景；虚线（`dashed`）适合表示可选或条件步骤；点线（`dotted`）适合表示弱关联。
6. **事件命名**：React 中事件使用 `onSlExpand`、`onSlClick` 格式（`on` + 事件名驼峰化）。

---

## 常见问题

### Q: 折叠动画不生效？

确保节点设置了 `collapsible` 属性和 `nodeKey` 属性，且节点有子元素内容。

### Q: 如何在受控模式下更新展开状态？

```tsx
const [expandedKeys, setExpandedKeys] = useState<string[]>([]);

<SlThoughtChain expandedKeys={expandedKeys} onSlExpand={(e: any) => setExpandedKeys(e.detail.expandedKeys)}>
  ...
</SlThoughtChain>;
```

### Q: 如何动态渲染节点列表？

使用 React 状态管理节点数据，通过 `map` 渲染：

```tsx
const [nodes, setNodes] = useState([...]);

<SlThoughtChain>
  {nodes.map(n => (
    <SlThoughtChainNode key={n.key} title={n.title} status={n.status} />
  ))}
</SlThoughtChain>
```

### Q: ThoughtChainItem 和 ThoughtChainNode 的区别？

- `SlThoughtChainNode` 是链路中的节点，必须放在 `SlThoughtChain` 内部使用，有连接线、序号图标等链路特性。
- `SlThoughtChainItem` 是独立的标签/徽章组件，可以在任何地方独立使用，适合展示单个动作条目。
