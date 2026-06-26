---
number: 14434
title: How to use isolatedDeclarations with defineComponent in typescript
category: Help/Questions
created: 2026-02-09
url: "https://github.com/orgs/vuejs/discussions/14434"
upvotes: 1
comments: 1
answered: false
---

# How to use isolatedDeclarations with defineComponent in typescript

When I am trying to speed up with oxc, I need to enable isolatedDeclarations for dts generation.

<img width="2064" height="648" alt="image" src="https://github.com/user-attachments/assets/1eb2a65e-0fad-4a10-8ec0-27bb37d1fbc5" />

However, I do not see any possibility to write a detailed type by hand. Is there anyway to "declare these components" gracefully?

---

## Top Comments

**@gitboyzcf** (+2):

下面是**在启用 `isolatedDeclarations` 的前提下，优雅生成 d.ts** 的常用做法与注意点（以 Vue + TS 为例），尽量不手写冗长类型：

---

##  核心思路

`isolatedDeclarations` 要求**每个文件都能独立产出声明**，因此禁止依赖“类型推断链过长/跨文件推断/复杂条件类型展开”。解决方案是：

1. **显式导出类型**
2. **把推断结果“固定住”**
3. **避免运行时值推断出复杂类型**

---

##  推荐做法 1：显式导出 Props/Emits 类型

```ts
export interface FadeInExpandTransitionProps {
  group?: boolean
  appear?: boolean
  width?: boolean
  mode?: 'default' | 'in-out' | 'out-in'
  onLeave?: () => void
  onAfterLeave?: () => void
  onAfterEnter?: () => void
}
```

然后：

```ts
export default defineComponent({
  props: {
    // ...使用 PropType 显式标注
  } as PropType<FadeInExpandTransitionProps>,
})
```...