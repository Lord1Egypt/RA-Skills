---
name: "layout"
description: "Layout 布局 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Layout 布局 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/layout.html"
---

---

## [#](#layout-布局) Layout 布局 [![](https://www.uviewui.com/common/to_api.png)](#api)

通过基础的 12 分栏，迅速简便地创建布局

注意

如需实现类似宫格的布局，请使用uView的[Grid宫格组件](https://www.uviewui.com/components/grid.html)，可以设置角标，功能更完善和灵活

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

通过`col`组件的`span`设置需要分栏的比例

```
<template>
    <view class="u-page">
        <view class="u-demo-block">
            <text class="u-demo-block__title">基础使用</text>
            <view class="u-demo-block__content">
                <u-row customStyle="margin-bottom: 10px">
                    <u-col span="6">
                        <view class="demo-layout bg-purple-light"></view>
                    </u-col>
                    <u-col span="6">
                        <view class="demo-layout bg-purple"></view>
                    </u-col>
                </u-row>
                <u-row customStyle="margin-bottom: 10px">
                    <u-col span="4">
                        <view class="demo-layout bg-purple"></view>
                    </u-col>
                    <u-col span="4">
                        <view class="demo-layout bg-purple-light"></view>
                    </u-col>
                    <u-col span="4">
                        <view class="demo-layout bg-purple-dark"></view>
                    </u-col>
                </u-row>
                <u-row justify="space-between">
                    <u-col span="3">
                        <view class="demo-layout bg-purple"></view>
                    </u-col>
                    <u-col span="3">
                        <view class="demo-layout bg-purple-light"></view>
                    </u-col>
                    <u-col span="3">
                        <view class="demo-layout bg-purple"></view>
                    </u-col>
                    <u-col span="3">
                        <view class="demo-layout bg-purple-light"></view>
                    </u-col>
                </u-row>
            </view>
        </view>
    </view>
</template>

<style lang="scss">
    .wrap {
        padding: 12px;
    }

    .demo-layout {
        height: 25px;
        border-radius: 4px;
    }

    .bg-purple {
        background: #CED7E1;
    }

    .bg-purple-light {
        background: #e5e9f2;
    }

    .bg-purple-dark {
        background: #99a9bf;
    }
</style>
```

### [#](#分栏间隔) 分栏间隔

通过设置`row`组件的`gutter`参数，来指定每一栏之间的间隔(最终表现为左边内边距各为gutter/2)，默认间隔为0

```
<view class="u-demo-block__content">
    <u-row
            justify="space-between"
            gutter="10"
    >
        <u-col span="3">
            <view class="demo-layout bg-purple"></view>
        </u-col>
        <u-col span="3">
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
        <u-col span="3">
            <view class="demo-layout bg-purple"></view>
        </u-col>
        <u-col span="3">
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
    </u-row>
</view>

<style lang="scss">
    .wrap {
        padding: 12px;
    }

    .demo-layout {
        height: 25px;
        border-radius: 4px;
    }

    .bg-purple {
        background: #CED7E1;
    }

    .bg-purple-light {
        background: #e5e9f2;
    }

    .bg-purple-dark {
        background: #99a9bf;
    }
</style>
```

### [#](#混合布局) 混合布局

通过指定`col`组件的`span`属性，指定不同的值，达到不同的比例

```
<view class="u-demo-block__content">
    <u-row
        justify="space-between"
        gutter="10"
    >
        <u-col span="2">
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
        <u-col span="4">
            <view class="demo-layout bg-purple"></view>
        </u-col>
        <u-col span="6">
            <view class="demo-layout bg-purple-dark"></view>
        </u-col>
    </u-row>
</view>

<style lang="scss">
    .wrap {
        padding: 12px;
    }

    .demo-layout {
        height: 25px;
        border-radius: 4px;
    }

    .bg-purple {
        background: #CED7E1;
    }

    .bg-purple-light {
        background: #e5e9f2;
    }

    .bg-purple-dark {
        background: #99a9bf;
    }
</style>
```

### [#](#分栏偏移) 分栏偏移

通过指定`col`组件的`offset`属性可以指定分栏偏移的栏数。

```
<view class="u-demo-block__content">
    <u-row
            justify="space-between"
            customStyle="margin-bottom: 10px"
    >
        <u-col
                span="3"
                offset="3"
        >
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
        <u-col
                span="3"
                offset="3"
        >
            <view class="demo-layout bg-purple"></view>
        </u-col>
    </u-row>
    <u-row>
        <u-col span="3">
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
        <u-col
                span="3"
                offset="3"
        >
            <view class="demo-layout bg-purple"></view>
        </u-col>
    </u-row>
</view>
```

### [#](#对齐方式) 对齐方式

通过`row`组件的`justify`来对分栏进行灵活的对齐， 可选值为`start`(或`flex-start`)、`end`(或`flex-end`)、`center`、`around`(或`space-around`)、`between`(或`space-between`)， 其最终的表现类似于css的`justify-content`属性。

**注意**：由于持微信小程序编译后的特殊结构，此方式不支持微信小程序。

```
<view class="u-demo-block__content">
    <u-row
            justify="space-between"
            customStyle="margin-bottom: 10px"
    >
        <u-col
                span="3"
        >
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
        <u-col
                span="3"
        >
            <view class="demo-layout bg-purple"></view>
        </u-col>
    </u-row>
    <u-row>
        <u-col span="3">
            <view class="demo-layout bg-purple-light"></view>
        </u-col>
        <u-col
                span="3"
        >
            <view class="demo-layout bg-purple"></view>
        </u-col>
    </u-row>
</view>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsC/layout/layout.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsC/layout/layout.nvue)

### [#](#api) API

### [#](#row-props) Row Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| gutter | 栅格间隔，左右各为此值的一半，单位任意 | String | Number | 0 | \- |
| justify | 水平排列方式(微信小程序暂不支持) | String | `start`(或`flex-start`) | `end`(或`flex-end`) / `center` / `around`(或`space-around`) / `between`(或`space-between`) |
| align | 垂直排列方式 | String | center | top / bottom |

### [#](#col-props) Col Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| span | 栅格占据的列数，总12等分 | String | Number | 0 | 1-12 |
| offset | 分栏左边偏移，计算方式与`span`相同 | String | Number | 0 | \- |
| justify | 水平排列方式 | String | start | `start`(或`flex-start`)、`end`(或`flex-end`)、`center`、`around`(或`space-around`)、`between`(或`space-between`) |
| align | 垂直对齐方式 | String | stretch | `top`、`center`、`bottom`、`stretch` |
| textAlign | 文字水平对齐方式 | String | left | center / right |

### [#](#row-events) Row Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | `row`被点击 | \- |

### [#](#col-events) Col Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | `col`被点击，会阻止事件冒泡到`row` | \- |

← [Text 文本](https://www.uviewui.com/components/text.html) [Cell 单元格](https://www.uviewui.com/components/cell.html) →


