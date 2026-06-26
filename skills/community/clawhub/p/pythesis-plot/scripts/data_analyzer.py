#!/usr/bin/env python3
"""
数据分析模块
分析数据特征，生成图表建议
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime


class DataAnalyzer:
    """数据分析器"""
    
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = None
        self.columns_info = {}
        self.suggestions = []
        self._load_data()
        self._analyze_columns()
    
    def _load_data(self):
        """加载数据文件"""
        ext = os.path.splitext(self.data_file)[1].lower()
        
        try:
            if ext in ['.csv']:
                self.df = pd.read_csv(self.data_file)
            elif ext in ['.xlsx', '.xls']:
                self.df = pd.read_excel(self.data_file)
            elif ext in ['.txt', '.md']:
                # 尝试读取表格格式
                self.df = pd.read_csv(self.data_file, sep=r'\s+')
            else:
                raise ValueError(f"不支持的文件格式: {ext}")
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            sys.exit(1)
    
    def _analyze_columns(self):
        """分析每列的特征"""
        for col in self.df.columns:
            info = {
                'name': col,
                'dtype': str(self.df[col].dtype),
                'null_count': self.df[col].isnull().sum(),
                'unique_count': self.df[col].nunique(),
            }
            
            # 数值型分析
            if pd.api.types.is_numeric_dtype(self.df[col]):
                info['type'] = 'numeric'
                info['min'] = self.df[col].min()
                info['max'] = self.df[col].max()
                info['mean'] = self.df[col].mean()
                info['std'] = self.df[col].std()
                
            # 时间序列分析
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                info['type'] = 'datetime'
                info['min'] = self.df[col].min()
                info['max'] = self.df[col].max()
                
            # 分类型分析
            else:
                info['type'] = 'categorical'
                # 尝试转换为时间序列
                try:
                    pd.to_datetime(self.df[col])
                    info['could_be_datetime'] = True
                except:
                    info['could_be_datetime'] = False
            
            self.columns_info[col] = info
    
    def _detect_datetime_columns(self):
        """检测可能的时间序列列"""
        datetime_cols = []
        for col, info in self.columns_info.items():
            if info['type'] == 'datetime':
                datetime_cols.append(col)
            elif info.get('could_be_datetime') and info['unique_count'] > 10:
                datetime_cols.append(col)
        return datetime_cols
    
    def _get_numeric_columns(self):
        """获取数值列"""
        return [col for col, info in self.columns_info.items() 
                if info['type'] == 'numeric']
    
    def _get_categorical_columns(self):
        """获取分类列"""
        return [col for col, info in self.columns_info.items() 
                if info['type'] == 'categorical']
    
    def _generate_suggestions(self):
        """生成图表建议"""
        suggestions = []
        
        datetime_cols = self._detect_datetime_columns()
        numeric_cols = self._get_numeric_columns()
        categorical_cols = self._get_categorical_columns()
        
        # 建议1: 时间趋势图
        if datetime_cols and numeric_cols:
            suggestions.append({
                'id': 1,
                'name': '时间趋势分析',
                'type': 'line',
                'description': f'{numeric_cols[0]}随时间变化趋势',
                'x_col': datetime_cols[0],
                'y_col': numeric_cols[0],
                'reason': '时间序列数据，适合展示趋势变化',
                'priority': 'high'
            })
        
        # 建议2: 柱状图对比
        if categorical_cols and numeric_cols:
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]
            
            # 如果类别太多，取Top N
            if self.columns_info[cat_col]['unique_count'] <= 20:
                suggestions.append({
                    'id': 2,
                    'name': '分类对比分析',
                    'type': 'bar',
                    'description': f'各{cat_col}的{num_col}对比',
                    'x_col': cat_col,
                    'y_col': num_col,
                    'reason': '分类数据对比，直观展示差异',
                    'priority': 'high'
                })
        
        # 建议3: 箱线图（如果有分类和数值）
        if categorical_cols and numeric_cols:
            suggestions.append({
                'id': 3,
                'name': '数据分布分析',
                'type': 'box',
                'description': f'{numeric_cols[0]}的分布情况',
                'x_col': categorical_cols[0] if len(categorical_cols) > 1 else None,
                'y_col': numeric_cols[0],
                'reason': '展示数据分布和异常值',
                'priority': 'medium'
            })
        
        # 建议4: 散点图（两个数值列）
        if len(numeric_cols) >= 2:
            # 计算相关性
            corr = self.df[numeric_cols[:5]].corr()
            
            # 找相关性最高的一对
            max_corr = 0
            best_pair = None
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    c = abs(corr.iloc[i, j])
                    if c > max_corr:
                        max_corr = c
                        best_pair = (numeric_cols[i], numeric_cols[j])
            
            if best_pair and max_corr > 0.3:
                suggestions.append({
                    'id': 4,
                    'name': '相关性分析',
                    'type': 'scatter',
                    'description': f'{best_pair[0]}与{best_pair[1]}的相关性',
                    'x_col': best_pair[0],
                    'y_col': best_pair[1],
                    'add_regression': True,
                    'reason': f'两变量相关性较强(r={max_corr:.2f})，适合散点图展示',
                    'priority': 'medium'
                })
        
        # 建议5: 热力图（多个数值列）
        if len(numeric_cols) >= 3:
            suggestions.append({
                'id': 5,
                'name': '相关性矩阵',
                'type': 'heatmap',
                'description': '数值变量间的相关性',
                'cols': numeric_cols[:8],  # 最多8列
                'reason': '多变量相关性分析，热力图最直观',
                'priority': 'medium'
            })
        
        # 建议6: 综合仪表盘（数据维度丰富）
        if len(numeric_cols) >= 2 and (datetime_cols or categorical_cols):
            plots_for_dashboard = []
            
            if datetime_cols and numeric_cols:
                plots_for_dashboard.append({
                    'type': 'line',
                    'title': '趋势分析',
                    'x': datetime_cols[0],
                    'y': numeric_cols[0]
                })
            
            if categorical_cols and numeric_cols:
                plots_for_dashboard.append({
                    'type': 'bar',
                    'title': '分类对比',
                    'x': categorical_cols[0],
                    'y': numeric_cols[0]
                })
            
            if len(numeric_cols) >= 2:
                plots_for_dashboard.append({
                    'type': 'scatter',
                    'title': '相关性',
                    'x': numeric_cols[0],
                    'y': numeric_cols[1]
                })
            
            if len(plots_for_dashboard) >= 2:
                suggestions.append({
                    'id': 6,
                    'name': '综合仪表盘',
                    'type': 'dashboard',
                    'layout': f'{len(plots_for_dashboard//2 + plots_for_dashboard%2)}x2',
                    'plots': plots_for_dashboard,
                    'description': f'{len(plots_for_dashboard)}个维度综合分析',
                    'reason': '数据维度丰富，综合展示更全面',
                    'priority': 'low'
                })
        
        self.suggestions = suggestions
        return suggestions
    
    def generate_report(self):
        """生成分析报告"""
        self._generate_suggestions()
        
        report = []
        report.append("# 数据分析报告\n")
        report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**数据文件**: {os.path.basename(self.data_file)}\n\n")
        
        # 数据概览
        report.append("## 📊 数据概览\n")
        report.append(f"- **数据维度**: {len(self.df)} 行 × {len(self.df.columns)} 列\n")
        report.append(f"- **数值列**: {len(self._get_numeric_columns())} 个\n")
        report.append(f"- **分类列**: {len(self._get_categorical_columns())} 个\n")
        report.append(f"- **时间列**: {len(self._detect_datetime_columns())} 个\n\n")
        
        # 列详情
        report.append("## 📋 列详情\n")
        report.append("| 列名 | 类型 | 唯一值 | 缺失值 | 说明 |\n")
        report.append("|------|------|--------|--------|------|\n")
        
        for col, info in self.columns_info.items():
            type_icon = {"numeric": "🔢", "categorical": "🏷️", "datetime": "📅"}.get(
                info['type'], "❓"
            )
            null_pct = info['null_count'] / len(self.df) * 100
            
            desc = ""
            if info['type'] == 'numeric':
                desc = f"均值={info['mean']:.2f}, 标准差={info['std']:.2f}"
            elif info['type'] == 'categorical':
                desc = f"类别数={info['unique_count']}"
            
            report.append(
                f"| {col} | {type_icon} {info['type']} | "
                f"{info['unique_count']} | {info['null_count']} ({null_pct:.1f}%) | {desc} |\n"
            )
        
        report.append("\n")
        
        # 图表建议
        report.append("## 💡 图表建议\n")
        report.append(f"基于数据特征，为您推荐 **{len(self.suggestions)}** 个图表方案：\n\n")
        
        for suggestion in self.suggestions:
            priority_icon = {"high": "⭐", "medium": "🔹", "low": "▫️"}.get(
                suggestion['priority'], "▫️"
            )
            
            report.append(f"### 方案{suggestion['id']}: {suggestion['name']} {priority_icon}\n")
            report.append(f"- **图表类型**: {suggestion['type']}\n")
            report.append(f"- **展示内容**: {suggestion['description']}\n")
            report.append(f"- **推荐理由**: {suggestion['reason']}\n\n")
        
        # 用户行动指引
        report.append("## 🎯 下一步\n")
        report.append("请告诉我您想要：\n")
        report.append('- **"生成方案1和2"** - 生成指定编号的图表\n')
        report.append('- **"全部生成"** - 生成所有建议的图表\n')
        report.append('- **"修改方案X..."** - 提出您的修改意见（如：修改X轴为...）\n')
        report.append('- **"我要做XXX图"** - 描述您想要的图表\n\n')
        
        return "".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='数据分析工具')
    parser.add_argument('--input', '-i', required=True, help='输入数据文件')
    parser.add_argument('--output', '-o', help='输出报告文件')
    
    args = parser.parse_args()
    
    analyzer = DataAnalyzer(args.input)
    report = analyzer.generate_report()
    
    print(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存: {args.output}")


if __name__ == '__main__':
    main()
