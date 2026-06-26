---
name: features-form
description: uni-app 表单 form 组件、report-submit、@submit、@reset、form-type
---

# 表单

## form 组件

**form** 用于收集内部 **switch、input、checkbox、radio、slider、picker** 等控件的值。表单控件需设置 **name** 作为提交时的 key。点击 **formType 为 submit** 的 **button** 时触发 **@submit**，event.detail 含 **value**（name 与值的对象）、**formId**（report-submit 为 true 时，用于模板消息等）。

## 属性与事件

- **report-submit**：是否返回 formId（微信、支付宝等用于模板消息）。可选 **report-submit-timeout** 等待 formId 生效检测。
- **@submit**：提交时触发，detail.value 为表单数据对象。
- **@reset**：点击 formType 为 reset 的 button 时触发，表单重置。

## button 的 form-type

- **submit**：提交表单，触发 form 的 @submit。
- **reset**：重置表单，触发 form 的 @reset。

校验与提交逻辑在 @submit 回调中自行处理（如校验、uni.request 上传）。

<!--
Source references:
- https://uniapp.dcloud.net.cn/component/form
-->
