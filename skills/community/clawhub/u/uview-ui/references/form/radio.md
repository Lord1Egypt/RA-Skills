---
name: "radio"
description: "Radio 单选框 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Radio 单选框 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/radio.html"
---

---

## [#](#radio-单选框) Radio 单选框 [![](https://www.uviewui.com/common/to_api.png)](#api)

单选框用于有一个选择，用户只能选择其中一个的场景。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   该组件需要搭配`radioGroup`组件使用，以便用户进行操作时，获得当前单选框组的选中情况
-   通过`v-model`给`radioGroup`组件绑定一个变量，对应的`name`将会被选中

```
<template>
  <u-radio-group
    v-model="radiovalue1"
    placement="column"
    @change="groupChange"
  >
    <u-radio
      :customStyle="{marginBottom: '8px'}"
      v-for="(item, index) in radiolist1"
      :key="index"
      :label="item.name"
      :name="item.name"
      @change="radioChange"
    >
    </u-radio>
  </u-radio-group>
</template>

<script>
export default {
	data() {
		return {

          radiolist1: [{
            name: '苹果',
            disabled: false
          },
            {
              name: '香蕉',
              disabled: false
            },
            {
              name: '橙子',
              disabled: false
            }, {
              name: '榴莲',
              disabled: false
            }
          ],

          radiovalue1: '苹果',
		};
	},
	methods: {
      groupChange(n) {
        console.log('groupChange', n);
      },
      radioChange(n) {
        console.log('radioChange', n);
      }
	}
};
</script>
```

### [#](#自定义形状) 自定义形状

可以通过设置`shape`为`square`或者`circle`，将单选框设置为方形或者圆形

```
<u-radio-group v-model="value">
	<u-radio shape="circle" label="月明人倚楼"></u-radio>
</u-radio-group>
```

### [#](#禁用radio) 禁用radio

设置`disabled`为`true`，即可禁用某个组件，让用户无法点击

```
<u-radio-group v-model="value">
	<u-radio :disabled="true" label="明月几时有"></u-radio>
</u-radio-group>
```

### [#](#是否禁止点击提示语选中复选框) 是否禁止点击提示语选中复选框

设置`labelDisabled`为`true`，即可禁止点击提示语选中复选框

```
<u-radio-group v-model="value">
	<u-radio :labelDisabled="true" label="明月几时有"></u-radio>
</u-radio-group>
```

### [#](#自定义颜色) 自定义颜色

此处所指的颜色，为`radio`选中时的背景颜色，参数为`activeColor`

```
<u-radio-group v-model="value">
	<u-radio activeColor="red" label="思悠悠，恨悠悠，恨到归时方始休"></u-radio>
</u-radio-group>
```

### [#](#横向排列形式) 横向排列形式

可以通过设置`placement`为`row`或者`column`，将复选框设置为横向排列或者竖向排列

```
<u-radio-group
    v-model="value"
    placement="row">
	<u-radio activeColor="red" label="思悠悠，恨悠悠，恨到归时方始休"></u-radio>
</u-radio-group>
```

### [#](#横向两端排列形式) 横向两端排列形式

可以通过设置`iconPlacement`为`left`或者`right`，将复选框勾选图标的对齐设置为左对齐或者右对齐

```
<u-radio-group
    v-model="value"
    iconPlacement="right">
	<u-radio activeColor="red" label="思悠悠，恨悠悠，恨到归时方始休"></u-radio>
</u-radio-group>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/radio/radio.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/radio/radio.nvue)

### [#](#api) API

### [#](#radio-props) Radio Props

注意：`radio`和`radio-group`二者同名参数中，`radio`的参数优先级更高。

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| name | checkbox的名称 | String \\ Number | \- | \- |
| shape | 形状，square为方形，circle为圆型 | String | square | circle |
| disabled | 是否禁用 | Boolean | \- | \- |
| labelDisabled | 是否禁止点击提示语选中复选框 | String \\ Boolean | \- | \- |
| activeColor | 选中状态下的颜色，如设置此值，将会覆盖parent的activeColor值 | String | \- | \- |
| inactiveColor | 未选中的颜色 | String | \- | \- |
| iconSize | 图标的大小，单位px | String \\ Number | \- | \- |
| labelSize | label的字体大小，px单位 | String \\ Number | \- | \- |
| label | label提示文字，因为nvue下，直接slot进来的文字，由于特殊的结构，无法修改样式 | String \\ Number | \- | \- |
| size | 整体的大小 | String \\ Number | \- | \- |
| iconColor | 图标颜色 | String | \- | \- |
| labelColor | label的颜色 | String | \- | \- |

### [#](#radiogroup-props) radioGroup Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| value | 绑定的值 | String\\Number\\Boolean | \[\] | \- |
| disabled | 是否禁用全部checkbox | Boolean | false | true |
| shape | 形状，circle-圆形，square-方形 | String | circle | square |
| activeColor | 选中状态下的颜色，如子`Checkbox`组件设置此值，将会覆盖本值 | String | #2979ff | \- |
| inactiveColor | 未选中的颜色 | String | #c8c9cc | \- |
| name | 标识符 | String | \- | \- |
| size | 整个组件的尺寸，默认px | String \\ Number | 18 | \- |
| placement | 布局方式，row-横向，column-纵向 | String | row | column |
| label | 文本 | String | \- | \- |
| labelColor | label的字体颜色 | String | #303133 | \- |
| labelSize | label的字体大小，px单位 | String \\ Number | 14 | \- |
| labelDisabled | 是否禁止点击文本操作 | Boolean | false | true |
| iconColor | 图标颜色 | String | #ffffff | \- |
| iconSize | 图标的大小，单位px | String \\ Number | 12 | \- |
| borderBottom | 竖向配列时，是否显示下划线 | Boolean | false | true |
| iconPlacement | 勾选图标的对齐方式，left-左边，right-右边 | String | left | right |

### [#](#radio-event) radio Event

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| change | 某个`radio`状态发生变化时触发(选中状态) | name: 通过`props`传递的`name`参数 | \- |

### [#](#radiogroup-event) radioGroup Event

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| change | 任一个`radio`状态发生变化时触发 | name: 值为`radio`通过`props`传递的`name`值 | \- |

← [Checkbox 复选框](https://www.uviewui.com/components/checkbox.html) [Switch 开关选择器](https://www.uviewui.com/components/switch.html) →


