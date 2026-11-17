---
name: vue
description: Vue 3 编码规范。编写任何 .vue 源码时都应触发。
---

## Coding Practices

### 版本约定

务必确保项目使用的依赖版本最低要求满足如下列表

- Vue 3.5+
- TypeScript 5.9+

### 细则

| 场景 | 入口 | 何时读 |
|---|---|---|
| Vue 组件目录结构与类型导出 | [vue-component-directory-structure.md](vue-component-directory-structure.md) | 创建新组件、重构组件目录、或搭建 Vue 组件架构时 |
| Vue Composition API 常用模式 | [vue-composition-api-patterns.md](vue-composition-api-patterns.md) | 写 / 改 / 审 Vue `<script setup>` 代码时 |
| Vue Composition API 代码就近组织 | [vue-composition-api-proximity.md](vue-composition-api-proximity.md) | 写 / 改 / 审 Vue `<script setup>` 代码时 |
| Vue 组件样式 | [vue-component-css-class-over-style.md](vue-component-css-class-over-style.md) | 写 / 改 / 审 Vue CSS 样式代码时 |
