---
name: "js-intro"
description: "API 介绍 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs API 介绍 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/js/intro.html"
---

---

## [#](#介绍) 介绍

此js函数方法，为uView框架提供的一部分功能，它的实现，需要通过js调用，而不是组件的形式。 工具库中的所有方法，均挂载在`$u`对象下，调用方法如下：

-   如果是在js中，需要通过`uni.$u.xxx`形式调用，如调用去除空格的`trim`方法：

```
console.log(uni.$u.trim(' abc '));
```

-   如果是在元素中，无需前缀`uni`，如：

```
<template>
	<view>
		去除所有空格：{{$u.trim(str, 'all')}}
	</view>
</template>

<script>
	export default {
		data() {
			return {
				str: 'a  b c '
			}
		}
	}
</script>
```

[便捷工具](https://www.uviewui.com/js/fastUse.html) →


