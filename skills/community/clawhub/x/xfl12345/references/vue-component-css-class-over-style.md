---
name: vue-component-css-class-over-style
description: 在编写或重构 Vue 3 组件时使用——用 CSS class prop 替代 `propsCssStyle` JS 对象，用 CSS 模块（CSS modules）+ `v-bind()` 取代内联样式。在组件通过 prop 传递 `CSSProperties` 或模板中存在内联 `style` 属性时触发。
---

# Vue 组件优先使用 CSS Class 而非 Style

## 概述

**禁止通过 prop 把 CSS 作为 JS 对象传递。内部元素定制用 CSS class prop，响应式动态值用 CSS 模块 + `v-bind()`。**

## 核心规则

### 禁止 propsCssStyle

`propsCssStyle?: CSSProperties` 被禁用。替换方式取决于它原来作用于哪个元素：

**根元素** → 直接移除该 prop。使用方可以在组件标签上直接写 `class` 或 `style`。

**内部元素** → 增加一个具名 class prop（`xxxClass?: string`），并在目标元素上用 `:class` 绑定。

```vue
<!-- ❌ BAD：通过 prop 用 JS 对象传递 CSS -->
<script setup lang="ts">
import type { CSSProperties } from 'vue'

interface Props {
  propsCssStyle?: CSSProperties
}
const props = withDefaults(defineProps<Props>(), {
  propsCssStyle: () => ({ backgroundColor: 'white' }),
})
</script>
<template>
  <div :style="props.propsCssStyle">...</div>
</template>

<!-- ✅ GOOD：CSS class prop（内部元素场景）-->
<script setup lang="ts">
defineProps<{ borderClass?: string }>()
</script>
<template>
  <div :class="[$style.circleBorder, borderClass]">...</div>
</template>
<style module>
.circleBorder {
  background-color: white;
}
</style>
```

### Class Prop 命名

prop 名称按它绑定的元素命名，而不是按 CSS 属性命名：

```typescript
// ❌ BAD：按 CSS 属性命名
backgroundColorClass?: string
shadowStyleClass?: string

// ✅ GOOD：按绑定元素命名
buttonBodyClass?: string      // 绑定到按钮主体元素
buttonBorderClass?: string    // 绑定到边框/阴影元素
centerPictureClass?: string   // 绑定到中间图片区域
```

### 禁止 `:style` 与内联样式

所有 `style="..."`、`:style="..."` 和 `:style="someComputed"` 都必须替换为 `<style module>` 类 + `v-bind()`。

## CSS class 静态引用规范

样式值会变，CSS class 挂定后不切换——业务数据经 computed 派生样式，CSS class 通过 `v-bind()` 直取。

### 1. 单字段 → `v-bind(name)`

```vue
<!-- ❌ BAD -->
<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'

const props = defineProps<{ boxSize: number }>()
const boxStyle = computed<CSSProperties>(() => ({ borderRadius: props.boxSize + 'px' }))
</script>
<template>
  <div :style="[boxStyle]" />
</template>

<!-- ✅ GOOD -->
<script setup lang="ts">
const props = defineProps<{ boxSize: number }>()
</script>
<template>
  <div :class="$style.box" />
</template>
<style module>
.box { border-radius: calc(v-bind(boxSize) * 1px); }
</style>
```

### 2. 多字段 → 逐字段 `v-bind('obj.field')`

```vue
<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'

const props = defineProps<{
  progress: number   // 业务值：进度 0-100
  speed: number      // 业务值：倍速
}>()
const circleStyle = computed<CSSProperties>(() => ({
  strokeDasharray: `${props.progress * 2.51} 251`,   // r=40 周长≈251：进度 → 弧长
  transitionDuration: `${1 / props.speed}s`,         // 倍速 → 过渡时长
}))
</script>

<!-- ❌ BAD: :style 直绑动态样式对象——应改走 CSS module + v-bind 逐字段 -->
<template>
  <circle :style="circleStyle" />
</template>

<!-- ✅ GOOD: 同一份派生样式，出口换成 CSS module + 逐字段 v-bind -->
<template>
  <circle :class="$style.filling" />
</template>
<style module>
.filling {
  stroke-dasharray: v-bind('circleStyle.strokeDasharray');
  transition-duration: v-bind('circleStyle.transitionDuration');
}
</style>
```

### 3. `calc(v-bind() * 1px)` 与 JS 字符串 computed 的取舍

单值单位转换优先用 CSS `calc(v-bind(numericRef) * 1px)`，而不是 JS 字符串拼接 computed。这样能让 JS 里保持数值类型，单位交给 CSS 处理。

```typescript
import { computed, type CSSProperties } from 'vue'

const props = defineProps<{ theFontSizeInPixel: number }>()

// ❌ BAD：单值用 JS 字符串拼接
const theFontSize = computed<CSSProperties['fontSize']>(() => props.theFontSizeInPixel + 'px')
```

```css
/* ✅ GOOD：JS 保持数值，单位交给 CSS */
font-size: calc(v-bind(theFontSizeInPixel) * 1px);
```

**阈值取决于表达式复杂度：**

**简单单位转换**（`* 1px`，无额外运算）—— CSS 中重复 **2 次** 可以接受；达到 **3 次及以上** 时提取为 computed：

```css
/* ✅ OK：简单 * 1px 重复两次——无需提取 */
.icon { width: calc(v-bind(size) * 1px); }
.thumb { height: calc(v-bind(size) * 1px); }
```

```typescript
import { computed, ref, type CSSProperties } from 'vue'

const qrCodeHeightInPixel = ref(100)
// ✅ GOOD：简单转换出现 3+ 次，值得提取为 computed
const qrCodeHeight = computed<CSSProperties['height']>(() => qrCodeHeightInPixel.value + 'px')
```

```css
.qrCode {
  width: v-bind(qrCodeHeight);
  height: v-bind(qrCodeHeight);
}
.middleBox { height: v-bind(qrCodeHeight); }
```

**非简单计算**（额外乘数如 `* 1.25`、Math 函数、除法等）—— 重复 **2+ 次** 就提取。重复复杂的 calc 表达式会隐藏语义关系，并且容易漂移：

```css
/* ❌ BAD：同一非简单 calc 重复——难以看出是同一个值 */
.titleBar { font-size: calc(v-bind(theFontSizeInPixel) * 1.25 * 1px); }
.sloganBar { font-size: calc(v-bind(theFontSizeInPixel) * 1.25 * 1px); }
```

```typescript
import { computed, type CSSProperties } from 'vue'

const props = defineProps<{ theFontSizeInPixel: number }>()

// ✅ GOOD：已提取——关系显式、单一真相源
const titleFontSize = computed<CSSProperties['fontSize']>(() => props.theFontSizeInPixel * 1.25 + 'px')
```

```css
.titleBar { font-size: v-bind(titleFontSize); }
.sloganBar { font-size: v-bind(titleFontSize); }
```

**例外：Math 函数保留在 JS computed 中**（即使只用一次）。`Math.floor`、`Math.ceil` 等没有 CSS 等价写法——数值中间结果必须留在 JS 里：

```typescript
import { computed } from 'vue'

const props = defineProps<{ theFontSizeInPixel: number }>()

// ✅ GOOD：Math.floor 留在 JS 里，供 CSS 和其他 JS computed 共用
const quarterFontSizeInPixel = computed<number>(() => Math.floor(props.theFontSizeInPixel / 4))
```

### 4. 多值 CSS 属性

像 `margin`、`padding`、`box-shadow` 这类简写属性，如果每个值都用 `calc(v-bind * 1px)` 会非常冗长，保留 JS 字符串 computed 以提升可读性：

```typescript
import { computed, type CSSProperties } from 'vue'

const props = defineProps<{ theFontSizeInPixel: number }>()
type CssTypeFontSize = CSSProperties['fontSize']
const oneEighthFontSize = computed<CssTypeFontSize>(() => `${props.theFontSizeInPixel / 8}px`)
const quarterFontSize = computed<CssTypeFontSize>(() => `${props.theFontSizeInPixel / 4}px`)

// ✅ GOOD：多值场景——JS computed 更清爽
const rootMargin = computed<string>(() =>
  [oneEighthFontSize.value, quarterFontSize.value, quarterFontSize.value, quarterFontSize.value].join(' ')
)
const boxShadow = computed<string>(() => {
  const fSize = oneEighthFontSize.value
  return [fSize, fSize, fSize, '0', 'gray'].join(' ')
})
```

```css
.root { margin: v-bind(rootMargin); }
.card { box-shadow: v-bind(boxShadow); }
```

### 5. `v-bind()` 点号写法必须加引号

简单标识符不加引号即可。点号写法**必须**使用字符串形式：

```css
/* ✅ 简单标识符——不加引号 */
width: v-bind(boxWidth);

/* ❌ 点号写法没加引号 */
stroke: v-bind(circleStyle.stroke);

/* ✅ 字符串形式 */
stroke: v-bind('circleStyle.stroke');
```

## CSS class 动态引用规范

CSS 值不变，变的是哪些 class 生效——条件激活与整套切换。

### 动态激活法

CSS 值是**静态**的、但按条件应用时，用 Vue 的条件 class 绑定即可，不需要 computed 或 v-bind()：

```vue
<!-- ❌ BAD：computed 返回静态值或 undefined，再绑定到样式 -->
<script setup lang="ts">
import { computed, reactive, type CSSProperties } from 'vue'

const settingsStore = reactive({ devMode: false })

const debugBorderAqua = computed<CSSProperties['border']>(() =>
  settingsStore.devMode ? '1px dashed aqua' : undefined
)
</script>
<template>
  <div :class="$style.cvBox" :style="{ border: debugBorderAqua }"></div>
</template>
<!-- 更差：把静态值塞进 CSS 的 v-bind 里（而非用 class）-->
<style module>
.cvBox { border: v-bind(debugBorderAqua); }
</style>

<!-- ✅ GOOD：静态 CSS class + 条件绑定 -->
<script setup lang="ts">
import { reactive } from 'vue'

const settingsStore = reactive({ devMode: false })
</script>
<template>
  <div :class="[$style.cvBox, { [$style.cvBoxDebug]: settingsStore.devMode }]"></div>
</template>
<style module>
.cvBoxDebug { border: 1px dashed aqua; }
</style>
```

**原因：** CSS 值本身是静态的——运行时不变，只变“是否应用”。这种情况下 CSS class 是正确抽象；v-bind() 用于动态值。

### 动态列表法

在多个完整布局模式之间切换时（例如居中 vs 左对齐），用 `useCssModule()` + 返回 CSS 模块键名的 computed，而不是返回 CSSProperties 对象的 computed：

```vue
<!-- ❌ BAD：computed CSSProperties + 每个属性单独 v-bind('obj.field') -->
<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'

const shouldCenter = ref(true)

const cvBoxParentStyle = computed<CSSProperties>(() => {
  if (shouldCenter.value) {
    return { justifyContent: 'center', width: '100%', height: '100%' }
  }
  return { justifyContent: 'flex-start' }
})
</script>
<template>
  <div :class="$style.cvBoxParent"></div>
</template>
<style module>
.cvBoxParent {
  justify-content: v-bind('cvBoxParentStyle.justifyContent');
  width: v-bind('cvBoxParentStyle.width');
  height: v-bind('cvBoxParentStyle.height');
}
</style>

<!-- ✅ GOOD：CSS class + useCssModule() 保证类型安全 -->
<script setup lang="ts">
import { computed, ref, useCssModule } from 'vue'

const shouldCenter = ref(true)

const cssModule = useCssModule()
type CssModuleKey = keyof typeof cssModule
const cvBoxParentLayoutClass = computed<CssModuleKey>(() => {
  return shouldCenter.value
    ? cssModule.cvBoxParentFoxy
    : cssModule.cvBoxParentDefault
})
</script>
<template>
  <div :class="[$style.cvBoxParent, cvBoxParentLayoutClass]"></div>
</template>
<style module>
.cvBoxParent { display: flex; }
.cvBoxParentFoxy { justify-content: center; width: 100%; height: 100%; }
.cvBoxParentDefault { justify-content: flex-start; }
</style>
```

**原因：** 所有值都是静态的——只有“选哪一个”是动态的。CSS class 能干净表达这种选择。`useCssModule()` 为 class 名字符串提供编译期类型安全。
