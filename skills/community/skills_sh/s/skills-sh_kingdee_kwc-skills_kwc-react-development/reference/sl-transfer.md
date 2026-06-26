# Transfer 穿梭框组件

## 组件概述

`SlTransfer` 是一个穿梭框组件，用于在两个列表之间移动数据。支持搜索、分页、全选、单向穿梭、自定义渲染等功能。

## 组件导入

```jsx
import SlTransfer from '@kdcloudjs/shoelace/dist/react/transfer/index.js';
```

## 基础用法

```jsx
import React, { useState } from "react";
import SlTransfer from '@kdcloudjs/shoelace/dist/react/transfer/index.js';

const dataSource = [
    { key: '1', title: '选项一' },
    { key: '2', title: '选项二' },
    { key: '3', title: '选项三' },
    { key: '4', title: '选项四' },
    { key: '5', title: '选项五' }
];

export default () => {
    const [targetKeys, setTargetKeys] = useState(['3', '5']);

    const handleChange = (e) => {
        setTargetKeys(e.detail.targetKeys);
    };

    return (
        <SlTransfer
            dataSource={dataSource}
            targetKeys={targetKeys}
            onSlTransferChange={handleChange}
        />
    );
};
```

## 带搜索框

```jsx
<SlTransfer
    dataSource={dataSource}
    targetKeys={targetKeys}
    showSearch
    searchPlaceholder="搜索"
    onSlTransferChange={handleChange}
/>
```

## 分页

```jsx
<SlTransfer
    dataSource={dataSource}
    targetKeys={targetKeys}
    pagination
    pageSize={5}
    onSlTransferChange={handleChange}
/>
```

## 单向穿梭

```jsx
<SlTransfer
    dataSource={dataSource}
    targetKeys={targetKeys}
    oneWay
    onSlTransferChange={handleChange}
/>
```

## 自定义渲染

```jsx
<SlTransfer
    dataSource={dataSource}
    targetKeys={targetKeys}
    itemRender={(item) => `${item.title} - ${item.key}`}
    onSlTransferChange={handleChange}
/>
```

## 自定义搜索过滤

```jsx
<SlTransfer
    dataSource={dataSource}
    targetKeys={targetKeys}
    showSearch
    filterOption={(inputValue, option) =>
        option.title.toLowerCase().includes(inputValue.toLowerCase())
    }
    onSlTransferChange={handleChange}
/>
```

## 受控选中

通过 `selectedKeys` 属性可以完全控制选中状态，配合 `onSlTransferSelectChange` 事件更新：

```jsx
const [selectedKeys, setSelectedKeys] = useState([]);

const handleSelectChange = (e) => {
    const { sourceSelectedKeys, targetSelectedKeys } = e.detail;
    setSelectedKeys([...sourceSelectedKeys, ...targetSelectedKeys]);
};

<SlTransfer
    dataSource={dataSource}
    targetKeys={targetKeys}
    selectedKeys={selectedKeys}
    onSlTransferChange={handleChange}
    onSlTransferSelectChange={handleSelectChange}
/>
```

## API

### Transfer 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `dataSource` | 数据源 | `TransferItem[]` | `[]` |
| `targetKeys` | 目标列表的 key 集合 | `string[]` | `[]` |
| `disabled` | 是否禁用 | `boolean` | `false` |
| `pagination` | 是否显示分页 | `boolean` | `false` |
| `pageSize` | 每页显示条数 | `number` | `10` |
| `showSearch` | 是否显示搜索框 | `boolean` | `false` |
| `showSelectAll` | 是否显示全选 | `boolean` | `true` |
| `oneWay` | 是否单向穿梭 | `boolean` | `false` |
| `titles` | 两个列表的标题 | `string[]` | `['源列表', '目标列表']` |
| `status` | 组件状态 | `'normal' \| 'success' \| 'error'` | `'normal'` |
| `searchPlaceholder` | 搜索框占位符 | `string` | `'请输入搜索内容'` |
| `selectedKeys` | 受控选中项 key 集合 | `string[]` | - |
| `itemRender` | 自定义渲染列表项内容 | `(item: TransferItem) => unknown` | - |
| `filterOption` | 自定义搜索过滤逻辑 | `(inputValue: string, option: TransferItem, direction: TransferDirection) => boolean` | - |

### TransferItem 数据项

| 属性 | 说明 | 类型 | 必填 |
|------|------|------|------|
| `key` | 唯一标识键 | `string` | 是 |
| `title` | 显示标题 | `string` | 是 |
| `description` | 描述信息 | `string` | 否 |
| `disabled` | 是否禁用 | `boolean` | 否 |

### 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `onSlTransferChange` | 数据穿梭完成时触发 | `{ targetKeys: string[], direction: 'left' \| 'right', moveKeys: string[] }` |
| `onSlTransferSelectChange` | 选中项变化时触发 | `{ sourceSelectedKeys: string[], targetSelectedKeys: string[], type: TransferSelectType }` |
| `onSlTransferSearch` | 搜索时触发 | `{ direction: 'left' \| 'right', value: string }` |
| `onSlTransferScroll` | 列表滚动时触发 | `{ direction: 'left' \| 'right', event: Event }` |

### TransferSelectType

`'single' | 'selectAll' | 'selectAllItems' | 'selectPage' | 'invertPage' | 'api'`

### 方法

| 方法名 | 说明 | 参数 |
|--------|------|------|
| `moveToTarget()` | 将源列表选中项移动到目标列表 | - |
| `moveToSource()` | 将目标列表选中项移动到源列表 | - |
| `setSourceSelectedKeys(keys)` | 设置源列表选中项 | `keys: string[]` |
| `setTargetSelectedKeys(keys)` | 设置目标列表选中项 | `keys: string[]` |

### Slots（插槽）

| Slot | 说明 |
|------|------|
| `move-to-target` | 自定义"移动到目标列表"按钮内容 |
| `move-to-source` | 自定义"移动到源列表"按钮内容 |
| `operation` | 完全自定义操作区域，替换默认穿梭按钮 |
| `source-empty` | 自定义源列表空提示内容 |
| `target-empty` | 自定义目标列表空提示内容 |
| `source-item-list` | 自定义源列表内容区域，替换默认列表渲染 |
| `target-item-list` | 自定义目标列表内容区域，替换默认列表渲染 |
| `source-footer` | 自定义源列表底部内容，位于分页上方 |
| `target-footer` | 自定义目标列表底部内容，位于分页上方 |

### CSS Parts

| Part 名称 | 说明 |
|-----------|------|
| `base` | 组件基础容器 |
| `source-panel` | 源列表面板 |
| `target-panel` | 目标列表面板 |
| `panel-header` | 面板头部 |
| `panel-list` | 面板列表 |
| `operation` | 操作按钮区域 |
| `search-input` | 搜索输入框 |

### CSS 自定义属性

| 属性 | 说明 |
|------|------|
| `--sl-transfer-list-width` | 单个面板的宽度 |
| `--sl-transfer-list-height` | 单个面板的高度 |
| `--sl-transfer-border-color` | 面板边框颜色 |
| `--sl-transfer-border-radius` | 面板圆角 |
| `--sl-transfer-bg-color` | 面板背景色 |
| `--sl-transfer-header-padding` | 面板头部内边距 |
| `--sl-transfer-header-bg-color` | 面板头部背景色 |
| `--sl-transfer-header-font-size` | 面板头部字体大小 |
| `--sl-transfer-search-padding` | 搜索框内边距 |
| `--sl-transfer-list-item-padding` | 列表项内边距 |
| `--sl-transfer-list-item-hover-bg-color` | 列表项悬停背景色 |
| `--sl-transfer-footer-padding` | 底部内边距 |
| `--sl-transfer-operation-button-gap` | 操作按钮间距 |
| `--sl-transfer-border-color-error` | 错误状态边框色 |
| `--sl-transfer-border-color-warn` | 成功状态边框色 |
