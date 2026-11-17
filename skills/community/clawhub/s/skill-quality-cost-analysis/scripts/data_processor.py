#!/usr/bin/env python3
"""
数据处理器 - 质量成本分析
功能：读取Excel/CSV文件，扫描所有sheet，智能识别列，清洗数据
"""

import pandas as pd
import numpy as np
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class DataProcessor:
    """数据处理器，负责读取、识别、清洗质量成本数据"""
    
    # 金额列识别关键词
    AMOUNT_KEYWORDS = ['金额', '费用', '成本', 'price', 'cost', 'amount', 'money', '元', '万元', '千元']
    
    # 日期列识别关键词
    DATE_KEYWORDS = ['日期', '时间', 'date', 'time', '年', '月', 'day']
    
    # 分类列识别关键词
    CATEGORY_KEYWORDS = ['分类', '类别', '类型', 'type', 'category', '项目', '成本项']
    
    # 描述列识别关键词
    DESC_KEYWORDS = ['描述', '说明', '备注', 'remark', 'note', 'description', '内容']
    
    def __init__(self, file_path: str):
        """
        初始化数据处理器
        
        Args:
            file_path: 数据文件路径
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        self.raw_data = {}
        self.cleaned_data = None
        self.column_types = {}
        
    def read_file(self) -> Dict[str, pd.DataFrame]:
        """
        读取文件，支持Excel和CSV
        
        Returns:
            字典，key为sheet名称，value为DataFrame
        """
        file_ext = self.file_path.suffix.lower()
        
        if file_ext in ['.xlsx', '.xls']:
            return self._read_excel()
        elif file_ext == '.csv':
            return self._read_csv()
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}，仅支持 .xlsx, .xls, .csv")
    
    def _read_excel(self) -> Dict[str, pd.DataFrame]:
        """读取Excel文件，扫描所有sheet"""
        print(f"正在读取Excel文件: {self.file_path}")
        
        # 获取所有sheet名称
        xls = pd.ExcelFile(self.file_path)
        sheet_names = xls.sheet_names
        print(f"发现 {len(sheet_names)} 个sheet: {sheet_names}")
        
        data_dict = {}
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                print(f"  Sheet '{sheet_name}': {df.shape[0]} 行, {df.shape[1]} 列")
                
                # 只保留包含数据的sheet
                if df.shape[0] > 0 and df.shape[1] > 0:
                    data_dict[sheet_name] = df
            except Exception as e:
                print(f"  读取 sheet '{sheet_name}' 失败: {e}")
                continue
        
        return data_dict
    
    def _read_csv(self) -> Dict[str, pd.DataFrame]:
        """读取CSV文件"""
        print(f"正在读取CSV文件: {self.file_path}")
        
        try:
            df = pd.read_csv(self.file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(self.file_path, encoding='gbk')
        
        print(f"读取成功: {df.shape[0]} 行, {df.shape[1]} 列")
        
        return {'data': df}
    
    def merge_sheets(self, data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        合并多个sheet的数据
        
        Args:
            data_dict: 多个sheet的数据字典
            
        Returns:
            合并后的DataFrame
        """
        if len(data_dict) == 1:
            # 只有一个sheet，直接返回
            return list(data_dict.values())[0]
        
        print("\n正在合并多个sheet的数据...")
        merged_dfs = []
        
        for sheet_name, df in data_dict.items():
            # 添加来源列，标识数据来自哪个sheet
            df_copy = df.copy()
            df_copy['data_source'] = sheet_name
            merged_dfs.append(df_copy)
        
        merged_df = pd.concat(merged_dfs, ignore_index=True)
        print(f"合并完成: {merged_df.shape[0]} 行, {merged_df.shape[1]} 列")
        
        return merged_df
    
    def identify_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        智能识别列类型
        
        Args:
            df: DataFrame
            
        Returns:
            列类型字典，包含 amount_cols, date_cols, category_cols, desc_cols
        """
        print("\n正在智能识别列类型...")
        
        column_types = {
            'amount_cols': [],
            'date_cols': [],
            'category_cols': [],
            'desc_cols': []
        }
        
        for col in df.columns:
            col_str = str(col).lower()
            
            # 基于列名识别
            if any(keyword in col_str for keyword in self.AMOUNT_KEYWORDS):
                column_types['amount_cols'].append(col)
            elif any(keyword in col_str for keyword in self.DATE_KEYWORDS):
                column_types['date_cols'].append(col)
            elif any(keyword in col_str for keyword in self.CATEGORY_KEYWORDS):
                column_types['category_cols'].append(col)
            elif any(keyword in col_str for keyword in self.DESC_KEYWORDS):
                column_types['desc_cols'].append(col)
        
        # 如果没有找到金额列，尝试基于数据类型识别
        if not column_types['amount_cols']:
            for col in df.columns:
                if col not in column_types['date_cols'] and col not in column_types['category_cols']:
                    # 尝试转换为数值
                    try:
                        numeric_values = pd.to_numeric(df[col], errors='coerce')
                        valid_ratio = numeric_values.notna().sum() / len(df)
                        if valid_ratio > 0.5:  # 超过50%是数值
                            column_types['amount_cols'].append(col)
                            break
                    except:
                        continue
        
        print(f"识别结果:")
        print(f"  金额列: {column_types['amount_cols']}")
        print(f"  日期列: {column_types['date_cols']}")
        print(f"  分类列: {column_types['category_cols']}")
        print(f"  描述列: {column_types['desc_cols']}")
        
        return column_types
    
    def clean_data(self, df: pd.DataFrame, column_types: Dict[str, List[str]]) -> pd.DataFrame:
        """
        清洗数据
        
        Args:
            df: 原始DataFrame
            column_types: 列类型字典
            
        Returns:
            清洗后的DataFrame
        """
        print("\n正在清洗数据...")
        df_cleaned = df.copy()
        
        # 处理金额列
        for col in column_types['amount_cols']:
            if col in df_cleaned.columns:
                # 移除货币符号和逗号
                if df_cleaned[col].dtype == 'object':
                    df_cleaned[col] = df_cleaned[col].astype(str).str.replace(',', '').str.replace('¥', '').str.replace('$', '')
                
                # 转换为数值
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
                
                # 填充空值为0
                df_cleaned[col] = df_cleaned[col].fillna(0)
                
                # 处理异常值（绝对值超过10倍的75分位数视为异常）
                q75 = df_cleaned[col].abs().quantile(0.75)
                if q75 > 0:
                    upper_bound = q75 * 10
                    outliers = df_cleaned[col].abs() > upper_bound
                    if outliers.sum() > 0:
                        print(f"  金额列 '{col}' 发现 {outliers.sum()} 个异常值，已截断处理")
                        df_cleaned.loc[outliers, col] = np.sign(df_cleaned.loc[outliers, col]) * upper_bound
        
        # 处理日期列
        for col in column_types['date_cols']:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
        
        # 处理其他列的空值
        for col in df_cleaned.columns:
            if col not in column_types['amount_cols'] and col not in column_types['date_cols']:
                if df_cleaned[col].isna().sum() > 0:
                    # 对于分类列，填充为"未分类"
                    if col in column_types['category_cols']:
                        df_cleaned[col] = df_cleaned[col].fillna('未分类')
                    # 对于描述列，填充为空字符串
                    elif col in column_types['desc_cols']:
                        df_cleaned[col] = df_cleaned[col].fillna('')
        
        print(f"数据清洗完成: {df_cleaned.shape[0]} 行, {df_cleaned.shape[1]} 列")
        print(f"空值统计:")
        null_stats = df_cleaned.isna().sum()
        for col, count in null_stats.items():
            if count > 0:
                print(f"  {col}: {count} 个空值")
        
        return df_cleaned
    
    def process(self, output_path: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
        """
        执行完整的数据处理流程
        
        Args:
            output_path: 输出文件路径（可选）
            
        Returns:
            (清洗后的DataFrame, 列类型字典)
        """
        # 读取文件
        self.raw_data = self.read_file()
        
        if not self.raw_data:
            raise ValueError("未读取到有效数据")
        
        # 合并sheet
        self.cleaned_data = self.merge_sheets(self.raw_data)
        
        # 识别列类型
        self.column_types = self.identify_columns(self.cleaned_data)
        
        # 清洗数据
        self.cleaned_data = self.clean_data(self.cleaned_data, self.column_types)
        
        # 保存结果
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self.cleaned_data.to_pickle(output_path)
            print(f"\n清洗后的数据已保存至: {output_path}")
        
        return self.cleaned_data, self.column_types


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='质量成本数据处理器')
    parser.add_argument('--file', required=True, help='输入文件路径（Excel或CSV）')
    parser.add_argument('--output', default='./output/cleaned_data.pkl', help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        processor = DataProcessor(args.file)
        df, column_types = processor.process(args.output)
        
        print("\n" + "="*50)
        print("数据处理完成!")
        print("="*50)
        
        return 0
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
