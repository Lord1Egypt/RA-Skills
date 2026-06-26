# wechat.bmpi.dev 机制分析

数据来源：抓取 `https://wechat.bmpi.dev/` 的首页与静态资源（`main.1262a36b.chunk.js`、`main.264e641e.chunk.css`）。

## 1) JS 架构机制

- 应用是基于 React + webpack 分包的 SPA，入口挂载到 `#root`。
- Markdown 渲染链路使用 `markdown-it`，并接入 `highlight.js`：
  - 高亮输出结构为 `<pre class="custom"><code class="hljs">...</code></pre>`。
- 页面预览容器在 `section#nice`，HTML 通过 `dangerouslySetInnerHTML` 注入。
- 导出有多目标逻辑：`getWeChatHtml()` / `getZhihuHtml()`。

## 2) 主题注入机制（核心）

前端通过动态创建 4 个 `<style>` 节点分层控制样式：

- `basic-theme`
- `markdown-theme`
- `code-theme`
- `font-theme`

并使用 `po(id, cssText)` 把 CSS 文本写入对应 style 节点。  
这意味着“正文主题”和“代码主题”是天然可独立切换的。

## 3) 状态与持久化

主题与编辑状态大量使用 `localStorage` 存储，例如：

- `theme_list`
- `style`
- `code_num`
- `is_mac_code`
- `template_num`
- `preview_type`

## 4) 主题集合

### 正文主题（模板菜单）

检测到的内置主题名包括：

- 默认主题
- 橙心
- 培紫
- 嫩青
- 绿意
- 红绯
- 蓝莹
- 兰青
- 山吹
- 前端之巅同款
- 极客黑
- 蔷薇紫
- 萌绿
- 全栈蓝
- 极简黑
- 橙蓝风
- 自定义

### 代码主题（可切换 + Mac 风格变体）

- wechat
- atom-one-dark / atom-one-light
- monokai
- github
- vs2015
- xcode
- 以及对应 `mac*` 变体（通过 `is_mac_code` 切换）

## 5) 对脚本实现的启发

复制其关键设计时，必须保持以下约束：

1. 正文与代码主题分层输出，分别写入不同 style block。
2. 代码块统一输出 `.hljs` 结构，便于独立替换 code theme。
3. 可选字体层独立，避免影响主题 CSS 维护。
