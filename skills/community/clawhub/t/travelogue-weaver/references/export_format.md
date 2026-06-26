# 导出格式规范

本文档定义了游记导出的各种格式规范和模板。

## 目录
- [Markdown 格式](#markdown-格式)
- [HTML 格式](#html-格式)
- [PDF 格式](#pdf-格式)
- [文件命名规范](#文件命名规范)
- [模板系统](#模板系统)

## Markdown 格式

### 基本结构

```markdown
# 【{旅行标题}】

## Day {N} · {地点/主题}
> {日期} ｜ {附加信息}

{内容段落}

{图片}

{分隔线}

---

## 后记

{总结内容}
```

### 文件命名

- 默认：`{旅行标题}.md`
- 示例：`云南七日漫游.md`

### 编码要求

- 文件编码：UTF-8
- 换行符：Unix 风格（LF, `\n`）
- 图片路径：相对路径

### 图片处理

#### 本地图片引用

```markdown
![图片描述](./uploads/{momentId}.jpg)
```

#### 带 EXIF 信息的图片

如果图片包含 EXIF 数据，在导出时添加说明：

```markdown
![洱海风光](./uploads/image_001.jpg)
*拍摄于 2026-04-03 15:30，洱海边*
```

### 多媒体嵌入

#### 音频

```markdown
🎵 *语音记录：{转写内容}*

[音频文件](./uploads/{momentId}.mp3)
```

#### 视频

```markdown
🎬 *视频记录：{描述内容}*

[视频文件](./uploads/{momentId}.mp4)
```

### 元数据嵌入

在 Markdown 文件头部嵌入元数据（可选）：

```markdown
---
title: 云南七日漫游
author: 用户名
created: 2026-04-09
trip_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
total_days: 7
total_moments: 42
---
```

## HTML 格式

### 基本结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{旅行标题}</title>
    <style>
        /* 样式定义 */
    </style>
</head>
<body>
    <article class="travelogue">
        <!-- 内容 -->
    </article>
    <footer>
        <p class="generated-info">生成时间：{时间}</p>
    </footer>
</body>
</html>
```

### 样式规范

#### 核心样式

```css
/* 整体布局 */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    line-height: 1.6;
    color: #333;
    background-color: #fafafa;
}

/* 标题样式 */
h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    font-size: 2em;
}

h2 {
    color: #34495e;
    margin-top: 30px;
    border-left: 4px solid #3498db;
    padding-left: 15px;
}

/* 图片样式 */
img {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 15px 0;
    display: block;
}

/* 引用块样式 */
blockquote {
    border-left: 4px solid #3498db;
    padding: 15px 20px;
    margin: 20px 0;
    background-color: #f0f8ff;
    font-style: italic;
    color: #555;
}

/* 高光时刻 */
.highlight {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}

/* 分隔线 */
hr {
    border: none;
    border-top: 1px solid #ecf0f1;
    margin: 30px 0;
}

/* 段落 */
p {
    margin: 15px 0;
    text-align: justify;
}

/* 列表 */
ul, ol {
    padding-left: 20px;
}

/* 页脚 */
footer {
    text-align: center;
    color: #95a5a6;
    font-size: 14px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #ecf0f1;
}
```

### 响应式设计

```css
/* 移动端适配 */
@media screen and (max-width: 600px) {
    body {
        padding: 15px;
    }
    
    h1 {
        font-size: 1.5em;
    }
    
    h2 {
        font-size: 1.2em;
    }
    
    img {
        margin: 10px 0;
    }
}
```

### 文件命名

- 默认：`{旅行标题}.html`
- 示例：`云南七日漫游.html`

## PDF 格式

### 生成流程

1. 先生成 HTML 内容
2. 使用 WeasyPrint 或类似工具转换
3. 添加页眉页脚和页码

### 页面设置

```python
# WeasyPrint 配置
from weasyprint import HTML, CSS

css = CSS(string='''
    @page {
        size: A4;
        margin: 2cm;
        @top-center {
            content: "云南七日漫游";
            font-size: 10pt;
            color: #999;
        }
        @bottom-right {
            content: "第 " counter(page) " 页";
            font-size: 10pt;
            color: #999;
        }
    }
''')
```

### 文件命名

- 默认：`{旅行标题}.pdf`
- 示例：`云南七日漫游.pdf`

### 图片处理

- 图片分辨率：建议 150-300 DPI
- 图片格式：JPG 或 PNG
- 图片大小：单张不超过 2MB（PDF 内嵌入）

### 字体要求

- 中文字体：思源宋体、方正书宋、SimSun
- 英文字体：Times New Roman、Georgia
- 代码字体：Consolas、Courier New

## 文件命名规范

### 基本规则

1. 使用旅行标题作为基础文件名
2. 特殊字符替换：
   - 空格 → 下划线或连字符
   - 特殊字符 → 删除或替换
3. 添加时间戳（可选）

### 命名模板

```
{旅行标题}_{导出格式}_{时间戳}.{扩展名}
```

### 示例

| 场景 | 文件名 |
|------|--------|
| 默认导出 | `云南七日漫游.md` |
| 带时间戳 | `云南七日漫游_20260409.md` |
| 多版本 | `云南七日漫游_v2.md` |
| 不同格式 | `云南七日漫游.html`, `云南七日漫游.pdf` |

## 模板系统

### 模板文件位置

```
assets/templates/
├── travelogue.html       # HTML 模板
├── travelogue_pdf.html   # PDF 专用模板（可选）
└── components/           # 组件模板（可选）
    ├── header.html
    ├── footer.html
    └── sidebar.html
```

### HTML 模板示例

**文件**：`assets/templates/travelogue.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --primary-color: #3498db;
            --text-color: #333;
            --bg-color: #fafafa;
            --border-color: #ecf0f1;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.8;
            color: var(--text-color);
            background-color: var(--bg-color);
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 15px;
            font-size: 2.2em;
            text-align: center;
        }
        
        h2 {
            color: #34495e;
            margin-top: 40px;
            border-left: 4px solid var(--primary-color);
            padding-left: 15px;
        }
        
        .day-meta {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        
        img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            margin: 20px 0;
            display: block;
        }
        
        blockquote {
            border-left: 4px solid var(--primary-color);
            padding: 15px 20px;
            margin: 25px 0;
            background-color: #f0f8ff;
            border-radius: 0 8px 8px 0;
        }
        
        blockquote.highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-style: italic;
        }
        
        blockquote.highlight strong {
            color: #ffd700;
        }
        
        hr {
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 40px 0;
        }
        
        .moment-text {
            margin: 15px 0;
            text-align: justify;
        }
        
        .moment-image {
            margin: 20px 0;
        }
        
        .moment-image figcaption {
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: center;
            margin-top: 8px;
            font-style: italic;
        }
        
        .audio-marker, .video-marker {
            display: inline-block;
            background-color: #e8f4f8;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.95em;
            margin: 10px 0;
        }
        
        footer {
            text-align: center;
            color: #95a5a6;
            font-size: 14px;
            margin-top: 50px;
            padding-top: 25px;
            border-top: 1px solid var(--border-color);
        }
        
        @media screen and (max-width: 600px) {
            body {
                padding: 15px;
            }
            
            h1 {
                font-size: 1.6em;
            }
            
            h2 {
                font-size: 1.3em;
            }
        }
        
        @media print {
            body {
                background-color: white;
                padding: 0;
            }
            
            img {
                page-break-inside: avoid;
            }
            
            h2 {
                page-break-after: avoid;
            }
        }
    </style>
</head>
<body>
    <article class="travelogue">
        {{ content|safe }}
    </article>
    
    <footer>
        <p>生成时间：{{ generated_at }}</p>
        <p>由 Travelogue Weaver 生成</p>
    </footer>
</body>
</html>
```

### 模板变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `title` | string | 游记标题 |
| `content` | html | HTML 正文内容 |
| `generated_at` | string | 生成时间 |
| `trip_id` | string | 旅行 ID（可选） |
| `author` | string | 作者（可选） |

### 自定义模板

用户可以提供自定义模板文件，需满足：

1. 文件位置：`./assets/templates/custom.html`
2. 包含必需变量：`{{ title }}`, `{{ content }}`
3. 使用 Jinja2 模板语法

## 导出选项

### 导出参数

```python
{
    "trip_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "format": "markdown",  # markdown | html | pdf
    "output_path": "./output/travelogue.md",
    "include_metadata": true,
    "image_quality": "high",  # high | medium | low
    "embed_images": false,    # 是否嵌入图片（base64）
    "template": "default"     # default | custom
}
```

### 批量导出

支持一次性导出多种格式：

```python
export_travelogue(
    trip_id="xxx",
    formats=["markdown", "html", "pdf"],
    output_dir="./output/"
)
```

## 质量检查

### Markdown 检查

- [ ] 文件编码为 UTF-8
- [ ] 所有图片路径有效
- [ ] 没有语法错误
- [ ] 元数据格式正确

### HTML 检查

- [ ] 符合 HTML5 标准
- [ ] 样式正常显示
- [ ] 响应式布局正常
- [ ] 图片加载正常

### PDF 检查

- [ ] 页面布局正常
- [ ] 中文字体显示正常
- [ ] 图片清晰度足够
- [ ] 页眉页脚正确
