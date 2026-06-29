---
name: "queryParams"
description: "对象转 URL 参数 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 对象转 URL 参数 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/queryParams.html"
---

---

## [#](#queryparams-对象转url参数) queryParams 对象转URL参数

该方法，可以将一个对象形式参数转换成`get`传参所需参数形式，如把`{name: 'lisa', age: 20}`转换成`?name=lisa&age=20`
用途：可以用于`uni.navigateTo`接口传参等场景，无需自己手动拼接`URL`参数

#### [#](#queryparams-data-isprefix-true-arrayformat-brackets) queryParams(data, isPrefix = true, arrayFormat = 'brackets')

-   `data` <Object> 对象值，如`{name: 'lisa', age: 20}`
-   `isPrefix` <Boolean> 是否在返回的字符串前加上"?"，默认为`true`
-   `arrayFormat` <Boolean> 属性为数组的情况下的处理办法，默认为`brackets`，见后面说明

```
export default {
	data() {
		return {
			data: {
				name: 'lisa',
				age: 20
			}
		}
	},
	onLoad() {
		console.log(uni.$u.queryParams(this.data));

	}
}
```

#### [#](#arrayformat参数说明) arrayFormat参数说明

如果您传入的`data`对象内部某些属性值为数组的情况下，您可能需要留意这个参数的配置：
该参数可选值有4个：`indices`，`brackets`，`repeat`，`comma`，具体效果请见下方的演示说明

```
export default {
	data() {
		return {
			data: {
				name: '冷月夜',
				fruits: ['apple', 'banana', 'orange']
			}
		}
	},
	onLoad() {
		uni.$u.queryParams(this.data, true, 'indices');

		uni.$u.queryParams(this.data, true, 'brackets');

		uni.$u.queryParams(this.data, true, 'repeat');

		uni.$u.queryParams(this.data, true, 'comma');

	}
}
```

← [颜色值](https://www.uviewui.com/js/color.html) [规则校验](https://www.uviewui.com/js/test.html) →


