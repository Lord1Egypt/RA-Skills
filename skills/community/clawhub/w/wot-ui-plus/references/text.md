# Text 文本


## 组件概况

用于展示文本的组件，支持主题设置、脱敏处理、日期格式化、金额格式化、多行省略等功能。

## 代码演示

### 基本用法

通过 `text` 属性设置要显示的文本内容。

```html
<wd-text text="这是一段普通的文本内容"></wd-text>
```

### 主题类型

通过 `type` 属性设置文本的主题类型，支持 `primary`、`error`、`success`、`warning`、`default`。

```html
<view style="display: flex">
  <wd-text type="primary" text="主色"></wd-text>
  <wd-text type="error" text="错误"></wd-text>
  <wd-text type="success" text="成功"></wd-text>
  <wd-text type="warning" text="警告"></wd-text>
  <wd-text text="默认"></wd-text>
</view>
```

### 自定义样式

通过 `color`、`size`、`bold`、`lineHeight`、`decoration` 等属性自定义文本样式。

```html
<!-- 自定义颜色 -->
<wd-text text="自定义颜色文本" color="#36B8C2"></wd-text>

<!-- 粗体 -->
<wd-text text="粗体文本" bold></wd-text>

<!-- 字体大小 -->
<wd-text text="16px字体" size="16px"></wd-text>

<!-- 文字装饰 -->
<wd-text text="下划线文本" type="warning" decoration="underline"></wd-text>

<!-- 删除线 -->
<wd-text text="16354.156" mode="price" type="success" decoration="line-through" prefix="￥"></wd-text>
```

### 多行省略

通过 `lines` 属性设置文本显示的行数，超出指定行数后显示省略号，最大值为 5。

```html
<wd-text :text="longText" :lines="2" size="16px"></wd-text>
```

### 文本脱敏

通过设置 `mode` 为 `phone` 或 `name`，并配合 `format` 属性实现文本脱敏。

```html
<!-- 姓名脱敏：张长三 -> 张**三 -->
<wd-text text="张长三" mode="name" :format="true"></wd-text>

<!-- 手机号脱敏：18888888888 -> 188****8888 -->
<wd-text text="18888888888" mode="phone" :format="true"></wd-text>
```

### 日期格式化

通过设置 `mode` 为 `date`，将时间戳格式化为 `YYYY-MM-DD` 格式的日期。

```html
<!-- 1719976636911 -> 2024-07-03 -->
<wd-text text="1719976636911" mode="date"></wd-text>
```

### 金额格式化

通过设置 `mode` 为 `price`，将数字格式化为带千分位分隔符的金额格式，保留两位小数。

```html
<!-- 16354.156 -> 16,354.16 -->
<wd-text text="16354.156" mode="price" type="success" prefix="￥"></wd-text>
```

### 前后置内容

通过 `prefix`、`suffix` 属性或 `prefix`、`suffix` 插槽添加前后置内容。

```html
<!-- 使用属性 -->
<wd-text text="12345678901" mode="phone" :format="true" type="primary" prefix="Prefix" suffix="Suffix"></wd-text>

<!-- 使用插槽 -->
<wd-text text="12345678901" mode="phone" :format="true" type="primary">
  <template #prefix>
    <text>前置插槽</text>
  </template>
  <template #suffix>
    <wd-icon name="phone-call-filled"></wd-icon>
  </template>
</wd-text>
```

## API

### Text Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
|--------|------|------|--------|--------|
| type | 主题类型 | string | `primary` / `error` / `success` / `warning` / `default` | `default` |
| text | 文字内容 | string / number | - | `''` |
| size | 字体大小 | number / string | - | `''` |
| mode | 文本处理的匹配模式 | string | `text` / `date` / `phone` / `name` / `price` | `text` |
| decoration | 文字装饰 | string | `underline` / `line-through` / `overline` | `none` |
| call | mode=phone时，点击文本是否拨打电话 | boolean | - | `false` |
| bold | 是否粗体 | boolean | - | `false` |
| format | 是否脱敏，当mode为phone和name时生效 | boolean | - | `false` |
| color | 文本颜色 | string | - | `''` |
| prefix | 前置内容 | string | - | `''` |
| suffix | 后置内容 | string | - | `''` |
| lines | 文本显示的行数，超出此行数将显示省略号，最大值为5 | number | - | - |
| lineHeight | 文本行高 | string | - | `''` |
| custom-style | 自定义根节点样式 | string | - | `''` |
| custom-class | 自定义根节点样式类 | string | - | `''` |

### Text Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| click | 点击文本时触发 | `(event: Event)` |

### Text Slots

| 插槽名 | 说明 |
|--------|------|
| prefix | 前置内容插槽 |
| suffix | 后置内容插槽 |

## 类型定义

### TextType

```ts
export type TextType = 'default' | 'primary' | 'success' | 'warning' | 'error'
```

## 注意事项

1. `lines` 属性最大值为 5，设置大于 5 的值可能不会生效。
2. 当设置了 `color` 属性时，`type` 属性定义的主题颜色将不再生效。
3. `format` 属性仅在 `mode` 为 `phone` 或 `name` 时生效。
4. `mode` 为 `date` 时，`text` 属性应为时间戳（毫秒）。
5. `mode` 为 `price` 时，文本会自动添加千分位分隔符并保留两位小数。
6. 脱敏规则：
   - 姓名脱敏：保留首尾字符，中间用 `**` 替换，例如 `张长三` -> `张**三`
   - 手机号脱敏：保留前三位和后四位，中间用 `****` 替换，例如 `18888888888` -> `188****8888`
