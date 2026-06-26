# Avatar 头像


## 组件概况

Avatar 头像组件用于展示用户头像、图标或文字标识，支持图片、图标、文字三种内容类型，并提供圆形和方形两种形状选择。该组件内置了性别角标、VIP 等级标识、小程序开放能力等扩展功能，同时还提供了 AvatarGroup 头像组组件，用于展示一组头像的层叠排列效果。在移动端应用中，头像组件常用于用户信息展示、群组成员列表、评论者标识等场景，是用户界面中最基础且高频使用的组件之一。

## 核心功能描述

- **多内容类型**：支持图片头像（`src`）、图标头像（`icon`）、文字头像（`text`）三种展示方式，优先级依次递减
- **形状切换**：支持圆形（`circle`）和方形（`square`）两种形状，方形采用 10% 圆角设计
- **尺寸灵活**：支持数字或字符串类型的 `size` 属性，可自由控制头像尺寸，默认值为 40
- **性别角标**：通过 `sexIcon` 属性在右上角显示性别标识（`male` 男性 / `female` 女性），支持自定义背景色
- **等级标识**：通过 `showLevel` 属性在右下角显示 VIP 等级图标，支持自定义背景色
- **随机背景色**：文字头像支持 `randomBgColor` 自动分配 20 种预设背景色之一，也可通过 `colorIndex` 指定具体颜色索引（0-19）
- **图片加载容错**：图片加载失败时自动显示内置的 base64 占位图或用户自定义的 `defaultUrl` 默认头像
- **小程序开放能力**：支持微信、QQ、百度小程序的 `open-data` 标签，直接展示用户头像
- **头像组层叠展示**：AvatarGroup 组件支持头像数组的层叠排列，通过 `gap` 属性控制重叠比例（0-1）
- **查看更多提示**：AvatarGroup 支持超出最大显示数量时展示 "+N" 的更多提示，点击触发 `showMore` 事件
- **对象数据适配**：AvatarGroup 支持字符串数组或对象数组，通过 `keyName` 指定对象中的图片路径属性
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **用户资料展示**：在个人中心、用户主页展示用户头像，支持性别、等级等附加信息
- **群组成员列表**：在群聊信息页展示群成员头像组，使用层叠效果节省空间
- **评论/动态列表**：在信息流中展示发布者头像，配合文字头像实现无图片用户的占位展示
- **分享/协作成员**：在文档协作、任务分配等场景展示参与成员的头像组
- **小程序用户信息**：在微信/QQ/百度小程序中直接获取并展示用户微信头像

## API

### wd-avatar Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| src | string | '' | 否 | 头像图片路径，不能为相对路径 |
| shape | string | 'circle' | 否 | 头像形状，可选值：`circle` 圆形、`square` 方形 |
| size | string \| number | 40 | 否 | 头像尺寸，支持数字或带单位的字符串（如 '50px'） |
| mode | string | 'scaleToFill' | 否 | 图片裁剪模式，可选值：`scaleToFill`、`aspectFit`、`aspectFill`、`widthFix`、`heightFix`、`top`、`bottom`、`center`、`left`、`right`、`top left`、`top right`、`bottom left`、`bottom right` |
| text | string | '' | 否 | 文字头像显示的文字内容 |
| bgColor | string | '#c0c4cc' | 否 | 文字/图标头像的背景颜色 |
| color | string | '#ffffff' | 否 | 文字/图标的颜色 |
| fontSize | string \| number | 18 | 否 | 文字/图标的大小 |
| icon | string | '' | 否 | 图标头像显示的图标名称 |
| mpAvatar | boolean | false | 否 | 是否显示小程序头像（使用 open-data），仅对微信、QQ、百度小程序有效 |
| randomBgColor | boolean | false | 否 | 是否使用随机背景色（仅文字/图标头像生效） |
| colorIndex | number | undefined | 否 | 当 randomBgColor 为 true 时，指定背景色数组中的索引，取值范围 0-19 |
| defaultUrl | string | '' | 否 | 图片加载失败时显示的默认头像路径（组件有内置默认图片） |
| sexIcon | string | '' | 否 | 右上角性别角标，可选值：`male` 男性、`female` 女性 |
| sexBgColor | string | '' | 否 | 性别角标的背景颜色 |
| showLevel | boolean | false | 否 | 是否显示右下角 VIP 等级图标 |
| levelBgColor | string | '' | 否 | 等级图标的背景颜色 |
| name | string | '' | 否 | 组件标识符，点击事件中作为参数返回 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### wd-avatar Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| click | 点击头像时触发 | `(name: string, event: any)` | `name` 为传入的组件标识符，`event` 为原生点击事件对象 |

### wd-avatar Methods

组件本身不对外暴露方法。

### wd-avatar Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义头像内容，当传入默认插槽内容时将替代内部的图片/图标/文字渲染逻辑 |

---

### wd-avatar-group Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| urls | array | [] | 否 | 头像图片组，支持字符串数组或对象数组 |
| maxCount | string \| number | 5 | 否 | 最多展示的头像数量 |
| shape | string | 'circle' | 否 | 头像形状，可选值：`circle` 圆形、`square` 方形 |
| mode | string | 'scaleToFill' | 否 | 图片裁剪模式，可选值同 wd-avatar |
| showMore | boolean | true | 否 | 超出 maxCount 时是否显示查看更多的提示 |
| size | string \| number | 40 | 否 | 头像大小，支持数字或带单位的字符串 |
| keyName | string | '' | 否 | 指定从数组的对象元素中读取哪个属性作为图片地址，如传入 'avatar' 则读取 item.avatar |
| gap | string \| number | 0.5 | 否 | 头像之间的重叠比例，取值范围 0-1，值越大重叠越多 |
| extraValue | string \| number | 0 | 否 | 需额外显示的数值，用于自定义 "+N" 中的 N 值 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### wd-avatar-group Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| showMore | 点击更多提示区域时触发 | - | 无参数 |

### wd-avatar-group Methods

组件本身不对外暴露方法。

### wd-avatar-group Slots

组件不提供插槽。

## 使用示例

### 示例 1：基础图片头像

展示最基本的图片头像用法，支持性别角标和等级标识。

```vue
<template>
  <view class="avatar-row">
    <wd-avatar :src="maleAvatar" sexIcon="male" size="50"></wd-avatar>
    <wd-avatar :src="femaleAvatar" sexIcon="female" size="50" showLevel></wd-avatar>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const maleAvatar = ref('http://106.55.153.212:88/a1.png')
  const femaleAvatar = ref('http://106.55.153.212:88/a2.png')
</script>

<style lang="scss" scoped>
  .avatar-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;
  }
</style>
```

该示例展示了两个基础图片头像，左侧头像带有男性性别角标（蓝色），右侧头像带有女性性别角标（红色）和 VIP 等级标识（橙色）。性别角标位于右上角，等级标识位于右下角。

### 示例 2：图标与文字头像

展示图标头像和文字头像的用法，文字头像支持自动随机背景色。

```vue
<template>
  <view class="avatar-row">
    <!-- 图标头像 -->
    <wd-avatar icon="logo-wechat" fontSize="22" shape="circle"></wd-avatar>
    <wd-avatar icon="logo-douyin-o" fontSize="22" shape="square"></wd-avatar>

    <!-- 文字头像（固定背景色） -->
    <wd-avatar text="A" fontSize="20" bgColor="#409eff"></wd-avatar>

    <!-- 文字头像（随机背景色） -->
    <wd-avatar text="张" fontSize="18" randomBgColor :colorIndex="0"></wd-avatar>
    <wd-avatar text="李" fontSize="18" randomBgColor></wd-avatar>
  </view>
</template>

<script lang="ts" setup>
  // 无需额外逻辑
</script>

<style lang="scss" scoped>
  .avatar-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
  }
</style>
```

该示例展示了四种头像类型：圆形图标头像、方形图标头像、固定背景色的文字头像以及随机背景色的文字头像。当 `randomBgColor` 为 true 且未指定 `colorIndex` 时，系统会从 20 种预设颜色中随机选取一种作为背景色。

### 示例 3：图片加载失败处理

展示图片加载失败时自动显示默认头像的容错机制。

```vue
<template>
  <view>
    <!-- 使用无效图片路径，将自动显示内置占位图 -->
    <wd-avatar :src="invalidUrl" size="60"></wd-avatar>

    <!-- 使用自定义默认头像 -->
    <wd-avatar :src="invalidUrl" defaultUrl="https://img12.360buyimg.com/imagetools/jfs/t1/122016/33/6657/1362/5f0692a1E8708d245/e47299e5945a6956.png" size="60"></wd-avatar>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const invalidUrl = ref('http://106.55.153.212:88/noExist.png')
</script>
```

当传入的 `src` 图片加载失败时，组件会自动触发 error 事件，显示内置的 base64 占位图。如果同时传入了 `defaultUrl` 属性，则优先显示用户自定义的默认头像。

### 示例 4：点击事件与组件标识

展示如何通过 `name` 属性标识组件，并在点击事件中获取标识信息。

```vue
<template>
  <view class="avatar-row">
    <wd-avatar :src="avatar1" name="user_001" @click="handleAvatarClick"></wd-avatar>
    <wd-avatar :src="avatar2" name="user_002" @click="handleAvatarClick"></wd-avatar>
    <wd-avatar :src="avatar3" name="user_003" @click="handleAvatarClick"></wd-avatar>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const avatar1 = ref('http://106.55.153.212:88/a1.png')
  const avatar2 = ref('http://106.55.153.212:88/a2.png')
  const avatar3 = ref('http://106.55.153.212:88/a3.png')

  function handleAvatarClick(name: string, event: any) {
    console.log('点击头像:', name)
    // 可根据 name 判断是哪个头像被点击，执行相应逻辑
  }
</script>

<style lang="scss" scoped>
  .avatar-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;
  }
</style>
```

通过 `name` 属性为每个头像设置唯一标识符，点击时会在回调函数的第一个参数中返回该标识符，方便在列表中区分不同头像的点击事件。

### 示例 5：头像组基础用法

展示 AvatarGroup 头像组的基础用法，支持字符串数组。

```vue
<template>
  <view>
    <wd-avatar-group :urls="avatarList" size="40" gap="0.4"></wd-avatar-group>

    <view style="margin-top: 20px">
      <wd-avatar-group :urls="avatarList" size="40" gap="0.6"></wd-avatar-group>
    </view>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const avatarList = ref([
    'http://106.55.153.212:88/a1.png',
    'http://106.55.153.212:88/a2.png',
    'http://106.55.153.212:88/a3.png',
    'http://106.55.153.212:88/a4.png',
    'http://106.55.153.212:88/a5.png',
    'http://106.55.153.212:88/a6.png',
    'http://106.55.153.212:88/a7.png'
  ])
</script>
```

该示例展示了两个头像组，第一个重叠比例为 0.4，第二个为 0.6。`gap` 值越大，头像之间的重叠程度越高。默认最多显示 5 个头像，超出部分会以 "+N" 的形式展示。

### 示例 6：头像组高级配置

展示 AvatarGroup 的对象数组支持、最大数量限制、查看更多功能及 `extraValue` 自定义显示。

```vue
<template>
  <view>
    <!-- 对象数组，通过 keyName 指定图片字段 -->
    <wd-avatar-group
      :urls="userList"
      keyName="avatarUrl"
      size="35"
      maxCount="3"
      gap="0.5"
      :extraValue="extraCount"
      @showMore="handleShowMore"
    ></wd-avatar-group>

    <!-- 关闭查看更多提示 -->
    <view style="margin-top: 20px">
      <wd-avatar-group :urls="avatarList" size="35" maxCount="4" :showMore="false"></wd-avatar-group>
    </view>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const userList = ref([
    { avatarUrl: 'http://106.55.153.212:88/a1.png', name: '用户1' },
    { avatarUrl: 'http://106.55.153.212:88/a2.png', name: '用户2' },
    { avatarUrl: 'http://106.55.153.212:88/a3.png', name: '用户3' },
    { avatarUrl: 'http://106.55.153.212:88/a4.png', name: '用户4' },
    { avatarUrl: 'http://106.55.153.212:88/a5.png', name: '用户5' }
  ])

  const avatarList = ref([
    'http://106.55.153.212:88/a1.png',
    'http://106.55.153.212:88/a2.png',
    'http://106.55.153.212:88/a3.png',
    'http://106.55.153.212:88/a4.png'
  ])

  const extraCount = ref(10)

  function handleShowMore() {
    console.log('点击了查看更多')
    // 可在此处打开弹窗或跳转页面展示完整列表
  }
</script>
```

该示例展示了 AvatarGroup 的高级用法：第一个头像组使用对象数组并通过 `keyName` 指定 `avatarUrl` 字段作为图片源，限制最多显示 3 个，超出部分使用 `extraValue` 自定义显示 "+10"；第二个头像组通过 `showMore` 为 false 关闭了查看更多提示。

## 注意事项

1. **图片路径限制**：`src` 和 `defaultUrl` 不能使用相对路径，需使用完整的网络 URL 或绝对路径
2. **内容渲染优先级**：当同时传入 `src`、`icon`、`text` 时，组件按 图片 > 图标 > 文字 的优先级进行渲染，只会显示最高优先级的内容
3. **randomBgColor 生效条件**：随机背景色仅在未传入 `src` 的情况下生效，即只对图标头像和文字头像有效
4. **colorIndex 取值范围**：`colorIndex` 的合法取值为 0-19，超出范围的颜色索引无效，组件内置 20 种预设背景色
5. **mpAvatar 平台限制**：`mpAvatar` 属性仅在微信小程序、QQ 小程序、百度小程序中有效，其他平台会渲染为空
6. **gap 取值范围**：AvatarGroup 的 `gap` 属性取值范围为 0-1，0 表示不重叠，1 表示完全重叠，超出范围的值可能导致显示异常
7. **showMore 显示逻辑**："+N" 提示仅在 `showMore` 为 true 且 `urls.length > maxCount` 或 `extraValue > 0` 时显示
8. **对象数组字段回退**：当 `urls` 为对象数组且 `keyName` 指定的属性不存在时，组件会尝试读取 `item.url` 作为回退方案
9. **尺寸单位**：`size` 和 `fontSize` 支持纯数字（默认单位为 px）或带单位的字符串（如 '50px'、'2rem'）
10. **暗色模式适配**：组件在暗色模式下会自动调整背景色和文字颜色，无需手动配置
