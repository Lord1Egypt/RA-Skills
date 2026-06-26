#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投放数据分析技能 - 主程序
基于《数据分析基础概念和逻辑v3.md》开发
"""

import pandas as pd
import numpy as np
import os
import glob
import chardet
from datetime import datetime
import argparse
import sys

# 导入自定义模块
from data_processor import DataProcessor
from calculator import MetricCalculator
from reporter import ReportGenerator
from config import CONFIG

def main():
    """主函数"""
    # 支持ClawHub运行：优先使用环境变量，其次使用命令行参数
    date_range = os.environ.get('TOUFANG_DATE_RANGE')
    data_dir = os.environ.get('TOUFANG_DATA_DIR', CONFIG['DEFAULT_DATA_DIR'])
    metrics = os.environ.get('TOUFANG_METRICS', 'all')
    output_dir = os.environ.get('TOUFANG_OUTPUT_DIR', CONFIG['DEFAULT_OUTPUT_DIR'])
    output_format = os.environ.get('TOUFANG_OUTPUT_FORMAT', 'html')
    
    # 如果没有环境变量，使用命令行参数
    if not date_range:
        parser = argparse.ArgumentParser(description='投放数据分析技能')
        parser.add_argument('--date-range', required=True, help='日期范围，格式: YYYY-MM-DD:YYYY-MM-DD')
        parser.add_argument('--data-dir', default=CONFIG['DEFAULT_DATA_DIR'], help='数据目录路径')
        parser.add_argument('--metrics', default='all', help='需要计算的指标，逗号分隔')
        parser.add_argument('--output-dir', default=CONFIG['DEFAULT_OUTPUT_DIR'], help='输出目录')
        parser.add_argument('--output-format', default='html', help='输出格式: html,csv')
        
        args = parser.parse_args()
        date_range = args.date_range
        data_dir = args.data_dir
        metrics = args.metrics
        output_dir = args.output_dir
        output_format = args.output_format
    
    print("🚀 开始执行投放数据分析技能...")
    print(f"日期范围: {date_range}")
    print(f"数据目录: {data_dir}")
    
    try:
        # 初始化处理器
        processor = DataProcessor(data_dir)
        
        # 自动识别数据文件
        print("📁 正在识别数据文件...")
        super_files, taobao_files, financial_files = processor.auto_detect_files()
        
        if not super_files and not taobao_files and not financial_files:
            print("❌ 未找到任何数据文件")
            return 1
            
        print(f"✅ 找到 {len(super_files)} 个超级直播文件")
        print(f"✅ 找到 {len(taobao_files)} 个淘宝直播文件") 
        print(f"✅ 找到 {len(financial_files)} 个财务文件")
        
        # 读取数据
        print("📊 正在读取数据...")
        super_df = processor.read_data(super_files, 'super')
        taobao_df = processor.read_data(taobao_files, 'taobao')
        financial_df = processor.read_data(financial_files, 'financial')
        
        # 数据预处理
        print("🔄 正在进行数据预处理...")
        super_df = processor.preprocess_data(super_df, 'super')
        taobao_df = processor.preprocess_data(taobao_df, 'taobao')
        financial_df = processor.preprocess_data(financial_df, 'financial')
        
        # 初始化计算器
        calculator = MetricCalculator()
        
        # 计算指标
        print("🧮 正在计算指标...")
        metrics_result = {}
        
        if not super_df.empty:
            metrics_result['super'] = calculator.calculate_super_metrics(super_df)
        if not taobao_df.empty:
            metrics_result['taobao'] = calculator.calculate_taobao_metrics(taobao_df)
        if not financial_df.empty:
            metrics_result['financial'] = calculator.calculate_financial_metrics(financial_df)
        
        # 跨报表关联分析
        if not super_df.empty and not taobao_df.empty and not financial_df.empty:
            cross_metrics = calculator.cross_report_analysis(super_df, taobao_df, financial_df)
            metrics_result['cross'] = cross_metrics
        
        # 生成报告
        print("📝 正在生成报告...")
        reporter = ReportGenerator(output_dir)
        
        # 生成HTML报告
        if 'html' in output_format:
            html_report = reporter.generate_html_report(
                super_df, taobao_df, financial_df, metrics_result, date_range
            )
            print(f"✅ HTML报告已生成: {html_report}")
        
        # 生成CSV报告
        if 'csv' in output_format:
            csv_files = reporter.generate_csv_reports(metrics_result, date_range)
            for file_type, file_path in csv_files.items():
                print(f"✅ {file_type} CSV报告已生成: {file_path}")
        
        print("🎉 投放数据分析完成!")
        return 0
        
    except Exception as e:
        print(f"❌ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())