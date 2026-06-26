#!/usr/bin/env python3
"""
生成完全符合文印格式规范的示例文档
使用正确字体：方正小标宋简体、黑体、楷体GB2312、仿宋GB2312
"""
import os
import sys
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors

def register_all_fonts():
    """注册所有所需字体"""
    fonts = {
        '方正小标宋简体': '/usr/share/fonts/truetype/sim/方正小标宋简体.TTF',
        '黑体': '/usr/share/fonts/truetype/sim/SIMHEI---b012cdfe-da20-419e-86f4-a69f457cee80',
        '楷体_GB2312': '/usr/share/fonts/truetype/sim/楷体_GB2312.TTF',
        '仿宋_GB2312': '/usr/share/fonts/truetype/sim/仿宋_GB2312.TTF',
    }
    
    registered = {}
    for name, path in fonts.items():
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                addMapping(name, 0, 0, name)  # normal
                addMapping(name, 0, 1, name)  # bold
                registered[name] = True
                print(f"✓ 注册字体: {name}")
            except Exception as e:
                print(f"✗ 注册失败 {name}: {e}")
                registered[name] = False
        else:
            print(f"✗ 字体文件不存在: {path}")
            registered[name] = False
    
    return registered

def create_proper_example(output_path='文印规范完整示例.pdf'):
    """创建完全符合规范的示例文档"""
    
    # 注册字体
    print("注册字体...")
    fonts_available = register_all_fonts()
    
    # 检查关键字体
    required_fonts = ['方正小标宋简体', '黑体', '楷体_GB2312', '仿宋_GB2312']
    missing_fonts = [f for f in required_fonts if not fonts_available.get(f)]
    
    if missing_fonts:
        print(f"警告：缺失关键字体: {missing_fonts}")
        print("将使用备用字体...")
    
    # 创建文档模板
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2.8*cm,
        leftMargin=2.8*cm,
        topMargin=3.5*cm,
        bottomMargin=3.5*cm,
        title="数科公司文印格式完整示例"
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # ===== 1. 标题样式（方正小标宋简体，二号，居中） =====
    title_style = ParagraphStyle(
        'ProperTitle',
        parent=styles['Heading1'],
        fontName='方正小标宋简体',
        fontSize=22,  # 二号约22pt
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.black
    )
    
    # ===== 2. 一级标题（黑体字，三号） =====
    h1_style = ParagraphStyle(
        'ProperH1',
        parent=styles['Heading1'],
        fontName='黑体',
        fontSize=16,  # 三号约16pt
        spaceBefore=12,
        spaceAfter=12,
        textColor=colors.black
    )
    
    # ===== 3. 二级标题（楷体GB2312，三号，加粗） =====
    h2_style = ParagraphStyle(
        'ProperH2',
        parent=styles['Heading2'],
        fontName='楷体_GB2312',
        fontSize=16,
        bold=True,
        spaceBefore=10,
        spaceAfter=10,
        textColor=colors.black
    )
    
    # ===== 4. 三级标题（仿宋GB2312，三号） =====
    h3_style = ParagraphStyle(
        'ProperH3',
        parent=styles['Heading3'],
        fontName='仿宋_GB2312',
        fontSize=16,
        spaceBefore=8,
        spaceAfter=8,
        textColor=colors.black
    )
    
    # ===== 5. 四级标题（仿宋GB2312，三号） =====
    h4_style = ParagraphStyle(
        'ProperH4',
        parent=styles['Heading4'],
        fontName='仿宋_GB2312',
        fontSize=16,
        spaceBefore=6,
        spaceAfter=6,
        textColor=colors.black
    )
    
    # ===== 6. 正文样式（仿宋GB2312，三号） =====
    body_style = ParagraphStyle(
        'ProperBody',
        parent=styles['Normal'],
        fontName='仿宋_GB2312',
        fontSize=16,
        leading=28,  # 固定值28磅
        firstLineIndent=32,  # 缩进两个字符（约32pt）
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        textColor=colors.black
    )
    
    # ===== 7. 页眉页脚样式（黑体，小四号，加粗） =====
    header_style = ParagraphStyle(
        'ProperHeader',
        parent=styles['Normal'],
        fontName='黑体',
        fontSize=12,  # 小四号约12pt
        alignment=TA_CENTER,
        textColor=colors.black
    )
    
    # 创建页眉页脚函数
    def create_header_footer(canvas, doc):
        canvas.saveState()
        
        # 页眉（距页顶2.5cm）
        canvas.setFont('黑体', 12)
        canvas.drawCentredString(
            A4[0] / 2.0,
            A4[1] - 2.5*cm,
            "数科公司文印格式完整示例"
        )
        
        # 页脚（距页底2.5cm）
        canvas.setFont('黑体', 12)
        page_num = canvas.getPageNumber()
        canvas.drawCentredString(
            A4[0] / 2.0,
            2.5*cm,
            f"第 {page_num} 页"
        )
        
        # 底部横线
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.5)
        canvas.line(2.8*cm, 2.2*cm, A4[0]-2.8*cm, 2.2*cm)
        
        canvas.restoreState()
    
    # ===== 构建文档内容 =====
    
    # 标题
    story.append(Paragraph('数科公司文印格式完整示例', title_style))
    story.append(Spacer(1, 20))
    
    # 文档信息
    info_style = ParagraphStyle(
        'Info',
        parent=body_style,
        alignment=TA_CENTER,
        fontSize=14,
        spaceAfter=30
    )
    story.append(Paragraph('技术部 ｜ 2026年3月27日', info_style))
    story.append(Spacer(1, 20))
    
    # 简介
    story.append(Paragraph('本文档展示数科公司文印格式规范的实际应用效果，所有字体、字号、间距、页边距均严格按照规范要求设置。', body_style))
    story.append(Spacer(1, 15))
    
    # ===== 示例一：项目文档结构 =====
    story.append(Paragraph('一、项目实施方案', h1_style))
    story.append(Paragraph('本项目旨在通过技术升级提升系统性能，满足业务快速发展需求。实施方案分为三个阶段，预计工期六个月。', body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph('（一）第一阶段：需求分析与设计', h2_style))
    story.append(Paragraph('本阶段主要完成需求调研、系统设计和技术方案评审，确保项目方向正确、方案可行。', body_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('1. 需求调研', h3_style))
    story.append(Paragraph('与业务部门深入沟通，收集功能需求和非功能需求，明确项目范围和优先级。', body_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('（1）功能需求', h4_style))
    story.append(Paragraph('包括用户管理、权限控制、数据报表、系统集成等核心功能模块。', body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph('（二）第二阶段：开发与测试', h2_style))
    story.append(Paragraph('本阶段完成系统开发、单元测试和集成测试，确保代码质量和系统稳定性。', body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph('（三）第三阶段：部署与上线', h2_style))
    story.append(Paragraph('本阶段完成系统部署、用户培训和正式上线，确保平稳过渡和用户满意度。', body_style))
    story.append(Spacer(1, 20))
    
    # ===== 示例二：字体展示 =====
    story.append(Paragraph('二、字体样式展示', h1_style))
    
    # 标题字体展示
    story.append(Paragraph('（一）标题字体：方正小标宋简体，二号', h2_style))
    title_demo_style = ParagraphStyle(
        'TitleDemo',
        parent=body_style,
        fontName='方正小标宋简体',
        fontSize=22,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    story.append(Paragraph('方正小标宋简体示例', title_demo_style))
    story.append(Paragraph('此字体用于文档主标题，字号二号，居中显示，不加粗。', body_style))
    story.append(Spacer(1, 10))
    
    # 一级标题字体展示
    story.append(Paragraph('（二）一级标题：黑体，三号', h2_style))
    h1_demo_style = ParagraphStyle(
        'H1Demo',
        parent=body_style,
        fontName='黑体',
        fontSize=16,
        spaceAfter=10
    )
    story.append(Paragraph('黑体字示例（一级标题）', h1_demo_style))
    story.append(Paragraph('此字体用于一级标题，字号三号，不加粗，使用中文数字编号（一、二、三...）。', body_style))
    story.append(Spacer(1, 10))
    
    # 二级标题字体展示
    story.append(Paragraph('（三）二级标题：楷体GB2312，三号，加粗', h2_style))
    h2_demo_style = ParagraphStyle(
        'H2Demo',
        parent=body_style,
        fontName='楷体_GB2312',
        fontSize=16,
        bold=True,
        spaceAfter=10
    )
    story.append(Paragraph('楷体GB2312示例（二级标题）', h2_demo_style))
    story.append(Paragraph('此字体用于二级标题，字号三号，加粗显示，使用括号加中文数字编号（（一）（二）...）。', body_style))
    story.append(Spacer(1, 10))
    
    # 三级标题字体展示
    story.append(Paragraph('（四）三级标题：仿宋GB2312，三号', h2_style))
    h3_demo_style = ParagraphStyle(
        'H3Demo',
        parent=body_style,
        fontName='仿宋_GB2312',
        fontSize=16,
        spaceAfter=10
    )
    story.append(Paragraph('仿宋GB2312示例（三级标题）', h3_demo_style))
    story.append(Paragraph('此字体用于三级标题，字号三号，不加粗，使用阿拉伯数字编号（1. 2. 3...）。', body_style))
    story.append(Spacer(1, 10))
    
    # 正文字体展示
    story.append(Paragraph('（五）正文：仿宋GB2312，三号', h2_style))
    story.append(Paragraph('正文使用仿宋GB2312三号字，每段段前缩进两个字符，行距固定值28磅。这是标准的正文格式，用于文档的主要内容阐述和说明。', body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph('多个段落示例：第一段内容结束。第二段开始，同样需要缩进两个字符。正文应当清晰明了，层次分明，便于阅读和理解。', body_style))
    story.append(Spacer(1, 20))
    
    # ===== 示例三：格式规范说明 =====
    story.append(Paragraph('三、格式规范说明', h1_style))
    story.append(Paragraph('以下为文印格式的具体要求，所有文档均应严格遵守：', body_style))
    story.append(Spacer(1, 10))
    
    spec_style = ParagraphStyle(
        'Spec',
        parent=body_style,
        leftIndent=20,
        firstLineIndent=0,
        spaceAfter=8
    )
    
    story.append(Paragraph('1. 页面设置', h3_style))
    story.append(Paragraph('• 纸张：A4（排版纸型A4，文件用纸A3，双面印刷）', spec_style))
    story.append(Paragraph('• 页边距：上3.5cm，下3.5cm，左2.8cm，右2.8cm', spec_style))
    story.append(Paragraph('• 页眉：距页顶2.5cm，黑体小四号加粗', spec_style))
    story.append(Paragraph('• 页脚：距页底2.5cm，黑体小四号加粗', spec_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('2. 字体规范', h3_style))
    story.append(Paragraph('• 标题：方正小标宋简体，二号，居中', spec_style))
    story.append(Paragraph('• 一级标题：黑体字，三号', spec_style))
    story.append(Paragraph('• 二级标题：楷体GB2312，三号，加粗', spec_style))
    story.append(Paragraph('• 三级/四级标题：仿宋GB2312，三号', spec_style))
    story.append(Paragraph('• 正文：仿宋GB2312，三号，段前缩进两字符', spec_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('3. 排版要求', h3_style))
    story.append(Paragraph('• 行距：固定值28磅', spec_style))
    story.append(Paragraph('• 每行28字，每页22行', spec_style))
    story.append(Paragraph('• 不使用自动编号和特殊字符（①、Ⅰ、❶、【】等）', spec_style))
    story.append(Paragraph('• 装订：骑缝订或粘页，不加封面', spec_style))
    story.append(Spacer(1, 20))
    
    # ===== 结束语 =====
    story.append(Paragraph('四、文档状态', h1_style))
    story.append(Paragraph('本文档为示例文档，展示数科公司文印格式规范的实际应用效果。实际使用时，请替换相应内容为实际文档内容。', body_style))
    story.append(Spacer(1, 10))
    
    status_style = ParagraphStyle(
        'Status',
        parent=body_style,
        fontName='黑体',
        fontSize=14,
        alignment=TA_CENTER,
        spaceBefore=20,
        spaceAfter=30
    )
    story.append(Paragraph('—— 文档结束 ——', status_style))
    
    # 构建文档
    print(f"生成文档: {output_path}")
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ 文档生成完成: {output_path}")
    print(f"📄 文件大小: {file_size} 字节")
    
    return output_path

def main():
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = '文印规范完整示例.pdf'
    
    print("=" * 60)
    print("生成完全符合文印格式规范的示例文档")
    print("=" * 60)
    
    try:
        output_path = create_proper_example(output_file)
        print(f"\n✅ 示例文档已生成: {output_path}")
        print("\n文档包含：")
        print("1. 完整文印格式规范展示")
        print("2. 所有字体样式示例")
        print("3. 格式规范说明")
        print("4. 正确的页眉页脚设置")
        return 0
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())