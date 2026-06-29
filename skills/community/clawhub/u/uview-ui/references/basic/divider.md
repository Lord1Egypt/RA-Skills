---
name: "divider"
description: "Divider 分割线 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Divider 分割线 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/divider.html"
---

---

## [#](#divider-分割线) Divider 分割线 [![](https://www.uviewui.com/common/to_api.png)](#api)

区隔内容的分割线，一般用于页面底部"没有更多"的提示。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

文字内容通过`text`传入

```
<u-divider text="分割线"></u-divider>
```

### [#](#设置虚线) 设置虚线

可以通过`dashed`指定虚线

```
<u-divider text="分割线" :dashed="true"></u-divider>
```

### [#](#设置细线) 设置细线

可以通过`hairline`指定细线

```
<u-divider text="分割线" :hairline="true"></u-divider>
```

### [#](#设置以点代替文字) 设置以点代替文字

可以通过`dot`指定以点代替文字

```
<u-divider text="分割线" :dot="true"></u-divider>
```

### [#](#设置文本靠左靠右) 设置文本靠左靠右

可以通过`textPosition`指定文字靠左靠右

```
<u-divider text="靠左" textPosition="left"></u-divider>
<u-divider text="靠右" textPosition="right"></u-divider>
```

### [#](#设置文本颜色和线条颜色) 设置文本颜色和线条颜色

可以通过`textColor`和`lineColor`指定文字刚线条颜色

```
<u-divider
        text="分割线"
        textColor="#2979ff"
        lineColor="#ff0000"
></u-divider>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/divider/divider.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/divider/divider.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| dashed | 是否虚线 | Boolean | false | true |
| hairline | 是否细线 | Boolean | true | false |
| dot | 是否以点替代文字，优先于text字段起作用 | Boolean | false | true |
| textPosition | 内容文本的位置 | String | center | left、right |
| text | 文本内容 | String | Number | \- | \- |
| textSize | 文本大小 | String | Number | 14 | \- |
| textColor | 文本颜色 | String | #909399 | \- |
| lineColor | 线条颜色 | String | #dcdfe6 | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| click | divider组件被点击时触发 | \- | \- |

← [Sticky 吸顶](https://www.uviewui.com/components/sticky.html) [Tabbar 底部导航栏](https://www.uviewui.com/components/tabbar.html) →


