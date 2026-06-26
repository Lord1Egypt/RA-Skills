#!/usr/bin/env python3
"""
文档鉴别材料PDF生成器
根据软件信息生成符合软著申请要求的用户手册PDF。
- 至少60页，每页不少于30行
- 包含软件名称、版本号、权利人信息
- 中文支持（自动查找系统中文字体）

使用方式：
  1. 从JSON配置生成：python generate_doc_pdf.py --config software_info.json
  2. 从已有文档转换：python generate_doc_pdf.py --input existing_doc.txt --name "软件名" --version "V1.0" --author "权利人"
"""

import argparse
import json
import os
import sys
import re
import textwrap
from pathlib import Path
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, cm
    from reportlab.lib.colors import HexColor, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     PageBreak, Table, TableStyle, Image,
                                     ListFlowable, ListItem)
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("错误：需要安装 reportlab 库")
    print("请运行：pip install reportlab")
    sys.exit(1)

# ============================================================
# 配置
# ============================================================
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 25 * mm
MIN_LINES_PER_PAGE = 30
MIN_PAGES = 60

# 中文字体查找路径
CHINESE_FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/simhei.ttf",
]

CHINESE_BOLD_FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",  # subfontIndex=1 for bold
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
]


def find_font(font_paths, font_name, subfont=0):
    """查找并注册字体。"""
    for path in font_paths:
        if os.path.exists(path):
            try:
                if path.endswith('.ttc'):
                    pdfmetrics.registerFont(TTFont(font_name, path, subfontIndex=subfont))
                else:
                    pdfmetrics.registerFont(TTFont(font_name, path))
                return font_name
            except Exception:
                continue
    return None


def setup_fonts():
    """初始化字体。"""
    cn = find_font(CHINESE_FONT_PATHS, "CN", 0)
    cn_bold = find_font(CHINESE_BOLD_FONT_PATHS, "CNBold", 1)
    if not cn_bold:
        cn_bold = find_font(CHINESE_BOLD_FONT_PATHS, "CNBold", 0)
    if not cn:
        print("警告：未找到中文字体")
        cn = "Helvetica"
    if not cn_bold:
        cn_bold = cn
    return cn, cn_bold


def create_styles(cn_font, cn_bold_font):
    """创建文档样式。"""
    styles = {}

    styles['title'] = ParagraphStyle(
        'Title', fontName=cn_bold_font, fontSize=22, leading=30,
        alignment=TA_CENTER, spaceAfter=20, textColor=HexColor('#1a1a1a')
    )
    styles['subtitle'] = ParagraphStyle(
        'Subtitle', fontName=cn_font, fontSize=14, leading=20,
        alignment=TA_CENTER, spaceAfter=10, textColor=HexColor('#555555')
    )
    styles['h1'] = ParagraphStyle(
        'H1', fontName=cn_bold_font, fontSize=18, leading=26,
        spaceBefore=24, spaceAfter=12, textColor=HexColor('#1a1a1a')
    )
    styles['h2'] = ParagraphStyle(
        'H2', fontName=cn_bold_font, fontSize=15, leading=22,
        spaceBefore=18, spaceAfter=8, textColor=HexColor('#2a2a2a')
    )
    styles['h3'] = ParagraphStyle(
        'H3', fontName=cn_bold_font, fontSize=12, leading=18,
        spaceBefore=12, spaceAfter=6, textColor=HexColor('#333333')
    )
    styles['body'] = ParagraphStyle(
        'Body', fontName=cn_font, fontSize=10.5, leading=18,
        alignment=TA_JUSTIFY, spaceAfter=6, firstLineIndent=21,
        textColor=HexColor('#1a1a1a')
    )
    styles['body_no_indent'] = ParagraphStyle(
        'BodyNoIndent', fontName=cn_font, fontSize=10.5, leading=18,
        alignment=TA_LEFT, spaceAfter=6, textColor=HexColor('#1a1a1a')
    )
    styles['bullet'] = ParagraphStyle(
        'Bullet', fontName=cn_font, fontSize=10.5, leading=18,
        leftIndent=20, bulletIndent=10, spaceAfter=4,
        textColor=HexColor('#1a1a1a')
    )
    styles['table_header'] = ParagraphStyle(
        'TableHeader', fontName=cn_bold_font, fontSize=10, leading=14,
        alignment=TA_CENTER, textColor=HexColor('#1a1a1a')
    )
    styles['table_cell'] = ParagraphStyle(
        'TableCell', fontName=cn_font, fontSize=10, leading=14,
        alignment=TA_LEFT, textColor=HexColor('#1a1a1a')
    )
    styles['footer'] = ParagraphStyle(
        'Footer', fontName=cn_font, fontSize=8, leading=12,
        alignment=TA_CENTER, textColor=HexColor('#999999')
    )

    return styles


# ============================================================
# 页眉/页脚
# ============================================================
class DocTemplate(SimpleDocTemplate):
    """带页眉页脚的文档模板。"""

    def __init__(self, *args, software_name="", version="", copyright_holder="",
                 cn_font="Helvetica", **kwargs):
        self.software_name = software_name
        self.version = version
        self.copyright_holder = copyright_holder
        self.cn_font_name = cn_font
        super().__init__(*args, **kwargs)

    def afterPage(self):
        """每页结束后绘制页眉页脚。"""
        c = self.canv
        page_num = c.getPageNumber()

        # 页眉
        c.setFont(self.cn_font_name, 9)
        c.setFillColor(HexColor('#666666'))
        header_text = f"{self.software_name} {self.version} 用户手册"
        c.drawString(MARGIN, PAGE_HEIGHT - 15 * mm, header_text)
        c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 15 * mm,
                          f"第 {page_num} 页")

        # 页眉分隔线
        c.setStrokeColor(HexColor('#CCCCCC'))
        c.setLineWidth(0.5)
        c.line(MARGIN, PAGE_HEIGHT - 18 * mm,
               PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 18 * mm)

        # 页脚分隔线
        c.line(MARGIN, 15 * mm, PAGE_WIDTH - MARGIN, 15 * mm)

        # 页脚
        c.setFont(self.cn_font_name, 8)
        c.setFillColor(HexColor('#999999'))
        c.drawCentredString(PAGE_WIDTH / 2, 10 * mm,
                            f"© {datetime.now().year} {self.copyright_holder} 版权所有")


# ============================================================
# 用户手册内容生成
# ============================================================
def generate_manual_content(info, styles):
    """
    根据软件信息生成用户手册内容。
    info 字典应包含:
    - software_name: 软件全称
    - software_short_name: 软件简称
    - version: 版本号
    - author: 权利人/著作权人
    - category: 软件分类
    - dev_hardware: 开发硬件环境
    - run_hardware: 运行硬件环境
    - dev_os: 开发操作系统
    - dev_tools: 开发工具
    - run_os: 运行平台/操作系统
    - run_support: 运行支撑环境
    - languages: 编程语言列表
    - source_lines: 源程序量
    - purpose: 开发目的
    - domain: 面向领域
    - main_functions: 主要功能
    - tech_features: 技术特点补充说明
    - tech_tags: 技术标签列表
    - functions_detail: 可选，详细功能描述字典 {模块名: 描述}
    """
    story = []
    name = info.get('software_name', '软件')
    short = info.get('software_short_name', '')
    ver = info.get('version', 'V1.0')
    author = info.get('author', '')
    display_name = short if short else name

    # ======== 封面 ========
    story.append(Spacer(1, 80 * mm))
    story.append(Paragraph(name, styles['title']))
    story.append(Paragraph(f"用户手册", styles['title']))
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph(f"版本：{ver}", styles['subtitle']))
    if author:
        story.append(Paragraph(f"著作权人：{author}", styles['subtitle']))
    story.append(Paragraph(f"日期：{datetime.now().strftime('%Y年%m月')}", styles['subtitle']))
    story.append(PageBreak())

    # ======== 版权声明 ========
    story.append(Paragraph("版权声明", styles['h1']))
    story.append(Paragraph(
        f"本文档是{name}（以下简称\"{display_name}\"）的用户手册。本文档的版权归{author}所有。"
        f"未经{author}书面许可，任何单位和个人不得以任何形式复制、传播本文档的全部或部分内容。",
        styles['body']
    ))
    story.append(Paragraph(
        f"{name}的著作权归{author}所有，受中华人民共和国著作权法及国际版权公约的保护。"
        f"任何未经授权的复制、修改、分发或使用本软件及相关文档的行为，均属于侵权行为，"
        f"将依法追究法律责任。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本文档中的信息如有变更，恕不另行通知。{author}保留对本文档进行修改和更新的权利。"
        f"本文档仅供{display_name}的合法用户参考使用。",
        styles['body']
    ))
    story.append(PageBreak())

    # ======== 目录（文字版） ========
    story.append(Paragraph("目  录", styles['title']))
    story.append(Spacer(1, 10 * mm))
    toc_items = [
        "第一章  概述",
        "    1.1 软件简介",
        "    1.2 开发背景与目的",
        "    1.3 面向领域与适用范围",
        "    1.4 软件特点与优势",
        "    1.5 文档说明",
        "第二章  系统环境要求",
        "    2.1 硬件环境要求",
        "    2.2 软件环境要求",
        "    2.3 网络环境要求",
        "    2.4 环境配置建议",
        "第三章  安装与部署",
        "    3.1 安装准备",
        "    3.2 安装步骤",
        "    3.3 安装验证",
        "    3.4 卸载说明",
        "    3.5 升级说明",
        "第四章  系统架构",
        "    4.1 总体架构",
        "    4.2 技术架构",
        "    4.3 功能架构",
        "    4.4 数据架构",
        "    4.5 安全架构",
        "第五章  功能详细说明",
        "    5.1 功能概览",
    ]
    # 动态添加功能模块目录
    functions_detail = info.get('functions_detail', {})
    main_funcs = info.get('main_functions', '')
    if functions_detail:
        for i, mod_name in enumerate(functions_detail.keys(), 2):
            toc_items.append(f"    5.{i} {mod_name}")
    toc_items.extend([
        "第六章  操作指南",
        "    6.1 系统登录与退出",
        "    6.2 界面布局说明",
        "    6.3 基本操作流程",
        "    6.4 常用操作说明",
        "    6.5 数据管理操作",
        "    6.6 高级操作",
        "第七章  系统管理",
        "    7.1 用户管理",
        "    7.2 权限管理",
        "    7.3 系统配置",
        "    7.4 日志管理",
        "    7.5 数据备份与恢复",
        "第八章  接口说明",
        "    8.1 接口概述",
        "    8.2 接口规范",
        "    8.3 接口安全",
        "第九章  安全说明",
        "    9.1 安全机制概述",
        "    9.2 身份认证",
        "    9.3 访问控制",
        "    9.4 数据安全",
        "    9.5 安全审计",
        "第十章  常见问题与解决方案",
        "    10.1 安装常见问题",
        "    10.2 使用常见问题",
        "    10.3 性能优化建议",
        "    10.4 错误代码说明",
        "附录A  术语表",
        "附录B  技术规格",
        "附录C  更新日志",
    ])
    for item in toc_items:
        story.append(Paragraph(item, styles['body_no_indent']))
    story.append(PageBreak())

    # ======== 第一章 概述 ========
    story.append(Paragraph("第一章  概述", styles['h1']))

    story.append(Paragraph("1.1 软件简介", styles['h2']))
    story.append(Paragraph(
        f"{name}（版本：{ver}）是一款面向{info.get('domain', '相关行业')}的"
        f"{info.get('category', '应用软件')}。"
        f"本软件使用{', '.join(info.get('languages', ['未知']))}等编程语言开发，"
        f"源程序量约{info.get('source_lines', 0)}行，具备完善的功能体系和良好的用户体验。",
        styles['body']
    ))
    if short:
        story.append(Paragraph(
            f"为便于表述，本手册以下内容将{name}简称为\"{short}\"。", styles['body']
        ))
    story.append(Paragraph(
        f"{display_name}致力于为用户提供专业、高效、安全的解决方案。软件采用先进的技术架构，"
        f"具备良好的可扩展性和可维护性，能够满足用户在日常业务场景中的各类需求。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本软件经过严格的开发流程和质量保证，包括需求分析、系统设计、编码实现、"
        f"单元测试、集成测试和系统测试等环节，确保软件的可靠性和稳定性。",
        styles['body']
    ))

    story.append(Paragraph("1.2 开发背景与目的", styles['h2']))
    purpose = info.get('purpose', '提升业务效率')
    story.append(Paragraph(
        f"随着信息技术的快速发展和{info.get('domain', '行业')}的数字化转型需求日益增长，"
        f"传统的业务处理方式已无法满足日益增长的效率和质量要求。在此背景下，{display_name}应运而生。",
        styles['body']
    ))
    story.append(Paragraph(f"本软件的开发目的为：{purpose}。", styles['body']))
    story.append(Paragraph(
        f"通过深入调研和分析{info.get('domain', '行业')}的业务需求与痛点，"
        f"研发团队采用先进的软件工程方法和技术手段，精心设计并开发了{display_name}。"
        f"软件旨在通过信息化手段优化业务流程、提高工作效率、降低运营成本，"
        f"为用户创造更大的价值。",
        styles['body']
    ))

    story.append(Paragraph("1.3 面向领域与适用范围", styles['h2']))
    story.append(Paragraph(
        f"{display_name}主要面向{info.get('domain', '相关领域')}，"
        f"适用于该领域中的各类组织和个人用户。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本软件的目标用户包括但不限于：行业从业人员、管理人员、技术人员以及决策者等。"
        f"无论是大型企业还是中小型组织，都可以根据自身需求使用{display_name}提供的功能模块，"
        f"实现业务流程的标准化和自动化。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本软件适用的主要业务场景包括：日常业务处理、数据分析与报表生成、"
        f"信息管理与共享、流程审批与协作等。用户可以根据实际业务需求灵活配置和使用各项功能。",
        styles['body']
    ))

    story.append(Paragraph("1.4 软件特点与优势", styles['h2']))
    tech_features = info.get('tech_features', '')
    tech_tags = info.get('tech_tags', [])

    features_list = [
        f"专业性：专为{info.get('domain', '行业')}设计，深度理解行业需求",
        f"易用性：界面友好、操作简便，降低用户学习成本",
        f"安全性：多层次安全防护机制，确保数据安全",
        f"可扩展：模块化设计，支持功能扩展和定制",
        f"高性能：优化的技术架构，保证系统响应速度",
        f"稳定性：经过严格测试验证，运行稳定可靠",
    ]
    for feat in features_list:
        story.append(Paragraph(f"• {feat}", styles['bullet']))

    if tech_tags:
        story.append(Paragraph(
            f"本软件在技术层面属于{'、'.join(tech_tags)}类型。{tech_features}",
            styles['body']
        ))
    elif tech_features:
        story.append(Paragraph(f"技术特点：{tech_features}", styles['body']))

    story.append(Paragraph("1.5 文档说明", styles['h2']))
    story.append(Paragraph(
        f"本手册是{name}{ver}版本的用户手册，旨在帮助用户了解和使用{display_name}的各项功能。"
        f"本手册详细描述了软件的安装部署、功能特性、操作方法、系统管理和常见问题处理等内容。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本手册适用于所有{display_name}的用户，包括系统管理员、普通用户和技术维护人员。"
        f"建议用户在使用软件前仔细阅读本手册，以充分了解软件的功能和使用方法。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本手册中的内容基于{name}{ver}版本编写。如软件版本更新导致功能变化，"
        f"请参考对应版本的用户手册。如有疑问，请联系技术支持获取帮助。",
        styles['body']
    ))
    story.append(Paragraph(
        f"本文档中使用以下约定：粗体文字表示界面元素名称（如按钮、菜单项）；"
        f"等宽字体表示需要用户输入的内容或系统路径；"
        f"注意事项将以特别标注的方式呈现，请读者留意。",
        styles['body']
    ))
    story.append(PageBreak())

    # ======== 第二章 系统环境要求 ========
    story.append(Paragraph("第二章  系统环境要求", styles['h1']))
    story.append(Paragraph(
        f"本章详细介绍运行{display_name}所需的硬件环境、软件环境和网络环境要求，"
        f"以帮助用户正确配置运行环境，确保软件能够正常安装和运行。",
        styles['body']
    ))

    story.append(Paragraph("2.1 硬件环境要求", styles['h2']))
    story.append(Paragraph(
        f"{display_name}对运行硬件有一定的基本要求。满足以下硬件配置要求可确保软件的正常运行：",
        styles['body']
    ))
    hw_data = [
        [Paragraph("项目", styles['table_header']),
         Paragraph("最低要求", styles['table_header']),
         Paragraph("推荐配置", styles['table_header'])],
    ]
    run_hw = info.get('run_hardware', 'PC服务器')
    story.append(Paragraph(
        f"运行硬件环境：{run_hw}。用户应确保硬件设备满足上述要求，"
        f"以获得最佳的软件运行体验。在实际生产环境中，建议使用推荐配置或更高配置，"
        f"以应对高并发访问和大数据量处理的需求。",
        styles['body']
    ))
    story.append(Paragraph(
        f"对于开发环境，建议使用以下硬件配置：{info.get('dev_hardware', '无特殊要求')}。"
        f"开发环境的硬件配置直接影响开发效率和编译速度，建议开发人员使用性能较好的设备。",
        styles['body']
    ))

    story.append(Paragraph("2.2 软件环境要求", styles['h2']))
    story.append(Paragraph(
        f"运行{display_name}需要以下软件环境支持：",
        styles['body']
    ))
    story.append(Paragraph(
        f"操作系统：{info.get('run_os', '请参考系统要求')}。请确保操作系统已安装最新的安全补丁和更新。",
        styles['body']
    ))
    story.append(Paragraph(
        f"运行支撑环境：{info.get('run_support', '请参考系统要求')}。"
        f"所有依赖软件应安装对应版本或更高版本，以确保兼容性。",
        styles['body']
    ))
    story.append(Paragraph(
        f"开发环境方面，本软件使用以下环境开发：操作系统为{info.get('dev_os', '无特殊要求')}，"
        f"开发工具为{info.get('dev_tools', '无特殊要求')}，"
        f"编程语言为{', '.join(info.get('languages', []))}。",
        styles['body']
    ))

    story.append(Paragraph("2.3 网络环境要求", styles['h2']))
    story.append(Paragraph(
        f"如果{display_name}需要网络功能支持，请确保以下网络环境条件满足：",
        styles['body']
    ))
    net_items = [
        "网络连接：稳定的网络连接（有线或无线网络均可）",
        "带宽要求：建议最低带宽不低于10Mbps，推荐100Mbps及以上",
        "防火墙设置：确保软件所需的网络端口未被防火墙封锁",
        "DNS配置：确保DNS解析正常，能够正确访问所需的网络服务",
        "代理设置：如使用网络代理，需正确配置代理参数",
    ]
    for item in net_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(Paragraph(
        f"在网络环境受限的情况下，{display_name}的部分功能（如在线更新、数据同步等）"
        f"可能无法正常使用。建议在良好的网络环境下使用软件的全部功能。",
        styles['body']
    ))

    story.append(Paragraph("2.4 环境配置建议", styles['h2']))
    story.append(Paragraph(
        f"为确保{display_name}的最佳运行效果，建议用户注意以下配置事项：",
        styles['body']
    ))
    config_tips = [
        "定期更新操作系统和依赖软件的安全补丁",
        "确保系统时钟准确，建议启用NTP时间同步",
        "为软件分配足够的磁盘空间，建议预留至少20%的空闲磁盘空间",
        "在生产环境中，建议使用独立的服务器或虚拟机部署",
        "配置适当的系统日志轮转策略，避免日志文件过大占用磁盘空间",
        "建议开启操作系统的防火墙，并只开放必要的端口",
        "定期备份系统配置和业务数据，制定灾难恢复计划",
    ]
    for tip in config_tips:
        story.append(Paragraph(f"• {tip}", styles['bullet']))
    story.append(PageBreak())

    # ======== 第三章 安装与部署 ========
    story.append(Paragraph("第三章  安装与部署", styles['h1']))
    story.append(Paragraph(
        f"本章详细介绍{display_name}的安装部署流程，包括安装前的准备工作、"
        f"详细的安装步骤、安装后的验证方法以及卸载和升级说明。",
        styles['body']
    ))

    story.append(Paragraph("3.1 安装准备", styles['h2']))
    story.append(Paragraph(
        f"在安装{display_name}之前，请完成以下准备工作：",
        styles['body']
    ))
    prep_items = [
        "确认硬件和软件环境满足第二章所述的要求",
        "获取软件安装包及相关许可文件",
        "备份现有系统数据和配置（如为升级安装）",
        "确认操作系统已安装所需的运行时环境和依赖库",
        "确保有足够的磁盘空间用于安装",
        "准备数据库环境（如软件需要数据库支持）",
        "关闭可能影响安装的杀毒软件或安全软件",
        "确保当前登录用户具有管理员权限",
    ]
    for item in prep_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))

    story.append(Paragraph("3.2 安装步骤", styles['h2']))
    story.append(Paragraph(
        f"以下是{display_name}的详细安装步骤。请按照顺序逐步执行：",
        styles['body']
    ))
    install_steps = [
        ("步骤一：解压安装包",
         f"将{display_name}安装包解压到目标目录。建议选择路径中不含中文和空格的目录作为安装路径。"
         f"解压完成后，检查文件完整性，确保所有文件都已正确解压。"),
        ("步骤二：配置环境",
         f"根据实际运行环境修改配置文件。主要配置项包括：数据库连接信息、服务端口号、"
         f"日志存储路径、缓存配置等。配置文件中包含详细的注释说明，请根据实际情况修改。"),
        ("步骤三：初始化数据",
         f"运行初始化脚本完成数据库表结构创建和基础数据导入。"
         f"初始化过程中请确保数据库连接正常，并注意查看初始化日志中是否有错误信息。"),
        ("步骤四：启动服务",
         f"使用启动脚本或命令启动{display_name}服务。启动后请查看运行日志确认服务是否正常运行。"
         f"首次启动可能需要较长时间用于数据预处理，请耐心等待。"),
        ("步骤五：访问验证",
         f"服务启动成功后，通过配置的访问地址访问{display_name}。"
         f"首次访问时需要使用默认管理员账号登录，并建议立即修改默认密码。"),
    ]
    for title, desc in install_steps:
        story.append(Paragraph(title, styles['h3']))
        story.append(Paragraph(desc, styles['body']))

    story.append(Paragraph("3.3 安装验证", styles['h2']))
    story.append(Paragraph(
        f"安装完成后，建议执行以下验证步骤以确保{display_name}已正确安装：",
        styles['body']
    ))
    verify_items = [
        "检查服务进程是否正常运行",
        "访问软件界面，确认能够正常打开",
        "使用管理员账号登录，确认登录功能正常",
        "测试核心功能模块是否可用",
        "检查日志文件中是否有异常错误信息",
        "验证数据库连接是否正常",
        "测试文件读写权限是否正确",
    ]
    for item in verify_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))

    story.append(Paragraph("3.4 卸载说明", styles['h2']))
    story.append(Paragraph(
        f"如需卸载{display_name}，请按照以下步骤操作：首先停止所有正在运行的服务进程；"
        f"其次备份需要保留的数据和配置文件；然后删除安装目录及相关文件；"
        f"最后清理数据库中的相关数据（如不再需要）。"
        f"卸载前请确保已备份所有重要数据，卸载操作不可逆。",
        styles['body']
    ))

    story.append(Paragraph("3.5 升级说明", styles['h2']))
    story.append(Paragraph(
        f"升级{display_name}时，请注意以下事项：升级前务必备份当前版本的程序文件、"
        f"配置文件和数据库；阅读版本更新说明，了解新版本的变更内容和注意事项；"
        f"按照升级指南的步骤进行操作；升级完成后执行验证测试确保功能正常。"
        f"如升级过程中出现问题，可使用备份文件回退到升级前的版本。",
        styles['body']
    ))
    story.append(PageBreak())

    # ======== 第四章 系统架构 ========
    story.append(Paragraph("第四章  系统架构", styles['h1']))

    story.append(Paragraph("4.1 总体架构", styles['h2']))
    story.append(Paragraph(
        f"{display_name}采用分层架构设计，整体架构清晰、层次分明。"
        f"系统从上到下分为表示层、业务逻辑层、数据访问层和数据存储层。"
        f"各层之间通过定义良好的接口进行通信，降低了层间耦合度，提高了系统的可维护性和可扩展性。",
        styles['body']
    ))
    story.append(Paragraph(
        f"表示层负责与用户的交互，提供直观友好的操作界面；"
        f"业务逻辑层实现系统的核心业务功能，处理各种业务规则和流程；"
        f"数据访问层封装了对数据源的访问操作，提供统一的数据访问接口；"
        f"数据存储层负责数据的持久化存储，保证数据的安全性和完整性。",
        styles['body']
    ))

    story.append(Paragraph("4.2 技术架构", styles['h2']))
    langs = ', '.join(info.get('languages', ['未知']))
    story.append(Paragraph(
        f"{display_name}基于{langs}等技术开发。系统采用成熟的技术栈，"
        f"确保了良好的性能和稳定性。",
        styles['body']
    ))
    if tech_tags:
        story.append(Paragraph(
            f"从技术分类来看，{display_name}属于{'、'.join(tech_tags)}类型软件。"
            f"{tech_features}",
            styles['body']
        ))
    story.append(Paragraph(
        f"在技术选型上，{display_name}充分考虑了技术的成熟度、社区支持、"
        f"性能表现和安全性等因素。采用的技术组件均为经过广泛验证的主流技术，"
        f"具有丰富的文档和社区支持，有利于系统的长期维护和演进。",
        styles['body']
    ))

    story.append(Paragraph("4.3 功能架构", styles['h2']))
    story.append(Paragraph(
        f"{display_name}的功能架构围绕核心业务需求设计，"
        f"将系统功能划分为多个相对独立的功能模块，各模块之间通过定义良好的接口进行协作。"
        f"这种模块化的设计使得系统具有良好的可扩展性，可以根据需要灵活地添加或调整功能模块。",
        styles['body']
    ))
    story.append(Paragraph(
        f"主要功能包括：{main_funcs}",
        styles['body']
    ))

    story.append(Paragraph("4.4 数据架构", styles['h2']))
    story.append(Paragraph(
        f"{display_name}的数据架构设计遵循数据完整性、一致性和安全性原则。"
        f"系统采用结构化数据存储方案，合理设计数据模型和数据库表结构，"
        f"确保数据的高效存取和可靠管理。",
        styles['body']
    ))
    story.append(Paragraph(
        f"数据流转方面，系统遵循统一的数据流转规范：用户操作产生的数据经过表示层收集、"
        f"业务逻辑层验证和处理后，通过数据访问层写入数据存储层。"
        f"数据查询则通过反向流程从存储层获取数据并展示给用户。"
        f"在数据传输过程中，系统采用加密等安全措施保护数据安全。",
        styles['body']
    ))

    story.append(Paragraph("4.5 安全架构", styles['h2']))
    story.append(Paragraph(
        f"{display_name}建立了多层次的安全防护体系，从网络安全、应用安全、数据安全等维度"
        f"提供全方位的安全保障。系统采用身份认证、访问控制、数据加密、安全审计等"
        f"安全机制，确保系统和数据的安全性。",
        styles['body']
    ))
    security_items = [
        "网络层：防火墙策略、端口控制、SSL/TLS加密传输",
        "应用层：身份认证、会话管理、输入验证、防注入攻击",
        "数据层：数据加密存储、访问权限控制、数据备份",
        "审计层：操作日志记录、安全事件监控、异常行为告警",
    ]
    for item in security_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(PageBreak())

    # ======== 第五章 功能详细说明 ========
    story.append(Paragraph("第五章  功能详细说明", styles['h1']))

    story.append(Paragraph("5.1 功能概览", styles['h2']))
    story.append(Paragraph(
        f"{display_name}提供了丰富的功能模块以满足{info.get('domain', '行业')}的业务需求。"
        f"以下是各功能模块的详细说明：",
        styles['body']
    ))
    story.append(Paragraph(f"{main_funcs}", styles['body']))

    # 详细功能模块描述
    if functions_detail:
        section_num = 2
        for mod_name, mod_desc in functions_detail.items():
            story.append(Paragraph(f"5.{section_num} {mod_name}", styles['h2']))
            # 如果描述较短，扩展为多段
            if isinstance(mod_desc, str):
                story.append(Paragraph(f"本模块提供{mod_name}相关功能。{mod_desc}", styles['body']))
                story.append(Paragraph(
                    f"{mod_name}模块是{display_name}的重要组成部分，为用户提供了便捷的操作方式。"
                    f"通过该模块，用户可以高效地完成相关业务操作，提升工作效率。",
                    styles['body']
                ))
                story.append(Paragraph(
                    f"该模块的设计充分考虑了用户体验和业务流程的优化，提供了直观的操作界面和"
                    f"完善的操作提示。同时，模块内置了数据验证和错误处理机制，"
                    f"确保操作的正确性和数据的完整性。",
                    styles['body']
                ))
            elif isinstance(mod_desc, list):
                for item in mod_desc:
                    story.append(Paragraph(f"• {item}", styles['bullet']))
            section_num += 1
    else:
        # 如果没有提供详细功能，根据主要功能文本生成展开描述
        story.append(Paragraph("5.2 核心功能模块", styles['h2']))
        story.append(Paragraph(
            f"{display_name}的核心功能模块涵盖了{info.get('domain', '行业')}的关键业务场景。"
            f"各功能模块设计合理、操作便捷，能够有效支撑用户的日常业务需求。",
            styles['body']
        ))
        story.append(Paragraph(
            f"核心功能模块采用模块化设计，各模块之间松耦合、高内聚。"
            f"用户可以根据实际需求选择使用不同的功能模块，也可以将多个模块组合使用，"
            f"以满足复杂的业务场景需求。",
            styles['body']
        ))
        story.append(Paragraph(
            f"每个功能模块都经过了严格的测试验证，确保功能的正确性和可靠性。"
            f"模块的界面设计遵循一致性原则，降低用户的学习成本。",
            styles['body']
        ))

    story.append(PageBreak())

    # ======== 第六章 操作指南 ========
    story.append(Paragraph("第六章  操作指南", styles['h1']))
    story.append(Paragraph(
        f"本章提供{display_name}的详细操作指南，帮助用户快速掌握软件的使用方法。",
        styles['body']
    ))

    story.append(Paragraph("6.1 系统登录与退出", styles['h2']))
    story.append(Paragraph(
        f"启动{display_name}后，用户需要通过身份验证才能使用系统功能。"
        f"以下是登录和退出的详细操作说明：",
        styles['body']
    ))
    story.append(Paragraph("登录操作：", styles['h3']))
    login_steps = [
        f"打开{display_name}的访问界面",
        "在登录页面输入用户名和密码",
        "点击\"登录\"按钮",
        "系统验证通过后进入主界面",
        "如忘记密码，可点击\"忘记密码\"链接进行密码重置",
    ]
    for i, step in enumerate(login_steps, 1):
        story.append(Paragraph(f"（{i}）{step}", styles['body']))

    story.append(Paragraph("退出操作：", styles['h3']))
    story.append(Paragraph(
        f"点击界面右上角的用户头像或用户名，在下拉菜单中选择\"退出登录\"即可安全退出系统。"
        f"建议在离开工作站时及时退出登录，以保护账号安全。"
        f"系统也设有自动超时退出机制，在用户长时间未操作时会自动退出登录。",
        styles['body']
    ))

    story.append(Paragraph("6.2 界面布局说明", styles['h2']))
    story.append(Paragraph(
        f"{display_name}的界面采用现代化的布局设计，主要分为以下几个区域：",
        styles['body']
    ))
    layout_items = [
        "顶部导航栏：显示系统名称、主要导航菜单、通知消息和用户信息",
        "左侧菜单栏：显示功能模块的树形导航菜单，支持展开和折叠",
        "中间内容区：显示当前选中功能模块的具体内容和操作界面",
        "底部状态栏：显示系统状态信息、版本号和版权信息",
    ]
    for item in layout_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(Paragraph(
        f"界面支持响应式布局，可适应不同分辨率的显示设备。用户可以通过拖拽调整各区域的大小比例，"
        f"以获得最佳的视觉效果和操作体验。",
        styles['body']
    ))

    story.append(Paragraph("6.3 基本操作流程", styles['h2']))
    story.append(Paragraph(
        f"以下是使用{display_name}的基本操作流程：",
        styles['body']
    ))
    basic_ops = [
        ("登录系统", "使用分配的账号和密码登录系统，进入主界面"),
        ("选择功能", "通过左侧菜单或顶部导航选择需要使用的功能模块"),
        ("执行操作", "在内容区域执行相关的业务操作，如数据查询、新增、修改、删除等"),
        ("查看结果", "操作完成后查看执行结果，系统会给出相应的成功或失败提示"),
        ("数据导出", "如需要，可将数据导出为常用格式（如Excel、PDF等）"),
        ("退出系统", "操作完成后安全退出系统"),
    ]
    for title, desc in basic_ops:
        story.append(Paragraph(f"• {title}：{desc}", styles['bullet']))

    story.append(Paragraph("6.4 常用操作说明", styles['h2']))

    story.append(Paragraph("6.4.1 数据查询", styles['h3']))
    story.append(Paragraph(
        f"{display_name}提供了强大的数据查询功能。用户可以通过设置查询条件快速定位所需数据。"
        f"查询功能支持精确查询和模糊查询，可以按多个条件组合查询。"
        f"查询结果以列表形式展示，支持排序、分页和导出操作。",
        styles['body']
    ))

    story.append(Paragraph("6.4.2 数据新增", styles['h3']))
    story.append(Paragraph(
        f"在需要新增数据时，点击\"新增\"或\"添加\"按钮，系统将弹出数据录入表单。"
        f"在表单中填写相关信息后点击\"保存\"按钮即可完成数据新增。"
        f"系统会对必填项和数据格式进行验证，确保数据的完整性和正确性。",
        styles['body']
    ))

    story.append(Paragraph("6.4.3 数据修改", styles['h3']))
    story.append(Paragraph(
        f"选择需要修改的数据记录，点击\"编辑\"按钮进入编辑模式。"
        f"修改相关字段后点击\"保存\"按钮提交修改。"
        f"系统会记录数据的修改历史，方便后续追溯。",
        styles['body']
    ))

    story.append(Paragraph("6.4.4 数据删除", styles['h3']))
    story.append(Paragraph(
        f"选择需要删除的数据记录，点击\"删除\"按钮。系统会弹出确认对话框，"
        f"确认后执行删除操作。为防止误操作，系统支持软删除机制，"
        f"被删除的数据可以在一定期限内恢复。",
        styles['body']
    ))

    story.append(Paragraph("6.5 数据管理操作", styles['h2']))
    story.append(Paragraph(
        f"{display_name}提供了完善的数据管理功能，包括数据导入导出、批量操作和数据统计等。",
        styles['body']
    ))
    story.append(Paragraph("6.5.1 数据导入", styles['h3']))
    story.append(Paragraph(
        f"系统支持从Excel、CSV等格式的文件中批量导入数据。点击\"导入\"按钮，"
        f"选择要导入的文件，系统会自动解析文件内容并显示预览。"
        f"确认数据无误后点击\"确定\"按钮完成导入。导入过程中系统会进行数据验证，"
        f"对不符合要求的数据会标注错误原因。",
        styles['body']
    ))
    story.append(Paragraph("6.5.2 数据导出", styles['h3']))
    story.append(Paragraph(
        f"系统支持将数据导出为Excel、PDF、CSV等多种格式。"
        f"在数据列表页面点击\"导出\"按钮，选择导出格式和范围（当前页或全部数据），"
        f"即可将数据导出到本地文件。",
        styles['body']
    ))
    story.append(Paragraph("6.5.3 批量操作", styles['h3']))
    story.append(Paragraph(
        f"对于需要对多条数据进行相同操作的场景，{display_name}提供了批量操作功能。"
        f"用户可以通过复选框选择多条记录，然后执行批量修改、批量删除等操作，"
        f"提高工作效率。",
        styles['body']
    ))

    story.append(Paragraph("6.6 高级操作", styles['h2']))
    story.append(Paragraph(
        f"除基本操作外，{display_name}还提供了一些高级功能以满足专业用户的需求。",
        styles['body']
    ))
    advanced_items = [
        "自定义报表：支持用户自定义数据报表的样式和内容",
        "数据分析：提供数据可视化分析功能，支持图表展示",
        "工作流自动化：支持配置自动化的业务流程和规则",
        "快捷键操作：支持常用操作的键盘快捷键，提升操作效率",
        "个性化设置：支持用户自定义界面主题、布局和偏好设置",
    ]
    for item in advanced_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(PageBreak())

    # ======== 第七章 系统管理 ========
    story.append(Paragraph("第七章  系统管理", styles['h1']))
    story.append(Paragraph(
        f"本章介绍{display_name}的系统管理功能，主要面向系统管理员。"
        f"系统管理功能用于管理用户、权限、系统配置和运维等方面的工作。",
        styles['body']
    ))

    story.append(Paragraph("7.1 用户管理", styles['h2']))
    story.append(Paragraph(
        f"用户管理模块用于管理系统的用户账号。管理员可以进行以下操作：",
        styles['body']
    ))
    user_mgmt = [
        "创建用户：填写用户基本信息（用户名、姓名、邮箱、手机号等）创建新用户账号",
        "编辑用户：修改用户的基本信息和状态",
        "禁用/启用用户：临时禁止或恢复用户的登录权限",
        "删除用户：永久删除不再需要的用户账号",
        "重置密码：为用户重置登录密码",
        "批量导入：通过Excel文件批量创建用户账号",
    ]
    for item in user_mgmt:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(Paragraph(
        f"建议管理员定期审查用户列表，及时清理不活跃的账号，确保系统安全。"
        f"对于离职或转岗的人员，应及时禁用或删除其系统账号。",
        styles['body']
    ))

    story.append(Paragraph("7.2 权限管理", styles['h2']))
    story.append(Paragraph(
        f"{display_name}采用基于角色的访问控制（RBAC）模型进行权限管理。"
        f"系统预置了多种角色，如系统管理员、普通用户、审核员等，"
        f"管理员也可以根据业务需要自定义角色。",
        styles['body']
    ))
    story.append(Paragraph(
        f"权限管理的核心概念包括：",
        styles['body']
    ))
    perm_items = [
        "角色：一组权限的集合，代表某种业务职责",
        "权限：对特定功能或数据的访问许可",
        "用户-角色关联：将角色分配给用户，用户获得角色对应的权限",
        "数据权限：控制用户可以访问的数据范围",
    ]
    for item in perm_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(Paragraph(
        f"管理员在分配权限时应遵循最小权限原则，即仅授予用户完成工作所需的最小权限集。"
        f"这有助于降低安全风险，防止权限滥用。",
        styles['body']
    ))

    story.append(Paragraph("7.3 系统配置", styles['h2']))
    story.append(Paragraph(
        f"系统配置模块允许管理员对{display_name}的全局参数进行配置。"
        f"主要配置项包括：",
        styles['body']
    ))
    config_items = [
        "基本设置：系统名称、Logo、版权信息等",
        "安全设置：密码策略、登录限制、会话超时时间等",
        "通知设置：邮件通知、短信通知、站内消息等",
        "存储设置：文件存储路径、上传文件大小限制等",
        "缓存设置：缓存策略、缓存有效期等",
        "接口设置：第三方接口参数配置",
    ]
    for item in config_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))

    story.append(Paragraph("7.4 日志管理", styles['h2']))
    story.append(Paragraph(
        f"{display_name}提供完善的日志管理功能，记录系统运行过程中的各类事件，"
        f"便于问题排查和安全审计。系统日志分为以下类别：",
        styles['body']
    ))
    log_items = [
        "操作日志：记录用户的操作行为，包括操作时间、操作人、操作内容等",
        "登录日志：记录用户的登录和退出信息，包括登录时间、IP地址等",
        "系统日志：记录系统运行状态和异常信息",
        "安全日志：记录安全相关的事件，如密码修改、权限变更等",
    ]
    for item in log_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(Paragraph(
        f"管理员可以通过日志管理界面查询和导出日志信息。建议定期查看安全日志和异常日志，"
        f"及时发现和处理潜在的安全威胁。日志数据会按照配置的保留策略自动归档和清理。",
        styles['body']
    ))

    story.append(Paragraph("7.5 数据备份与恢复", styles['h2']))
    story.append(Paragraph(
        f"数据备份是保障系统安全的重要措施。{display_name}提供了以下备份功能：",
        styles['body']
    ))
    backup_items = [
        "手动备份：管理员可以手动触发数据备份操作",
        "定时备份：支持配置定时备份计划，按照设定的时间自动执行备份",
        "增量备份：支持增量备份模式，减少备份时间和存储空间",
        "备份恢复：在数据丢失或损坏时，可以使用备份文件恢复数据",
        "备份管理：查看备份历史记录，管理备份文件",
    ]
    for item in backup_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))
    story.append(Paragraph(
        f"建议制定合理的备份策略，定期执行数据备份，并将备份文件存储在与生产环境隔离的安全位置。"
        f"同时建议定期进行备份恢复演练，验证备份文件的可用性。",
        styles['body']
    ))
    story.append(PageBreak())

    # ======== 第八章 接口说明 ========
    story.append(Paragraph("第八章  接口说明", styles['h1']))

    story.append(Paragraph("8.1 接口概述", styles['h2']))
    story.append(Paragraph(
        f"{display_name}提供了标准化的接口规范，支持与其他系统进行数据交互和功能集成。"
        f"系统接口遵循RESTful架构风格，使用JSON作为数据交换格式，"
        f"支持HTTP/HTTPS协议通信。",
        styles['body']
    ))
    story.append(Paragraph(
        f"通过接口，第三方系统可以实现与{display_name}的数据同步、功能调用和业务协同。"
        f"接口的设计遵循高内聚、低耦合的原则，确保接口的稳定性和可维护性。",
        styles['body']
    ))

    story.append(Paragraph("8.2 接口规范", styles['h2']))
    story.append(Paragraph(
        f"系统接口遵循以下规范：",
        styles['body']
    ))
    api_specs = [
        "协议：支持HTTP和HTTPS协议，生产环境建议使用HTTPS",
        "数据格式：请求和响应数据统一使用JSON格式",
        "字符编码：统一使用UTF-8字符编码",
        "认证方式：支持Token认证和OAuth2.0认证",
        "版本控制：通过URL路径进行接口版本管理",
        "错误处理：统一的错误码和错误消息规范",
        "限流策略：防止接口被过度调用的限流保护机制",
    ]
    for item in api_specs:
        story.append(Paragraph(f"• {item}", styles['bullet']))

    story.append(Paragraph("8.3 接口安全", styles['h2']))
    story.append(Paragraph(
        f"系统接口安全措施包括：身份认证机制确保调用方的合法性；"
        f"数据传输加密保护数据在传输过程中的安全；"
        f"参数签名验证防止数据被篡改；"
        f"IP白名单控制接口的访问来源；"
        f"调用频率限制防止接口被恶意调用。"
        f"所有接口调用都会被记录到日志中，便于安全审计和问题追踪。",
        styles['body']
    ))
    story.append(PageBreak())

    # ======== 第九章 安全说明 ========
    story.append(Paragraph("第九章  安全说明", styles['h1']))

    story.append(Paragraph("9.1 安全机制概述", styles['h2']))
    story.append(Paragraph(
        f"{display_name}建立了完善的安全防护体系，从多个维度保障系统和数据的安全性。"
        f"安全机制覆盖了身份认证、访问控制、数据保护和安全审计等方面。",
        styles['body']
    ))

    story.append(Paragraph("9.2 身份认证", styles['h2']))
    story.append(Paragraph(
        f"系统采用严格的身份认证机制，确保只有合法用户才能访问系统。"
        f"主要认证措施包括：",
        styles['body']
    ))
    auth_items = [
        "用户名密码认证：基本的身份验证方式",
        "密码强度要求：密码需满足长度和复杂度要求",
        "登录失败锁定：连续多次登录失败将临时锁定账号",
        "密码定期更换：建议用户定期更换密码",
        "会话管理：自动超时退出，防止未授权访问",
    ]
    for item in auth_items:
        story.append(Paragraph(f"• {item}", styles['bullet']))

    story.append(Paragraph("9.3 访问控制", styles['h2']))
    story.append(Paragraph(
        f"系统实现了精细化的访问控制策略。基于RBAC模型的权限管理确保用户只能访问被授权的功能和数据。"
        f"管理员可以灵活配置角色和权限，实现细粒度的访问控制。"
        f"系统还支持数据级别的权限控制，确保用户只能查看和操作其权限范围内的数据。",
        styles['body']
    ))

    story.append(Paragraph("9.4 数据安全", styles['h2']))
    story.append(Paragraph(
        f"{display_name}对数据安全的保护体现在以下几个方面：",
        styles['body']
    ))
    data_sec = [
        "数据传输加密：使用SSL/TLS协议加密数据传输",
        "敏感数据加密存储：密码等敏感信息使用不可逆加密算法存储",
        "数据完整性校验：通过数据校验机制确保数据不被篡改",
        "数据备份：定期备份数据，防止数据丢失",
        "数据脱敏：对敏感数据进行脱敏处理后展示",
    ]
    for item in data_sec:
        story.append(Paragraph(f"• {item}", styles['bullet']))

    story.append(Paragraph("9.5 安全审计", styles['h2']))
    story.append(Paragraph(
        f"系统记录所有重要操作的审计日志，包括登录登出、数据变更、权限修改、"
        f"系统配置变更等关键操作。审计日志不可被修改和删除，确保审计记录的真实性和完整性。"
        f"管理员可以通过审计报表功能查看和分析系统的安全状况，及时发现和处理安全隐患。",
        styles['body']
    ))
    story.append(PageBreak())

    # ======== 第十章 常见问题 ========
    story.append(Paragraph("第十章  常见问题与解决方案", styles['h1']))

    story.append(Paragraph("10.1 安装常见问题", styles['h2']))
    install_faqs = [
        ("安装过程中提示权限不足", "请确保使用管理员权限运行安装程序。在Windows系统中右键选择\"以管理员身份运行\"，在Linux系统中使用sudo命令。"),
        ("安装过程中提示端口被占用", "请检查目标端口是否被其他程序占用，可以修改配置文件中的端口号或停止占用端口的程序。"),
        ("安装后无法启动服务", "请检查运行环境是否满足要求，查看错误日志文件获取详细的错误信息。确认所有依赖服务（如数据库）已正常启动。"),
        ("数据库初始化失败", "请确认数据库服务已启动，数据库连接参数配置正确，且数据库用户具有足够的权限。"),
    ]
    for q, a in install_faqs:
        story.append(Paragraph(f"问题：{q}", styles['h3']))
        story.append(Paragraph(f"解决方案：{a}", styles['body']))

    story.append(Paragraph("10.2 使用常见问题", styles['h2']))
    use_faqs = [
        ("登录时提示用户名或密码错误", "请确认输入的用户名和密码正确，注意区分大小写。如多次尝试仍无法登录，请联系管理员重置密码。"),
        ("页面加载缓慢", "请检查网络连接是否正常，清除浏览器缓存后重试。如问题持续，请联系系统管理员检查服务器状态。"),
        ("数据导出失败", "请检查导出的数据量是否过大，尝试缩小查询范围后重新导出。同时检查磁盘空间是否充足。"),
        ("上传文件失败", "请检查文件大小是否超过系统限制，文件格式是否在允许列表中。如需调整上传限制，请联系管理员修改系统配置。"),
        ("操作提示无权限", "请确认当前用户是否具有执行该操作所需的权限。如需要额外权限，请联系系统管理员进行授权。"),
    ]
    for q, a in use_faqs:
        story.append(Paragraph(f"问题：{q}", styles['h3']))
        story.append(Paragraph(f"解决方案：{a}", styles['body']))

    story.append(Paragraph("10.3 性能优化建议", styles['h2']))
    perf_tips = [
        "定期清理系统缓存和临时文件，释放存储空间",
        "优化数据库索引，提高数据查询效率",
        "合理配置系统资源（内存、CPU、连接池等）",
        "对大数据量的查询操作使用分页加载",
        "定期归档历史数据，减少在线数据量",
        "使用CDN加速静态资源的访问",
        "开启GZIP压缩，减少网络传输数据量",
    ]
    for tip in perf_tips:
        story.append(Paragraph(f"• {tip}", styles['bullet']))

    story.append(Paragraph("10.4 错误代码说明", styles['h2']))
    error_codes = [
        ("400", "请求参数错误", "检查请求参数是否正确"),
        ("401", "未授权访问", "请重新登录或检查认证信息"),
        ("403", "权限不足", "联系管理员授权"),
        ("404", "资源未找到", "检查请求地址是否正确"),
        ("500", "服务器内部错误", "联系管理员查看服务器日志"),
        ("502", "网关错误", "检查后端服务是否正常运行"),
        ("503", "服务不可用", "服务可能正在重启，请稍后重试"),
    ]
    err_table_data = [
        [Paragraph("错误代码", styles['table_header']),
         Paragraph("含义", styles['table_header']),
         Paragraph("处理建议", styles['table_header'])]
    ]
    for code, meaning, solution in error_codes:
        err_table_data.append([
            Paragraph(code, styles['table_cell']),
            Paragraph(meaning, styles['table_cell']),
            Paragraph(solution, styles['table_cell']),
        ])
    err_table = Table(err_table_data, colWidths=[80, 150, 280])
    err_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F0F0F0')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(err_table)
    story.append(PageBreak())

    # ======== 附录 ========
    story.append(Paragraph("附录A  术语表", styles['h1']))
    terms = [
        ("RBAC", "基于角色的访问控制（Role-Based Access Control），一种通过角色来管理权限的模型"),
        ("API", "应用程序编程接口（Application Programming Interface），用于不同系统之间的数据交互"),
        ("JSON", "JavaScript对象表示法（JavaScript Object Notation），轻量级的数据交换格式"),
        ("RESTful", "表述性状态传递（Representational State Transfer），一种Web服务的架构风格"),
        ("SSL/TLS", "安全套接层/传输层安全协议，用于网络数据传输加密"),
        ("HTTPS", "超文本传输安全协议，HTTP协议的安全版本"),
        ("OAuth", "开放授权协议，用于第三方应用的授权认证"),
        ("Token", "令牌，用于身份认证的凭证信息"),
        ("CDN", "内容分发网络（Content Delivery Network），加速静态资源访问"),
        ("GZIP", "一种文件压缩算法，用于减少网络传输数据量"),
    ]
    for term, desc in terms:
        story.append(Paragraph(f"<b>{term}</b>：{desc}", styles['body_no_indent']))

    story.append(PageBreak())
    story.append(Paragraph("附录B  技术规格", styles['h1']))
    specs = [
        ("软件名称", name),
        ("版本号", ver),
        ("软件分类", info.get('category', '')),
        ("编程语言", ', '.join(info.get('languages', []))),
        ("源程序量", f"{info.get('source_lines', '')} 行"),
        ("运行操作系统", info.get('run_os', '')),
        ("运行支撑环境", info.get('run_support', '')),
        ("运行硬件环境", info.get('run_hardware', '')),
        ("开发操作系统", info.get('dev_os', '')),
        ("开发工具", info.get('dev_tools', '')),
        ("开发硬件环境", info.get('dev_hardware', '')),
    ]
    spec_table_data = [
        [Paragraph("项目", styles['table_header']),
         Paragraph("内容", styles['table_header'])]
    ]
    for label, value in specs:
        spec_table_data.append([
            Paragraph(label, styles['table_cell']),
            Paragraph(str(value), styles['table_cell']),
        ])
    spec_table = Table(spec_table_data, colWidths=[150, 360])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F0F0F0')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(spec_table)

    story.append(PageBreak())
    story.append(Paragraph("附录C  更新日志", styles['h1']))
    story.append(Paragraph(
        f"以下是{name}的版本更新记录：",
        styles['body']
    ))
    log_table_data = [
        [Paragraph("版本", styles['table_header']),
         Paragraph("日期", styles['table_header']),
         Paragraph("更新内容", styles['table_header'])]
    ]
    log_table_data.append([
        Paragraph(ver, styles['table_cell']),
        Paragraph(datetime.now().strftime('%Y-%m-%d'), styles['table_cell']),
        Paragraph(f"初始版本发布，包含{display_name}的全部核心功能", styles['table_cell']),
    ])
    log_table = Table(log_table_data, colWidths=[80, 120, 310])
    log_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F0F0F0')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(log_table)

    return story


# ============================================================
# 从已有文档转换
# ============================================================
def convert_text_to_pdf(input_path, output_path, software_name, version, author,
                        cn_font, cn_bold_font):
    """将纯文本文档转换为PDF。"""
    styles = create_styles(cn_font, cn_bold_font)

    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']
    content = None
    for enc in encodings:
        try:
            with open(input_path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue

    if content is None:
        print(f"错误：无法读取文件 {input_path}")
        sys.exit(1)

    doc = DocTemplate(
        str(output_path), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 5 * mm, bottomMargin=MARGIN,
        software_name=software_name, version=version,
        copyright_holder=author, cn_font=cn_font
    )

    story = []
    for line in content.split('\n'):
        line = line.rstrip()
        if line.startswith('# '):
            story.append(Paragraph(line[2:], styles['h1']))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], styles['h2']))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['h3']))
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph(f"• {line[2:]}", styles['bullet']))
        elif line.strip() == '':
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(line, styles['body']))

    doc.build(story)


# ============================================================
# 主函数
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='软著文档鉴别材料PDF生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 从JSON配置生成用户手册
  python generate_doc_pdf.py --config software_info.json

  # 从已有文档转换
  python generate_doc_pdf.py --input manual.txt --name "智慧管理系统" --version "V1.0" --author "XX公司"

JSON配置文件格式见 references/fields.md 中的字段说明。
        """
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--config', '-c', help='软件信息JSON配置文件路径')
    group.add_argument('--input', '-i', help='已有文档文件路径（纯文本格式）')

    parser.add_argument('--name', '-n', help='软件全称（--input模式必填）')
    parser.add_argument('--version', '-v', help='版本号（--input模式必填）')
    parser.add_argument('--author', '-a', help='著作权人（--input模式必填）')
    parser.add_argument('--output', '-o', default=None, help='输出PDF路径')

    args = parser.parse_args()

    # 设置字体
    cn_font, cn_bold_font = setup_fonts()

    if args.input:
        # 从已有文档转换模式
        if not args.name or not args.version or not args.author:
            print("错误：--input 模式需要同时提供 --name、--version 和 --author")
            sys.exit(1)

        if not os.path.isfile(args.input):
            print(f"错误：文件不存在: {args.input}")
            sys.exit(1)

        output_path = args.output or f"{re.sub(r'[^\\w\\u4e00-\\u9fff]', '_', args.name)}_文档鉴别材料.pdf"
        print(f"正在转换文档: {args.input}")
        convert_text_to_pdf(args.input, output_path, args.name, args.version,
                            args.author, cn_font, cn_bold_font)
        print(f"生成完成！输出文件: {output_path}")
    else:
        # 从JSON配置生成模式
        if not os.path.isfile(args.config):
            print(f"错误：配置文件不存在: {args.config}")
            sys.exit(1)

        with open(args.config, 'r', encoding='utf-8') as f:
            info = json.load(f)

        software_name = info.get('software_name', '软件')
        version = info.get('version', 'V1.0')
        author = info.get('author', '')

        output_path = args.output or f"{re.sub(r'[^\\w\\u4e00-\\u9fff]', '_', software_name)}_文档鉴别材料.pdf"

        styles = create_styles(cn_font, cn_bold_font)

        doc = DocTemplate(
            str(output_path), pagesize=A4,
            leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=MARGIN + 5 * mm, bottomMargin=MARGIN,
            software_name=software_name, version=version,
            copyright_holder=author, cn_font=cn_font
        )

        print(f"正在生成用户手册: {output_path}")
        story = generate_manual_content(info, styles)
        doc.build(story)

        # 检查页数
        try:
            import fitz  # PyMuPDF
            pdf_doc = fitz.open(str(output_path))
            page_count = len(pdf_doc)
            pdf_doc.close()
            print(f"生成完成！")
            print(f"  输出文件: {output_path}")
            print(f"  总页数: {page_count}")
            if page_count < MIN_PAGES:
                print(f"  ⚠️ 警告：文档页数({page_count})不足{MIN_PAGES}页，建议补充更多内容")
        except ImportError:
            print(f"生成完成！输出文件: {output_path}")
            print(f"  提示：安装 PyMuPDF (pip install pymupdf) 可自动检查页数")


if __name__ == '__main__':
    main()
