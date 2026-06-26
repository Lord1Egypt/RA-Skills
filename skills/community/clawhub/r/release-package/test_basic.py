#!/usr/bin/env python3
"""
基本功能测试
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage_manager import FeishuStorageManager

def test_initialization():
    """测试初始化"""
    print("1. 测试初始化...")
    manager = FeishuStorageManager()
    
    # 测试配置加载
    assert manager.app_id == ""
    assert manager.app_secret == ""
    assert manager.bitable_token == ""
    assert manager.table_id == ""
    
    print("   ✅ 初始化测试通过")

def test_search_function():
    """测试搜索功能（使用环境变量）"""
    print("2. 测试搜索功能...")
    
    # 设置环境变量
    os.environ["FEISHU_APP_ID"] = "cli_a956c03ffcb9dcbb"
    os.environ["FEISHU_APP_SECRET"] = "HHEZEDoNZwfNdoediXiGSbaRFKDmpB71"
    os.environ["FEISHU_BITABLE_TOKEN"] = "AO6rbfj7aa8nbGsG7Rfc90honjK"
    os.environ["FEISHU_TABLE_ID"] = "tbl0T6d9uTv4Fk3c"
    
    manager = FeishuStorageManager()
    
    try:
        results = manager.search_storage_item("梳子")
        print(f"   找到 {len(results)} 条记录")
        
        if results:
            first_result = results[0]
            assert "record_id" in first_result
            assert "fields" in first_result
            
            fields = first_result["fields"]
            assert "AI收纳管家-物品位置记录" in fields
            assert "Location" in fields
            
            print(f"   ✅ 搜索功能测试通过，找到 {len(results)} 条记录")
        else:
            print("   ⚠️ 未找到记录，但API调用成功")
            
    except Exception as e:
        print(f"   ❌ 搜索功能测试失败: {e}")
        raise

def main():
    print("🚀 开始测试收纳管家技能...")
    print("=" * 50)
    
    tests = [
        test_initialization,
        test_search_function
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✅ 所有测试通过！")
        return 0
    else:
        print(f"❌ {total - passed} 项测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())