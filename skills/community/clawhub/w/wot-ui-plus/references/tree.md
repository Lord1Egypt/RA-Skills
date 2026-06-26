# Tree 树形控件


## 组件概况

Tree 树形控件是一种层级数据结构展示组件，用于以树状形式展示具有父子层级关系的数据。该组件支持展开/折叠节点、多选/单选、级联选择、异步加载、搜索过滤等丰富功能，广泛应用于组织架构、分类目录、文件系统、权限管理等场景。

Tree 组件采用扁平化渲染策略，通过内部节点索引和可见节点计算，高效处理多层级树形数据的展示与交互。

## 核心功能描述

- **展开/折叠**：通过节点前的开关按钮（switcher）展开或折叠子节点，支持自定义展开/折叠图标和动画旋转效果
- **多选勾选**：通过 `checkable` 属性开启复选框，支持节点多选，提供受控（`checked-keys`）和非受控（`default-checked-keys`）两种模式
- **级联选择**：开启 `cascade` 后，勾选父节点会联动勾选所有子节点，勾选子节点会影响父节点的半选状态
- **单选选中**：通过 `selectable` 属性开启单选模式，点击节点高亮选中，使用 `selectedBgColor` 控制高亮背景色
- **异步加载**：通过 `load-node` 函数实现子节点的异步加载，展开节点时动态请求数据并插入到对应子节点中
- **搜索过滤**：通过 `pattern` 属性设置搜索关键词，匹配节点标签文字；`showIrrelevantNodes` 控制是否显示未匹配的节点
- **自定义字段名**：支持通过 `key-field`、`label-field`、`children-field`、`is-leaf-field`、`disabled-field` 自定义数据字段的映射关系
- **点击展开/勾选**：通过 `expand-on-click` 和 `check-on-click` 实现点击节点内容区域即可展开或勾选，无需精确点击图标
- **自定义节点内容**：提供 `content` 和 `switcher` 插槽，允许完全自定义节点内容和展开按钮的渲染
- **受控模式**：支持 `checked-keys` 和 `expanded-keys` 受控属性，配合 `update:checked-keys` 和 `update:expanded-keys` 事件实现外部状态管理

## 适用业务场景

- **组织架构展示**：展示公司部门层级、团队结构、员工汇报关系等
- **分类目录管理**：商品分类、文件目录、标签体系等层级分类数据展示
- **权限角色管理**：权限树勾选，通过级联选择快速分配权限集合
- **异步数据加载**：数据量较大的树形结构，按需加载子节点数据提升性能
- **搜索导航**：在复杂层级结构中快速搜索定位目标节点

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| data | 树形数据源，为数组类型，每项包含节点字段及子节点 | array | - | [] | - |
| keyField | 节点唯一标识映射的字段名 | string | - | 'id' | - |
| labelField | 节点展示值映射的字段名 | string | - | 'label' | - |
| childrenField | 子节点数组映射的字段名 | string | - | 'children' | - |
| isLeafField | 判断是否为叶子节点的字段名 | string | - | 'isLeaf' | - |
| disabledField | 判断节点是否禁用的字段名 | string | - | 'disabled' | - |
| defaultCheckedKeys | 默认选中的节点 key 数组 | array | - | [] | - |
| defaultExpandedKeys | 默认展开的节点 key 数组 | array | - | [] | - |
| checkedKeys | 受控的选中节点 key 数组，传入后组件内部状态由外部控制 | array | - | - | - |
| expandedKeys | 受控的展开节点 key 数组，传入后组件内部状态由外部控制 | array | - | - | - |
| checkable | 是否显示复选框（可选择） | boolean | - | false | - |
| selectable | 是否开启单选选中模式 | boolean | - | false | - |
| cascade | 是否开启级联选择（勾选父节点联动子节点） | boolean | - | false | - |
| expandOnClick | 是否允许点击节点内容区域展开/收缩 | boolean | - | false | - |
| checkOnClick | 是否允许点击节点内容区域勾选/取消勾选 | boolean | - | false | - |
| loadNode | 异步加载子节点数据的函数，接收节点对象作为参数，返回 Promise | function | - | - | - |
| allowCheckingNotLoaded | 是否允许勾选未加载子节点的节点（异步加载场景） | boolean | - | false | - |
| pattern | 搜索过滤关键词，匹配节点 label 中包含该字符串的节点 | string | - | '' | - |
| showIrrelevantNodes | 搜索时是否显示未匹配关键词的节点 | boolean | - | true | - |
| indentWidth | 每级缩进宽度，单位为 px | number / string | - | 24 | - |
| showSwitcher | 是否显示展开/收缩按钮 | boolean | - | true | - |
| expandIcon | 展开状态时的图标名称 | string | - | 'right-box-filled' | - |
| collapseIcon | 收缩状态时的图标名称 | string | - | 'down-box-filled' | - |
| loadingColor | 异步加载时的 loading 颜色 | string | - | '' | - |
| checkedColor | 复选框选中时的颜色 | string | - | '' | - |
| rotatableSwitcher | 展开/收缩按钮是否可旋转动画 | boolean | - | false | - |
| highlightBgColor | 搜索匹配节点的高亮背景颜色 | string | - | '#f9ae3d' | - |
| selectedBgColor | 单选模式下选中节点的背景颜色 | string | - | '#f3f4f6' | - |
| switcherSize | 展开/收缩按钮大小 | number / string | - | 14 | - |
| switcherColor | 展开/收缩按钮颜色 | string | - | '#909399' | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| switcher | 自定义展开/收缩按钮，作用域参数 `{ hide, loading, expanded }` 分别表示是否隐藏按钮、是否正在加载、是否已展开 | 按钮内容（图标、动画等） |
| content | 自定义节点内容，作用域参数 `{ node }` 为当前节点完整数据 | 节点内容（文字、标签等） |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| click | 节点点击事件 | 事件参数 |
| checked | 节点勾选变化事件 | `(string \| number)[]` - 当前所有已勾选的节点 key 数组 |
| expanded | 节点展开/折叠变化事件 | `(string \| number)[]` - 当前所有已展开的节点 key 数组 |
| update:checked-keys | 受控模式下选中 key 变化事件，用于 v-model:checked-keys | `(string \| number)[]` - 当前所有已勾选的节点 key 数组 |
| update:expanded-keys | 受控模式下展开 key 变化事件，用于 v-model:expanded-keys | `(string \| number)[]` - 当前所有已展开的节点 key 数组 |

## 使用示例

### 基础用法

通过 `data` 属性传入树形数据，每个节点需要包含 `id`（节点唯一标识）和 `label`（节点展示文字），子节点通过 `children` 数组嵌套。使用 `default-expanded-keys` 设置默认展开的节点。

```vue
<template>
  <wd-tree :data="basicData" :default-expanded-keys="['1', '1-1']" expand-on-click checkable />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface TreeNode {
    label: string
    id: string
    children?: TreeNode[]
  }

  const basicData = ref<TreeNode[]>([
    {
      label: '技术部',
      id: '1',
      children: [
        {
          label: '前端组',
          id: '1-1',
          children: [
            { label: 'Vue开发', id: '1-1-1' },
            { label: 'React开发', id: '1-1-2' }
          ]
        },
        {
          label: '后端组',
          id: '1-2',
          children: [
            { label: 'Java开发', id: '1-2-1' },
            { label: 'Python开发', id: '1-2-2' }
          ]
        }
      ]
    }
  ])
</script>
```

### 级联选择

开启 `cascade` 属性后，勾选父节点会自动勾选所有子节点，勾选子节点会根据兄弟节点状态自动更新父节点的半选或全选状态。

```vue
<template>
  <wd-tree
    :data="cascadeData"
    cascade
    checkable
    :default-expanded-keys="['0', '0-0', '0-1', '0-2']"
    :default-checked-keys="['0-0-0']"
    @checked="updateCheckedKeys"
  />
  <view class="checked-info">
    <text>已选中: {{ checkedKeys.join(', ') || '无' }}</text>
  </view>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface TreeNode {
    label: string
    id: string
    children?: TreeNode[]
  }

  const cascadeData = ref<TreeNode[]>([
    {
      label: '文件系统',
      id: '0',
      children: [
        {
          label: '文档',
          id: '0-0',
          children: [
            { label: '工作文档', id: '0-0-0' },
            { label: '学习资料', id: '0-0-1' },
            { label: '项目文件', id: '0-0-2' }
          ]
        },
        {
          label: '媒体',
          id: '0-1',
          children: [
            { label: '图片', id: '0-1-0' },
            { label: '视频', id: '0-1-1' },
            { label: '音频', id: '0-1-2' }
          ]
        },
        {
          label: '应用程序',
          id: '0-2',
          children: [
            { label: '系统工具', id: '0-2-0' },
            { label: '办公软件', id: '0-2-1' },
            { label: '娱乐软件', id: '0-2-2' }
          ]
        }
      ]
    }
  ])

  const checkedKeys = ref<string[]>([])

  const updateCheckedKeys = (keys: string[]): void => {
    checkedKeys.value = keys
  }
</script>

<style lang="scss" scoped>
  .checked-info {
    margin-top: 20rpx;
    padding: 20rpx;
    background-color: #f8f9fa;
    border-radius: 8rpx;
    font-size: 28rpx;
    color: #666;
  }
</style>
```

### 搜索过滤

通过 `pattern` 属性绑定搜索关键词，树组件会自动过滤并高亮匹配的节点。设置 `show-irrelevant-nodes="false"` 可仅显示匹配的节点及其祖先路径。

```vue
<template>
  <wd-input v-model="searchPattern" placeholder="输入节点名称搜索" :clearable="true" />
  <wd-tree :data="searchData" expand-on-click :pattern="searchPattern" :show-irrelevant-nodes="showIrrelevantNodes" />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface TreeNode {
    label: string
    id: string
    children?: TreeNode[]
  }

  const searchPattern = ref<string>('')
  const showIrrelevantNodes = ref<boolean>(false)

  const searchData = ref<TreeNode[]>([
    {
      label: '项目管理',
      id: '0',
      children: [
        {
          label: '需求分析',
          id: '0-0',
          children: [
            { label: '用户调研', id: '0-0-0' },
            { label: '功能规划', id: '0-0-1' },
            { label: '原型设计', id: '0-0-2' }
          ]
        },
        {
          label: '开发阶段',
          id: '0-1',
          children: [
            { label: '前端开发', id: '0-1-0' },
            { label: '后端开发', id: '0-1-1' },
            { label: '测试调试', id: '0-1-2' }
          ]
        },
        {
          label: '部署上线',
          id: '0-2',
          children: [
            { label: '环境配置', id: '0-2-0' },
            { label: '数据迁移', id: '0-2-1' },
            { label: '监控运维', id: '0-2-2' }
          ]
        }
      ]
    }
  ])
</script>
```

### 自定义字段名

当数据源字段名与组件默认字段不一致时，可通过 `key-field`、`label-field`、`children-field` 等属性自定义字段映射。

```vue
<template>
  <wd-tree
    :data="customFieldData"
    :default-expanded-keys="['1', '1-1']"
    key-field="key"
    label-field="name"
    children-field="items"
    selectable
  />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface CustomTreeNode {
    name: string
    key: string
    items?: CustomTreeNode[]
  }

  const customFieldData = ref<CustomTreeNode[]>([
    {
      name: '电子产品',
      key: '1',
      items: [
        {
          name: '手机数码',
          key: '1-1',
          items: [
            { name: '智能手机', key: '1-1-1' },
            { name: '平板电脑', key: '1-1-2' }
          ]
        },
        {
          name: '电脑办公',
          key: '1-2',
          items: [
            { name: '笔记本电脑', key: '1-2-1' },
            { name: '台式电脑', key: '1-2-2' }
          ]
        }
      ]
    }
  ])
</script>
```

### 异步加载

通过 `load-node` 属性传入加载函数，在展开节点时异步请求子节点数据。加载期间显示 loading 动画，加载完成后自动渲染子节点。

```vue
<template>
  <wd-tree :data="asyncData" :load-node="loadNodeData" />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface TreeNode {
    label: string
    id: string
    children?: TreeNode[]
    isLeaf?: boolean
  }

  interface LoadNodeParams {
    id: string
    label: string
    children?: TreeNode[]
  }

  const asyncData = ref<TreeNode[]>([
    { label: '在线课程', id: '1', children: [] },
    { label: '技术文档', id: '2', children: [] },
    { label: '开源项目', id: '3', children: [] }
  ])

  const loadNodeData = (node: LoadNodeParams): Promise<boolean> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const childrenMap: Record<string, TreeNode[]> = {
          '1': [
            { label: 'Vue.js 基础教程', id: '1-1', isLeaf: true },
            { label: 'React 入门指南', id: '1-2', isLeaf: true },
            { label: 'TypeScript 实战', id: '1-3', isLeaf: true }
          ],
          '2': [
            { label: 'API 接口文档', id: '2-1' },
            { label: '组件使用说明', id: '2-2' },
            { label: '最佳实践指南', id: '2-3' }
          ],
          '3': [
            { label: 'UI 组件库', id: '3-1' },
            { label: '工具函数库', id: '3-2' },
            { label: '示例项目', id: '3-3' }
          ]
        }

        node.children = childrenMap[node.id] || []
        resolve(true)
      }, 1000)
    })
  }
</script>
```

### 自定义图标

通过 `expand-icon` 和 `collapse-icon` 属性自定义展开/折叠状态的图标，同时支持通过 `switcher-size`、`switcher-color` 调整图标样式。

```vue
<template>
  <wd-tree
    :data="basicData"
    :default-expanded-keys="['1', '1-1']"
    expand-icon="unfold-more"
    collapse-icon="unfold-less"
    expand-on-click
    selectable
  />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface TreeNode {
    label: string
    id: string
    children?: TreeNode[]
  }

  const basicData = ref<TreeNode[]>([
    {
      label: '技术部',
      id: '1',
      children: [
        {
          label: '前端组',
          id: '1-1',
          children: [
            { label: 'Vue开发', id: '1-1-1' },
            { label: 'React开发', id: '1-1-2' }
          ]
        },
        {
          label: '后端组',
          id: '1-2',
          children: [
            { label: 'Java开发', id: '1-2-1' },
            { label: 'Python开发', id: '1-2-2' }
          ]
        }
      ]
    }
  ])
</script>
```

### 隐藏箭头

通过设置 `show-switcher="false"` 隐藏展开/折叠按钮，仅保留点击节点内容区域展开的功能（需配合 `expand-on-click`）。

```vue
<template>
  <wd-tree :data="basicData" :default-expanded-keys="['1', '1-1']" :show-switcher="false" expand-on-click checkable />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  interface TreeNode {
    label: string
    id: string
    children?: TreeNode[]
  }

  const basicData = ref<TreeNode[]>([
    {
      label: '技术部',
      id: '1',
      children: [
        {
          label: '前端组',
          id: '1-1',
          children: [
            { label: 'Vue开发', id: '1-1-1' },
            { label: 'React开发', id: '1-1-2' }
          ]
        }
      ]
    }
  ])
</script>
```

## 注意事项

1. **数据字段要求**：每个节点必须包含唯一标识字段（默认 `id`）和展示文字字段（默认 `label`）。子节点通过 `children` 数组嵌套，如字段名不一致，需通过对应的 `*-field` 属性配置映射。

2. **叶子节点判断**：组件通过节点的 `isLeaf` 字段（默认）判断是否为叶子节点。当 `isLeaf` 为 `true` 时，即使节点没有 `children` 数组也不会显示展开按钮。异步加载场景中，未加载子节点的节点不应设置 `isLeaf` 为 `true`。

3. **级联选择状态**：`cascade` 模式下，父节点的勾选状态由子节点决定。当所有子节点都勾选时，父节点自动勾选；当部分子节点勾选时，父节点显示半选状态；当没有子节点勾选时，父节点不勾选。

4. **异步加载规则**：`load-node` 函数接收当前节点对象作为参数，需在此对象上直接设置 `children` 属性添加子节点数据。函数需返回 `Promise`，在数据加载完成后 resolve。

5. **搜索过滤行为**：搜索时组件会自动展开匹配节点的祖先节点路径。`show-irrelevant-nodes` 为 `false` 时仅显示匹配节点及其祖先节点，为 `true` 时显示所有节点但高亮匹配项。

6. **受控与非受控模式**：使用 `default-checked-keys`/`default-expanded-keys` 为非受控模式，组件内部管理选中/展开状态。使用 `checked-keys`/`expanded-keys` 为受控模式，需配合 `@update:checked-keys`/`@update:expanded-keys` 事件手动同步外部状态。

7. **点击展开/勾选**：`expand-on-click` 和 `check-on-click` 控制点击节点内容区域的行为，默认关闭，用户需要精确点击展开图标或复选框。开启后可提升移动端操作体验。

8. **缩进宽度**：`indent-width` 控制每层级的缩进距离，默认 24px。层级较深时可适当增大此值以保证层级关系的可视区分。

9. **自定义插槽**：`content` 插槽提供完整的节点数据 `node` 对象，可用于自定义节点展示（如添加标签、图标、操作按钮等）。`switcher` 插槽可用于自定义展开/折叠按钮的样式和交互。

10. **节点唯一性**：树中所有节点的 `key`（由 `keyField` 指定的字段值）必须唯一，否则会导致展开/勾选状态错乱和搜索过滤异常。
