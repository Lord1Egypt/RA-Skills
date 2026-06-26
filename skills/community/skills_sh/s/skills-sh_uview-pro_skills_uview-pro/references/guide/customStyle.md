---
name: "customStyle"
description: "uView Pro 默认提供了一套美观且统一的组件样式，但在实际项目开发中，往往需要根据业务需求进行个性化定制。参考[自定义主题](/zh/guide/theme.html)。. Invoke when user needs guidance on customStyle."
url: "https://uviewpro.cn/zh/guide/customStyle.html"
triggers: ["customStyle","自定义样式"]
---

# 自定义样式 <BadgeVersion text="0.3.0" />


uView Pro 默认提供了一套美观且统一的组件样式，但在实际项目开发中，往往需要根据业务需求进行个性化定制。参考[自定义主题](/zh/guide/theme.html)。

然而，如果仅是需要覆盖组件的默认样式，或增加样式，uView Pro 则支持两种主流的自定义样式方式，灵活满足各种场景。

:::tip 说明
自 uView Pro 0.3.0 版本开始，所有组件支持两种自定义样式方式。
:::

## 方式一：custom-class 样式穿透

所有组件均支持 `custom-class` 属性，可为组件根节点添加自定义 class，实现样式穿透和深度定制。推荐配合 `:deep()` 或 `/deep/` 实现作用域样式穿透。

**示例：**

```html
<view class="my-page">
  <u-button custom-class="my-btn"></u-button>
</view>
```

```scss
.my-page {
  :deep(.my-btn) {
    background-color: #2979ff;
    color: #fff;
    border-radius: 8px;
  }
}
```

- 可用于自定义背景、字体、边框、动画等任意样式。
- 支持多层嵌套和全局样式覆盖。

## 方式二：custom-style 内联样式

所有组件均支持 `custom-style` 属性，可直接传递内联样式字符串，快速实现样式定制。

**示例：**

```html
<u-button
  custom-style="background: linear-gradient(90deg,#2979ff,#00c6ff);color:#fff;border-radius:8px;"
></u-button>
```

- 适合简单样式调整和动态样式绑定。
- 支持与变量、计算属性结合。

## 进阶说明

- 两种方式可结合使用，优先级：`custom-style` > `custom-class` > 组件默认样式。
- 推荐在页面根节点加唯一 class，避免样式污染。
- 复杂场景建议使用 `custom-class`，便于维护和复用。
- 组件文档均有对应属性说明，详见各组件 API。

## 常见问题

- **为什么样式不生效？**
  - 检查 class 名称是否正确，是否在正确的作用域下。
  - 确认样式优先级，必要时使用 `!important`。
  - Vue3/uni-app 下建议用 `:deep()` 实现穿透。
- **如何批量定制所有组件样式？**
  - 可通过全局样式或主题变量统一覆盖，参考[自定义主题](/zh/guide/theme.html)。
