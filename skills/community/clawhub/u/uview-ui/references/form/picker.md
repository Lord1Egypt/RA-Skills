---
name: "picker"
description: "Picker 选择器 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Picker 选择器 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/picker.html"
---

---

## [#](#picker-选择器) Picker 选择器 [![](https://www.uviewui.com/common/to_api.png)](#api)

此选择器用于单列，多列，多列联动的选择场景。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`show`绑定一个布尔值变量，用于控制组件的弹出与收起。
-   都通过传入数组`columns`配置选择项。

```
<template>
	<view>
		<u-picker :show="show" :columns="columns"></u-picker>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				show: false,
                columns: [
                    ['中国', '美国', '日本']
                ],
			}
		}
	}
</script>
```

### [#](#多列模式与多列联动) 多列模式与多列联动

此模式通过传入`columns`参数，此参数为二维数组，通过`change`事件完成联动操作。

```
<template>
    <u-picker :show="show" ref="uPicker" :columns="columns" @confirm="confirm" @change="changeHandler"></u-picker>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
                columns: [
                    ['中国', '美国'],
                    ['深圳', '厦门', '上海', '拉萨']
				],
                columnData: [
                    ['深圳', '厦门', '上海', '拉萨'],
                    ['得州', '华盛顿', '纽约', '阿拉斯加']
                ]
			}
		},
		methods: {
            changeHandler(e) {
                const {
                    columnIndex,
                    value,
                    values,
                    index,

                    picker = this.$refs.uPicker
                } = e

                if (columnIndex === 0) {

                    picker.setColumnValues(1, this.columnData[index])
                }
            },

			confirm(e) {
                console.log('confirm', e)
                this.show = false
			}
		}
	}
</script>
```

### [#](#加载状态) 加载状态

由于需要多列联动，此模式和上面的"多列模式"基本相同，在加载之前将`loading`设置为`true`，数据获取完成之后再置为`false`即可。

```
<template>
    <u-picker :show="show" ref="uPicker" :loading="loading" :columns="columns" @change="changeHandler"></u-picker>
</template>

<script>
    export default {
        data() {
            return {
                show: true,
                loading: false,
                columns: [
                    ['中国', '美国'],
                    ['深圳', '厦门', '上海', '拉萨']
                ],
                columnData: [
                    ['深圳', '厦门', '上海', '拉萨'],
                    ['得州', '华盛顿', '纽约', '阿拉斯加']
                ]
            }
        },
        methods: {
            changeHandler(e) {
                const {
                    columnIndex,
                    index,

					picker = this.$refs.uPicker
                } = e
                if (columnIndex === 0) {
                    this.loading = true

                    uni.$u.sleep(1500).then(() => {
                        picker.setColumnValues(1, this.columnData[index])
                        this.loading = false
                    })
                }
            }
        }
    }
</script>
```

### [#](#自定义选项值) 自定义选项值

参数`columns`可以传入自定义选项值，可以通过`keyName`参数控制对应的显示属性。

```
<template>
    <u-picker :show="show" :columns="columns" keyName="label"></u-picker>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
                columns: [
                    [{
                        label: '雪月夜',

                        id: 2021

                    }, {
                        label: '冷夜雨',
                        id: 804
                    }]
                ],
			}
		}
	}
</script>
```

### [#](#默认值) 默认值

此组件的所有模式，都可以设置默认值，通过`defaultIndex`数组参数配置，数组元素的0表示选中每列的哪个值(从0开始)，下面分别对几种模式进行说明：

**注意：** `defaultIndex`数组的长度，必须与列数相同，否则无效。

1.  单列模式

如设置`defaultIndex`为`[1]`表示默认选中第2个(从0开始)，`[5]`表示选中第6个。

2.  多列模式

如设置`defaultIndex`为`[1, 3]`表示第一列默认选中第2个，第二列默认选中第4个。

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsC/picker/picker.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsC/picker/picker.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| show | 用于控制选择器的弹出与收起 | Boolean | false | true |
| showToolbar | 是否显示顶部的操作栏 | Boolean | true | false |
| title | 顶部中间的标题 | String | \- | \- |
| columns | 设置每一列的数据，见上方说明 | Array | \- | \- |
| loading | 加载状态 | Boolean | false | true |
| itemHeight | 各列中，单个选项的高度 | String | Number | 44 | \- |
| cancelText | 取消按钮的文字 | String | 取消 | \- |
| confirmText | 确认按钮的文字 | String | 确认 | \- |
| cancelColor | 取消按钮的颜色 | String | #909193 | \- |
| confirmColor | 确认按钮的颜色 | String | #3c9cff | \- |
| visibleItemCount | 每列中可见选项的数量 | String | Number | 5 | \- |
| keyName | 自定义需要展示的`text`属性键名 | String | text | \- |
| closeOnClickOverlay | 是否允许点击遮罩关闭选择器（注意：关闭事件需要自行处理，只会在开启closeOnClickOverlay后点击遮罩层执行close回调） | Boolean | false | true |
| defaultIndex | 各列的默认索引 | Array | \- | \- |
| immediateChange 2.0.22 | 是否在手指松开时立即触发`change`事件。若不开启则会在滚动动画结束后触发`change`事件，只在微信`2.21.1`及以上有效 | Boolean | false | true |

### [#](#methods) Methods

| 名称 | 说明 |
| --- | --- |
| setIndexs | (index, setLastIndex) 设置对应列的选择值 |
| setColumnValues | 多列联动时需要用到，见上方说明，注意`微信小程序`的特殊用法 |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| close | 关闭选择器时触发 | \- | \- |
| confirm | 点击确定按钮，返回当前选择的值 | Array: 见上方"回调参数"部分说明 | \- |
| change | 当选择值变化时触发 | Array: 见上方"回调参数"部分说明 | \- |
| cancel | 点击取消按钮 | \- | \- |

← [Keyboard 键盘](https://www.uviewui.com/components/keyboard.html) [DatetimePicker 选择器](https://www.uviewui.com/components/datetimePicker.html) →


