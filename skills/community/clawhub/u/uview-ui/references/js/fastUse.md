---
name: "fastUse"
description: "便捷工具 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 便捷工具 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/fastUse.html"
---

---

## [#](#便捷工具) 便捷工具

此专题内容为一些方便用户快速，便捷使用的小工具，可能是uView的一些方法的简易版，或者对uni的一些方法进行二次封装，方便用户 快速使用。

### [#](#os) os()

此方法用于返回平台的名称，为小写的`ios`或`android`

```
uni.$u.os()
```

### [#](#sys) sys()

此方法用于获取设备的信息，相当于uni.getSystemInfoSync()的效果

```
uni.$u.sys()
```

### [#](#platform) platform

此`属性`用于获取当前运行的平台名称，相较于`uni-app`系统自带的条件编译的区别是，此方式让我们可以通过`js`的`if | else if`进行判断， 您可以结合实际场景进行使用。

-   注意：此属性返回的结果，和`uni-app`的条件编译名称有差别，并且结果都为小写。

使用前配置：如果您的项目为`vue-cli`模式，必须要在`根目录`的`vue.config.js`进行配置才有效，如下：

```

module.exports = {
    transpileDependencies: ['uview-ui']
}
```

使用：

```

uni.$u.platform

const { platform } = uni.$u
if(platform === 'app') {
	......
} else if(platform === 'nvue') {
	......
}
```

#### [#](#各平台对应返回值如下表) 各平台对应返回值如下表：

| 平台 | 返回值 |
| --- | --- |
| VUE3，HBuilderX 3.2.0+ | vue3 |
| VUE2 | vue2 |
| App | plus |
| App nvue | nvue |
| H5 | h5 |
| 微信小程序 | weixin |
| 支付宝小程序 | alipay |
| 百度小程序 | baidu |
| 字节跳动小程序、飞书小程序 | toutiao |
| QQ小程序 | qq |
| 快手小程序 | kuaishou |
| 360小程序 | 360 |
| 微信小程序/支付宝小程序/百度小程序/字节跳动小程序/QQ小程序/360小程序 | mp |
| 快应用通用(包含联盟、华为) | webview |
| 快应用联盟 | webview-union |
| 快应用华为 | webview-huawei |

### [#](#range-min-max-value) range(min, max, value)

此方法用于限制`value`的大小，如果其在`min`和`max`之间，则不变；如果其小于`min`，则取`min`值；如果其大于`max`，则取`max`值。

```

uni.$u.range(1, 5, 8)

uni.$u.range(1, 5, 4)
```

### [#](#getpx-value-unit-false) getPx(value \[, unit = false\])

此方法用于返回带单位的值的数值结果，如果第二个参数为`true`，返回的结果将会带上`px`的单位；可接受的值如下：

-   带`upx`和`rpx`单位，返回使用`uni.upx2px`转换后，为`px`单位的结果
-   带`px`单位，返回去掉`px`单位的具体数值
-   具体数值，如`5`，将会返回`5`

```

uni.$u.getPx('10rpx')

uni.$u.getPx('12px')

uni.$u.getPx(14)

uni.$u.getPx('20rpx', true)
```

### [#](#sleep-value) sleep(value)

延时一定时间进行回调，类似于`promise`的使用方式

-   `value`，数值，单位默认为`ms`

```

uni.$u.sleep(300).then(() => {
	console.log('定时结束')
})
```

### [#](#parent-call-instance-name) $parent.call(instance \[, name\])

用于抹平各端差异，在组件中向上获取父组件或者页面的实例。

-   `instance`，实例，传`this`即可，不可修改
-   `name`，可选，页面或者父组件的`name`属性值，不传则默认查找页面(最顶层)的实例

```

<template>
	<child></child>
</template>

<script>
export default {

	name: 'page',
	......
}
</script>

<script>
export default {
	mounted() {

		uni.$u.$parent.call(this, 'page')
	}
}
</script>
```

### [#](#addstyle-style-target-object) addStyle(style \[, target = 'object'\])

用于将`字符串`形式的内联样式样式转为`对象`形式，或者将`对象`形式的样式写法转为`字符串`形式。

-   `style`，样式，可为对象或者字符串形式
-   `target`，可选，转换结果的类型，默认为`object`；如果为`object`则返回对象形式的结果，如果为`string`则返回字符串形式的结果

```

const style = { padding: '10px', margin: '20px' }
uni.$u.addStyle(style, 'string')

const style = "padding: 10px; margin: 20px"
uni.$u.addStyle(style)
```

### [#](#addunit-value-unit-px) addUnit(value \[, unit = 'px'\])

用于给值加上单位，如果值已有单位，则直接原样返回，如果值为`数值`，则加上`unit`参数的单位。

-   `value`，可为`5`，`5px`，`6rpx`，`100%`等格式的值
-   `unit`，可选，默认为`px`，如果第一个参数为`数值`，则拼接上此单位

```

uni.$u.addUnit(5)
uni.$u.addUnit('5px')

uni.$u.addUnit(5, 'rpx')
```

### [#](#priceformat-value-decimals-0-decimalpoint-thousandsseparator) priceFormat(value \[, decimals = 0 \[, decimalPoint = '.' \[, thousandsSeparator = ','\]\]\])

此方法可用于对数值形式的金额进行格式化

-   value，需要格式化的金额数值，只能为数值，如`300.52`，`300`，而不能为诸如带千分位的写法`3,000.5`
-   decimals，可选，格式化后小数点的位数，默认为`0`，小数最后一位会进行四舍五入
-   decimalPoint，可选，小数点的符号，默认为`.`
-   thousandsSeparator，可选，千分位分隔符，默认为英文逗号`,`

```

uni.$u.priceFormat(3002.365, 2)

uni.$u.priceFormat(3002.365)
```

### [#](#page) page()

此方法用于获取当前页面的路径，返回的路径以`/`开头。

```

uni.$u.page()
```

### [#](#pages) pages() 2.0.22

本方法为`getCurrentPages()`的封装，用于获取当前页面栈的实例，以数组形式按栈的顺序给出，第一个元素为首页，最后一个元素为当前页面。

```
uni.$u.pages()
```

← [介绍](https://www.uviewui.com/js/intro.html) [Http 请求](https://www.uviewui.com/js/http.html) →


