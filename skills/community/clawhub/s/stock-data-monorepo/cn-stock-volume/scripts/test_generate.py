#!/usr/bin/env python3
"""
test_generate.py - 测试报告生成（使用实际获取的数据）

使用从同花顺问财实际获取的数据生成测试报告
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 导入 generate_report 模块
sys.path.insert(0, str(Path(__file__).parent))
from generate_report import generate_markdown, generate_json, save_reports

# 实际获取的数据（2026-03-22 测试）
TEST_DATA = {
    'date': '2026-03-22',
    'query_date': '2026-03-22',
    'indices': {
        'shanghai': {
            'point': 3957.05,
            'change': -1.24,
        },
        'shenzhen': {
            'point': 13866.20,
            'change': -0.25,
        },
        'chinext': {
            'point': 3352.10,
            'change': 1.30,
        },
    },
    'sentiment': {
        'up': 662,
        'down': 4786,
        'ratio': '1:7.2',
        'description': '下跌显著多于上涨',
    },
    'volume': {
        'today': None,  # 待用户补充
        'previous': None,  # 待用户补充
    },
    '_from_cache': False,
    'dataSource': 'iwencai',
    'manualDataRequired': ['volume.today', 'volume.previous'],
}


def main():
    print("=" * 60)
    print("📊 cn-stock-volume 测试报告生成")
    print("=" * 60)
    print()
    
    # 生成 Markdown
    print("1️⃣ 生成 Markdown 报告...")
    md_content = generate_markdown(TEST_DATA)
    print("   ✅ Markdown 生成完成")
    print()
    
    # 生成 JSON
    print("2️⃣ 生成 JSON 数据...")
    json_content = generate_json(TEST_DATA)
    print("   ✅ JSON 生成完成")
    print()
    
    # 保存报告
    print("3️⃣ 保存报告...")
    (out_md, out_json), (desk_md, desk_json) = save_reports(TEST_DATA)
    print(f"   ✅ Workspace: {out_md}")
    print(f"   ✅ Desktop: {desk_md}")
    print()
    
    # 打印 Markdown 预览
    print("=" * 60)
    print("📄 Markdown 预览:")
    print("=" * 60)
    print(md_content)
    
    print()
    print("=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
    print()
    print("💡 下一步:")
    print(f"   1. 补充成交量数据:")
    print(f"      python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30")
    print(f"   2. 重新生成报告:")
    print(f"      python3 scripts/generate_report.py 2026-03-22")


if __name__ == '__main__':
    main()
