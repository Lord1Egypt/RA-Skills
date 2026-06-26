#!/usr/bin/env python3
"""
WoL 技能测试脚本
测试所有功能是否正常工作
"""

import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HANDLER = os.path.join(SCRIPT_DIR, 'message_handler.py')

def run_test(name, command, expected_keywords):
    """运行测试并检查结果"""
    print(f"\n{'='*60}")
    print(f"测试：{name}")
    print(f"命令：{command}")
    print('-'*60)
    
    result = subprocess.run(
        ['python3', HANDLER] + command.split(),
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR
    )
    
    output = result.stdout.strip()
    print(f"输出：{output}")
    
    # 检查期望的关键字
    passed = True
    for keyword in expected_keywords:
        if keyword.lower() not in output.lower():
            print(f"❌ 未找到期望的关键字：{keyword}")
            passed = False
    
    if passed:
        print(f"✅ 测试通过")
    else:
        print(f"❌ 测试失败")
    
    return passed

def main():
    print("="*60)
    print("WoL 技能测试套件")
    print("="*60)
    
    tests = [
        ("列出设备（空）", "帮我开机", ["暂无", "设备"]),
        ("添加设备", "添加网络唤醒|00:11:22:33:44:55|测试电脑", ["已添加", "测试电脑"]),
        ("列表设备", "列表", ["测试电脑", "00:11:22:33:44:55"]),
        ("唤醒设备", "开机 - 测试电脑", ["唤醒信号", "测试电脑"]),
        ("删除设备", "删除 - 测试电脑", ["已删除", "测试电脑"]),
        ("验证删除", "列表", ["暂无", "设备"]),
    ]
    
    passed = 0
    failed = 0
    
    for name, command, keywords in tests:
        if run_test(name, command, keywords):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("="*60)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
