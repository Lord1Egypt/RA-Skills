#!/usr/bin/env python3
"""
飞书收纳管家最终CLI接口
支持智能位置匹配和位置图片管理
"""

import os
import sys
import argparse
from typing import Optional

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from final_integrated import FeishuStorageManager, main as init_main
except ImportError:
    # 如果导入失败，使用备用方案
    print("⚠️ 无法导入完整模块，使用简化版")
    
    class FeishuStorageManager:
        def __init__(self):
            print("简化版管理器")
        
        def initialize(self):
            print("初始化简化版")
            return True
        
        def add_storage_item(self, item_name, location, item_image_path=None):
            print(f"添加物品: {item_name} -> {location}")
            return {"status": "simulated_success"}

def add_item(args):
    """添加物品命令"""
    print(f"📦 添加物品: {args.item} -> {args.location}")
    
    manager = FeishuStorageManager()
    if not manager.initialize():
        print("❌ 系统初始化失败")
        return 1
    
    result = manager.add_storage_item(
        item_name=args.item,
        location=args.location,
        item_image_path=args.image
    )
    
    if result["status"] == "needs_location_photo":
        print(f"\n📸 需要位置拍照!")
        print(f"   位置: {result['location']}")
        print(f"   下一步: {result['next_step']}")
        print(f"\n请使用以下命令上传位置图片:")
        print(f"  storage-manager add-location-photo \"{result['location']}\" --image=\"位置图片路径\"")
        return 2
    elif result["status"] == "success":
        print(f"\n✅ 物品入库成功!")
        print(f"   物品: {result['item']}")
        print(f"   位置: {result['location']}")
        if result["is_new_location"]:
            print(f"   📍 新位置: 是")
        if result.get("has_location_image"):
            print(f"   📷 有位置图片: 是")
        return 0
    else:
        print(f"\n❌ 入库失败: {result.get('message', '未知错误')}")
        return 1

def add_location_photo(args):
    """添加位置图片命令"""
    print(f"📷 为位置添加图片: {args.location}")
    
    manager = FeishuStorageManager()
    if not manager.initialize():
        print("❌ 系统初始化失败")
        return 1
    
    if not args.image or not os.path.exists(args.image):
        print(f"❌ 图片文件不存在: {args.image}")
        return 1
    
    result = manager.add_location_photo(
        location=args.location,
        image_path=args.image
    )
    
    if result["status"] == "success":
        print(f"\n✅ 位置图片添加成功!")
        print(f"   位置: {result['location']}")
        print(f"   文件token: {result['file_token']}")
        print(f"   消息: {result['message']}")
        
        print(f"\n现在可以重新添加物品到该位置:")
        print(f"  storage-manager add \"物品名称\" \"{args.location}\"")
        return 0
    else:
        print(f"\n❌ 位置图片添加失败: {result.get('message', '未知错误')}")
        return 1

def search_item(args):
    """搜索物品命令"""
    print(f"🔍 搜索物品: {args.item}")
    
    # 这里需要实现搜索功能
    print("搜索功能正在开发中...")
    return 0

def update_location(args):
    """更新位置命令"""
    print(f"🔄 更新位置: {args.item} -> {args.new_location}")
    
    # 这里需要实现更新功能
    print("更新功能正在开发中...")
    return 0

def test_match(args):
    """测试位置匹配命令"""
    print(f"🧪 测试位置匹配: {args.location}")
    
    manager = FeishuStorageManager()
    if not manager.initialize():
        print("❌ 系统初始化失败")
        return 1
    
    # 模拟添加物品来测试匹配
    result = manager.add_storage_item(
        item_name="测试物品",
        location=args.location,
        item_image_path=None
    )
    
    if result["status"] == "needs_location_photo":
        print(f"✅ 测试结果: 新位置需要拍照")
        print(f"   匹配位置: {result['location']}")
    elif result["status"] == "success":
        print(f"✅ 测试结果: 位置匹配成功")
        print(f"   最终位置: {result['location']}")
        print(f"   是否新位置: {result['is_new_location']}")
    else:
        print(f"❌ 测试失败: {result.get('message', '未知错误')}")
    
    return 0

def main():
    """主CLI函数"""
    parser = argparse.ArgumentParser(
        description="飞书收纳管家 - 智能位置匹配 + 位置图片管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 添加物品（智能位置匹配）
  storage-manager add "护照" "双肩包内层" --image="passport.jpg"
  
  # 添加位置图片（新位置需要拍照时使用）
  storage-manager add-location-photo "2号纸箱" --image="box_location.jpg"
  
  # 测试位置匹配
  storage-manager test-match "白色行李箱"
  
  # 搜索物品
  storage-manager search "梳子"
  
  # 更新位置
  storage-manager update "护照" "办公桌抽屉"

功能特点:
  ✅ 智能位置匹配 (>75%相似度自动匹配)
  ✅ 位置图片管理（新位置需拍照）
  ✅ 无需用户二次确认
  ✅ 位置图片缓存复用
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加物品（智能位置匹配）")
    add_parser.add_argument("item", help="物品名称")
    add_parser.add_argument("location", help="存放位置")
    add_parser.add_argument("--image", help="物品图片路径（可选）")
    add_parser.set_defaults(func=add_item)
    
    # add-location-photo 命令
    photo_parser = subparsers.add_parser("add-location-photo", help="添加位置图片")
    photo_parser.add_argument("location", help="位置名称")
    photo_parser.add_argument("--image", required=True, help="位置图片路径")
    photo_parser.set_defaults(func=add_location_photo)
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索物品")
    search_parser.add_argument("item", help="要查找的物品名称")
    search_parser.set_defaults(func=search_item)
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新物品位置")
    update_parser.add_argument("item", help="物品名称")
    update_parser.add_argument("new_location", help="新位置")
    update_parser.set_defaults(func=update_location)
    
    # test-match 命令
    test_parser = subparsers.add_parser("test-match", help="测试位置匹配")
    test_parser.add_argument("location", help="要测试的位置")
    test_parser.set_defaults(func=test_match)
    
    # 如果没有命令，显示帮助
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        return args.func(args)
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())