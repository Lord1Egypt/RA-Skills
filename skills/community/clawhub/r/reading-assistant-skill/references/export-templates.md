# 导出模板说明

本文档说明笔记导出的模板和使用方法。

## 目录

- [支持的导出格式](#支持的导出格式)
- [Markdown 模板](#markdown-模板)
- [HTML 模板](#html-模板)
- [PDF 导出](#pdf-导出)
- [自定义模板](#自定义模板)
- [使用示例](#使用示例)

## 支持的导出格式

| 格式 | 文件扩展名 | 特点 | 适用场景 |
|------|-----------|------|----------|
| Markdown | .md | 纯文本，易于编辑 | 博客发布、笔记整理 |
| HTML | .html | 格式美观，支持样式 | 网页展示、打印 |
| PDF | .pdf | 固定格式，便于分享 | 文档存档、打印 |

## Markdown 模板

### 模板结构

```markdown
# {书名}

**作者**: {作者}
**标签**: {标签列表}
**创建时间**: {创建日期}
**摘录数量**: {总数}

---

## 目录

- [第1章](#第1章)
- [第2章](#第2章)

---

## 第1章

### 摘录 1

> {摘录内容}

**标签**: {标签1}, {标签2}

**深层含义**:

{深层含义分析}

**应用建议**:

{应用建议}

---

### 摘录 2

> {第二条摘录内容}

...
```

### 模板特点

- **清晰的层级结构**：使用 Markdown 标题组织内容
- **引用格式**：摘录内容使用引用块（>）突出显示
- **元信息**：包含书籍信息和统计数据
- **目录导航**：自动生成章节目录
- **可读性强**：适合在 Markdown 编辑器中阅读和编辑

### 适用场景

- 在 Obsidian、Notion 等 Markdown 编辑器中使用
- 发布到支持 Markdown 的博客平台
- 进行二次编辑和整理

## HTML 模板

### 模板特点

- **美观的样式**：内置 CSS 样式，无需额外配置
- **响应式设计**：适配不同屏幕尺寸
- **打印友好**：适合打印为纸质文档
- **独立文件**：包含所有样式，无需外部依赖

### 样式说明

#### 主体样式

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    line-height: 1.6;
    color: #333;
}
```

#### 标题样式

- **一级标题**：深色背景，底部边框
- **二级标题**：章节标题，清晰的视觉层级
- **三级标题**：摘录标题，次要层级

#### 内容样式

- **引用块**：浅灰背景，左侧蓝色边框
- **标签**：蓝色圆角背景，白色文字
- **分析区域**：浅灰背景，圆角边框

### 自定义样式

可以编辑 `assets/export_html.html` 文件来自定义样式：

```html
<style>
    /* 自定义标题颜色 */
    h1 { color: #your-color; }
    
    /* 自定义标签样式 */
    .tag { background: #your-color; }
    
    /* 自定义引用块样式 */
    blockquote { border-left-color: #your-color; }
</style>
```

## PDF 导出

### 导出方式

由于 PDF 生成需要额外的依赖库，当前采用以下方式：

1. **先生成 HTML**：使用 HTML 模板生成格式化的 HTML 文件
2. **浏览器打印**：在浏览器中打开 HTML，使用"打印"功能导出为 PDF

### 推荐设置

在浏览器打印对话框中：

- **布局**：纵向
- **边距**：默认
- **背景图形**：勾选（保留样式）
- **页眉页脚**：可选

### 自动化 PDF 生成（高级）

如果需要脚本自动生成 PDF，可以安装额外依赖：

```bash
pip install weasyprint
```

然后修改 `scripts/export_notes.py`，添加 PDF 生成逻辑：

```python
from weasyprint import HTML

def export_to_pdf(html_content: str, output_path: str):
    """将 HTML 转换为 PDF"""
    HTML(string=html_content).write_pdf(output_path)
```

## 自定义模板

### 创建自定义模板

如果默认模板不满足需求，可以创建自定义模板：

#### Markdown 自定义模板

在 `assets/` 目录下创建 `custom_markdown.md`：

```markdown
# {book_title}

{% for excerpt in excerpts %}
## {{ excerpt.chapter }}

> {{ excerpt.content }}

{% if excerpt.tags %}
标签: {{ excerpt.tags | join(', ') }}
{% endif %}

{% endfor %}
```

使用 Jinja2 模板语法，在脚本中渲染。

#### HTML 自定义模板

创建 `assets/custom_html.html`，使用类似的模板语法。

### 模板变量

| 变量 | 说明 |
|------|------|
| book_title | 书名 |
| book_author | 作者 |
| book_tags | 书籍标签 |
| created_at | 创建日期 |
| excerpts | 摘录列表 |
| excerpt.content | 摘录内容 |
| excerpt.chapter | 章节 |
| excerpt.tags | 标签列表 |
| excerpt.deep_meaning | 深层含义 |
| excerpt.application | 应用建议 |

## 使用示例

### 示例 1：导出为 Markdown

```bash
python scripts/export_notes.py "思考，快与慢" --format markdown
```

**输出**：

```
已成功导出《思考，快与慢》
格式: Markdown
路径: ./reading-notes/exports/思考，快与慢.md
摘录数量: 45
```

### 示例 2：导出为 HTML

```bash
python scripts/export_notes.py "思考，快与慢" --format html --output ./my-notes.html
```

**输出**：

```
已成功导出《思考，快与慢》
格式: HTML
路径: ./my-notes.html
摘录数量: 45
```

### 示例 3：不包含深层分析

```bash
python scripts/export_notes.py "思考，快与慢" --format markdown --no-analysis
```

**说明**：导出的 Markdown 文件不包含深层含义和应用建议部分。

### 示例 4：在对话中导出

```
用户：导出《思考，快与慢》的笔记为 Markdown 格式
智能体：是否包含深层分析？（默认包含）
用户：包含
智能体：（调用导出脚本）
已成功导出笔记文件：./reading-notes/exports/思考，快与慢.md
共包含 45 条摘录，已按章节组织。
您可以直接下载使用，或在 Markdown 编辑器中打开编辑。
```

## 导出选项

### 基本选项

| 选项 | 参数 | 说明 |
|------|------|------|
| 书籍名称 | book_name | 必需，指定要导出的书籍 |
| 格式 | --format | markdown / html / pdf |
| 输出路径 | --output | 自定义输出路径 |
| 是否包含分析 | --no-analysis | 不包含深层含义和应用建议 |

### 高级选项（未来扩展）

- **选择章节**：仅导出指定章节的笔记
- **日期范围**：仅导出指定时间段的笔记
- **标签筛选**：仅导出包含特定标签的笔记
- **模板选择**：使用自定义模板

## 注意事项

### 导出路径

- 默认导出到 `./reading-notes/exports/` 目录
- 如果目录不存在，会自动创建
- 如果文件已存在，会覆盖

### 中文文件名

- 支持中文文件名
- 确保系统编码为 UTF-8

### 大文件处理

- 如果摘录数量很多，Markdown 文件可能较大
- 建议按章节分批导出（未来功能）

### 兼容性

- Markdown 文件可在任何 Markdown 编辑器中打开
- HTML 文件可在任何现代浏览器中打开
- PDF 文件需要 PDF 阅读器
