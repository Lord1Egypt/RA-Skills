---
name: wot-ui-plus
description: wot-ui-plus 组件使用指南。当用户询问 wot-ui-plus 组件、组合式 API、全局配置、主题定制、示例写法或 API 参考时使用此技能。优先基于 `references/` 目录中的组件文档回答问题。
---

# wot-ui-plus

此技能提供 `wot-ui-plus` 组件库的使用指导，重点是帮助快速定位组件文档、提取正确 API，并给出可直接复用的示例。

## 何时使用

当用户需要以下帮助时使用此技能：

- 查询某个组件怎么用，例如 Button、Popup、Upload、Calendar
- 查询 props、events、slots、methods 或 `v-model` 用法
- 查询组合式 API，例如 `use-toast`、`use-message`、`use-upload`
- 查询全局配置、主题配置、Provider 相关能力
- 基于组件文档给出示例、接入方式或常见注意点

## 组件参考

`references/` 目录已经包含组件与 API 文档。回答具体问题时，先定位对应的 markdown 文件，再基于文档组织答案。

### 基础

- `button.md`
- `cell.md`
- `configProvider.md`
- `icon.md`
- `img.md`
- `layout.md`
- `popup.md`
- `resize.md`
- `transition.md`
- `gap.md`
- `rootPortal.md`

### 表单

- `calendar.md`
- `calendarView.md`
- `checkbox.md`
- `colPicker.md`
- `datetimePicker.md`
- `datetimePickerView.md`
- `form.md`
- `input.md`
- `inputNumber.md`
- `passwordInput.md`
- `textarea.md`
- `keyboard.md`
- `picker.md`
- `pickerView.md`
- `radio.md`
- `rate.md`
- `search.md`
- `selectPicker.md`
- `signature.md`
- `slider.md`
- `switch.md`
- `upload.md`
- `imgCropper.md`
- `code.md`
- `codeInput.md`

### 反馈与交互

- `actionSheet.md`
- `curtain.md`
- `dropMenu.md`
- `overlay.md`
- `popover.md`
- `swipeAction.md`
- `messageBox.md`
- `notify.md`
- `toast.md`
- `loading.md`
- `loadingPage.md`
- `tooltip.md`
- `fab.md`
- `floatingPanel.md`
- `sliderButton.md`

### 展示

- `avatar.md`
- `badge.md`
- `tag.md`
- `card.md`
- `circle.md`
- `divider.md`
- `collapse.md`
- `countDown.md`
- `countTo.md`
- `grid.md`
- `table.md`
- `noticeBar.md`
- `statusTip.md`
- `progress.md`
- `steps.md`
- `segmented.md`
- `skeleton.md`
- `sortButton.md`
- `swiper.md`
- `text.md`
- `tour.md`
- `watermark.md`
- `waterfall.md`
- `sticky.md`
- `videoPreview.md`

### 导航与布局

- `backtop.md`
- `indexBar.md`
- `navbar.md`
- `pagination.md`
- `sidebar.md`
- `tabbar.md`
- `tabs.md`
- `row.md`

### 组合式 API

- `use-count-down.md`
- `use-message.md`
- `use-notify.md`
- `use-toast.md`
- `use-upload.md`

### 其他常用能力

- `dateStrip.md`
- `lazyLoad.md`
- `loadMore.md`
- `numberKeyboard.md`
- `table.md`
- `tree.md`

## 使用模式

1. 识别目标：先确定用户问的是组件、组合式 API、主题配置，还是具体示例。
2. 查阅文档：优先读取 `references/` 中对应的 markdown 文件。
3. 提炼答案：优先输出直接可用的示例、关键 API、注意事项。
4. 保持收敛：围绕用户提问的组件回答，不把答案扩展成整套组件库综述。

## 工作规则

- 默认把 wot-ui-plus 视为 `uni-app + Vue 3 + TypeScript` 组件库。
- 写页面时优先输出 `script setup` 风格。
- 反馈类能力如 `useToast`、`useDialog`、`useNotify`、`useImagePreview`、`useVideoPreview`，除了 hook 调用外，通常还需要页面内显式声明对应组件实例。
- 生成代码时尽量沿用组件库文档里的命名和交互模式，例如 `v-model:visible`、`before-confirm`、`confirm`、`change`、`custom-class`、`custom-style`。


## 最佳实践

- 示例优先：优先给出可以直接复制的最小示例，再补充 API 说明。
- API 对齐：严格以文档中的 props、events、slots、methods 名称作答，不自行发明字段。
- 绑定意识：遇到表单类组件时，优先检查是否涉及 `v-model`、受控值和事件联动。
- 服务式能力：遇到 `toast`、`notify`、`message` 等场景时，优先检查是否应使用对应 `use-*` API。
- 配置类问题：涉及全局配置与主题时，优先查看 `configProvider.md` 及相关文档，而不是分散回答。

## 约束

- 默认使用中文回答。
- 优先基于 `references/` 中已有文档作答。
- 若文档足以回答问题，不额外扩展到实现分析。
