---
name: "icon"
description: "Icon 图标 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Icon 图标 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/icon.html"
---

---

## [#](#icon-图标) Icon 图标 [![](https://www.uviewui.com/common/to_api.png)](#api)

基于字体的图标集，包含了大多数常见场景的图标。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

注意

因为在`nvue`下暂时无法解决自定义图标的问题，所以此功能暂缓推出。

[icon 下载地址](https://www.uviewui.com/components/resource.html)

通过`<u-icon>`形式来调用，设置`name`参数为图标名即可。其中`color`默认为`#606266`，`size`默认为`16px`

```
<u-icon name="photo"></u-icon>
```

### [#](#修改图标的样式) 修改图标的样式

-   通过`color`参数修改图标的颜色
-   通过`size`参数修改图标的大小，单位为 px

```
<u-icon name="photo" color="#2979ff" size="28"></u-icon>
```

### [#](#图片图标) 图片图标

这里说的图片图标，指的是小图标，起作用定位为"icon"图标作用，而非大尺寸的图片展示场景，理论上，这个小图标应该为`png`格式的正方形图标。

上面说到，给组件的`name`参数传入一个图片的名称即可显示字体图标，这些名称中不能带有`/`斜杠符号，否则会被认为是传入了图片图标，同时，`size`参数 也被设置为这个图片图标的宽度，由于是图片，诸如颜色`color`等参数都会失效。

```
<u-icon
  label="uView"
  size="40"
  name="https://uviewui.com/example/button.png"
></u-icon>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/icon/icon.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/icon/icon.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| name | 图标名称，见示例图标集，如名称带有`/`，会被认为是图片图标 | String | \- | \- |
| color | 图标颜色 | String | color\['u-content-color'\] | \- |
| size | 图标字体大小，单位默认 px | String | Number | 16px | \- |
| bold | 是否显示粗体 | Boolean | false | \- |
| index | 一个用于区分多个图标的值，点击图标时通过`click`事件传出 | String | Number | \- | \- |
| hoverClass | 图标按下去的样式类，用法同 uni 的`view`组件的`hover-class`参数，详见：[hover-class (opens new window)](https://uniapp.dcloud.io/component/view) | String | \- | \- |
| customPrefix（暂不可用） | 自定义字体图标库时，需要写上此值，详见：[扩展自定义图标库 (opens new window)](https://www.uviewui.com/guide/customIcon.html) | String | uicon | \- |
| label | 图标右侧/下方的 label 文字 | String | Number | \- | \- |
| labelPos | `label`相对于图标的位置 | String | right | bottom / top / left |
| labelSize | `label`字体大小，单位默认 px | String | Number | 15px | \- |
| labelColor | `label`字体颜色 | String | color\['u-content-color'\] | \- |
| space | `label`与图标的距离，单位默认 px | String | Number | 3px | \- |
| imgMode | 图片裁剪、缩放的模式，image 组件原生属性，详见：[image (opens new window)](https://uniapp.dcloud.io/component/image?id=image) | String | \- | \- |
| width | `name`为图片路径时图片的宽度，单位默认 px | String | Number | \- | \- |
| height | `name`为图片路径时图片的高度，单位默认 px | String | Number | \- | \- |
| top | 图标到顶部的距离，如果某些场景，如果图标没有垂直居中，可以调整此参数，单位默认 px | String | Number | 0 | \- |
| stop | 是否阻止事件传播 | Boolean | false | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| click | 点击图标时触发 | index: 通过`props`传递的`index`值 | \- |

### [#](#图标集) 图标集

level

woman

man

arrow-left-double

arrow-right-double

chat

chat-fill

red-packet

red-packet-fill

order

checkbox-mark

arrow-up-fill

arrow-down-fill

backspace

photo

photo-fill

lock

lock-fill

lock-open

lock-opened-fill

hourglass

hourglass-half-fill

home

home-fill

fingerprint

cut

star

star-fill

share

share-fill

volume

volume-fill

volume-off

volume-off-fill

trash

trash-fill

rewind-right

rewind-right-fill

rewind-left

rewind-left-fill

shopping-cart

shopping-cart-fill

question

question-circle

question-circle-fill

plus

plus-circle

plus-circle-fill

tags

tags-fill

pause

pause-circle

pause-circle-fill

play-circle

play-circle-fill

map

map-fill

phone

phone-fill

list

list-dot

man-delete

man-add

man-add-fill

person-delete-fill

info

info-circle

info-circle-fill

minus

minus-circle

minus-circle-fill

mic

mic-off

grid

grid-fill

eye

eye-fill

eye-off

file-text

file-text-fill

edit-pen

edit-pen-fill

email

email-fill

download

checkmark

checkmark-circle

checkmark-circle-fill

clock

clock-fill

close

close-circle

close-circle-fill

calendar

calendar-fill

car

car-fill

bell

bell-fill

bookmark

bookmark-fill

attach

play-right

play-right-fill

play-left

play-left-fill

error

error-circle

error-circle-fill

wifi

wifi-off

skip-back-left

skip-forward-right

search

setting

setting-fill

more-dot-fill

more-circle

more-circle-fill

bag

bag-fill

arrow-upward

arrow-downward

arrow-leftward

arrow-rightward

arrow-up

arrow-down

arrow-left

arrow-right

rmb

rmb-circle

rmb-circle-fill

thumb-up

thumb-up-fill

thumb-down

thumb-down-fill

coupon

coupon-fill

kefu-ermai

server-fill

server-man

scan

warning

warning-fill

google

google-circle-fill

chrome-circle-fill

ie

IE-circle-fill

github-circle-fill

android-fill

android-circle-fill

apple-fill

camera

camera-fill

pushpin

pushpin-fill

minus-square-fill

plus-square-fill

heart

heart-fill

reload

account

account-fill

minus-people-fill

plus-people-fill

integral

integral-fill

zhihu

zhihu-circle-fill

gift

gift-fill

zhifubao

zhifubao-circle-fill

weixin-fill

weixin-circle-fill

twitter

twitter-circle-fill

taobao

taobao-circle-fill

weibo

weibo-circle-fill

qq-fill

qq-circle-fill

moments

moments-circel-fill

qzone

qzone-circle-fill

facebook

facebook-circle-fill

baidu

baidu-circle-fill

share-square

← [Color 色彩](https://www.uviewui.com/components/color.html) [Image 图片](https://www.uviewui.com/components/image.html) →


