#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""查看翻译监控记录"""

import json

def view_records():
    try:
        with open('translation_monitor.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"=== 翻译监控记录概览 ===")
        print(f"总记录数: {len(data)}")
        
        # 状态统计
        status_count = {}
        engines = {}
        for record in data:
            status = record.get('status', 'unknown')
            status_count[status] = status_count.get(status, 0) + 1
            
            engine = record.get('engine', 'unknown')
            engines[engine] = engines.get(engine, 0) + 1
        
        print(f"\n状态统计:")
        for status, count in status_count.items():
            print(f"  {status}: {count}次")
            
        print(f"\n引擎使用:")
        for engine, count in engines.items():
            print(f"  {engine}: {count}次")
        
        if data:
            print(f"\n最近记录:")
            for record in data[-3:]:  # 显示最近3条
                print(f"  ID {record['id']}: {record['file_path']} ({record['status']})")
                
    except Exception as e:
        print(f"读取记录失败: {e}")

if __name__ == "__main__":
    view_records()