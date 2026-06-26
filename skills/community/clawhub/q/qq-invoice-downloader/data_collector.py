#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票下载器 - 持续测试数据收集器
用于长期测试和数据收集
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict

TEST_DIR = r"Z:\OpenClaw\InvoiceOC"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "test_data.json")

@dataclass
class DownloadRecord:
    """下载记录"""
    timestamp: str
    directory: str
    date_range: str
    total_files: int
    pdf_count: int
    zip_count: int
    ofd_count: int
    xml_count: int
    browser_files: int
    total_size_mb: float
    version: str = "unknown"

def analyze_directory(dir_path: str) -> Dict:
    """分析下载目录"""
    attachments_dir = os.path.join(dir_path, "attachments")
    if not os.path.exists(attachments_dir):
        return None
    
    files = os.listdir(attachments_dir)
    
    stats = {
        "total": len(files),
        "pdf": 0,
        "zip": 0,
        "ofd": 0,
        "xml": 0,
        "browser": 0,
        "other": 0,
        "total_size": 0
    }
    
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        file_path = os.path.join(attachments_dir, f)
        size = os.path.getsize(file_path)
        stats["total_size"] += size
        
        if ext == '.pdf':
            if f.startswith('browser_'):
                stats["browser"] += 1
            else:
                stats["pdf"] += 1
        elif ext == '.zip':
            stats["zip"] += 1
        elif ext == '.ofd':
            stats["ofd"] += 1
        elif ext == '.xml':
            stats["xml"] += 1
        else:
            stats["other"] += 1
    
    stats["total_size_mb"] = round(stats["total_size"] / (1024 * 1024), 2)
    return stats

def collect_data():
    """收集所有测试数据"""
    print("📊 收集测试数据...")
    
    records = []
    
    if not os.path.exists(TEST_DIR):
        print(f"❌ 测试目录不存在: {TEST_DIR}")
        return records
    
    for item in sorted(os.listdir(TEST_DIR)):
        item_path = os.path.join(TEST_DIR, item)
        if not os.path.isdir(item_path):
            continue
        
        # 解析日期范围
        if '_v' in item:
            date_range = item.split('_v')[0]
        else:
            date_range = item
        
        # 分析目录
        stats = analyze_directory(item_path)
        if not stats:
            continue
        
        # 获取目录修改时间
        mtime = os.path.getmtime(item_path)
        timestamp = datetime.fromtimestamp(mtime).isoformat()
        
        record = DownloadRecord(
            timestamp=timestamp,
            directory=item,
            date_range=date_range,
            total_files=stats["total"],
            pdf_count=stats["pdf"],
            zip_count=stats["zip"],
            ofd_count=stats["ofd"],
            xml_count=stats["xml"],
            browser_files=stats["browser"],
            total_size_mb=stats["total_size_mb"]
        )
        
        records.append(record)
        print(f"  ✅ {item}: {stats['total']} 个文件 ({stats['total_size_mb']} MB)")
    
    return records

def generate_stats(records: List[DownloadRecord]):
    """生成统计信息"""
    if not records:
        return {}
    
    total_files = sum(r.total_files for r in records)
    total_pdf = sum(r.pdf_count for r in records)
    total_browser = sum(r.browser_files for r in records)
    total_size = sum(r.total_size_mb for r in records)
    
    stats = {
        "total_records": len(records),
        "total_files": total_files,
        "total_pdf": total_pdf,
        "total_browser": total_browser,
        "total_size_mb": round(total_size, 2),
        "avg_files_per_run": round(total_files / len(records), 1),
        "latest_record": records[-1].directory if records else None,
        "first_record": records[0].directory if records else None
    }
    
    return stats

def save_data(records: List[DownloadRecord], stats: Dict):
    """保存数据到JSON"""
    data = {
        "collection_time": datetime.now().isoformat(),
        "test_directory": TEST_DIR,
        "statistics": stats,
        "records": [asdict(r) for r in records]
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 数据已保存: {OUTPUT_FILE}")

def print_summary(stats: Dict):
    """打印摘要"""
    print("\n" + "=" * 60)
    print("📈 数据统计摘要")
    print("=" * 60)
    print(f"""
  测试记录数: {stats['total_records']}
  总文件数: {stats['total_files']}
  总大小: {stats['total_size_mb']} MB
  
  文件类型分布:
    - PDF附件: {stats['total_pdf']}
    - 浏览器下载: {stats['total_browser']}
  
  平均每轮: {stats['avg_files_per_run']} 个文件
  
  最新记录: {stats['latest_record']}
  最早记录: {stats['first_record']}
""")

def main():
    print("=" * 60)
    print("📊 发票下载器 - 数据收集器")
    print("=" * 60)
    
    # 收集数据
    records = collect_data()
    
    if not records:
        print("\n⚠️ 未找到测试数据")
        return
    
    # 生成统计
    stats = generate_stats(records)
    
    # 打印摘要
    print_summary(stats)
    
    # 保存数据
    save_data(records, stats)
    
    print("\n✅ 完成!")

if __name__ == "__main__":
    main()
