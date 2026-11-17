# 笔记模板参考

以下模板展示了不同来源类型的 Obsidian 笔记格式。

**核心规则（不可违反）**：
- ✅ tags 必须使用多行列表格式
- ✅ 日期必须使用 YYYY-MM-DD 格式
- ✅ 必须包含 fetch_tool 来源追踪字段
- ❌ 禁止 tags: [a, b, c] inline 格式
- ❌ 禁止 ISO datetime 格式

---

## 1. 标准技术文档笔记（opencli 抓取）

```markdown
---
title: "React 18 安装与使用指南"
source: "https://react.dev/docs/getting-started"
created: 2026-07-02
fetch_tool: "opencli"
tags:
  - web-clip
  - react
  - frontend
  - installation
  - guide
---

# React 18 安装与使用指南

> [!note]- 来源信息
> - **URL**: https://react.dev/docs/getting-started
> - **抓取时间**: 2026-07-02 15:30
> - **抓取工具**: opencli
> - **内容大小**: 约 12 KB

## 安装

使用 npm 安装 React：

```bash
npm install react react-dom
```

或者使用 yarn：

```bash
yarn add react react-dom
```

## 快速开始

创建你的第一个 React 组件...
```

---

## 2. GitHub README 笔记

```markdown
---
title: "Starship - 跨 shell 提示符工具"
source: "https://github.com/starship/starship"
created: 2026-07-02
fetch_tool: "fetchGithubReadme"
tags:
  - web-clip
  - github
  - readme
  - rust
  - shell
  - cli
---

# Starship

> [!note]- 来源信息
> - **仓库**: https://github.com/starship/starship
> - **抓取时间**: 2026-07-02 15:45
> - **抓取工具**: fetchGithubReadme

Starship 是一个适用于任何 shell 的最小、极速、无限可定制的提示符工具...

## 安装

```bash
curl -sS https://starship.rs/install.sh | sh
```

## 配置

在 `~/.config/starship.toml` 中配置...
```

---

## 3. 技术博客笔记（Firecrawl 抓取，含降级说明）

```markdown
---
title: "Understanding React Server Components"
source: "https://example.com/blog/react-server-components"
created: 2026-07-02
fetch_tool: "firecrawl"
tags:
  - web-clip
  - react
  - rsc
  - tutorial
  - nextjs
---

# Understanding React Server Components

> [!note]- 来源信息
> - **URL**: https://example.com/blog/react-server-components
> - **抓取时间**: 2026-07-02 16:00
> - **抓取工具**: firecrawl（opencli daemon 未运行，自动降级）
> - **内容大小**: 约 25 KB

React Server Components (RSC) 代表了 React 渲染模型的一个根本性转变...
```

---

## 4. API 文档笔记（fetchWebContent 抓取）

```markdown
---
title: "OpenAI API Reference"
source: "https://platform.openai.com/docs/api-reference"
created: 2026-07-02
fetch_tool: "fetchWebContent"
tags:
  - web-clip
  - api
  - openai
  - reference
  - llm
---

# OpenAI API Reference

> [!note]- 来源信息
> - **URL**: https://platform.openai.com/docs/api-reference
> - **抓取时间**: 2026-07-02 16:15
> - **抓取工具**: fetchWebContent
> - **内容大小**: 约 8 KB

## Chat Completions

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| model | string | 是 | 使用的模型 ID |
| messages | array | 是 | 消息列表 |
| temperature | number | 否 | 采样温度 |
```

---

## 5. 内容过长截断笔记

```markdown
---
title: "Complete Linux Kernel Documentation"
source: "https://docs.kernel.org/admin-guide/README.html"
created: 2026-07-02
fetch_tool: "opencli"
tags:
  - web-clip
  - linux
  - kernel
  - documentation
  - reference
---

# Complete Linux Kernel Documentation

> [!note]- 来源信息
> - **URL**: https://docs.kernel.org/admin-guide/README.html
> - **抓取时间**: 2026-07-02 16:30
> - **抓取工具**: opencli
> - **内容大小**: 约 78 KB（已截断，原始 250 KB）

<正文内容...>

> [!warning] 内容过长已截断
> 原始约 250 KB，保存约 78 KB。完整内容请访问原始 URL: https://docs.kernel.org/admin-guide/README.html
```
