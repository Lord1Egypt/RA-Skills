# md-to-pdf

[English](#english) | [中文](#中文)

---

<a id="english"></a>

## English

A Claude Code skill that converts Markdown files to styled PDF documents with CJK support, code syntax highlighting, and clean typography.

### Features

| Feature | Description |
|---------|-------------|
| Headings (H1-H6) | Styled with visual hierarchy and bottom borders |
| Code blocks | Monospace font with light background and borders |
| Tables | Bordered cells with zebra striping |
| Lists | Bulleted and numbered lists |
| Images | Embedded with auto-scaling (relative paths resolved) |
| Links | Clickable hyperlinks in the generated PDF |
| CJK/Chinese | Full Unicode and CJK text support |
| Page numbers | Bottom center by default (optional) |

### Prerequisites

- **Node.js** v18+
- **Google Chrome** or **Microsoft Edge** installed on the system

### Installation

In your target project directory:

```bash
mkdir -p .md-to-pdf-tool && cd .md-to-pdf-tool
npm init -y
npm install marked@4.3.0 puppeteer-core@19.11.1
```

Then copy `convert.js` from this skill directory into `.md-to-pdf-tool/`.

### Usage

```bash
# Basic conversion (outputs input.pdf alongside the .md file)
node convert.js input.md

# Specify output path
node convert.js input.md output.pdf

# Disable page numbers
node convert.js input.md --no-page-numbers
```

### How It Works

1. **marked** parses the Markdown into HTML
2. **puppeteer-core** launches a headless browser (Chrome/Edge)
3. The HTML is rendered with embedded CSS styling
4. `page.pdf()` generates a print-ready A4 PDF

### Customization

Edit the CSS block inside `convert.js` to adjust:

- **Font family** - `body` style's `font-family`
- **Colors** - `color` and `background` values throughout
- **Page margins** - `marginTop`, `marginBottom`, `marginLeft`, `marginRight` options in `page.pdf()`
- **Code theme** - `pre` and `code` background/border colors
- **Page footer** - `footerTemplate` in the PDF options

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `CHROME_PATH` | Override Chrome executable path |
| `EDGE_PATH` | Override Edge executable path |

If neither is set, the script auto-discovers Edge or Chrome from default install locations.

### Troubleshooting

| Problem | Fix |
|---------|-----|
| Browser not found | Set `CHROME_PATH` or `EDGE_PATH` to the browser executable |
| Permission denied | Try Edge instead of Chrome, or run with elevated permissions |
| ESM module errors | Use `marked@4.3.0` and `puppeteer-core@19.11.1` (CommonJS compatible) |
| Large file timeout | Increase the `waitUntil` timeout in `page.setContent()` |

---

<a id="中文"></a>

## 中文

一个 Claude Code 技能，用于将 Markdown 文件转换为带样式的 PDF 文档，支持中日韩文本、代码语法高亮和精美排版。

### 功能特性

| 功能 | 说明 |
|------|------|
| 标题 (H1-H6) | 分层级样式，带底部边框 |
| 代码块 | 等宽字体，浅色背景和边框 |
| 表格 | 带边框单元格，斑马纹间隔行 |
| 列表 | 有序列表和无序列表 |
| 图片 | 自动缩放嵌入（支持相对路径） |
| 链接 | PDF 中可点击的超链接 |
| 中日韩文字 | 完整支持 Unicode 和 CJK 文本 |
| 页码 | 默认底部居中显示（可选） |

### 环境要求

- **Node.js** v18+
- 系统已安装 **Google Chrome** 或 **Microsoft Edge**

### 安装步骤

在目标项目目录下执行：

```bash
mkdir -p .md-to-pdf-tool && cd .md-to-pdf-tool
npm init -y
npm install marked@4.3.0 puppeteer-core@19.11.1
```

然后将本技能目录下的 `convert.js` 复制到 `.md-to-pdf-tool/` 中。

### 使用方法

```bash
# 基本转换（在 .md 文件同目录生成同名 PDF）
node convert.js input.md

# 指定输出路径
node convert.js input.md output.pdf

# 不显示页码
node convert.js input.md --no-page-numbers
```

### 工作原理

1. **marked** 将 Markdown 解析为 HTML
2. **puppeteer-core** 启动无头浏览器（Chrome/Edge）
3. 使用内嵌 CSS 样式渲染 HTML
4. `page.pdf()` 生成可打印的 A4 PDF

### 自定义配置

编辑 `convert.js` 中的 CSS 样式块以调整：

- **字体** - `body` 样式中的 `font-family`
- **颜色** - 各处的 `color` 和 `background` 值
- **页边距** - `page.pdf()` 中的 `marginTop`、`marginBottom`、`marginLeft`、`marginRight` 选项
- **代码主题** - `pre` 和 `code` 的背景色/边框色
- **页脚** - PDF 选项中的 `footerTemplate`

### 环境变量

| 变量名 | 用途 |
|--------|------|
| `CHROME_PATH` | 指定 Chrome 可执行文件路径 |
| `EDGE_PATH` | 指定 Edge 可执行文件路径 |

如果未设置，脚本会自动从默认安装位置查找 Edge 或 Chrome。

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 找不到浏览器 | 设置 `CHROME_PATH` 或 `EDGE_PATH` 环境变量指向浏览器可执行文件 |
| 权限被拒绝 | 尝试使用 Edge 替代 Chrome，或以管理员权限运行 |
| ESM 模块错误 | 使用 `marked@4.3.0` 和 `puppeteer-core@19.11.1`（兼容 CommonJS） |
| 大文件超时 | 增加 `page.setContent()` 中的 `waitUntil` 超时时间 |

---

### File Structure / 目录结构

```
md-to-pdf/
  SKILL.md       # Claude Code skill definition / 技能定义文件
  convert.js     # Conversion script (Node.js) / 转换脚本
  README.md      # This file / 本文件
```
