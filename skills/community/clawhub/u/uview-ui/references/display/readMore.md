---
name: "readMore"
description: "ReadMore 展开阅读更多 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs ReadMore 展开阅读更多 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/readMore.html"
---

---

## [#](#readmore-展开阅读更多) ReadMore 展开阅读更多 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件一般用于内容较长，预先收起一部分，点击展开全部内容的场景。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

通过slot传入正文内容

```
<template>
	<u-read-more>
		<rich-text :nodes="content"></rich-text>
	</u-read-more>
</template>

<script>
	export default {
		data() {
			return {

				content: `山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。
				苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。
				无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？`,
			}
		}
	}
</script>
```

### [#](#兼容性) 兼容性

由于一些微信小程序平台的渲染能力的问题，在解析[u-parse](https://www.uviewui.com/components/parse.html)组件内容时会比较耗时，导致`read-more`组件内部无法准确得知 内容的高度，而出现计算错误，这种情况下，我们需要借助`u-parse`组件的`@load`(内容多为文字时)或者`@ready`(内容多为图片时，可能会有较大延时)事件，通过`ref` 重新初始化`read-more`组件的高度，如下：

```
<template>
	<u-read-more ref="uReadMore">
		<u-parse :content="content" @load="load"></u-parse>
	</u-read-more>
</template>

<script>
	export default {
		data() {
			return {

				content: `山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。
				苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。
				无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？`,
			}
		},
		methods: {
            load() {
                this.$refs.uReadMore.init();
            }
		}
	}
</script>
```

### [#](#展开收起) 展开收起

配置`toggle`为`true`，展开后可以收起，否则展开后没有收起的按钮

```
<u-read-more :toggle="true">
    <rich-text :nodes="content"></rich-text>
</u-read-more>
```

### [#](#配置展开高度) 配置展开高度

可以配置一个高度，单位rpx，只有slot传入的内容高度超出这个值，才会出现"展开阅读全文"字样的按钮

```
<u-read-more showHeight="600">
    <rich-text :nodes="content"></rich-text>
</u-read-more>
```

### [#](#异步初始化) 异步初始化

有时候需要展示的内容是从后端获取的，组件内部的`mounted`生命周期初始化时，请求尚未回来，会导致 内容的高度在初始化有误差。可以在请求完毕渲染后(指的是this.$nextTick)，通过`ref`调用组件的`init`方法，重新初始化

```
<template>
	<u-read-more ref="uReadMore">
        <rich-text :nodes="content"></rich-text>
	</u-read-more>
</template>

<script>
	export default {
		data() {
			return {
				content: '',
			}
		},
		onLoad() {

			setTimeout(() => {
				this.content = `山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。
				苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。
				无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？`,

				this.$nextTick(() => {
					this.$refs.uReadMore.init();
				})
			}, 2000);
		}
	}
</script>
```

### [#](#自定义样式) 自定义样式

此组件上边部分有一个白色虚化的阴影，用以将点击区域与文字内容进行融合，如果您不想要这个阴影，可以调整`shadowStyle`对象，此对象内部如下：

```
{

    backgroundImage: "linear-gradient(-180deg, rgba(255, 255, 255, 0) 0%, #fff 80%)",

    backgroundImage: "linear-gradient(to top, #fff, rgba(255, 255, 255, 0.5))",

    paddingTop: "100px",
    marginTop: "-100px",
}
```

如果您不想要阴影，将`backgroundImage`设置为`none`即可，关于`paddingTop`和`marginTop`自行调整至合适数值即可。

```
<template>
	<u-read-more ref="uReadMore" :shadowStyle="shadowStyle" :showHeight="200">
		<rich-text :nodes="content"></rich-text>
	</u-read-more>
</template>

<script>
	export default {
		data() {
			return {
				content: '',
				shadowStyle: {
					backgroundImage: "none",
					paddingTop: "0",
					marginTop: "20rpx"
				}
			}
		}
	}
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsC/readMore/readMore.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsC/readMore/readMore.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| showHeight | 内容超出此高度才会显示展开全文按钮，单位rpx | String | Number | 400 | \- |
| toggle | 展开后是否显示收起按钮 | Boolean | false | true |
| closeText | 关闭时的提示文字 | String | 展开阅读全文 | \- |
| openText | 展开时的提示文字 | String | 收起 | \- |
| color | 提示文字的颜色 | String | #2979ff | \- |
| fontSize | 提示文字的大小，默认单位px | String | Number | 14 | \- |
| shadowStyle | 对阴影的自定义处理，对象形式 | Object | 见上方说明 | \- |
| textIndent | 段落首行缩进的字符个数 | String | 2em | \- |
| name | 用于在`open`和`close`事件中当作回调参数返回 | String | Number | \- | \- |

### [#](#methods) Methods

此方法如要通过ref手动调用

| 名称 | 说明 |
| --- | --- |
| init | 重新初始化组件内部高度计算过程，如果内嵌[u-parse](https://www.uviewui.com/components/parse.html)组件时可能需要用到 |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| open | 内容被展开时触发 | name - props中传入的`name`参数值 |
| close | 内容被收起时触发 | name - props中传入的`name`参数值 |

← [LoadMore 加载更多](https://www.uviewui.com/components/loadMore.html) [Gap 间隔槽](https://www.uviewui.com/components/gap.html) →


