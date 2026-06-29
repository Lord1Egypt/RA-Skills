---
name: "mpShare"
description: "小程序分享 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 小程序分享 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/mpShare.html"
---

---

## [#](#mpshare-小程序分享) mpShare 小程序分享

此功能，是对uni的[onShareAppMessage 生命周期 (opens new window)](https://uniapp.dcloud.io/api/plugins/share?id=onshareappmessage)的封装。

这里说的小程序，指的是"微信小程序、百度小程序、头条小程序、QQ小程序，支付宝小程序等"。

由于小程序的分享(微信、头条平台)，需要监听页面的`onShareAppMessage`生命周期，小程序需要在页面声明了此生命周期，点击右上角的"胶囊"才会有分享功能， 而一般情况下，我们希望每个页面都可以分享，那就需要每个页面都写一遍这个生命周期，是很繁琐的。

基于以上，uView通过`mixin`的形式，给每一个页面注入了`onShareAppMessage`生命周期，让您简单引入，无需任何后续操作，即可让每一个页面都有分享功能(仅针对小程序)。

### [#](#平台差异说明) 平台差异说明

| App | H5 | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ小程序 |
| --- | --- | --- | --- | --- | --- | --- |
| x | x | √ | √ | √ | √ | √ |

### [#](#基本使用) 基本使用

需要注意的是，小程序(uni)没有提供类似"getNavigationBarTitle"这样的接口，所以我们无法获取当前页面导航栏的标题，换言之，我们想要每个页面个性化的 分享标题，需要手动设置，否则**默认为小程序的名称**。

注意：

分享功能是默认关闭的，但是我们写好各项配置，您只要在`main.js`中引入对应的文件即可，我们没有默认引入，是因为某些用户并不需要此功能。

打开小程序分享功能：

```

let mpShare = require('uview-ui/libs/mixin/mpShare.js');
Vue.mixin(mpShare)

```

分享功能，一般有三个参数，如下：

```

uni.$u.mpShare = {
	title: '',
	path: '',

	imageUrl: ''
}
```

以上这些，uView已通过`mixin`集成，当某一个页面您需要自定义分享信息时，可以通过"uni.$u.mpShare"对进行修改，在页面的`onLoad`生命周期修改即可。

```
export default {
	onLoad() {
		uni.$u.mpShare.title = '天苍苍野茫茫，风吹草低见牛羊';
	}
}
```

### [#](#重写-onshareappmessage-生命周期) 重写"onShareAppMessage"生命周期

如果您基于自己的一些业务逻辑，需要更加自定义的实现逻辑，可以在页面中重写`onShareAppMessage`生命周期即可覆盖uView通过`mixin`监听的`onShareAppMessage`生命周期。

```
export default {

	onShareAppMessage(res) {
		if (res.from === 'button') {
			console.log(res.target)
		}
		return {
			title: '自定义分享标题',
			path: '/pages/test/test?id=123'
		}
    }
}
```

### [#](#分享到朋友圈) 分享到朋友圈

此功能为微信小程序最新加入的功能，仅适用于微信小程序，uView也全局监听了此生命周期。

同理，你也可以在页面中重写`onShareTimeline`生命周期即可覆盖uView通过`mixin`监听的`onShareTimeline`生命周期。

```
export default {
	onShareTimeline(res) {
		if (res.from === 'button') {
			console.log(res.target)
		}
		return {
			title: '自定义分享标题',
			path: '/pages/test/test?id=123'
		}
    }
}
```

← [节点布局信息](https://www.uviewui.com/js/getRect.html)


