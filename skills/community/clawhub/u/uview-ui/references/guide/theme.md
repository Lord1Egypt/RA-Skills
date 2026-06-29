---
name: "theme"
description: "主题指南 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 主题指南 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/guide/theme.html"
---

---

## [#](#自定义主题) 自定义主题

uView目前可以自定主题色，字体颜色，边框颜色等，所有组件内部的样式，都基于同一套主题，比如您修改了`primary`主题色，所有用到了`primary`颜色 的组件都会受影响。

### [#](#教程) 教程

1.  可以在打开的颜色拾取器中输入或者选择颜色，再点"确定"按钮即可。
2.  颜色配置完后，在页面底部下载文件，会得到一个名为`uview.theme.scss`的文件。
3.  将文件复制到项目的公共目录(视情况而定)中，再在项目根目录的`uni.scss`中引入即可。
4.  删除`uni.scss`文件中原来引入的`@import 'uview-ui/theme.scss';`(旧的内置主题文件引入语句)。
5.  重新编译项目或者重启HX即可生效。

### [#](#主题色) 主题色

目前有五个主题色，每个主题色又分别有对应的`light`(淡色)、`dark`(深色)、`disabled`(禁止状态时的颜色)：

primary

#2979ff

清空 确定

success

#19be6b

清空 确定

error

#fa3534

清空 确定

warning

#ff9900

清空 确定

info

#909399

清空 确定

primary-dark

#2b85e4

清空 确定

success-dark

#18b566

清空 确定

error-dark

#dd6161

清空 确定

warning-dark

#f29100

清空 确定

info-dark

#82848a

清空 确定

primary-disabled

#a0cfff

清空 确定

success-disabled

#71d5a1

清空 确定

error-disabled

#fab6b6

清空 确定

warning-disabled

#fcbd71

清空 确定

info-disabled

#c8c9cc

清空 确定

primary-light

#ecf5ff

清空 确定

success-light

#dbf1e1

清空 确定

error-light

#fef0f0

清空 确定

warning-light

#fdf6ec

清空 确定

info-light

#f4f4f5

清空 确定

### [#](#文字颜色) 文字颜色

内置的文字颜色有：主要文字、常规文字，次要文字、占位文字颜色，如需更详细的，详见：[Color 色彩](https://www.uviewui.com/components/color.html)章节。

main-color

#303133

清空 确定

content-color

#606266

清空 确定

tips-color

#909399

清空 确定

light-color

#c0c4cc

清空 确定

### [#](#边框颜色) 边框颜色

uView所有组件边框相关的(特别说明的除外)，用的都是这一个颜色。

border-color

#e4e7ed

清空 确定

### [#](#背景颜色) 背景颜色

这个颜色是uView推荐的背景色，目前内置组件中使用的场景不多。

bg-color

#f3f4f6

清空 确定

### [#](#input边框颜色) Input边框颜色

此颜色用于在`u-input`组件显示边框时的边框颜色。

form-item-border-color

#dcdfe6

清空 确定

重置 下载主题文件


