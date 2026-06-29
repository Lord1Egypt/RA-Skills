---
name: "setting"
description: "配置 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 配置 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/setting.html"
---

---

## [#](#配置) 配置

### [#](#安装配置) 安装配置

由于uView支持`npm`和`下载`的方式安装，二者配置几乎一致，因为某些平台的兼容性，在配置easycom稍有不同，为了不造成混淆，这里将两种 方式分开说明：

-   [NPM方式安装的配置](https://www.uviewui.com/components/npmSetting.html)
-   [下载方式安装的配置](https://www.uviewui.com/components/downloadSetting.html)

### [#](#默认单位配置) 默认单位配置2.0.12

**温馨提示：** 2.0.25版本后，建议通过下方的`setCofig`方法进行设置。

在uView1.x中，组件参数如果为数值的话，默认为`rpx`单位，但是`rpx`在平板上会导致尺寸超大，为了更高的可用性，所以uView2.x将单位默认改为`px`，如果您出于 某些需求，需要将单位改为`rpx`，可以在`main.js`中进行如下配置即可：

```

import uView from 'uview-ui'
Vue.use(uView)

uni.$u.config.unit = 'rpx'
```

### [#](#修改uview内置配置方案) 修改uView内置配置方案 2.0.25

我们可以通过`setCofig`方法配置uView内部的各项内置配置，目前可配置的有`config`、`props`、`zIndex`、`color`属性，目前只建议修改`config`、`props`属性， 除非您清楚知道自己的修改所带来的影响。

```

import uView from 'uview-ui'
Vue.use(uView)

uni.$u.setConfig({

	config: {

		unit: 'rpx'
	},

	props: {

		radio: {
			size: 15
		}

	}
})
```

← [安装](https://www.uviewui.com/components/install.html) [快速上手](https://www.uviewui.com/components/quickstart.html) →


