#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票下载器 - 快速测试脚本
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

# 配置
TEST_DIR = r"Z:\OpenClaw\InvoiceOC"
SCRIPT_DIR = r"C:\Users\admin\.openclaw\workspace\skills\skills\qq-invoice-downloader"

def check_dependencies():
    """检查依赖"""
    print("=" * 60)
    print("📦 依赖检查")
    print("=" * 60)
    
    deps = ['requests', 'playwright', 'pandas', 'openpyxl', 'imap_tools']
    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} (未安装)")

def count_attachments():
    """统计已下载附件"""
    print("\n📊 已下载附件统计")
    print("-" * 60)
    
    results = []
    if not os.path.exists(TEST_DIR):
        print("  ❌ 测试目录不存在")
        return results
    
    for item in sorted(os.listdir(TEST_DIR)):
        item_path = os.path.join(TEST_DIR, item)
        if os.path.isdir(item_path):
            attachments_path = os.path.join(item_path, "attachments")
            if os.path.exists(attachments_path):
                count = len(os.listdir(attachments_path))
                results.append({"name": item, "count": count})
                print(f"  {item}: {count} 个")
    
    if results:
        total = sum(r['count'] for r in results)
        print(f"\n  总计: {total} 个发票")
    
    return results

def test_date_range(date_range: str):
    """测试指定日期范围"""
    print(f"\n📨 测试日期范围: {date_range}")
    print("-" * 60)
    
    script = os.path.join(SCRIPT_DIR, "invoice_downloader_v72.py")
    
    if not os.path.exists(script):
        print(f"  ❌ 脚本不存在: {script}")
        return None
    
    output_dir = os.path.join(TEST_DIR, f"{date_range}_v1")
    if os.path.exists(output_dir):
        attachments = os.path.join(output_dir, "attachments")
        if os.path.exists(attachments):
            existing = len(os.listdir(attachments))
            print(f"  ℹ️ 已有 {existing} 个附件")
    
    print(f"  🚀 运行中...")
    
    try:
        result = subprocess.run(
            [sys.executable, script, date_range],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=SCRIPT_DIR
        )
        
        output = result.stdout + result.stderr
        
        # 提取关键信息
        emails = 0
        success = 0
        failed = 0
        
        for line in output.split('\n'):
            if '封邮件' in line or '封发票' in line:
                import re
                nums = re.findall(r'\d+', line)
                if nums:
                    emails = int(nums[0])
        
        # 检查新下载的文件
        if os.path.exists(output_dir):
            attachments = os.path.join(output_dir, "attachments")
            if os.path.exists(attachments):
                count = len(os.listdir(attachments))
                print(f"  ✅ 完成")
                print(f"     邮件数: {emails}")
                print(f"     附件数: {count}")
                return {"emails": emails, "attachments": count, "status": "success"}
        
        print(f"  ✅ 完成 (邮件: {emails})")
        return {"emails": emails, "status": "success"}
        
    except subprocess.TimeoutExpired:
        print(f"  ❌ 超时")
        return {"status": "timeout"}
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return {"status": "error", "message": str(e)}

def test_edge_cases():
    """边界情况测试"""
    print("\n🔍 边界情况测试")
    print("-" * 60)
    
    # 测试日期范围
    test_ranges = [
        ("无发票日期", "250101-250102"),
        ("单天", "260309-260309"),
        ("近期", "260303-260309"),
    ]
    
    results = []
    for name, date_range in test_ranges:
        print(f"\n  🧪 {name} ({date_range})")
        result = test_date_range(date_range)
        results.append({"name": name, "date_range": date_range, "result": result})
        time.sleep(2)  # 避免过快
    
    return results

def analyze_versions():
    """分析可用版本"""
    print("\n📋 可用版本分析")
    print("-" * 60)
    
    versions = {}
    for f in os.listdir(SCRIPT_DIR):
        if f.startswith("invoice_downloader_v") and f.endswith(".py"):
            version = f.replace("invoice_downloader_", "").replace(".py", "")
            path = os.path.join(SCRIPT_DIR, f)
            size = os.path.getsize(path)
            versions[version] = {"size": size, "path": path}
    
    # 按版本号排序
    sorted_versions = sorted(versions.items(), key=lambda x: x[0], reverse=True)
    
    print("  可用版本:")
    for version, info in sorted_versions:
        size_kb = info['size'] / 1024
        print(f"    {version}: {size_kb:.1f} KB")
    
    return versions

def generate_summary(attachments, edge_results, versions):
    """生成测试摘要"""
    print("\n" + "=" * 60)
    print("📝 测试摘要")
    print("=" * 60)
    
    total_invoices = sum(a['count'] for a in attachments)
    
    print(f"""
  📊 下载统计:
     - 总发票数: {total_invoices}
     - 下载目录: {len(attachments)}
     
  🔍 边界测试:
""")
    
    if edge_results:
        for er in edge_results:
            status = er['result'].get('status', 'unknown') if er['result'] else 'error'
            print(f"     - {er['name']}: {status}")
    
    print(f"""
  📦 版本信息:
     - 最新版本: {list(versions.keys())[0] if versions else 'N/A'}
     - 可用版本: {len(versions)}
""")
    
    # 生成报告
    report = {
        "test_time": datetime.now().isoformat(),
        "total_invoices": total_invoices,
        "download_dirs": len(attachments),
        "attachments": attachments,
        "edge_tests": edge_results,
        "available_versions": list(versions.keys())
    }
    
    report_file = os.path.join(SCRIPT_DIR, "test_summary.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"  📄 报告已保存: test_summary.json")

def main():
    print("\n" + "=" * 60)
    print("🧪 发票下载器测试")
    print("=" * 60)
    
    # 1. 检查依赖
    check_dependencies()
    
    # 2. 统计已下载附件
    attachments = count_attachments()
    
    # 3. 分析版本
    versions = analyze_versions()
    
    # 4. 边界测试
    edge_results = test_edge_cases()
    
    # 5. 生成摘要
    generate_summary(attachments, edge_results, versions)
    
    print("\n✅ 测试完成!")

if __name__ == "__main__":
    main()
