---
name: "quickstart"
description: "快速上手 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 快速上手 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/quickstart.html"
---

---

## [#](#快速上手) 快速上手

### [#](#如何使用) 如何使用

通过npm和下载方式的配置之后，在某个页面可以直接使用组件，无需通过`import`引入组件。

```
<template>
	<view>
		<u-action-sheet :actions="list" :title="title" :show="show"></u-action-sheet>
		<u-button @click="show = true">打开ActionSheet</u-button>
	</view>
</template>

<script>
export default {
	data() {
		return {
			title:'标题',
			list: [
				{
					name:'选项一',
					subname:"选项一描述",
					color:'#ffaa7f',
					fontSize:'20'
				},
				{
					name: '选项二禁用',
					disabled:true
				},
				{
					name: '开启load加载',
					loading:true
				}
			],
			show: false
		};
	}
};
</script>
```

### [#](#关于uni-u) 关于uni.$u

从`1.7.9`开始，uView将`$u`对象同时挂载到了`uni`对象上，这意味着您可以在外部的`js`文件中，通过`uni.$u.xxx`的形式去调用uView提供的一些工具方法，而不再像从前一样必须在`*.vue`中通过`uni.$u.xxx`的形式调用。

### [#](#如何不使用easycom而单独引用某一个组件) 如何不使用easycom而单独引用某一个组件

某些情况下，您可能不想通过easycom引用组件(虽然我们极力推荐您使用easycom)，那么您可以使用`import`这个常规的引入方式，如下：

```
<template>
	<u-action-sheet :list="list" v-model="show"></u-action-sheet>
</template>

<script>
	import uActionSheet from "uView-ui/components/u-action-sheet/u-action-sheet.vue";
	export default {
		components: {
			uActionSheet
		},
		data() {
			return {
				list: [{
					text: '点赞',
					color: 'blue',
					fontSize: 28
				}, {
					text: '分享'
				}, {
					text: '评论'
				}],
				show: true
			}
		}
	}
</script>
```

### [#](#关于uview组件的esaycom规则可能和其他组件引入名称冲突的问题) 关于uView组件的esaycom规则可能和其他组件引入名称冲突的问题

uView的组件引入是通过easycom形式的，写在pages.json中，以`u-`开头，这可能和其他UI组件，或者uni-app插件市场的[uParse修复版-html富文本加载 (opens new window)](https://ext.dcloud.net.cn/plugin?id=364)组件名冲突而**报错**， 原因是此`uParse`的组件引用名为`u-parse`，也是`u-`开头，即使您在页面中显式地配置了组件引入，但uni-app仍认为easycom配置的规则优先级比页面引入的组件规则高。

以下为`uParse`第三方插件的官方写法：

```
<template>
    <u-parse :content="xxx"></u-parse>
</template>

<script>
	import uParse from '@/components/gaoyia-parse/parse.vue'
	export default {
		 components: {
			uParse
		 }
	}
</script>
```

可以看到，上方虽然通过`import`声明了此组件，最终引用的组件名称为`<u-parse>`("u-"开头)，但是uni-app仍然忽视了，而认为uView在`pages.json`配置的easycom规则的优先级更高，因而去uView的组件库 中查找`u-parse`，因为找不到而报错，这是不合理的。

解决办法也很简单，给冲突的插件换一个名字即可，比如上面的`uParse`插件，我们在`import`和`components`声明的时候换一个名字即可，比如这里让其为字母`a`开头：

```
<template>
    <a-parse :content="xxx"></a-parse>
</template>

<script>

	import aParse from '@/components/gaoyia-parse/parse.vue'
	export default {
		 components: {
			aParse
		 }
	}
</script>
```

← [配置](https://www.uviewui.com/components/setting.html) [内置样式](https://www.uviewui.com/components/common.html) →


