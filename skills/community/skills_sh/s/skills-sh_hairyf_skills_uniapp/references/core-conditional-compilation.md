---
name: core-conditional-compilation
description: uni-app 条件编译 #ifdef/#ifndef、平台标识、多端差异化代码
---

# 条件编译

用特殊注释在编译时按平台保留/剔除代码，避免运行时 if-else 和二次改包。支持 .vue/.nvue/.uvue、.js/.uts、.css、pages.json、.scss/.less/.ts 等。

## 写法

- **#ifdef %PLATFORM%**：仅在该平台存在
- **#ifndef %PLATFORM%**：除该平台外均存在
- **#endif**：结束
- 支持 **||**（或）、**&&**（且）、**!**（非），如 `#ifdef H5 || MP-WEIXIN`、`#ifdef APP && !VUE3-VAPOR`

注释语法：js/uts 用 `//`，css 用 `/* */`，vue 模板用 `<!-- -->`。

## 常用平台标识

| 标识 | 说明 |
|------|------|
| APP-PLUS / APP | App（js 引擎版） |
| APP-NVUE / APP-PLUS-NVUE | App nvue 页面 |
| APP-ANDROID / APP-IOS / APP-HARMONY | App 各系统 |
| H5 / WEB | H5（推荐用 WEB） |
| MP-WEIXIN / MP-ALIPAY / MP-BAIDU / MP-TOUTIAO / MP-LARK / MP-QQ / MP-KUAISHOU / MP-JD / MP-XHS / MP-HARMONY | 各小程序 |
| MP | 任意小程序 |
| VUE2 / VUE3 | 区分 Vue 版本（js 引擎版） |
| UNI-APP-X | uni-app x 项目 |

未定义或写错的平台名：`#ifdef` 不生效，`#ifndef` 生效。需保证编译前后语法正确（如 json 无多余逗号、js 无重复 import）。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/platform
-->
