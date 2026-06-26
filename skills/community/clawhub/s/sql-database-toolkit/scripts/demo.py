"""
sql-dataviz 完整演示脚本
展示所�?24 种图表的使用方法
"""

import sys
import os
from pathlib import Path

# 添加 charts 模块到路�?sys.path.insert(0, str(Path(__file__).parent.parent))

from .charts import ChartFactory, ChartConfig, Theme

def demo_comparison_charts():
    """演示对比与趋势分析类图表"""
    print("\n" + "="*60)
    print("演示 1: 对比与趋势分析类�?种）")
    print("="*60)
    
    factory = ChartFactory()
    factory.set_theme('powerbi')
    
    # 数据
    data = {
        'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
        'series': [
            {'name': '销售额', 'data': [100, 150, 120, 200]},
            {'name': '成本', 'data': [60, 80, 70, 100]}
        ]
    }
    
    # 1. 簇状柱形�?    print("\n1. 簇状柱形�?..")
    chart = factory.create_clustered_column(data)
    save_chart(chart, 'clustered_column.png')
    print("   �?已保�? clustered_column.png")
    
    # 2. 堆积柱形�?    print("2. 堆积柱形�?..")
    chart = factory.create_stacked_column(data)
    save_chart(chart, 'stacked_column.png')
    print("   �?已保�? stacked_column.png")
    
    # 3. 100%堆积柱形�?    print("3. 100%堆积柱形�?..")
    chart = factory.create_percent_stacked_column(data)
    save_chart(chart, 'percent_stacked_column.png')
    print("   �?已保�? percent_stacked_column.png")
    
    # 4. 簇状条形�?    print("4. 簇状条形�?..")
    chart = factory.create_clustered_bar(data)
    save_chart(chart, 'clustered_bar.png')
    print("   �?已保�? clustered_bar.png")
    
    # 5. 折线�?    print("5. 折线�?..")
    chart = factory.create_line(data)
    save_chart(chart, 'line.png')
    print("   �?已保�? line.png")
    
    # 6. 面积�?    print("6. 面积�?..")
    chart = factory.create_area(data)
    save_chart(chart, 'area.png')
    print("   �?已保�? area.png")
    
    # 7. 瀑布�?    print("7. 瀑布�?..")
    waterfall_data = {
        'categories': ['开�?, '收入', '成本', '费用', '结束'],
        'values': [100, 200, -80, -50, 170]
    }
    chart = factory.create_waterfall(waterfall_data)
    save_chart(chart, 'waterfall.png')
    print("   �?已保�? waterfall.png")

def demo_composition_charts():
    """演示部分与整体关系类图表"""
    print("\n" + "="*60)
    print("演示 2: 部分与整体关系类�?种）")
    print("="*60)
    
    factory = ChartFactory()
    factory.set_theme('alibaba')
    
    data = {
        'labels': ['北京', '上海', '广州', '深圳'],
        'values': [35, 25, 25, 15]
    }
    
    # 1. 饼图
    print("\n1. 饼图...")
    chart = factory.create_pie(data)
    save_chart(chart, 'pie.png')
    print("   �?已保�? pie.png")
    
    # 2. 圆环�?    print("2. 圆环�?..")
    chart = factory.create_donut(data)
    save_chart(chart, 'donut.png')
    print("   �?已保�? donut.png")
    
    # 3. 树状�?    print("3. 树状�?..")
    treemap_data = {
        'labels': ['产品A', '产品B', '产品C', '产品D'],
        'sizes': [100, 200, 150, 120],
        'colors': [1, 2, 3, 4]
    }
    chart = factory.create_treemap(treemap_data)
    save_chart(chart, 'treemap.png')
    print("   �?已保�? treemap.png")
    
    # 4. 漏斗�?    print("4. 漏斗�?..")
    funnel_data = {
        'stages': ['访问', '点击', '注册', '购买'],
        'values': [1000, 800, 500, 200]
    }
    chart = factory.create_funnel(funnel_data)
    save_chart(chart, 'funnel.png')
    print("   �?已保�? funnel.png")

def demo_distribution_charts():
    """演示分布与关系分析类图表"""
    print("\n" + "="*60)
    print("演示 3: 分布与关系分析类�?种）")
    print("="*60)
    
    factory = ChartFactory()
    factory.set_theme('tencent')
    
    import numpy as np
    
    # 1. 散点�?    print("\n1. 散点�?..")
    scatter_data = {
        'x': [1, 2, 3, 4, 5, 6, 7, 8],
        'y': [2, 4, 5, 4, 6, 7, 8, 9],
        'labels': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    }
    chart = factory.create_scatter(scatter_data)
    save_chart(chart, 'scatter.png')
    print("   �?已保�? scatter.png")
    
    # 2. 气泡�?    print("2. 气泡�?..")
    bubble_data = {
        'x': [1, 2, 3, 4],
        'y': [2, 4, 5, 4],
        'size': [100, 200, 150, 300],
        'labels': ['A', 'B', 'C', 'D']
    }
    chart = factory.create_bubble(bubble_data)
    save_chart(chart, 'bubble.png')
    print("   �?已保�? bubble.png")
    
    # 3. 点图
    print("3. 点图...")
    dot_data = {
        'categories': ['门店A', '门店B', '门店C', '门店D'],
        'values': [100, 150, 120, 200]
    }
    chart = factory.create_dot(dot_data)
    save_chart(chart, 'dot.png')
    print("   �?已保�? dot.png")
    
    # 4. 高密度散点图
    print("4. 高密度散点图...")
    np.random.seed(42)
    hd_scatter_data = {
        'x': np.random.randn(1000),
        'y': np.random.randn(1000)
    }
    chart = factory.create_high_density_scatter(hd_scatter_data)
    save_chart(chart, 'high_density_scatter.png')
    print("   �?已保�? high_density_scatter.png")

def demo_geographic_charts():
    """演示地理空间类图�?""
    print("\n" + "="*60)
    print("演示 4: 地理空间类（3种）")
    print("="*60)
    
    factory = ChartFactory()
    factory.set_theme('bytedance')
    
    # 1. 填充地图
    print("\n1. 填充地图...")
    map_data = {
        'regions': ['北京', '上海', '广州', '深圳', '杭州'],
        'values': [100, 150, 120, 200, 180]
    }
    chart = factory.create_filled_map(map_data)
    save_chart(chart, 'filled_map.png')
    print("   �?已保�? filled_map.png")
    
    # 2. 形状地图
    print("2. 形状地图...")
    import numpy as np
    shape_data = {
        'x': np.random.rand(50) * 10,
        'y': np.random.rand(50) * 10,
        'size': np.random.rand(50) * 200 + 50,
        'values': np.random.rand(50) * 100
    }
    chart = factory.create_shape_map(shape_data)
    save_chart(chart, 'shape_map.png')
    print("   �?已保�? shape_map.png")
    
    # 3. ArcGIS 地图
    print("3. ArcGIS 地图...")
    chart = factory.create_arcgis_map({})
    save_chart(chart, 'arcgis_map.png')
    print("   �?已保�? arcgis_map.png")

def demo_kpi_charts():
    """演示指标监控类图�?""
    print("\n" + "="*60)
    print("演示 5: 指标监控类（3种）")
    print("="*60)
    
    factory = ChartFactory()
    factory.set_theme('powerbi')
    
    # 1. 卡片�?    print("\n1. 卡片�?..")
    card_data = {
        'title': '日活用户',
        'value': '1,234,567',
        'unit': '�?,
        'change': '+12.5%'
    }
    chart = factory.create_card(card_data)
    save_chart(chart, 'card.png')
    print("   �?已保�? card.png")
    
    # 2. KPI 视觉对象
    print("2. KPI 视觉对象...")
    kpi_data = {
        'title': '年度营收目标',
        'current': 750,
        'target': 1000,
        'unit': '万元'
    }
    chart = factory.create_kpi(kpi_data)
    save_chart(chart, 'kpi.png')
    print("   �?已保�? kpi.png")
    
    # 3. 仪表盘图
    print("3. 仪表盘图...")
    gauge_data = {
        'title': '服务器负�?,
        'value': 65,
        'min': 0,
        'max': 100
    }
    chart = factory.create_gauge(gauge_data)
    save_chart(chart, 'gauge.png')
    print("   �?已保�? gauge.png")

def demo_ai_charts():
    """演示 AI 智能分析类图�?""
    print("\n" + "="*60)
    print("演示 6: AI 智能分析类（4种）")
    print("="*60)
    
    factory = ChartFactory()
    factory.set_theme('powerbi')
    
    # 1. 分解�?    print("\n1. 分解�?..")
    decomp_data = {
        'root': '销售额下降',
        'children': [
            {'name': '产品A', 'value': -30},
            {'name': '产品B', 'value': -20},
            {'name': '产品C', 'value': -10}
        ]
    }
    chart = factory.create_decomposition_tree(decomp_data)
    save_chart(chart, 'decomposition_tree.png')
    print("   �?已保�? decomposition_tree.png")
    
    # 2. 关键影响因素
    print("2. 关键影响因素...")
    influencers_data = {
        'factors': ['价格', '质量', '服务', '品牌'],
        'weights': [0.35, 0.30, 0.20, 0.15]
    }
    chart = factory.create_key_influencers(influencers_data)
    save_chart(chart, 'key_influencers.png')
    print("   �?已保�? key_influencers.png")
    
    # 3. 异常检�?    print("3. 异常检�?..")
    anomaly_data = {
        'x': [1, 2, 3, 4, 5, 6, 7, 8],
        'y': [10, 12, 11, 50, 13, 12, 11, 10],
        'anomalies': [3]
    }
    chart = factory.create_anomaly_detection(anomaly_data)
    save_chart(chart, 'anomaly_detection.png')
    print("   �?已保�? anomaly_detection.png")
    
    # 4. 智能叙事
    print("4. 智能叙事...")
    narrative_data = {
        'title': '月度业绩总结',
        'insights': [
            '销售额环比增长 15%',
            '北京地区贡献最大，占比 35%',
            '新客户转化率达到历史新高'
        ]
    }
    chart = factory.create_smart_narrative(narrative_data)
    save_chart(chart, 'smart_narrative.png')
    print("   �?已保�? smart_narrative.png")

def demo_sql_report_generator():
    """演示报告生成�?""
    print("\n" + "="*60)
    print("演示 7: 报告生成器（表格、矩阵、切片器�?)
    print("="*60)
    
    try:
        from .report_generator import (
            ReportBuilder, TableChart, MatrixChart, SlicerComponent, ButtonNavigator
        )
        
        # 1. 表格
        print("\n1. 生成表格...")
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
        save_chart(table_b64, 'table.png')
        print("   �?已保�? table.png")
        
        # 2. 矩阵
        print("2. 生成矩阵...")
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
        save_chart(matrix_b64, 'matrix.png')
        print("   �?已保�? matrix.png")
        
        # 3. 切片�?        print("3. 生成切片�?..")
        slicer = SlicerComponent()
        slicer_b64 = slicer.create({
            'title': '时间筛�?,
            'options': ['2026-01', '2026-02', '2026-03'],
            'selected': '2026-03'
        })
        save_chart(slicer_b64, 'slicer.png')
        print("   �?已保�? slicer.png")
        
        # 4. 导航按钮
        print("4. 生成导航按钮...")
        navigator = ButtonNavigator()
        nav_b64 = navigator.create({
            'buttons': [
                {'label': '首页', 'active': True},
                {'label': '销售分�?, 'active': False},
                {'label': '财务报表', 'active': False}
            ]
        })
        save_chart(nav_b64, 'navigator.png')
        print("   �?已保�? navigator.png")
        
        # 5. 生成完整报告
        print("5. 生成完整报告...")
        report = ReportBuilder()
        report.set_metadata(
            title='月度业绩报告',
            author='数据分析团队',
            date='2026-03-26'
        )
        
        report.add_title('月度业绩报告', level=1)
        report.add_text('本报告汇总了本月的关键业绩指标和分析洞察�?)
        report.add_title('订单数据', level=2)
        report.add_table('订单列表', table_b64)
        report.add_title('地区分析', level=2)
        report.add_table('地区季度销售额', matrix_b64)
        
        report.export_html('demo_report.html')
        print("   �?已保�? demo_report.html")
        
    except ImportError as e:
        print(f"   �?跳过报告生成演示: {e}")

def save_chart(chart_b64: str, filename: str):
    """保存 base64 图表为文�?""
    import base64
    
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(chart_b64))

def main():
    """主函�?""
    print("\n")
    print("�? + "="*58 + "�?)
    print("�? + " "*58 + "�?)
    print("�? + "  sql-dataviz + sql-report-generator 完整演示".center(58) + "�?)
    print("�? + "  24 �?Power BI 风格图表 + 交互组件".center(58) + "�?)
    print("�? + " "*58 + "�?)
    print("�? + "="*58 + "�?)
    
    try:
        # 演示所有图�?        demo_comparison_charts()
        demo_composition_charts()
        demo_distribution_charts()
        demo_geographic_charts()
        demo_kpi_charts()
        demo_ai_charts()
        demo_sql_report_generator()
        
        print("\n" + "="*60)
        print("�?所有演示完成！")
        print("="*60)
        print("\n输出文件位置: ./output/")
        print("\n生成的文�?")
        print("  - 24 种图�?PNG 文件")
        print("  - 表格、矩阵、切片器、导航按�?)
        print("  - demo_report.html (完整报告)")
        print("\n快速开�?")
        print("  1. 查看 output/ 目录中的 PNG 文件")
        print("  2. 用浏览器打开 demo_report.html")
        print("  3. 参�?SKILL.md 了解更多用法")
        print("\n")
        
    except Exception as e:
        print(f"\n�?演示出错: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
