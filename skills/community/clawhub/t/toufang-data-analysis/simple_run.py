#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版投放数据分析 - 专注于核心功能
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

def simple_analysis():
    """简化分析"""
    print("🎯 简化版投放数据分析")
    print("=" * 50)
    
    data_dir = "/Users/zhouhao/Documents/投放数据"
    
    # 只分析2026年1月数据
    super_file = "/Users/zhouhao/Documents/投放数据/26年/超级直播/2026-01超级直播.csv"
    
    if os.path.exists(super_file):
        print(f"✅ 分析文件: {super_file}")
        
        # 读取数据
        df = pd.read_csv(super_file, encoding='utf-8')
        print(f"✅ 数据读取成功，形状: {df.shape}")
        
        # 核心指标计算
        results = {}
        
        if '花费' in df.columns:
            df['花费'] = pd.to_numeric(df['花费'], errors='coerce')
            results['总花费'] = df['花费'].sum()
            results['平均花费'] = df['花费'].mean()
        
        if '总成交金额' in df.columns:
            df['总成交金额'] = pd.to_numeric(df['总成交金额'], errors='coerce')
            results['总成交金额'] = df['总成交金额'].sum()
        
        if '花费' in df.columns and '总成交金额' in df.columns:
            results['ROI'] = df['总成交金额'].sum() / df['花费'].sum()
        
        if '观看次数' in df.columns:
            df['观看次数'] = pd.to_numeric(df['观看次数'], errors='coerce')
            results['总观看次数'] = df['观看次数'].sum()
            if '花费' in df.columns:
                results['观看成本'] = df['花费'].sum() / df['观看次数'].sum()
        
        if '总成交笔数' in df.columns:
            df['总成交笔数'] = pd.to_numeric(df['总成交笔数'], errors='coerce')
            results['总成交笔数'] = df['总成交笔数'].sum()
            if '花费' in df.columns:
                results['订单成本'] = df['花费'].sum() / df['总成交笔数'].sum()
        
        # 显示结果
        print("\n📊 分析结果:")
        print("=" * 30)
        for key, value in results.items():
            if isinstance(value, float):
                print(f"{key}: {value:,.2f}")
            else:
                print(f"{key}: {value:,}")
        
        # 保存简要报告
        output_file = os.path.expanduser("~/Desktop/投放数据分析简要报告.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("投放数据分析简要报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"数据文件: {super_file}\n")
            f.write(f"数据行数: {len(df):,}\n\n")
            
            f.write("核心指标:\n")
            f.write("-" * 20 + "\n")
            for key, value in results.items():
                if isinstance(value, float):
                    f.write(f"{key}: {value:,.2f}\n")
                else:
                    f.write(f"{key}: {value:,}\n")
        
        print(f"\n✅ 报告已保存到: {output_file}")
        return True
    else:
        print("❌ 文件不存在")
        return False

if __name__ == "__main__":
    simple_analysis()