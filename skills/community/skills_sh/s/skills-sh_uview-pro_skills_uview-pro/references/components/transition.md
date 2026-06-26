---
name: "transition"
description: "统一的过渡与进出场动效封装，支持多种预设动画和自定义时长。基于CSS动画实现，性能优异。. Invoke when user needs to use transition component."
url: "https://uviewpro.cn/zh/components/transition.html"
triggers: ["transition"]
---

# Transition 过渡动画 <BadgeVersion text="0.5.2" /> <to-api/>

<demo-model url="/pages/componentsB/transition/index"></demo-model>

统一的过渡与进出场动效封装，支持多种预设动画和自定义时长。基于CSS动画实现，性能优异。

::: tip 说明

- 组件内部使用CSS动画实现，性能优异
- 支持H5、APP 和所有主流小程序平台
- 可以通过自定义样式覆盖默认动画效果
- 动画事件回调函数会接收到当前动画的DOM元素作为参数

:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`show`属性控制内容的显示和隐藏，默认使用`fade`动画效果

```html
<u-transition :show="visible">
    <view>这是需要动画的内容</view>
</u-transition>
```

## 设置动画类型

通过`name`属性设置不同的动画效果，支持`fade`、`slide-up`、`slide-down`、`slide-left`、`slide-right`、`zoom-in`、`zoom-out`

```html
<u-transition :show="visible" name="slide-up">
    <view>从下方滑入</view>
</u-transition>

<u-transition :show="visible" name="slide-down">
    <view>从上方滑入</view>
</u-transition>

<u-transition :show="visible" name="slide-left">
    <view>从左侧滑入</view>
</u-transition>

<u-transition :show="visible" name="slide-right">
    <view>从右侧滑入</view>
</u-transition>

<u-transition :show="visible" name="zoom-in">
    <view>放大进入</view>
</u-transition>

<u-transition :show="visible" name="zoom-out">
    <view>缩小进入</view>
</u-transition>
```

## 自定义动画时长

通过`duration`属性设置动画时长，单位为毫秒。支持设置不同的进入和离开时长

```html
<!-- 统一设置进入和离开时长 -->
<u-transition :show="visible" :duration="500">
    <view>动画时长500ms</view>
</u-transition>

<!-- 分别设置进入和离开时长 -->
<u-transition :show="visible" :duration="{ enter: 300, leave: 500 }">
    <view>进入300ms，离开500ms</view>
</u-transition>
```

## 设置动画曲线

通过`timing-function`属性设置动画曲线，支持CSS动画曲线值

```html
<u-transition :show="visible" timing-function="ease-in-out">
    <view>使用ease-in-out曲线</view>
</u-transition>

<u-transition :show="visible" timing-function="linear">
    <view>使用linear曲线</view>
</u-transition>
```

## 设置动画延迟

通过`delay`属性设置动画延迟开始的时间，单位为毫秒

```html
<u-transition :show="visible" :delay="200">
    <view>延迟200ms后开始动画</view>
</u-transition>
```

## 首次渲染时执行动画

通过`appear`属性控制组件首次渲染时是否执行进入动画

```html
<u-transition :show="visible" :appear="true">
    <view>首次渲染时会执行进入动画</view>
</u-transition>
```

## 设置过渡模式

通过`mode`属性控制动画的执行顺序，类似于Vue原生的transition组件

- `out-in`: 离开动画完成后开始进入动画
- `in-out`: 进入动画完成后开始离开动画

```html
<u-transition :show="visible" mode="out-in">
    <view>离开动画完成后才开始进入动画</view>
</u-transition>
```

## 监听动画事件

组件提供了完整的动画生命周期事件，可以监听各种动画状态

```html
<u-transition
    :show="visible"
    @before-enter="onBeforeEnter"
    @enter="onEnter"
    @after-enter="onAfterEnter"
    @before-leave="onBeforeLeave"
    @leave="onLeave"
    @after-leave="onAfterLeave"
>
    <view>监听动画事件</view>
</u-transition>
```

## API

### Props

| 参数          | 说明            | 类型            |        默认值        | 可选值   |
|-------------  |---------------- |---------------- |---------------------- |-------- |
| show | 是否展示内容 | Boolean | true | false |
| name | 预设动画名 | String | fade | fade / slide-up / slide-down / slide-left / slide-right / zoom-in / zoom-out |
| mode | 进入/离开过渡模式，等同于原生 transition 的 mode | String | '' | out-in / in-out / '' |
| duration | 进入/离开动画时长，单位ms，支持 { enter, leave } | Number \| Object | 300 | - |
| timing-function | 动画曲线 | String | cubic-bezier(0.2,0.8,0.2,1) | - |
| delay | 动画延迟，单位ms | Number | 0 | - |
| appear | 首次渲染时是否执行动画 | Boolean | false | true |
| custom-class | 自定义 class | String | - | - |
| custom-style | 自定义样式 | String \| Object | - | - |

### Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| before-enter | 进入动画开始前触发 | element | - |
| enter | 进入动画开始时触发 | element | - |
| after-enter | 进入动画结束后触发 | element | - |
| enter-cancelled | 进入动画被取消时触发 | element | - |
| before-leave | 离开动画开始前触发 | element | - |
| leave | 离开动画开始时触发 | element | - |
| after-leave | 离开动画结束后触发 | element | - |
| leave-cancelled | 离开动画被取消时触发 | element | - |

### Slots

|名称|说明|
|:-|:-|
| default | 需要执行过渡动画的内容 |
