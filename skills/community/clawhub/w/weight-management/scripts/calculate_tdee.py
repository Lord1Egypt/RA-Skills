#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算 TDEE（每日总能量消耗）
使用 Mifflin-St Jeor 公式

安全说明：
- 仅使用标准库（argparse, math）
- 无文件写入操作
- 无网络请求
- 仅内存计算，返回结果
"""

import argparse
import math

def calculate_bmr(weight, height, age, gender):
    """
    计算基础代谢（BMR）
    
    Mifflin-St Jeor 公式：
    男性：BMR = 10×体重 + 6.25×身高 - 5×年龄 + 5
    女性：BMR = 10×体重 + 6.25×身高 - 5×年龄 - 161
    
    参数：
    - weight: 体重（KG）
    - height: 身高（CM）
    - age: 年龄
    - gender: 性别（male/female）
    
    返回：
    - BMR 值（卡/天）
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    return bmr

def calculate_tdee(bmr, activity_level):
    """
    计算 TDEE（每日总能量消耗）
    
    活动系数：
    1.2  = 久坐（几乎不运动）
    1.375 = 轻度活动（每周 1-3 天运动）
    1.55  = 中度活动（每周 3-5 天运动）
    1.725 = 高度活动（每周 6-7 天运动）
    1.9   = 非常活跃（体力劳动）
    
    参数：
    - bmr: 基础代谢
    - activity_level: 活动系数
    
    返回：
    - TDEE 值（卡/天）
    """
    return bmr * activity_level

def main():
    """
    主函数：解析参数，计算并输出结果
    """
    parser = argparse.ArgumentParser(
        description='计算 TDEE（每日总能量消耗）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
安全说明：
- 仅使用标准库（argparse, math）
- 无文件写入操作
- 无网络请求
- 仅内存计算，返回结果
        """
    )
    parser.add_argument('--weight', type=float, required=True, help='体重（KG）')
    parser.add_argument('--height', type=float, required=True, help='身高（CM）')
    parser.add_argument('--age', type=int, required=True, help='年龄')
    parser.add_argument('--gender', type=str, required=True, choices=['male', 'female'], help='性别')
    parser.add_argument('--activity', type=float, default=1.2, help='活动系数（默认 1.2）')
    
    args = parser.parse_args()
    
    # 计算 BMR
    bmr = calculate_bmr(args.weight, args.height, args.age, args.gender)
    
    # 计算 TDEE
    tdee = calculate_tdee(bmr, args.activity)
    
    # 输出结果
    print(f"基础代谢（BMR）：{bmr:.0f} 卡/天")
    print(f"每日总消耗（TDEE）：{tdee:.0f} 卡/天")
    print(f"减重建议摄入：{tdee - 500:.0f} 卡/天（缺口 500 卡）")
    print(f"维持体重摄入：{tdee:.0f} 卡/天")

if __name__ == '__main__':
    main()
