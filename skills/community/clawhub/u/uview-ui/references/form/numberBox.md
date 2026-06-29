---
name: "numberBox"
description: "NumberBox 步进器 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs NumberBox 步进器 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/numberBox.html"
---

---

## [#](#numberbox-步进器) NumberBox 步进器 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件一般用于商城购物选择物品数量的场景

注意：该输入框只能输入大于或等于0的整数

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

通过`v-model`绑定`value`初始值，此值是双向绑定的，**无需**在回调中将返回的数值重新赋值给`value`。

```
<template>
	<u-number-box v-model="value" @change="valChange"></u-number-box>
</template>

<script>
	export default {
		data() {
			return {
				value: 0
			}
		},
		methods: {
			valChange(e) {
				console.log('当前值为: ' + e.value)
			}
		}
	}
</script>
```

### [#](#步长设置) 步长设置

-   通过`step`属性设置每次点击增加或减少按钮时变化的值，默认为1，下面示例每次都会加2或者减2

```
<u-number-box :step="2"></u-number-box>
```

### [#](#限制输入范围) 限制输入范围

通过`min`和`max`参数限制输的入值最小值和最大值

```
<u-number-box :min="1" :max="100"></u-number-box>
```

### [#](#限制只能输入整数) 限制只能输入整数

通过`integer`限制输入类型

```
<u-number-box integer></u-number-box>
```

### [#](#禁用) 禁用

```

<u-number-box :disabled="true"></u-number-box>

<u-number-box :disabledInput="true"></u-number-box>

<u-number-box :disablePlus="true"></u-number-box>

<u-number-box :disableMinus="true"></u-number-box>

<u-number-box :longPress="false"></u-number-box>
```

### [#](#固定小数位数) 固定小数位数

通过`step`设置步进长度，`decimal-length`设置显示小数位数

```
<u-number-box step="0.25" decimal-length="1" ></u-number-box>
```

### [#](#异步变更) 异步变更

通过`asyncChange`设置异步变更，开启后需要手动控制输入值 （默认 false ）

```
<template>
    <u-number-box v-model="value" :asyncChange="true" @change="onChange"></u-number-box>
</template>

<script>
export default {
    data(){
        return {
            value:1
        }
    },
    methods:{
        onChange(e){
            setTimeout(() => {
                this.value = this.value + 1;
            }, 3000)
        }
    }
}
</script>
```

### [#](#自定义颜色和大小) 自定义颜色和大小

-   通过`button-size`参数设置按钮大小
-   通过`icon-style`参数设置加减按钮图标的样式

```
<u-number-box
    button-size="36"
    color="#ffffff"
    bgColor="#2979ff"
    iconStyle="color: #fff"
></u-number-box>
```

### [#](#自定义-slot) 自定义 slot

```
<template>
    <u-number-box v-model="value">
        <view
            slot="minus"
            class="minus"
        >
            <u-icon
                name="minus"
                size="12"
            ></u-icon>
        </view>
        <text
            slot="input"
            style="width: 50px;text-align: center;"
            class="input"
        >{{value}}</text>
        <view
            slot="plus"
            class="plus"
        >
            <u-icon
                name="plus"
                color="#FFFFFF"
                size="12"
            ></u-icon>
        </view>
    </u-number-box>
</template>

<script>
export default {
    data(){
        return {
            value:1
        }
    }
}
</script>

<style lang="scss">
	.minus {
		width: 22px;
		height: 22px;
		border-width: 1px;
		border-color: #E6E6E6;
		border-style: solid;
		border-top-left-radius: 100px;
		border-top-right-radius: 100px;
		border-bottom-left-radius: 100px;
		border-bottom-right-radius: 100px;
		@include flex;
		justify-content: center;
		align-items: center;
	}

	.input {
		padding: 0 10px;
	}

	.plus {
		width: 22px;
		height: 22px;
		background-color: #FF0000;
		border-radius: 50%;

		display: flex;

		justify-content: center;
		align-items: center;
	}
</style>

```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsB/numberBox/numberBox.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsB/numberBox/numberBox.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| name | 步进器标识符，在change回调返回 | String | Number | \- | \- |
| value | 用于双向绑定的值，初始化时设置设为默认min值(最小值) | String | Number | 1 | \- |
| min | 用户可输入的最小值 | String | Number | 1 | \- |
| max | 用户可输入的最大值 | String | Number | `Number.MAX_SAFE_INTEGER` | \- |
| step | 步长，每次加或减的值， 支持小数值，如需小数 | String | Number | 1 | \- |
| integer | 是否只能输入正整数 | Boolean | false | true |
| disabled | 是否禁用操作，包括输入框，加减按钮 | Boolean | false | true |
| disabledInput | 是否禁止输入框 | Boolean | false | true |
| asyncChange | 是否开启异步变更，开启后需要手动控制输入值 | Boolean | false | true |
| inputWidth | 输入框宽度，单位px | String | Number | 35 | \- |
| showMinus | 是否显示减少按钮 | Boolean | true | false |
| showPlus | 是否显示增加按钮 | Boolean | true | false |
| decimalLength | 显示的小数位数 | String | Number | \- | \- |
| longPress | 是否允许长按进行加减 | Boolean | true | false |
| color | 输入框文字和加减按钮图标的颜色 | String | #323233 | \- |
| buttonSize | 按钮大小，宽高等于此值，单位px，输入框高度和此值保持一致 | String | Number | 30 | \- |
| bgColor | 输入框和按钮的背景颜色 | String | #EBECEE | \- |
| cursorSpacing | 指定光标于键盘的距离，避免键盘遮挡输入框，单位px | String | Number | 100 | \- |
| disablePlus | 是否禁用增加按钮 | Boolean | false | true |
| disableMinus | 是否禁用减少按钮 | Boolean | false | true |
| iconStyle | 加减按钮图标的样式 | String | \- | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| focus | 输入框得到焦点触发(按钮可点击情况下)，对象形式 | value：输入框当前值，name：步进器标识符 |
| blur | 输入框失去焦点时触发，对象形式 | value：输入框当前值，name：步进器标识符 |
| change | 输入框内容发生变化时触发，对象形式 | value：输入框当前值，name：步进器标识符 |
| overlimit | 超过范围阈值时触发 | type：（`minus`已达最小值，`plus`已达最大值） |

### [#](#slots) Slots

| 名称 | 说明 |
| --- | --- |
| minus | 减少按钮 |
| input | 输入框 |
| plus | 增加按钮 |

← [Search 搜索](https://www.uviewui.com/components/search.html) [Upload 上传](https://www.uviewui.com/components/upload.html) →


