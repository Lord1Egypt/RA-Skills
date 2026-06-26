#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""查看详细翻译记录"""

import json

def view_detailed_record():
    try:
        with open('translation_monitor.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("暂无记录")
            return
            
        # 查看最新记录
        record = data[-1]
        print("=== 最新翻译记录详情 ===")
        print(f"ID: {record['id']}")
        print(f"文件: {record['file_path']}")
        print(f"引擎: {record['engine']}")
        print(f"目标语言: {record['target_lang']}")
        print(f"状态: {record['status']}")
        print(f"总耗时: {record['duration']:.1f}秒")
        print(f"时间戳: {record['timestamp']}")
        
        print("\n各阶段耗时:")
        total_phase_time = 0
        for phase, details in record['phases'].items():
            duration = details.get('duration', 0)
            success = "✓" if details.get('success', False) else "✗"
            print(f"  {success} {phase}: {duration:.2f}秒")
            total_phase_time += duration
            
        print(f"\n阶段总计: {total_phase_time:.2f}秒")
        print(f"记录总计: {record['duration']:.2f}秒")
        
        # 如果有结果统计
        if 'result_stats' in record:
            stats = record['result_stats']
            print(f"\n翻译统计:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"查看记录失败: {e}")

if __name__ == "__main__":
    view_detailed_record()