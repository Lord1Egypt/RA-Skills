---
name: resume-html
description: HTML-based resume generator with PDF export. Creates pixel-perfect resumes with advanced layouts, photo support, custom styling. Generates beautiful HTML resumes and exports to PDF. HTML简历、PDF简历、专业排版。
version: 1.0.2
license: MIT-0
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install playwright && playwright install chromium"
---

# Resume HTML Generator

Create pixel-perfect HTML resumes with advanced layouts, photo support, and PDF export.

## Features

- 📄 **HTML Output**: Beautiful, editable HTML resumes
- 📸 **Photo Support**: Automatic photo embedding
- 🎨 **Advanced Layouts**: CSS Grid, Flexbox, custom styling
- 📑 **PDF Export**: High-quality PDF output via Playwright
- 🎯 **Pixel-Perfect**: Professional, print-ready design
- 🌍 **Multi-Language**: Chinese and English presets
- 🖥️ **Cross-Platform**: Windows, macOS, Linux
- 🎨 **10 Presets**: 5 Chinese + 5 English styles

## Presets Available

### Chinese (中文)

| Style | Design | Best For |
|-------|--------|----------|
| **经典蓝** | Blue gradient header | 通用、职场 |
| **极简白** | Clean, minimal | 简约、设计 |
| **商务黑** | Dark professional | 金融、法律 |
| **科技绿** | Green tech style | 互联网、科技 |
| **学术紫** | Purple academic | 学术、研究 |

### English

| Style | Design | Best For |
|-------|--------|----------|
| **Silicon Valley** | Modern left-aligned | Tech companies |
| **Academic** | Traditional serif | Research |
| **Creative** | Gradient sidebar | Design, creative |
| **Modern Dark** | Dark header | Management |
| **Minimal** | Simple centered | General |

## Trigger Conditions

- "Create HTML resume" / "创建HTML简历"
- "Generate PDF resume" / "生成PDF简历"
- "Make a pixel-perfect resume" / "制作精美简历"
- "resume-html"

---

## How It Works

```
User provides info
    ↓
1. Generate HTML with CSS
    ↓
2. Embed photo (optional)
    ↓
3. Render in browser
    ↓
4. Export to PDF
    ↓
Output: resume.html + resume.pdf
```

---

## HTML Template Example

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Sans SC', 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            background: white;
        }
        
        .resume {
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            padding: 15mm 20mm;
            background: white;
        }
        
        .header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #1a365d;
        }
        
        .name {
            font-size: 28pt;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 5px;
        }
        
        .position {
            font-size: 14pt;
            color: #666;
            font-style: italic;
        }
        
        .contact {
            margin-top: 10px;
            font-size: 10pt;
            color: #666;
        }
        
        .photo {
            float: right;
            width: 100px;
            height: 120px;
            margin-left: 20px;
            border: 2px solid #1a365d;
            object-fit: cover;
        }
        
        .section {
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 14pt;
            font-weight: bold;
            color: #1a365d;
            border-left: 4px solid #3182ce;
            padding-left: 10px;
            margin-bottom: 10px;
        }
        
        .entry {
            margin-bottom: 15px;
        }
        
        .entry-header {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .company { color: #1a365d; }
        .duration { color: #666; font-weight: normal; }
        
        .responsibilities {
            padding-left: 20px;
        }
        
        .responsibilities li {
            margin-bottom: 3px;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        
        .skill-category {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
        }
        
        .skill-category-title {
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 5px;
        }
        
        @media print {
            .resume {
                margin: 0;
                padding: 15mm 20mm;
            }
        }
    </style>
</head>
<body>
    <div class="resume">
        <!-- Photo (optional) -->
        <!-- <img class="photo" src="photo.jpg" alt="Photo"> -->
        
        <div class="header">
            <div class="name">{{name}}</div>
            <div class="position">{{position}}</div>
            <div class="contact">
                📞 {{phone}} | 📧 {{email}} | 📍 {{location}}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">求职意向</div>
            <div>职位：{{target_position}} | 期望薪资：{{salary}}</div>
        </div>
        
        <div class="section">
            <div class="section-title">教育背景</div>
            <div class="entry">
                <div class="entry-header">
                    <span class="company">{{school}}</span>
                    <span class="duration">{{education_year}}</span>
                </div>
                <div>{{major}} - {{degree}}</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">工作经历</div>
            {{#each experience}}
            <div class="entry">
                <div class="entry-header">
                    <span class="company">{{company}}</span>
                    <span class="duration">{{duration}}</span>
                </div>
                <div>{{position}}</div>
                <ul class="responsibilities">
                    {{#each responsibilities}}
                    <li>{{this}}</li>
                    {{/each}}
                </ul>
            </div>
            {{/each}}
        </div>
        
        <div class="section">
            <div class="section-title">专业技能</div>
            <div class="skills-grid">
                {{#each skills}}
                <div class="skill-category">
                    <div class="skill-category-title">{{category}}</div>
                    <div>{{items}}</div>
                </div>
                {{/each}}
            </div>
        </div>
    </div>
</body>
</html>
```

---

## PDF Export

```python
from playwright.sync_api import sync_playwright

def export_to_pdf(html_path, pdf_path):
    """Export HTML to PDF using Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'file://{html_path}')
        page.pdf(path=pdf_path, format='A4', margin={
            'top': '0mm',
            'bottom': '0mm',
            'left': '0mm',
            'right': '0mm'
        })
        browser.close()
    return pdf_path
```

---

## Usage Examples

```
User: "Create a beautiful HTML resume"
Agent: Generate HTML with CSS styling

User: "生成PDF简历，包含照片"
Agent: Generate HTML, embed photo, export PDF

User: "做一个科技风格的简历"
Agent: Use Modern style template
```

---

## Advantages Over Word-based Resume

| Feature | Word | HTML → PDF |
|---------|------|------------|
| Photo embedding | ⚠️ Limited | ✅ Perfect |
| Complex layouts | ❌ Tables only | ✅ CSS Grid/Flexbox |
| Custom styling | ⚠️ Limited | ✅ Unlimited |
| Print quality | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| File size | Large | Small |
| Editable | ✅ Yes | ✅ HTML editable |

---

## Notes

- HTML provides pixel-perfect control
- PDF export using Playwright
- Photo embedding with base64
- Cross-platform compatible
- Professional, print-ready output
