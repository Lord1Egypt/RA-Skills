---
name: "checkbox"
description: "复选框组件一般用于需要多个选择的场景，该组件功能完整，使用方便. Invoke when user needs to use checkbox component."
url: "https://uviewpro.cn/zh/components/checkbox.html"
triggers: ["checkbox","复选框"]
---

# Checkbox 复选框 <to-api/>

<demo-model url="/pages/componentsB/checkbox/index"></demo-model>


复选框组件一般用于需要多个选择的场景，该组件功能完整，使用方便

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

:::tip
- 0.5.2 版本开始，`checkbox-group` 组件支持 `v-model` 双向绑定，`checkbox` 组件新增 `value` 参数，`value`如不设置，默认值取`name`属性, 详情见下方 API 说明。
- 本次升级完全兼容之前用法，但推荐使用 `checkbox-group` 的 `v-model` 进行双向绑定，更加简洁方便。
:::

## 基本使用

- 该组件无需强制搭配`checkboxGroup`组件使用(视情况而定)，可以单个独立使用`u-checkbox`组件

```html
<template>
	<view>
		<u-checkbox-group v-model="checkboxValues" @change="checkboxGroupChange">
			<u-checkbox 
				v-for="(item, index) in list" :key="index"
				:label="item.label" :value="item.value"
				@change="checkboxChange" 
			></u-checkbox>
		</u-checkbox-group>
		<u-button @click="checkedAll">全选</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface CheckboxItem {
  label: string
  value: string
  checked: boolean
  disabled: boolean
}

const checkboxValues = ref(['apple']);

const list = reactive<CheckboxItem[]>([
  {
    label: 'apple',
    value: 'apple',
    checked: false,
    disabled: false
  },
  {
    label: 'banner',
    value: 'banner',
    checked: false,
    disabled: false
  },
  {
    label: 'orange',
    value: 'orange',
    checked: false,
    disabled: false
  }
])

// 选中某个复选框时，由checkbox时触发
const checkboxChange = (e: any) => {
  //console.log(e);
}

// 选中任一checkbox时，由checkbox-group触发
const checkboxGroupChange = (e: any) => {
  // console.log(e);
}

// 全选
const checkedAll = () => {
  checkboxValues.value = list.map(item => item.value)
}
</script>
```

## 禁用checkbox

设置`disabled`为`true`，即可禁用某个组件，让用户无法点击，禁用分为两种状态，一是未勾选前禁用，这时只显示一个灰色的区域。二是已勾选后
再禁用，会有灰色的已勾选的图标，但此时依然是不可操作的。

```html
<u-checkbox v-model="checked" :disabled="false" label="天涯" />
```

## 自定义形状

可以通过设置`shape`为`square`或者`circle`，将复选框设置为方形或者圆形


```html
<u-checkbox v-model="checked" shape="circle" label="明月" />
```


## 自定义颜色

此处所指的颜色，为`checkbox`选中时的背景颜色，参数为`active-color`


```html
<u-checkbox v-model="checked" active-color="red" label="光影" />
```


## 文本是否可点击

设置`label-disabled`为`false`，点击文本时，无法操作`checkbox`

```html
<u-checkbox v-model="checked" :label-disabled="false" label="剑舞" />
```

## API

## Checkbox Props

注意：需要给`checkbox`组件通过`v-model`绑定一个**布尔值**，来初始化`checkbox`的状态，随后该值被双向绑定，
当用户勾选复选框时，该值在`checkbox`内部被修改为`true`，并反映到父组件，否则为`false`，换言之，您无需监听`checkbox`的`change`事件，也能
知道某一个`checkbox`是否被选中的状态

注意：`checkbox`和`checkbox-group`二者同名参数中，`checkbox`的参数优先级更高。

| 参数          | 说明            | 类型            | 默认值             |  可选值   | 版本 |
|-------------  |---------------- |---------------|------------------ |-------- | - |
| v-model | 双向绑定某一个`checkbox`的值，如果将该变量设置为`true`，将会被选中 | String \ Number | - | - |
| size | 组件整体的大小，单位rpx  | String \ Number | - | - | - |
| label-size | label字体大小，单位rpx  | String \ Number | - | - | - |
| icon-size | 图标大小，单位rpx  | String \ Number | - | - | - |
| label | `checkbox`组件的文本显示名称  | String \ Number | - | - | - |
| value | `checkbox`组件的标示符 | String \ Number | - | - | <BadgeVersion text="0.5.2" align="middle" /> |
| name | 同 `value`，即将废弃 | String \ Number | - | - | - |
| shape | 形状，见上方说明 | String  | - | square | - |
| disabled | 是否禁用 | Boolean  | - | false / true | - |
| label-disabled | 是否禁止点击文本操作`checkbox` | Boolean  | - | false / true | - |
| active-color | 选中时的颜色，如设置`CheckboxGroup`的`active-color`将失效 | String  | - | - | - |

## CheckboxGroup Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   | 版本 |
|-------------  |---------------- |---------------|------------------ |-------- | - |
| v-model | 双向绑定某一个`checkbox`的值，如果将该变量设置为`true`，将会被选中 | Array | - | - | <BadgeVersion text="0.5.2" align="middle" /> |
| max | 最多能选中多少个`checkbox`  | String \ Number | 999 | - | - |
| disabled | 是否禁用所有`checkbox`  | Boolean | false | true | - |
| icon-size | 图标大小，单位rpx  | String \ Number | 20 | - | - |
| size | 组件整体的大小，单位rpx  | String \ Number | 34 | - | - |
| shape | 形状，见上方说明 | String  | circle | square | - |
| active-color | 选中时的颜色，应用到所有子`Checkbox`组件 | String  | #2979ff | - | - |
| label-disabled | 是否禁止点击文本操作`checkbox` | Boolean  | false | true | - |
| width | `checkbox`的宽度，需带单位，如`50%`，`150rpx` | String  | auto | - | - |
| wrap | 是否每个`checkbox`占一行 | Boolean  | false | true | - |

## Checkbox Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 某个`checkbox`状态发生变化时触发，回调为boolean类型数值 | boolean(当前`checkbox`的选中状态) | `v0.5.2`由object改为boolean |

## CheckboxGroup Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 任一个`checkbox`状态发生变化时触发，回调为一个对象 | detail = array( [元素为被选中的`checkbox`的`value`] ) | - |

## Checkbox Slots
| 名称 | 说明 | 版本 |
|:-|:-|:-|
| default | 默认插槽，用于放置`checkbox`的文本 | - |