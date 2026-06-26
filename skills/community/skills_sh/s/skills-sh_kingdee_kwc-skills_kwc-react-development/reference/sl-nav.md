# Nav 导航组件 Skill

## 组件概述

`SlNav` 现在以 **Ant Design Menu API 兼容** 为核心，保留 Shoelace 的视觉呈现。核心组件包括：

- `SlNav`
- `SlNavItem`
- `SlNavGroup`
- `SlNavSubmenu`

相比旧版，核心状态已经从 `value` 切换为 `key / selectedKeys / openKeys`。

## 功能列表

| 功能 | 说明 |
|------|------|
| Antd 兼容 API | 支持 `items`、`selectedKeys`、`defaultSelectedKeys`、`openKeys`、`defaultOpenKeys` |
| 三种模式 | `inline`、`vertical`、`horizontal` |
| 折叠菜单 | `inlineCollapsed` |
| 多选与禁选 | `multiple`、`selectable` |
| 子菜单交互 | `triggerSubMenuAction`、`subMenuOpenDelay`、`subMenuCloseDelay` |
| 回调属性 | `onClick`、`onSelect`、`onDeselect`、`onOpenChange` |
| 事件监听 | `onSlChange`、`onSlNavOpenChange`、`onSlNavSelect` |

## 核心约束

### 必须遵守的规则

1. **导入必须使用 React Wrapper**
   ```js
   import SlNav from '@kdcloudjs/shoelace/dist/react/nav/index.js';
   import SlNavItem from '@kdcloudjs/shoelace/dist/react/nav-item/index.js';
   import SlNavGroup from '@kdcloudjs/shoelace/dist/react/nav-group/index.js';
   import SlNavSubmenu from '@kdcloudjs/shoelace/dist/react/nav-submenu/index.js';
   ```

2. **状态体系已经改为 `key`**
   - 数据模型仍然以 `key` 为唯一标识
   - **React 子组件组合写法请优先使用 `itemKey`**，因为 React 自身的 `key` 不会透传给自定义元素
   - 选中状态使用 `selectedKeys`
   - 展开状态使用 `openKeys`
   - 不要继续按旧版 `value` 写逻辑

3. **React 中有两类入口都可用**
   - Web Component 事件：`onSlChange`、`onSlNavOpenChange`、`onSlNavSelect`
   - 兼容回调属性：`onClick`、`onSelect`、`onDeselect`、`onOpenChange`

4. **模式语义必须按新版本理解**
   - `inline`：默认侧边栏行为
   - `vertical`：弹出式垂直菜单
   - `horizontal`：顶部菜单
   - `inlineCollapsed` 只配合 `inline`
   - 当 `inlineCollapsed` 或 `mode` 切换时，组件会主动清空当前展开的 submenu

5. **`SlNavGroup` 没有 `title` 属性**
   - JSX 结构写法用 `<span slot="title">基础设置</span>`
   - `items` API 用 `label`

## 快速开始

### 组件导入

```jsx
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';
import SlNav from '@kdcloudjs/shoelace/dist/react/nav/index.js';
import SlNavItem from '@kdcloudjs/shoelace/dist/react/nav-item/index.js';
import SlNavGroup from '@kdcloudjs/shoelace/dist/react/nav-group/index.js';
import SlNavSubmenu from '@kdcloudjs/shoelace/dist/react/nav-submenu/index.js';
```

### 最简示例

```jsx
import React from 'react';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';
import SlNav from '@kdcloudjs/shoelace/dist/react/nav/index.js';
import SlNavItem from '@kdcloudjs/shoelace/dist/react/nav-item/index.js';

export default function BasicNav() {
  return (
    <SlNav defaultSelectedKeys={['home']}>
      <SlNavItem itemKey="home">
        <SlIcon slot="prefix" name="house" />
        首页
      </SlNavItem>
      <SlNavItem itemKey="profile">
        <SlIcon slot="prefix" name="person" />
        个人中心
      </SlNavItem>
    </SlNav>
  );
}
```

### 受控侧边导航示例

```jsx
import React, { useState, useCallback } from 'react';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';
import SlNav from '@kdcloudjs/shoelace/dist/react/nav/index.js';
import SlNavItem from '@kdcloudjs/shoelace/dist/react/nav-item/index.js';
import SlNavGroup from '@kdcloudjs/shoelace/dist/react/nav-group/index.js';
import SlNavSubmenu from '@kdcloudjs/shoelace/dist/react/nav-submenu/index.js';

export default function SidebarNav() {
  const [selectedKeys, setSelectedKeys] = useState(['security']);
  const [openKeys, setOpenKeys] = useState(['system']);

  const handleChange = useCallback((event) => {
    setSelectedKeys([...event.detail.selectedKeys]);
  }, []);

  const handleOpenChange = useCallback((event) => {
    setOpenKeys([...event.detail.openKeys]);
  }, []);

  return (
    <SlNav
      mode="inline"
      style={{ maxWidth: '256px' }}
      selectedKeys={selectedKeys}
      openKeys={openKeys}
      onSlChange={handleChange}
      onSlNavOpenChange={handleOpenChange}
    >
      <SlNavSubmenu itemKey="system" title="系统设置">
        <SlIcon slot="prefix" name="gear" />
        <SlNavGroup>
          <span slot="title">基础设置</span>
          <SlNavItem itemKey="profile">个人资料</SlNavItem>
          <SlNavItem itemKey="security">安全设置</SlNavItem>
        </SlNavGroup>
      </SlNavSubmenu>
    </SlNav>
  );
}
```

### `items` API 示例

```jsx
import React, { useState } from 'react';
import SlNav from '@kdcloudjs/shoelace/dist/react/nav/index.js';

export default function DataDrivenNav() {
  const [selectedKeys, setSelectedKeys] = useState(['logs']);
  const [openKeys, setOpenKeys] = useState(['system']);

  return (
    <SlNav
      mode="inline"
      style={{ maxWidth: '256px' }}
      items={[
        { key: 'dashboard', label: 'Dashboard' },
        {
          key: 'system',
          label: 'System',
          children: [
            { key: 'logs', label: 'Logs' },
            { key: 'alerts', label: 'Alerts', danger: true }
          ]
        }
      ]}
      selectedKeys={selectedKeys}
      openKeys={openKeys}
      onSelect={info => setSelectedKeys([...info.selectedKeys])}
      onOpenChange={keys => setOpenKeys([...keys])}
    />
  );
}
```

### 只展开当前父级菜单示例

```jsx
import React, { useState, useCallback } from 'react';
import SlNav from '@kdcloudjs/shoelace/dist/react/nav/index.js';
import SlNavItem from '@kdcloudjs/shoelace/dist/react/nav-item/index.js';
import SlNavSubmenu from '@kdcloudjs/shoelace/dist/react/nav-submenu/index.js';

export default function AccordionNav() {
  const rootSubmenuKeys = ['system', 'workspace'];
  const [selectedKeys, setSelectedKeys] = useState(['security']);
  const [openKeys, setOpenKeys] = useState(['system']);

  const handleChange = useCallback((event) => {
    setSelectedKeys([...event.detail.selectedKeys]);
  }, []);

  const handleOpenChange = useCallback((event) => {
    const nextOpenKeys = [...event.detail.openKeys];
    const latestRootKey = nextOpenKeys.find(key => !openKeys.includes(key));

    if (!latestRootKey) {
      setOpenKeys(nextOpenKeys);
      return;
    }

    setOpenKeys(rootSubmenuKeys.includes(latestRootKey) ? [latestRootKey] : nextOpenKeys);
  }, [openKeys]);

  return (
    <SlNav
      mode="inline"
      style={{ maxWidth: '256px' }}
      selectedKeys={selectedKeys}
      openKeys={openKeys}
      onSlChange={handleChange}
      onSlNavOpenChange={handleOpenChange}
    >
      <SlNavSubmenu itemKey="system" title="系统设置">
        <SlNavItem itemKey="profile">个人资料</SlNavItem>
        <SlNavItem itemKey="security">安全设置</SlNavItem>
      </SlNavSubmenu>

      <SlNavSubmenu itemKey="workspace" title="工作台">
        <SlNavItem itemKey="todo">待办任务</SlNavItem>
        <SlNavItem itemKey="report">报表中心</SlNavItem>
      </SlNavSubmenu>
    </SlNav>
  );
}
```

## API 概览

### `SlNav` 主要属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `items` | Antd 风格菜单数据 | `SlNavItemType[]` | `[]` |
| `selectedKeys` | 受控选中项 | `string[]` | `[]` |
| `defaultSelectedKeys` | 非受控默认选中项 | `string[]` | `[]` |
| `openKeys` | 受控展开子菜单 | `string[]` | `[]` |
| `defaultOpenKeys` | 非受控默认展开子菜单 | `string[]` | `[]` |
| `mode` | 菜单模式 | `'inline' \| 'vertical' \| 'horizontal'` | `'inline'` |
| `multiple` | 是否允许多选 | `boolean` | `false` |
| `selectable` | 是否允许选中 | `boolean` | `true` |
| `inlineCollapsed` | 是否折叠内联菜单 | `boolean` | `false` |
| `inlineIndent` | inline 模式缩进宽度 | `number` | `16` |
| `subMenuOpenDelay` | 子菜单展开延迟，单位秒 | `number` | `0` |
| `subMenuCloseDelay` | 子菜单收起延迟，单位秒 | `number` | `0.1` |
| `triggerSubMenuAction` | 子菜单触发方式 | `'hover' \| 'click'` | `'hover'` |
| `theme` | 主题兼容字段 | `'light' \| 'dark'` | `'light'` |
| `expandIcon` | 自定义展开图标 | `unknown` | - |
| `forceSubMenuRender` | 是否强制渲染子菜单内容 | `boolean` | `false` |
| `overflowedIndicator` | 溢出指示器兼容字段 | `unknown` | - |
| `disabledOverflow` | 是否禁用溢出处理 | `boolean` | `false` |

### `SlNavItem` 主要属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `key` | 菜单项唯一标识 | `string` | `''` |
| `itemKey` | React 安全别名，推荐在 JSX 组合时使用 | `string` | `''` |
| `label` | `items` API 下的标签内容 | `unknown` | - |
| `icon` | `items` API 下的图标内容 | `unknown` | - |
| `extra` | 右侧额外内容 | `unknown` | - |
| `danger` | 危险态菜单项 | `boolean` | `false` |
| `title` | 提示文案 | `string` | `''` |
| `disabled` | 是否禁用 | `boolean` | `false` |
| `active` | 是否激活 | `boolean` | `false` |
| `collapsed` | 是否处于折叠侧栏状态，由父级 nav 同步 | `boolean` | `false` |
| `href` | 跳转链接 | `string` | `''` |
| `target` | 链接打开方式 | `'_blank' \| '_parent' \| '_self' \| '_top'` | - |
| `download` | 下载文件名 | `string` | - |
| `rel` | 链接 rel 属性 | `string` | `'noreferrer noopener'` |

### `SlNavGroup` 主要属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `label` | `items` API 下的分组标题 | `unknown` | - |
| `active` | 组内是否存在激活项 | `boolean` | `false` |

### `SlNavSubmenu` 主要属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `key` | 子菜单唯一标识 | `string` | `''` |
| `itemKey` | React 安全别名，推荐在 JSX 组合时使用 | `string` | `''` |
| `open` | 是否展开 | `boolean` | `false` |
| `nested` | 是否为嵌套子菜单 | `boolean` | `false` |
| `title` | 标题字符串 | `string` | `''` |
| `label` | `items` API 下的标题内容 | `unknown` | - |
| `icon` | `items` API 下的图标内容 | `unknown` | - |
| `theme` | 子菜单主题 | `'light' \| 'dark'` | `'light'` |
| `popupClassName` | 弹层类名 | `string` | `''` |
| `popupOffset` | 弹层偏移 | `[number, number]` | - |
| `disabled` | 是否禁用 | `boolean` | `false` |
| `active` | 是否包含激活项 | `boolean` | `false` |
| `collapsed` | 是否处于折叠侧栏状态，由父级 nav 同步 | `boolean` | `false` |

### 主要事件

| 事件 | React 写法 | 获取方式 |
|------|------------|----------|
| `sl-change` | `onSlChange` | `event.detail.selectedKeys` |
| `sl-nav-open-change` | `onSlNavOpenChange` | `event.detail.openKeys` |
| `sl-nav-select` | `onSlNavSelect` | `event.detail.item`、`event.detail.domEvent` |

### 回调属性

| 属性 | 说明 |
|------|------|
| `onClick` | 点击菜单项时触发，返回 `key`、`keyPath`、`item`、`domEvent` |
| `onSelect` | 选中时触发 |
| `onDeselect` | 多选取消时触发 |
| `onOpenChange` | 展开项变化时触发 |

### 主要 Slots

| 组件 | Slot | 说明 |
|------|------|------|
| `SlNavItem` | `prefix` / `suffix` | 导航项前后缀 |
| `SlNavGroup` | `title` | 分组标题插槽 |
| `SlNavSubmenu` | `title` / `prefix` / `suffix` / `expand-icon` / `collapse-icon` | 子菜单标题与图标区域 |

### 主要方法

| 组件 | 方法 | 说明 |
|------|------|------|
| `SlNavSubmenu` | `show(source?)` | 展开子菜单 |
| `SlNavSubmenu` | `hide(source?)` | 收起子菜单 |

## 使用建议

1. **React 中优先用受控写法**，尤其是路由侧栏、权限菜单和 Layout 导航。
2. **事件和回调不要混着滥用**，普通 React 业务推荐优先 `onSelect` / `onOpenChange`；需要和 DOM 事件统一时再用 `onSl*`。
3. **动态菜单优先 `items`**，静态小菜单再手写 JSX 结构。
4. **`inlineCollapsed` 是新版本折叠侧栏的关键入口**，不要再沿用旧版 `vertical-popup` 思路。
5. **菜单项唯一标识必须稳定**，推荐直接对齐路由 key 或权限编码。
6. **React 子组件组合时统一用 `itemKey`**，只有 `items` 数据对象里才写 `key`。
7. **切换 `inlineCollapsed` 或 `mode` 时记得重置外部 `openKeys` 状态**，因为组件内部会同步清空展开项。
8. **如果要做手风琴侧栏**，在 `onSlNavOpenChange` 中把 `openKeys` 限制为当前一级父菜单即可。
