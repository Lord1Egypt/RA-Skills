---
trigger: always_on
---
# Vue 2 项目专项规则

本规则适用于 Vue 2.x（含 2.7）项目，使用 Options API 风格。

## 版本识别
在执行任何修改前，先确认：
- package.json 中 vue 版本为 ^2.x
- 构建工具为 Vue CLI (@vue/cli) 或 Webpack
- 状态管理为 Vuex（3.x）
- UI 库为 Element UI 或其他 Vue 2 兼容库
如果发现实际是 Vue 3 项目，立即停止并切换到 Vue 3 规则

## 组件规范

### 文件组织
- 单文件组件（SFC）按 template → script → style 顺序排列
- 组件文件名使用 PascalCase：UserProfile.vue
- 每个文件只包含一个组件

### Options API 书写顺序
严格按照以下顺序排列 options：
1. name
2. components
3. directives / filters
4. mixins
5. props
6. data
7. computed
8. watch
9. 生命周期钩子（按执行顺序）：beforeCreate → created → beforeMount → mounted → beforeUpdate → updated → beforeDestroy → destroyed
10. methods

### Props 规范
- props 必须有类型定义，禁止纯数组写法
- 正确：props: { title: { type: String, required: true, default: '' } }
- 错误：props: ['title']
- 必要时提供 validator 函数
- 复杂对象的 default 必须用工厂函数返回

### Data 规范
- data 必须是一个返回对象的函数，禁止直接写对象
- data 中不放与模板无关的变量（不需要响应式的数据放在 created 里用 this.xxx = ... 赋值）

### Computed 与 Watch
- 能用 computed 解决的不用 watch
- watch 中避免复杂逻辑，复杂操作抽到 methods
- 需要 deep watch 时显式声明 deep: true 并注释原因

### 事件规范
- 子组件向父组件通信用 $emit，事件名用 kebab-case
- 禁止滥用 $parent / $children 直接访问
- 禁止滥用 EventBus 做跨层级通信（大范围通信走 Vuex）

## Vuex 规范
- State：只存全局共享数据，组件私有状态留在组件内
- Mutations：只做同步状态变更，命名用 SET_XXX / UPDATE_XXX
- Actions：处理异步逻辑，命名用动词：fetchUserList / submitOrder
- Getters：用于派生状态，等同于 Store 级别的 computed
- 模块化：使用 namespaced: true，按业务领域拆分 module

## 路由规范（Vue Router 3.x）
- 路由配置使用懒加载：component: () => import('@/views/xxx.vue')
- 路由 name 使用 PascalCase，与组件文件名一致
- 路由守卫中的异步操作必须有错误处理
- 禁止在组件内直接操作 window.location，使用 $router

## 样式规范
- 使用 scoped 样式避免全局污染
- 需要穿透子组件时用 ::v-deep 或 /deep/（Vue 2 语法）
- 禁止在 scoped style 中使用标签选择器
- BEM 或项目已有的命名约定（先确认再使用）

## 兼容性注意
- Vue 2 不支持 Fragments（模板只能有一个根元素）
- Vue 2 不支持 Teleport / Suspense
- 数组变更检测限制：使用 Vue.set 或 this.$set 修改数组索引
- 对象新增属性检测限制：使用 Vue.set 或 this.$set 添加新属性
- 如果项目是 Vue 2.7，可使用 Composition API（setup 语法糖除外），但必须先确认项目是否引入了 @vue/composition-api 或已升级到 2.7

## 禁止事项
- 禁止使用已废弃的 API：$on / $off / $once（Vue 2.x 原生支持但 Vue 3 已移除，迁移风险高）
- 禁止在模板中使用复杂的内联表达式（超过一个函数调用的逻辑必须移到 computed 或 methods）
- 禁止修改 props（如需修改，用 data 接收或 computed 转换）
- 禁止在 data 中引用 props 的默认值后不追踪变化（常见 bug）
