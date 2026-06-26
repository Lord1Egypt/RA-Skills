"""
指标计算模块 - 基于《数据分析基础概念和逻辑v3.md》文档
"""

import pandas as pd
import numpy as np

class MetricCalculator:
    def __init__(self):
        pass
    
    def calculate_super_metrics(self, df):
        """计算超级直播指标"""
        metrics = {}
        
        # 基础效率指标
        if '花费' in df.columns and '总成交金额' in df.columns:
            metrics['ROI'] = pd.to_numeric(df['总成交金额'], errors='coerce') / pd.to_numeric(df['花费'], errors='coerce').replace(0, np.nan)
        
        if '花费' in df.columns and '直接成交金额' in df.columns:
            metrics['直接ROI'] = pd.to_numeric(df['直接成交金额'], errors='coerce') / pd.to_numeric(df['花费'], errors='coerce').replace(0, np.nan)
        
        # 成本指标
        if '花费' in df.columns and '观看次数' in df.columns:
            metrics['观看成本'] = pd.to_numeric(df['花费'], errors='coerce') / pd.to_numeric(df['观看次数'], errors='coerce').replace(0, np.nan)
        
        if '花费' in df.columns and '总成交笔数' in df.columns:
            metrics['订单成本'] = df['花费'] / df['总成交笔数'].replace(0, np.nan)
        
        if '花费' in df.columns and '直接成交笔数' in df.columns:
            metrics['直接订单成本'] = df['花费'] / df['直接成交笔数'].replace(0, np.nan)
        
        # 加购成本（根据文档公式）
        if '花费' in df.columns and '总收藏数' in df.columns and '总购物车数' in df.columns:
            total_collect_cart = df['总收藏数'] + df['总购物车数']
            metrics['加购成本'] = df['花费'] / total_collect_cart.replace(0, np.nan)
        
        # 转化率指标
        if '展现量' in df.columns and '观看次数' in df.columns:
            metrics['点击率'] = df['观看次数'] / df['展现量'].replace(0, np.nan)
        
        if '展现量' in df.columns and '互动量' in df.columns:
            metrics['互动率'] = df['互动量'] / df['展现量'].replace(0, np.nan)
        
        if '观看次数' in df.columns and '有效观看次数' in df.columns:
            metrics['有效观看率'] = df['有效观看次数'] / df['观看次数'].replace(0, np.nan) * 100
        
        # 千次展现成本
        if '花费' in df.columns and '展现量' in df.columns:
            metrics['千次展现成本'] = (df['花费'] / df['展现量'].replace(0, np.nan)) * 1000
        
        return metrics
    
    def calculate_taobao_metrics(self, df):
        """计算淘宝直播指标"""
        metrics = {}
        
        # 转化率指标
        if '商品点击人数' in df.columns and '成交人数' in df.columns:
            metrics['成交转化率'] = pd.to_numeric(df['成交人数'], errors='coerce') / pd.to_numeric(df['商品点击人数'], errors='coerce').replace(0, np.nan)
        
        if '商品点击人数' in df.columns and '加购人数' in df.columns:
            metrics['加购转化率'] = pd.to_numeric(df['加购人数'], errors='coerce') / pd.to_numeric(df['商品点击人数'], errors='coerce').replace(0, np.nan)
        
        # 价值指标
        if '成交金额' in df.columns and '成交人数' in df.columns:
            metrics['客单价'] = pd.to_numeric(df['成交金额'], errors='coerce') / pd.to_numeric(df['成交人数'], errors='coerce').replace(0, np.nan)
        
        if '成交金额' in df.columns and '成交笔数' in df.columns:
            metrics['笔单价'] = pd.to_numeric(df['成交金额'], errors='coerce') / pd.to_numeric(df['成交笔数'], errors='coerce').replace(0, np.nan)
        
        if '成交金额' in df.columns and '成交件数' in df.columns:
            metrics['件单价'] = pd.to_numeric(df['成交金额'], errors='coerce') / pd.to_numeric(df['成交件数'], errors='coerce').replace(0, np.nan)
        
        # 退款相关指标
        if '退款金额' in df.columns and '成交金额' in df.columns:
            metrics['退款率'] = pd.to_numeric(df['退款金额'], errors='coerce') / pd.to_numeric(df['成交金额'], errors='coerce').replace(0, np.nan)
        
        if '退款订单笔数' in df.columns and '成交订单笔数' in df.columns:
            metrics['退单率'] = pd.to_numeric(df['退款订单笔数'], errors='coerce') / pd.to_numeric(df['成交订单笔数'], errors='coerce').replace(0, np.nan)
        
        return metrics
    
    def calculate_financial_metrics(self, df):
        """计算财务指标"""
        metrics = {}
        
        # 业务口径收入（根据文档公式）
        revenue_components = ['品牌费', '切片', '保量佣金', '预估结算机构佣金', '预估结算线下佣金']
        existing_components = [col for col in revenue_components if col in df.columns]
        
        if existing_components:
            # 确保所有字段都是数值类型
            numeric_df = df[existing_components].apply(pd.to_numeric, errors='coerce')
            metrics['业务口径收入'] = numeric_df.sum(axis=1)
            
            # 财务口径收入
            metrics['财务口径收入'] = metrics['业务口径收入'] / 1.06
        
        # 毛利率
        if '毛利' in df.columns and '财务口径收入' in metrics:
            metrics['毛利率'] = pd.to_numeric(df['毛利'], errors='coerce') / metrics['财务口径收入'].replace(0, np.nan)
        elif '毛利' in df.columns and '业务口径收入' in metrics:
            # 如果没有财务口径收入，使用业务口径收入估算
            estimated_financial_revenue = metrics['业务口径收入'] / 1.06
            metrics['毛利率'] = pd.to_numeric(df['毛利'], errors='coerce') / estimated_financial_revenue.replace(0, np.nan)
        
        return metrics
    
    def cross_report_analysis(self, super_df, taobao_df, financial_df):
        """跨报表关联分析"""
        cross_metrics = {}
        
        # 确保有日期字段用于关联
        super_date_col = next((col for col in super_df.columns if '日期' in str(col)), None)
        taobao_date_col = next((col for col in taobao_df.columns if '日期' in str(col)), None)
        financial_date_col = next((col for col in financial_df.columns if '日期' in str(col)), None)
        
        if super_date_col and taobao_date_col:
            # 合并超级直播和淘宝直播数据
            merged_df = pd.merge(
                super_df, 
                taobao_df, 
                left_on=super_date_col, 
                right_on=taobao_date_col, 
                how='inner',
                suffixes=('_super', '_taobao')
            )
            
            # 超级直播去退ROI参考值（根据文档公式）
            if '总成交金额_super' in merged_df.columns and '退货率_taobao' in merged_df.columns:
                adjusted_revenue = merged_df['总成交金额_super'] * (1 - merged_df['退货率_taobao'])
                cross_metrics['超级直播去退ROI'] = adjusted_revenue / merged_df['花费_super'].replace(0, np.nan)
                cross_metrics['超级直播去退成交金额'] = adjusted_revenue
            
            # 推广投入回报率
            if all(col in merged_df.columns for col in ['花费_super', '总成交笔数_super', '成交笔数_taobao']):
                financial_cols = ['保量佣金', '预估结算线下佣金', '预估结算机构佣金']
                existing_financial_cols = [col for col in financial_cols if col in financial_df.columns]
                
                if existing_financial_cols:
                    # 计算广告成交占比
                    ad_conversion_ratio = merged_df['总成交笔数_super'] / merged_df['成交笔数_taobao'].replace(0, np.nan)
                    
                    # 计算推广投入回报率
                    financial_income = financial_df[existing_financial_cols].sum(axis=1)
                    cross_metrics['推广投入回报率'] = (financial_income * ad_conversion_ratio) / merged_df['花费_super'].replace(0, np.nan)
        
        return cross_metrics
    
    def generate_summary_report(self, metrics_dict):
        """生成指标汇总报告"""
        summary = {}
        
        for metric_type, metrics in metrics_dict.items():
            summary[metric_type] = {}
            for metric_name, values in metrics.items():
                if hasattr(values, 'mean'):  # 如果是Series
                    summary[metric_type][metric_name] = {
                        'mean': values.mean(),
                        'median': values.median(),
                        'min': values.min(),
                        'max': values.max(),
                        'std': values.std()
                    }
                else:
                    summary[metric_type][metric_name] = values
        
        return summary