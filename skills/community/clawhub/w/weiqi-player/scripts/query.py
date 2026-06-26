#!/usr/bin/env python3
"""
围棋选手信息统一查询脚本
同时查询手谈等级分和易查分业余段位

使用方法:
    python3 query.py <姓名>
    python3 query.py --batch 姓名1 姓名2 姓名3
    
示例:
    python3 query.py 张三
    python3 query.py --batch 李四 王五 赵六
"""

import sys
import subprocess
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def query_shoutan(name):
    """调用手谈查询脚本"""
    script_path = os.path.join(SCRIPTS_DIR, "query_shoutan.py")
    try:
        result = subprocess.run(
            ["python3", script_path, name],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"❌ 手谈查询失败: {e}"


def query_yichafen(name):
    """调用易查分查询脚本"""
    script_path = os.path.join(SCRIPTS_DIR, "query_yichafen.py")
    try:
        result = subprocess.run(
            ["python3", script_path, name],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout
    except Exception as e:
        return f"❌ 易查分查询失败: {e}"


def query_single(name):
    """查询单个选手（双平台）"""
    print(f"\n{'='*60}")
    print(f"🔍 正在查询: {name}")
    print(f"{'='*60}\n")
    
    # 查询手谈等级分
    print("【1/2】手谈等级分查询")
    print("-" * 40)
    shoutan_result = query_shoutan(name)
    print(shoutan_result)
    
    # 查询易查分段位
    print("\n【2/2】易查分业余段位查询")
    print("-" * 40)
    yichafen_result = query_yichafen(name)
    print(yichafen_result)
    
    print(f"\n{'='*60}")
    print(f"✅ {name} 查询完成")
    print(f"{'='*60}\n")


def query_batch(names):
    """批量查询多个选手"""
    print(f"\n{'='*60}")
    print(f"🚀 批量查询 {len(names)} 位棋手")
    print(f"名单: {', '.join(names)}")
    print(f"{'='*60}\n")
    
    for i, name in enumerate(names, 1):
        print(f"\n[{i}/{len(names)}] {'='*50}")
        query_single(name)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n【单个查询】")
        print("  python3 query.py <姓名>")
        print("  示例: python3 query.py 张三")
        print("\n【批量查询】")
        print("  python3 query.py --batch 姓名1 姓名2 ...")
        print("  示例: python3 query.py --batch 李四 王五 赵六")
        sys.exit(1)
    
    # 批量模式
    if sys.argv[1] == "--batch":
        names = sys.argv[2:]
        if not names:
            print("❌ 批量查询需要至少一个姓名")
            sys.exit(1)
        query_batch(names)
    else:
        # 单个查询
        query_single(sys.argv[1])


if __name__ == "__main__":
    main()
