---
name: send-md-as
description: "在即时通讯 app 中以优雅图片形式展示 Markdown。支持标题、代码高亮（行号、Monokai）、LaTeX 公式、Mermaid 图表、表格、列表。4 种色彩主题，智能分页。渲染阶段零 CDN 依赖（安装时需网络下载依赖）。| Render Markdown as a polished image for messaging apps. Supports code highlighting, LaTeX, Mermaid diagrams, tables. 4 themes, smart page split. Zero CDN at render time (deps downloaded at install)."
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires":
          {
            "bins": ["python3"],
          },
        "install":
          [
            {
              "id": "setup",
              "kind": "script",
              "script": "setup.sh",
              "label": "Run setup.sh to install dependencies",
            },
          ],
      }
  }
---

# send-md-as (v0.4.1)

Render Markdown as a polished image (JPEG / PNG / WebP / PDF) and send it via `openclaw message send --media`.
将 Markdown 渲染为精美图片，通过 `openclaw message send --media` 发送。
适用于不原生支持 Markdown 的聊天渠道（如微信/WeChat）。

**Manual trigger only / 完全手动触发** — Only use when user explicitly asks to render. Do not auto-detect. / 用户主动要求渲染时使用，不自动判断。

**Default behavior / 默认行为** — No cropping, no page split. Output complete single image. Only use `--pages` when user explicitly requests pagination. PDF naturally paginated via Playwright PDF API. / 不裁剪不分页，输出完整单张图片。仅在用户明确要求分页时使用 `--pages`。输出 PDF 时自然分页（Playwright PDF API）。

---

## Usage / 使用方式

```bash
# Basic render / 基础渲染
bash render.sh input.md output.jpg

# With theme / 指定主题
bash render.sh --theme dark input.md output.jpg

# With page split / 自动分页（仅当用户明确要求时使用）
bash render.sh --pages a5 input.md output.jpg

# Output format / 输出格式
bash render.sh --format pdf input.md output.pdf
bash render.sh --format png input.md output.png

# Combined / 组合使用
bash render.sh --theme nord --pages a4 --format png input.md output.png

# Send via channel / 通过渠道发送
openclaw message send --channel <channel> --target "<id>" --media output.jpg
```

### Hard Rules / 硬性规则

- **Never crop or paginate without explicit user request / 禁止自作主张裁剪/分页**。默认输出完整内容，不丢任何部分。只有用户明确要求分页时才用 `--pages`。
- **Prefer PDF for long content / 内容较长时优先选 PDF**（PDF 自然分页，图片会超长）。

---

## Options / 选项

| Option 选项 | Values 值 | Default 默认 | Description 说明 |
|------------|-----------|-------------|-----------------|
| `--theme` | `light`, `dark`, `sepia`, `nord` | `light` | Color theme 色彩主题 |
| `--pages` | `none`, `a4`, `a5` | `none` | Page split mode 分页模式（图片模式有效）|
| `--format` | `jpg`, `png`, `webp`, `pdf` | `jpg` | Output format 输出格式 |

---

## Setup / 安装

```bash
bash /path/to/skills/send-md-as/setup.sh
```

---

## Dependencies / 依赖

| Item 组件 | Required 必需 | Notes 说明 |
|----------|-------------|-----------|
| python3 | Yes 是 | Runtime 运行时 |
| playwright | Yes 是 | 渲染引擎（截图 / PDF） |
| python3-pillow | Yes 是 | Page split 分页处理 |
| python3-mistune | Yes 是 | Markdown parser Markdown 解析器 |
| nh3 | Yes 是 | HTML sanitization HTML 消毒 |
| python3-pygments | No 否 | Syntax highlighting 语法高亮 |
| katex (npm) | No 否 | LaTeX offline rendering LaTeX 离线渲染 |
| mermaid-cli (npm) | No 否 | Diagram rendering 图表渲染 |

---

## Features / 功能

- Headings (h1–h3), bold, italic, inline code / 标题、加粗、斜体、行内代码
- Code blocks — line numbers, Monokai/nord syntax highlighting (Pygments), auto word-wrap / 代码块—行号、Monokai/nord 高亮、自动换行
- LaTeX — inline `$...$` and display `$$...$$` (KaTeX CLI, offline) / LaTeX 公式—KaTeX CLI 离线渲染
- Mermaid diagrams (rendered as SVG) with styled fallback placeholder / Mermaid 图表—SVG 渲染，失败时优雅降级
- Unordered/ordered lists, blockquotes, horizontal rules, links, tables / 列表、引用、分割线、链接、表格
- Task lists / GitHub 风格任务列表 (`- [ ]` / `- [x]`)
- **4 color themes**: light, dark, sepia, nord / 4 种色彩主题
- **Smart page splitting**: none, A4, A5 (blank-row + heading-aware breakpoints) / 智能分页
- **Multi-format output**: JPEG, PNG, WebP, PDF (native Playwright PDF API) / 多格式输出
- **Zero CDN at render time**: fully offline once deps are installed / 渲染阶段零 CDN 依赖（安装时需网络下载依赖）

---

## Troubleshooting / 故障排除

| Problem 问题 | Solution 解决方案 |
|-------------|------------------|
| Chromium launch fails (WSL2/Docker) | render.sh auto-retries with compatibility fallback. If still fails, check Chromium is installed: `python3 -m playwright install chromium` |
| Playwright download slow (China) | Set mirror: `export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright playwright install chromium` |
| `command not found` after install | Run: `export PATH="$HOME/.local/bin:$PATH"` and add to `~/.bashrc` or `~/.zshrc` |
| LaTeX shows as raw text | Install KaTeX: `npm install --prefix ./vendor katex` |
| Mermaid shows as code block | Install mermaid-cli: `npm install --prefix ./vendor @mermaid-js/mermaid-cli` |
| Code blocks have no colors | Install Pygments: `python3 -m pip install --user pygments` |

## Architecture / 架构

```
Markdown → preprocess task lists
  → mistune → HTML
LaTeX → extracted → §placeholder§ → KaTeX CLI (npm) → restored
Mermaid → mmdc → SVG → embedded; fallback → styled placeholder
  → Playwright Chromium screenshot → JPEG / PNG / WebP
  → Playwright page.pdf() → PDF (native pagination)
→ Pillow page split → multiple images (JPEG/PNG/WebP only)
```
