---
name: "changelog"
description: "更新日志 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs 更新日志 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/changelog.html"
---

---

## [#](#更新日志) 更新日志

-   ## 2.0.38

    `2024-10-29`

    -   修复 修复\`picker\`组件和\`datetime-picker\`组件的头条小程序循环引用问题 [#1040](https://github.com/umicro/uView2.0/pull/1040)
    -   修复 修复\`image\`组件的\`bgColor\`属性不生效问题 [#1076](https://github.com/umicro/uView2.0/pull/1076)
    -   修复 修复\`textarea\`组件部分回调事件参数丢失问题 [#797](https://github.com/umicro/uView2.0/pull/797)
    -   修复 修复\`input\`组件部分回调事件参数丢失问题
    -   添加 \`datetime-picker\`组件支持\`immediateChange\`属性 [#1098](https://github.com/umicro/uView2.0/pull/1098)
    -   修复 修复\`datetime-picker\`组件\`v-model\`绑定异步设置无效问题 [#803](https://github.com/umicro/uView2.0/pull/803)
    -   修复 修复\`popup\`组件设置\`duration\`属性为字符串值时，遮罩的打开、关闭很缓慢问题 [#1097](https://github.com/umicro/uView2.0/pull/1097)
    -   修复 修复\`radio\`参数\`iconColor\`属性不生效问题 [#941](https://github.com/umicro/uView2.0/pull/941)
    -   修复 修复\`tooltip\`组件\`size\`属性不生效的问题 [#1070](https://github.com/umicro/uView2.0/pull/1070)
    -   修复 修复\`image\`组件当\`src\`为空时，loading状态问题 [#910](https://github.com/umicro/uView2.0/pull/910)
    -   修复 其他一些修复

-   ## 2.0.37

    `2024-03-17`

    -   修复 表单校验trigger触发器参数无效问题 [#546](https://github.com/umicro/uView2.0/pull/546)
    -   修复 u-input组件的password属性在动态切换为false时失效的问题 [#1009](https://github.com/umicro/uView2.0/pull/1009)
    -   添加 添加微信小程序用户同意隐私协议事件回调 [#992](https://github.com/umicro/uView2.0/pull/992)
    -   修复 修复支付宝小程序picker样式问题 [#955](https://github.com/umicro/uView2.0/pull/955)
    -   添加 u-modal添加duration字段控制动画过度时间 [#1023](https://github.com/umicro/uView2.0/pull/1023)
    -   修复 修复picker lastIndex异常导致的column异常问题 [#1028](https://github.com/umicro/uView2.0/pull/1028)
    -   添加 tabs增加长按事件支持 [#1029](https://github.com/umicro/uView2.0/pull/1029)
    -   修复 修复u-avatar square属性在小程序open-data下无效问题 [#1030](https://github.com/umicro/uView2.0/pull/1030)
    -   修复 其他一些修复

-   ## 2.0.36

    `2023-03-27`

    -   优化 重构deepClone & deepMerge
    -   修复 路由在部分情况下不能跳转问题
    -   修复 其他一些修复

-   ## 2.0.35

    `2022-10-29`

    -   修复 修复$u.route()方法type参数无效问题

-   ## 2.0.34

    `2022-09-24`

    -   修复 修复route方法调用可能报错的问题
    -   添加 u-input、u-textarea增加ignoreCompositionEvent属性
    -   修复 修复u-no-network组件z-index无效的问题
    -   修复 修复textarea组件在h5上confirmType=""报错的问题
    -   优化 u-rate适配nvue
    -   优化 优化验证手机号码的正则表达式(根据工信部发布的《电信网编号计划（2017年版）》进行修改。)
    -   添加 form-item添加labelPosition属性
    -   修复 u-calendar修复maxDate设置为当前日期，并且当前时间大于08：00时无法显示日期列表的问题 [#724](https://github.com/umicro/uView2.0/pull/724)
    -   添加 u-radio增加一个默认插槽用于自定义修改label内容 [#680](https://github.com/umicro/uView2.0/pull/680)
    -   修复 修复timeFormat函数在safari重的兼容性问题 [#664](https://github.com/umicro/uView2.0/pull/664)

-   ## 2.0.33

    `2022-06-17`

    -   修复 修复loadmore组件lineColor类型错误问题
    -   修复 修复u-parse组件imgtap、linktap不生效问题

-   ## 2.0.32

    `2022-06-16`

    -   添加 u-loadmore新增自定义颜色、虚/实线
    -   修复 修复u-swiper-action组件部分平台不能上下滑动的问题
    -   修复 修复u-list回弹问题
    -   修复 修复notice-bar组件动画在低端安卓机可能会抖动的问题
    -   添加 u-loading-page添加控制图标大小的属性iconSize
    -   修复 修复u-tooltip组件color参数不生效的问题
    -   修复 修复u--input组件使用blur事件输出为undefined的bug
    -   添加 u-code-input组件新增键盘弹起时，是否自动上推页面参数adjustPosition
    -   修复 修复image组件load事件无回调对象问题
    -   修复 修复button组件loadingSize设置无效问题
    -   修复 其他修复

-   ## 2.0.31

    `2022-04-19`

    -   修复 修复upload在vue页面上传成功后没有成功标志的问题
    -   修复 解决演示项目中微信小程序模拟上传图片一直出于上传中问题
    -   修复 修复u-code-input组件在nvue页面编译到app平台上光标异常问题（app去除此功能）
    -   修复 修复actionSheet组件标题关闭按钮点击事件名称错误的问题
    -   修复 其他修复

-   ## 2.0.30

    `2022-04-04`

    -   添加 u-rate增加readonly属性
    -   添加 tabs滑块支持设置背景图片
    -   修复 修复u-subsection mode为subsection时，滑块样式不正确的问题
    -   添加 u-code-input添加光标效果动画
    -   修复 修复popup的open事件不触发的问题
    -   修复 修复u-flex-column无效的问题
    -   修复 修复u-datetime-picker索引在特定场合异常问题
    -   修复 修复u-datetime-picker最小时间字符串模板错误问题
    -   添加 u-swiper添加m3u8验证
    -   优化 u-swiper修改判断image和video逻辑
    -   修复 修复swiper无法使用本地图片问题，增加type参数
    -   修复 修复u-row-notice格式错误问题
    -   修复 修复u-switch组件当unit为rpx时,nodeStyle消失的问题
    -   修复 修复datetime-picker组件showToolbar与visibleItemCount属性无效的问题
    -   修复 修复upload组件条件编译位置判断错误，导致previewImage属性设置为false时，整个组件都会被隐藏的问题
    -   修复 修复u-checkbox-group设置shape属性无效的问题
    -   修复 修复u-upload的capture传入字符串的时候不生效的问题
    -   修复 修复u-action-sheet组件，关闭事件逻辑错误的问题
    -   修复 修复u-list触顶事件的触发错误的问题
    -   修复 修复u-text只有手机号可拨打的问题
    -   修复 修复u-textarea不能换行的问题
    -   修复 其他修复

-   ## 2.0.29

    `2022-03-13`

    -   修复 修复u--text组件设置decoration属性未生效的问题
    -   修复 修复u-datetime-picker使用formatter后返回值不正确
    -   修复 修复u-datetime-picker intercept 可能为undefined
    -   修复 修复已设置单位 uni..config.unit = 'rpx'时，线型指示器 transform 的位置翻倍，导致指示器超出宽度
    -   修复 修复mixin中bem方法生成的类名在支付宝和字节小程序中失效
    -   修复 修复默认值传值为空的时候，打开u-datetime-picker报错，不能选中第一列时间的bug
    -   修复 修复u-datetime-picker使用formatter后返回值不正确
    -   修复 修复u-image组件loading无效果的问题
    -   修复 修复config.unit属性设为rpx时，导航栏占用高度不足导致塌陷的问题
    -   修复 修复u-datetime-picker组件itemHeight无效问题
    -   修复 其他修复

-   ## 2.0.28

    `2022-02-22`

    -   添加 search组件新增searchIconSize属性
    -   修复 兼容Safari/Webkit中传入时间格式如2022-02-17 12:00:56
    -   修复 修复text value.js 判断日期出format错误问题
    -   修复 priceFormat格式化金额出现精度错误
    -   修复 priceFormat在部分情况下出现精度损失问题
    -   修复 优化表单rules提示
    -   修复 修复avatar组件src为空时，展示状态不对
    -   修复 其他修复

-   ## 2.0.27

    `2022-01-28`

    -   修复 样式修复

-   ## 2.0.25

    `2022-01-27`

    -   添加 添加$u.setConfig()方法，可设置uView内置的config, props, zIndex, color属性
    -   优化 优化遗留的通过正则判断rpx单位的问题
    -   修复 修复text组件mode=price时，可能会导致精度错误的问题
    -   修复 修复$u.addUnit()对配置默认单位可能无效的问题
    -   修复 其他修复

-   ## 2.0.24

    `2022-01-25`

    -   修复 修复swiper在current指定非0时缩放有误
    -   修复 修复u-icon添加stop属性的时候报错
    -   优化 优化遗留的通过正则判断rpx单位的问题
    -   优化 优化Layout布局 vue使用gutter时，会超出固定区域
    -   优化 优化search组件高度单位问题（rpx -> px）
    -   修复 修复u-image slot 加载和错误的图片失去了高度
    -   修复 修复u-index-list中footer插槽与header插槽存在性判断错误
    -   修复 修复部分机型下u-popup关闭时会闪烁
    -   修复 修复u-image在nvue-app下失去宽高
    -   修复 修复u-popup运行报错
    -   修复 修复u-tooltip报错
    -   修复 修复box-sizing在app下的警告
    -   修复 修复u-navbar在小程序中报运行时错误
    -   修复 其他修复

-   ## 2.0.0

    `2021-11-15`

    -   添加 包含50+组件
    -   添加 众多JS工具库

← [对比 1.X](https://www.uviewui.com/components/diff1.x.html) [升级指南](https://www.uviewui.com/components/changeGuide.html) →


