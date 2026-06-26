# Badge 徽章


## 组件概况

Badge 徽章组件是一种轻量级的视觉标记元素，用于在目标元素的右上角显示数字、文字或点状标记。该组件通常用于提示用户有新消息、新任务或需要关注的内容状态，能够有效吸引用户注意力而不干扰主要操作流程。

徽章采用绝对定位布局，自动贴附在目标元素的右上角，支持数字计数、文本标签、圆点提示等多种展示形态，并提供丰富的主题色和自定义配置选项。

## 核心功能描述

- **数字标记**：显示具体数值，支持设置最大值上限，超出后自动显示 `{max}+` 格式
- **点状标记**：通过 `is-dot` 属性切换为小型圆点样式，适用于无需展示具体数量的场景
- **主题配色**：内置 primary、success、warning、danger、info 五种预设主题色
- **零值控制**：支持通过 `show-zero` 属性控制数值为 0 时是否展示徽章
- **位置偏移**：提供 `top` 和 `right` 属性，支持像素级微调徽章定位位置
- **显隐控制**：通过 `hidden` 属性动态控制徽章的显示与隐藏
- **自定义样式**：支持自定义背景颜色、根节点样式和样式类

## 适用业务场景

- **消息通知**：展示未读消息数量、待办事项数量等
- **状态标识**：标记新功能（NEW）、热门内容（HOT）等文本标签
- **数量提示**：购物车商品数量、收藏数量、点赞数量等
- **状态激活**：使用点状徽章表示某项功能已开启或处于活跃状态
- **信息提醒**：需要引起用户注意但不展示具体数量的场景

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 显示值，支持数字和字符串 | number / string | - | - | - |
| type | 徽标主题类型 | string | primary / success / warning / danger / info | - | - |
| max | 最大值，超过最大值会显示 `{max}+`，要求 modelValue 是 Number 类型 | number | - | - | - |
| isDot | 是否为点状徽标，设置为 true 时不显示内容，仅展示圆点 | boolean | - | false | - |
| showZero | 当数值为 0 时，是否展示徽标 | boolean | - | false | - |
| hidden | 是否隐藏徽章 | boolean | - | false | - |
| bgColor | 自定义徽标背景颜色 | string | - | - | - |
| top | 徽标垂直偏移量，正值向下偏移，支持带单位的字符串或纯数字（默认单位为 px） | number / string | - | - | - |
| right | 徽标水平偏移量，正值向左偏移，支持带单位的字符串或纯数字（默认单位为 px） | number / string | - | - | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于包裹需要添加徽章的目标元素（如按钮、图标、文本等） | 任意内容 |

### Methods

组件未暴露外部可调用的方法。

### Events

组件未定义对外抛出的事件。

## 使用示例

### 基础用法 - 展示消息数量

最基本的徽章使用方式，通过 `modelValue` 属性传入需要显示的数值，将目标元素放置在默认插槽中即可。

```vue
<template>
  <wd-badge :modelValue="12">
    <wd-button :round="false" type="info" size="small">评论</wd-button>
  </wd-badge>

  <wd-badge :modelValue="3" bg-color="pink">
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>
</template>
```

### 主题类型

通过 `type` 属性设置徽章的预设主题色，支持 primary、success、warning、danger、info 五种类型。

```vue
<template>
  <wd-badge :modelValue="1" type="primary">
    <wd-button :round="false" type="info" size="small">评论</wd-button>
  </wd-badge>

  <wd-badge :modelValue="2" type="warning">
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>

  <wd-badge :modelValue="1" type="success">
    <wd-button :round="false" type="info" size="small">评论</wd-button>
  </wd-badge>

  <wd-badge :modelValue="2" type="info">
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>
</template>
```

### 最大值限制

通过 `max` 属性设置显示的最大值，当 `modelValue` 超过 `max` 时，会自动显示为 `{max}+` 的格式。此功能要求 `modelValue` 为 Number 类型。

```vue
<template>
  <wd-badge :modelValue="200" :max="99">
    <wd-button :round="false" type="info" size="small">评论</wd-button>
  </wd-badge>

  <wd-badge :modelValue="200" :max="10">
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>
</template>
```

### 自定义文本内容

`modelValue` 支持字符串类型，可用于显示自定义文本标签，如"NEW"、"HOT"等。

```vue
<template>
  <wd-badge modelValue="new">
    <wd-button :round="false" type="info" size="small">评论</wd-button>
  </wd-badge>

  <wd-badge modelValue="hot">
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>
</template>
```

### 点状徽章

通过 `is-dot` 属性将徽章切换为圆点样式，适用于不需要展示具体数量、仅需提示存在状态的场景。

```vue
<template>
  <wd-badge is-dot>数据查询</wd-badge>

  <wd-badge is-dot>
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>
</template>
```

### 零值显示控制

默认情况下，当 `modelValue` 为 0 时徽章不会显示。通过设置 `show-zero` 属性可以在值为 0 时仍然展示徽章。

```vue
<template>
  <!-- 显示 0 值徽章 -->
  <wd-badge :modelValue="0" show-zero>
    <wd-button :round="false" type="info" size="small">评论</wd-button>
  </wd-badge>

  <!-- 不显示 0 值徽章（默认行为） -->
  <wd-badge :modelValue="0">
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>

  <!-- 点状徽章在值为 0 时依然显示 -->
  <wd-badge :modelValue="0" is-dot>
    <wd-button :round="false" type="info" size="small">回复</wd-button>
  </wd-badge>
</template>
```

### 位置偏移

通过 `top` 和 `right` 属性可以微调徽章的位置。`top` 为正值时徽章向下偏移，`right` 为正值时徽章向左偏移。支持带单位的字符串（如 `'10px'`）或纯数字（默认单位为 px）。

```vue
<template>
  <wd-badge :modelValue="5" :top="10" :right="10">
    <wd-icon name="star-filled" size="22px"></wd-icon>
  </wd-badge>

  <wd-badge :modelValue="8" top="-5px" right="-5px">
    <wd-button :round="false" type="info" size="small">偏移示例</wd-button>
  </wd-badge>
</template>
```

## 注意事项

1. **默认插槽必填**：Badge 组件需要包裹目标元素使用，默认插槽中应放置需要添加徽章的内容（如按钮、图标、文本等）。组件会自动以 `inline-block` 方式展示。

2. **最大值生效条件**：`max` 属性仅在 `modelValue` 为 Number 类型且不是 NaN 时生效。如果传入的是字符串类型的数字，最大值限制将不会触发。

3. **点状徽章优先级**：当 `is-dot` 设置为 `true` 时，徽章内容始终为空，即使设置了 `modelValue` 也不会显示数字或文字，仅展示圆点。

4. **零值显示逻辑**：默认情况下值为 0 时徽章不显示。如果需要在值为 0 时仍然展示，必须显式设置 `show-zero` 属性为 `true`。但 `is-dot` 模式下不受此限制，点状徽章始终显示。

5. **隐藏控制**：`hidden` 属性为 `true` 时，无论其他条件如何，徽章都将不显示。该属性的优先级高于其他显示控制逻辑。

6. **定位方式**：徽章采用绝对定位（absolute）相对于父容器（relative）进行定位，默认贴附在目标元素的右上角。如需调整位置，请使用 `top` 和 `right` 属性，避免直接使用自定义样式覆盖定位属性。

7. **样式定制**：推荐使用 `custom-class` 和 `custom-style` 属性进行样式定制。如需调整徽章容器间距，建议在外部包裹元素或使用自定义类名进行控制。

8. **内容渲染规则**：徽章的显示逻辑遵循以下判断顺序：首先检查 `hidden` 状态，其次判断是否为点状模式，最后检查内容值或零值显示条件。
