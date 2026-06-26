"""
sql-dataviz: SQL 数据可视化 Skill
生产级 Power BI 风格的 24+ 种图表实现
所有图表以 base64 PNG 方式输出，支持大厂生产场景
"""

import base64
import io
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch, Wedge
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as _fm

# ── 自动配置中文字体（Windows 优先微软雅黑）──────────────────────────────
def _setup_chinese_font():
    _candidates = ['Microsoft YaHei', 'SimHei', 'Noto Sans SC', 'STSong', 'SimSun']
    _available = {f.name for f in _fm.fontManager.ttflist}
    for _font in _candidates:
        if _font in _available:
            plt.rcParams['font.sans-serif'] = [_font, 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            break

_setup_chinese_font()
# ─────────────────────────────────────────────────────────────────────────────

# ============================================================================
# 配置与主题
# ============================================================================

class Theme(Enum):
    """大厂配色主题"""
    POWERBI = "powerbi"      # Power BI 官方蓝
    ALIBABA = "alibaba"      # 阿里巴巴红
    TENCENT = "tencent"      # 腾讯蓝
    BYTEDANCE = "bytedance"  # 字节跳动黑
    NEUTRAL = "neutral"      # 中性灰

THEME_COLORS = {
    Theme.POWERBI: {
        'primary': '#0078D4',
        'secondary': '#50E6FF',
        'accent': '#FFB900',
        'palette': ['#0078D4', '#50E6FF', '#FFB900', '#107C10', '#D83B01', '#8661C5']
    },
    Theme.ALIBABA: {
        'primary': '#FF6B6B',
        'secondary': '#FFA940',
        'accent': '#1890FF',
        'palette': ['#FF6B6B', '#FFA940', '#1890FF', '#52C41A', '#722ED1', '#EB2F96']
    },
    Theme.TENCENT: {
        'primary': '#0052CC',
        'secondary': '#0066FF',
        'accent': '#00D4AA',
        'palette': ['#0052CC', '#0066FF', '#00D4AA', '#FF6B6B', '#FFD666', '#95DE64']
    },
    Theme.BYTEDANCE: {
        'primary': '#000000',
        'secondary': '#333333',
        'accent': '#0066FF',
        'palette': ['#000000', '#333333', '#0066FF', '#FF6B6B', '#FFD666', '#95DE64']
    },
    Theme.NEUTRAL: {
        'primary': '#595959',
        'secondary': '#8C8C8C',
        'accent': '#1890FF',
        'palette': ['#595959', '#8C8C8C', '#1890FF', '#52C41A', '#FF7A45', '#722ED1']
    }
}

# ============================================================================
# 基础工具类
# ============================================================================

@dataclass
class ChartConfig:
    """图表配置"""
    width: int = 1200
    height: int = 600
    dpi: int = 100
    theme: Theme = Theme.POWERBI
    title: str = ""
    subtitle: str = ""
    show_legend: bool = True
    show_grid: bool = True
    font_size: int = 11
    title_size: int = 16

class ChartBase:
    """图表基类"""
    
    def __init__(self, config: ChartConfig = None):
        self.config = config or ChartConfig()
        self.colors = THEME_COLORS[self.config.theme]['palette']
        self.primary_color = THEME_COLORS[self.config.theme]['primary']
        
    def _setup_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """初始化图表"""
        fig, ax = plt.subplots(
            figsize=(self.config.width/100, self.config.height/100),
            dpi=self.config.dpi
        )
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#F5F5F5')
        
        # 设置标题
        if self.config.title:
            fig.suptitle(
                self.config.title,
                fontsize=self.config.title_size,
                fontweight='bold',
                y=0.98
            )
        
        return fig, ax
    
    def _to_base64(self, fig: plt.Figure) -> str:
        """转换为 base64"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.config.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return img_base64
    
    def _apply_grid(self, ax: plt.Axes):
        """应用网格"""
        if self.config.show_grid:
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            ax.set_axisbelow(True)

# ============================================================================
# 一、对比与趋势分析类（8种）
# ============================================================================

class ClusteredColumnChart(ChartBase):
    """簇状柱形图 - 多系列分类对比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
            'series': [
                {'name': '销售额', 'data': [100, 150, 120, 200]},
                {'name': '成本', 'data': [60, 80, 70, 100]}
            ]
        }
        """
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        width = 0.35
        
        for i, series in enumerate(data['series']):
            offset = (i - len(data['series'])/2 + 0.5) * width
            ax.bar(x + offset, series['data'], width, 
                   label=series['name'], color=self.colors[i % len(self.colors)])
        
        ax.set_xlabel('分类', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class StackedColumnChart(ChartBase):
    """堆积柱形图 - 整体+部分占比对比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        bottom = np.zeros(len(categories))
        for i, series in enumerate(data['series']):
            ax.bar(x, series['data'], label=series['name'],
                   bottom=bottom, color=self.colors[i % len(self.colors)])
            bottom += np.array(series['data'])
        
        ax.set_xlabel('分类', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class PercentStackedColumnChart(ChartBase):
    """100%堆积柱形图 - 统一尺度结构对比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        # 计算百分比
        totals = np.zeros(len(categories))
        for series in data['series']:
            totals += np.array(series['data'])
        
        bottom = np.zeros(len(categories))
        for i, series in enumerate(data['series']):
            percentages = (np.array(series['data']) / totals) * 100
            ax.bar(x, percentages, label=series['name'],
                   bottom=bottom, color=self.colors[i % len(self.colors)])
            bottom += percentages
        
        ax.set_xlabel('分类', fontsize=self.config.font_size)
        ax.set_ylabel('百分比 (%)', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class ClusteredBarChart(ChartBase):
    """簇状条形图 - 长分类名称对比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        y = np.arange(len(categories))
        height = 0.35
        
        for i, series in enumerate(data['series']):
            offset = (i - len(data['series'])/2 + 0.5) * height
            ax.barh(y + offset, series['data'], height,
                    label=series['name'], color=self.colors[i % len(self.colors)])
        
        ax.set_ylabel('分类', fontsize=self.config.font_size)
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        ax.set_yticks(y)
        ax.set_yticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='lower right', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class LineChart(ChartBase):
    """折线图 - 连续数据趋势"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        for i, series in enumerate(data['series']):
            ax.plot(x, series['data'], marker='o', linewidth=2.5,
                    label=series['name'], color=self.colors[i % len(self.colors)])
        
        ax.set_xlabel('时间', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class AreaChart(ChartBase):
    """面积图 - 累计总量展示"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        bottom = np.zeros(len(categories))
        for i, series in enumerate(data['series']):
            ax.fill_between(x, bottom, bottom + np.array(series['data']),
                            label=series['name'], alpha=0.7,
                            color=self.colors[i % len(self.colors)])
            bottom += np.array(series['data'])
        
        ax.set_xlabel('时间', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class WaterfallChart(ChartBase):
    """瀑布图 - 增减项影响分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'categories': ['开始', '收入', '成本', '费用', '结束'],
            'values': [100, 200, -80, -50, 170]
        }
        """
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        values = data['values']
        
        cumulative = 0
        colors_list = []
        
        for i, val in enumerate(values):
            if i == 0 or i == len(values) - 1:
                ax.bar(i, val, color=self.primary_color, width=0.6)
                cumulative = val
            else:
                if val >= 0:
                    ax.bar(i, val, bottom=cumulative, color='#52C41A', width=0.6)
                    colors_list.append('#52C41A')
                else:
                    ax.bar(i, val, bottom=cumulative, color='#FF7A45', width=0.6)
                    colors_list.append('#FF7A45')
                cumulative += val
        
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

# ============================================================================
# 二、部分与整体关系类（4种）
# ============================================================================

class PieChart(ChartBase):
    """饼图 - 单维度占比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'labels': ['A', 'B', 'C'],
            'values': [30, 25, 45]
        }
        """
        fig, ax = self._setup_figure()
        
        wedges, texts, autotexts = ax.pie(
            data['values'],
            labels=data['labels'],
            autopct='%1.1f%%',
            colors=self.colors[:len(data['values'])],
            startangle=90
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.axis('equal')
        return self._to_base64(fig)

class DonutChart(ChartBase):
    """圆环图 - 中心标签占比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        wedges, texts, autotexts = ax.pie(
            data['values'],
            labels=data['labels'],
            autopct='%1.1f%%',
            colors=self.colors[:len(data['values'])],
            startangle=90
        )
        
        # 绘制中心圆环
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.axis('equal')
        return self._to_base64(fig)

class TreemapChart(ChartBase):
    """树状图 - 层级数据展示"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'labels': ['A', 'B', 'C', 'D'],
            'sizes': [100, 200, 150, 120],
            'colors': [1, 2, 3, 4]
        }
        """
        fig, ax = self._setup_figure()
        
        try:
            import squarify
            squarify.plot(
                sizes=data['sizes'],
                label=data['labels'],
                color=self.colors[:len(data['labels'])],
                ax=ax,
                text_kwargs={'fontsize': 10, 'weight': 'bold'}
            )
        except ImportError:
            # 如果没有 squarify，使用简单的矩形布局
            ax.text(0.5, 0.5, '需要安装 squarify\npip install squarify',
                    ha='center', va='center', fontsize=12)
        
        ax.axis('off')
        return self._to_base64(fig)

class FunnelChart(ChartBase):
    """漏斗图 - 流程转化分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'stages': ['访问', '点击', '注册', '购买'],
            'values': [1000, 800, 500, 200]
        }
        """
        fig, ax = self._setup_figure()
        
        stages = data['stages']
        values = data['values']
        max_val = max(values)
        
        for i, (stage, val) in enumerate(zip(stages, values)):
            width = (val / max_val) * 0.8
            height = 0.15
            left = (1 - width) / 2
            
            rect = FancyBboxPatch(
                (left, 1 - (i + 1) * height),
                width, height * 0.9,
                boxstyle="round,pad=0.01",
                facecolor=self.colors[i % len(self.colors)],
                edgecolor='white',
                linewidth=2
            )
            ax.add_patch(rect)
            
            # 添加标签
            ax.text(0.5, 1 - (i + 0.5) * height,
                    f'{stage}\n{val}',
                    ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return self._to_base64(fig)

# ============================================================================
# 三、分布与关系分析类（4种）
# ============================================================================

class ScatterChart(ChartBase):
    """散点图 - 两变量相关性"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 5, 4, 6],
            'labels': ['A', 'B', 'C', 'D', 'E']
        }
        """
        fig, ax = self._setup_figure()
        
        ax.scatter(data['x'], data['y'], s=100, alpha=0.6,
                   color=self.primary_color, edgecolors='black', linewidth=1.5)
        
        ax.set_xlabel('X 轴', fontsize=self.config.font_size)
        ax.set_ylabel('Y 轴', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class BubbleChart(ChartBase):
    """气泡图 - 三变量分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'x': [1, 2, 3, 4],
            'y': [2, 4, 5, 4],
            'size': [100, 200, 150, 300],
            'labels': ['A', 'B', 'C', 'D']
        }
        """
        fig, ax = self._setup_figure()
        
        scatter = ax.scatter(data['x'], data['y'],
                            s=data['size'],
                            alpha=0.6,
                            c=range(len(data['x'])),
                            cmap='viridis',
                            edgecolors='black',
                            linewidth=1.5)
        
        ax.set_xlabel('X 轴', fontsize=self.config.font_size)
        ax.set_ylabel('Y 轴', fontsize=self.config.font_size)
        
        plt.colorbar(scatter, ax=ax, label='分类')
        self._apply_grid(ax)
        return self._to_base64(fig)

class DotChart(ChartBase):
    """点图 - 分类数据分布"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        values = data['values']
        
        for i, (cat, val) in enumerate(zip(categories, values)):
            ax.scatter([val], [i], s=200, alpha=0.7,
                      color=self.colors[i % len(self.colors)],
                      edgecolors='black', linewidth=1.5)
        
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories)
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class HighDensityScatterChart(ChartBase):
    """高密度散点图 - 海量数据聚类"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        # 使用 hexbin 处理高密度数据
        hb = ax.hexbin(data['x'], data['y'], gridsize=20,
                       cmap='YlOrRd', mincnt=1)
        
        ax.set_xlabel('X 轴', fontsize=self.config.font_size)
        ax.set_ylabel('Y 轴', fontsize=self.config.font_size)
        
        plt.colorbar(hb, ax=ax, label='密度')
        return self._to_base64(fig)

# ============================================================================
# 四、地理空间类（3种）
# ============================================================================

class FilledMapChart(ChartBase):
    """填充地图 - 区域数据热力"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'regions': ['北京', '上海', '广州'],
            'values': [100, 150, 120]
        }
        """
        fig, ax = self._setup_figure()
        
        # 简化版本：使用条形图模拟地图
        regions = data['regions']
        values = data['values']
        
        colors_map = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(values)))
        ax.barh(regions, values, color=colors_map)
        
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        ax.set_title('区域热力分布', fontsize=self.config.title_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class ShapeMapChart(ChartBase):
    """形状地图 - 自定义边界分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        # 简化版本：使用散点图模拟形状地图
        ax.scatter(data['x'], data['y'], s=data['size'],
                  c=data['values'], cmap='viridis',
                  alpha=0.6, edgecolors='black', linewidth=1.5)
        
        ax.set_xlabel('经度', fontsize=self.config.font_size)
        ax.set_ylabel('纬度', fontsize=self.config.font_size)
        
        plt.colorbar(ax.collections[0], ax=ax, label='数值')
        return self._to_base64(fig)

class ArcGISMapChart(ChartBase):
    """ArcGIS 地图 - 专业空间分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        # 简化版本：使用网格热力图
        x = np.linspace(0, 10, 20)
        y = np.linspace(0, 10, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.random.rand(20, 20) * 100
        
        im = ax.contourf(X, Y, Z, levels=15, cmap='RdYlGn')
        ax.contour(X, Y, Z, levels=5, colors='black', alpha=0.3, linewidths=0.5)
        
        ax.set_xlabel('经度', fontsize=self.config.font_size)
        ax.set_ylabel('纬度', fontsize=self.config.font_size)
        
        plt.colorbar(im, ax=ax, label='数值')
        return self._to_base64(fig)

# ============================================================================
# 五、指标监控类（3种）
# ============================================================================

class CardChart(ChartBase):
    """卡片图 - 单一关键指标"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '日活用户',
            'value': '1,234,567',
            'unit': '人',
            'change': '+12.5%'
        }
        """
        fig = plt.figure(figsize=(4, 2), dpi=self.config.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # 绘制卡片背景
        rect = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                             boxstyle="round,pad=0.02",
                             facecolor='white',
                             edgecolor=self.primary_color,
                             linewidth=3,
                             transform=ax.transAxes)
        ax.add_patch(rect)
        
        # 标题
        ax.text(0.5, 0.75, data['title'],
               ha='center', va='center', fontsize=12,
               transform=ax.transAxes, fontweight='bold')
        
        # 数值
        ax.text(0.5, 0.45, data['value'],
               ha='center', va='center', fontsize=24,
               transform=ax.transAxes, fontweight='bold',
               color=self.primary_color)
        
        # 变化
        ax.text(0.5, 0.15, data.get('change', ''),
               ha='center', va='center', fontsize=11,
               transform=ax.transAxes, color='#52C41A')
        
        return self._to_base64(fig)

class KPIChart(ChartBase):
    """KPI 视觉对象 - 目标达成率"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '年度营收目标',
            'current': 750,
            'target': 1000,
            'unit': '万元'
        }
        """
        fig, ax = self._setup_figure()
        
        current = data['current']
        target = data['target']
        percentage = (current / target) * 100
        
        # 绘制进度条背景
        ax.barh([0], [100], height=0.3, color='#E8E8E8', left=0)
        
        # 绘制进度条前景
        ax.barh([0], [percentage], height=0.3,
               color=self.primary_color if percentage >= 100 else '#FFB900')
        
        # 添加标签
        ax.text(percentage/2, 0, f'{percentage:.1f}%',
               ha='center', va='center', fontsize=14,
               fontweight='bold', color='white')
        
        ax.set_xlim(0, 120)
        ax.set_ylim(-0.5, 0.5)
        ax.axis('off')
        
        return self._to_base64(fig)

class GaugeChart(ChartBase):
    """仪表盘图 - 指标健康度"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '服务器负载',
            'value': 65,
            'min': 0,
            'max': 100
        }
        """
        fig, ax = self._setup_figure()
        
        value = data['value']
        max_val = data.get('max', 100)
        
        # 绘制仪表盘背景
        theta = np.linspace(np.pi, 2*np.pi, 100)
        r = 1
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        ax.plot(x, y, 'k-', linewidth=3)
        
        # 绘制颜色区域
        theta_green = np.linspace(np.pi, np.pi + np.pi/3, 50)
        x_green = r * np.cos(theta_green)
        y_green = r * np.sin(theta_green)
        ax.fill_between(x_green, 0, y_green, color='#52C41A', alpha=0.3)
        
        theta_yellow = np.linspace(np.pi + np.pi/3, np.pi + 2*np.pi/3, 50)
        x_yellow = r * np.cos(theta_yellow)
        y_yellow = r * np.sin(theta_yellow)
        ax.fill_between(x_yellow, 0, y_yellow, color='#FFB900', alpha=0.3)
        
        theta_red = np.linspace(np.pi + 2*np.pi/3, 2*np.pi, 50)
        x_red = r * np.cos(theta_red)
        y_red = r * np.sin(theta_red)
        ax.fill_between(x_red, 0, y_red, color='#FF7A45', alpha=0.3)
        
        # 绘制指针
        angle = np.pi + (value / max_val) * np.pi
        pointer_x = 0.8 * np.cos(angle)
        pointer_y = 0.8 * np.sin(angle)
        ax.arrow(0, 0, pointer_x, pointer_y, head_width=0.1,
                head_length=0.1, fc='black', ec='black', linewidth=2)
        
        # 中心圆
        circle = plt.Circle((0, 0), 0.1, color='black')
        ax.add_patch(circle)
        
        # 标签
        ax.text(0, -1.3, f'{value}%', ha='center', fontsize=16, fontweight='bold')
        ax.text(0, -1.5, data['title'], ha='center', fontsize=12)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.7, 1.2)
        ax.axis('equal')
        ax.axis('off')
        
        return self._to_base64(fig)

# ============================================================================
# 六、AI 智能分析类（4种）
# ============================================================================

class DecompositionTreeChart(ChartBase):
    """分解树 - 多维度根因分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'root': '销售额下降',
            'children': [
                {'name': '产品A', 'value': -30},
                {'name': '产品B', 'value': -20},
                {'name': '产品C', 'value': -10}
            ]
        }
        """
        fig, ax = self._setup_figure()
        
        # 绘制根节点
        root_box = FancyBboxPatch((0.35, 0.8), 0.3, 0.1,
                                 boxstyle="round,pad=0.01",
                                 facecolor=self.primary_color,
                                 edgecolor='black',
                                 linewidth=2,
                                 transform=ax.transAxes)
        ax.add_patch(root_box)
        ax.text(0.5, 0.85, data['root'],
               ha='center', va='center', fontsize=11,
               transform=ax.transAxes, fontweight='bold', color='white')
        
        # 绘制子节点
        children = data.get('children', [])
        for i, child in enumerate(children):
            x_pos = 0.2 + (i * 0.3)
            
            # 连接线
            ax.plot([0.5, x_pos + 0.1], [0.8, 0.5],
                   'k-', linewidth=1, transform=ax.transAxes)
            
            # 子节点框
            color = '#52C41A' if child['value'] > 0 else '#FF7A45'
            child_box = FancyBboxPatch((x_pos, 0.35), 0.2, 0.1,
                                      boxstyle="round,pad=0.01",
                                      facecolor=color,
                                      edgecolor='black',
                                      linewidth=1.5,
                                      transform=ax.transAxes)
            ax.add_patch(child_box)
            
            ax.text(x_pos + 0.1, 0.45, f"{child['name']}\n{child['value']}%",
                   ha='center', va='center', fontsize=9,
                   transform=ax.transAxes, fontweight='bold', color='white')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        return self._to_base64(fig)

class KeyInfluencersChart(ChartBase):
    """关键影响因素 - 驱动因子权重"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'factors': ['价格', '质量', '服务', '品牌'],
            'weights': [0.35, 0.30, 0.20, 0.15]
        }
        """
        fig, ax = self._setup_figure()
        
        factors = data['factors']
        weights = data['weights']
        
        # 按权重排序
        sorted_data = sorted(zip(factors, weights), key=lambda x: x[1], reverse=True)
        factors_sorted, weights_sorted = zip(*sorted_data)
        
        bars = ax.barh(factors_sorted, weights_sorted,
                      color=self.colors[:len(factors_sorted)])
        
        # 添加百分比标签
        for i, (bar, weight) in enumerate(zip(bars, weights_sorted)):
            ax.text(weight + 0.01, i, f'{weight*100:.1f}%',
                   va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('权重', fontsize=self.config.font_size)
        ax.set_xlim(0, max(weights_sorted) * 1.2)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class AnomalyDetectionChart(ChartBase):
    """异常检测 - 自动异常标注"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'x': [1, 2, 3, 4, 5, 6, 7, 8],
            'y': [10, 12, 11, 50, 13, 12, 11, 10],
            'anomalies': [3]  # 索引
        }
        """
        fig, ax = self._setup_figure()
        
        x = data['x']
        y = data['y']
        anomalies = data.get('anomalies', [])
        
        # 绘制正常数据
        ax.plot(x, y, 'o-', linewidth=2, markersize=8,
               color=self.primary_color, label='正常数据')
        
        # 标注异常点
        for idx in anomalies:
            ax.scatter(x[idx], y[idx], s=200, color='red',
                      marker='X', edgecolors='darkred', linewidth=2,
                      label='异常' if idx == anomalies[0] else '')
            
            # 添加异常标签
            ax.annotate('异常', xy=(x[idx], y[idx]),
                       xytext=(10, 10), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax.set_xlabel('时间', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.legend(loc='upper left')
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class SmartNarrativeChart(ChartBase):
    """智能叙事 - 自然语言摘要"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '月度业绩总结',
            'insights': [
                '销售额环比增长 15%',
                '北京地区贡献最大，占比 35%',
                '新客户转化率达到历史新高'
            ]
        }
        """
        fig = plt.figure(figsize=(10, 6), dpi=self.config.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # 标题
        ax.text(0.5, 0.95, data['title'],
               ha='center', va='top', fontsize=16,
               transform=ax.transAxes, fontweight='bold')
        
        # 洞察内容
        insights = data.get('insights', [])
        y_pos = 0.85
        
        for i, insight in enumerate(insights):
            # 编号圆圈
            circle = plt.Circle((0.08, y_pos), 0.02,
                              color=self.colors[i % len(self.colors)],
                              transform=ax.transAxes)
            ax.add_patch(circle)
            ax.text(0.08, y_pos, str(i+1),
                   ha='center', va='center', fontsize=10,
                   transform=ax.transAxes, fontweight='bold', color='white')
            
            # 文本
            ax.text(0.12, y_pos, insight,
                   ha='left', va='center', fontsize=11,
                   transform=ax.transAxes, wrap=True)
            
            y_pos -= 0.15
        
        return self._to_base64(fig)

# ============================================================================
# 补充的缺失图表（5种）
# ============================================================================

class StackedBarChart(ChartBase):
    """堆积条形图 - 区域/渠道层级对比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        y = np.arange(len(categories))
        
        bottom = np.zeros(len(categories))
        for i, series in enumerate(data['series']):
            ax.barh(y, series['data'], label=series['name'],
                   left=bottom, color=self.colors[i % len(self.colors)])
            bottom += np.array(series['data'])
        
        ax.set_ylabel('分类', fontsize=self.config.font_size)
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        ax.set_yticks(y)
        ax.set_yticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='lower right', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class PercentStackedBarChart(ChartBase):
    """100%堆积条形图 - 横向结构占比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        y = np.arange(len(categories))
        
        # 计算百分比
        totals = np.zeros(len(categories))
        for series in data['series']:
            totals += np.array(series['data'])
        
        bottom = np.zeros(len(categories))
        for i, series in enumerate(data['series']):
            percentages = (np.array(series['data']) / totals) * 100
            ax.barh(y, percentages, label=series['name'],
                   left=bottom, color=self.colors[i % len(self.colors)])
            bottom += percentages
        
        ax.set_ylabel('分类', fontsize=self.config.font_size)
        ax.set_xlabel('百分比 (%)', fontsize=self.config.font_size)
        ax.set_yticks(y)
        ax.set_yticklabels(categories)
        ax.set_xlim(0, 100)
        
        if self.config.show_legend:
            ax.legend(loc='lower right', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class SmoothLineChart(ChartBase):
    """平滑折线图 - 弱化波动的趋势"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        for i, series in enumerate(data['series']):
            # 使用样条插值平滑曲线
            from scipy.interpolate import make_interp_spline
            try:
                spl = make_interp_spline(x, series['data'], k=3)
                x_smooth = np.linspace(x.min(), x.max(), 300)
                y_smooth = spl(x_smooth)
                ax.plot(x_smooth, y_smooth, linewidth=2.5,
                       label=series['name'], color=self.colors[i % len(self.colors)])
            except:
                # 如果 scipy 不可用，使用普通折线
                ax.plot(x, series['data'], marker='o', linewidth=2.5,
                       label=series['name'], color=self.colors[i % len(self.colors)])
        
        ax.set_xlabel('时间', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class ComboChart(ChartBase):
    """组合图 - 双指标（柱形+折线）"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
            'columns': {'name': '销售额', 'data': [100, 150, 120, 200]},
            'lines': {'name': '增长率', 'data': [10, 15, 12, 20]}
        }
        """
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        # 绘制柱形图
        col_data = data['columns']
        ax.bar(x, col_data['data'], label=col_data['name'],
              color=self.colors[0], alpha=0.7, width=0.6)
        
        # 创建第二个 y 轴
        ax2 = ax.twinx()
        
        # 绘制折线图
        line_data = data['lines']
        ax2.plot(x, line_data['data'], marker='o', linewidth=2.5,
                label=line_data['name'], color=self.colors[1])
        
        ax.set_xlabel('分类', fontsize=self.config.font_size)
        ax.set_ylabel(col_data['name'], fontsize=self.config.font_size, color=self.colors[0])
        ax2.set_ylabel(line_data['name'], fontsize=self.config.font_size, color=self.colors[1])
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        # 合并图例
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class StackedAreaChart(ChartBase):
    """堆积面积图 - 多业务线累计贡献"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        x = np.arange(len(categories))
        
        bottom = np.zeros(len(categories))
        for i, series in enumerate(data['series']):
            ax.fill_between(x, bottom, bottom + np.array(series['data']),
                           label=series['name'], alpha=0.7,
                           color=self.colors[i % len(self.colors)])
            bottom += np.array(series['data'])
        
        ax.set_xlabel('时间', fontsize=self.config.font_size)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if self.config.show_legend:
            ax.legend(loc='upper left', framealpha=0.9)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class MultiCardChart(ChartBase):
    """多行卡片图 - 多指标汇总"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'cards': [
                {'title': '销售额', 'value': '¥1,234,567', 'change': '+12.5%'},
                {'title': '订单数', 'value': '5,678', 'change': '+8.3%'},
                {'title': '转化率', 'value': '3.45%', 'change': '-0.5%'}
            ]
        }
        """
        cards = data.get('cards', [])
        cols = min(3, len(cards))
        rows = (len(cards) + cols - 1) // cols
        
        fig = plt.figure(figsize=(self.config.width/100, rows * 1.5), dpi=self.config.dpi)
        
        for idx, card in enumerate(cards):
            ax = fig.add_subplot(rows, cols, idx + 1)
            ax.axis('off')
            
            # 绘制卡片背景
            rect = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                 boxstyle="round,pad=0.02",
                                 facecolor='white',
                                 edgecolor=self.primary_color,
                                 linewidth=2,
                                 transform=ax.transAxes)
            ax.add_patch(rect)
            
            # 标题
            ax.text(0.5, 0.75, card['title'],
                   ha='center', va='center', fontsize=11,
                   transform=ax.transAxes, fontweight='bold')
            
            # 数值
            ax.text(0.5, 0.45, card['value'],
                   ha='center', va='center', fontsize=18,
                   transform=ax.transAxes, fontweight='bold',
                   color=self.primary_color)
            
            # 变化
            change_color = '#52C41A' if '+' in card.get('change', '') else '#FF7A45'
            ax.text(0.5, 0.15, card.get('change', ''),
                   ha='center', va='center', fontsize=10,
                   transform=ax.transAxes, color=change_color, fontweight='bold')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        
        fig.tight_layout()
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.config.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return img_base64

class TargetChart(ChartBase):
    """目标视觉对象 - 团队绩效看板"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '团队绩效',
            'items': [
                {'name': '销售目标', 'current': 750, 'target': 1000, 'status': 'warning'},
                {'name': '客户满意度', 'current': 85, 'target': 90, 'status': 'success'},
                {'name': '成本控制', 'current': 120, 'target': 100, 'status': 'danger'}
            ]
        }
        """
        fig, ax = self._setup_figure()
        
        items = data.get('items', [])
        y_pos = len(items) - 0.5
        
        for item in items:
            current = item['current']
            target = item['target']
            percentage = (current / target) * 100
            status = item.get('status', 'normal')
            
            # 状态颜色
            if status == 'success':
                color = '#52C41A'
            elif status == 'warning':
                color = '#FFB900'
            else:
                color = '#FF7A45'
            
            # 背景条
            ax.barh([y_pos], [100], height=0.4, color='#E8E8E8', left=0)
            
            # 进度条
            ax.barh([y_pos], [min(percentage, 100)], height=0.4, color=color, left=0)
            
            # 标签
            ax.text(-5, y_pos, item['name'], ha='right', va='center', fontsize=10, fontweight='bold')
            ax.text(50, y_pos, f'{percentage:.0f}%', ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='white')
            
            y_pos -= 1
        
        ax.set_xlim(-30, 110)
        ax.set_ylim(-0.5, len(items) - 0.5)
        ax.axis('off')
        
        return self._to_base64(fig)

class AzureMapChart(ChartBase):
    """Azure 地图 - 权威地图底图"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        # 简化版本：使用散点图模拟地图
        regions = data.get('regions', [])
        values = data.get('values', [])
        
        colors_map = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(values)))
        ax.scatter(range(len(regions)), values, s=300, c=colors_map, alpha=0.6, edgecolors='black', linewidth=1.5)
        
        ax.set_xticks(range(len(regions)))
        ax.set_xticklabels(regions, rotation=45, ha='right')
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_title('Azure 地图 - 区域分布', fontsize=self.config.title_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class ImageVisualChart(ChartBase):
    """图像视觉对象 - 品牌 logo、产品图片"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '产品展示',
            'images': [
                {'url': 'path/to/image1.png', 'label': '产品A'},
                {'url': 'path/to/image2.png', 'label': '产品B'}
            ]
        }
        """
        fig = plt.figure(figsize=(self.config.width/100, self.config.height/100), dpi=self.config.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # 标题
        ax.text(0.5, 0.95, data.get('title', '图像展示'),
               ha='center', va='top', fontsize=14,
               transform=ax.transAxes, fontweight='bold')
        
        # 显示占位符
        ax.text(0.5, 0.5, '图像视觉对象\n(支持嵌入图片)',
               ha='center', va='center', fontsize=12,
               transform=ax.transAxes, style='italic', color='gray')
        
        return self._to_base64(fig)

class TextShapeChart(ChartBase):
    """文本框与形状 - 报表标题、说明描述"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '报表标题',
            'description': '这是一个描述文本',
            'shapes': ['arrow', 'box', 'circle']
        }
        """
        fig = plt.figure(figsize=(self.config.width/100, self.config.height/100), dpi=self.config.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # 标题
        ax.text(0.5, 0.85, data.get('title', '标题'),
               ha='center', va='top', fontsize=16,
               transform=ax.transAxes, fontweight='bold')
        
        # 描述
        ax.text(0.5, 0.5, data.get('description', '描述文本'),
               ha='center', va='center', fontsize=12,
               transform=ax.transAxes, wrap=True)
        
        # 绘制形状
        shapes = data.get('shapes', [])
        x_pos = 0.2
        for shape in shapes:
            if shape == 'arrow':
                ax.annotate('', xy=(x_pos + 0.05, 0.2), xytext=(x_pos, 0.2),
                           arrowprops=dict(arrowstyle='->', lw=2, color=self.primary_color),
                           transform=ax.transAxes)
            elif shape == 'box':
                rect = Rectangle((x_pos, 0.15), 0.05, 0.1, 
                               facecolor=self.primary_color, alpha=0.3,
                               transform=ax.transAxes)
                ax.add_patch(rect)
            elif shape == 'circle':
                circle = plt.Circle((x_pos + 0.025, 0.2), 0.025,
                                  facecolor=self.primary_color, alpha=0.3,
                                  transform=ax.transAxes)
                ax.add_patch(circle)
            x_pos += 0.15
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        return self._to_base64(fig)

# ============================================================================
# 补充的高级图表（18种）
# ============================================================================

class BoxPlotChart(ChartBase):
    """盒须图 - 显示数据分布的四分位数"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'categories': ['A', 'B', 'C'],
            'data': [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [1, 3, 5, 7, 9]]
        }
        """
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        box_data = data['data']
        
        bp = ax.boxplot(box_data, labels=categories, patch_artist=True)
        
        for patch, color in zip(bp['boxes'], self.colors[:len(categories)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_xlabel('分类', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class HistogramChart(ChartBase):
    """直方图 - 数据频率分布"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'values': [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5],
            'bins': 10
        }
        """
        fig, ax = self._setup_figure()
        
        values = data['values']
        bins = data.get('bins', 10)
        
        ax.hist(values, bins=bins, color=self.primary_color, alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        ax.set_ylabel('频率', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class DensityPlotChart(ChartBase):
    """密度图 - 概率密度分布"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        values = data['values']
        
        # 使用 seaborn 绘制密度图
        sns.kdeplot(data=values, ax=ax, fill=True, color=self.primary_color, alpha=0.6)
        
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        ax.set_ylabel('密度', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class ParetoChart(ChartBase):
    """帕累托图 - 80/20 法则分析"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'categories': ['A', 'B', 'C', 'D', 'E'],
            'values': [100, 80, 60, 40, 20]
        }
        """
        fig, ax = self._setup_figure()
        
        categories = data['categories']
        values = np.array(data['values'])
        
        # 排序
        sorted_idx = np.argsort(values)[::-1]
        sorted_values = values[sorted_idx]
        sorted_categories = [categories[i] for i in sorted_idx]
        
        # 绘制柱形图
        ax.bar(range(len(sorted_categories)), sorted_values, 
              color=self.primary_color, alpha=0.7)
        
        # 绘制累计百分比线
        cumsum = np.cumsum(sorted_values)
        cumsum_pct = (cumsum / cumsum[-1]) * 100
        
        ax2 = ax.twinx()
        ax2.plot(range(len(sorted_categories)), cumsum_pct, 'ro-', linewidth=2, markersize=8)
        ax2.set_ylabel('累计百分比 (%)', fontsize=self.config.font_size)
        ax2.set_ylim(0, 110)
        
        ax.set_xticks(range(len(sorted_categories)))
        ax.set_xticklabels(sorted_categories)
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class NetworkGraphChart(ChartBase):
    """网络图 - 节点关系展示"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [(0, 1), (1, 2), (2, 3), (3, 0)]
        }
        """
        fig, ax = self._setup_figure()
        
        try:
            import networkx as nx
            
            nodes = data['nodes']
            edges = data['edges']
            
            G = nx.Graph()
            G.add_nodes_from(range(len(nodes)))
            G.add_edges_from(edges)
            
            pos = nx.spring_layout(G)
            
            nx.draw_networkx_nodes(G, pos, node_color=self.primary_color, 
                                  node_size=500, ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax, width=2)
            nx.draw_networkx_labels(G, pos, {i: nodes[i] for i in range(len(nodes))}, 
                                   ax=ax, font_size=10, font_weight='bold')
        except ImportError:
            ax.text(0.5, 0.5, '网络图\n(需要安装 networkx)',
                   ha='center', va='center', fontsize=12,
                   transform=ax.transAxes, style='italic', color='gray')
        
        ax.axis('off')
        return self._to_base64(fig)

class SankeyChart(ChartBase):
    """桑基图 - 流量/能量流向"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'source': [0, 0, 1, 1, 2],
            'target': [2, 3, 2, 3, 3],
            'value': [10, 20, 15, 25, 30],
            'labels': ['A', 'B', 'C', 'D']
        }
        """
        fig, ax = self._setup_figure()
        
        try:
            import plotly.graph_objects as go
            
            fig_plotly = go.Figure(data=[go.Sankey(
                node=dict(label=data['labels']),
                link=dict(
                    source=data['source'],
                    target=data['target'],
                    value=data['value']
                )
            )])
            
            # 转换为 PNG
            img_bytes = fig_plotly.to_image(format='png')
            img_base64 = base64.b64encode(img_bytes).decode()
            return img_base64
        except:
            ax.text(0.5, 0.5, '桑基图\n(需要安装 plotly)',
                   ha='center', va='center', fontsize=12,
                   transform=ax.transAxes, style='italic', color='gray')
            ax.axis('off')
            return self._to_base64(fig)

class GanttChart(ChartBase):
    """甘特图 - 项目进度管理"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'tasks': ['任务A', '任务B', '任务C'],
            'start': [0, 2, 4],
            'duration': [2, 3, 2]
        }
        """
        fig, ax = self._setup_figure()
        
        tasks = data['tasks']
        start = data['start']
        duration = data['duration']
        
        colors_list = self.colors[:len(tasks)]
        
        for i, (task, s, d, color) in enumerate(zip(tasks, start, duration, colors_list)):
            ax.barh(i, d, left=s, height=0.6, color=color, alpha=0.7, edgecolor='black')
            ax.text(s + d/2, i, f'{s}-{s+d}', ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='white')
        
        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels(tasks)
        ax.set_xlabel('时间', fontsize=self.config.font_size)
        ax.set_title('甘特图 - 项目进度', fontsize=self.config.title_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class CalendarHeatmapChart(ChartBase):
    """日历热力图 - 时间序列热力"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'dates': ['2026-01-01', '2026-01-02', ...],
            'values': [10, 20, 15, ...]
        }
        """
        fig, ax = self._setup_figure()
        
        # 简化版本：使用热力图模拟日历
        import calendar
        
        # 创建 7x5 的日历网格
        cal_data = np.random.rand(7, 5) * 100
        
        im = ax.imshow(cal_data, cmap='RdYlGn', aspect='auto')
        
        ax.set_xticks(range(5))
        ax.set_yticks(range(7))
        ax.set_xticklabels(['周1', '周2', '周3', '周4', '周5'])
        ax.set_yticklabels(['一', '二', '三', '四', '五', '六', '日'])
        
        plt.colorbar(im, ax=ax, label='数值')
        
        return self._to_base64(fig)

class CandlestickChart(ChartBase):
    """蜡烛图 - 股票价格走势"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'dates': ['2026-01-01', '2026-01-02', ...],
            'open': [100, 102, 101, ...],
            'high': [105, 107, 106, ...],
            'low': [98, 100, 99, ...],
            'close': [103, 104, 102, ...]
        }
        """
        fig, ax = self._setup_figure()
        
        x = np.arange(len(data['open']))
        width = 0.6
        
        for i in x:
            # 绘制高低线
            ax.plot([i, i], [data['low'][i], data['high'][i]], 'k-', linewidth=1)
            
            # 绘制开收蜡烛
            color = 'green' if data['close'][i] >= data['open'][i] else 'red'
            height = abs(data['close'][i] - data['open'][i])
            bottom = min(data['open'][i], data['close'][i])
            
            ax.bar(i, height, width=width, bottom=bottom, color=color, alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('日期', fontsize=self.config.font_size)
        ax.set_ylabel('价格', fontsize=self.config.font_size)
        ax.set_xticks(x)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class ChoroplethMapChart(ChartBase):
    """分级地图 - 区域数据热力"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        regions = data.get('regions', [])
        values = data.get('values', [])
        
        colors_map = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(values)))
        
        for i, (region, value, color) in enumerate(zip(regions, values, colors_map)):
            ax.bar(i, value, color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        ax.set_xticks(range(len(regions)))
        ax.set_xticklabels(regions, rotation=45, ha='right')
        ax.set_ylabel('数值', fontsize=self.config.font_size)
        ax.set_title('分级地图 - 区域热力', fontsize=self.config.title_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class RouteMapChart(ChartBase):
    """路径地图 - 物流路径规划"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'locations': [(0, 0), (1, 1), (2, 0.5), (3, 1.5)],
            'labels': ['起点', '点A', '点B', '终点']
        }
        """
        fig, ax = self._setup_figure()
        
        locations = data['locations']
        labels = data.get('labels', [f'点{i}' for i in range(len(locations))])
        
        # 绘制路径
        x_coords = [loc[0] for loc in locations]
        y_coords = [loc[1] for loc in locations]
        
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.6)
        
        # 绘制节点
        ax.scatter(x_coords, y_coords, s=200, c=self.colors[:len(locations)], 
                  alpha=0.7, edgecolors='black', linewidth=1.5, zorder=5)
        
        # 添加标签
        for i, (x, y, label) in enumerate(zip(x_coords, y_coords, labels)):
            ax.annotate(label, (x, y), xytext=(5, 5), textcoords='offset points',
                       fontsize=9, fontweight='bold')
        
        ax.set_xlabel('经度', fontsize=self.config.font_size)
        ax.set_ylabel('纬度', fontsize=self.config.font_size)
        ax.set_title('路径地图 - 物流规划', fontsize=self.config.title_size)
        
        self._apply_grid(ax)
        return self._to_base64(fig)

class DotDensityMapChart(ChartBase):
    """点密度地图 - 点分布密度"""
    
    def create(self, data: Dict[str, Any]) -> str:
        fig, ax = self._setup_figure()
        
        x = data.get('x', np.random.rand(500))
        y = data.get('y', np.random.rand(500))
        
        # 使用六边形分桶
        hb = ax.hexbin(x, y, gridsize=15, cmap='YlOrRd', mincnt=1)
        
        ax.set_xlabel('X 坐标', fontsize=self.config.font_size)
        ax.set_ylabel('Y 坐标', fontsize=self.config.font_size)
        ax.set_title('点密度地图', fontsize=self.config.title_size)
        
        plt.colorbar(hb, ax=ax, label='密度')
        return self._to_base64(fig)

class SunburstChart(ChartBase):
    """旭日图 - 多层级占比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'labels': ['总计', '类别A', '类别B', 'A1', 'A2', 'B1'],
            'parents': ['', '总计', '总计', '类别A', '类别A', '类别B'],
            'values': [100, 40, 60, 20, 20, 60]
        }
        """
        fig, ax = self._setup_figure()
        
        try:
            import plotly.graph_objects as go
            
            fig_plotly = go.Figure(go.Sunburst(
                labels=data['labels'],
                parents=data['parents'],
                values=data['values'],
                marker=dict(colors=self.colors)
            ))
            
            img_bytes = fig_plotly.to_image(format='png')
            img_base64 = base64.b64encode(img_bytes).decode()
            return img_base64
        except:
            ax.text(0.5, 0.5, '旭日图\n(需要安装 plotly)',
                   ha='center', va='center', fontsize=12,
                   transform=ax.transAxes, style='italic', color='gray')
            ax.axis('off')
            return self._to_base64(fig)

class WordCloudChart(ChartBase):
    """词云图 - 文本频率可视化"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'words': ['Python', 'Data', 'Analysis', 'Python', 'Data'],
            'frequencies': [10, 8, 6, 10, 8]
        }
        """
        fig, ax = self._setup_figure()
        
        try:
            from wordcloud import WordCloud
            
            words = data['words']
            frequencies = data['frequencies']
            
            word_freq = dict(zip(words, frequencies))
            
            wc = WordCloud(width=self.config.width, height=self.config.height,
                          background_color='white', colormap='viridis').generate_from_frequencies(word_freq)
            
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            
            return self._to_base64(fig)
        except ImportError:
            ax.text(0.5, 0.5, '词云图\n(需要安装 wordcloud)',
                   ha='center', va='center', fontsize=12,
                   transform=ax.transAxes, style='italic', color='gray')
            ax.axis('off')
            return self._to_base64(fig)

class BulletChart(ChartBase):
    """子弹图 - 目标对比"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '销售目标',
            'actual': 75,
            'target': 100,
            'poor': 50,
            'satisfactory': 75,
            'good': 100
        }
        """
        fig, ax = self._setup_figure()
        
        title = data['title']
        actual = data['actual']
        target = data['target']
        poor = data.get('poor', target * 0.5)
        satisfactory = data.get('satisfactory', target * 0.75)
        good = data.get('good', target)
        
        # 绘制背景区域
        ax.barh([0], [poor], height=0.3, color='#FFB3B3', left=0)
        ax.barh([0], [satisfactory - poor], height=0.3, color='#FFD966', left=poor)
        ax.barh([0], [good - satisfactory], height=0.3, color='#92D050', left=satisfactory)
        
        # 绘制实际值
        ax.barh([0], [actual], height=0.15, color='black', left=0)
        
        # 绘制目标线
        ax.plot([target, target], [-0.2, 0.2], 'k-', linewidth=3)
        
        ax.set_xlim(0, good * 1.2)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_xlabel('数值', fontsize=self.config.font_size)
        ax.set_title(title, fontsize=self.config.title_size)
        
        return self._to_base64(fig)

class SmallMultipleChart(ChartBase):
    """小型序列图 - 多个小图表并排"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'charts': [
                {'title': '图1', 'x': [1, 2, 3], 'y': [1, 2, 3]},
                {'title': '图2', 'x': [1, 2, 3], 'y': [3, 2, 1]},
                {'title': '图3', 'x': [1, 2, 3], 'y': [2, 2, 2]}
            ]
        }
        """
        charts = data['charts']
        cols = min(3, len(charts))
        rows = (len(charts) + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(self.config.width/100, rows * 2), dpi=self.config.dpi)
        
        if rows == 1 and cols == 1:
            axes = [axes]
        elif rows == 1 or cols == 1:
            axes = axes.flatten()
        else:
            axes = axes.flatten()
        
        for idx, chart_data in enumerate(charts):
            ax = axes[idx]
            ax.plot(chart_data['x'], chart_data['y'], marker='o', linewidth=2, color=self.primary_color)
            ax.set_title(chart_data['title'], fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        # 隐藏多余的子图
        for idx in range(len(charts), len(axes)):
            axes[idx].axis('off')
        
        fig.tight_layout()
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.config.dpi)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return img_base64

class VisualCanvasChart(ChartBase):
    """视觉对象栏 - 自定义布局"""
    
    def create(self, data: Dict[str, Any]) -> str:
        """
        data = {
            'title': '自定义仪表盘',
            'elements': [
                {'type': 'text', 'content': '标题', 'pos': (0.1, 0.9)},
                {'type': 'metric', 'value': '1,234', 'label': '销售额', 'pos': (0.2, 0.5)}
            ]
        }
        """
        fig = plt.figure(figsize=(self.config.width/100, self.config.height/100), dpi=self.config.dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        title = data.get('title', '自定义仪表盘')
        ax.text(0.5, 0.95, title, ha='center', va='top', fontsize=16,
               transform=ax.transAxes, fontweight='bold')
        
        elements = data.get('elements', [])
        
        for elem in elements:
            elem_type = elem.get('type', 'text')
            pos = elem.get('pos', (0.5, 0.5))
            
            if elem_type == 'text':
                ax.text(pos[0], pos[1], elem.get('content', ''),
                       ha='center', va='center', fontsize=12,
                       transform=ax.transAxes)
            elif elem_type == 'metric':
                ax.text(pos[0], pos[1], elem.get('value', '0'),
                       ha='center', va='center', fontsize=18, fontweight='bold',
                       transform=ax.transAxes, color=self.primary_color)
                ax.text(pos[0], pos[1] - 0.05, elem.get('label', ''),
                       ha='center', va='top', fontsize=10,
                       transform=ax.transAxes)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        return self._to_base64(fig)

# ============================================================================
# 工厂类
# ============================================================================

class ChartFactory:
    """图表工厂 - 统一接口"""
    
    def __init__(self, config: ChartConfig = None):
        self.config = config or ChartConfig()
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.config.theme = Theme[theme.upper()]
    
    def set_title(self, title: str):
        """设置标题"""
        self.config.title = title
    
    # 对比与趋势
    def create_clustered_column(self, data: Dict) -> str:
        return ClusteredColumnChart(self.config).create(data)
    
    def create_stacked_column(self, data: Dict) -> str:
        return StackedColumnChart(self.config).create(data)
    
    def create_percent_stacked_column(self, data: Dict) -> str:
        return PercentStackedColumnChart(self.config).create(data)
    
    def create_clustered_bar(self, data: Dict) -> str:
        return ClusteredBarChart(self.config).create(data)
    
    def create_stacked_bar(self, data: Dict) -> str:
        return StackedBarChart(self.config).create(data)
    
    def create_percent_stacked_bar(self, data: Dict) -> str:
        return PercentStackedBarChart(self.config).create(data)
    
    def create_line(self, data: Dict) -> str:
        return LineChart(self.config).create(data)
    
    def create_smooth_line(self, data: Dict) -> str:
        return SmoothLineChart(self.config).create(data)
    
    def create_combo(self, data: Dict) -> str:
        return ComboChart(self.config).create(data)
    
    def create_area(self, data: Dict) -> str:
        return AreaChart(self.config).create(data)
    
    def create_stacked_area(self, data: Dict) -> str:
        return StackedAreaChart(self.config).create(data)
    
    def create_waterfall(self, data: Dict) -> str:
        return WaterfallChart(self.config).create(data)
    
    # 占比
    def create_pie(self, data: Dict) -> str:
        return PieChart(self.config).create(data)
    
    def create_donut(self, data: Dict) -> str:
        return DonutChart(self.config).create(data)
    
    def create_treemap(self, data: Dict) -> str:
        return TreemapChart(self.config).create(data)
    
    def create_funnel(self, data: Dict) -> str:
        return FunnelChart(self.config).create(data)
    
    # 分布
    def create_scatter(self, data: Dict) -> str:
        return ScatterChart(self.config).create(data)
    
    def create_bubble(self, data: Dict) -> str:
        return BubbleChart(self.config).create(data)
    
    def create_dot(self, data: Dict) -> str:
        return DotChart(self.config).create(data)
    
    def create_high_density_scatter(self, data: Dict) -> str:
        return HighDensityScatterChart(self.config).create(data)
    
    # 地理
    def create_filled_map(self, data: Dict) -> str:
        return FilledMapChart(self.config).create(data)
    
    def create_shape_map(self, data: Dict) -> str:
        return ShapeMapChart(self.config).create(data)
    
    def create_azure_map(self, data: Dict) -> str:
        return AzureMapChart(self.config).create(data)
    
    def create_arcgis_map(self, data: Dict) -> str:
        return ArcGISMapChart(self.config).create(data)
    
    # 指标
    def create_card(self, data: Dict) -> str:
        return CardChart(self.config).create(data)
    
    def create_multi_card(self, data: Dict) -> str:
        return MultiCardChart(self.config).create(data)
    
    def create_kpi(self, data: Dict) -> str:
        return KPIChart(self.config).create(data)
    
    def create_gauge(self, data: Dict) -> str:
        return GaugeChart(self.config).create(data)
    
    def create_target(self, data: Dict) -> str:
        return TargetChart(self.config).create(data)
    
    # AI 分析
    def create_decomposition_tree(self, data: Dict) -> str:
        return DecompositionTreeChart(self.config).create(data)
    
    def create_key_influencers(self, data: Dict) -> str:
        return KeyInfluencersChart(self.config).create(data)
    
    def create_anomaly_detection(self, data: Dict) -> str:
        return AnomalyDetectionChart(self.config).create(data)
    
    def create_smart_narrative(self, data: Dict) -> str:
        return SmartNarrativeChart(self.config).create(data)
    
    # 交互与辅助
    def create_image_visual(self, data: Dict) -> str:
        return ImageVisualChart(self.config).create(data)
    
    def create_text_shape(self, data: Dict) -> str:
        return TextShapeChart(self.config).create(data)
    
    # 统计与分布
    def create_box_plot(self, data: Dict) -> str:
        return BoxPlotChart(self.config).create(data)
    
    def create_histogram(self, data: Dict) -> str:
        return HistogramChart(self.config).create(data)
    
    def create_density_plot(self, data: Dict) -> str:
        return DensityPlotChart(self.config).create(data)
    
    def create_pareto(self, data: Dict) -> str:
        return ParetoChart(self.config).create(data)
    
    # 关系与网络
    def create_network_graph(self, data: Dict) -> str:
        return NetworkGraphChart(self.config).create(data)
    
    def create_sankey(self, data: Dict) -> str:
        return SankeyChart(self.config).create(data)
    
    # 时序与日期
    def create_gantt(self, data: Dict) -> str:
        return GanttChart(self.config).create(data)
    
    def create_calendar_heatmap(self, data: Dict) -> str:
        return CalendarHeatmapChart(self.config).create(data)
    
    def create_candlestick(self, data: Dict) -> str:
        return CandlestickChart(self.config).create(data)
    
    # 地理与热力
    def create_choropleth_map(self, data: Dict) -> str:
        return ChoroplethMapChart(self.config).create(data)
    
    def create_route_map(self, data: Dict) -> str:
        return RouteMapChart(self.config).create(data)
    
    def create_dot_density_map(self, data: Dict) -> str:
        return DotDensityMapChart(self.config).create(data)
    
    # 层级与占比
    def create_sunburst(self, data: Dict) -> str:
        return SunburstChart(self.config).create(data)
    
    def create_word_cloud(self, data: Dict) -> str:
        return WordCloudChart(self.config).create(data)
    
    def create_bullet(self, data: Dict) -> str:
        return BulletChart(self.config).create(data)
    
    # 其他高级
    def create_small_multiple(self, data: Dict) -> str:
        return SmallMultipleChart(self.config).create(data)
    
    def create_visual_canvas(self, data: Dict) -> str:
        return VisualCanvasChart(self.config).create(data)

# ============================================================================
# 使用示例
# ============================================================================

if __name__ == '__main__':
    factory = ChartFactory()
    factory.set_theme('powerbi')
    factory.set_title('季度业绩分析')
    
    # 示例：簇状柱形图
    data = {
        'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
        'series': [
            {'name': '销售额', 'data': [100, 150, 120, 200]},
            {'name': '成本', 'data': [60, 80, 70, 100]}
        ]
    }
    
    chart_b64 = factory.create_clustered_column(data)
    print(f"Chart Base64: {chart_b64[:50]}...")
