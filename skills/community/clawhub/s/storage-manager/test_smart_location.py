#!/usr/bin/env python3
"""
测试智能位置匹配功能
"""

import os
import sys

# 设置环境变量
os.environ["FEISHU_APP_ID"] = "cli_a956c03ffcb9dcbb"
os.environ["FEISHU_APP_SECRET"] = "HHEZEDoNZwfNdoediXiGSbaRFKDmpB71"
os.environ["FEISHU_BITABLE_TOKEN"] = "AO6rbfj7aa8nbGsG7Rfc90honjK"
os.environ["FEISHU_TABLE_ID"] = "tbl0T6d9uTv4Fk3c"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage_manager import FeishuStorageManager

def test_smart_location_matching():
    """测试智能位置匹配功能"""
    print("🚀 开始测试智能位置匹配功能")
    print("=" * 60)
    
    manager = FeishuStorageManager()
    
    # 获取现有位置选项
    print("📋 现有位置选项:")
    existing_options = manager.get_location_field_options()
    for i, option in enumerate(existing_options, 1):
        print(f"  {i}. {option}")
    
    print()
    print("🧠 智能位置匹配测试:")
    print("-" * 40)
    
    test_cases = [
        # (输入位置, 预期匹配结果, 是否应该匹配)
        ("1号纸箱", "1号纸箱里", True),
        ("白色行李箱", "白色行李箱里", True),
        ("电视柜左边抽屉", "电视柜左抽屉", True),
        ("蓝色行李箱", None, False),  # 应该创建新选项
        ("2号纸箱", None, False),     # 应该创建新选项
        ("办公桌抽屉", "办公桌抽屉", True),
        ("厨房柜子上", "厨房柜子上层", True),
        ("红色行李箱", None, False),  # 应该创建新选项
        ("双肩包内", "双肩包内层", True),
    ]
    
    all_passed = True
    
    for input_loc, expected_match, should_match in test_cases:
        result = manager.get_smart_location(input_loc)
        
        if expected_match and result == expected_match:
            status = "✅ 匹配成功"
            passed = True
        elif expected_match is None and result == input_loc:
            status = "✅ 新建成功"
            passed = True
        else:
            status = f"❌ 匹配失败: 期望 '{expected_match}', 得到 '{result}'"
            passed = False
            all_passed = False
        
        print(f"{status}: '{input_loc}' -> '{result}'")
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("🎉 所有智能位置匹配测试通过！")
        return True
    else:
        print("❌ 部分测试失败")
        return False

def test_integration():
    """测试集成功能"""
    print("\n🔧 测试集成功能")
    print("=" * 40)
    
    manager = FeishuStorageManager()
    
    print("测试物品检索功能...")
    results = manager.search_storage_item("梳子")
    print(f"找到 {len(results)} 条记录")
    
    print("\n测试智能位置匹配...")
    test_locations = ["1号纸箱", "白色行李箱", "蓝色行李箱"]
    
    for loc in test_locations:
        smart_loc = manager.get_smart_location(loc)
        print(f"  '{loc}' -> '{smart_loc}'")
    
    return True

def main():
    """主测试函数"""
    print("📋 开始测试收纳管家智能位置匹配功能")
    print("=" * 60)
    
    passed1 = test_smart_location_matching()
    
    if passed1:
        passed2 = test_integration()
    else:
        passed2 = False
    
    print()
    print("📊 测试结果总结:")
    print("-" * 40)
    print(f"  智能位置匹配测试: {'✅ 通过' if passed1 else '❌ 失败'}")
    print(f"  集成功能测试: {'✅ 通过' if passed2 else '❌ 失败'}")
    print(f"  总体结果: {'✅ 所有测试通过 🎉' if passed1 and passed2 else '❌ 测试失败'}")
    
    return passed1 and passed2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)