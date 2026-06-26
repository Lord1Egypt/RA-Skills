#!/usr/bin/env python3
"""
数科公司文印格式文档生成器
根据文印格式要求生成PDF文档
"""
import os
import sys
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors

class DocumentGenerator:
    """文印格式文档生成器"""
    
    def __init__(self, output_path):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._register_fonts()
        self._create_styles()
        
    def _register_fonts(self):
        """注册所需字体"""
        # 字体文件路径映射 - 使用中文字体名称作为键
        font_files = {
            '方正小标宋简体': self._find_font_file('FZXiaoBiaoSong-B05S', '方正小标宋简体', '方正小标宋简体.TTF'),
            '黑体': self._find_font_file('SimHei', '黑体', 'SIMHEI.TTF'),
            '楷体_GB2312': self._find_font_file('KaiTi_GB2312', '楷体_GB2312', '楷体_GB2312.TTF'),
            '仿宋_GB2312': self._find_font_file('FangSong_GB2312', '仿宋_GB2312', '仿宋_GB2312.TTF'),
            # 备用字体
            '楷体': self._find_font_file('KaiTi', '楷体', 'SIMKAI.TTF'),
            '仿宋': self._find_font_file('FangSong', '仿宋', 'SIMFANG.TTF'),
            '方正小标宋_GBK': self._find_font_file('FZXiaoBiaoSong-B05', '方正小标宋_GBK', '方正小标宋_GBK.TTF'),
        }
        
        self.available_fonts = {}
        for font_name, font_path in font_files.items():
            if font_path and os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    addMapping(font_name, 0, 0, font_name)  # normal
                    addMapping(font_name, 0, 1, font_name)  # bold
                    self.available_fonts[font_name] = True
                    print(f"✓ 字体已注册: {font_name}")
                except Exception as e:
                    print(f"✗ 注册字体失败 {font_name}: {e}")
                    self.available_fonts[font_name] = False
            else:
                print(f"⚠️ 字体文件不存在: {font_name}")
                self.available_fonts[font_name] = False
        
        # 向后兼容性：保留旧键名
        if '黑体' in self.available_fonts:
            self.available_fonts['SimHei'] = self.available_fonts['黑体']
        if '楷体' in self.available_fonts:
            self.available_fonts['KaiTi'] = self.available_fonts['楷体']
    
    def _find_font_file(self, en_name, zh_name, filename):
        """查找字体文件"""
        # 1. 检查系统安装路径
        system_path = f'/usr/share/fonts/truetype/sim/{filename}'
        if os.path.exists(system_path):
            return system_path
        
        # 2. 检查工作区备份
        workspace_path = os.path.join(
            os.path.expanduser('~/.openclaw/workspace/fonts'),
            filename
        )
        if os.path.exists(workspace_path):
            return workspace_path
        
        # 3. 使用fc-list查找
        import subprocess
        try:
            for name in [en_name, zh_name]:
                result = subprocess.run(
                    ['fc-list', name, 'file'],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if ':' in line:
                            file_path = line.split(':')[1].strip()
                            if os.path.exists(file_path):
                                return file_path
        except Exception:
            pass
        
        return None
    
    def _create_styles(self):
        """创建文印格式样式"""
        
        # 获取实际可用字体，优先使用规范字体，不可用时使用备用字体
        title_font = '方正小标宋简体' if self.available_fonts.get('方正小标宋简体') else '黑体'
        h1_font = '黑体' if self.available_fonts.get('黑体') else 'Helvetica-Bold'
        h2_font = '楷体_GB2312' if self.available_fonts.get('楷体_GB2312') else '楷体'
        body_font = '仿宋_GB2312' if self.available_fonts.get('仿宋_GB2312') else '仿宋'
        
        # 如果仿宋不可用，使用楷体
        if not self.available_fonts.get('仿宋_GB2312') and not self.available_fonts.get('仿宋'):
            body_font = '楷体_GB2312' if self.available_fonts.get('楷体_GB2312') else '楷体'
        
        # 如果楷体GB2312不可用，使用普通楷体
        if not self.available_fonts.get('楷体_GB2312') and not self.available_fonts.get('楷体'):
            h2_font = '黑体'
        
        # 如果黑体不可用，使用Helvetica-Bold
        if not self.available_fonts.get('黑体'):
            h1_font = 'Helvetica-Bold'
            title_font = 'Helvetica-Bold' if title_font == '黑体' else title_font
        
        # 标题样式（方正小标宋简体，二号，居中）
        self.title_style = ParagraphStyle(
            'DocTitle',
            parent=self.styles['Heading1'],
            fontName=title_font,
            fontSize=22,  # 二号约22pt
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.black
        )
        
        # 一级标题（黑体字，三号）
        self.h1_style = ParagraphStyle(
            'DocH1',
            parent=self.styles['Heading1'],
            fontName=h1_font,
            fontSize=16,  # 三号约16pt
            spaceBefore=12,
            spaceAfter=12,
            textColor=colors.black
        )
        
        # 二级标题（楷体GB2312，三号，加粗）
        self.h2_style = ParagraphStyle(
            'DocH2',
            parent=self.styles['Heading2'],
            fontName=h2_font,
            fontSize=16,
            bold=True,
            spaceBefore=10,
            spaceAfter=10,
            textColor=colors.black
        )
        
        # 三级标题（仿宋GB2312，三号）
        self.h3_style = ParagraphStyle(
            'DocH3',
            parent=self.styles['Heading3'],
            fontName=body_font,
            fontSize=16,
            spaceBefore=8,
            spaceAfter=8,
            textColor=colors.black
        )
        
        # 四级标题（仿宋GB2312，三号）
        self.h4_style = ParagraphStyle(
            'DocH4',
            parent=self.styles['Heading4'],
            fontName=body_font,
            fontSize=16,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.black
        )
        
        # 正文样式（仿宋GB2312，三号）
        self.body_style = ParagraphStyle(
            'DocBody',
            parent=self.styles['Normal'],
            fontName=body_font,
            fontSize=16,
            leading=28,  # 固定值28磅
            firstLineIndent=32,  # 缩进两个字符（约32pt）
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            textColor=colors.black
        )
        
        # 列表样式
        self.bullet_style = ParagraphStyle(
            'DocBullet',
            parent=self.body_style,
            leftIndent=20,
            firstLineIndent=-20,
            spaceAfter=8
        )
        
        # 页眉页脚样式（小四号，黑体，加粗）
        self.header_style = ParagraphStyle(
            'DocHeader',
            parent=self.styles['Normal'],
            fontName='黑体' if self.available_fonts.get('黑体') else 'Helvetica-Bold',
            fontSize=12,  # 小四号约12pt
            alignment=TA_CENTER,
            textColor=colors.black
        )
    
    def _create_header_footer(self, canvas, doc):
        """创建页眉页脚"""
        canvas.saveState()
        
        # 页眉（距页顶2.5cm）
        canvas.setFont('黑体' if self.available_fonts.get('黑体') else 'Helvetica-Bold', 12)
        canvas.drawCentredString(
            A4[0] / 2.0,
            A4[1] - 2.5*cm,
            "数科公司文印格式文档"
        )
        
        # 页脚（距页底2.5cm）
        canvas.setFont('黑体' if self.available_fonts.get('黑体') else 'Helvetica-Bold', 12)
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
    
    def generate(self, document_data):
        """
        生成文档
        
        Args:
            document_data: 文档数据字典，包含：
                - title: 文档标题
                - author: 作者（可选）
                - date: 日期（可选）
                - sections: 章节列表，每个章节为字典：
                    - level: 1-4 (标题级别)
                    - title: 章节标题
                    - content: 正文内容（字符串或列表）
                    - subsections: 子章节列表（可选）
        """
        print(f"开始生成文档: {self.output_path}")
        
        # 创建文档模板
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2.8*cm,
            leftMargin=2.8*cm,
            topMargin=3.5*cm,
            bottomMargin=3.5*cm,
            title=document_data.get('title', '未命名文档')
        )
        
        story = []
        
        # 添加标题
        title = document_data.get('title', '')
        if title:
            story.append(Paragraph(title, self.title_style))
            story.append(Spacer(1, 20))
        
        # 添加作者和日期
        meta_info = []
        if document_data.get('author'):
            meta_info.append(f"起草人：{document_data['author']}")
        if document_data.get('date'):
            meta_info.append(f"日期：{document_data['date']}")
        else:
            meta_info.append(f"日期：{datetime.now().strftime('%Y年%m月%d日')}")
        
        if meta_info:
            meta_style = ParagraphStyle(
                'MetaInfo',
                parent=self.body_style,
                alignment=TA_CENTER,
                fontSize=14,
                spaceAfter=30
            )
            story.append(Paragraph(' | '.join(meta_info), meta_style))
            story.append(Spacer(1, 20))
        
        # 添加章节
        sections = document_data.get('sections', [])
        for i, section in enumerate(sections):
            self._add_section(story, section, i+1)
        
        # 构建文档
        doc.build(story, onFirstPage=self._create_header_footer,
                 onLaterPages=self._create_header_footer)
        
        print(f"✅ 文档生成完成: {self.output_path}")
        print(f"📄 文件大小: {os.path.getsize(self.output_path)} 字节")
        
        return self.output_path
    
    def _add_section(self, story, section, section_num=None):
        """添加章节到文档"""
        level = section.get('level', 1)
        title = section.get('title', '')
        content = section.get('content', '')
        subsections = section.get('subsections', [])
        
        # 添加章节标题
        if title:
            # 根据标题级别添加编号
            if level == 1:
                title_text = f"{self._number_to_chinese(section_num)}、{title}"
                story.append(Paragraph(title_text, self.h1_style))
            elif level == 2:
                title_text = f"（{self._number_to_chinese(section_num)}）{title}"
                story.append(Paragraph(title_text, self.h2_style))
            elif level == 3:
                title_text = f"{section_num}. {title}"
                story.append(Paragraph(title_text, self.h3_style))
            elif level == 4:
                title_text = f"（{section_num}）{title}"
                story.append(Paragraph(title_text, self.h4_style))
            else:
                story.append(Paragraph(title, self.h4_style))
        
        # 添加章节内容
        if content:
            if isinstance(content, list):
                # 内容为列表（多个段落）
                for para in content:
                    story.append(Paragraph(para, self.body_style))
            else:
                # 内容为字符串
                story.append(Paragraph(content, self.body_style))
        
        # 添加子章节
        for j, subsection in enumerate(subsections, 1):
            subsection['level'] = level + 1
            self._add_section(story, subsection, j)
        
        # 章节间距
        if level <= 2:
            story.append(Spacer(1, 15))
        else:
            story.append(Spacer(1, 10))
    
    def _number_to_chinese(self, num):
        """数字转中文数字（一、二、三...）"""
        chinese_nums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        if 1 <= num <= 10:
            return chinese_nums[num-1]
        else:
            return str(num)
    
    def create_example_document(self):
        """创建示例文档"""
        example_data = {
            'title': '数科公司项目实施方案',
            'author': '技术部',
            'date': '2026年3月27日',
            'sections': [
                {
                    'level': 1,
                    'title': '项目背景与目标',
                    'content': [
                        '随着数字化转型的深入推进，公司业务系统面临升级改造的需求。',
                        '本项目旨在构建新一代业务平台，提升系统性能与用户体验。'
                    ],
                    'subsections': [
                        {
                            'level': 2,
                            'title': '项目背景',
                            'content': '当前系统已运行多年，存在性能瓶颈和技术债务，难以满足业务快速发展需求。'
                        },
                        {
                            'level': 2,
                            'title': '项目目标',
                            'content': '通过技术架构升级，实现系统性能提升50%，用户体验改善，运维成本降低30%。'
                        }
                    ]
                },
                {
                    'level': 1,
                    'title': '实施计划',
                    'content': '项目实施分为三个阶段，预计工期6个月。',
                    'subsections': [
                        {
                            'level': 2,
                            'title': '第一阶段：需求分析与设计',
                            'content': '完成需求调研、系统设计和技术方案评审。',
                            'subsections': [
                                {
                                    'level': 3,
                                    'title': '需求调研',
                                    'content': '与业务部门沟通，收集功能需求和非功能需求。'
                                },
                                {
                                    'level': 3,
                                    'title': '系统设计',
                                    'content': '完成系统架构设计、数据库设计和接口设计。'
                                }
                            ]
                        },
                        {
                            'level': 2,
                            'title': '第二阶段：开发与测试',
                            'content': '完成系统开发、单元测试和集成测试。'
                        },
                        {
                            'level': 2,
                            'title': '第三阶段：部署与上线',
                            'content': '完成系统部署、用户培训和正式上线。'
                        }
                    ]
                },
                {
                    'level': 1,
                    'title': '资源需求',
                    'content': '项目所需资源包括人力、设备和预算。',
                    'subsections': [
                        {
                            'level': 2,
                            'title': '人力资源',
                            'content': '需要项目经理1名、开发工程师3名、测试工程师1名。'
                        },
                        {
                            'level': 2,
                            'title': '设备资源',
                            'content': '需要服务器5台、网络设备若干、开发测试环境。'
                        }
                    ]
                }
            ]
        }
        
        return self.generate(example_data)

def main():
    """主函数"""
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = '文印格式文档示例.pdf'
    
    # 创建生成器
    generator = DocumentGenerator(output_file)
    
    # 检查字体状态
    print("=" * 60)
    print("文档生成器状态检查")
    print("=" * 60)
    print(f"楷体可用: {'✓' if generator.available_fonts.get('KaiTi') else '✗'}")
    print(f"黑体可用: {'✓' if generator.available_fonts.get('SimHei') else '✗'}")
    
    # 创建示例文档
    print("\n" + "=" * 60)
    print("生成示例文档")
    print("=" * 60)
    
    output_path = generator.create_example_document()
    
    print("\n" + "=" * 60)
    print("使用说明")
    print("=" * 60)
    print("1. 自定义文档内容:")
    print("   from doc_generator import DocumentGenerator")
    print("   generator = DocumentGenerator('output.pdf')")
    print("   generator.generate(your_document_data)")
    print("\n2. document_data格式:")
    print("   {'title': '文档标题', 'author': '作者', 'sections': [...]}")
    print("\n3. 章节格式:")
    print("   {'level': 1, 'title': '标题', 'content': '内容', 'subsections': [...]}")
    
    return output_path

if __name__ == '__main__':
    main()