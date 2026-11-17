#!/usr/bin/env python3
"""
质量成本计算器
功能：计算质量成本四大分类（预防、鉴定、内部损失、外部损失）
"""

import pandas as pd
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
import json


class QualityCostCalculator:
    """质量成本计算器"""
    
    # 质量成本四大分类关键词
    PREVENTION_KEYWORDS = ['预防', '培训', '评审', '规划', '预防措施', '质量策划', '质量培训', '预防成本']
    APPRAISAL_KEYWORDS = ['检验', '检测', '试验', '审核', '鉴定', '测量', '测试', '检验成本', '鉴定成本']
    INTERNAL_FAILURE_KEYWORDS = ['报废', '返工', '重做', '停工', '内部', '内部损失', '内部故障', '返修']
    EXTERNAL_FAILURE_KEYWORDS = ['退货', '索赔', '投诉', '售后', '外部', '外部损失', '外部故障', '保修']
    
    def __init__(self, df: pd.DataFrame, column_types: Optional[Dict] = None):
        """
        初始化计算器
        
        Args:
            df: 清洗后的DataFrame
            column_types: 列类型字典（可选）
        """
        self.df = df
        self.column_types = column_types or {}
        self.calculation_result = {}
        
    def classify_quality_cost(self) -> pd.DataFrame:
        """
        对质量成本进行分类
        
        Returns:
            添加了分类列的DataFrame
        """
        print("\n正在进行质量成本分类...")
        
        df = self.df.copy()
        
        # 确定分类列和金额列
        category_col = self.column_types.get('category_cols', ['项目'])[0] if self.column_types.get('category_cols') else None
        amount_cols = self.column_types.get('amount_cols', [])
        
        if not amount_cols:
            raise ValueError("未找到金额列，无法进行计算")
        
        amount_col = amount_cols[0]  # 使用第一个金额列
        
        # 如果有分类列，基于分类列进行分类
        if category_col and category_col in df.columns:
            df['quality_cost_category'] = df[category_col].apply(self._classify_by_category)
        else:
            # 如果没有分类列，基于描述列进行分类
            desc_col = self.column_types.get('desc_cols', [])[0] if self.column_types.get('desc_cols') else None
            if desc_col and desc_col in df.columns:
                df['quality_cost_category'] = df[desc_col].astype(str).apply(self._classify_by_description)
            else:
                # 基于所有文本列进行分类
                text_cols = df.select_dtypes(include=['object']).columns
                if len(text_cols) > 0:
                    # 合并所有文本列的内容
                    df['combined_text'] = df[text_cols].astype(str).agg(' '.join, axis=1)
                    df['quality_cost_category'] = df['combined_text'].apply(self._classify_by_description)
                    df = df.drop('combined_text', axis=1)
                else:
                    # 无法分类，全部归为"未分类"
                    df['quality_cost_category'] = '未分类'
        
        # 统计分类结果
        category_counts = df['quality_cost_category'].value_counts()
        print("分类统计:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} 条记录")
        
        return df
    
    def _classify_by_category(self, category: str) -> str:
        """基于分类名称进行分类"""
        category_lower = str(category).lower()
        
        if any(keyword in category_lower for keyword in self.PREVENTION_KEYWORDS):
            return '预防成本'
        elif any(keyword in category_lower for keyword in self.APPRAISAL_KEYWORDS):
            return '鉴定成本'
        elif any(keyword in category_lower for keyword in self.INTERNAL_FAILURE_KEYWORDS):
            return '内部损失成本'
        elif any(keyword in category_lower for keyword in self.EXTERNAL_FAILURE_KEYWORDS):
            return '外部损失成本'
        else:
            return '未分类'
    
    def _classify_by_description(self, description: str) -> str:
        """基于描述内容进行分类"""
        desc_lower = str(description).lower()
        
        if any(keyword in desc_lower for keyword in self.PREVENTION_KEYWORDS):
            return '预防成本'
        elif any(keyword in desc_lower for keyword in self.APPRAISAL_KEYWORDS):
            return '鉴定成本'
        elif any(keyword in desc_lower for keyword in self.INTERNAL_FAILURE_KEYWORDS):
            return '内部损失成本'
        elif any(keyword in desc_lower for keyword in self.EXTERNAL_FAILURE_KEYWORDS):
            return '外部损失成本'
        else:
            return '未分类'
    
    def calculate_by_category(self, df: pd.DataFrame) -> Dict:
        """
        按分类计算质量成本
        
        Args:
            df: 已分类的DataFrame
            
        Returns:
            分类汇总结果
        """
        print("\n正在计算质量成本...")
        
        amount_col = self.column_types.get('amount_cols', [])[0] if self.column_types.get('amount_cols') else df.select_dtypes(include=['number']).columns[0]
        
        # 按分类汇总
        category_summary = df.groupby('quality_cost_category')[amount_col].agg(['sum', 'count'])
        category_summary = category_summary.reset_index()
        category_summary.columns = ['category', 'total_amount', 'record_count']
        
        # 计算总额
        total_amount = category_summary['total_amount'].sum()
        
        # 计算占比
        category_summary['percentage'] = (category_summary['total_amount'] / total_amount * 100).round(2)
        
        # 按金额降序排序
        category_summary = category_summary.sort_values('total_amount', ascending=False)
        
        print("质量成本汇总:")
        for _, row in category_summary.iterrows():
            print(f"  {row['category']}: {row['total_amount']:,.2f} 元 ({row['percentage']:.2f}%)")
        
        print(f"\n质量成本总额: {total_amount:,.2f} 元")
        
        return {
            'category_summary': category_summary.to_dict('records'),
            'total_amount': float(total_amount)
        }
    
    def calculate_trend(self, df: pd.DataFrame) -> Optional[Dict]:
        """
        计算趋势（如果有日期列）
        
        Args:
            df: DataFrame
            
        Returns:
            趋势数据（如果有）
        """
        date_cols = self.column_types.get('date_cols', [])
        if not date_cols:
            print("\n未找到日期列，跳过趋势分析")
            return None
        
        date_col = date_cols[0]
        if date_col not in df.columns:
            print(f"\n日期列 '{date_col}' 不存在，跳过趋势分析")
            return None
        
        print("\n正在计算趋势...")
        
        amount_col = self.column_types.get('amount_cols', [])[0] if self.column_types.get('amount_cols') else df.select_dtypes(include=['number']).columns[0]
        
        # 提取年月
        df['year_month'] = pd.to_datetime(df[date_col]).dt.to_period('M')
        
        # 按年月和分类汇总
        trend_summary = df.groupby(['year_month', 'quality_cost_category'])[amount_col].sum().reset_index()
        trend_summary.columns = ['period', 'category', 'amount']
        
        # 转换为字典格式
        trend_data = {}
        for period, group in trend_summary.groupby('period'):
            period_str = str(period)
            trend_data[period_str] = {}
            for _, row in group.iterrows():
                trend_data[period_str][row['category']] = float(row['amount'])
        
        print("趋势数据:")
        for period, categories in sorted(trend_data.items()):
            print(f"  {period}:")
            for category, amount in categories.items():
                print(f"    {category}: {amount:,.2f} 元")
        
        return trend_data
    
    def calculate_indicators(self, category_summary: Dict) -> Dict:
        """
        计算关键指标
        
        Args:
            category_summary: 分类汇总结果
            
        Returns:
            指标字典
        """
        print("\n正在计算关键指标...")
        
        total_amount = category_summary['total_amount']
        categories = {item['category']: item for item in category_summary['category_summary']}
        
        # 提取四大分类金额
        prevention_amount = categories.get('预防成本', {}).get('total_amount', 0)
        appraisal_amount = categories.get('鉴定成本', {}).get('total_amount', 0)
        internal_failure_amount = categories.get('内部损失成本', {}).get('total_amount', 0)
        external_failure_amount = categories.get('外部损失成本', {}).get('total_amount', 0)
        
        # 计算损失成本占比
        failure_cost = internal_failure_amount + external_failure_amount
        failure_ratio = (failure_cost / total_amount * 100) if total_amount > 0 else 0
        
        # 计算预防鉴定成本占比
        prevention_appraisal_cost = prevention_amount + appraisal_amount
        prevention_appraisal_ratio = (prevention_appraisal_cost / total_amount * 100) if total_amount > 0 else 0
        
        indicators = {
            'total_amount': total_amount,
            'prevention_cost': prevention_amount,
            'appraisal_cost': appraisal_amount,
            'internal_failure_cost': internal_failure_amount,
            'external_failure_cost': external_failure_amount,
            'failure_cost': failure_cost,
            'failure_ratio': round(failure_ratio, 2),
            'prevention_appraisal_cost': prevention_appraisal_cost,
            'prevention_appraisal_ratio': round(prevention_appraisal_ratio, 2)
        }
        
        print("关键指标:")
        print(f"  质量成本总额: {total_amount:,.2f} 元")
        print(f"  损失成本: {failure_cost:,.2f} 元 ({failure_ratio:.2f}%)")
        print(f"  预防鉴定成本: {prevention_appraisal_cost:,.2f} 元 ({prevention_appraisal_ratio:.2f}%)")
        
        return indicators
    
    def calculate(self, output_path: Optional[str] = None) -> Dict:
        """
        执行完整的计算流程
        
        Args:
            output_path: 输出文件路径（可选）
            
        Returns:
            计算结果字典
        """
        # 分类
        df_classified = self.classify_quality_cost()
        
        # 按分类汇总
        category_summary = self.calculate_by_category(df_classified)
        
        # 计算趋势
        trend_data = self.calculate_trend(df_classified)
        
        # 计算指标
        indicators = self.calculate_indicators(category_summary)
        
        # 整合结果
        self.calculation_result = {
            'category_summary': category_summary['category_summary'],
            'total_amount': category_summary['total_amount'],
            'trend_data': trend_data,
            'indicators': indicators
        }
        
        # 保存结果
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.calculation_result, f, ensure_ascii=False, indent=2)
            print(f"\n计算结果已保存至: {output_path}")
        
        return self.calculation_result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='质量成本计算器')
    parser.add_argument('--data', required=True, help='清洗后的数据文件（.pkl）')
    parser.add_argument('--column-types', help='列类型文件（.json）')
    parser.add_argument('--output', default='./output/calculation_result.json', help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        # 读取数据
        df = pd.read_pickle(args.data)
        print(f"已读取数据: {df.shape[0]} 行, {df.shape[1]} 列")
        
        # 读取列类型（如果有）
        column_types = None
        if args.column_types:
            with open(args.column_types, 'r', encoding='utf-8') as f:
                column_types = json.load(f)
        
        # 计算质量成本
        calculator = QualityCostCalculator(df, column_types)
        result = calculator.calculate(args.output)
        
        print("\n" + "="*50)
        print("质量成本计算完成!")
        print("="*50)
        
        return 0
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
