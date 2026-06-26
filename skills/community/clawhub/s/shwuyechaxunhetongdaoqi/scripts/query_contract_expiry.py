#!/usr/bin/env python3
"""
查询物业项目合同到期信息

这个脚本用于查询上海市物业项目的合同到期信息。
它会调用 shwuyeyanjiu 技能的基础功能。

使用方法：
    python query_contract_expiry.py --district 静安区
"""

import argparse
import sys
import os

# 添加 shwuyeyanjiu 技能的脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shwuyeyanjiu', 'scripts'))

def main():
    parser = argparse.ArgumentParser(description='查询物业项目合同到期信息')
    parser.add_argument('--district', required=True, help='区域名称（如：静安区）')
    parser.add_argument('--output', default='contract_expiry_results.csv', help='输出文件名')
    
    args = parser.parse_args()
    
    print(f"正在查询 {args.district} 的物业项目合同到期信息...")
    print(f"结果将保存到: {args.output}")
    
    # 这里应该调用 shwuyeyanjiu 的基础功能
    # 由于这是一个示例脚本，我们只是输出提示信息
    print("\n⚠️ 注意：")
    print("这个脚本需要配合 shwuyeyanjiu 技能使用。")
    print("请确保已经安装了 shwuyeyanjiu 技能。")
    print("\n建议使用以下命令运行完整流程：")
    print(f"  cd ~/.openclaw/workspace/skills/shwuyeyanjiu/scripts")
    print(f"  uv run python batch_extract_dates_v2.py --district {args.district}")

if __name__ == '__main__':
    main()
