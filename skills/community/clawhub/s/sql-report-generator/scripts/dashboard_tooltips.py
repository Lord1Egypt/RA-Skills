"""
dashboard_tooltips.py - 工具提示（Tooltip）功能模块
实现 Power BI 原生的工具提示交互功能

功能说明：
- 鼠标悬停工具提示（Tooltip）交互
- 光标定位至数据点时自动弹出维度、指标及明细信息
- 支持自定义多指标、多图表 tooltip 展示
- 提升数据探查效率
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# 工具提示类型枚举
# ============================================================================

class TooltipType(Enum):
    """工具提示类型"""
    DEFAULT = "default"           # 默认工具提示（自动生成）
    CUSTOM = "custom"             # 自定义工具提示（大厂标配）
    DRILLTHROUGH = "drillthrough" # 钻取型工具提示

class TooltipPosition(Enum):
    """工具提示位置"""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    AUTO = "auto"

# ============================================================================
# 工具提示配置
# ============================================================================

@dataclass
class TooltipField:
    """工具提示字段配置"""
    field_name: str              # 字段名称
    display_name: str            # 显示名称
    format: str = "default"     # 格式化类型：default | currency | percent | number
    precision: int = 0          # 精度（小数位数）
    comparison: bool = False    # 是否显示同比/环比
    background_color: Optional[str] = None  # 背景颜色
    text_color: Optional[str] = None         # 文字颜色

@dataclass
class TooltipStyle:
    """工具提示样式配置"""
    width: int = 280            # 宽度（像素）
    max_height: int = 400       # 最大高度
    background_color: str = "#ffffff"  # 背景颜色
    border_color: str = "#e0e0e0"      # 边框颜色
    border_radius: int = 8      # 边框圆角
    shadow: bool = True         # 是否显示阴影
    font_family: str = "Microsoft YaHei, Segoe UI, sans-serif"
    font_size: int = 12         # 字体大小
    title_size: int = 14        # 标题字体大小
    padding: int = 12           # 内边距
    position: TooltipPosition = TooltipPosition.AUTO
    animation: bool = True      # 是否启用动画

@dataclass
class CustomTooltipContent:
    """自定义工具提示内容配置"""
    title: str                          # 提示标题
    subtitle: Optional[str] = None      # 副标题
    metrics: List[TooltipField] = field(default_factory=list)  # 指标列表
    dimensions: List[str] = field(default_factory=list)         # 维度列表
    table_data: Optional[Dict] = None   # 表格数据（可选）
    chart: Optional[Dict] = None        # 迷你图表（可选）
    conditional_format: Optional[Dict] = None  # 条件格式

@dataclass
class TooltipConfig:
    """
    工具提示（Tooltip）完整配置
    
    业务/开发口语：悬停提示、鼠标悬浮提示、数据点详情弹窗
    
    它到底是什么？
    就是你鼠标悬停（Hover）在图表的某个数据点、柱形、折线点、扇形、气泡上时，
    自动弹出的小浮层，展示：
    - 维度名称（如：2025-10、华东区、商品 A）
    - 指标数值（如：销售额 120 万）
    - 同比 / 环比 / 占比等附加信息
    """
    
    # 基本配置
    enabled: bool = True                    # 是否启用工具提示
    tooltip_type: TooltipType = TooltipType.DEFAULT  # 工具提示类型
    
    # 显示内容配置
    show_dimensions: bool = True             # 显示维度名称
    show_metrics: bool = True                # 显示指标数值
    show_comparison: bool = True             # 显示同比/环比/占比
    show_percentage: bool = True              # 显示占比
    show_ranking: bool = False               # 显示排名
    
    # 延迟配置
    show_delay: int = 200                    # 显示延迟（毫秒）
    hide_delay: int = 500                    # 隐藏延迟（毫秒）
    follow_mouse: bool = True                # 是否跟随鼠标
    
    # 样式配置
    style: TooltipStyle = field(default_factory=TooltipStyle)
    
    # 自定义内容（用于 CUSTOM 类型）
    custom_content: Optional[CustomTooltipContent] = None
    
    # 配套交互
    enable_highlight: bool = True             # 突出显示（点击一个，其他变暗）
    enable_drillthrough: bool = False        # 钻取功能
    enable_filter: bool = True                # 筛选功能（点击数据点，整个页面联动筛选）

# ============================================================================
# 工具提示数据格式
# ============================================================================

def create_default_tooltip_config() -> TooltipConfig:
    """创建默认工具提示配置"""
    return TooltipConfig(
        enabled=True,
        tooltip_type=TooltipType.DEFAULT,
        show_dimensions=True,
        show_metrics=True,
        show_comparison=True,
        show_percentage=True,
        show_ranking=False,
        show_delay=200,
        hide_delay=500,
        follow_mouse=True,
        style=TooltipStyle(),
        enable_highlight=True,
        enable_drillthrough=False,
        enable_filter=True
    )

def create_custom_tooltip_config(
    title: str,
    metrics: List[Dict],
    dimensions: List[str] = None,
    table_data: Dict = None,
    chart: Dict = None
) -> TooltipConfig:
    """
    创建自定义工具提示配置（大厂生产环境标准配置）
    
    生产场景标准描述：
    图表支持 **鼠标悬停工具提示（Tooltip）** 交互，光标定位至数据点时自动弹出维度、指标及明细信息，
    支持自定义多指标、多图表 tooltip 展示，提升数据探查效率。
    
    示例：
    - 悬停显示：2025年10月 | 华东区 | 商品A
    - 指标显示：销售额 ¥1,200,000 | 同比 +15% | 环比 +8% | 占比 12%
    - 表格明细：TOP5 明细列表
    - 迷你图表：迷你趋势图
    """
    custom_content = CustomTooltipContent(
        title=title,
        subtitle=None,
        metrics=[
            TooltipField(
                field_name=m["field"],
                display_name=m["name"],
                format=m.get("format", "default"),
                precision=m.get("precision", 0),
                comparison=m.get("comparison", True)
            ) for m in metrics
        ],
        dimensions=dimensions or [],
        table_data=table_data,
        chart=chart
    )
    
    return TooltipConfig(
        enabled=True,
        tooltip_type=TooltipType.CUSTOM,
        show_dimensions=True,
        show_metrics=True,
        show_comparison=True,
        show_percentage=True,
        show_ranking=True,
        show_delay=150,  # 自定义提示响应更快
        hide_delay=300,
        follow_mouse=True,
        style=TooltipStyle(
            width=320,
            background_color="#fafafa",
            border_color="#1890ff",
            border_radius=8
        ),
        custom_content=custom_content,
        enable_highlight=True,
        enable_drillthrough=True,
        enable_filter=True
    )

# ============================================================================
# 图表工具提示配置模板
# ============================================================================

CHART_TOOLTIP_CONFIGS = {
    # 卡片图工具提示
    "card": create_default_tooltip_config(),
    
    # 折线图工具提示
    "line": create_custom_tooltip_config(
        title="趋势数据详情",
        metrics=[
            {"field": "value", "name": "数值", "format": "number", "precision": 0},
            {"field": "yoy", "name": "同比", "format": "percent", "precision": 1},
            {"field": "mom", "name": "环比", "format": "percent", "precision": 1}
        ],
        dimensions=["date", "category"]
    ),
    
    # 柱形图工具提示
    "column": create_custom_tooltip_config(
        title="柱状数据详情",
        metrics=[
            {"field": "value", "name": "数值", "format": "number", "precision": 0},
            {"field": "target", "name": "目标", "format": "number", "precision": 0},
            {"field": "achievement", "name": "完成率", "format": "percent", "precision": 1}
        ],
        dimensions=["category", "period"]
    ),
    
    # 饼图/圆环图工具提示
    "pie": create_custom_tooltip_config(
        title="占比详情",
        metrics=[
            {"field": "value", "name": "数值", "format": "number", "precision": 0},
            {"field": "percentage", "name": "占比", "format": "percent", "precision": 1},
            {"field": "ranking", "name": "排名", "format": "number", "precision": 0}
        ],
        dimensions=["category"]
    ),
    
    # 散点图工具提示
    "scatter": create_custom_tooltip_config(
        title="分布详情",
        metrics=[
            {"field": "x", "name": "X轴", "format": "number", "precision": 1},
            {"field": "y", "name": "Y轴", "format": "number", "precision": 1},
            {"field": "size", "name": "大小", "format": "number", "precision": 0}
        ],
        dimensions=["label", "category"]
    ),
    
    # 漏斗图工具提示
    "funnel": create_custom_tooltip_config(
        title="转化详情",
        metrics=[
            {"field": "value", "name": "数值", "format": "number", "precision": 0},
            {"field": "conversion", "name": "转化率", "format": "percent", "precision": 1},
            {"field": "drop_off", "name": "流失", "format": "number", "precision": 0}
        ],
        dimensions=["stage"]
    ),
    
    # 地图工具提示
    "map": create_custom_tooltip_config(
        title="区域详情",
        metrics=[
            {"field": "value", "name": "数值", "format": "number", "precision": 0},
            {"field": "percentage", "name": "占比", "format": "percent", "precision": 1},
            {"field": "rank", "name": "排名", "format": "number", "precision": 0}
        ],
        dimensions=["region", "province", "city"]
    ),
    
    # 表格工具提示
    "table": create_default_tooltip_config()
}

# ============================================================================
# 工具提示生成器
# ============================================================================

class TooltipGenerator:
    """工具提示生成器"""
    
    def __init__(self, config: TooltipConfig = None):
        self.config = config or create_default_tooltip_config()
    
    def get_tooltip_config(self, chart_type: str) -> TooltipConfig:
        """获取图表类型的工具提示配置"""
        return CHART_TOOLTIP_CONFIGS.get(chart_type, create_default_tooltip_config())
    
    def generate_tooltip_html(self, data: Dict[str, Any]) -> str:
        """生成工具提示 HTML"""
        if self.config.tooltip_type == TooltipType.DEFAULT:
            return self._generate_default_tooltip(data)
        elif self.config.tooltip_type == TooltipType.CUSTOM:
            return self._generate_custom_tooltip(data)
        return ""
    
    def _generate_default_tooltip(self, data: Dict[str, Any]) -> str:
        """生成默认工具提示"""
        style = self.config.style
        html = f"""
        <div class="tooltip" style="
            width: {style.width}px;
            background: {style.background_color};
            border: 1px solid {style.border_color};
            border-radius: {style.border_radius}px;
            padding: {style.padding}px;
            font-family: {style.font_family};
            font-size: {style.font_size}px;
            box-shadow: {'0 4px 12px rgba(0,0,0,0.15)' if style.shadow else 'none'};
        ">
        """
        # 添加维度
        if self.config.show_dimensions and "dimensions" in data:
            for dim in data["dimensions"]:
                html += f'<div class="tooltip-dim">{dim}</div>'
        
        # 添加指标
        if self.config.show_metrics and "metrics" in data:
            for metric in data["metrics"]:
                html += f'<div class="tooltip-metric">{metric}</div>'
        
        # 添加比较
        if self.config.show_comparison and "comparison" in data:
            html += f'<div class="tooltip-comparison">{data["comparison"]}</div>'
        
        html += "</div>"
        return html
    
    def _generate_custom_tooltip(self, data: Dict[str, Any]) -> str:
        """生成自定义工具提示（大厂标配）"""
        style = self.config.style
        content = self.config.custom_content
        
        html = f"""
        <div class="custom-tooltip" style="
            width: {style.width}px;
            background: {style.background_color};
            border: 1px solid {style.border_color};
            border-radius: {style.border_radius}px;
            padding: {style.padding}px;
            font-family: {style.font_family};
            box-shadow: {'0 8px 24px rgba(0,0,0,0.2)' if style.shadow else 'none'};
        ">
            <div class="tooltip-title" style="
                font-size: {style.title_size}px;
                font-weight: 600;
                margin-bottom: 8px;
                color: #333;
            ">{content.title}</div>
        """
        
        # 添加副标题
        if content.subtitle:
            html += f'<div class="tooltip-subtitle" style="color: #666; margin-bottom: 12px;">{content.subtitle}</div>'
        
        # 添加指标
        html += '<div class="tooltip-metrics">'
        for metric in content.metrics:
            value = data.get(metric.field_name, "-")
            if metric.format == "currency":
                value = f"¥{value:,.0f}"
            elif metric.format == "percent":
                value = f"{value:.1f}%"
            html += f'''
            <div class="tooltip-metric-item" style="display: flex; justify-content: space-between; margin: 4px 0;">
                <span style="color: #666;">{metric.display_name}</span>
                <span style="font-weight: 600; color: #333;">{value}</span>
            </div>
            '''
        html += '</div>'
        
        # 添加表格数据
        if content.table_data and "rows" in content.table_data:
            html += '''
            <div class="tooltip-table" style="margin-top: 12px; border-top: 1px solid #eee; padding-top: 12px;">
                <table style="width: 100%; font-size: 11px;">
            '''
            for row in content.table_data["rows"][:5]:  # 最多显示5行
                html += f'<tr><td>{row[0]}</td><td style="text-align: right;">{row[1]}</td></tr>'
            html += '</table></div>'
        
        html += "</div>"
        return html
    
    def generate_tooltip_js(self) -> str:
        """生成工具提示 JavaScript 代码"""
        return f"""
        // 工具提示配置
        const tooltipConfig = {{
            enabled: {str(self.config.enabled).lower()},
            showDelay: {self.config.show_delay},
            hideDelay: {self.config.hide_delay},
            followMouse: {str(self.config.follow_mouse).lower()},
            showDimensions: {str(self.config.show_dimensions).lower()},
            showMetrics: {str(self.config.show_metrics).lower()},
            showComparison: {str(self.config.show_comparison).lower()},
            showPercentage: {str(self.config.show_percentage).lower()},
            showRanking: {str(self.config.show_ranking).lower()},
            enableHighlight: {str(self.config.enable_highlight).lower()},
            enableDrillthrough: {str(self.config.enable_drillthrough).lower()},
            enableFilter: {str(self.config.enable_filter).lower()},
            style: {{
                width: {self.config.style.width},
                maxHeight: {self.config.style.max_height},
                backgroundColor: '{self.config.style.background_color}',
                borderColor: '{self.config.style.border_color}',
                borderRadius: {self.config.style.border_radius},
                fontFamily: '{self.config.style.font_family}',
                fontSize: {self.config.style.font_size},
                padding: {self.config.style.padding}
            }}
        }};
        
        // 工具提示事件处理
        document.querySelectorAll('.chart-element').forEach(element => {{
            element.addEventListener('mouseenter', showTooltip);
            element.addEventListener('mousemove', moveTooltip);
            element.addEventListener('mouseleave', hideTooltip);
        }});
        
        function showTooltip(event) {{
            const tooltip = document.getElementById('tooltip');
            tooltip.style.display = 'block';
            tooltip.style.opacity = '1';
        }}
        
        function moveTooltip(event) {{
            if (tooltipConfig.followMouse) {{
                const tooltip = document.getElementById('tooltip');
                tooltip.style.left = event.pageX + 10 + 'px';
                tooltip.style.top = event.pageY + 10 + 'px';
            }}
        }}
        
        function hideTooltip(event) {{
            const tooltip = document.getElementById('tooltip');
            tooltip.style.opacity = '0';
            setTimeout(() => {{
                tooltip.style.display = 'none';
            }}, tooltipConfig.hideDelay);
        }}
        """

# ============================================================================
# 使用示例
# ============================================================================

if __name__ == '__main__':
    # 创建默认配置
    default_config = create_default_tooltip_config()
    print("默认工具提示配置:")
    print(f"  - 启用: {default_config.enabled}")
    print(f"  - 显示维度: {default_config.show_dimensions}")
    print(f"  - 显示指标: {default_config.show_metrics}")
    print(f"  - 显示同比/环比: {default_config.show_comparison}")
    
    # 创建自定义配置
    custom_config = create_custom_tooltip_config(
        title="销售数据详情",
        metrics=[
            {"field": "sales", "name": "销售额", "format": "currency", "precision": 0},
            {"field": "yoy", "name": "同比", "format": "percent", "precision": 1},
            {"field": "mom", "name": "环比", "format": "percent", "precision": 1}
        ],
        dimensions=["月份", "地区", "产品"]
    )
    print("\n自定义工具提示配置:")
    print(f"  - 类型: {custom_config.tooltip_type.value}")
    print(f"  - 标题: {custom_config.custom_content.title}")
    print(f"  - 指标数: {len(custom_config.custom_content.metrics)}")
    
    # 使用图表配置
    generator = TooltipGenerator()
    line_config = generator.get_tooltip_config("line")
    print(f"\n折线图工具提示配置:")
    print(f"  - 类型: {line_config.tooltip_type.value}")
    
    # 生成 JavaScript
    js_code = generator.generate_tooltip_js()
    print(f"\n生成的 JavaScript 代码长度: {len(js_code)} 字符")
