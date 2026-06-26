#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI翻译性能深度分析 - 基于监控数据"""

import json
from collections import defaultdict
from datetime import datetime

def load_monitor_data():
    """加载所有监控数据"""
    try:
        with open('translation_monitor.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载监控数据失败: {e}")
        return []

def analyze_single_record(record):
    """分析单条记录"""
    print(f"\n=== 记录 #{record['id']} 详细分析 ===")
    print(f"文件: {record['file_path']}")
    print(f"引擎: {record['engine']}")
    print(f"状态: {record['status']}")
    print(f"时间: {record['timestamp'][:19]}")
    
    # 阶段时间分析
    phases = record['phases']
    total_duration = record['duration']
    
    print(f"\n--- 阶段时间分布 ---")
    sorted_phases = sorted(phases.items(), key=lambda x: x[1].get('duration', 0), reverse=True)
    for phase_name, details in sorted_phases:
        duration = details.get('duration', 0)
        percentage = (duration / total_duration) * 100 if total_duration > 0 else 0
        status = "✓" if details.get('success', False) else "✗"
        print(f"  {status} {phase_name:12}: {duration:6.2f}秒 ({percentage:5.1f}%)")
    
    # 翻译性能指标
    if '翻译执行' in phases:
        translate_time = phases['翻译执行']['duration']
        # 估算字符数（如果有结果统计）
        char_count = 5060  # 默认值
        if 'result_stats' in record and 'characters_processed' in record['result_stats']:
            char_count = record['result_stats']['characters_processed']
        
        speed = char_count / translate_time if translate_time > 0 else 0
        print(f"\n--- 翻译性能指标 ---")
        print(f"  处理字符数: {char_count:,}")
        print(f"  翻译耗时:   {translate_time:.2f}秒")
        print(f"  翻译速度:   {speed:.0f}字符/秒")
        
        # 批次分析（如果有详细信息）
        if 'batch_details' in record.get('result_stats', {}):
            batches = record['result_stats']['batch_details']
            print(f"  批次数量:   {len(batches)}批")
            for i, batch in enumerate(batches, 1):
                print(f"    批次{i}: {batch['count']}条, {batch['chars']}字符, {batch['time']:.2f}秒")

def analyze_history_trends(data):
    """分析历史趋势"""
    if len(data) < 2:
        print("\n--- 历史趋势 ---")
        print("记录不足，无法进行趋势分析")
        return
        
    print("\n=== 历史性能趋势分析 ===")
    
    # 成功率统计
    success_count = len([r for r in data if r.get('success', False)])
    total_count = len(data)
    success_rate = (success_count / total_count) * 100
    
    print(f"总体成功率: {success_rate:.1f}% ({success_count}/{total_count})")
    
    # 引擎使用统计
    engine_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'success': 0})
    for record in data:
        engine = record.get('engine', 'unknown')
        engine_stats[engine]['count'] += 1
        engine_stats[engine]['total_time'] += record.get('duration', 0)
        if record.get('success', False):
            engine_stats[engine]['success'] += 1
    
    print(f"\n--- 引擎性能对比 ---")
    for engine, stats in engine_stats.items():
        avg_time = stats['total_time'] / stats['count']
        success_rate = (stats['success'] / stats['count']) * 100
        print(f"  {engine:8}: 平均{avg_time:5.1f}秒, 成功率{success_rate:5.1f}% ({stats['count']}次)")
    
    # 时间趋势
    print(f"\n--- 时间趋势 ---")
    durations = [r['duration'] for r in data]
    print(f"  最快: {min(durations):.1f}秒")
    print(f"  最慢: {max(durations):.1f}秒")
    print(f"  平均: {sum(durations)/len(durations):.1f}秒")
    
    # 最近5次的趋势
    if len(data) >= 5:
        recent = data[-5:]
        recent_times = [r['duration'] for r in recent]
        print(f"  最近5次平均: {sum(recent_times)/len(recent_times):.1f}秒")

def generate_optimization_suggestions(data):
    """生成优化建议"""
    print(f"\n=== 优化建议 ===")
    
    if not data:
        print("暂无数据，无法生成建议")
        return
        
    latest = data[-1]  # AI翻译时间分析
    ai_time = latest['phases'].get('翻译执行', {}).get('duration', 0)
    total_time = latest['duration']
    
    if ai_time / total_time > 0.9:  # AI翻译占比超过90%
        print("⚠️  AI翻译占比过高 (>90%)")
        print("  建议:")
        print("    1. 考虑使用更快的翻译模型")
        print("    2. 优化批次大小和token限制")
        print("    3. 检查网络连接质量")
    
    # 成功率分析
    success_records = [r for r in data if r.get('success', False)]
    if len(success_records) / len(data) < 0.8:  # 成功率低于80%
        print("⚠️  翻译成功率偏低 (<80%)")
        print("  建议:")
        print("    1. 检查API密钥和网络连接")
        print("    2. 调整超时设置")
        print("    3. 降低单次处理量")
    
    # 性能基准
    avg_time = sum(r['duration'] for r in data) / len(data)
    if avg_time > 60:  # 平均时间超过60秒
        print("⚠️  平均翻译时间较长 (>60秒)")
        print("  建议:")
        print("    1. 减少单次处理的文本量")
        print("    2. 优化预处理和后处理")
        print("    3. 考虑并行处理")
    
    print("\n✅ 持续监控有助于发现更多优化机会")

def analyze_performance():
    """主分析函数"""
    data = load_monitor_data()
    
    if not data:
        print("暂无监控数据")
        return
    
    print("=== AI翻译性能深度分析 ===")
    print(f"总记录数: {len(data)}")
    
    # 分析最新记录
    analyze_single_record(data[-1])
    
    # 历史趋势分析
    analyze_history_trends(data)
    
    # 生成优化建议
    generate_optimization_suggestions(data)
    
    print(f"\n=== 分析完成 ===")
    print(f"下次自动总结: {10 - (len(data) % 10)} 次翻译后")

if __name__ == "__main__":
    analyze_performance()