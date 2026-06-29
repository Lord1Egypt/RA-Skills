---
name: "http"
description: "Http 请求 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Http 请求 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/http.html"
---

---

## [#](#http请求) Http请求

该插件适用于普遍的请求场景，支持`post`、`get`、`put`和`delete`，以及上传下载等请求，有如下特点：

-   基于`Promise`对象实现更简单的`request`使用方式，支持请求和响应拦截
-   支持全局挂载
-   支持多个全局配置实例
-   支持自定义验证器
-   支持文件上传/下载
-   支持task 操作
-   支持自定义参数
-   支持多拦截器
-   对参数的处理比`uni.request`更强

### [#](#平台差异说明) 平台差异说明

| App | H5 | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ小程序 |
| --- | --- | --- | --- | --- | --- | --- |
| √ | √ | √ | √ | √ | √ | √ |

说明

此插件集成自优秀的开源请求库：[luch-request (opens new window)](https://www.quanzhan.co/luch-request/)。uView对其进行了简单封装以及说明，如有不全之处， 可参考[luch-request (opens new window)](https://www.quanzhan.co/luch-request/)官方文档。

### [#](#基本使用) 基本使用

```
uni.$u.http.middleware(config)
uni.$u.http.request(config)
uni.$u.http.get(url[, config])
uni.$u.http.upload(url[, config])
uni.$u.http.delete(url[, data[, config]])
uni.$u.http.head(url[, data[, config]])
uni.$u.http.post(url[, data[, config]])
uni.$u.http.put(url[, data[, config]])
uni.$u.http.connect(url[, data[, config]])
uni.$u.http.options(url[, data[, config]])
uni.$u.http.trace(url[, data[, config]])
```

### [#](#全局配置) 全局配置

可选的配置项有如下：

```
{
    baseURL: '',
    header: {},
    method: 'GET',
    dataType: 'json',

    responseType: 'text',

    custom: {},

    timeout: 60000,

    sslVerify: true,

    withCredentials: false,

    firstIpv4: false,

    validateStatus: (statusCode) => {
        return statusCode >= 200 && statusCode < 300
    }
}
```

可以通过`uni.$u.http.setConfig()`方法进行全局配置，比如配置请求的全局域名`baseUrl`：

```
uni.$u.http.setConfig((config) => {

    config.baseURL = `https://www.example.com`;
    return config
})
```

### [#](#get请求) GET请求

需要注意的是，`get`请求与`post`请求略有不同，`get`请求所有参数都在方法的第二个参数中，而`post`请求的第二个参数为请求参数`params`，而第三个参数才为配置项。

```

uni.$u.http.get('/user/login', {params: {userName: 'name', password: '123456'}}).then(res => {

}).catch(err => {

})

uni.$u.http.get('/user/login', {
    params: {userName: 'name', password: '123456'},
    header: {},
    dataType: 'json',

    custom: {auth: true},

    responseType: 'text',

    timeout: 60000,

    sslVerify: true,

    firstIpv4: false,

    withCredentials: false,

    getTask: (task, options) => {

    },

}).then(res => {

}).catch(err => {

})
```

### [#](#post请求) POST请求

需要注意的是，get请求与post请求略有不同，get请求所有参数都在方法的第二个参数中，而post请求的第二个参数为请求参数params，而第三个参数才为配置项。

```

uni.$u.http.post('/user/login', {userName: 'name', password: '123456'} ).then(res => {

}).catch(err => {

})

uni.$u.http.post('/user/login', {userName: 'name', password: '123456'}, {
    params: {},
    header: {},
    dataType: 'json',

    custom: {auth: true},

    responseType: 'text',

    timeout: 60000,

    sslVerify: true,

    firstIpv4: false,

    withCredentials: false,

    getTask: (task, options) => {

    },

}).then(res => {

}).catch(err => {

})
```

### [#](#upload请求) UPLOAD请求

具体参数说明：[uni.uploadFile (opens new window)](https://uniapp.dcloud.io/api/request/network-file)

```
uni.$u.http.upload('api/upload/img', {
    params: {},

    files: [],

    fileType: 'image/video/audio',

    filePath: '',

    custom: {auth: true},
    name: 'file',

    timeout: 60000,

    header: {},
    formData: {},

    getTask: (task, options) => {

    },

}).then(res => {

}).catch(err => {

})
```

### [#](#download请求) DOWNLOAD请求

具体参数说明：[uni.downloadFile (opens new window)](https://uniapp.dcloud.io/api/request/network-file?id=downloadfile)

```
uni.$u.http.download('api/download', {
    params: {},

    timeout: 3000,

    header: {},
    custom: {},

    getTask: (task, options) => {

    },

}).then(res => {

}).catch(err => {

})
```

### [#](#请求拦截器) 请求拦截器

```
uni.$u.http.interceptors.request.use((config) => {
	config.header = {
		...config.header,
		a: 1
	}

	return config
}, config => {
	return Promise.reject(config)
})
```

### [#](#响应拦截器) 响应拦截器

```
uni.$u.http.interceptors.response.use((response) => {

	console.log(response)
	return response
}, (response) => {

	console.log(response)
	return Promise.reject(response)
})
```

### [#](#实践) 实践

假设我们项目中需要用到请求和响应拦截器，并且在请求拦截器中需要调用`vuex`中的变量，可按如下步骤进行操作(仅供参考)：

#### [#](#_1-全局配置-以及请求-响应拦截器定义) 1. 全局配置，以及请求，响应拦截器定义

在`/config/request.js`中，写入如下内容：

```

module.exports = (vm) => {

    uni.$u.http.setConfig((config) => {

        config.baseURL = 'https://www.example.com';
        return config
    })

	uni.$u.http.interceptors.request.use((config) => {

	    config.data = config.data || {}

		if(config?.custom?.auth) {

			config.header.token = vm.$store.state.userInfo.token
		}
	    return config
	}, config => {
	    return Promise.reject(config)
	})

	uni.$u.http.interceptors.response.use((response) => {
		const data = response.data

		const custom = response.config?.custom
		if (data.code !== 200) {

			if (custom.toast !== false) {
				uni.$u.toast(data.message)
			}

			if (custom?.catch) {
				return Promise.reject(data)
			} else {

				return new Promise(() => { })
			}
		}
		return data.data === undefined ? {} : data.data
	}, (response) => {

		return Promise.reject(response)
	})
}
```

#### [#](#_2-引用配置) 2. 引用配置

我们可以在`main.js`中引用`/config/request.js`，注意引用的位置，需要在`new Vue`得到`Vue`实例之后，如下：

```
import Vue from 'vue'
import App from './App'

import store from './store'
Vue.prototype.$store = store

Vue.config.productionTip = false
App.mpType = 'app'

import uView from 'uview-ui'
Vue.use(uView)

import mixin from './common/mixin'
Vue.mixin(mixin)

const app = new Vue({
	store,
	...App
})

require('/config/request.js')(app)

app.$mount()
```

#### [#](#_3-api集中管理) 3. Api集中管理

在`/config/api.js`中编写请求接口：

```
const http = uni.$u.http

export const postMenu = (params, config = {}) => http.post('/ebapi/public_api/index', params, config)

export const getMenu = (data) => http.get('/ebapi/public_api/index', data)
```

#### [#](#_4-发送请求) 4. 发送请求

```
import { postMenu, getMenu } from '/config/api.js';

postMenu({ custom: { auth: true }}).then(() => {

}).catch(() =>{

})

await postMenu({ custom: { auth: true }})

postMenu({ custom: { auth: true, toast: false, catch: false }}).then(() => {

})

getMenu({ custom: { auth: true }}).then(() => {

}).catch(() =>{

})

uni.$u.http.post('/common/menu', { custom: { auth: true }}).then(() => {

}).catch(() =>{

})
```

← [便捷工具](https://www.uviewui.com/js/fastUse.html) [节流防抖](https://www.uviewui.com/js/debounce.html) →


