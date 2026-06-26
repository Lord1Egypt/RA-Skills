---
name: "useColor"
description: "响应式颜色管理 composable，提供响应式的颜色访问，支持主题切换和暗黑模式。. Invoke when user needs to use useColor hook."
url: "https://uviewpro.cn/zh/hooks/useColor.html"
triggers: ["useColor","颜色管理"]
---

# useColor 主题颜色

响应式颜色管理 composable，提供响应式的颜色访问，支持主题切换和暗黑模式。

## 概述

`useColor` 是一个 Vue 3 composable，用于获取和管理应用的颜色主题。它会响应式地根据当前主题和暗黑模式状态返回对应的颜色值。

## 引入方式

```typescript
import { useColor } from 'uview-pro';
```

## API

### 返回值

`useColor()` 返回一个包含以下属性的对象：

| 属性 | 类型 | 说明 |
|------|------|------|
| `color` | `ComputedRef<Record<ColorType, string>>` | 响应式的颜色对象，包含当前主题的所有颜色 |
| `getColor` | `(name: ColorType) => ComputedRef<string>` | 获取指定颜色的响应式引用 |

### color

当前激活模式下的颜色对象（响应式）。

```typescript
const { color } = useColor();

// 在模板中直接使用
<view :style="{ color: color.primary }">文本</view>

// 在 script 中使用
console.log(color.value.primary); // 获取主色调
console.log(color.value.success); // 获取成功色
```

颜色对象包含以下常用颜色：

- `primary` - 主色调
- `success` - 成功色
- `warning` - 警告色
- `error` - 错误色
- `info` - 信息色

### getColor(name)

获取指定颜色的响应式引用。

```typescript
const { getColor } = useColor();

// 获取主色调的响应式引用
const primaryColor = getColor('primary');

// 在模板中使用
<view :style="{ color: primaryColor }">主色调文本</view>

// 在 computed 中使用
const buttonStyle = computed(() => ({
    backgroundColor: primaryColor.value
}));
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | `ColorType` | 是 | 颜色名称，如 `primary`、`success`、`error` 等 |

**ColorType类型：**

```typescript
type ColorType =
    | 'primary'
    | 'primaryDark'
    | 'primaryDisabled'
    | 'primaryLight'
    | 'bgColor'
    | 'bgWhite'
    | 'bgGrayLight'
    | 'bgGrayDark'
    | 'bgBlack'
    | 'info'
    | 'infoDark'
    | 'infoDisabled'
    | 'infoLight'
    | 'warning'
    | 'warningDark'
    | 'warningDisabled'
    | 'warningLight'
    | 'error'
    | 'errorDark'
    | 'errorDisabled'
    | 'errorLight'
    | 'success'
    | 'successDark'
    | 'successDisabled'
    | 'successLight'
    | 'mainColor'
    | 'contentColor'
    | 'tipsColor'
    | 'lightColor'
    | 'borderColor'
    | 'whiteColor'
    | 'blackColor'
    | 'dividerColor'
    | 'maskColor'
    | 'shadowColor';
```

## 使用示例

### 基础用法

```html
<script setup lang="ts">
import { useColor } from 'uview-pro';

const { color, getColor } = useColor();

// 直接使用颜色对象
const bgStyle = {
    backgroundColor: color.value.bgColor,
    color: color.value.mainColor
};

// 使用 getColor 获取特定颜色
const primaryTextStyle = computed(() => ({
    color: getColor('primary').value
}));
</script>

<template>
    <view :style="bgStyle">
        背景颜色：{{ color.value.bgColor }}
        <view :style="primaryTextStyle">主色调文字</view>
    </view>
</template>
```

### 结合暗黑模式使用

```typescript
<script setup lang="ts">
import { useColor } from 'uview-pro';

const { color } = useColor();

// 根据暗黑模式调整样式
const cardStyle = computed(() => ({
    backgroundColor: color.value.bgColor,
    borderColor: color.value.borderColor,
    color: color.value.mainColor
}));
</script>

<template>
    <view :style="cardStyle" class="card">
        <text>卡片内容</text>
    </view>
</template>
```

## 注意事项

1. `color` 是计算属性，会自动响应主题和暗黑模式的变化
2. `getColor` 返回的也是响应式引用，当主题切换时会自动更新
3. 建议在 `script setup` 中使用，配合 `computed` 或直接在模板中使用
4. 颜色类型 `ColorType` 定义在 `uni_modules/uview-pro/types/global.ts`
