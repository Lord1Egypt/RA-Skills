---
name: "color"
description: "Color 色彩 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Color 色彩 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/color.html"
---

---

## [#](#color-色彩) Color 色彩

uView经过大量调试和研究，得出一套专有的调色板，在各个组件内部，使用统一的配色，为您的产品带来统一又鲜明的视觉效果。

注意

uView为了更好编写css，使用了scss预处理器，使用uView之前，请确认您的Hbuilder X已经安装了scss预处理器，一般情况下，相信您已经安装了。如果没有安装， 请在 Hbuilder X->工具->插件安装 中找到找到"scss/sass编译"安装即可，安装完毕如果不生效，请重启Hbuilder X。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#主题色) 主题色

`primary`，`success`，`error`，`warning`，`info`是uView的主题色，他们给人在视觉感受上分别对应于蓝色，绿色，红色，黄色，灰色。 而他们又有对应的`disabled`、`dark`和`light`状态，分别表示对应的禁止，加深和变浅的对应颜色。举例uView的`button`组件来说：

1.  设置`type`参数为`primary`时，按钮显示蓝色。
2.  按钮被按下时，使用的是`primary`的加深颜色，也即`dark`状态。
3.  按钮设置为镂空状态(`plain`为`true`)时，背景色为`primary`的变浅颜色，也即`light`状态。
4.  按钮处于禁止状态时，使用的是`primary`的稍浅颜色，也即`disabled`状态。

### [#](#主色) 主色

蓝色作为uView主色调，表示一种鲜明，积极的态度

Primary
#2979ff

Dark
#2b85e4

Disabled
#a0cfff

Light
#ecf5ff

我们在全局样式中，通过`scss`提供了对应的颜色变量名，方便您在任何可写css的地方，调用这些变量，如下：

```

$u-primary: #3c9cff;
$u-warning: #f9ae3d;
$u-success: #5ac725;
$u-error: #f56c6c;
$u-info: #909399;

.title {
	color: $u-primary;
	......
}
```

### [#](#辅助色) 辅助色

除了主色外的场景色，需要在不同的场景中使用，如绿色代表成功，红色代表错误，黄色代表警示。

Error
#fa3534

Dark
#dd6161

Disabled
#fab6b6

Light
#fef0f0

Warning
#ff9900

Dark
#f29100

Disabled
#fcbd71

Light
#fdf6ec

Success
#19be6b

Dark
#18b566

Disabled
#71d5a1

Light
#dbf1e1

Info
#909399

Dark
#82848a

Disabled
#c8c9cc

Light
#f4f4f5

我们在全局样式中，通过`scss`提供了对应的颜色变量名，方便您在任何可写css的地方，调用这些变量，如下：

```

$u-primary: #3c9cff;
$u-primary-dark: #398ade;
$u-primary-disabled: #9acafc;
$u-primary-light: #ecf5ff;

$u-warning: #f9ae3d;
$u-warning-dark: #f1a532;
$u-warning-disabled: #f9d39b;
$u-warning-light: #fdf6ec;

$u-success: #5ac725;
$u-success-dark: #53c21d;
$u-success-disabled: #a9e08f;
$u-success-light: #f5fff0;

$u-error: #f56c6c;
$u-error-dark: #e45656;
$u-error-disabled: #f7b2b2;
$u-error-light: #fef0f0;

$u-info: #909399;
$u-info-dark: #767a82;
$u-info-disabled: #c4c6c9;
$u-info-light: #f4f4f5;

.title {
	color: $u-type-info;
	......
}
```

### [#](#文字颜色) 文字颜色

uView中，分别提炼了4种用于文字颜色，分别是：主要文字、常规文字、次要文字、占位文字颜色。

-   主要文字颜色一般用于内容的标题等，如新闻列表的标题
-   常规文字颜色一般用于内容的主体，如新闻列表的概要
-   次要文字颜色一般用于内容的提示部分，如新闻列表底部的时间，评论数量的提示文字
-   占位文字颜色属于更浅的灰色，看场景选择使用

主要文字
#303133

常规文字
#606266

次要文字
#909399

占位文字
#c0c4cc

```

$u-main-color: #303133;
$u-content-color: #606266;
$u-tips-color: #909193;
$u-light-color: #c0c4cc;
$u-border-color: #dadbde;
$u-bg-color: #f3f4f6;
$u-disabled-color: #c8c9cc;

.title {
	color: $u-main-color;
}
```

### [#](#背景颜色) 背景颜色

uView中，定义了一个背景颜色，如下：

背景颜色
#f3f4f6

我们在全局样式中，通过`scss`提供了对应的颜色变量名，方便您在任何可写css的地方，调用这个变量，如下：

```

$u-bg-color: #f3f4f6;

.title {
	color: $u-bg-color;
}
```

### [#](#边框颜色) 边框颜色

uView自定义了一个边框的颜色，值为`#e4e7ed`，如果想使用，如下：

```

$u-border-color: #e4e7ed;

.item {
	border: 1px solid $u-border-color;
}
```

← [2.X 常见问题整理 (opens new window)](https://www.kancloud.cn/uview/uview-ui_v2/2593659) [Icon 图标](https://www.uviewui.com/components/icon.html) →


