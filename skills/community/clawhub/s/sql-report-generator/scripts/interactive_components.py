"""
sql-report-generator: 报告生成与交互组件
支持表格、矩阵、切片器、交互导航、分页报表等
"""

import base64
import io
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import seaborn as sns

# ============================================================================
# 表格与矩阵类
# ============================================================================

class TableChart:
    """表格 - 明细数据展示"""
    
    def __init__(self, width: int = 1200, height: int = 600, dpi: int = 100):
        self.width = width
        self.height = height
        self.dpi = dpi
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'columns': ['订单ID', '客户', '金额', '日期'],
            'rows': [
                ['ORD001', '张三', '¥1,000', '2026-03-26'],
                ['ORD002', '李四', '¥2,500', '2026-03-25'],
                ...
            ],
            'title': '订单列表'
        }
        """
        fig, ax = plt.subplots(figsize=(self.width/100, self.height/100), dpi=self.dpi)
        ax.axis('tight')
        ax.axis('off')
        
        # 创建表格
        table = ax.table(
            cellText=data['rows'],
            colLabels=data['columns'],
            cellLoc='center',
            loc='center',
            colWidths=[0.2] * len(data['columns'])
        )
        
        # 设置样式
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # 头部样式
        for i in range(len(data['columns'])):
            table[(0, i)].set_facecolor('#0078D4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # 行样式（交替颜色）
        for i in range(1, len(data['rows']) + 1):
            for j in range(len(data['columns'])):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#F5F5F5')
                else:
                    table[(i, j)].set_facecolor('white')
        
        # 标题
        if 'title' in data:
            fig.suptitle(data['title'], fontsize=14, fontweight='bold', y=0.98)
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return img_base64

class MatrixChart:
    """矩阵 - 跨维度分析"""
    
    def __init__(self, width: int = 1200, height: int = 600, dpi: int = 100):
        self.width = width
        self.height = height
        self.dpi = dpi
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'rows': ['北京', '上海', '广州'],
            'columns': ['Q1', 'Q2', 'Q3', 'Q4'],
            'values': [
                [100, 150, 120, 200],
                [80, 120, 100, 180],
                [60, 90, 80, 140]
            ],
            'title': '地区季度销售额'
        }
        """
        fig, ax = plt.subplots(figsize=(self.width/100, self.height/100), dpi=self.dpi)
        
        # 创建热力图
        values = np.array(data['values'])
        im = ax.imshow(values, cmap='RdYlGn', aspect='auto')
        
        # 设置坐标轴
        ax.set_xticks(np.arange(len(data['columns'])))
        ax.set_yticks(np.arange(len(data['rows'])))
        ax.set_xticklabels(data['columns'])
        ax.set_yticklabels(data['rows'])
        
        # 旋转标签
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # 添加数值标签
        for i in range(len(data['rows'])):
            for j in range(len(data['columns'])):
                text = ax.text(j, i, values[i, j],
                             ha="center", va="center", color="black", fontweight='bold')
        
        # 标题
        if 'title' in data:
            ax.set_title(data['title'], fontsize=14, fontweight='bold', pad=20)
        
        # 颜色条
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('数值', rotation=270, labelpad=20)
        
        fig.tight_layout()
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return img_base64

# ============================================================================
# 切片器与交互组件
# ============================================================================

class SlicerComponent:
    """切片器 - 多维度筛选"""
    
    def __init__(self, width: int = 300, height: int = 400, dpi: int = 100):
        self.width = width
        self.height = height
        self.dpi = dpi
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '时间筛选',
            'type': 'date',  # 'button', 'list', 'date'
            'options': ['2026-01', '2026-02', '2026-03'],
            'selected': '2026-03'
        }
        """
        fig = plt.figure(figsize=(self.width/100, self.height/100), dpi=self.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # 标题
        ax.text(0.5, 0.95, data['title'],
               ha='center', va='top', fontsize=12,
               transform=ax.transAxes, fontweight='bold')
        
        # 选项
        options = data.get('options', [])
        y_pos = 0.85
        
        for i, option in enumerate(options):
            is_selected = option == data.get('selected')
            
            # 复选框
            checkbox_color = '#0078D4' if is_selected else '#E8E8E8'
            checkbox = Rectangle((0.05, y_pos - 0.03), 0.04, 0.04,
                               facecolor=checkbox_color,
                               edgecolor='black',
                               linewidth=1.5,
                               transform=ax.transAxes)
            ax.add_patch(checkbox)
            
            # 文本
            text_color = '#0078D4' if is_selected else 'black'
            ax.text(0.12, y_pos, option,
                   ha='left', va='center', fontsize=10,
                   transform=ax.transAxes, color=text_color,
                   fontweight='bold' if is_selected else 'normal')
            
            y_pos -= 0.08
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return img_base64

class ButtonNavigator:
    """按钮与导航器 - 报表页面跳转"""
    
    def __init__(self, width: int = 1200, height: int = 100, dpi: int = 100):
        self.width = width
        self.height = height
        self.dpi = dpi
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'buttons': [
                {'label': '首页', 'active': True},
                {'label': '销售分析', 'active': False},
                {'label': '财务报表', 'active': False},
                {'label': '导出', 'active': False}
            ]
        }
        """
        fig = plt.figure(figsize=(self.width/100, self.height/100), dpi=self.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        buttons = data.get('buttons', [])
        button_width = 0.18
        start_x = 0.05
        
        for i, button in enumerate(buttons):
            x_pos = start_x + i * (button_width + 0.02)
            
            # 按钮背景
            color = '#0078D4' if button.get('active') else '#E8E8E8'
            text_color = 'white' if button.get('active') else 'black'
            
            btn_box = FancyBboxPatch(
                (x_pos, 0.2), button_width, 0.6,
                boxstyle="round,pad=0.01",
                facecolor=color,
                edgecolor='black',
                linewidth=1.5,
                transform=ax.transAxes
            )
            ax.add_patch(btn_box)
            
            # 按钮文本
            ax.text(x_pos + button_width/2, 0.5, button['label'],
                   ha='center', va='center', fontsize=11,
                   transform=ax.transAxes, fontweight='bold',
                   color=text_color)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return img_base64

# ============================================================================
# 报告生成器
# ============================================================================

class ReportBuilder:
    """报告生成器 - 组织图表与内容"""
    
    def __init__(self):
        self.sections = []
        self.metadata = {
            'title': '',
            'author': '',
            'date': '',
            'version': '1.0'
        }
    
    def set_metadata(self, title: str = '', author: str = '', date: str = ''):
        """设置报告元数据"""
        self.metadata['title'] = title
        self.metadata['author'] = author
        self.metadata['date'] = date
    
    def add_title(self, title: str, level: int = 1):
        """添加标题"""
        self.sections.append({
            'type': 'title',
            'level': level,
            'content': title
        })
    
    def add_text(self, text: str):
        """添加文本段落"""
        self.sections.append({
            'type': 'text',
            'content': text
        })
    
    def add_chart(self, title: str, chart_b64: str, description: str = ''):
        """添加图表"""
        self.sections.append({
            'type': 'chart',
            'title': title,
            'chart': chart_b64,
            'description': description
        })
    
    def add_table(self, title: str, table_b64: str):
        """添加表格"""
        self.sections.append({
            'type': 'table',
            'title': title,
            'table': table_b64
        })
    
    def add_slicer(self, slicer_b64: str):
        """添加切片器"""
        self.sections.append({
            'type': 'slicer',
            'slicer': slicer_b64
        })
    
    def add_page_break(self):
        """添加分页符"""
        self.sections.append({
            'type': 'page_break'
        })
    
    def export_html(self, filename: str = 'report.html'):
        """导出为 HTML"""
        html_content = self._generate_html()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return filename
    
    def _generate_html(self) -> str:
        """生成 HTML 内容"""
        html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #0078D4;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            color: #0078D4;
            margin-bottom: 10px;
        }}
        .header .meta {{
            font-size: 12px;
            color: #999;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            font-size: 20px;
            color: #333;
            margin-bottom: 15px;
            border-left: 4px solid #0078D4;
            padding-left: 10px;
        }}
        .section h3 {{
            font-size: 16px;
            color: #555;
            margin-bottom: 10px;
        }}
        .section p {{
            font-size: 14px;
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }}
        .table-container {{
            margin: 20px 0;
        }}
        .table-container img {{
            max-width: 100%;
            height: auto;
        }}
        .slicer-container {{
            display: inline-block;
            margin: 10px 20px 10px 0;
        }}
        .page-break {{
            page-break-after: always;
            margin: 40px 0;
            border-top: 2px dashed #ccc;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 12px;
            color: #999;
            text-align: center;
        }}
        @media print {{
            body {{ background-color: white; }}
            .container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="meta">
                <span>作者: {author}</span> | 
                <span>日期: {date}</span> | 
                <span>版本: {version}</span>
            </div>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            <p>本报告由 sql-dataviz + sql-report-generator 自动生成</p>
        </div>
    </div>
</body>
</html>
        """
        
        content = self._render_sections()
        
        return html.format(
            title=self.metadata['title'],
            author=self.metadata['author'],
            date=self.metadata['date'],
            version=self.metadata['version'],
            content=content
        )
    
    def _render_sections(self) -> str:
        """渲染所有章节"""
        html_parts = []
        
        for section in self.sections:
            if section['type'] == 'title':
                level = section.get('level', 1)
                html_parts.append(f"<h{level}>{section['content']}</h{level}>")
            
            elif section['type'] == 'text':
                html_parts.append(f"<p>{section['content']}</p>")
            
            elif section['type'] == 'chart':
                html_parts.append(f"""
                <div class="section">
                    <h3>{section['title']}</h3>
                    {f'<p>{section["description"]}</p>' if section.get('description') else ''}
                    <div class="chart-container">
                        <img src="data:image/png;base64,{section['chart']}" />
                    </div>
                </div>
                """)
            
            elif section['type'] == 'table':
                html_parts.append(f"""
                <div class="section">
                    <h3>{section['title']}</h3>
                    <div class="table-container">
                        <img src="data:image/png;base64,{section['table']}" />
                    </div>
                </div>
                """)
            
            elif section['type'] == 'slicer':
                html_parts.append(f"""
                <div class="slicer-container">
                    <img src="data:image/png;base64,{section['slicer']}" />
                </div>
                """)
            
            elif section['type'] == 'page_break':
                html_parts.append('<div class="page-break"></div>')
        
        return '\n'.join(html_parts)
    
    def export_json(self, filename: str = 'report.json') -> str:
        """导出为 JSON（用于 API 集成）"""
        report_data = {
            'metadata': self.metadata,
            'sections': self.sections
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        return filename

# ============================================================================
# 使用示例
# ============================================================================

if __name__ == '__main__':
    # 1. 创建表格
    table = TableChart()
    table_b64 = table.create({
        'columns': ['订单ID', '客户', '金额', '日期'],
        'rows': [
            ['ORD001', '张三', '¥1,000', '2026-03-26'],
            ['ORD002', '李四', '¥2,500', '2026-03-25'],
            ['ORD003', '王五', '¥1,800', '2026-03-24']
        ],
        'title': '订单列表'
    })
    
    # 2. 创建矩阵
    matrix = MatrixChart()
    matrix_b64 = matrix.create({
        'rows': ['北京', '上海', '广州'],
        'columns': ['Q1', 'Q2', 'Q3', 'Q4'],
        'values': [
            [100, 150, 120, 200],
            [80, 120, 100, 180],
            [60, 90, 80, 140]
        ],
        'title': '地区季度销售额'
    })
    
    # 3. 创建切片器
    slicer = SlicerComponent()
    slicer_b64 = slicer.create({
        'title': '时间筛选',
        'options': ['2026-01', '2026-02', '2026-03'],
        'selected': '2026-03'
    })
    
    # 4. 创建导航按钮
    navigator = ButtonNavigator()
    nav_b64 = navigator.create({
        'buttons': [
            {'label': '首页', 'active': True},
            {'label': '销售分析', 'active': False},
            {'label': '财务报表', 'active': False}
        ]
    })
    
    # 5. 生成报告
    report = ReportBuilder()
    report.set_metadata(
        title='月度业绩报告',
        author='数据分析团队',
        date='2026-03-26'
    )
    
    report.add_title('月度业绩报告', level=1)
    report.add_text('本报告汇总了本月的关键业绩指标和分析洞察。')
    
    report.add_title('订单数据', level=2)
    report.add_table('订单列表', table_b64)
    
    report.add_title('地区分析', level=2)
    report.add_table('地区季度销售额', matrix_b64)
    
    report.export_html('report.html')
    print("✓ 报告已生成: report.html")
