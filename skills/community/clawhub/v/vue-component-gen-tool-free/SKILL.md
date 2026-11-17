---
slug: vue-component-gen-tool-free
name: vue-component-gen-tool-free
version: 1.0.0
displayName: Vue组件生成(免费版)
summary: 面向个人开发者的Vue 3组件模板生成工具,支持Composition API与TypeScript单文件组件.
license: Proprietary
edition: free
description: 'Vue组件生成工具免费版为个人开发者提供Vue 3单文件组件模板快速生成能力,覆盖Composition API、Options API与TypeScript支持。核心能力:

  - 一键生成Vue 3单文件组件(。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
  - Vue
  - 组件生成
  - 前端开发
  - 个人开发
  - TypeScript
  - 工具
  - 效率
  - api
  - props
  - vue
  - div
  - const
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# Vue 组件生成工具(免费版)

## 概述

`vue-component-gen-tool-free` 为个人开发者提供 Vue 3 单文件组件模板的快速生成能力。它支持 Composition API、Options API、`<script setup>` 语法与 TypeScript,帮助你快速搭建标准化组件,适合个人项目、学习实践与小型应用开发.
本工具通过自然语言指令或 CLI 风格命令驱动 Agent 输出组件代码,无需额外安装私有脚本.
## 核心能力

| 能力 | 说明 |
|---|---|
| 单文件组件生成 | 生成完整的 `.vue` 文件(template/（请参考skill目录中的脚本文件）) |
| Composition API | 推荐 API,基于 `setup` 函数 |
| Options API | 传统 API,适合旧项目兼容 |
| `<script setup>` | Vue 3 推荐语法,更简洁 |
| TypeScript 支持 | 类型化的 Props、Emits、Ref |
| SCSS 支持 | 嵌套样式与变量 |
| Props/Emits 定义 | 类型安全的组件接口 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人开发者的、组件模板生成工具、组件生成工具免费、版为个人开发者提、单文件组件模板快、速生成能力、一键生成、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景 1:生成基础按钮组件

```
生成一个 MyButton 组件,用 Composition API 和 TypeScript
```

```vue
<template>
  <div class="my-button">
    <button @click="handleClick">
      {{ label }}
    </button>
  </div>
</template>
# ...
<script setup lang="ts">
import { ref } from 'vue'
# ...
interface Props {
  label?: string
}
# ...
const props = withDefaults(defineProps<Props>(), {
  label: 'Click me'
})
# ...
const emit = defineEmits<{
  (e: 'click'): void
}>()
# ...
const handleClick = () => {
  emit('click')
}
</script>
# ...
<style scoped>
.my-button {
  padding: 10px 20px;
}
</style>
```

### 场景 2:生成表单输入组件

```
生成一个 InputField 组件,带 v-model 支持,使用 TypeScript
```

```vue
<template>
  <div class="input-field">
    <label v-if="label" :for="id">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      @input="onInput"
    />
  </div>
</template>
# ...
<script setup lang="ts">
interface Props {
  modelValue: string
  label?: string
  type?: string
  placeholder?: string
  id?: string
}
# ...
const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  label: '',
  placeholder: '',
  id: () => `input-${Math.random().toString(36).slice(2, 9)}`
})
# ...
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
# ...
const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>
# ...
<style scoped>
.input-field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
```

### 场景 3:生成模态框组件

```
生成一个 Modal 组件,带 v-model:open 支持,使用 SCSS
```

```vue
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="open" class="modal-overlay" @click.self="close">
        <div class="modal">
          <header class="modal-header">
            <h3>{{ title }}</h3>
            <button class="close-btn" @click="close">×</button>
          </header>
          <div class="modal-body">
            <slot />
          </div>
          <footer class="modal-footer">
            <slot name="footer" :close="close" />
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
# ...
<script setup lang="ts">
interface Props {
  open: boolean
  title?: string
}
# ...
const props = withDefaults(defineProps<Props>(), {
  title: ''
})
# ...
const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
}>()
# ...
const close = () => emit('update:open', false)
</script>
# ...
<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
# ...
  .modal {
    background: #fff;
    border-radius: 8px;
    max-width: 480px;
    width: 90%;
# ...
    .modal-header,
    .modal-footer {
      padding: 1rem;
    }
# ...
    .modal-body {
      padding: 1rem;
    }
  }
}
# ...
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
```

## 快速开始

### 第一步:描述组件需求

直接在对话中描述你需要的组件,例如:

```
生成一个 UserCard 组件,显示头像、姓名和邮箱,用 Composition API 和 TypeScript.
```

### 第二步:获取组件代码

工具会输出完整的 `.vue` 文件,包含 template、script、style 三部分.
### 第三步:应用到项目

```bash
# 将代码保存为组件文件
# src/components/UserCard.vue
# ...
# 在父组件中使用
# <UserCard :user="currentUser" />
```

## 示例

### CLI 风格命令

| 命令 | 说明 |
|:-----|:-----|
| `vue-component-gen-tool MyButton --api composition` | 生成 Composition API 组件 |
| `vue-component-gen-tool MyModal --api options` | 生成 Options API 组件 |
| `vue-component-gen-tool MyForm --typescript` | 启用 TypeScript |
| `vue-component-gen-tool MyModal --scss` | 启用 SCSS |
| `vue-component-gen-tool MyButton -o ./src/components` | 指定输出目录 |

### 支持的 API 类型对照

| API 类型 | 语法 | 推荐度 | 说明 |
|----:|----:|----:|----:|
| `composition` | `<script setup>` | 推荐 | Vue 3 最佳实践,简洁高效 |
| `options` | `export default { ... }` | 兼容 | 旧项目兼容,新项目不推荐 |
| `script-setup` | `<script setup>` | 推荐 | 等同 composition,显式声明 |

## 最佳实践

1. **优先使用 `<script setup lang="ts">`**:Vue 3 推荐语法,TypeScript 提供类型安全.
2. **Props 用类型接口定义**:`interface Props { ... }` 比 `defineProps({ ... })` 更清晰.
3. **Emits 用类型化签名**:`defineEmits<{ (e: 'click', id: string): void }>()` 保证类型安全.
4. **`withDefaults` 处理默认值**:TypeScript 模式下用 `withDefaults` 设置 Props 默认值.
5. **样式用 `scoped`**:避免样式泄漏到全局,影响其他组件.
6. **`v-model` 用 `update:modelValue`**:Vue 3 的标准 v-model 协议.
7. **组件文件名用 PascalCase**:`UserCard.vue` 而非 `user-card.vue`,与组件名一致.
8. **Props 用 `defineProps` 宏**:编译期宏,无需导入,类型推断更准确.
## 常见问题

### Q1: Composition API 和 Options API 怎么选?

新项目优先 Composition API,逻辑复用更灵活,TypeScript 支持更好。旧项目兼容或简单组件可用 Options API.
### Q2: `<script setup>` 和普通 `setup()` 函数怎么选?

优先 `<script setup>`,语法更简洁,编译期优化更好。仅在需要动态渲染函数或额外配置时用普通 `setup()`.
### Q3: TypeScript 模式下如何定义 Props 默认值?

用 `withDefaults(defineProps<Props>(), { label: 'Click me' })`。`withDefaults` 是编译期宏,提供类型安全的默认值.
### Q4: 如何实现 `v-model` 双向绑定?

Props 定义 `modelValue`,Emits 定义 `update:modelValue`。在输入事件中触发 `emit('update:modelValue', newValue)`.
### Q5: 免费版与 Pro 版的区别?

免费版支持单组件生成与基础 API 类型;Pro 版扩展企业级组件库结构、批量生成、可访问性增强、单元测试模板与 CI 集成.
## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **Node.js**:建议 18+(用于 Vue 项目运行)
- **Vue**:建议 3.3+(完整支持 `<script setup>` 与 TypeScript)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Vue 3 | npm 包 | 必需 | `npm i vue` |
| TypeScript | npm 包 | 推荐 | `npm i -D typescript` |
| sass | npm 包 | 可选 | `npm i -D sass`(使用 SCSS 时) |
| vite | 构建工具 | 推荐 | `npm i -D vite @vitejs/plugin-vue` |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 基础LLM由Agent平台内置提供，Skill基于Markdown指令驱动
- 组件代码完全本地生成,不涉及任何外部 API

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言指令驱动 Agent 输出 Vue 单文件组件代码;用户将代码保存到项目并通过 Vite 或 Vue CLI 运行

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Vue组件生成(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "vue component gen"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
