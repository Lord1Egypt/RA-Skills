---
name: "safeAreaInset"
description: "这个适配，主要是针对 IPhone X 等一些底部带指示条的机型，指示条的操作区域与页面底部存在重合，容易导致用户误操作，因此我们需要针对这些机型进行底部安全区适配。. Invoke when user needs to use safeAreaInset component."
url: "https://uviewpro.cn/zh/components/safeAreaInset.html"
triggers: ["safeAreaInset"]
---

# 安全区适配

## 底部安全区 <BadgeVersion text="0.3.4" />

这个适配，主要是针对 IPhone X 等一些底部带指示条的机型，指示条的操作区域与页面底部存在重合，容易导致用户误操作，因此我们需要针对这些机型进行底部安全区适配。  
uView Pro 是 uni-app 态的 UI 框架 uni-app 专门针对底部安全区域的解决方案，具体如下(也可见 uni 官方说明[全面屏、刘海屏适配（iphoneX 适配）及安全区设置](https://ask.dcloud.net.cn/article/35564))：

- 在 APP 上(以下只对 APP 生效)，可以通过项目根目录的`mainfest.json`文件`app-plus`节点下配置`safearea`的`bottom`属性为`none`，以此来关闭 IPhone X 等机型的底部安全区域。

配置后需要重新编译，并重启调试基座才会生效，具体如下：

```json
"app-plus": {
	"safearea": {
		"bottom": {
			"offset": "none"
		}
	}
}
```

如果`offset`设置为`auto`，那么在 IPhone X 的底部安全区，APP 上就会生成一个原生的元素进行占位，此时也就无需解决安全区指示条引起的问题。

- 在非 APP 端，诸如小程序，或者微信浏览器(其他浏览器，如 UC 等手机浏览器，底部有浏览器工具条，不存在安全区指示条引起的问题)，底部是没有安全区占位的。

像这种情况，就要使用 css 去解决，一般是通过给元素添加底部内边距的形式，如下：

```html
<style>
  .list {
    padding-bottom: 0;
    padding-bottom: constant(safe-area-inset-bottom);
    padding-bottom: env(safe-area-inset-bottom);
  }
</style>
```

鉴于以上问题，uView Pro 提供了一个组件`u-safe-bottom`，如果有需要，您可以在任何地方引用它，它会自动判断在并且在 IPhone X 等机型的时候，给元素加上一个适当
底部内边距，在 APP 上，即使您保留了原生安全区占位(`offset`设置为`auto`)，也不会导致底部出现双倍的空白区域，也即 APP 上`offset`设置为`auto`时。

```html
<template>
  <view>
    ......
    <u-safe-bottom></u-safe-bottom>
  </view>
</template>
```

## 顶部安全区 <BadgeVersion text="0.3.4" />

由于我们在做页面布局时经常会使用顶部位置，uView Pro 提供了一个组件`u-status-bar`，如`u-popup`从顶部弹出时，可以考虑使用此组件。

```html
<template>
  <view>
    <u-status-bar></u-status-bar>
    ......
  </view>
</template>
```

## 关于 uView Pro 某些组件`safe-area-inset`参数的说明

在 uView Pro 中，一些组件如`u-popup`、`u-keyboard`组件等，提供了一个`safeAreaInsetBottom`参数(布尔类型)，如果设置为`true`，就会在组件内部对安全区进行适配，
从而避免安全区指示条引起的问题，以下为 uView Pro 的`u-keyboard`组件在`微信浏览器`中分别设置`safeAreaInsetBottom`参数
为`false`和`true`的表现：

<div>
	<img src="https://ik.imagekit.io/anyup/uview-pro/docs/common/keyboard.png" alt="uView Pro" class="logo">
</div>
