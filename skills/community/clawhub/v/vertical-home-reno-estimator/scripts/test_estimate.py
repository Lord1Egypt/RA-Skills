#!/usr/bin/env python3
"""
住宅装修估算脚本 - 完整测试
"""

import subprocess
import json
import sys
import os

# 切换到脚本目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_cmd(args):
    """运行估算命令"""
    cmd = f"python3 estimate.py {' '.join(str(a) for a in args)}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

def test_case(args, expected_keys=None):
    """测试用例"""
    result = run_cmd(args)
    
    if result.returncode != 0:
        return False, f"命令失败: {result.stderr[:100]}"
    
    try:
        data = json.loads(result.stdout)
        if expected_keys:
            for key in expected_keys:
                if key not in data:
                    return False, f"缺少字段: {key}"
        return True, f"OK - {data.get('总价估算', {}).get('舒适型', 'N/A')}万"
    except json.JSONDecodeError as e:
        return False, f"JSON解析失败: {e}"
    except Exception as e:
        return False, f"错误: {e}"

def test_error_case(args, expected_error):
    """错误用例测试"""
    result = run_cmd(args)
    
    if result.returncode == 0:
        return False, "应该失败但成功了"
    
    try:
        data = json.loads(result.stdout)
        if 'error' not in data:
            return False, "没有error字段"
        if expected_error not in data['error']:
            return False, f"错误信息不匹配: {data['error']}"
        return True, "正确报错"
    except:
        return False, "解析失败"

def main():
    print("=" * 50)
    print("住宅装修估算脚本 - 测试")
    print("=" * 50)
    print()
    
    all_passed = True
    
    # 正常用例
    print("【正常用例】")
    tests = [
        (["100", "精装", "北京"], ["总价估算", "分项估算", "基础信息"]),
        (["80", "简装", "成都"], ["总价估算"]),
        (["150", "豪装", "上海"], ["总价估算"]),
        (["60", "简装", "杭州"], ["总价估算"]),
        (["200", "豪装", "深圳"], ["总价估算"]),
        (["100", "精装", "武汉"], ["总价估算"]),
    ]
    
    for args, expected in tests:
        passed, msg = test_case(args, expected)
        status = "✅" if passed else "❌"
        print(f"  {status} {' '.join(args)}: {msg}")
        if not passed:
            all_passed = False
    
    print()
    print("【边界用例】")
    
    # 边界用例
    edge_tests = [
        (["1000", "精装", "北京"], "面积过大"),
        (["5", "精装", "北京"], "面积过小"),
        (["abc", "精装", "北京"], "面积非数字"),
    ]
    
    for args, desc in edge_tests:
        passed, msg = test_error_case(args, "")
        status = "✅" if passed else "❌"
        print(f"  {status} {desc}: {msg}")
        if not passed:
            all_passed = False
    
    print()
    print("【档次验证】")
    
    # 档次验证
    grade_tests = [
        ["100", "简装", "北京"],
        ["100", "精装", "北京"],
        ["100", "豪装", "北京"],
    ]
    
    for args in grade_tests:
        result = run_cmd(args)
        try:
            data = json.loads(result.stdout)
            grade = data.get("基础信息", {}).get("档次", "")
            expected_grade = args[1]
            if grade == expected_grade:
                print(f"  ✅ 档次正确: {grade}")
            else:
                print(f"  ❌ 档次错误: {grade} != {expected_grade}")
                all_passed = False
        except:
            print(f"  ❌ 解析失败")
            all_passed = False
    
    print()
    print("=" * 50)
    if all_passed:
        print("✅ 全部测试通过")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
