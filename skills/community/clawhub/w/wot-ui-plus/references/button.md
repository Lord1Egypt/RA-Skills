# Button 按钮


## 组件概况

Button 按钮组件是用户交互中最常用的基础组件之一，用于触发特定操作或行为。该组件支持多种类型（主要、成功、信息、警告、危险、文本、图标）、三种尺寸（小、中、大），以及幽灵、圆角、细边框、块状等丰富的样式变体。同时提供加载状态、图标集成和完整的小程序开放能力支持，适用于各种业务场景下的用户交互需求。

## 核心功能描述

- **多种按钮类型**：支持 `primary`（主要）、`success`（成功）、`info`（信息）、`warning`（警告）、`error`（危险）、`text`（文字）、`icon`（图标）共 7 种类型
- **三种按钮尺寸**：支持 `small`（28px 高，12px 字号）、`medium`（35px 高，14px 字号）、`large`（42px 高，16px 字号）
- **幽灵按钮**：通过 `plain` 属性切换为透明背景、带边框的幽灵样式
- **细边框**：通过 `hairline` 属性实现 0.5px 的细边框效果，提升视觉精致度
- **圆角控制**：默认 `round` 为 `true`，显示圆角按钮；设置为 `false` 显示小圆角按钮
- **块状按钮**：通过 `block` 属性使按钮宽度占满父容器，适用于底部操作栏等场景
- **加载状态**：通过 `loading` 属性展示加载动画，加载期间按钮自动禁用点击
- **图标支持**：通过 `icon` 属性集成图标，支持自定义类名前缀 `classPrefix`
- **禁用状态**：通过 `disabled` 属性禁用按钮，禁用状态下点击事件不会触发
- **小程序开放能力**：通过 `openType` 属性支持微信小程序的多种开放能力，如获取用户信息、联系客服、获取手机号等
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **主要操作**：表单提交、确认操作等核心交互，使用 `primary` 类型按钮
- **辅助操作**：取消、返回等次要操作，使用 `info` 类型或 `plain` 幽灵按钮
- **成功/反馈操作**：操作成功后的确认按钮，使用 `success` 类型
- **警告/危险操作**：删除、清除等需要用户谨慎操作的行为，使用 `warning` 或 `error` 类型
- **文字链接式操作**：列表内的展开、查看更多等操作，使用 `text` 类型按钮
- **纯图标操作**：工具栏内的功能按钮，使用 `icon` 类型按钮
- **加载反馈**：提交表单后显示加载状态，防止重复提交，使用 `loading` 属性
- **小程序场景**：获取用户信息、联系客服、获取手机号、打开 APP 等微信小程序特有场景
- **底部固定操作**：表单底部、弹窗底部等需要宽度占满的操作区域，使用 `block` 属性

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| type | `'primary' \| 'success' \| 'info' \| 'warning' \| 'error' \| 'default' \| 'text' \| 'icon'` | `'primary'` | 否 | 按钮类型 |
| size | `'small' \| 'medium' \| 'large'` | `'medium'` | 否 | 按钮尺寸 |
| plain | boolean | false | 否 | 是否为幽灵按钮，透明背景带边框 |
| round | boolean | true | 否 | 是否为圆角按钮 |
| hairline | boolean | false | 否 | 是否显示 0.5px 细边框，仅幽灵按钮生效 |
| block | boolean | false | 否 | 是否为块状按钮，宽度 100% |
| disabled | boolean | false | 否 | 是否禁用按钮 |
| loading | boolean | false | 否 | 是否显示加载状态 |
| loadingColor | string | - | 否 | 加载图标颜色，默认根据按钮类型自动匹配 |
| icon | string | - | 否 | 图标类名 |
| classPrefix | string | `'wd-icon'` | 否 | 图标类名前缀 |
| openType | ButtonOpenType | - | 否 | 微信小程序开放能力类型，详见下方说明 |
| hoverStopPropagation | boolean | false | 否 | 是否阻止本节点的祖先节点出现点击态 |
| lang | `'zh_CN' \| 'zh_TW' \| 'en'` | - | 否 | 指定返回用户信息的语言 |
| sessionFrom | string | - | 否 | 会话来源，`open-type="contact"` 时有效 |
| sendMessageTitle | string | - | 否 | 会话内消息卡片标题，`open-type="contact"` 时有效 |
| sendMessagePath | string | - | 否 | 会话内消息卡片点击跳转路径，`open-type="contact"` 时有效 |
| sendMessageImg | string | - | 否 | 会话内消息卡片图片，`open-type="contact"` 时有效 |
| appParameter | string | - | 否 | 打开 APP 时传递的参数，`open-type="launchApp"` 时有效 |
| showMessageCard | boolean | false | 否 | 是否显示会话内消息卡片，`open-type="contact"` 时有效 |
| buttonId | string | - | 否 | 按钮唯一标识，可用于设置隐私同意授权按钮的 id |
| scope | `'phoneNumber' \| 'userInfo'` | - | 否 | 支付宝小程序授权作用域，`open-type="getAuthorize"` 时有效 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

#### openType 可选值

`ButtonOpenType` 类型支持以下微信小程序开放能力：

| 值 | 说明 |
|---|------|
| feedback | 打开小程序意见反馈面板 |
| share | 触发用户转发 |
| getUserInfo | 获取用户信息 |
| contact | 打开客服会话 |
| getPhoneNumber | 获取用户手机号 |
| launchApp | 打开 APP |
| openSetting | 打开授权设置页 |
| chooseAvatar | 选择用户头像 |
| getAuthorize | 支付宝小程序授权 |
| lifestyle | 支付宝小程序生活号授权 |
| contactShare | 分享到微信好友 |
| openGroupProfile | 展示群信息 |
| openGuildProfile | 打开群设置页 |
| openPublicProfile | 打开公众号主页 |
| shareMessageToFriend | 转发消息给好友 |
| addFriend | 添加好友 |
| addColorSign | 添加彩色签名 |
| addGroupApp | 添加到群应用 |
| addToFavorites | 加入收藏 |
| chooseAddress | 选择收货地址 |
| chooseInvoiceTitle | 选择发票抬头 |
| login | 用户登录 |
| subscribe | 订阅消息 |
| favorite | 收藏 |
| watchLater | 稍后再看 |
| openProfile | 打开个人页 |
| agreePrivacyAuthorization | 同意隐私授权 |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| click | event | 按钮点击事件，禁用和加载状态下不会触发 |
| getuserinfo | event.detail | 获取用户信息回调，`open-type="getUserInfo"` 时有效 |
| contact | event.detail | 客服消息回调，`open-type="contact"` 时有效 |
| getphonenumber | event.detail | 获取用户手机号回调，`open-type="getPhoneNumber"` 时有效 |
| getrealtimephonenumber | event.detail | 获取用户实时手机号回调 |
| error | event.detail | 使用开放能力发生错误时的回调 |
| launchapp | event.detail | 打开 APP 成功回调，`open-type="launchApp"` 时有效 |
| opensetting | event.detail | 打开授权设置页回调，`open-type="openSetting"` 时有效 |
| chooseavatar | event.detail | 选择头像回调，`open-type="chooseAvatar"` 时有效 |
| agreeprivacyauthorization | event.detail | 同意隐私授权回调 |

### Methods

组件不对外暴露任何方法。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 按钮内容，可放置文字、图标或其他组件 |

## 使用示例

### 示例 1：基本用法

展示不同类型的按钮以及圆角/方角的切换效果。

```vue
<template>
  <view>
    <!-- 默认圆角按钮 -->
    <wd-button>主要按钮</wd-button>
    <wd-button type="success">成功按钮</wd-button>
    <wd-button type="info">信息按钮</wd-button>
    <wd-button type="warning">警告按钮</wd-button>
    <wd-button type="error">危险按钮</wd-button>

    <!-- 方角按钮 -->
    <wd-button :round="false">主要按钮</wd-button>
    <wd-button :round="false" type="success">成功按钮</wd-button>
    <wd-button :round="false" type="info">信息按钮</wd-button>
    <wd-button :round="false" type="warning">警告按钮</wd-button>
    <wd-button :round="false" type="error">危险按钮</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

`round` 属性默认为 `true`，显示大圆角按钮；设置为 `false` 时显示小圆角按钮。按钮类型通过 `type` 属性控制，默认为 `primary` 主要按钮。

### 示例 2：幽灵按钮与细边框

展示幽灵按钮效果，以及叠加细边框的精致样式。

```vue
<template>
  <view>
    <!-- 幽灵按钮 -->
    <wd-button plain>主要按钮</wd-button>
    <wd-button type="success" plain>成功按钮</wd-button>
    <wd-button type="info" plain>信息按钮</wd-button>
    <wd-button type="warning" plain>警告按钮</wd-button>
    <wd-button type="error" plain>危险按钮</wd-button>

    <!-- 细边框幽灵按钮 -->
    <wd-button plain hairline>主要按钮</wd-button>
    <wd-button type="success" plain hairline>成功按钮</wd-button>
    <wd-button type="info" plain hairline>信息按钮</wd-button>
    <wd-button type="warning" plain hairline>警告按钮</wd-button>
    <wd-button type="error" plain hairline>危险按钮</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `plain` 属性将按钮切换为幽灵样式（透明背景，边框颜色与按钮类型一致）。在 `plain` 基础上添加 `hairline` 属性，可显示 0.5px 的细边框效果。

### 示例 3：禁用状态

展示不同类型按钮的禁用效果。

```vue
<template>
  <view>
    <wd-button disabled>主要按钮</wd-button>
    <wd-button type="success" disabled>成功按钮</wd-button>
    <wd-button type="info" disabled>信息按钮</wd-button>
    <wd-button type="warning" disabled>警告按钮</wd-button>
    <wd-button type="error" disabled>危险按钮</wd-button>
    <wd-button :round="false" disabled>主要按钮</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `disabled` 属性禁用按钮，禁用状态下按钮透明度降低至 0.6，且点击事件不会触发。

### 示例 4：按钮尺寸

展示三种尺寸的按钮效果。

```vue
<template>
  <view>
    <wd-button size="small">小型按钮</wd-button>
    <wd-button size="medium">普通按钮</wd-button>
    <wd-button size="large">大型按钮</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

各尺寸的规格如下：

| 尺寸 | 高度 | 内边距 | 字号 | 圆角 | Loading 图标大小 |
|------|------|--------|------|------|-----------------|
| `small` | 28px | 0 12px | 12px | 3px | 14px |
| `medium` | 35px | 0 15px | 14px | 4px | 18px |
| `large` | 42px | 0 30px | 16px | 5px | 24px |

### 示例 5：加载状态

展示按钮的加载状态效果。

```vue
<template>
  <view>
    <wd-button loading>加载中</wd-button>
    <wd-button type="success" loading>加载中</wd-button>
    <wd-button type="warning" loading>加载中</wd-button>
    <wd-button type="error" loading>加载中</wd-button>
    <wd-button type="info" plain loading>加载中</wd-button>
    <wd-button :round="false" loading>加载中</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `loading` 属性展示加载动画，加载期间按钮自动禁用点击交互。加载图标颜色会根据按钮类型自动匹配（未设置 `loadingColor` 时）：`primary` 为 `#4D80F0`，`success` 为 `#34d19d`，`info`/`default` 为 `#333`，`warning` 为 `#f0883a`，`error` 为 `#fa4350`。

### 示例 6：文字按钮与图标按钮

展示文字按钮和纯图标按钮的使用方式。

```vue
<template>
  <view>
    <!-- 文字按钮 -->
    <wd-button type="text">按钮</wd-button>
    <wd-button type="text" disabled>按钮</wd-button>

    <!-- 图标按钮 -->
    <wd-button type="icon" plain icon="delete"></wd-button>
    <wd-button type="icon" icon="delete"></wd-button>
    <wd-button :round="false" type="icon" plain icon="add" disabled></wd-button>
    <wd-button type="icon" icon="add" disabled></wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

`type="text"` 创建文字按钮样式（无背景、无边框，hover 时透明度变为 0.7）。`type="icon"` 创建纯图标按钮，默认尺寸为 40px，支持 `plain` 属性添加边框背景。

### 示例 7：带图标的按钮

在按钮中集成图标，增强视觉识别性。

```vue
<template>
  <view>
    <wd-button icon="download" size="small">下载</wd-button>
    <wd-button icon="download">下载</wd-button>
    <wd-button icon="download" size="large">下载</wd-button>
    <wd-button icon="setting" size="small">设置</wd-button>
    <wd-button icon="setting">设置</wd-button>
    <wd-button icon="setting" size="large">设置</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `icon` 属性设置图标类名，图标默认显示在按钮文字左侧，间距为 6px，图标大小为 18px。使用 `classPrefix` 属性可自定义图标类名前缀，默认为 `wd-icon`。

### 示例 8：块状按钮

展示宽度占满父容器的块状按钮。

```vue
<template>
  <view>
    <wd-button block size="large">主要按钮</wd-button>
    <wd-button type="success" block size="large">成功按钮</wd-button>
    <wd-button type="info" block size="large">信息按钮</wd-button>
    <wd-button type="warning" block size="large">警告按钮</wd-button>
    <wd-button type="error" block size="large">危险按钮</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `block` 属性使按钮以块级元素渲染，宽度占满 100% 父容器，适用于表单底部操作栏、弹窗底部按钮等场景。

### 示例 9：常用组合

展示表单提交场景中常见的主次操作按钮组合。

```vue
<template>
  <view>
    <!-- 禁用状态 -->
    <wd-button disabled>主操作</wd-button>
    <wd-button size="small" disabled>主操作</wd-button>

    <!-- 正常状态 -->
    <wd-button>主操作</wd-button>
    <wd-button size="small">主操作</wd-button>

    <!-- 次要操作 -->
    <wd-button type="info" disabled>次操作</wd-button>
    <wd-button type="info" size="small" disabled>次操作</wd-button>
    <wd-button type="info">次操作</wd-button>
    <wd-button type="info" size="small">次操作</wd-button>

    <!-- 幽灵按钮 -->
    <wd-button plain disabled>幽灵按钮</wd-button>
    <wd-button size="small" plain disabled>幽灵按钮</wd-button>
    <wd-button plain>幽灵按钮</wd-button>
    <wd-button size="small" plain>幽灵按钮</wd-button>

    <!-- 次要幽灵按钮 -->
    <wd-button type="info" plain disabled>次操作</wd-button>
    <wd-button type="info" size="small" plain disabled>次操作</wd-button>
    <wd-button type="info" plain>次操作</wd-button>
    <wd-button type="info" size="small" plain>次操作</wd-button>
  </view>
</template>
<script lang="ts" setup>
</script>
```

在表单提交等场景中，通常主操作用 `primary` 默认类型（蓝色填充），次操作用 `info` 类型或 `plain` 幽灵按钮，形成视觉层级区分。

### 示例 10：小程序开放能力

展示微信小程序常见开放能力的用法。

```vue
<template>
  <view>
    <!-- 获取用户信息 -->
    <wd-button open-type="getUserInfo" @getuserinfo="handleGetuserinfo">
      获取用户信息
    </wd-button>

    <!-- 获取手机号 -->
    <wd-button open-type="getPhoneNumber" @getphonenumber="handleGetPhone">
      获取手机号
    </wd-button>

    <!-- 打开客服 -->
    <wd-button
      open-type="contact"
      session-from="weapp"
      send-message-title="欢迎咨询"
      send-message-path="/pages/index/index"
      send-message-img="/static/logo.png"
      :show-message-card="true"
      @contact="handleContact"
    >
      联系客服
    </wd-button>

    <!-- 打开 APP -->
    <wd-button open-type="launchApp" app-parameter="wechat" @launchapp="handleLaunchApp">
      打开 APP
    </wd-button>

    <!-- 打开授权设置 -->
    <wd-button open-type="openSetting" @opensetting="handleOpenSetting">
      授权设置
    </wd-button>

    <!-- 选择头像 -->
    <wd-button open-type="chooseAvatar" @chooseavatar="handleChooseAvatar">
      选择头像
    </wd-button>
  </view>
</template>
<script lang="ts" setup>
  function handleGetuserinfo(event: any) {
    console.log('用户信息', event)
  }

  function handleGetPhone(event: any) {
    console.log('手机号', event)
  }

  function handleContact(event: any) {
    console.log('客服消息', event)
  }

  function handleLaunchApp(event: any) {
    console.log('打开APP', event)
  }

  function handleOpenSetting(event: any) {
    console.log('授权设置', event)
  }

  function handleChooseAvatar(event: any) {
    console.log('选择头像', event)
  }
</script>
```

使用 `openType` 属性触发微信小程序的开放能力，对应的事件通过 `@事件名` 监听。注意：当按钮处于 `disabled` 或 `loading` 状态时，`openType` 不会生效。

## 注意事项

1. **禁用与加载状态自动阻止交互**：当 `disabled` 或 `loading` 为 `true` 时，按钮的点击事件不会触发，同时 `openType` 开放能力也不会生效
2. **hairline 仅对幽灵按钮生效**：`hairline` 属性需要配合 `plain` 属性使用，非幽灵按钮状态下设置 `hairline` 不会产生细边框效果
3. **加载图标颜色自动匹配**：未设置 `loadingColor` 时，加载图标颜色会根据 `type` 自动匹配对应主题色；幽灵按钮的加载图标颜色会与实心按钮相反（使用白色）
4. **icon 类型按钮尺寸固定**：`type="icon"` 的按钮默认尺寸为 40px，内边距为 0，且默认不显示边框伪元素
5. **text 类型按钮无背景**：`type="text"` 的按钮默认无背景、无边框，hover/active 时通过透明度变化提供视觉反馈，而非背景色变化
6. **圆角模式下的特殊处理**：当 `round` 为 `true` 且 `type` 为 `icon` 时，按钮会呈现圆形效果；`type` 为 `text` 时，圆角设置为 0
7. **openType 在禁用时不生效**：当按钮 `disabled` 或 `loading` 为 `true` 时，`openType` 属性会被设置为 `undefined`，不会触发任何小程序开放能力
8. **customStyle 与 customClass 的使用**：通过 `customStyle` 和 `customClass` 可以进行自定义样式扩展，例如添加 Material Design 风格的 box-shadow 阴影效果
9. **暗色模式自动适配**：组件已内置暗色主题样式，包括 `info`、`text`、`icon` 等类型在暗色模式下的背景和颜色都会自动调整，无需额外配置
