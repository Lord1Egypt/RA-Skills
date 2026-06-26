# Slidev Assist 🦐📽️

**一个 AI Skill：任何原材料 → AI 解析 → Slidev PPT → 一键预览+导出。**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-FF4500)](https://clawhub.ai)
[![Slidev](https://img.shields.io/badge/Slidev-v52-blue)](https://sli.dev)

---

## ⚠️ 关于本项目

**Slidev Assist 不是一个独立或原创的软件，而是一个调用开源项目的辅助工具。**

它的核心依赖是 [**Slidev**](https://github.com/slidevjs/slidev)（一个用 Markdown 写 PPT 的开源项目，MIT 协议），项目地址：

👉 **https://github.com/slidevjs/slidev**

Slidev 能生成效果酷炫的演示内容，但对电脑小白来说门槛较高——需要装 Node.js、记 Markdown 语法和 frontmatter 配置。

**Slidev Assist 的作用就是让小白也能用上这个好工具：你不需要懂命令行，不需要记语法，只要给个主题或原材料，5 分钟内就能生成一份可用的演示内容。**

---

## 什么是 Slidev Assist？

[Slidev](https://sli.dev) 是一个用 Markdown 写 PPT 的工具——但小白入门门槛高（要装 Node.js、记语法、搞 frontmatter）。

**Slidev Assist 是一个 OpenClaw Skill，让 AI 替你完成从"原材料"到"PPT"的全过程。**

> **你给什么，我就能做什么。**
> 一个主题 → 做成 PPT
> 一份研究报告 → 提炼成 PPT
> 一堆数据 → 汇报成 PPT
> 一段文案 → 排版成 PPT
> 一个 PPTX → 转成 Slidev 版

### 工作流程

```
你提供原材料（主题/文件/数据/文案...）
  → AI 解析提炼 → 结构化成 slides.md
    → exec npm install + npx slidev
      → 浏览器预览 → 导出 PDF/PPTX
```

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub
openclaw skills install slidev-assist

# 或从 GitHub 本地安装
openclaw skills install ./slidev-assist
```

### 使用

安装后，在对话里说任意一种：

> "帮我做一个关于 XX 的 PPT"（纯主题）
> "读了这份报告，帮我提炼成10页PPT"（PDF/文件）
> "这些数据做成汇报PPT"（Excel/表格）
> "这个PPTX帮我转成Slidev版"（已有文件）
> "这段文字帮我做成演示"（文案稿件）

AI 会自动完成：**解析 → 提炼 → 结构化 → 生成 slides.md → 启动预览 → 导出成品**

---

## ✨ 核心功能

| 功能 | 说明 |
|:----|:-----|
| 💬 **主题 → PPT** | 你说主题，AI 构思内容大纲并生成完整演示 |
| 📄 **文件 → PPT** | 研究报告/PDF/文案 → 提炼要点 → 结构化 |
| 📊 **数据 → PPT** | Excel/CSV → 提取结论 → 图表化展示 |
| 🎞️ **PPTX → Slidev** | 读取已有 PPTX 转成带劲效的 Slidev 版 |
| 🔗 **网页 → PPT** | 抓取内容 → 摘要 → 知识整理演示 |
| 📚 **多源混搭** | 多个材料合并成一个统一汇报 |
| 🎨 **布局与动效** | cover / two-cols / v-click / transition |
| 📤 **一键导出** | PDF / PPTX / PNG |

---

## 🗂️ 项目结构

```
slidev-assist/
├── SKILL.md               ← AI 语法指南 + 工作流
├── metadata.json          ← 元数据
├── references/
│   └── quickref.md        ← 速查手册（主题/布局/命令）
├── scripts/
│   └── init-slidev.sh     ← 自动初始化脚本
├── assets/
│   ├── template-default.md  ← 默认内容模板
│   ├── template-cover.md    ← 封面页模板
│   └── template-section.md  ← 章节页模板
├── README.md
├── CHANGELOG.md
├── LICENSE (MIT)
└── .gitignore
```

---

## 📖 使用示例

### 纯主题生成

```
你：帮我做一个"AI Agent 入门"的 PPT，10页左右
AI：好的，我构思内容大纲……
AI：写 slides.md……安装依赖……启动预览……
AI：好了！http://localhost:3030/
```

### 文件导入

```
你：https://xxx.com/research.pdf
     帮我读这报告做个PPT
AI：抓取内容 → 提炼核心论据……
AI：生成 slides.md → 启动预览……
AI：http://localhost:3031/
```

### 已有 PPTX 转换

```
你：帮我读这个PPTX，转成Slidev版
AI：用 python-pptx 解析37页内容……
AI：重新结构化，添加动效……
AI：http://localhost:3032/
```

### 调整内容

```
你：第5页内容太多了
AI：拆成两页
你：加点动效
AI：添加 v-click 过渡
```

---

## 🛠️ 技术栈

- [Slidev](https://sli.dev) — 演示框架
- [Vite](https://vitejs.dev) — 构建工具
- [Vue 3](https://vuejs.org) — 组件引擎
- [UnoCSS](https://unocss.dev) — 工具类 CSS
- [python-pptx](https://python-pptx.readthedocs.io) — PPTX 解析
- [Playwright](https://playwright.dev) — PDF/PPTX 导出

---

## 📦 发布

```bash
# ClawHub 发布
clawhub publish ./slidev-assist --slug slidev-assist --name "Slidev Assist" --version 1.0.0

# 本地安装测试
openclaw skills install ./slidev-assist
```

---

## 📄 License

[MIT](LICENSE)
