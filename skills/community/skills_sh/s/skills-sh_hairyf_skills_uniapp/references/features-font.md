---
name: features-font
description: uni-app 字体与单位 loadFontFace、rpx2px、upx2px
---

# 字体与单位换算

## uni.loadFontFace(OBJECT)

动态加载字体。常用场景：字体图标、自定义字体渲染。参数：**family**（必填，字体名）、**source**（必填，字体地址，网络需 https；本地放 static 下）、**global**（是否全局，微信 2.10+ 支持，需在 App.vue 调用）、**desc**（style、weight、variant）、success/fail/complete。app-nvue 不支持，需用 DOM.addRule。各端对网络/本地字体支持见官方「font」文档。

## 单位换算

- **uni.rpx2px(rpx)**：将 rpx 值转为 px（数字）。用于在 JS 中根据设计稿 rpx 计算实际像素。
- **uni.upx2px(upx)**：将 upx 转为 px，**已废弃**，建议用 rpx2px。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/font
-->
