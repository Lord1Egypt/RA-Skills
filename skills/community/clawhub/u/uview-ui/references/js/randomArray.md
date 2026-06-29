---
name: "randomArray"
description: "数组乱序 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 数组乱序 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/randomArray.html"
---

---

## [#](#randomarray-数组乱序) randomArray 数组乱序

#### [#](#randomarray-array) randomArray(array)

该函数可以打乱一维数组元素的顺序，这是随机过程

-   `array` <Array> 一维数组

```
export default{
	data() {
		return {
			array: [1,2,3,4,5]
		}
	},
	onLoad() {
		console.log(uni.$u.randomArray(this.array));
	}
}
```

← [路由跳转](https://www.uviewui.com/js/route.html) [全局唯一标识符](https://www.uviewui.com/js/guid.html) →


