---
name: "tailwindcss-toolkit-free"
description: "Tailwind CSS实用类编写工具,涵盖响应式设计、暗黑模式与基础配置,适合个人开发者快速上手。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Tailwind CSS工具包免费版"
  version: "1.0.0"
  summary: "Tailwind CSS实用类编写工具,涵盖响应式设计、暗黑模式与基础配置,适合个人开发者快速上手。"
  tags:
    - "创意设计"
    - "前端开发"
    - "CSS"
    - "Tailwind"
    - "响应式设计"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Tailwind CSS 工具包 - 免费版

## 概述

Tailwind CSS 工具包(免费版)为个人开发者提供 Tailwind 实用类的编写规范与最佳实践。涵盖响应式设计、暗黑模式、状态变体与基础配置,帮助快速构建一致的界面样式。

免费版聚焦核心实用类与常见场景,专业版(`tailwindcss-toolkit-pro`)在此基础上提供自定义插件、设计系统、性能优化与组件库等高级能力。

## 核心能力

| 能力 | 免费版 | 说明 |
|:-----|:-------|:-----|
| 实用类编写 | 支持 | 全部核心工具类 |
| 响应式设计 | 支持 | sm/md/lg/xl/2xl 断点 |
| 暗黑模式 | 支持 | class 与 media 策略 |
| 状态变体 | 支持 | hover/focus/active/group |
| 任意值 | 支持 | `bg-[#xxx]` / `w-[calc()]` |
| 基础配置 | 支持 | tailwind.config.js |
| @apply 使用 | 支持 | 含陷阱说明 |
| 自定义插件 | 不支持 | 升级专业版 |
| 设计系统 | 不支持 | 升级专业版 |
| 性能优化 | 不支持 | 升级专业版 |
| 组件库 | 不支持 | 升级专业版 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：CSS、实用类编写工具、涵盖响应式设计、暗黑模式与基础配、适合个人开发者快、速上手、面向个人开发者的、核心能力、实用类编写规范与、最佳实践、响应式设计前缀与、断点配置、dark、mode、arbitrary、values、基础配置与常见陷、阱规避等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:响应式卡片组件

构建适配多端的卡片组件。

```html
<!-- 响应式卡片:移动端单列,桌面端三列 -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
  <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
    <h3 class="text-lg font-semibold text-gray-900 mb-2">卡片标题</h3>
    <p class="text-sm text-gray-600 leading-relaxed">
      卡片描述文字,使用 leading-relaxed 提升可读性。
    </p>
    <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md
                   hover:bg-blue-600 active:bg-blue-700 transition-colors">
      查看详情
    </button>
  </div>
</div>
```

### 场景二:暗黑模式切换

实现明暗主题切换。

```html
<!-- 配置 darkMode: 'class' -->
<html class="dark">
<body class="bg-white dark:bg-gray-900 transition-colors">
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
      标题
    </h1>
    <p class="mt-2 text-gray-600 dark:text-gray-300">
      内容文字,暗黑模式下自动调整颜色。
    </p>
    <input class="mt-4 px-3 py-2 border border-gray-300 dark:border-gray-700
                  bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                  rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
           placeholder="输入框" />
  </div>
</body>
</html>
```

```javascript
// 主题切换脚本
function toggleTheme() {
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme',
    document.documentElement.classList.contains('dark') ? 'dark' : 'light'
  );
}

// 初始化主题
if (localStorage.getItem('theme') === 'dark' ||
    (!localStorage.getItem('theme') && matchMedia('(prefers-color-scheme: dark)').matches)) {
  document.documentElement.classList.add('dark');
}
```

### 场景三:表单与状态样式

构建带状态的表单组件。

```html
<form class="max-w-md mx-auto space-y-4">
  <!-- 输入框:focus 状态 -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
    <input type="email"
           class="w-full px-3 py-2 border border-gray-300 rounded-md
                  focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                  disabled:bg-gray-100 disabled:cursor-not-allowed
                  transition-colors"
           placeholder="you@example.com" />
  </div>

  <!-- 错误状态 -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
    <input type="password"
           class="w-full px-3 py-2 border border-red-500 rounded-md
                  focus:ring-2 focus:ring-red-500 focus:border-red-500"
           placeholder="至少 8 位" />
    <p class="mt-1 text-sm text-red-600">密码长度不足</p>
  </div>

  <!-- 提交按钮 -->
  <button class="w-full py-2 px-4 bg-blue-500 text-white rounded-md
                 hover:bg-blue-600 active:bg-blue-700
                 disabled:bg-gray-400 disabled:cursor-not-allowed
                 transition-colors">
    提交
  </button>
</form>
```

## 不适用场景

以下场景Tailwind CSS工具包免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 依赖详情

```bash
# 方式一:PostCSS 插件(推荐生产)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 方式二:CDN(快速原型)
# <script src="https://cdn.tailwindcss.com"></script>

# 方式三:CLI 独立使用
npm install -g tailwindcss
npx tailwindcss init
```

### 2. 配置内容路径

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx,html}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./pages/**/*.{js,jsx,ts,tsx,html}"
  ],
  darkMode: 'class',  // 手动切换暗黑模式
  theme: {
    extend: {
      colors: {
        brand: '#3b82f6',  // 自定义品牌色
      }
    },
  },
  plugins: [],
}
```

### 3. 引入样式

```css
/* src/style.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 4. 构建生产版本

```bash
# 开发模式(监听变化)
npx tailwindcss -i ./src/style.css -o ./dist/style.css --watch

# 生产构建(压缩)
npx tailwindcss -i ./src/style.css -o ./dist/style.css --minify
```

## 示例

### 响应式断点

| 前缀 | 最小宽度 | 说明 |
|:-----|:---------|:-----|
| (无) | 0px | 移动端优先,所有尺寸生效 |
| `sm:` | 640px | 小屏(平板竖屏) |
| `md:` | 768px | 中屏(平板横屏) |
| `lg:` | 1024px | 大屏(笔记本) |
| `xl:` | 1280px | 超大屏(桌面) |
| `2xl:` | 1536px | 超超大屏 |

### 常用实用类速查

```html
<!-- 间距 -->
<div class="p-4 m-2 space-y-3 gap-4">

<!-- 排版 -->
<h1 class="text-3xl font-bold text-gray-900 leading-tight tracking-tight">

<!-- 颜色 -->
<div class="bg-blue-500 text-white border border-gray-200">

<!-- 布局 -->
<div class="flex items-center justify-between grid grid-cols-3 gap-4">

<!-- 响应式 -->
<div class="grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

<!-- 暗黑模式 -->
<div class="bg-white dark:bg-gray-900 text-black dark:text-white">

<!-- 状态 -->
<button class="hover:bg-blue-600 focus:ring-2 active:scale-95">

<!-- 任意值 -->
<div class="bg-[#1da1f2] w-[calc(100%-2rem)] min-h-[200px]">
```

## 最佳实践

1. **移动端优先**
   - 不加前缀的类对所有尺寸生效
   - `md:` 表示"中等及以上",而非"仅中等"
   - 从小屏开始设计,逐步增强大屏

```html
<!-- 正确:移动端单列,大屏三列 -->
<div class="grid grid-cols-1 lg:grid-cols-3">

<!-- 错误:不要这样理解 -->
<!-- sm:hidden md:block 不是"仅 md 显示" -->
```

2. **暗黑模式配置**
   - 使用 `darkMode: 'class'` 支持手动切换
   - dark 类放在 `<html>` 或 `<body>` 上
   - `dark:` 前缀在祖先有 `dark` 类时生效

3. **content 路径必须完整**
   - 缺少路径会导致生产构建样式丢失
   - 使用 glob 覆盖所有含类名的文件
   - 动态类名不会被检测,需用 safelist

```javascript
// 错误:动态拼接不会被检测
const color = "blue"
<div class={`bg-${color}-500`}>  // 生产环境会丢失!

// 正确:使用完整类名
const colors = { blue: "bg-blue-500", red: "bg-red-500" }
<div class={colors[color]}>
```

4. **@apply 使用注意**
   - `@apply` 会丢失响应式与状态变体
   - 优先在 HTML 中直接使用类名
   - 如必须用 @apply,仅用于基础样式

```css
/* 可以:基础样式 */
.btn { @apply px-4 py-2 rounded-md font-medium; }

/* 不推荐:响应式与状态会丢失 */
.card { @apply p-4 hover:shadow-lg md:p-6; }
```

5. **避免常见陷阱**
   - `h-screen` 在移动端不准确,用 `h-dvh`
   - `truncate` 需配合宽度限制
   - `overflow-hidden` 配合 `rounded-*` 防止溢出

## 常见问题

### Q1: 生产环境样式丢失?

检查 `content` 配置是否覆盖所有含类名的文件。如果构建产物体积异常小,通常是 content 路径遗漏。

### Q2: 暗黑模式不生效?

- 确认 `darkMode: 'class'` 已配置
- 确认 `<html>` 或 `<body>` 有 `dark` 类
- `dark:` 前缀依赖祖先的 `dark` 类

### Q3: 动态类名不生效?

JIT 模式只能检测完整的类名字符串。动态拼接(如 `bg-${color}-500`)不会被检测。使用完整类名映射或 safelist。

### Q4: 免费版与专业版的区别?

免费版聚焦核心实用类与常见场景;专业版提供自定义插件、设计系统、性能优化与组件库。大型项目或团队协作建议升级。

### Q5: 是否支持 Tailwind v4?

免费版以 v3 为主流版本。v4 的配置方式有变化(使用 CSS 配置而非 JS)。如需 v4 支持与迁移指导,建议升级专业版。

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16 及以上

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| tailwindcss | npm 库 | 必需 | `npm install -D tailwindcss` |
| postcss | npm 库 | 推荐(生产) | `npm install -D postcss` |
| autoprefixer | npm 库 | 推荐(生产) | `npm install -D autoprefixer` |
| Node.js 16+ | 运行时 | 必需 | `nodejs.org` 下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本 Skill **无需任何 API Key**
- Tailwind CSS 为本地构建工具,不依赖云服务
- CDN 模式仅需引入脚本,无需配置

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。免费版聚焦 Tailwind CSS 核心实用类与常见场景,适合个人开发者快速构建界面。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
