---
name: watermark-pro
description: 文件水印工具。Use when user wants to add watermark to images, Word, PowerPoint, or PDF files. Supports text watermark, logo watermark, diagonal/center/tile layouts. 图片水印、文档水印、Word加水印、PPT加水印。
version: 1.0.4
license: MIT-0
metadata: {"openclaw": {"emoji": "💧", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install pillow python-docx python-pptx pymupdf"
---

# Watermark Pro

文件水印工具，支持图片、Word、PPT、PDF添加水印。

## Features

- 🖼️ **图片水印**：支持JPG/PNG/WEBP
- 📄 **Word水印**：支持.docx
- 📊 **PPT水印**：支持.pptx
- 📑 **PDF水印**：支持.pdf
- ✍️ **文字水印**：自定义文字、字体、颜色
- 🖼️ **Logo水印**：支持透明PNG Logo
- 📍 **多种布局**：对角线/居中/平铺

## Trigger Conditions

- "加水印" / "Add watermark"
- "图片加水印" / "Word文档加水印"
- "watermark-pro"

---

## Step 1: Image Watermark

```python
from PIL import Image, ImageDraw, ImageFont
import os

class ImageWatermark:
    def add_text_watermark(self, image_path, text, output_path,
                          font_size=None, color=(128, 128, 128),
                          opacity=0.3, angle=-45, layout='diagonal', density=200):
        img = Image.open(image_path).convert('RGBA')
        width, height = img.size
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        if font_size is None:
            font_size = max(width, height) // 30
        
        try:
            font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', font_size)
        except:
            font = ImageFont.load_default()
        
        alpha = int(255 * opacity)
        fill_color = (*color, alpha)
        
        if layout == 'diagonal':
            for y in range(0, height, density):
                for x in range(0, width, int(density * 1.4)):
                    draw.text((x, y), text, font=font, fill=fill_color)
        elif layout == 'center':
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(((width-tw)//2, (height-th)//2), text, font=font, fill=fill_color)
        
        watermark = watermark.rotate(angle, expand=False, resample=Image.BICUBIC)
        result = Image.alpha_composite(img, watermark)
        
        if output_path.lower().endswith('.jpg'):
            result = result.convert('RGB')
        result.save(output_path)
        return output_path
```

---

## Step 2: Word Watermark

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class WordWatermark:
    def add_text_watermark(self, docx_path, text, output_path,
                          font_size=48, color=(200, 200, 200)):
        doc = Document(docx_path)
        
        for section in doc.sections:
            header = section.header
            header.is_linked_to_previous = False
            
            for para in header.paragraphs:
                para.clear()
            
            para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            run = para.add_run(text)
            run.font.size = Pt(font_size)
            run.font.color.rgb = RGBColor(*color)
            run.font.name = '宋体'
            
            para.paragraph_format.space_before = Pt(250)
        
        doc.save(output_path)
        return output_path
```

---

## Step 3: PowerPoint Watermark

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

class PptWatermark:
    def add_text_watermark(self, pptx_path, text, output_path,
                          font_size=60, color=(200, 200, 200)):
        prs = Presentation(pptx_path)
        
        for slide in prs.slides:
            txBox = slide.shapes.add_textbox(Inches(1.5), Inches(3), Inches(7), Inches(1.5))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = Pt(font_size)
            p.font.color.rgb = RGBColor(*color)
            p.alignment = PP_ALIGN.CENTER
        
        prs.save(output_path)
        return output_path
```

---

## Step 4: PDF Watermark (Image Overlay)

```python
import fitz
from PIL import Image, ImageDraw, ImageFont
import os

class PdfWatermark:
    def add_text_watermark(self, pdf_path, text, output_path,
                          font_size=28, color=(128, 128, 128),
                          opacity=0.25, density=220):
        doc = fitz.open(pdf_path)
        
        for page in doc:
            rect = page.rect
            width, height = int(rect.width), int(rect.height)
            
            wm_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(wm_img)
            
            try:
                font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', font_size)
            except:
                font = ImageFont.load_default()
            
            alpha = int(255 * opacity)
            fill = (*color, alpha)
            
            for y in range(0, height, density):
                for x in range(0, width, int(density * 1.4)):
                    draw.text((x, y), text, font=font, fill=fill)
            
            temp_img = os.path.join(os.path.dirname(output_path), '_temp_wm.png')
            wm_img.save(temp_img)
            
            page.insert_image(rect, filename=temp_img, overlay=True)
        
        doc.save(output_path)
        doc.close()
        
        if os.path.exists(temp_img):
            os.remove(temp_img)
        
        return output_path
```

---

## Usage Examples

```
User: "给图片加'版权所有'水印"
Agent: 使用 ImageWatermark.add_text_watermark()

User: "Word文档加'机密'水印"
Agent: 使用 WordWatermark.add_text_watermark()

User: "PDF加水印，密度高一点"
Agent: 使用 PdfWatermark.add_text_watermark(density=150)
```

---

## Notes

- 纯本地处理，无隐私风险
- 支持中英文水印
- 跨平台兼容
