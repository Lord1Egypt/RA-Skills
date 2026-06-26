# TreeSelect 树选择

允许用户从树形结构的数据中选择一个或多个节点，支持搜索、勾选、懒加载等功能。

## 特性概览

- **单选/多选**：支持单选和多选模式（`multiple`），多选可显示标签
- **搜索过滤**：支持输入关键词搜索树节点（`showSearch`）
- **勾选模式**：支持父子联动勾选（`treeCheckable`）
- **懒加载**：支持异步加载子节点（`lazy` + `sl-lazy-load`）
- **展示策略**：多选模式下支持 `all` / `parent` / `child` 三种标签展示策略
- **表单集成**：支持 `name`、`required`、`form` 属性参与表单提交和验证
- **丰富插槽**：支持前缀/后缀图标、自定义标签、自定义树节点图标等
- **自定义样式**：支持 `filled`、`pill`、`size` 等外观属性

## TreeSelectNodeData 数据结构

`treeData` 中每个节点的数据结构如下：

| 属性         | 说明                                                                           | 类型                                      | 默认值  |
| ------------ | ------------------------------------------------------------------------------ | ----------------------------------------- | ------- |
| `title`      | 节点标题，支持字符串、HTMLElement 或 Lit TemplateResult                        | `string \| HTMLElement \| TemplateResult` | -       |
| `value`      | 节点值，唯一标识                                                               | `string`                                  | -       |
| `key`        | 节点 key                                                                       | `string`                                  | -       |
| `children`   | 子节点数组                                                                     | `TreeSelectNodeData[]`                    | -       |
| `disabled`   | 是否禁用                                                                       | `boolean`                                 | `false` |
| `selectable` | 是否可选                                                                       | `boolean`                                 | -       |
| `checkable`  | 是否可勾选                                                                     | `boolean`                                 | -       |
| `isLeaf`     | 是否为叶子节点                                                                 | `boolean`                                 | -       |
| `icon`       | 节点图标，支持 `sl-icon` 图标名称（字符串）、HTMLElement 或 Lit TemplateResult | `string \| HTMLElement \| TemplateResult` | -       |
| `lazy`       | 是否启用懒加载，展开时触发 `sl-lazy-load` 事件                                 | `boolean`                                 | -       |

## 基础用法

最简单的用法，从树形数据中选择一个节点。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node4', value: '0-1-0' },
      { title: 'Child Node5', value: '0-1-1' }
    ]
  }
];

export default () => <SlTreeSelect treeData={treeData} placeholder="请选择" style={{ width: '300px' }} />;
```

## 多选模式

设置 `multiple` 属性启用多选模式，选中的节点以标签形式展示。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node4', value: '0-1-0' },
      { title: 'Child Node5', value: '0-1-1' }
    ]
  }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" multiple clearable style={{ width: '400px' }} />
);
```

## 可勾选（Checkable）

通过 `treeCheckable` 属性启用勾选模式，父子节点联动选中。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node4', value: '0-1-0' },
      { title: 'Child Node5', value: '0-1-1' }
    ]
  }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" multiple treeCheckable clearable style={{ width: '400px' }} />
);
```

## 带搜索

设置 `showSearch` 属性启用搜索功能，可以在输入框中输入关键词筛选树节点。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node3', value: '0-1-0' },
      { title: 'Child Node4', value: '0-1-1' }
    ]
  },
  { title: 'Leaf Node', value: '0-2' }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请搜索并选择" showSearch style={{ width: '300px' }} />
);
```

## 自定义搜索过滤（filterTreeNode）

通过 `showSearch` 对象配置自定义过滤函数，实现按标题搜索等需求。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' },
      { title: '测试组', value: 'qa' }
    ]
  },
  {
    title: '产品部',
    value: 'product',
    children: [
      { title: '产品设计', value: 'design' },
      { title: '产品运营', value: 'operation' }
    ]
  }
];

const searchConfig = {
  filterTreeNode: (inputValue, treeNode) => {
    const title = typeof treeNode.title === 'string' ? treeNode.title : '';
    return title.toLowerCase().includes(inputValue.toLowerCase());
  }
};

export default () => (
  <SlTreeSelect
    treeData={treeData}
    showSearch={searchConfig}
    placeholder="输入 title 搜索"
    style={{ width: '300px' }}
  />
);
```

## 搜索过滤字段（treeNodeFilterProp）

通过 `showSearch.treeNodeFilterProp` 指定默认过滤匹配的字段，默认为 `value`，设为 `title` 可按标题搜索。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' }
    ]
  },
  {
    title: '产品部',
    value: 'product',
    children: [
      { title: '产品设计', value: 'design' },
      { title: '产品运营', value: 'operation' }
    ]
  }
];

export default () => (
  <SlTreeSelect
    treeData={treeData}
    showSearch={{ treeNodeFilterProp: 'title' }}
    placeholder="输入 title 搜索"
    style={{ width: '300px' }}
  />
);
```

## 受控搜索值（searchValue）

通过 `showSearch.searchValue` 设置受控搜索值，配合 `onSlSearch` 事件实现防抖搜索等场景。

```jsx
import React, { useRef, useState, useCallback } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node3', value: '0-1-0' },
      { title: 'Child Node4', value: '0-1-1' }
    ]
  }
];

export default () => {
  const debounceRef = useRef(null);
  const [searchInfo, setSearchInfo] = useState('');
  const [searchValue, setSearchValue] = useState(undefined);

  const handleSearch = useCallback(event => {
    setSearchInfo('输入中: ' + event.detail.value);
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      setSearchValue(event.detail.value);
      setSearchInfo('已搜索: ' + event.detail.value);
    }, 300);
  }, []);

  return (
    <div>
      <SlTreeSelect
        treeData={treeData}
        showSearch={{ treeNodeFilterProp: 'title', searchValue }}
        placeholder="输入搜索（带防抖）"
        onSlSearch={handleSearch}
        style={{ width: '300px' }}
      />
      <p style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>{searchInfo}</p>
    </div>
  );
};
```

## 选中后自动清空搜索（autoClearSearchValue）

多选模式下，`showSearch.autoClearSearchValue` 默认为 `true`，选中节点后自动清空搜索框。设为 `false` 可保留搜索内容继续选择。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node4', value: '0-1-0' },
      { title: 'Child Node5', value: '0-1-1' }
    ]
  }
];

export default () => (
  <SlTreeSelect
    treeData={treeData}
    showSearch={{ treeNodeFilterProp: 'title', autoClearSearchValue: false }}
    placeholder="选中后保留搜索"
    multiple
    clearable
    style={{ width: '300px' }}
  />
);
```

## 默认展开所有节点

设置 `treeDefaultExpandAll` 属性，默认展开所有树节点。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      {
        title: 'Child Node1',
        value: '0-0-0',
        children: [
          { title: 'Grandchild 1', value: '0-0-0-0' },
          { title: 'Grandchild 2', value: '0-0-0-1' }
        ]
      },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [{ title: 'Child Node3', value: '0-1-0' }]
  }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" treeDefaultExpandAll style={{ width: '300px' }} />
);
```

## 可清除

设置 `clearable` 属性，当有选中值时显示清除按钮。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => <SlTreeSelect treeData={treeData} placeholder="请选择" clearable style={{ width: '300px' }} />;
```

## 禁用状态

设置 `disabled` 属性禁用整个组件。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  { title: 'Node1', value: '0-0' },
  { title: 'Node2', value: '0-1' }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="已禁用" value="0-0" disabled style={{ width: '300px' }} />
);
```

## 禁用节点

通过节点数据中的 `disabled` 属性禁用特定的树节点。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2 (disabled)', value: '0-0-1', disabled: true },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2 (disabled)',
    value: '0-1',
    disabled: true,
    children: [{ title: 'Child Node4', value: '0-1-0' }]
  }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" treeDefaultExpandAll style={{ width: '300px' }} />
);
```

## 尺寸

使用 `size` 属性设置组件尺寸，支持 `small`、`medium`（默认）和 `large`。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
    <SlTreeSelect treeData={treeData} placeholder="Small" size="small" style={{ width: '300px' }} />
    <SlTreeSelect treeData={treeData} placeholder="Medium" size="medium" style={{ width: '300px' }} />
    <SlTreeSelect treeData={treeData} placeholder="Large" size="large" style={{ width: '300px' }} />
  </div>
);
```

## Label 和 Help Text

使用 `label` 和 `helpText` 属性为组件添加标签和帮助文本。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' },
      { title: '测试组', value: 'qa' }
    ]
  },
  {
    title: '产品部',
    value: 'product',
    children: [
      { title: '产品设计', value: 'design' },
      { title: '产品运营', value: 'operation' }
    ]
  },
  { title: '行政部', value: 'admin' }
];

export default () => (
  <SlTreeSelect
    treeData={treeData}
    label="部门"
    helpText="请选择您所在的部门"
    placeholder="请选择部门"
    style={{ width: '300px' }}
  />
);
```

## 设置默认值

通过 `value` 属性设置默认选中值。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => (
  <SlTreeSelect
    treeData={treeData}
    placeholder="请选择"
    value="0-0-1"
    treeDefaultExpandAll
    style={{ width: '300px' }}
  />
);
```

## showCheckedStrategy

`showCheckedStrategy` 属性控制多选模式下标签的展示策略：

- `all`（默认）：显示所有选中的节点
- `parent`：当父节点下所有子节点都选中时，只显示父节点
- `child`：只显示叶子节点

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node3', value: '0-1-0' },
      { title: 'Child Node4', value: '0-1-1' }
    ]
  }
];

export default () => (
  <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
    <div>
      <p style={{ margin: '0 0 4px', fontSize: '12px', color: '#999' }}>strategy="all"</p>
      <SlTreeSelect
        treeData={treeData}
        placeholder="all"
        multiple
        treeCheckable
        clearable
        showCheckedStrategy="all"
        treeDefaultExpandAll
        style={{ width: '280px' }}
      />
    </div>
    <div>
      <p style={{ margin: '0 0 4px', fontSize: '12px', color: '#999' }}>strategy="parent"</p>
      <SlTreeSelect
        treeData={treeData}
        placeholder="parent"
        multiple
        treeCheckable
        clearable
        showCheckedStrategy="parent"
        treeDefaultExpandAll
        style={{ width: '280px' }}
      />
    </div>
    <div>
      <p style={{ margin: '0 0 4px', fontSize: '12px', color: '#999' }}>strategy="child"</p>
      <SlTreeSelect
        treeData={treeData}
        placeholder="child"
        multiple
        treeCheckable
        clearable
        showCheckedStrategy="child"
        treeDefaultExpandAll
        style={{ width: '280px' }}
      />
    </div>
  </div>
);
```

## 最大显示标签数

多选模式下，通过 `maxOptionsVisible` 属性控制最多显示的标签数量，超出部分以 `+n` 形式展示。设为 `0` 则不限制。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node4', value: '0-1-0' },
      { title: 'Child Node5', value: '0-1-1' }
    ]
  }
];

export default () => (
  <SlTreeSelect
    treeData={treeData}
    placeholder="请选择"
    multiple
    clearable
    maxOptionsVisible={2}
    treeDefaultExpandAll
    style={{ width: '400px' }}
  />
);
```

## 连接线（Tree Line）

设置 `treeLine` 属性，在父节点之间显示连接线。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      {
        title: 'Child Node1',
        value: '0-0-0',
        children: [
          { title: 'Grandchild 1', value: '0-0-0-0' },
          { title: 'Grandchild 2', value: '0-0-0-1' }
        ]
      },
      { title: 'Child Node2', value: '0-0-1' },
      { title: 'Child Node3', value: '0-0-2' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node4', value: '0-1-0' },
      { title: 'Child Node5', value: '0-1-1' }
    ]
  }
];

export default () => (
  <SlTreeSelect
    treeData={treeData}
    placeholder="请选择"
    treeLine
    treeDefaultExpandAll
    clearable
    style={{ width: '300px' }}
  />
);
```

## 节点图标

通过 `treeData` 中的 `icon` 字段为节点添加图标。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    icon: 'gear',
    children: [
      { title: '前端组', value: 'frontend', icon: 'code-slash' },
      { title: '后端组', value: 'backend', icon: 'hdd-stack' },
      { title: '测试组', value: 'qa', icon: 'bug' }
    ]
  },
  {
    title: '产品部',
    value: 'product',
    icon: 'lightbulb',
    children: [
      { title: '产品设计', value: 'design', icon: 'palette' },
      { title: '产品运营', value: 'operation', icon: 'graph-up' }
    ]
  },
  { title: '行政部', value: 'admin', icon: 'building' }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" treeDefaultExpandAll clearable style={{ width: '350px' }} />
);
```

## Filled 样式

使用 `filled` 属性绘制填充样式的选择器。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => <SlTreeSelect treeData={treeData} placeholder="Filled style" filled style={{ width: '300px' }} />;
```

## Pill 样式

使用 `pill` 属性绘制圆角药丸样式。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => <SlTreeSelect treeData={treeData} placeholder="Pill style" pill style={{ width: '300px' }} />;
```

## Hoist

设置 `hoist` 属性使下拉面板使用 `fixed` 定位策略，可以突破 `overflow: hidden` 的容器限制。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => (
  <div
    style={{ overflow: 'hidden', border: '1px dashed var(--sl-color-neutral-300)', padding: '16px', height: '120px' }}
  >
    <p style={{ margin: '0 0 8px', fontSize: '12px', color: '#999' }}>overflow: hidden 容器</p>
    <SlTreeSelect treeData={treeData} placeholder="请选择" hoist style={{ width: '260px' }} />
  </div>
);
```

## 弹出位置

通过 `placement` 属性手动指定弹出的位置。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" placement="top-start" style={{ width: '300px' }} />
);
```

## 前缀和后缀图标（Prefix & Suffix）

通过 `prefix` 和 `suffix` 插槽在输入框前后添加图标。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' }
    ]
  },
  { title: '产品部', value: 'product' },
  { title: '行政部', value: 'admin' }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="带前缀图标" clearable style={{ width: '300px' }}>
    <SlIcon name="search" slot="prefix" />
  </SlTreeSelect>
);
```

## 自定义树节点展开/收起图标

通过 `tree-expand-icon` 和 `tree-collapse-icon` 插槽自定义树节点的展开和收起图标。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      {
        title: 'Child Node1',
        value: '0-0-0',
        children: [
          { title: 'Grandchild 1', value: '0-0-0-0' },
          { title: 'Grandchild 2', value: '0-0-0-1' }
        ]
      },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  {
    title: 'Node2',
    value: '0-1',
    children: [
      { title: 'Child Node3', value: '0-1-0' },
      { title: 'Child Node4', value: '0-1-1' }
    ]
  }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="请选择" treeDefaultExpandAll clearable style={{ width: '300px' }}>
    <SlIcon name="plus-square" slot="tree-expand-icon" />
    <SlIcon name="dash-square" slot="tree-collapse-icon" />
  </SlTreeSelect>
);
```

## 自定义下拉箭头图标（Expand Icon）

通过 `expand-icon` 插槽替换默认的下拉箭头图标。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => (
  <SlTreeSelect treeData={treeData} placeholder="自定义箭头" style={{ width: '300px' }}>
    <SlIcon name="caret-down-fill" slot="expand-icon" />
  </SlTreeSelect>
);
```

## 自定义标签渲染（getTag）

通过 `getTag` 属性自定义多选模式下标签的渲染方式。

```jsx
import React from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Fruits',
    value: 'fruits',
    children: [
      { title: '🍎 Apple', value: 'apple' },
      { title: '🍊 Orange', value: 'orange' },
      { title: '🍇 Grape', value: 'grape' }
    ]
  },
  {
    title: 'Vegetables',
    value: 'vegetables',
    children: [
      { title: '🥕 Carrot', value: 'carrot' },
      { title: '🥦 Broccoli', value: 'broccoli' }
    ]
  }
];

const colors = ['#e6f7ff', '#fff7e6', '#f6ffed', '#fff1f0', '#f9f0ff'];

const customGetTag = (node, index) => {
  const tag = document.createElement('sl-tag');
  tag.size = 'medium';
  tag.removable = true;
  tag.setAttribute('part', 'tag');
  tag.style.setProperty('--sl-color-neutral-0', colors[index % colors.length]);
  tag.textContent = typeof node.title === 'string' ? node.title : node.value;
  return tag;
};

export default () => (
  <SlTreeSelect
    treeData={treeData}
    getTag={customGetTag}
    placeholder="请选择"
    multiple
    clearable
    treeDefaultExpandAll
    style={{ width: '400px' }}
  />
);
```

## 异步加载（Lazy Load）

在 `treeData` 中设置 `lazy: true` 标记需要懒加载的节点。展开时触发 `sl-lazy-load` 事件，在回调中调用 `loadChildren(parentValue, children)` 方法完成加载。

```jsx
import React, { useRef, useCallback } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  { title: 'Expand to load', value: 'parent-0', lazy: true },
  { title: 'Expand to load', value: 'parent-1', lazy: true },
  { title: 'Leaf Node', value: 'leaf-0' }
];

export default () => {
  const ref = useRef(null);

  const handleLazyLoad = useCallback(async event => {
    const nodeValue = event.detail.value;
    // 模拟异步请求
    const children = await new Promise(resolve => {
      setTimeout(() => {
        resolve([
          { title: nodeValue + ' - Child 1', value: nodeValue + '-0' },
          { title: nodeValue + ' - Child 2', value: nodeValue + '-1' },
          { title: nodeValue + ' - Child 3 (lazy)', value: nodeValue + '-2', lazy: true }
        ]);
      }, 1000);
    });
    if (ref.current) {
      ref.current.loadChildren(nodeValue, children);
    }
  }, []);

  return (
    <SlTreeSelect
      ref={ref}
      treeData={treeData}
      placeholder="请选择"
      clearable
      onSlLazyLoad={handleLazyLoad}
      style={{ width: '300px' }}
    />
  );
};
```

## 表单集成

`SlTreeSelect` 支持表单集成，可通过 `name`、`required` 属性参与表单提交和验证。

```jsx
import React, { useRef, useCallback, useState } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' }
    ]
  },
  { title: '产品部', value: 'product' },
  { title: '行政部', value: 'admin' }
];

export default () => {
  const formRef = useRef(null);
  const [output, setOutput] = useState('');

  const handleSubmit = useCallback(e => {
    e.preventDefault();
    const data = new FormData(formRef.current);
    setOutput('提交值: ' + (data.get('department') || '(空)'));
  }, []);

  return (
    <form ref={formRef} onSubmit={handleSubmit} style={{ width: '300px' }}>
      <SlTreeSelect
        treeData={treeData}
        name="department"
        label="部门"
        placeholder="请选择部门"
        required
        helpText="必填项"
        clearable
      />
      <br />
      <SlButton type="submit" variant="primary" style={{ marginTop: '8px' }}>
        提交
      </SlButton>
      <p style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>{output}</p>
    </form>
  );
};
```

## 监听事件

通过 `onSlChange`、`onSlFocus`、`onSlBlur`、`onSlClear`、`onSlShow`、`onSlHide` 等属性监听组件状态变化。

```jsx
import React, { useRef, useState, useCallback } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => {
  const ref = useRef(null);
  const [eventMsg, setEventMsg] = useState('等待事件...');

  const handleChange = useCallback(() => {
    setEventMsg('sl-change: value=' + (ref.current ? ref.current.value : ''));
  }, []);

  return (
    <div>
      <div
        style={{ padding: '8px', background: 'var(--sl-color-neutral-100)', borderRadius: '4px', marginBottom: '8px' }}
      >
        <p style={{ margin: '4px 0', fontSize: '12px' }}>{eventMsg}</p>
      </div>
      <SlTreeSelect
        ref={ref}
        treeData={treeData}
        placeholder="请选择"
        clearable
        onSlChange={handleChange}
        onSlFocus={useCallback(() => setEventMsg('sl-focus'), [])}
        onSlBlur={useCallback(() => setEventMsg('sl-blur'), [])}
        onSlClear={useCallback(() => setEventMsg('sl-clear'), [])}
        onSlShow={useCallback(() => setEventMsg('sl-show'), [])}
        onSlHide={useCallback(() => setEventMsg('sl-hide'), [])}
        style={{ width: '300px' }}
      />
    </div>
  );
};
```

## 动态更新数据

通过 `useState` 管理 `treeData` 和 `value`，状态变化时 React 重渲染并将新值传给组件。

```jsx
import React, { useState, useCallback } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const defaultData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' }
    ]
  },
  { title: '产品部', value: 'product' }
];

export default () => {
  const [treeData, setTreeData] = useState(defaultData);
  const [value, setValue] = useState('');

  const handleSetValue = useCallback(() => {
    setValue('frontend');
  }, []);

  const handleUpdateData = useCallback(() => {
    setTreeData([
      {
        title: '新部门A',
        value: 'new-a',
        children: [
          { title: '子部门1', value: 'new-a-1' },
          { title: '子部门2', value: 'new-a-2' }
        ]
      },
      { title: '新部门B', value: 'new-b' }
    ]);
  }, []);

  const handleReset = useCallback(() => {
    setTreeData(defaultData);
    setValue('');
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', gap: '8px' }}>
        <SlButton size="small" onClick={handleSetValue}>
          选中 frontend
        </SlButton>
        <SlButton size="small" onClick={handleUpdateData}>
          更新数据
        </SlButton>
        <SlButton size="small" onClick={handleReset}>
          重置
        </SlButton>
      </div>
      <SlTreeSelect treeData={treeData} value={value} placeholder="请选择" clearable style={{ width: '300px' }} />
    </div>
  );
};
```

## 编程式控制（show / hide / focus / blur）

通过 `ref` 调用 `show()`、`hide()`、`focus()`、`blur()` 方法编程式控制下拉面板和焦点。

```jsx
import React, { useRef } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    children: [
      { title: 'Child Node1', value: '0-0-0' },
      { title: 'Child Node2', value: '0-0-1' }
    ]
  },
  { title: 'Node2', value: '0-1' }
];

export default () => {
  const ref = useRef(null);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', gap: '8px' }}>
        <SlButton size="small" onClick={() => ref.current?.show()}>
          show()
        </SlButton>
        <SlButton size="small" onClick={() => ref.current?.hide()}>
          hide()
        </SlButton>
        <SlButton size="small" onClick={() => ref.current?.focus()}>
          focus()
        </SlButton>
        <SlButton size="small" onClick={() => ref.current?.blur()}>
          blur()
        </SlButton>
      </div>
      <SlTreeSelect ref={ref} treeData={treeData} placeholder="请选择" style={{ width: '300px' }} />
    </div>
  );
};
```

## 表单验证（checkValidity / reportValidity / setCustomValidity）

通过 `ref` 调用 `checkValidity()`、`reportValidity()`、`setCustomValidity()` 方法进行表单验证。

```jsx
import React, { useRef, useState } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const treeData = [
  {
    title: '技术部',
    value: 'tech',
    children: [
      { title: '前端组', value: 'frontend' },
      { title: '后端组', value: 'backend' }
    ]
  },
  { title: '产品部', value: 'product' }
];

export default () => {
  const ref = useRef(null);
  const [output, setOutput] = useState('');

  return (
    <div>
      <SlTreeSelect
        ref={ref}
        treeData={treeData}
        name="dept"
        label="部门"
        placeholder="请选择"
        required
        clearable
        style={{ width: '300px' }}
      />
      <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
        <SlButton size="small" onClick={() => setOutput('checkValidity: ' + ref.current?.checkValidity())}>
          checkValidity()
        </SlButton>
        <SlButton size="small" onClick={() => ref.current?.reportValidity()}>
          reportValidity()
        </SlButton>
        <SlButton size="small" onClick={() => ref.current?.setCustomValidity('请选择一个有效的部门')}>
          setCustomValidity()
        </SlButton>
        <SlButton size="small" onClick={() => ref.current?.setCustomValidity('')}>
          清除自定义验证
        </SlButton>
      </div>
      <p style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>{output}</p>
    </div>
  );
};
```

## Properties

| 属性                 | 描述                                               | 类型                              | 默认值      |
| -------------------- | -------------------------------------------------- | --------------------------------- | ----------- |
| name                 | 表单提交时的字段名                                 | `string`                          | `''`        |
| value                | 当前选中值。多选时为 `string[]`，单选时为 `string` | `string \| string[]`              | `''`        |
| size                 | 组件尺寸                                           | `'small' \| 'medium' \| 'large'`  | `'medium'`  |
| placeholder          | 占位文本                                           | `string`                          | `''`        |
| multiple             | 是否多选                                           | `boolean`                         | `false`     |
| maxOptionsVisible    | 多选时最多显示的标签数量，0 表示不限制             | `number`                          | `3`         |
| disabled             | 是否禁用                                           | `boolean`                         | `false`     |
| clearable            | 是否显示清除按钮                                   | `boolean`                         | `false`     |
| open                 | 下拉面板是否打开                                   | `boolean`                         | `false`     |
| hoist                | 是否使用 fixed 定位策略                            | `boolean`                         | `false`     |
| filled               | 是否使用填充样式                                   | `boolean`                         | `false`     |
| pill                 | 是否使用药丸样式                                   | `boolean`                         | `false`     |
| label                | 标签文本                                           | `string`                          | `''`        |
| placement            | 下拉面板弹出位置                                   | `string`                          | `'bottom'`  |
| helpText             | 帮助文本                                           | `string`                          | `''`        |
| required             | 是否必填                                           | `boolean`                         | `false`     |
| form                 | 关联的表单 ID                                      | `string`                          | `''`        |
| treeData             | 树形数据                                           | `TreeSelectNodeData[]`            | `[]`        |
| showSearch           | 是否启用搜索，支持布尔值或配置对象                 | `boolean \| ShowSearchConfig`     | `false`     |
| treeDefaultExpandAll | 是否默认展开所有节点                               | `boolean`                         | `false`     |
| treeCheckable        | 是否启用勾选模式（多选时父子联动）                 | `boolean`                         | `false`     |
| showCheckedStrategy  | 多选标签展示策略                                   | `'all' \| 'parent' \| 'child'`    | `'all'`     |
| treeLine             | 是否显示连接线                                     | `boolean`                         | `false`     |
| getTag               | 自定义标签渲染函数                                 | `(node, index) => TemplateResult` | 默认 sl-tag |

### ShowSearchConfig

| 属性                 | 说明                                     | 类型                                             | 默认值    |
| -------------------- | ---------------------------------------- | ------------------------------------------------ | --------- |
| autoClearSearchValue | 多选模式下选中后是否自动清空搜索框       | `boolean`                                        | `true`    |
| filterTreeNode       | 是否根据输入项进行筛选，或自定义过滤函数 | `boolean \| ((inputValue, treeNode) => boolean)` | `true`    |
| searchValue          | 受控搜索值                               | `string`                                         | -         |
| treeNodeFilterProp   | 输入项过滤对应的 treeNode 属性           | `string`                                         | `'value'` |

## Events

| 事件名称      | JSX 属性        | 描述                       | 事件详情                              |
| ------------- | --------------- | -------------------------- | ------------------------------------- |
| sl-change     | `onSlChange`    | 选中值变化时触发           | -                                     |
| sl-clear      | `onSlClear`     | 清除按钮点击时触发         | -                                     |
| sl-input      | `onSlInput`     | 输入值变化时触发           | -                                     |
| sl-focus      | `onSlFocus`     | 获得焦点时触发             | -                                     |
| sl-blur       | `onSlBlur`      | 失去焦点时触发             | -                                     |
| sl-show       | `onSlShow`      | 下拉面板打开时触发         | -                                     |
| sl-after-show | `onSlAfterShow` | 下拉面板打开动画完成后触发 | -                                     |
| sl-hide       | `onSlHide`      | 下拉面板关闭时触发         | -                                     |
| sl-after-hide | `onSlAfterHide` | 下拉面板关闭动画完成后触发 | -                                     |
| sl-invalid    | `onSlInvalid`   | 表单验证不通过时触发       | -                                     |
| sl-search     | `onSlSearch`    | 搜索值变化时触发           | `{ value: string }`                   |
| sl-lazy-load  | `onSlLazyLoad`  | 懒加载节点展开时触发       | `{ value: string, item: SlTreeItem }` |

## CSS Custom Properties

| 方法名              | 描述                               | 参数                                                  | 返回值                    |
| ------------------- | ---------------------------------- | ----------------------------------------------------- | ------------------------- |
| show()              | 打开下拉面板                       | -                                                     | `Promise<void>`           |
| hide()              | 关闭下拉面板                       | -                                                     | `Promise<void>`           |
| focus(options?)     | 聚焦到输入框                       | `FocusOptions?`                                       | `void`                    |
| blur()              | 移除焦点                           | -                                                     | `void`                    |
| checkValidity()     | 检查有效性（不显示提示）           | -                                                     | `boolean`                 |
| reportValidity()    | 检查有效性并显示浏览器提示         | -                                                     | `boolean`                 |
| setCustomValidity() | 设置自定义验证消息，传空字符串恢复 | `message: string`                                     | `void`                    |
| getForm()           | 获取关联的表单元素                 | -                                                     | `HTMLFormElement \| null` |
| loadChildren()      | 为懒加载节点加载子节点             | `parentValue: string, children: TreeSelectNodeData[]` | `void`                    |

## Slots

| 插槽名             | 描述                                                    |
| ------------------ | ------------------------------------------------------- |
| label              | 标签内容，替代 `label` 属性                             |
| help-text          | 帮助文本，替代 `helpText` 属性                          |
| prefix             | 输入框前缀图标或元素                                    |
| suffix             | 入框后缀图标或元素                                      |
| clear-icon         | 自定义清除图标                                          |
| expand-icon        | 自定义下拉箭头图标                                      |
| tree-expand-icon   | 自定义树节点展开图标（转发到 sl-tree 的 expand-icon）   |
| tree-collapse-icon | 自定义树节点收起图标（转发到 sl-tree 的 collapse-icon） |

## CSS Parts

| Part 名称              | 描述                                     |
| ---------------------- | ---------------------------------------- |
| form-control           | 表单控件外层容器                         |
| form-control-label     | 标签容器                                 |
| form-control-input     | 输入区域容器                             |
| form-control-help-text | 帮助文本容器                             |
| combobox               | 组合框容器（包含前缀、输入、清除、箭头） |
| prefix                 | 前缀容器                                 |
| suffix                 | 后缀容器                                 |
| display-input          | 显示输入框                               |
| tags                   | 标签容器（多选模式）                     |
| tag                    | 单个标签                                 |
| clear-button           | 清除按钮                                 |
| expand-icon            | 下拉箭头容器                             |
| dropdown               | 下拉面板                                 |
| tree                   | 树组件                                   |

## 事件处理最佳实践

`sl-change` 等事件在 React 中使用 `onSlChange` 属性绑定（遵循 `onSl*` 命名规范）：

```jsx
import React, { useCallback } from 'react';
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';

const handleChange = useCallback(event => {
  console.log('选中值变化');
}, []);

const handleLazyLoad = useCallback(event => {
  const { value } = event.detail;
  console.log('懒加载节点:', value);
}, []);

<SlTreeSelect onSlChange={handleChange} onSlLazyLoad={handleLazyLoad} />;
```

## 最佳实践

### 1. 正确导入组件

```javascript
import SlTreeSelect from '@kdcloudjs/shoelace/dist/react/tree-select/index.js';
```

### 2. treeData、showSearch、getTag 等属性直接通过 JSX 属性传入

`@lit/react` 的 `createComponent` 会将所有 Lit `@property()` 声明的属性映射为 React props，包括 `attribute: false` 的属性。因此复杂对象属性可以直接传入：

```jsx
<SlTreeSelect
  treeData={[
    { title: 'Node1', value: '0-0', children: [...] }
  ]}
  showSearch={{ treeNodeFilterProp: 'title' }}
  getTag={(node, index) => { ... }}
/>
```

### 3. 使用 useCallback 包裹事件处理函数

```jsx
const handleChange = useCallback(event => {
  console.log('选中值:', event.target.value);
}, []);

<SlTreeSelect onSlChange={handleChange} />;
```

### 4. 通过 ref 调用组件方法

需要调用 `show()`、`hide()`、`loadChildren()` 等方法时，使用 `ref`：

```jsx
const ref = useRef(null);

const handleShow = () => {
  ref.current?.show();
};

<SlTreeSelect ref={ref} />;
```

### 5. 动态更新也可通过 ref

当需要在事件回调中命令式地更新属性时，也可以通过 `ref` 操作：

```jsx
const ref = useRef(null);

const handleReset = () => {
  if (ref.current) {
    ref.current.treeData = newData;
    ref.current.value = '';
  }
};
```

## 常见问题

### Q: treeData 可以直接通过 JSX 属性传入吗？

A: 可以。`@lit/react` 的 `createComponent` 会将 Lit 组件的所有 `@property()` 属性（包括 `attribute: false` 的）映射为 React props，所以 `treeData`、`showSearch`、`getTag` 都可以直接作为 JSX 属性传入。

### Q: 多选模式下如何获取选中的值？

A: 监听 `onSlChange` 事件，通过 `ref.current.value` 或 `event.target.value` 获取选中值数组。多选模式下 `value` 是 `string[]` 类型。

### Q: 如何实现远程搜索？

A: 将 `showSearch` 设为 `{ filterTreeNode: false }` 禁用本地过滤，监听 `onSlSearch` 事件获取搜索关键词，在回调中请求远程数据并更新 `treeData`。

### Q: 懒加载节点如何使用？

A: 在 `treeData` 中设置 `lazy: true`，监听 `onSlLazyLoad` 事件，在回调中异步获取子节点数据后调用 `ref.current.loadChildren(parentValue, children)` 完成加载。

### Q: 受控模式 vs 非受控模式有什么区别？

A:

- **非受控模式**：设置初始 `value`，组件内部管理状态。
- **受控模式**：使用 `value` 属性，需要在 `onSlChange` 回调中更新状态。
