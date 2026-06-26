#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投放数据分析技能使用示例
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

def usage_example():
    """使用示例"""
    print("🎯 投放数据分析技能使用示例")
    print("=" * 50)
    
    # 1. 基本使用
    print("\n📋 基本使用:")
    print("python main.py --date-range \"2026-01-01:2026-01-31\" --data-dir \"/Users/zhouhao/Documents/投放数据\"")
    
    # 2. 指定指标
    print("\n📊 指定特定指标:")
    print("python main.py --date-range \"2026-01-01:2026-01-31\" \\")
    print("               --metrics \"ROI,观看成本,订单成本,加购成本\" \\")
    print("               --output-format \"html,csv\"")
    
    # 3. 自定义输出
    print("\n📁 自定义输出目录:")
    print("python main.py --date-range \"2026-01-01:2026-01-31\" \\")
    print("               --output-dir \"/Users/zhouhao/Desktop/自定义报告\"")
    
    # 4. 技能特性
    print("\n✨ 技能特性:")
    print("✅ 自动文件识别 - 识别超级直播、淘宝直播、财务三类文件")
    print("✅ 编码自动处理 - 支持GBK、UTF-8等多种编码")
    print("✅ 字段智能映射 - 基于《数据分析基础概念和逻辑v3.md》")
    print("✅ 跨报表分析 - 支持多数据源关联计算")
    print("✅ 数据质量检查 - 自动检测数据问题")
    
    # 5. 输出内容
    print("\n📈 输出内容:")
    print("📊 HTML可视化报告 - 包含数据概览、指标分析、优化建议")
    print("📋 CSV数据汇总 - 各指标的详细计算结果")
    print("🔍 数据质量报告 - 数据完整性检查")
    print("💡 优化建议 - 基于分析结果的业务建议")
    
    # 6. 支持的指标
    print("\n📊 支持的指标:")
    print("• ROI (投入产出比)")
    print("• 观看成本、订单成本、加购成本")
    print("• 转化率、互动率、有效观看率")
    print("• 客单价、笔单价、件单价")
    print("• 业务口径收入、财务口径收入、毛利率")
    
    print("\n🚀 开始使用:")
    print("1. 安装依赖: pip install -r requirements.txt")
    print("2. 运行示例: python main.py --date-range \"2026-01-01:2026-01-31\"")
    print("3. 查看报告: 打开生成的HTML文件")
    
    print("\n✅ 示例完成!")

if __name__ == "__main__":
    usage_example()