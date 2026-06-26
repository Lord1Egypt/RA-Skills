# python-docx Skill

## 概述

本Skill提供使用python-docx生成专业Word文档的标准方法和最佳实践。

## 适用场景

- 生成安全服务方案文档
- 生成技术架构设计文档
- 生成任何需要专业排版的Word文档

## 技术栈

- **核心库**: `python-docx`
- **辅助库**: `docx.shared`, `docx.enum`, `docx.oxml.ns`

## 标准代码模板

### 1. 文档初始化

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

def create_document():
    """创建标准文档"""
    doc = Document()

    # 设置默认字体（关键！）
    style = doc.styles['Normal']
    style.font.name = 'Microsoft YaHei'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

    return doc
```

### 2. 字体设置（必须！）

```python
def set_font(run, font_name='Microsoft YaHei'):
    """设置字体"""
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
```

### 3. 标题添加

```python
def add_heading_custom(doc, text, level=1):
    """
    添加标准标题

    Args:
        doc: Document对象
        text: 标题文本
        level: 1=一级, 2=二级, 3=三级

    Returns:
        标题段落对象
    """
    heading = doc.add_heading(level=level)
    run = heading.add_run(text)
    set_font(run)

    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0, 51, 102)
        run.font.bold = True
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 51, 102)
        run.font.bold = True
    else:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.font.bold = True

    return heading
```

### 4. 段落添加

```python
def add_para_custom(doc, text, bold=False, indent=0, color=None):
    """
    添加标准段落

    Args:
        doc: Document对象
        text: 段落文本
        bold: 是否加粗
        indent: 首行缩进（厘米）
        color: RGBColor颜色对象

    Returns:
        段落对象
    """
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(indent)

    run = p.add_run(text)
    run.font.size = Pt(11)
    set_font(run)

    if bold:
        run.font.bold = True
    if color:
        run.font.color.rgb = color

    return p
```

### 5. 项目符号列表

```python
def add_bullet_custom(doc, text, level=0):
    """
    添加项目符号段落

    Args:
        doc: Document对象
        text: 列表项文本
        level: 缩进级别（0=一级, 1=二级）

    Returns:
        段落对象
    """
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.5)

    run = p.add_run(text)
    run.font.size = Pt(11)
    set_font(run)

    return p
```

### 6. 编号列表

```python
def add_numbered_custom(doc, text, level=0):
    """
    添加编号列表段落

    Args:
        doc: Document对象
        text: 列表项文本
        level: 缩进级别

    Returns:
        段落对象
    """
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.5)

    run = p.add_run(text)
    run.font.size = Pt(11)
    set_font(run)

    return p
```

### 7. 表格创建

```python
def create_table(doc, headers, data):
    """
    创建标准表格

    Args:
        doc: Document对象
        headers: 表头列表
        data: 二维列表，每行是一个列表

    Returns:
        表格对象
    """
    table = doc.add_table(rows=1+len(data), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # 表头
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(10)
                set_font(run)

    # 数据
    for row_idx, row_data in enumerate(data, 1):
        for col_idx, cell_data in enumerate(row_data):
            cell = table.rows[row_idx].cells[col_idx]
            cell.text = str(cell_data)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)
                    set_font(run)

    return table
```

### 8. 图片插入

```python
def insert_image(doc, image_path, width=Inches(6), caption=None):
    """
    插入标准图片

    Args:
        doc: Document对象
        image_path: 图片路径
        width: 图片宽度
        caption: 图片标题（可选）

    Returns:
        段落对象
    """
    # 插入图片
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(image_path, width=width)

    # 添加标题
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(caption)
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(102, 102, 102)
        set_font(run)

    return p
```

### 9. 分页

```python
def add_page_break(doc):
    """添加分页符"""
    doc.add_page_break()
```

### 10. 封面创建

```python
def create_cover(doc, title, subtitle=None, customer=None, date=None, version=None):
    """
    创建标准封面

    Args:
        doc: Document对象
        title: 主标题
        subtitle: 副标题（可选）
        customer: 客户名称（可选）
        date: 日期（可选）
        version: 版本号（可选）
    """
    # 空行占位
    for _ in range(6):
        doc.add_paragraph()

    # 主标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    set_font(run)

    # 副标题
    if subtitle:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(subtitle)
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(102, 102, 102)
        set_font(run)

    # 空行
    for _ in range(4):
        doc.add_paragraph()

    # 信息
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if customer:
        run = info.add_run(f'客户：{customer}\n')
        run.font.size = Pt(14)
        set_font(run)

    if date:
        run = info.add_run(f'日期：{date}\n')
        run.font.size = Pt(14)
        set_font(run)

    if version:
        run = info.add_run(f'版本：{version}')
        run.font.size = Pt(14)
        set_font(run)
```

## 完整示例

```python
# 创建文档
doc = create_document()

# 添加封面
create_cover(doc, 
    title='安全服务方案',
    subtitle='Security Service Proposal',
    customer='某某公司',
    date='2026-03-23',
    version='V1.0'
)

# 分页
doc.add_page_break()

# 添加一级标题
add_heading_custom(doc, '一、 服务概述', level=1)

# 添加二级标题
add_heading_custom(doc, '1.1 服务背景', level=2)

# 添加正文
add_para_custom(doc, '这是正文内容，首行缩进两字符。', indent=0.5)

# 添加项目符号
add_bullet_custom(doc, '项目符号内容')

# 添加编号列表
add_numbered_custom(doc, '编号列表内容')

# 添加表格
headers = ['列1', '列2', '列3']
data = [['A', 'B', 'C'], ['D', 'E', 'F']]
create_table(doc, headers, data)

# 保存
doc.save('output.docx')
```

## 常见问题

**Q: 中文显示为方框？**  
A: 确保每个run都调用set_font()设置字体

**Q: 表格样式不统一？**  
A: 设置table.style = 'Light Grid Accent 1'

**Q: 图片无法显示？**  
A: 检查图片路径是否正确，使用绝对路径

**Q: 文档格式错乱？**  
A: 确保所有文本都设置了字体和大小

## 参考

- python-docx官方文档: https://python-docx.readthedocs.io/
