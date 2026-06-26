"""
报表生成模块 - 生成HTML和CSV格式的报告
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_html_report(self, super_df, taobao_df, financial_df, metrics_result, date_range):
        """生成完整的HTML报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"投放数据分析报告_{date_range.replace(':', '_')}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = self._build_html_content(super_df, taobao_df, financial_df, metrics_result, date_range)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _build_html_content(self, super_df, taobao_df, financial_df, metrics_result, date_range):
        """构建HTML内容"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>投放数据分析报告 - {date_range}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1 {{ color: #1a73e8; text-align: center; margin-bottom: 10px; }}
        h2 {{ color: #333; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; margin-top: 30px; }}
        h3 {{ color: #555; margin-top: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; font-size: 14px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: right; }}
        th {{ background-color: #1a73e8; color: white; font-weight: bold; text-align: center; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        tr:hover {{ background-color: #f0f7ff; }}
        .summary {{ background-color: #e7f3ff; font-weight: bold; }}
        .section {{ margin-bottom: 40px; }}
        .note {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107; }}
        .success {{ background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745; }}
        .info-box {{ background-color: #d1ecf1; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #17a2b8; }}
        .timestamp {{ text-align: center; color: #666; font-style: italic; margin-bottom: 30px; }}
        .metric-card {{ background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin: 10px 0; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #1a73e8; }}
        .metric-label {{ color: #666; margin-bottom: 5px; }}
    </style>
</head>
<body>
    <h1>📊 投放数据分析报告</h1>
    <div class="timestamp">日期范围: {date_range} | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    
    <div class="success">
        <h3>✅ 分析完成</h3>
        <p>已成功分析三个数据源，共处理 {self._get_total_rows(super_df, taobao_df, financial_df):,} 行数据</p>
    </div>
    
    <div class="section">
        <h2>📈 数据概览</h2>
        <table>
            <tr><th>数据源</th><th>数据行数</th><th>字段数量</th><th>日期范围</th></tr>
            <tr><td>超级直播</td><td>{len(super_df):,}</td><td>{len(super_df.columns) if not super_df.empty else 0}</td><td>{self._get_date_range(super_df)}</td></tr>
            <tr><td>淘宝直播</td><td>{len(taobao_df):,}</td><td>{len(taobao_df.columns) if not taobao_df.empty else 0}</td><td>{self._get_date_range(taobao_df)}</td></tr>
            <tr><td>财务报表</td><td>{len(financial_df):,}</td><td>{len(financial_df.columns) if not financial_df.empty else 0}</td><td>{self._get_date_range(financial_df)}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>📊 关键指标</h2>
        {self._generate_metrics_html(metrics_result)}
    </div>
    
    <div class="section">
        <h2>🔍 数据样本</h2>
        <h3>超级直播数据（前5行）</h3>
        <pre>{super_df.head().to_string() if not super_df.empty else '无数据'}</pre>
        
        <h3>淘宝直播数据（前5行）</h3>
        <pre>{taobao_df.head().to_string() if not taobao_df.empty else '无数据'}</pre>
        
        <h3>财务报表数据（前5行）</h3>
        <pre>{financial_df.head().to_string() if not financial_df.empty else '无数据'}</pre>
    </div>
    
    <div class="section">
        <h2>💡 优化建议</h2>
        <div class="info-box">
            <h3>基于分析结果的建议</h3>
            {self._generate_recommendations(metrics_result)}
        </div>
    </div>
    
    <div class="section">
        <h2>📋 技术详情</h2>
        <div class="note">
            <p><strong>分析依据:</strong> 基于《数据分析基础概念和逻辑v3.md》文档</p>
            <p><strong>数据处理:</strong> 自动编码检测、字段标准化、数据清洗</p>
            <p><strong>计算公式:</strong> 严格按照文档中的业务规则计算</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_total_rows(self, *dataframes):
        """获取总数据行数"""
        return sum(len(df) for df in dataframes if not df.empty)
    
    def _get_date_range(self, df):
        """获取数据的日期范围"""
        if df.empty:
            return "无数据"
        
        date_cols = [col for col in df.columns if '日期' in str(col)]
        if not date_cols:
            return "无日期字段"
        
        date_col = date_cols[0]
        try:
            dates = pd.to_datetime(df[date_col], errors='coerce')
            valid_dates = dates.dropna()
            if not valid_dates.empty:
                return f"{valid_dates.min().strftime('%Y-%m-%d')} 至 {valid_dates.max().strftime('%Y-%m-%d')}"
        except:
            pass
        
        return "日期格式异常"
    
    def _generate_metrics_html(self, metrics_result):
        """生成指标HTML"""
        html = ""
        
        for metric_type, metrics in metrics_result.items():
            html += f"<h3>{metric_type.upper()} 指标</h3>"
            html += "<div style='display: flex; flex-wrap: wrap; gap: 15px;'>"
            
            for metric_name, values in metrics.items():
                if isinstance(values, dict) and 'mean' in values:
                    # 汇总统计
                    value_html = f"""
                    <div class="metric-card">
                        <div class="metric-label">{metric_name}</div>
                        <div class="metric-value">{values['mean']:,.2f}</div>
                        <div style="font-size: 12px; color: #666;">
                            范围: {values['min']:,.2f} - {values['max']:,.2f}
                        </div>
                    </div>
                    """
                else:
                    # 单个值，确保是标量值
                    if hasattr(values, 'iloc'):
                        # 如果是Series，取第一个值
                        scalar_value = values.iloc[0] if len(values) > 0 else 0
                    else:
                        scalar_value = values
                    
                    value_html = f"""
                    <div class="metric-card">
                        <div class="metric-label">{metric_name}</div>
                        <div class="metric-value">{scalar_value:,.2f}</div>
                    </div>
                    """
                
                html += value_html
            
            html += "</div>"
        
        return html
    
    def _generate_recommendations(self, metrics_result):
        """生成优化建议"""
        recommendations = []
        
        # 基于ROI的建议
        if 'super' in metrics_result and 'ROI' in metrics_result['super']:
            roi = metrics_result['super']['ROI'].get('mean', 0)
            if roi < 2:
                recommendations.append("⚠️ ROI偏低，建议优化投放策略或提高转化率")
            elif roi > 5:
                recommendations.append("✅ ROI表现优秀，可考虑增加投放预算")
        
        # 基于成本的建议
        if 'super' in metrics_result and '观看成本' in metrics_result['super']:
            cost = metrics_result['super']['观看成本'].get('mean', 0)
            if cost > 10:
                recommendations.append("⚠️ 观看成本较高，建议优化创意质量")
        
        # 基于转化率的建议
        if 'taobao' in metrics_result and '成交转化率' in metrics_result['taobao']:
            conversion_rate = metrics_result['taobao']['成交转化率'].get('mean', 0)
            if conversion_rate < 0.02:
                recommendations.append("⚠️ 转化率偏低，建议优化商品选择和话术")
        
        if not recommendations:
            recommendations.append("📊 数据分析完成，建议根据具体业务情况制定优化策略")
        
        return "<ul>" + "".join(f"<li>{rec}</li>" for rec in recommendations) + "</ul>"
    
    def generate_csv_reports(self, metrics_result, date_range):
        """生成CSV格式的报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        files_created = {}
        
        for metric_type, metrics in metrics_result.items():
            filename = f"{metric_type}_指标汇总_{date_range.replace(':', '_')}_{timestamp}.csv"
            filepath = os.path.join(self.output_dir, filename)
            
            # 转换指标数据为DataFrame
            report_data = []
            for metric_name, values in metrics.items():
                if isinstance(values, dict):
                    # 汇总统计
                    row = {'指标': metric_name, **values}
                else:
                    # 单个值
                    row = {'指标': metric_name, '值': values}
                report_data.append(row)
            
            if report_data:
                df = pd.DataFrame(report_data)
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                files_created[metric_type] = filepath
        
        return files_created