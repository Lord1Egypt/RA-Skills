# -*- coding: utf-8 -*-
"""
Report-gama — PDF导出模块
使用 ReportLab 将 Markdown 报告转换为专业 PDF
"""

import os
import re
import logging
import tempfile
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, Image, HRFlowable,
        KeepTogether, ListFlowable, ListItem
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

from config import OUTPUT_DIR, LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Windows 中文字体路径
CHINESE_FONTS = [
    'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/msyh.ttc',
]
FONT_REGISTERED = False

def register_fonts():
    """注册中文字体"""
    global FONT_REGISTERED
    if FONT_REGISTERED:
        return

    for font_path in CHINESE_FONTS:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                FONT_REGISTERED = True
                logger.info(f"注册字体: {font_path}")
                return
            except Exception as e:
                logger.warning(f"注册字体失败: {font_path} - {e}")

    logger.warning("未找到中文字体，PDF中文可能无法正常显示")


class PDFExporter:
    """Markdown → PDF 导出器"""

    def __init__(self, output_dir=None):
        self.output_dir = output_dir or OUTPUT_DIR
        self.styles = None
        self.elements = []
        self.current_font = "ChineseFont" if FONT_REGISTERED else "Helvetica"
        register_fonts()

    def _init_styles(self):
        """初始化样式"""
        if self.styles is not None:
            return

        base = getSampleStyleSheet()
        self.styles = {
            "title": ParagraphStyle(
                "ReportTitle",
                parent=base["Title"],
                fontName=self.current_font,
                fontSize=24,
                textColor=colors.HexColor("#1a3c6e"),
                spaceAfter=12,
                alignment=TA_CENTER,
                leading=30,
            ),
            "subtitle": ParagraphStyle(
                "ReportSubtitle",
                parent=base["Normal"],
                fontName=self.current_font,
                fontSize=14,
                textColor=colors.HexColor("#4a6fa5"),
                spaceAfter=8,
                alignment=TA_CENTER,
            ),
            "cover_meta": ParagraphStyle(
                "CoverMeta",
                parent=base["Normal"],
                fontName=self.current_font,
                fontSize=10,
                textColor=colors.HexColor("#666666"),
                spaceAfter=4,
                alignment=TA_CENTER,
            ),
            "h1": ParagraphStyle(
                "H1",
                parent=base["Heading1"],
                fontName=self.current_font,
                fontSize=18,
                textColor=colors.HexColor("#1a3c6e"),
                spaceBefore=24,
                spaceAfter=12,
                leading=22,
                borderPad=0,
            ),
            "h2": ParagraphStyle(
                "H2",
                parent=base["Heading2"],
                fontName=self.current_font,
                fontSize=14,
                textColor=colors.HexColor("#2e6da4"),
                spaceBefore=18,
                spaceAfter=8,
                leading=18,
            ),
            "h3": ParagraphStyle(
                "H3",
                parent=base["Heading3"],
                fontName=self.current_font,
                fontSize=12,
                textColor=colors.HexColor("#4a6fa5"),
                spaceBefore=12,
                spaceAfter=6,
                leading=16,
            ),
            "body": ParagraphStyle(
                "Body",
                parent=base["Normal"],
                fontName=self.current_font,
                fontSize=10,
                textColor=colors.HexColor("#333333"),
                spaceAfter=6,
                leading=15,
                alignment=TA_JUSTIFY,
            ),
            "body_bold": ParagraphStyle(
                "BodyBold",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                textColor=colors.HexColor("#333333"),
                spaceAfter=4,
                leading=15,
            ),
            "table_header": ParagraphStyle(
                "TableHeader",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=9,
                textColor=colors.white,
                alignment=TA_CENTER,
            ),
            "table_cell": ParagraphStyle(
                "TableCell",
                parent=base["Normal"],
                fontName=self.current_font,
                fontSize=8,
                textColor=colors.HexColor("#333333"),
                leading=12,
                alignment=TA_LEFT,
            ),
            "blockquote": ParagraphStyle(
                "Blockquote",
                parent=base["Normal"],
                fontName="Helvetica-Oblique",
                fontSize=10,
                textColor=colors.HexColor("#555555"),
                leftIndent=20,
                rightIndent=20,
                spaceAfter=8,
                leading=14,
            ),
            "toc": ParagraphStyle(
                "TOC",
                parent=base["Normal"],
                fontName=self.current_font,
                fontSize=11,
                textColor=colors.HexColor("#333333"),
                spaceAfter=6,
                leading=16,
            ),
            "page_number": ParagraphStyle(
                "PageNumber",
                parent=base["Normal"],
                fontName=self.current_font,
                fontSize=9,
                textColor=colors.HexColor("#888888"),
                alignment=TA_CENTER,
            ),
        }

    def _is_chinese_text(self, text):
        """判断文本是否包含中文"""
        return bool(re.search(r'[\u4e00-\u9fff]', text))

    def _parse_markdown(self, md_content):
        """将 Markdown 内容解析为 PDF elements"""
        self._init_styles()
        elements = []

        lines = md_content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # 跳过水平线/分隔线
            if re.match(r'^---+$', line.strip()) or re.match(r'^---+', line):
                elements.append(HRFlowable(
                    width="100%", thickness=1,
                    color=colors.HexColor("#cccccc"),
                    spaceAfter=8, spaceBefore=8
                ))
                i += 1
                continue

            # 封面标题处理（首个 # 且包含报告标题）
            if line.startswith('# ') and not any(h.startswith('# ') for h in lines[:i] if h.strip()):
                title = line[2:].strip()
                elements.append(Spacer(1, 3*cm))
                elements.append(Paragraph(title, self.styles["title"]))
                i += 1
                continue

            # H1 标题
            if line.startswith('## '):
                title = line[3:].strip()
                # 移除 emoji 前缀
                title_clean = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title)
                elements.append(Spacer(1, 0.3*cm))
                elements.append(Paragraph(title_clean, self.styles["h1"]))
                elements.append(HRFlowable(
                    width="100%", thickness=2,
                    color=colors.HexColor("#1a3c6e"),
                    spaceAfter=8
                ))
                i += 1
                continue

            # H2 标题
            if line.startswith('### '):
                title = line[4:].strip()
                title_clean = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title)
                elements.append(Spacer(1, 0.2*cm))
                elements.append(Paragraph(title_clean, self.styles["h2"]))
                i += 1
                continue

            # H3 标题
            if line.startswith('#### '):
                title = line[5:].strip()
                title_clean = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title)
                elements.append(Paragraph(title_clean, self.styles["h3"]))
                i += 1
                continue

            # 表格处理
            if line.startswith('|') and '|' in line:
                table_data = []
                header_row = []
                table_started = False
                col_count = 0

                while i < len(lines) and lines[i].startswith('|'):
                    row_text = lines[i].strip()
                    # 跳过 Markdown 表格分隔行
                    if re.match(r'^\|[-:\s|]+\|$', row_text):
                        i += 1
                        continue

                    # 解析单元格
                    cells = [c.strip() for c in row_text.strip('|').split('|')]
                    if not table_started:
                        col_count = len(cells)
                        table_started = True
                        header_row = cells
                    else:
                        table_data.append(cells)

                    i += 1

                if table_data and header_row:
                    try:
                        # 构建表格数据
                        all_rows = [header_row] + table_data

                        # 设置列宽
                        col_widths = []
                        available_width = 17 * cm  # A4 有效宽度
                        per_col = available_width / len(header_row)
                        col_widths = [per_col] * len(header_row)

                        # 创建表格
                        tbl = Table(all_rows, colWidths=col_widths, repeatRows=1)

                        # 样式
                        style = [
                            # 表头
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a3c6e")),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 9),
                            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                            ('TOPPADDING', (0, 0), (-1, 0), 8),
                            # 表格内容
                            ('FONTNAME', (0, 1), (-1, -1), self.current_font),
                            ('FONTSIZE', (0, 1), (-1, -1), 8),
                            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
                            ('TOPPADDING', (0, 1), (-1, -1), 5),
                            ('LEFTPADDING', (0, 0), (-1, -1), 6),
                            # 边框
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                             [colors.white, colors.HexColor("#f5f8fa")]),
                        ]

                        tbl.setStyle(TableStyle(style))
                        elements.append(Spacer(1, 0.2*cm))
                        elements.append(tbl)
                        elements.append(Spacer(1, 0.2*cm))
                    except Exception as e:
                        logger.warning(f"表格渲染失败: {e}")
                continue

            # 图片处理
            if line.startswith('![') and '](' in line:
                match = re.search(r'!\[.*?\]\((.*?)\)', line)
                if match:
                    img_path = match.group(1)
                    if os.path.exists(img_path):
                        try:
                            img = Image(img_path)
                            # 按比例缩放
                            img_width = 15 * cm
                            aspect = img.imageHeight / img.imageWidth
                            img_height = img_width * aspect
                            if img_height > 10 * cm:
                                img_height = 10 * cm
                                img_width = img_height / aspect
                            img.drawWidth = img_width
                            img.drawHeight = img_height
                            elements.append(Spacer(1, 0.2*cm))
                            elements.append(img)
                            elements.append(Spacer(1, 0.2*cm))
                        except Exception as e:
                            logger.warning(f"图片插入失败: {img_path} - {e}")
                i += 1
                continue

            # 引用块（> 开头）
            if line.startswith('>'):
                quote_lines = []
                while i < len(lines) and lines[i].startswith('>'):
                    quote_lines.append(lines[i][1:].strip())
                    i += 1
                quote_text = ' '.join(quote_lines)
                # 移除 Markdown 格式
                quote_text = re.sub(r'\*\*(.*?)\*\*', r'\1', quote_text)
                quote_text = re.sub(r'\*(.*?)\*', r'\1', quote_text)
                quote_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', quote_text)
                elements.append(Paragraph(quote_text, self.styles["blockquote"]))
                elements.append(Spacer(1, 0.1*cm))
                continue

            # 列表项
            if re.match(r'^[-*]\s', line) or re.match(r'^\d+\.\s', line):
                list_items = []
                while i < len(lines) and (re.match(r'^[-*]\s', lines[i]) or re.match(r'^\d+\.\s', lines[i])):
                    item_text = lines[i].strip()
                    # 移除列表标记
                    item_text = re.sub(r'^[-*]\s+', '', item_text)
                    item_text = re.sub(r'^\d+\.\s+', '', item_text)
                    # 移除 Markdown 格式
                    item_text = re.sub(r'\*\*(.*?)\*\*', r'\1', item_text)
                    item_text = re.sub(r'\*(.*?)\*', r'\1', item_text)
                    list_items.append(Paragraph(item_text, self.styles["body"]))
                    i += 1

                if list_items:
                    elements.extend(list_items)
                    elements.append(Spacer(1, 0.1*cm))
                continue

            # 普通段落
            if line.strip():
                # 移除 Markdown 格式
                text = line
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
                # 清理剩余的标记
                text = re.sub(r'[*_`#>]+', '', text)
                text = text.strip()

                if text:
                    elements.append(Paragraph(text, self.styles["body"]))

            i += 1

        return elements

    def _on_page(self, canvas, doc):
        """页面装饰（页眉、页脚）"""
        canvas.saveState()
        width, height = A4

        # 页眉
        canvas.setFont(self.current_font if FONT_REGISTERED else "Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawString(2*cm, height - 1.2*cm, f"Report-gama | 市场调研报告")
        canvas.drawRightString(width - 2*cm, height - 1.2*cm,
                               f"{datetime.now().strftime('%Y-%m-%d')}")

        # 页脚线
        canvas.setStrokeColor(colors.HexColor("#cccccc"))
        canvas.line(2*cm, 1.5*cm, width - 2*cm, 1.5*cm)

        # 页码
        canvas.setFont(self.current_font if FONT_REGISTERED else "Helvetica", 9)
        canvas.drawCentredString(width / 2, 1*cm, f"— {doc.page} —")

        canvas.restoreState()

    def markdown_to_pdf(self, md_path, pdf_path=None):
        """
        将 Markdown 文件转换为 PDF

        Args:
            md_path: Markdown 文件路径
            pdf_path: 输出 PDF 路径（可选）

        Returns:
            str: PDF 文件路径
        """
        if not HAS_REPORTLAB:
            raise RuntimeError(
                "请先安装 reportlab: pip3 install reportlab\n"
                "PDF导出需要此库"
            )

        if not os.path.exists(md_path):
            raise FileNotFoundError(f"Markdown 文件不存在: {md_path}")

        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        # 生成输出路径
        if pdf_path is None:
            md_basename = os.path.splitext(os.path.basename(md_path))[0]
            pdf_path = os.path.join(self.output_dir, f"{md_basename}.pdf")

        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # 解析 Markdown
        elements = self._parse_markdown(md_content)

        # 创建 PDF
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm,
            title="市场调研报告",
            author="Report-gama",
            subject="市场调研报告",
        )

        doc.build(elements, onFirstPage=self._on_page, onLaterPages=self._on_page)
        logger.info(f"PDF 已生成: {pdf_path}")
        return pdf_path

    def markdown_str_to_pdf(self, md_content, pdf_path=None):
        """
        将 Markdown 字符串直接转换为 PDF

        Args:
            md_content: Markdown 内容字符串
            pdf_path: 输出 PDF 路径

        Returns:
            str: PDF 文件路径
        """
        if not HAS_REPORTLAB:
            raise RuntimeError("请先安装 reportlab: pip3 install reportlab")

        if pdf_path is None:
            pdf_path = os.path.join(
                self.output_dir,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )

        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        elements = self._parse_markdown(md_content)

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm,
            title="市场调研报告",
            author="Report-gama",
        )

        doc.build(elements, onFirstPage=self._on_page, onLaterPages=self._on_page)
        logger.info(f"PDF 已生成: {pdf_path}")
        return pdf_path


def quick_export(md_path, pdf_path=None):
    """快捷导出函数"""
    exporter = PDFExporter()
    return exporter.markdown_to_pdf(md_path, pdf_path)


if __name__ == "__main__":
    # 测试
    test_md = """# 俄罗斯血糖检测设备市场调研报告

## 执行摘要

这是一份测试报告。

## 一、行业概述

### 近30天行业重大事件

- **事件1**：Росздравнадзор обновил список требований
- **事件2**： рынок медицинского оборудования вырос

## 二、市场数据

| 指标 | 数值 |
|------|------|
| TAM | $1.2B |
| SAM | $300M |
| SOM | $50M |

![价格分布]()

"""
    exporter = PDFExporter()
    try:
        pdf_path = exporter.markdown_str_to_pdf(test_md, "test_report.pdf")
        print(f"PDF 生成成功: {pdf_path}")
    except Exception as e:
        print(f"PDF 生成失败（缺少 reportlab）: {e}")
        print("请运行: pip3 install reportlab")
