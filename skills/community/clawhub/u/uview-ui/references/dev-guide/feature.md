---
name: "feature"
description: "注意事项 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 注意事项 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/feature.html"
---

---

## [#](#注意事项) 注意事项

由于uni-app支持多端开发，而各端，特别是各小程序平台，没有统一的标准，加重了开发者和企业的成本，幸好uni-app使用Vue标准，对各端进行了写法的统一， 推动了生态的发展，但是由于某些小程序平台自身的原因，仍然会出现某些兼容性问题，我们会将制作uView过程中遇到，和平时收集的兼容性问题呈现在本专题，希望能 帮助到uni-app开发者。

### [#](#微信小程序) 微信小程序

注意

微信小程序基础库需要设置在2.19.2及以上

### [#](#支付宝小程序) 支付宝小程序

注意

uView需要开启了`component2`模式才支持支付宝小程序

1.  支付宝在很早前，已升级为`component2`模式，此模式支持更多的功能和特性，uni-app上，很多的特性，如`provide/inject`、`$slots`等，需要开启此模式才能支持， 而此模式在uni-app新建项目中默认是关闭的，因而需要在项目根目录的`manifest.json`中开启，如没有`alipay`属性节点，新增即可：

```
......
"mp-alipay" : {
	"component2": true
},
......
```

2.  uView的`waterfall`瀑布流组件使用了`$scoped slot`特性，由于hx的问题，在hx2.8.2修正了此问题，所以瀑布流组件需要hx2.8.2及以上才支持支付宝小程序。

### [#](#vue特性在各平台支持度) Vue特性在各平台支持度

1.  以下特性，uView已对各小程序开发工具，H5浏览器，APP(不含NVUE)进行过实测，均获得支持，其中支付宝小程序需要开启`component2`模式。

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

-   provide / inject
-   $slots
-   v-model / sync
-   $parent / $children

### [#](#设置页面背景颜色) 设置页面背景颜色

一般情况下，我们给页面的`page`节点或者给页面的最外层`view`设置背景颜色，二者分别有如下需要注意点：

#### [#](#_1-通过page节点设置) 1. 通过`page`节点设置

这个方式全端有效，但是需要注意的是，在微信小程序，或者某些安卓机型上，该节点如果写在带`scoped`属性的样式标签内是无效的，所以我们建议 您可以在页面多加一个不带scoped属性的样式标签，如下：

```

<style lang="scss">
page {
	background-color: $u-bg-color;
}
</style>

<style lang="scss" scoped>
.box {
	......
}
</style>
```

#### [#](#_2-通过页面外层view设置) 2. 通过页面外层`view`设置

相比`page`节点，`view`的高度默认为内容高度，所以如果页面内容不足一屏高度时，底部剩余部分依然为默认的白色，所以我们给需要这个`view`设置一个 最低高度，让它等于窗口高度：

```
<template>
	<view class="wrap">
		......
	</view>
</template>

<style scoped lang="scss">
.wrap {
	background-color: $u-bg-color;
	min-height: 100vh;
}
</style>
```

### [#](#全局赋值设备信息的陷阱) 全局赋值设备信息的陷阱

我们都知道，可以通过`uni.getSystemInfoSync()`获取设备信息，但是每次用到时都写一遍是很繁琐的，所以很多同学们都会突发奇想，比如在`main.js`或者 在`App.vue`中将`uni.getSystemInfoSync()`的结果赋值给`Vue.prototype`，如下：

```

Vue.prototype.system = uni.getSystemInfoSync();
```

上面的写法没有问题，我们可以任意地方通过`this.system`得到设备的信息，但是这里有一个陷阱，写在`main.js`，意味着赋值代码只会被执行一次，且是APP启动的时候， 但是uni-app中，设备信息的`windowHeight`属性是不含APP的导航栏和tabbar高度在内的，当我们进入首页时，`windowHeight`不含tabbar高度在内，高度可能为 '700px'，但是进入内页后，没有tabbar，这时的`windowHeight`高度依然为700px(少掉了tabbar的50px高度)，显然是不正确的。
上面说的只是对`windowHeight`属性有影响，其他的属性无碍，如果是需要获取高度，建议每次都执行`uni.getSystemInfoSync()`，或者通过uView提供的快捷工具 `uni.$u.sys()`方法获取即可。

### [#](#小程序主包太大无法预览和发布) 小程序主包太大无法预览和发布

我们都知道微信小程序预览和发布的主包大小都不能超过`2M`，否则无法真机预览和上传发布，经常有同学反馈刚使用uView，调试时候主包就超过了`2M`而无法真机预览， 我们在这里做一个说明，uView是`按需引入`的，在发行时，HX会自动剔除您没有使用组件，即使您使用了uView的全部组件，整个uView的大小也只有500K左右，但是有如下两点前提：

-   **调试**
    在调试阶段，为了调试的友好效果和编译速度等，HX默认是没有对JS进行压缩和去除注释，也没有进行组件按需引入的，所以会导致JS文件都很大，我们需要在 HBuilder X进行如下操作，再重新编译即可：

```
HBuilderX   运行->运行到小程序模拟器->勾选 运行时是否压缩代码
```

-   **发布**
    在HX中进行发布时，uView的组件会按需引入(使用uView所有组件的情况下，占用空间500k左右)，如果主包依然超出`2M`，您需要从多个方面着手：

1.  [小程序分包 (opens new window)](https://uniapp.dcloud.io/collocation/pages?id=subpackages)
2.  将静态资源放到服务器进行引用
3.  取消"ES6转ES5"设置

### [#](#uni-scss的优缺点) uni.scss的优缺点

`uni.scss`为uni-app新建项目自带工程文件，使用的预处理器为`sass/scss`，由此可见，uni-app官方推荐的是`scss`，同时我们uView也是`scss`的坚定推崇者，不建议在 uni-app中使用`less`、`stylus`等。

`uni.scss`具有如下一些特点：

-   无需引入，uni-app在编译时，会自动引入此文件
-   在此中定义的`scss`变量，可以全局使用，可以在此定义一些颜色，主题，尺寸等变量
-   **`uni.scss`会编译到每个`scss`文件中**(请着重理解这一句话)

综上所述，我们可以得知，`uni.scss`主要是利用`scss`的特性，定义一些全局变量，供各个写了`lang=scss`的style标签引用，但是这引出了一个重要的问题：
`uni.scss`中所写的一切内容，都会注入到每个声明了`scss`的文件中，这意味着，如果您的`uni.scss`如果有几百行，大小10k左右，那么这个10k都会被注入所有的 其他`scss`文件(页面)中，如果您的应用有50个页面，那么有可能因此导致整体的包体积多了50 \* 10 = 500k的大小，这可能会导致小程序包太大而无法预览和发布， 所以，我们建议您只将`scss`变量相关的内容放到`uni.scss`中。

### [#](#样式覆盖兼容性) 样式覆盖兼容性

为了避免样式被用户覆盖，或者被污染，一般组件或者页面都会给`style`标签加上`scoped`属性，如下演示为一个组件的内部构造：

```
/* item.vue */
<template>
	<view class="item"></view>
</template>

<style scoped>
	.item {
		border: 1px solid red;
	}
</style>
```

我们在页面中引入上方的`item`组件，并且想修改它的`border`边框为颜色(blue)，一般通过`v-deep`或`/deep/`指令修改，如下写法：

```
<template>
	<item></item>
</template>

<style scoped>
::v-deep .item {
	border: 1px solid blue;
}
</style>
```

上面的写法，在`App`和`H5`正常，但是在微信小程序无效，它要求`::v-deep`或`/deep/`前面必须还要有父元素的类名存在，如下：

```
<template>
	<view class="wrap">
		<item></item>
	</view>
</template>

<style scoped>
.wrap ::v-deep .item {
	border: 1px solid blue;
}
</style>
```

如果是在支付宝小程序中，写在组件上的类名和内联样式，都是无效的，如下：

```
<template>
	/* 在支付宝小程序，组件标签上的任何class和style都会被剔除，不会添加到组件内部的根元素中 */
	<item style="border: 1px solid blue" class="item"></item>
</template>
```

← [内置样式](https://www.uviewui.com/components/common.html) [对比 1.X](https://www.uviewui.com/components/diff1.x.html) →


