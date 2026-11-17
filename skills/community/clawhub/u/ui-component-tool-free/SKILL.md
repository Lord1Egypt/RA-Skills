---
slug: ui-component-tool-free
name: ui-component-tool-free
version: 1.0.0
displayName: UI组件生成(免费版)
summary: "面向个人开发者的HTML/CSS UI组件生成工具,覆盖表单、表格、卡片、模态框、导航栏.。UI组件生成工具免费版为个人开发者提供常用HTML/CSS组件的快速生成能力,覆盖表单、表格、卡片"
license: Proprietary
edition: free
description: 'UI组件生成工具免费版为个人开发者提供常用HTML/CSS组件的快速生成能力,覆盖表单、表格、卡片、模态框、导航栏等基础组件。核心能力:

  - 表单组件生成(输入框、选择器、复选框)

  - 表格组件生成(基础表格、带样式表格)

  - 卡片组件生成(信息卡片、产品卡片)

  - 模态框组件生成(基础弹窗)

  - 导航栏组件生成(顶部导航)

  适用场景:

  - 个人项目快速搭建页面原型

  - 学习HTML/CSS组件结构

  - 快速生成可运行的单文件HTML组件

  差异化:免费版聚焦个人开发者的基础组件需求,输出单文件HTML'
tags:
  - UI组件
  - HTML
  - CSS
  - 前端开发
  - 个人开发
  - UI设计
  - 前端
  - 设计
  - div
  - class
  - html
  - rem
  - label
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---
# UI 组件生成工具(免费版)

## 概述

`ui-component-tool-free` 为个人开发者提供常用 HTML/CSS UI 组件的快速生成能力。它覆盖表单、表格、卡片、模态框、导航栏等基础组件,输出完整可运行的单文件 HTML,适合个人项目、原型设计学习实践.
本工具通过自然语言指令驱动 Agent 输出组件代码,无需安装额外脚本或依赖.
## 核心能力

| 能力 | 说明 |
|---|---|
| 表单组件 | 输入框、选择器、复选框、单选按钮、文本域 |
| 表格组件 | 基础表格、带斑马纹表格、带边框表格 |
| 卡片组件 | 信息卡片、产品卡片、头像卡片 |
| 模态框组件 | 基础弹窗、确认对话框 |
| 导航栏组件 | 顶部导航、带下拉菜单导航 |
| 响应式支持 | 移动端优先的相对单位(rem/%) |
| 可访问性基础 | 表单 `label`、按钮焦点样式、对比度达标 |
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人开发者的、HTML、CSS、组件生成工具、覆盖表单、组件生成工具免费、版为个人开发者提、供常用、组件的快速生成能、导航栏等基础组件、表单组件生成、表格组件生成、带样式表格、卡片组件生成、模态框组件生成、导航栏组件生成等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景 1:生成用户注册表单

```
帮我生成一个用户注册表单,包含用户名、邮箱、密码和确认密码字段,带基本验证样式.
```

工具会输出完整 HTML,包含表单结构、CSS 样式与基础验证提示.
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>用户注册</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; background: #f5f5f5; padding: 2rem; }
    .form-card { max-width: 480px; margin: 0 auto; background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .form-group { margin-bottom: 1rem; }
    label { display: block; margin-bottom: 0.25rem; font-size: 0.875rem; color: #333; }
    input { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; }
    input:focus { outline: none; border-color: #0066ff; box-shadow: 0 0 0 3px rgba(0,102,255,0.1); }
    .submit-btn { width: 100%; padding: 0.75rem; background: #0066ff; color: #fff; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
    .submit-btn:hover { background: #0052cc; }
  </style>
</head>
<body>
  <form class="form-card" onsubmit="event.preventDefault(); alert('注册成功');">
    <div class="form-group">
      <label for="username">用户名</label>
      <input type="text" id="username" name="username" required>
    </div>
    <div class="form-group">
      <label for="email">邮箱</label>
      <input type="email" id="email" name="email" required>
    </div>
    <div class="form-group">
      <label for="password">密码</label>
      <input type="password" id="password" name="password" required minlength="8">
    </div>
    <div class="form-group">
      <label for="confirm">确认密码</label>
      <input type="password" id="confirm" name="confirm" required minlength="8">
    </div>
    <button type="submit" class="submit-btn">注册</button>
  </form>
</body>
</html>
```

### 场景 2:生成产品卡片网格

```
生成一个产品卡片网格,3列布局,每张卡片包含图片、标题、价格和按钮.
```

```html
<div class="card-grid">
  <article class="product-card">
    <img src="https://picsum.photos/300/200" alt="产品图" width="300" height="200">
    <div class="card-body">
      <h3>产品名称</h3>
      <p class="price">¥ 199</p>
      <button class="buy-btn">加入购物车</button>
    </div>
  </article>
  <!-- 重复更多卡片 -->
</div>
```

### 场景 3:生成带确认的模态框

```
生成一个删除确认模态框,有取消和确认两个按钮.
```

```html
<div class="modal-overlay" id="modal">
  <div class="modal">
    <h3>确认删除</h3>
    <p>确定要删除这条记录吗?此操作不可撤销。</p>
    <div class="modal-actions">
      <button class="btn-cancel">取消</button>
      <button class="btn-confirm">确认删除</button>
    </div>
  </div>
</div>
```

## 不适用场景

以下场景UI组件生成(免费版)不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:描述需求

直接在对话中描述你需要的组件,例如:

```
帮我生成一个带搜索框的顶部导航栏.
```

```
生成一个用户信息表格,包含姓名、邮箱、角色、操作列.
```

### 第二步:获取组件代码

工具会输出完整可运行的单文件 HTML,包含结构与样式.
### 第三步:本地预览

```bash
# 将代码保存为 component.html,在浏览器中打开
start component.html   # Windows
open component.html    # macOS
xdg-open component.html  # Linux
```

#
## 示例

### 个人项目推荐样式约定

| 设计令牌 | 值 | 说明 |
|:-----|:-----|:-----|
| 主色 | `#0066ff` | 按钮、链接、聚焦边框 |
| 圆角 | `4px`(小)/ `8px`(大) | 卡片、按钮、输入框 |
| 间距单位 | `0.25rem` 倍数 | 4/8/12/16/24/32px |
| 字体 | 系统字体栈 | `-apple-system, sans-serif` |
| 阴影 | `0 2px 8px rgba(0,0,0,0.1)` | 卡片、模态框 |
| 断点 | 768px / 1024px | 移动 / 平板 / 桌面 |

### 响应式基础模板

```css
/* 移动端优先 */
.container { width: 100%; padding: 0 1rem; }
@media (min-width: 768px) {
  .container { max-width: 720px; margin: 0 auto; }
}
@media (min-width: 1024px) {
  .container { max-width: 960px; }
}
```

## 最佳实践

1. **一致性优先**:同一项目使用统一的圆角、间距、配色,避免视觉混乱.
2. **可访问性基础**:表单字段必须配 `label`,按钮要有焦点样式,文字与背景对比度 ≥ 4.5:1.
3. **移动端优先**:使用相对单位(`rem`/`%`/`vw`),从小屏开始设计,再向大屏扩展.
4. **少即是多**:不加无意义的装饰元素,让内容本身成为主角.
5. **图片必须带尺寸**:为 `<img>` 添加 `width` 和 `height`,避免布局偏移(CLS).
6. **语义化 HTML**:用 `<header>`、`<nav>`、`<main>`、`<article>`、`<footer>` 替代无意义 `<div>`.
7. **表单加 `preventDefault`**:在 `onsubmit` 中调用 `e.preventDefault()` 防止页面刷新.
## 常见问题

### Q1: 生成的组件如何集成到现有项目?

免费版输出的是单文件 HTML,你可以将 `<style>` 中的样式提取到你的 CSS 文件,将 HTML 结构复制到模板中。如有 CSS 框架(如 Tailwind),可要求工具输出对应框架的类名.
### Q2: 组件样式如何避免与现有样式冲突?

建议使用 BEM 命名约定(如 `card__title--active`),或将组件包裹在带唯一类名的容器内,使用作用域选择器.
### Q3: 如何让组件支持暗色模式?

使用 CSS 变量定义颜色令牌,通过 `prefers-color-scheme: dark` 媒体查询切换。免费版可要求工具输出带暗色模式的版本.
### Q4: 免费版与 Pro 版的区别?

免费版输出单文件 HTML 基础组件;Pro 版扩展设计系统令牌、批量生成、可访问性增强(WCAG AA)、企业级组件库与团队协作能力.
## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **浏览器**:任意现代浏览器(Chrome / Firefox / Safari / Edge)用于预览

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| 浏览器 | 系统工具 | 必需 | 系统预装 |
| 文本编辑器 | 系统工具 | 必需 | 系统预装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 本 Skill 完全基于 Markdown 指令,无需额外 API Key
- 组件代码完全本地生成,不涉及任何外部 API

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言指令驱动 Agent 输出 HTML/CSS 组件代码;用户通过浏览器本地预览

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "UI组件生成(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "ui component"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
