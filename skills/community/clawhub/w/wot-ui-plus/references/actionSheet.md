# ActionSheet 动作面板


## 组件概况

ActionSheet 动作面板是一个从底部弹出的选择器组件，用于展示一组操作选项或自定义面板内容。该组件基于 Popup 弹出层实现，通过底部滑入动画展示菜单列表，支持普通列表选项和图标面板两种展示模式，为用户提供了清晰、简洁的操作选择入口。在移动端应用中，动作面板常用于分享菜单、操作选择、确认提示等场景，能够有效减少页面跳转，提升用户操作效率。

## 核心功能描述

- **双模式展示**：支持 `actions` 普通列表模式和 `panels` 图标面板模式，满足不同场景的视觉需求
- **选项状态管理**：支持选项的禁用（disabled）、加载中（loading）、自定义颜色（color）等状态
- **单行/多行面板**：panels 支持一维数组单行滚动展示，也支持二维数组多行展示
- **子描述信息**：actions 模式支持通过 `subname` 字段展示辅助描述信息
- **安全区域适配**：内置底部安全区域（safe-area-inset-bottom）支持，适配 iPhone X 等异形屏机型
- **懒渲染优化**：默认开启懒渲染（lazyRender），触发展示时才渲染内容，提升页面性能
- **根脱离支持**：通过 `rootPortal` 属性解决 fixed 定位失效问题，适配 H5、APP、小程序多端场景
- **丰富的事件机制**：提供 open、opened、close、closed、cancel、select、click-modal 等完整生命周期事件
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **分享操作**：在内容详情页提供分享到微信好友、朋友圈、QQ 等平台的快捷操作面板
- **文件操作**：在文件列表页提供复制、移动、删除、重命名等文件管理操作
- **图片操作**：在图片预览时提供保存到相册、分享、识别等操作选项
- **账户设置**：在个人中心页面提供退出登录、切换账号、清除缓存等设置操作

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | boolean | false | 是 | 控制动作面板的显示与隐藏，支持 v-model 双向绑定 |
| actions | Action[] | [] | 否 | 菜单选项列表，每项包含 name（名称）、subname（描述）、color（颜色）、disabled（禁用）、loading（加载中） |
| panels | Panel \| Panel[] | [] | 否 | 自定义面板项，一维数组为单行滚动展示，二维数组为多行展示，每项包含 iconUrl（图标地址）、title（标题） |
| title | string | - | 否 | 面板标题，显示在面板顶部 |
| cancelText | string | - | 否 | 取消按钮文案，设置后底部显示取消按钮 |
| closeOnClickAction | boolean | true | 否 | 点击选项后是否自动关闭面板 |
| closeOnClickModal | boolean | true | 否 | 点击遮罩层是否自动关闭面板 |
| duration | number | 200 | 否 | 弹出层动画持续时间（毫秒） |
| zIndex | number | 10 | 否 | 面板层级（z-index） |
| lazyRender | boolean | true | 否 | 是否开启懒渲染，触发展示时才渲染内容 |
| safeAreaInsetBottom | boolean | true | 否 | 是否设置底部安全距离，适配 iPhone X 等机型 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 失效问题（H5: teleport, APP: renderjs, 小程序: root-portal） |
| customHeaderClass | string | '' | 否 | 自定义 header 头部样式类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| select | 点击选中某个选项时触发 | `(data: { item: Action \| Panel, index?: number, rowIndex?: number, colIndex?: number })` | actions 模式返回 item（选项对象）和 index（索引）；panels 单行模式返回 item 和 index；panels 多行模式返回 item、rowIndex（行索引）和 colIndex（列索引） |
| cancel | 点击取消按钮时触发 | - | 无参数 |
| close | 面板关闭时触发 | - | 无参数 |
| closed | 面板关闭动画完成时触发 | - | 无参数 |
| open | 面板开始打开时触发 | - | 无参数 |
| opened | 面板打开动画完成时触发 | - | 无参数 |
| click-modal | 点击遮罩层时触发 | - | 无参数 |
| update:modelValue | 面板显示状态变化时触发（v-model 支持） | `(value: boolean)` | 新的显示状态值 |

### Methods

组件本身不对外暴露方法，面板的显示与隐藏通过 `v-model` 或 `modelValue` 属性控制。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义面板内容区域，在 actions/panels 列表和取消按钮之间插入自定义内容，可用于展示自定义表单、图文信息等 |

## 使用示例

### 示例 1：基础用法

最基础的菜单选项展示，通过 `actions` 属性传入选项列表，支持显示子描述信息。

```vue
<template>
  <view>
    <wd-button @click="showActions">弹出菜单</wd-button>
    <wd-action-sheet v-model="show" :actions="actions" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const show = ref<boolean>(false)
  const actions = ref<any[]>([])

  function showActions() {
    show.value = true
    actions.value = [
      {
        name: '选项1'
      },
      {
        name: '选项2'
      },
      {
        name: '选项3',
        subname: '描述信息'
      }
    ]
  }
</script>
```

该示例展示了最基本的动作面板用法，点击按钮后面板从底部弹出，显示三个菜单选项，第三个选项附带了灰色的描述信息。

### 示例 2：选项状态与取消按钮

展示选项的多种状态（自定义颜色、禁用、加载中），并添加取消按钮。

```vue
<template>
  <view>
    <wd-button @click="showActions">弹出菜单</wd-button>
    <wd-action-sheet v-model="show" :actions="actions" cancel-text="取消" @close="close" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const show = ref<boolean>(false)
  const actions = ref<any[]>([])

  function showActions() {
    show.value = true
    actions.value = [
      {
        name: '颜色',
        color: '#0083ff'
      },
      {
        name: '禁用',
        disabled: true
      },
      {
        loading: true
      }
    ]
  }

  function close() {
    show.value = false
  }
</script>
```

该示例中，第一个选项使用蓝色文字，第二个选项处于禁用状态（灰色且不可点击），第三个选项显示加载动画。底部显示取消按钮，点击可关闭面板。

### 示例 3：自定义面板单行展示

使用 `panels` 属性展示带图标的单行滚动面板，常用于分享场景。

```vue
<template>
  <view>
    <wd-button @click="showActions">弹出菜单</wd-button>
    <wd-action-sheet v-model="show" :panels="panels" cancel-text="取消" @close="close" @select="select" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const show = ref<boolean>(false)
  const panels = ref<any[]>([])

  function showActions() {
    show.value = true
    panels.value = [
      {
        iconUrl: 'https://img12.360buyimg.com/imagetools/jfs/t1/122016/33/6657/1362/5f0692a1E8708d245/e47299e5945a6956.png',
        title: '微信好友'
      },
      {
        iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/111572/11/11734/1245/5f0692a1E39d13d21/b35dfe9243bd6c2a.png',
        title: '微信朋友圈'
      },
      {
        iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/132639/25/4003/945/5f069336E18778248/fa181913030bed8a.png',
        title: 'QQ好友'
      },
      {
        iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/134807/4/3950/1256/5f069336E76949e27/d20641da8e699f07.png',
        title: '微信收藏'
      }
    ]
  }

  function close() {
    show.value = false
  }

  function select({ item, index }: { item: any; index: number }) {
    console.log(`当前选中：${item.title}，下标：${index}`)
  }
</script>
```

该示例使用面板模式展示带图标的选项，选项横向排列可左右滚动，每项包含图标和标题。点击选项时触发 select 事件，返回选中项的信息。

### 示例 4：自定义面板多行展示

使用二维数组传入 `panels`，实现多行面板布局。

```vue
<template>
  <view>
    <wd-button @click="showActions">弹出菜单</wd-button>
    <wd-action-sheet v-model="show" :panels="panels" cancel-text="取消" @close="close" @select="select" />
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const show = ref<boolean>(false)
  const panels = ref<any[]>([])

  function showActions() {
    show.value = true
    panels.value = [
      [
        {
          iconUrl: 'https://img12.360buyimg.com/imagetools/jfs/t1/122016/33/6657/1362/5f0692a1E8708d245/e47299e5945a6956.png',
          title: '微信好友'
        },
        {
          iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/111572/11/11734/1245/5f0692a1E39d13d21/b35dfe9243bd6c2a.png',
          title: '微信朋友圈'
        },
        {
          iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/132639/25/4003/945/5f069336E18778248/fa181913030bed8a.png',
          title: 'QQ好友'
        },
        {
          iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/134807/4/3950/1256/5f069336E76949e27/d20641da8e699f07.png',
          title: '微信收藏'
        }
      ],
      [
        {
          iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/132639/25/4003/945/5f069336E18778248/fa181913030bed8a.png',
          title: 'QQ好友'
        },
        {
          iconUrl: 'https://img14.360buyimg.com/imagetools/jfs/t1/134807/4/3950/1256/5f069336E76949e27/d20641da8e699f07.png',
          title: '微信收藏'
        }
      ]
    ]
  }

  function close() {
    show.value = false
  }

  function select({ item, rowIndex, colIndex }: { item: any; rowIndex: number; colIndex: number }) {
    console.log(`当前选中：${item.title}，行下标：${rowIndex}，列下标：${colIndex}`)
  }
</script>
```

该示例通过二维数组定义多行面板，每行内的选项可横向滚动。多行模式下 select 事件返回 rowIndex（行索引）和 colIndex（列索引），方便定位选中项。

### 示例 5：标题与自定义内容

使用 `title` 属性设置面板标题，并通过默认插槽插入自定义内容。

```vue
<template>
  <view>
    <wd-button @click="showActions">弹出菜单</wd-button>
    <wd-action-sheet v-model="show" title="标题" @close="close" cancel-text="取消">
      <view style="padding: 15px 15px 150px 15px">自定义内容区域</view>
    </wd-action-sheet>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const show = ref<boolean>(false)

  function showActions() {
    show.value = true
  }

  function close() {
    show.value = false
  }
</script>
```

该示例展示了带标题的面板，并在默认插槽中插入了自定义内容区域，适用于需要在动作面板中展示复杂内容的场景。标题右侧会自动显示关闭按钮。

## 注意事项

1. **actions 与 panels 互斥**：同时传入 `actions` 和 `panels` 时，两者会同时渲染，建议根据实际需求只使用其中一个
2. **modelValue 必填**：`modelValue` 为必填属性，必须使用 v-model 或 :modelValue 控制面板显示状态
3. **disabled 与 loading 状态**：当选项的 `disabled` 或 `loading` 为 true 时，点击该选项不会触发 select 事件
4. **自动关闭控制**：设置 `closeOnClickAction` 为 false 时，点击选项后面板不会自动关闭，需在 select 事件回调中手动关闭
5. **面板模式 select 事件参数差异**：actions 模式返回 `{ item, index }`，panels 单行模式返回 `{ item, index }`，panels 多行模式返回 `{ item, rowIndex, colIndex }`，需根据实际模式处理回调参数
6. **rootPortal 使用场景**：当面板内部包含 fixed 定位元素或在某些平台出现定位异常时，可设置 `rootPortal` 为 true 将面板脱离当前页面层级
7. **自定义内容高度**：使用默认插槽插入自定义内容时，需注意内容高度可能超出屏幕，建议配合滚动容器使用
8. **样式自定义**：当同时使用 actions/panels 时，组件会自动添加 margin 和 border-radius 样式形成卡片效果；不使用这些属性时则采用全屏底部样式
9. **性能优化**：默认开启懒渲染（lazyRender），面板内容只在首次展示时渲染，关闭后不会销毁，适合需要频繁开关的场景
