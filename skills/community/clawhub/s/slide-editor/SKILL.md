---
name: slide-editor
version: 0.2.0
description: "Visual editor for HTML presentations. Self-contained, offline-capable, designed for AI agent control. HTML 演示文稿可视化编辑器，自包含可离线，支持 AI Agent 控制。"
---

# Slide Editor

[中文](#中文) | [English](#english)

---

## English

Visual editor for HTML presentations. Self-contained, offline-capable, designed for both AI agent control and direct user manipulation.

### Installation

**Prerequisites**: Install [bun](https://bun.sh) first (required for running the injector).

```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows (PowerShell)
powershell -c "irm bun.sh/install.ps1 | iex"

# Or use npm
npm install -g bun
```

Then install and build:

```bash
# Clone or download this project
cd slide-editor

# Install dependencies and build (use bun, not npm)
bun install
bun run build
```

### Quick Start

When user wants to visually edit an HTML presentation:

```bash
# Inject editor and open in browser (one command)
bun ~/projects/slide-editor/inject.ts <html-file> --inline --enable --open
```

This will:
1. Inject the editor bundle into the HTML file
2. Automatically open the browser with editor enabled

### CLI Commands

```bash
# Full workflow: inject + enable + open (recommended)
bun ~/projects/slide-editor/inject.ts presentation.html --inline --enable --open

# Inline mode (single file, portable)
bun ~/projects/slide-editor/inject.ts presentation.html --inline --enable

# Link mode (separate bundle file)
bun ~/projects/slide-editor/inject.ts presentation.html --link --enable

# Remove editor from HTML
bun ~/projects/slide-editor/inject.ts presentation.html --remove
```

### User Interaction

| Action | How |
|--------|-----|
| Select | Click on element |
| Move | Drag selected element |
| Resize | Drag 8 corner handles |
| Edit text | Double-click text |
| Delete | Delete/Backspace key |
| Undo | Ctrl/Cmd + Z |
| Redo | Ctrl/Cmd + Shift + Z |
| Toggle Panel | P key or Panel button |
| Toggle Theme | T key or Theme button |
| Deselect | Escape |

### Toolbar Buttons

| Button | Function |
|--------|----------|
| T | Add text box |
| Image | Add image (file picker) |
| Trash | Delete selected |
| Undo/Redo | History controls |
| Panel | Toggle properties panel |
| Theme | Toggle light/dark/auto theme |
| Export | Export as new HTML file |

### Workflow

1. **Inject**: Run inject.ts with `--open` flag
2. **Edit**: Make changes in browser (editor auto-enables)
3. **Export**: Click Export button
4. **Done**: File is downloaded to your downloads folder

### API Reference

All methods available via `window.__openclawEditor`:

#### Core
- `enable()` / `disable()` - Toggle editor
- `isEnabled()` - Check if active

#### Slides
- `addSlide(index?)` - Add new slide
- `deleteSlide(index)` - Delete slide
- `moveSlide(from, to)` - Reorder slide
- `duplicateSlide(index)` - Copy slide
- `getSlides()` - Get all slides
- `getCurrentSlide()` / `setCurrentSlide(index)` - Get/set current

#### Elements
- `addText(options)` - Add text box
- `addImage(options)` - Add image (supports local file via File picker)
- `deleteElement(id)` / `deleteSelected()` - Delete
- `moveElement(id, x, y)` - Move
- `resizeElement(id, w, h)` - Resize
- `setTextContent(id, content)` - Set text
- `setStyle(id, styles)` - Apply CSS
- `cropImage(id, rect)` - Crop image
- `bringToFront(id)` / `sendToBack(id)` - Layer order

#### Selection
- `selectElement(id)` / `deselectAll()`
- `getSelectedElement()` / `getSelectedElements()`

#### History
- `undo()` / `redo()`
- `canUndo()` / `canRedo()`

#### Export
- `export()` - Export clean HTML
- `exportWithEditor()` - Export with editor embedded

### Type Definitions

```typescript
interface TextOptions {
  x?: number; y?: number;
  width?: number; height?: number;
  content?: string;
  fontSize?: string;
  color?: string;
  fontWeight?: string;
  textAlign?: 'left' | 'center' | 'right';
}

interface ImageOptions {
  x?: number; y?: number;
  width?: number; height?: number;
  src: string;  // URL or data URI
  alt?: string;
}

interface CropRect {
  x: number; y: number;
  width: number; height: number;
}
```

### Examples

```javascript
// Add text
window.__openclawEditor.addText({
  x: 100, y: 200, width: 400,
  content: 'Hello World',
  fontSize: '48px'
});

// Move element
window.__openclawEditor.moveElement('editor-el-1', 150, 250);

// Export
const html = window.__openclawEditor.export();
```

---

## 中文

HTML 演示文稿的可视化编辑器。自包含、可离线使用，支持 AI Agent 控制和直接用户操作。

### 安装

**前置条件**：先安装 [bun](https://bun.sh)（运行注入器必需）。

```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows (PowerShell)
powershell -c "irm bun.sh/install.ps1 | iex"

# 或使用 npm
npm install -g bun
```

然后安装和构建：

```bash
# 克隆或下载此项目
cd slide-editor

# 安装依赖并构建（使用 bun，不要用 npm）
bun install
bun run build
```

### 快速开始

当用户想要可视化编辑 HTML 演示文稿时：

```bash
# 注入编辑器并在浏览器中打开（一条命令）
bun ~/projects/slide-editor/inject.ts <html文件> --inline --enable --open
```

这将：
1. 将编辑器包注入到 HTML 文件中
2. 自动打开浏览器并启用编辑器

### CLI 命令

```bash
# 完整流程：注入 + 启用 + 打开（推荐）
bun ~/projects/slide-editor/inject.ts presentation.html --inline --enable --open

# 内联模式（单文件，便携）
bun ~/projects/slide-editor/inject.ts presentation.html --inline --enable

# 链接模式（独立的 bundle 文件）
bun ~/projects/slide-editor/inject.ts presentation.html --link --enable

# 从 HTML 中移除编辑器
bun ~/projects/slide-editor/inject.ts presentation.html --remove
```

### 用户操作

| 操作 | 方法 |
|------|------|
| 选择 | 点击元素 |
| 移动 | 拖拽选中的元素 |
| 调整大小 | 拖拽 8 个角点手柄 |
| 编辑文本 | 双击文本 |
| 删除 | Delete/Backspace 键 |
| 撤销 | Ctrl/Cmd + Z |
| 重做 | Ctrl/Cmd + Shift + Z |
| 切换面板 | P 键或面板按钮 |
| 切换主题 | T 键或主题按钮 |
| 取消选择 | Escape |

### 工具栏按钮

| 按钮 | 功能 |
|------|------|
| T | 添加文本框 |
| 图片 | 添加图片（文件选择器） |
| 垃圾桶 | 删除选中 |
| 撤销/重做 | 历史控制 |
| 面板 | 切换属性面板 |
| 主题 | 切换亮/暗/自动主题 |
| 导出 | 导出为新的 HTML 文件 |

### 工作流程

1. **注入**：使用 `--open` 标志运行 inject.ts
2. **编辑**：在浏览器中进行更改（编辑器自动启用）
3. **导出**：点击导出按钮
4. **完成**：文件下载到你的下载文件夹

### API 参考

所有方法通过 `window.__openclawEditor` 访问：

#### 核心
- `enable()` / `disable()` - 切换编辑器
- `isEnabled()` - 检查是否激活

#### 幻灯片
- `addSlide(index?)` - 添加新幻灯片
- `deleteSlide(index)` - 删除幻灯片
- `moveSlide(from, to)` - 重新排序幻灯片
- `duplicateSlide(index)` - 复制幻灯片
- `getSlides()` - 获取所有幻灯片
- `getCurrentSlide()` / `setCurrentSlide(index)` - 获取/设置当前幻灯片

#### 元素
- `addText(options)` - 添加文本框
- `addImage(options)` - 添加图片（支持通过文件选择器选择本地文件）
- `deleteElement(id)` / `deleteSelected()` - 删除
- `moveElement(id, x, y)` - 移动
- `resizeElement(id, w, h)` - 调整大小
- `setTextContent(id, content)` - 设置文本
- `setStyle(id, styles)` - 应用 CSS
- `cropImage(id, rect)` - 裁剪图片
- `bringToFront(id)` / `sendToBack(id)` - 图层顺序

#### 选择
- `selectElement(id)` / `deselectAll()`
- `getSelectedElement()` / `getSelectedElements()`

#### 历史
- `undo()` / `redo()`
- `canUndo()` / `canRedo()`

#### 导出
- `export()` - 导出干净的 HTML
- `exportWithEditor()` - 导出带编辑器的 HTML

### 示例

```javascript
// 添加文本
window.__openclawEditor.addText({
  x: 100, y: 200, width: 400,
  content: '你好世界',
  fontSize: '48px'
});

// 移动元素
window.__openclawEditor.moveElement('editor-el-1', 150, 250);

// 导出
const html = window.__openclawEditor.export();
```
