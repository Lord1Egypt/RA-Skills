#!/usr/bin/env python3
"""
图表生成器
功能：根据质量成本计算结果自动生成图表
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self, calculation_result: Dict):
        """
        初始化图表生成器
        
        Args:
            calculation_result: 质量成本计算结果
        """
        self.calculation_result = calculation_result
        self.charts = {}
        
    def generate_pie_chart(self) -> go.Figure:
        """
        生成饼图 - 质量成本分类占比
        
        Returns:
            Plotly Figure对象
        """
        print("\n正在生成饼图（质量成本分类占比）...")
        
        category_summary = self.calculation_result['category_summary']
        
        categories = [item['category'] for item in category_summary]
        amounts = [item['total_amount'] for item in category_summary]
        percentages = [item['percentage'] for item in category_summary]
        
        # 创建饼图
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=amounts,
            textinfo='label+percent',
            texttemplate='%{label}<br>%{value:,.0f}元<br>%{percent}',
            hovertemplate='<b>%{label}</b><br>金额: %{value:,.0f}元<br>占比: %{percent}<extra></extra>',
            hole=0.3,
            marker=dict(
                colors=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B'],
                line=dict(color='#FFFFFF', width=2)
            )
        )])
        
        fig.update_layout(
            title={
                'text': '质量成本分类占比',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial'}
            },
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            height=500,
            margin=dict(l=20, r=150, t=60, b=20)
        )
        
        self.charts['pie'] = fig
        print("饼图生成完成")
        return fig
    
    def generate_bar_chart(self) -> go.Figure:
        """
        生成柱状图 - 质量成本分类金额对比
        
        Returns:
            Plotly Figure对象
        """
        print("\n正在生成柱状图（质量成本分类金额对比）...")
        
        category_summary = self.calculation_result['category_summary']
        
        categories = [item['category'] for item in category_summary]
        amounts = [item['total_amount'] for item in category_summary]
        
        # 创建柱状图
        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=amounts,
            text=[f'{amt:,.0f}' for amt in amounts],
            textposition='outside',
            marker=dict(
                color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B'],
                line=dict(color='#FFFFFF', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>金额: %{y:,.0f}元<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': '质量成本分类金额对比',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial'}
            },
            xaxis_title='成本分类',
            yaxis_title='金额（元）',
            showlegend=False,
            height=400,
            margin=dict(l=80, r=20, t=60, b=80),
            xaxis=dict(tickangle=-45)
        )
        
        self.charts['bar'] = fig
        print("柱状图生成完成")
        return fig
    
    def generate_line_chart(self) -> Optional[go.Figure]:
        """
        生成折线图 - 质量成本趋势
        
        Returns:
            Plotly Figure对象，如果没有趋势数据则返回None
        """
        trend_data = self.calculation_result.get('trend_data')
        if not trend_data:
            print("\n无趋势数据，跳过折线图生成")
            return None
        
        print("\n正在生成折线图（质量成本趋势）...")
        
        # 整理数据
        periods = sorted(trend_data.keys())
        
        # 获取所有分类
        all_categories = set()
        for period_data in trend_data.values():
            all_categories.update(period_data.keys())
        all_categories = sorted(all_categories)
        
        # 为每个分类创建一条线
        traces = []
        for category in all_categories:
            amounts = [trend_data.get(period, {}).get(category, 0) for period in periods]
            
            trace = go.Scatter(
                x=periods,
                y=amounts,
                mode='lines+markers',
                name=category,
                hovertemplate='<b>%{fullData.name}</b><br>时期: %{x}<br>金额: %{y:,.0f}元<extra></extra>',
                line=dict(width=3),
                marker=dict(size=8)
            )
            traces.append(trace)
        
        # 创建折线图
        fig = go.Figure(data=traces)
        
        fig.update_layout(
            title={
                'text': '质量成本趋势分析',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial'}
            },
            xaxis_title='时期',
            yaxis_title='金额（元）',
            showlegend=True,
            height=500,
            margin=dict(l=80, r=20, t=60, b=80),
            hovermode='x unified'
        )
        
        self.charts['line'] = fig
        print("折线图生成完成")
        return fig
    
    def generate_indicator_chart(self) -> go.Figure:
        """
        生成指标卡片 - 关键指标展示
        
        Returns:
            Plotly Figure对象
        """
        print("\n正在生成指标卡片（关键指标展示）...")
        
        indicators = self.calculation_result['indicators']
        
        # 创建指标卡片的子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('质量成本总额', '损失成本占比', '预防鉴定成本占比', '预防成本'),
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        # 质量成本总额
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=indicators['total_amount'],
                title={"text": "质量成本总额（元）"},
                number={'format': ',.0f', 'font': {'size': 40, 'color': '#2E86AB'}}
            ),
            row=1, col=1
        )
        
        # 损失成本占比
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=indicators['failure_ratio'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "损失成本占比（%）"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#C73E1D"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 60], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ),
            row=1, col=2
        )
        
        # 预防鉴定成本占比
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=indicators['prevention_appraisal_ratio'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "预防鉴定成本占比（%）"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2E86AB"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 60], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 30
                    }
                }
            ),
            row=2, col=1
        )
        
        # 预防成本
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=indicators['prevention_cost'],
                delta={'reference': indicators['total_amount'] * 0.1},
                title={"text": "预防成本（元）"},
                number={'format': ',.0f'}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=60, b=20),
            title={
                'text': '质量成本关键指标',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial'}
            }
        )
        
        self.charts['indicator'] = fig
        print("指标卡片生成完成")
        return fig
    
    def generate_all_charts(self) -> Dict[str, str]:
        """
        生成所有图表并转换为HTML
        
        Returns:
            图表HTML字典
        """
        print("\n开始生成所有图表...")
        
        charts_html = {}
        
        # 生成饼图
        pie_fig = self.generate_pie_chart()
        charts_html['pie'] = pie_fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # 生成柱状图
        bar_fig = self.generate_bar_chart()
        charts_html['bar'] = bar_fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # 生成折线图（如果有趋势数据）
        line_fig = self.generate_line_chart()
        if line_fig:
            charts_html['line'] = line_fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # 生成指标卡片
        indicator_fig = self.generate_indicator_chart()
        charts_html['indicator'] = indicator_fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        print(f"\n共生成 {len(charts_html)} 个图表")
        
        return charts_html
    
    def save_charts(self, output_path: str) -> str:
        """
        保存图表为HTML文件
        
        Args:
            output_path: 输出HTML文件路径
            
        Returns:
            HTML内容
        """
        charts_html = self.generate_all_charts()
        
        # 合并所有图表到一个HTML文件
        combined_html = '<!DOCTYPE html>\n<html>\n<head>\n'
        combined_html += '<meta charset="UTF-8">\n'
        combined_html += '<title>质量成本分析图表</title>\n'
        combined_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n'
        combined_html += '<style>\n'
        combined_html += 'body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }\n'
        combined_html += '.chart-container { background-color: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n'
        combined_html += '</style>\n'
        combined_html += '</head>\n<body>\n'
        combined_html += '<h1 style="text-align: center; color: #333;">质量成本分析图表</h1>\n'
        
        # 添加各个图表
        for chart_type, html in charts_html.items():
            combined_html += f'<div class="chart-container">\n{html}\n</div>\n'
        
        combined_html += '</body>\n</html>'
        
        # 保存文件
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(combined_html)
        
        print(f"\n图表已保存至: {output_path}")
        
        return combined_html


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='质量成本图表生成器')
    parser.add_argument('--result', required=True, help='计算结果文件（.json）')
    parser.add_argument('--output', default='./output/charts.html', help='输出HTML文件路径')
    
    args = parser.parse_args()
    
    try:
        # 读取计算结果
        with open(args.result, 'r', encoding='utf-8') as f:
            calculation_result = json.load(f)
        
        print(f"已读取计算结果")
        
        # 生成图表
        generator = ChartGenerator(calculation_result)
        html = generator.save_charts(args.output)
        
        print("\n" + "="*50)
        print("图表生成完成!")
        print("="*50)
        
        return 0
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
