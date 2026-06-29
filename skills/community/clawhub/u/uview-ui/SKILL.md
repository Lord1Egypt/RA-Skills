---
name: uview-ui
description: "uView UI uni-app component library for Vue 2. Invoke when developing uni-app pages with Vue 2, using uView components (u-button, u-input, u-form, etc.), or needing UI elements like forms, buttons, modals, toasts, navigation for multi-platform apps."
---

# uView UI 组件库技能

uView UI，是全面兼容 nvue 的 uni-app 生态框架，基于 Vue 2.x，全面的组件和便捷的工具让 uni-app 开发信手拈来。

## 触发条件

**在以下场景中自动调用此技能：**

1. 开发 uni-app 页面时（Vue 2.x）
2. 使用 `u-` 前缀的组件时（如 `u-button`, `u-input`, `u-form` 等）
3. 需要表单、按钮、弹窗、提示、导航等移动端 UI 组件时
4. 需要使用 uView UI 工具函数（防抖、节流、深拷贝、时间格式化等）时
5. 需要 uView UI 的布局系统（`u-row`, `u-col`）或常用页面模板时
6. 需要参考 uni-app Vue 2.x 组件库的 API 属性（Props）、事件（Events）、插槽（Slots）时

## 组件快速索引

### 基础组件
| 组件 | 说明 | 文档 |
|------|------|------|
| button | Button 按钮 | [button](references/basic/button.md) |
| icon | Icon 图标 | [icon](references/basic/icon.md) |
| image | Image 图片 | [image](references/basic/image.md) |
| text | Text 文本 | [text](references/basic/text.md) |
| layout | Layout 布局 | [layout](references/basic/layout.md) |
| cell | Cell 单元格 | [cell](references/basic/cell.md) |
| badge | Badge 徽标数 | [badge](references/basic/badge.md) |
| tag | Tag 标签 | [tag](references/basic/tag.md) |
| avatar | Avatar 头像 | [avatar](references/basic/avatar.md) |
| link | Link 超链接 | [link](references/basic/link.md) |
| color | Color 色彩 | [color](references/basic/color.md) |
| loadingIcon | LoadingIcon 加载动画 | [loadingIcon](references/basic/loadingIcon.md) |
| loadingPage | LoadingPage 加载页 | [loadingPage](references/basic/loadingPage.md) |
| gap | Gap 间隔槽 | [gap](references/basic/gap.md) |
| line | Line 线条 | [line](references/basic/line.md) |
| divider | Divider 分割线 | [divider](references/basic/divider.md) |

### 表单组件
| 组件 | 说明 | 文档 |
|------|------|------|
| form | Form 表单 | [form](references/form/form.md) |
| input | Input 输入框 | [input](references/form/input.md) |
| textarea | Textarea 文本域 | [textarea](references/form/textarea.md) |
| checkbox | Checkbox 复选框 | [checkbox](references/form/checkbox.md) |
| radio | Radio 单选框 | [radio](references/form/radio.md) |
| switch | Switch 开关选择器 | [switch](references/form/switch.md) |
| slider | Slider 滑动选择器 | [slider](references/form/slider.md) |
| numberBox | NumberBox 步进器 | [numberBox](references/form/numberBox.md) |
| rate | Rate 评分 | [rate](references/form/rate.md) |
| picker | Picker 选择器 | [picker](references/form/picker.md) |
| datetimePicker | DatetimePicker 时间选择器 | [datetimePicker](references/form/datetimePicker.md) |
| calendar | Calendar 日历 | [calendar](references/form/calendar.md) |
| upload | Upload 上传 | [upload](references/form/upload.md) |
| search | Search 搜索 | [search](references/form/search.md) |
| keyboard | Keyboard 键盘 | [keyboard](references/form/keyboard.md) |
| code | Code 验证码输入框 | [code](references/form/code.md) |

### 数据展示组件
| 组件 | 说明 | 文档 |
|------|------|------|
| grid | Grid 宫格布局 | [grid](references/display/grid.md) |
| list | List 列表 | [list](references/display/list.md) |
| album | Album 相册 | [album](references/display/album.md) |
| swiper | Swiper 轮播图 | [swiper](references/display/swiper.md) |
| skeleton | Skeleton 骨架屏 | [skeleton](references/display/skeleton.md) |
| empty | Empty 内容为空 | [empty](references/display/empty.md) |
| collapse | Collapse 折叠面板 | [collapse](references/display/collapse.md) |
| steps | Steps 步骤条 | [steps](references/display/steps.md) |
| indexList | IndexList 索引列表 | [indexList](references/display/indexList.md) |
| lineProgress | LineProgress 线形进度条 | [lineProgress](references/display/lineProgress.md) |
| countDown | CountDown 倒计时 | [countDown](references/display/countDown.md) |
| countTo | CountTo 数字滚动 | [countTo](references/display/countTo.md) |
| parse | Parse 富文本解析器 | [parse](references/display/parse.md) |
| codeInput | CodeInput 验证码输入 | [codeInput](references/display/codeInput.md) |
| loadMore | LoadMore 加载更多 | [loadMore](references/display/loadMore.md) |
| readMore | ReadMore 展开阅读更多 | [readMore](references/display/readMore.md) |
| sticky | Sticky 吸顶 | [sticky](references/display/sticky.md) |

### 反馈组件
| 组件 | 说明 | 文档 |
|------|------|------|
| toast | Toast 消息提示 | [toast](references/feedback/toast.md) |
| modal | Modal 模态框 | [modal](references/feedback/modal.md) |
| popup | Popup 弹出层 | [popup](references/feedback/popup.md) |
| actionSheet | ActionSheet 操作菜单 | [actionSheet](references/feedback/actionSheet.md) |
| alert | Alert 警告提示 | [alert](references/feedback/alert.md) |
| notify | Notify 消息提示 | [notify](references/feedback/notify.md) |
| noticeBar | NoticeBar 滚动通知 | [noticeBar](references/feedback/noticeBar.md) |
| tooltip | Tooltip 长按提示 | [tooltip](references/feedback/tooltip.md) |
| swipeAction | SwipeAction 滑动单元格 | [swipeAction](references/feedback/swipeAction.md) |
| overlay | Overlay 遮罩层 | [overlay](references/feedback/overlay.md) |
| noNetwork | NoNetwork 无网络提示 | [noNetwork](references/feedback/noNetwork.md) |
| scrollList | ScrollList 横向滚动列表 | [scrollList](references/feedback/scrollList.md) |

### 导航组件
| 组件 | 说明 | 文档 |
|------|------|------|
| navbar | Navbar 自定义导航栏 | [navbar](references/navigation/navbar.md) |
| tabbar | Tabbar 底部导航栏 | [tabbar](references/navigation/tabbar.md) |
| tabs | Tabs 标签 | [tabs](references/navigation/tabs.md) |
| subsection | Subsection 分段器 | [subsection](references/navigation/subsection.md) |
| backTop | BackTop 返回顶部 | [backTop](references/navigation/backTop.md) |

### 其他组件
| 组件 | 说明 | 文档 |
|------|------|------|
| transition | Transition 动画 | [transition](references/others/transition.md) |

## 工具函数快速索引

| 工具 | 说明 | 文档 |
|------|------|------|
| http | Http 请求 | [http](references/js/http.md) |
| debounce | 节流防抖 | [debounce](references/js/debounce.md) |
| time | 时间格式化 | [time](references/js/time.md) |
| route | 路由跳转 | [route](references/js/route.md) |
| object | 对象操作 | [object](references/js/object.md) |
| test | 规则校验 | [test](references/js/test.md) |
| queryParams | 对象转URL参数 | [queryParams](references/js/queryParams.md) |
| guid | 全局唯一标识符 | [guid](references/js/guid.md) |
| random | 随机数值 | [random](references/js/random.md) |
| randomArray | 数组乱序 | [randomArray](references/js/randomArray.md) |
| trim | 去除空格 | [trim](references/js/trim.md) |
| color | 颜色值 | [color](references/js/js-color.md) |
| colorSwitch | 颜色转换 | [colorSwitch](references/js/colorSwitch.md) |
| getRect | 节点布局信息 | [getRect](references/js/getRect.md) |
| mpShare | 小程序分享 | [mpShare](references/js/mpShare.md) |
| fastUse | 便捷工具 | [fastUse](references/js/fastUse.md) |

## 指南文档

| 指南 | 说明 | 文档 |
|------|------|------|
| design | 设计指南 | [design](references/guide/design.md) |
| demo | 示例指南 | [demo](references/guide/demo.md) |
| theme | 主题指南 | [theme](references/guide/theme.md) |
| customIcon | 自定义图标指南 | [customIcon](references/guide/customIcon.md) |
| customStyle | 自定义样式指南 | [customStyle](references/guide/customStyle.md) |
| i18n | 国际化指南 | [i18n](references/guide/i18n.md) |
| note | 注意事项 | [note](references/guide/note.md) |
| faq | 常见问题 | [faq](references/guide/faq.md) |
| intro | 介绍 | [intro](references/dev-guide/intro.md) |
| install | 安装 | [install](references/dev-guide/install.md) |
| setting | 配置 | [setting](references/dev-guide/setting.md) |
| quickstart | 快速上手 | [quickstart](references/dev-guide/quickstart.md) |
| common | 内置样式 | [common](references/dev-guide/common.md) |
| feature | 注意事项 | [feature](references/dev-guide/feature.md) |
| changelog | 更新日志 | [changelog](references/dev-guide/changelog.md) |
| changeGuide | 升级指南 | [changeGuide](references/dev-guide/changeGuide.md) |

## 使用示例

### 按钮组件
```vue
<template>
  <view>
    <u-button type="primary" @click="handleClick">主要按钮</u-button>
    <u-button type="success">成功按钮</u-button>
    <u-button type="warning" plain>镂空按钮</u-button>
    <u-button type="error" disabled>错误按钮</u-button>
  </view>
</template>

<script>
export default {
  methods: {
    handleClick() {
      uni.showToast({ title: '点击成功', icon: 'success' })
    }
  }
}
</script>
```

### 表单组件
```vue
<template>
  <view>
    <u-form :model="form" ref="formRef">
      <u-form-item label="用户名" prop="username">
        <u-input v-model="form.username" placeholder="请输入用户名" />
      </u-form-item>
      <u-form-item label="密码" prop="password">
        <u-input v-model="form.password" type="password" placeholder="请输入密码" />
      </u-form-item>
      <u-form-item label="性别" prop="gender">
        <u-radio-group v-model="form.gender">
          <u-radio name="male">男</u-radio>
          <u-radio name="female">女</u-radio>
        </u-radio-group>
      </u-form-item>
      <u-form-item>
        <u-button type="primary" @click="submit">提交</u-button>
      </u-form-item>
    </u-form>
  </view>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
        gender: 'male'
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submit() {
      this.$refs.formRef.validate(valid => {
        if (valid) {
          uni.showToast({ title: '提交成功', icon: 'success' })
        }
      })
    }
  }
}
</script>
```

### 提示组件
```vue
<template>
  <view>
    <u-button @click="showToast">显示提示</u-button>
    <u-button @click="showModal">显示弹窗</u-button>
    <u-toast ref="uToast" />
  </view>
</template>

<script>
export default {
  methods: {
    showToast() {
      this.$refs.uToast.show({
        title: '操作成功',
        type: 'success',
        duration: 2000
      })
    },
    showModal() {
      uni.showModal({
        title: '提示',
        content: '确认执行此操作？',
        success: (res) => {
          if (res.confirm) {
            this.$refs.uToast.show({ title: '已确认', type: 'success' })
          }
        }
      })
    }
  }
}
</script>
```

## 完整文档列表

### 指南类（8 篇）
- [design](references/guide/design.md) - 设计指南
- [demo](references/guide/demo.md) - 示例指南
- [theme](references/guide/theme.md) - 主题指南
- [customIcon](references/guide/customIcon.md) - 自定义图标指南
- [customStyle](references/guide/customStyle.md) - 自定义样式指南
- [i18n](references/guide/i18n.md) - 国际化指南
- [note](references/guide/note.md) - 注意事项
- [faq](references/guide/faq.md) - 常见问题

### 开发指南类（11 篇）
- [intro](references/dev-guide/intro.md) - 介绍
- [install](references/dev-guide/install.md) - 安装
- [setting](references/dev-guide/setting.md) - 配置
- [quickstart](references/dev-guide/quickstart.md) - 快速上手
- [common](references/dev-guide/common.md) - 内置样式
- [feature](references/dev-guide/feature.md) - 注意事项
- [diff1.x](references/dev-guide/diff1.x.md) - 对比 1.X
- [changelog](references/dev-guide/changelog.md) - 更新日志
- [changeGuide](references/dev-guide/changeGuide.md) - 升级指南
- [resource](references/dev-guide/resource.md) - 资源
- [addQQGroup](references/dev-guide/addQQGroup.md) - 加群交流

### 基础组件（16 个）
- [color](references/basic/color.md) - Color 色彩
- [icon](references/basic/icon.md) - Icon 图标
- [image](references/basic/image.md) - Image 图片
- [button](references/basic/button.md) - Button 按钮
- [text](references/basic/text.md) - Text 文本
- [layout](references/basic/layout.md) - Layout 布局
- [cell](references/basic/cell.md) - Cell 单元格
- [badge](references/basic/badge.md) - Badge 徽标数
- [tag](references/basic/tag.md) - Tag 标签
- [loadingIcon](references/basic/loadingIcon.md) - LoadingIcon 加载动画
- [loadingPage](references/basic/loadingPage.md) - LoadingPage 加载页
- [gap](references/basic/gap.md) - Gap 间隔槽
- [avatar](references/basic/avatar.md) - Avatar 头像
- [link](references/basic/link.md) - Link 超链接
- [line](references/basic/line.md) - Line 线条
- [divider](references/basic/divider.md) - Divider 分割线

### 表单组件（16 个）
- [form](references/form/form.md) - Form 表单
- [input](references/form/input.md) - Input 输入框
- [textarea](references/form/textarea.md) - Textarea 文本域
- [checkbox](references/form/checkbox.md) - Checkbox 复选框
- [radio](references/form/radio.md) - Radio 单选框
- [switch](references/form/switch.md) - Switch 开关选择器
- [slider](references/form/slider.md) - Slider 滑动选择器
- [numberBox](references/form/numberBox.md) - NumberBox 步进器
- [rate](references/form/rate.md) - Rate 评分
- [picker](references/form/picker.md) - Picker 选择器
- [datetimePicker](references/form/datetimePicker.md) - DatetimePicker 时间选择器
- [calendar](references/form/calendar.md) - Calendar 日历
- [upload](references/form/upload.md) - Upload 上传
- [search](references/form/search.md) - Search 搜索
- [keyboard](references/form/keyboard.md) - Keyboard 键盘
- [code](references/form/code.md) - Code 验证码输入框

### 数据展示组件（17 个）
- [grid](references/display/grid.md) - Grid 宫格布局
- [list](references/display/list.md) - List 列表
- [album](references/display/album.md) - Album 相册
- [swiper](references/display/swiper.md) - Swiper 轮播图
- [skeleton](references/display/skeleton.md) - Skeleton 骨架屏
- [empty](references/display/empty.md) - Empty 内容为空
- [collapse](references/display/collapse.md) - Collapse 折叠面板
- [steps](references/display/steps.md) - Steps 步骤条
- [indexList](references/display/indexList.md) - IndexList 索引列表
- [lineProgress](references/display/lineProgress.md) - LineProgress 线形进度条
- [countDown](references/display/countDown.md) - CountDown 倒计时
- [countTo](references/display/countTo.md) - CountTo 数字滚动
- [parse](references/display/parse.md) - Parse 富文本解析器
- [codeInput](references/display/codeInput.md) - CodeInput 验证码输入
- [loadMore](references/display/loadMore.md) - LoadMore 加载更多
- [readMore](references/display/readMore.md) - ReadMore 展开阅读更多
- [sticky](references/display/sticky.md) - Sticky 吸顶

### 反馈组件（12 个）
- [toast](references/feedback/toast.md) - Toast 消息提示
- [modal](references/feedback/modal.md) - Modal 模态框
- [popup](references/feedback/popup.md) - Popup 弹出层
- [actionSheet](references/feedback/actionSheet.md) - ActionSheet 操作菜单
- [alert](references/feedback/alert.md) - Alert 警告提示
- [notify](references/feedback/notify.md) - Notify 消息提示
- [noticeBar](references/feedback/noticeBar.md) - NoticeBar 滚动通知
- [tooltip](references/feedback/tooltip.md) - Tooltip 长按提示
- [swipeAction](references/feedback/swipeAction.md) - SwipeAction 滑动单元格
- [overlay](references/feedback/overlay.md) - Overlay 遮罩层
- [noNetwork](references/feedback/noNetwork.md) - NoNetwork 无网络提示
- [scrollList](references/feedback/scrollList.md) - ScrollList 横向滚动列表

### 导航组件（5 个）
- [navbar](references/navigation/navbar.md) - Navbar 自定义导航栏
- [tabbar](references/navigation/tabbar.md) - Tabbar 底部导航栏
- [tabs](references/navigation/tabs.md) - Tabs 标签
- [subsection](references/navigation/subsection.md) - Subsection 分段器
- [backTop](references/navigation/backTop.md) - BackTop 返回顶部

### 其他组件（1 个）
- [transition](references/others/transition.md) - Transition 动画

### JS 工具库（17 个）
- [js-intro](references/js/js-intro.md) - API 介绍
- [fastUse](references/js/fastUse.md) - 便捷工具
- [http](references/js/http.md) - Http 请求
- [debounce](references/js/debounce.md) - 节流防抖
- [object](references/js/object.md) - 对象操作
- [time](references/js/time.md) - 时间格式化
- [route](references/js/route.md) - 路由跳转
- [randomArray](references/js/randomArray.md) - 数组乱序
- [guid](references/js/guid.md) - 全局唯一标识符
- [colorSwitch](references/js/colorSwitch.md) - 颜色转换
- [color](references/js/js-color.md) - 颜色值
- [queryParams](references/js/queryParams.md) - 对象转 URL 参数
- [test](references/js/test.md) - 规则校验
- [random](references/js/random.md) - 随机数值
- [trim](references/js/trim.md) - 去除空格
- [getRect](references/js/getRect.md) - 节点布局信息
- [mpShare](references/js/mpShare.md) - 小程序分享
