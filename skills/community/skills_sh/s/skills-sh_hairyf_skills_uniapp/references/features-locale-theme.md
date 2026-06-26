---
name: features-locale-theme
description: uni-app 语言与主题 getLocale、setLocale、onLocaleChange、onThemeChange
---

# 语言与主题

## 语言（国际化）

- **uni.getLocale()**：获取当前设置的语言；未设置时按系统语言自动选择。
- **uni.setLocale(locale)**：设置当前语言，需符合 BCP47；仅可设为框架内置或自定义扩展语言，见「国际化」文档。
- **uni.onLocaleChange(callback)**：监听应用语言切换。元服务不支持。

## 系统主题

- **uni.onThemeChange(CALLBACK)**：监听系统主题变化（如深色/浅色）。回调参数含 theme。部分平台支持。
- **uni.offThemeChange(CALLBACK)**：取消监听。需在页面卸载或业务结束时调用。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/locale
- https://uniapp.dcloud.net.cn/api/system/theme
- https://uniapp.dcloud.net.cn/tutorial/i18n
-->
