# Cascader 级联选择

允许用户从一组层级选项中进行级联选择，适用于省市区、组织架构、分类目录等场景。

## 特性概览

- **级联选择**：从层级数据中逐级选择，支持多层级
- **多选模式**：支持多选（`multiple`），选中项以标签形式展示
- **展开触发**：支持点击或鼠标悬浮展开子级（`expandTrigger`）
- **选择即改变**：支持选中非叶子节点即改变值（`changeOnSelect`）
- **路径显示**：支持显示完整路径或仅显示最后一级（`showFullPath`）
- **自定义字段**：支持自定义数据字段名（`fieldNames`）
- **自定义分隔符**：支持自定义路径分隔符（`separator`）
- **表单集成**：支持 `name`、`required`、`form` 属性参与表单提交和验证
- **丰富插槽**：支持前缀/后缀图标、自定义清除图标、自定义展开图标等
- **外观变体**：支持 `variant`（outlined/borderless/filled/underlined）和 `size` 等外观属性
- **搜索过滤**：支持搜索过滤选项（`showSearch`），可自定义过滤、排序和数量限制
- **异步加载**：支持数据懒加载（`loadData`）
- **自定义渲染**：支持自定义选项渲染（`optionRender`）和显示渲染（`displayRender`）
- **标签控制**：多选模式支持最大标签数（`maxTagCount`）和标签文本长度限制（`maxTagTextLength`）
- **验证状态**：支持 `status` 属性设置 error/warning 状态
- **选中策略**：多选模式支持 `showCheckedStrategy` 控制显示父节点或子节点
- **面板禁用**：支持禁用面板选项交互（`panelDisabled`），面板可正常打开但选项不可点击

## CascaderOption 数据结构

`options` 中每个选项的数据结构如下：

| 属性       | 说明                   | 类型               | 默认值  |
| ---------- | ---------------------- | ------------------ | ------- |
| `value`    | 选项值，唯一标识       | `string`           | -       |
| `label`    | 选项标签，显示文本     | `string`           | -       |
| `disabled` | 是否禁用               | `boolean`          | `false` |
| `children` | 子选项数组             | `CascaderOption[]` | -       |
| `isLeaf`   | 是否为叶子节点         | `boolean`          | -       |
| `loading`  | 是否正在加载子节点     | `boolean`          | -       |

## FieldNames 自定义字段

可通过 `fieldNames` 自定义数据中的字段名映射：

| 属性       | 说明               | 类型     | 默认值       |
| ---------- | ------------------ | -------- | ------------ |
| `label`    | 标签字段名         | `string` | `'label'`    |
| `value`    | 值字段名           | `string` | `'value'`    |
| `children` | 子选项字段名       | `string` | `'children'` |

## 基础用法

最简单的用法，从层级数据中逐级选择。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      {
        value: 'hangzhou',
        label: '杭州',
        children: [
          { value: 'xihu', label: '西湖区' },
          { value: 'binjiang', label: '滨江区' }
        ]
      },
      {
        value: 'ningbo',
        label: '宁波',
        children: [
          { value: 'haishu', label: '海曙区' }
        ]
      }
    ]
  },
  {
    value: 'jiangsu',
    label: '江苏',
    children: [
      {
        value: 'nanjing',
        label: '南京',
        children: [
          { value: 'xuanwu', label: '玄武区' },
          { value: 'jianye', label: '建邺区' }
        ]
      }
    ]
  }
];

export default () => <SlCascader options={options} placeholder="请选择" style={{ width: '300px' }} />;
```

## 多选模式

设置 `multiple` 属性启用多选模式，选中的路径以标签形式展示。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      {
        value: 'hangzhou',
        label: '杭州',
        children: [
          { value: 'xihu', label: '西湖区' },
          { value: 'binjiang', label: '滨江区' }
        ]
      }
    ]
  },
  {
    value: 'jiangsu',
    label: '江苏',
    children: [
      {
        value: 'nanjing',
        label: '南京',
        children: [
          { value: 'xuanwu', label: '玄武区' },
          { value: 'jianye', label: '建邺区' }
        ]
      }
    ]
  }
];

export default () => (
  <SlCascader options={options} placeholder="请选择" multiple allowClear style={{ width: '400px' }} />
);
```

## 悬浮展开

设置 `expandTrigger="hover"` 属性，鼠标悬浮时自动展开子级菜单。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      {
        value: 'hangzhou',
        label: '杭州',
        children: [
          { value: 'xihu', label: '西湖区' }
        ]
      }
    ]
  }
];

export default () => (
  <SlCascader options={options} placeholder="请选择" expandTrigger="hover" style={{ width: '300px' }} />
);
```

## 选择即改变

设置 `changeOnSelect` 属性，选中任意层级的选项即可改变值，不必选到叶子节点。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      {
        value: 'hangzhou',
        label: '杭州',
        children: [
          { value: 'xihu', label: '西湖区' }
        ]
      }
    ]
  }
];

export default () => (
  <SlCascader options={options} placeholder="请选择" changeOnSelect style={{ width: '300px' }} />
);
```

## 仅显示最后一级

设置 `showFullPath={false}`，输入框中仅显示最后一级选项的标签。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      {
        value: 'hangzhou',
        label: '杭州',
        children: [
          { value: 'xihu', label: '西湖区' }
        ]
      }
    ]
  }
];

export default () => (
  <SlCascader options={options} placeholder="请选择" showFullPath={false} style={{ width: '300px' }} />
);
```

## 自定义分隔符

通过 `separator` 属性自定义路径分隔符，默认为 ` / `。

```jsx
<SlCascader options={options} placeholder="请选择" separator=" > " style={{ width: '300px' }} />
```

## 自定义字段名

通过 `fieldNames` 属性自定义数据中的字段名映射，适用于后端返回的数据字段与默认不一致的场景。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const options = [
  {
    code: 'zhejiang',
    name: '浙江',
    items: [
      {
        code: 'hangzhou',
        name: '杭州',
        items: [
          { code: 'xihu', name: '西湖区' }
        ]
      }
    ]
  }
];

export default () => (
  <SlCascader
    options={options}
    fieldNames={{ label: 'name', value: 'code', children: 'items' }}
    placeholder="请选择"
    style={{ width: '300px' }}
  />
);
```

## 可清除

设置 `allowClear` 属性（默认已启用），当有选中值时显示清除按钮。

```jsx
<SlCascader options={options} placeholder="请选择" allowClear style={{ width: '300px' }} />
```

## 禁用状态

设置 `disabled` 属性禁用整个级联选择器。

```jsx
<SlCascader options={options} placeholder="请选择" disabled style={{ width: '300px' }} />
```

## 禁用选项

在选项数据中设置 `disabled: true` 禁用特定选项。

```jsx
const options = [
  {
    value: 'zhejiang',
    label: '浙江',
    children: [
      { value: 'hangzhou', label: '杭州', disabled: true },
      { value: 'ningbo', label: '宁波' }
    ]
  }
];
```

## 尺寸

通过 `size` 属性设置组件尺寸，支持 `small`、`medium`（默认）、`large`。

```jsx
<SlCascader options={options} placeholder="Small" size="small" style={{ width: '300px' }} />
<SlCascader options={options} placeholder="Medium" style={{ width: '300px' }} />
<SlCascader options={options} placeholder="Large" size="large" style={{ width: '300px' }} />
```

## Label 和 Help Text

通过 `label` 和 `helpText` 属性设置标签和帮助文本。

```jsx
<SlCascader options={options} label="所在地区" helpText="请选择省/市/区" placeholder="请选择" style={{ width: '300px' }} />
```

## 外观变体

通过 `variant` 属性设置组件外观变体，支持 `outlined`（默认）、`borderless`、`filled`、`underlined`。

```jsx
<SlCascader options={options} placeholder="Outlined（默认）" style={{ width: '300px' }} />
<SlCascader options={options} placeholder="Borderless" variant="borderless" style={{ width: '300px' }} />
<SlCascader options={options} placeholder="Filled" variant="filled" style={{ width: '300px' }} />
<SlCascader options={options} placeholder="Underlined" variant="underlined" style={{ width: '300px' }} />
```

## 验证状态

通过 `status` 属性设置验证状态，支持 `error` 和 `warning`。

```jsx
<SlCascader options={options} placeholder="Error" status="error" style={{ width: '300px' }} />
<SlCascader options={options} placeholder="Warning" status="warning" style={{ width: '300px' }} />
```

## Hoist

设置 `hoist` 属性使用 fixed 定位策略，防止菜单被容器的 `overflow` 裁切。默认已启用。

```jsx
<SlCascader options={options} placeholder="请选择" hoist style={{ width: '300px' }} />
```

## 弹出位置

通过 `placement` 属性设置菜单弹出位置，支持 `bottomLeft`（默认）、`bottomRight`、`topLeft`、`topRight`。

```jsx
<SlCascader options={options} placeholder="请选择" placement="topLeft" style={{ width: '300px' }} />
```

## 前缀和后缀图标

通过 `prefix` 和 `suffix` 插槽添加自定义前缀和后缀图标。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

export default () => (
  <SlCascader options={options} placeholder="请选择" style={{ width: '300px' }}>
    <SlIcon name="geo-alt" slot="prefix" />
  </SlCascader>
);
```

## 设置默认值

通过 `value` 属性设置默认选中值，值为选中路径的 value 数组。

```jsx
<SlCascader options={options} value={['zhejiang', 'hangzhou', 'xihu']} style={{ width: '300px' }} />
```

## 监听事件

使用 `onSl*` 属性绑定事件处理函数。

```jsx
import React, { useCallback } from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

export default () => {
  const handleChange = useCallback(event => {
    console.log('选中值变化:', event.target.value);
  }, []);

  const handleClear = useCallback(() => {
    console.log('已清除');
  }, []);

  return (
    <SlCascader
      options={options}
      placeholder="请选择"
      clearable
      onSlChange={handleChange}
      onSlClear={handleClear}
      style={{ width: '300px' }}
    />
  );
};
```

## 编程式控制

通过 `ref` 调用组件方法。

```jsx
import React, { useRef } from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

export default () => {
  const ref = useRef(null);

  const handleShow = () => {
    ref.current?.show();
  };

  const handleHide = () => {
    ref.current?.hide();
  };

  const handleReset = () => {
    if (ref.current) {
      ref.current.value = [];
    }
  };

  return (
    <>
      <button onClick={handleShow}>打开</button>
      <button onClick={handleHide}>关闭</button>
      <button onClick={handleReset}>重置</button>
      <SlCascader ref={ref} options={options} placeholder="请选择" style={{ width: '300px' }} />
    </>
  );
};
```

## 表单集成

级联选择器支持表单集成，可通过 `name` 和 `required` 属性参与表单提交和验证。

```jsx
import React from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

export default () => (
  <form>
    <SlCascader
      name="region"
      label="所在地区"
      options={options}
      placeholder="请选择"
      required
      style={{ width: '300px' }}
    />
    <button type="submit">提交</button>
  </form>
);
```

## 表单验证

```jsx
const ref = useRef(null);

// 检查有效性（不显示提示）
const isValid = ref.current?.checkValidity();

// 检查有效性并显示浏览器提示
ref.current?.reportValidity();

// 设置自定义验证消息
ref.current?.setCustomValidity('请选择地区');

// 清除自定义验证消息
ref.current?.setCustomValidity('');
```

## Properties

| 属性                 | 描述                                                   | 类型                                                                               | 默认值           |
| -------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------- | ---------------- |
| name                 | 表单提交时的字段名                                     | `string`                                                                           | `''`             |
| value                | 当前选中路径值数组（单选为 `string[]`，多选为 `string[][]`） | `(string \| number)[] \| (string \| number)[][]`                                    | `[]`             |
| size                 | 组件尺寸                                               | `'small' \| 'medium' \| 'large'`                                                   | `'medium'`       |
| placeholder          | 占位文本                                               | `string`                                                                           | `''`             |
| multiple             | 是否多选                                               | `boolean`                                                                          | `false`          |
| disabled             | 是否禁用                                               | `boolean`                                                                          | `false`          |
| panelDisabled        | 是否禁用面板选项交互（面板可打开但选项不可操作）       | `boolean`                                                                          | `false`          |
| allowClear           | 是否显示清除按钮                                       | `boolean`                                                                          | `true`           |
| open                 | 下拉面板是否打开                                       | `boolean`                                                                          | `false`          |
| defaultOpen          | 初始是否展开下拉面板                                   | `boolean`                                                                          | `false`          |
| hoist                | 是否使用 fixed 定位策略                                | `boolean`                                                                          | `true`           |
| label                | 标签文本                                               | `string`                                                                           | `''`             |
| placement            | 下拉面板弹出位置                                       | `'bottomLeft' \| 'bottomRight' \| 'topLeft' \| 'topRight'`                         | `'bottomLeft'`   |
| helpText             | 帮助文本                                               | `string`                                                                           | `''`             |
| required             | 是否必填                                               | `boolean`                                                                          | `false`          |
| form                 | 关联的表单 ID                                          | `string`                                                                           | `''`             |
| options              | 级联选项数据                                           | `CascaderOption[]`                                                                 | `[]`             |
| fieldNames           | 自定义字段名映射                                       | `FieldNames`                                                                       | `{ label: 'label', value: 'value', children: 'children' }` |
| separator            | 路径分隔符                                             | `string`                                                                           | `' / '`          |
| expandTrigger        | 子级展开触发方式                                       | `'click' \| 'hover'`                                                               | `'click'`        |
| changeOnSelect       | 是否选中非叶子节点即改变值                             | `boolean`                                                                          | `false`          |
| showFullPath         | 是否在输入框中显示完整路径                             | `boolean`                                                                          | `true`           |
| variant              | 外观变体                                               | `'outlined' \| 'borderless' \| 'filled' \| 'underlined'`                           | `'outlined'`     |
| status               | 验证状态                                               | `'error' \| 'warning' \| ''`                                                       | `''`             |
| showSearch           | 是否显示搜索输入框                                     | `boolean \| ShowSearchConfig`                                                      | `false`          |
| notFoundContent      | 无匹配结果时显示的内容                                 | `string`                                                                           | `'Not Found'`    |
| loadData             | 异步加载数据函数                                       | `(selectedOptions: CascaderOption[]) => void`                                      | `null`           |
| displayRender        | 自定义已选项显示渲染                                   | `(labels: string[], selectedOptions: CascaderOption[]) => string`                  | `null`           |
| optionRender         | 自定义选项渲染                                       | `(option: CascaderOption) => string \| HTMLElement`                                | `null`           |
| maxTagCount          | 多选模式下最多显示的标签数                             | `number`                                                                           | -                |
| maxTagPlaceholder    | 超出最大标签数时的占位文本                             | `string`                                                                           | `''`             |
| maxTagTextLength     | 标签文本最大显示长度                                   | `number`                                                                           | -                |
| showCheckedStrategy  | 多选模式选中项展示策略                                 | `'show-parent' \| 'show-child'`                                                    | `'show-parent'`  |

## Events

| 事件名称      | JSX 属性        | 描述                       | 事件详情 |
| ------------- | --------------- | -------------------------- | -------- |
| sl-change     | `onSlChange`    | 选中值变化时触发           | -        |
| sl-clear      | `onSlClear`     | 清除按钮点击时触发         | -        |
| sl-input      | `onSlInput`     | 输入值变化时触发           | -        |
| sl-focus      | `onSlFocus`     | 获得焦点时触发             | -        |
| sl-blur       | `onSlBlur`      | 失去焦点时触发             | -        |
| sl-show       | `onSlShow`      | 下拉面板打开时触发         | -        |
| sl-after-show | `onSlAfterShow` | 下拉面板打开动画完成后触发 | -        |
| sl-hide       | `onSlHide`      | 下拉面板关闭时触发         | -        |
| sl-after-hide | `onSlAfterHide` | 下拉面板关闭动画完成后触发 | -        |

## Methods

| 方法名              | 描述                               | 参数              | 返回值                    |
| ------------------- | ---------------------------------- | ----------------- | ------------------------- |
| show()              | 打开下拉面板                       | -                 | `Promise<void>`           |
| hide()              | 关闭下拉面板                       | -                 | `Promise<void>`           |
| focus(options?)     | 聚焦到输入框                       | `FocusOptions?`   | `void`                    |
| blur()              | 移除焦点                           | -                 | `void`                    |
| checkValidity()     | 检查有效性（不显示提示）           | -                 | `boolean`                 |
| reportValidity()    | 检查有效性并显示浏览器提示         | -                 | `boolean`                 |
| setCustomValidity() | 设置自定义验证消息，传空字符串恢复 | `message: string` | `void`                    |
| getForm()           | 获取关联的表单元素                 | -                 | `HTMLFormElement \| null` |

## Slots

| 插槽名      | 描述                                |
| ----------- | ----------------------------------- |
| label       | 标签内容，替代 `label` 属性        |
| help-text   | 帮助文本，替代 `helpText` 属性     |
| prefix      | 输入框前缀图标或元素               |
| suffix      | 输入框后缀图标或元素               |
| clear-icon  | 自定义清除图标                     |
| expand-icon | 自定义展开/收起图标                |
| not-found   | 无匹配结果时显示的自定义内容       |

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
| menu                   | 级联菜单容器                             |
| menu-column            | 级联菜单列                               |
| menu-item              | 级联菜单项                               |
| tags                   | 标签容器（多选模式）                     |
| tag                    | 单个标签                                 |
| clear-button           | 清除按钮                                 |
| expand-icon            | 展开图标容器                             |
| search-input           | 搜索输入框（showSearch 启用时）          |
| not-found              | 无匹配结果容器                           |

## 事件处理最佳实践

`sl-change` 等事件在 React 中使用 `onSlChange` 属性绑定（遵循 `onSl*` 命名规范）：

```jsx
import React, { useCallback } from 'react';
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';

const handleChange = useCallback(event => {
  console.log('选中值变化:', event.target.value);
}, []);

const handleClear = useCallback(() => {
  console.log('已清除');
}, []);

<SlCascader onSlChange={handleChange} onSlClear={handleClear} />;
```

## 最佳实践

### 1. 正确导入组件

```javascript
import SlCascader from '@kdcloudjs/shoelace/dist/react/cascader/index.js';
```

### 2. options、fieldNames 等属性直接通过 JSX 属性传入

`@lit/react` 的 `createComponent` 会将所有 Lit `@property()` 声明的属性映射为 React props，包括 `attribute: false` 的属性。因此复杂对象属性可以直接传入：

```jsx
<SlCascader
  options={[
    { value: 'zhejiang', label: '浙江', children: [...] }
  ]}
  fieldNames={{ label: 'name', value: 'code', children: 'items' }}
/>
```

### 3. 使用 useCallback 包裹事件处理函数

```jsx
const handleChange = useCallback(event => {
  console.log('选中值:', event.target.value);
}, []);

<SlCascader onSlChange={handleChange} />;
```

### 4. 通过 ref 调用组件方法

需要调用 `show()`、`hide()` 等方法时，使用 `ref`：

```jsx
const ref = useRef(null);

const handleShow = () => {
  ref.current?.show();
};

<SlCascader ref={ref} />;
```

### 5. 动态更新也可通过 ref

当需要在事件回调中命令式地更新属性时，也可以通过 `ref` 操作：

```jsx
const ref = useRef(null);

const handleReset = () => {
  if (ref.current) {
    ref.current.options = newOptions;
    ref.current.value = [];
  }
};
```

## 常见问题

### Q: options 可以直接通过 JSX 属性传入吗？

A: 可以。`@lit/react` 的 `createComponent` 会将 Lit 组件的所有 `@property()` 属性（包括 `attribute: false` 的）映射为 React props，所以 `options`、`fieldNames` 都可以直接作为 JSX 属性传入。

### Q: 如何获取选中的完整路径值？

A: 监听 `onSlChange` 事件，通过 `ref.current.value` 或 `event.target.value` 获取选中路径值数组。例如选中「浙江 / 杭州 / 西湖区」时，`value` 为 `['zhejiang', 'hangzhou', 'xihu']`。

### Q: 如何仅显示最后一级标签？

A: 设置 `showFullPath={false}`，输入框中将仅显示最后一级选项的标签。

### Q: value 的格式是什么？

A: `value` 是一个字符串数组（`string[]`），表示从根到选中节点的路径。例如 `['zhejiang', 'hangzhou', 'xihu']`。

### Q: 受控模式 vs 非受控模式有什么区别？

A:

- **非受控模式**：设置初始 `value`，组件内部管理状态。
- **受控模式**：使用 `value` 属性，需要在 `onSlChange` 回调中更新状态。
