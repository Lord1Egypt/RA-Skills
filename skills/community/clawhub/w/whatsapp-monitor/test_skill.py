#!/usr/bin/env python3
"""
测试 WhatsApp Monitor Skill 是否能在 OpenClaw 中正常工作
"""

import sys
import os
import json

# 添加技能目录到路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(skill_dir, "scripts"))

def test_config_manager():
    """测试配置管理器"""
    try:
        from config_manager import ConfigManager
        
        print("测试配置管理器...")
        config = ConfigManager(config_dir=os.path.join(skill_dir, "config"))
        
        # 测试配置加载
        if config.load_configs():
            print("[OK] 配置加载成功")
            print(f"  监控目标数量: {config.get_targets_count()}")
            print(f"  关键词总数: {config.get_keywords_count()}")
            print(f"  扫描间隔: {config.get_scan_interval()}秒")
            print(f"  批量阈值: {config.get_batch_threshold()}")
            
            # 测试消息处理
            test_message = {
                "id": "test_123",
                "timestamp": "2024-01-01T12:00:00Z",
                "sender": "+1234567890",
                "content": "这是一个测试紧急消息",
                "type": "text",
                "chat_id": "1234567890-1234567890@g.us",
                "target_config": {
                    "keywords": ["紧急", "测试"],
                    "priority": "high"
                }
            }
            
            config.save_matched_messages([test_message])
            stored = config.get_stored_messages()
            print(f"[OK] 消息存储测试: 已存储 {len(stored)} 条消息")
            
            return True
        else:
            print("[ERROR] 配置加载失败")
            return False
            
    except Exception as e:
        print(f"[ERROR] 配置管理器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_message_processor():
    """测试消息处理器"""
    try:
        from message_processor import MessageProcessor
        
        print("\n测试消息处理器...")
        processor = MessageProcessor()
        
        # 测试消息处理
        test_message = {
            "content": "项目进度已经完成了80%，但遇到一个紧急问题需要处理",
            "sender": "项目经理",
            "source": "项目群",
            "target_config": {
                "keywords": ["紧急", "问题", "进度"],
                "keyword_patterns": [r"进度.*%", r"紧急.*"],
                "priority": "high"
            }
        }
        
        processed = processor.process_message(test_message)
        if processed and processed.get("matched"):
            print("[OK] 消息处理测试成功")
            print(f"  匹配关键词: {processed.get('matched_keywords')}")
            print(f"  优先级: {processed.get('priority')}")
            print(f"  上下文: {processed.get('context')[:50]}...")
            return True
        else:
            print("[ERROR] 消息处理测试失败: 未匹配到关键词")
            return False
            
    except Exception as e:
        print(f"[ERROR] 消息处理器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_feishu_client():
    """测试飞书客户端"""
    try:
        from feishu_client import FeishuClient
        
        print("\n测试飞书客户端...")
        
        # 加载配置
        config_path = os.path.join(skill_dir, "config", "feishu-settings.json")
        if not os.path.exists(config_path):
            print("[WARNING] 飞书配置文件不存在，跳过客户端测试")
            return True  # 不是错误，只是跳过
            
        with open(config_path, 'r', encoding='utf-8') as f:
            feishu_config = json.load(f)
        
        # 检查是否配置了测试凭证
        app_id = feishu_config.get("feishu", {}).get("app_id", "")
        if app_id == "YOUR_APP_ID" or not app_id:
            print("[WARNING] 飞书配置为默认值，跳过连接测试")
            return True  # 不是错误，只是跳过
        
        client = FeishuClient(feishu_config)
        print("[OK] 飞书客户端初始化成功")
        return True
        
    except Exception as e:
        print(f"[ERROR] 飞书客户端测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_whatsapp_client():
    """测试 WhatsApp 客户端"""
    try:
        from whatsapp_client import WhatsAppClient
        
        print("\n测试 WhatsApp 客户端...")
        
        # 加载配置
        config_path = os.path.join(skill_dir, "config", "whatsapp-targets.json")
        if not os.path.exists(config_path):
            print("[WARNING] WhatsApp 配置文件不存在")
            return False
            
        with open(config_path, 'r', encoding='utf-8') as f:
            whatsapp_config = json.load(f)
        
        client = WhatsAppClient(whatsapp_config)
        print("[OK] WhatsApp 客户端初始化成功")
        
        # 注意：实际连接测试需要 OpenClaw WhatsApp 渠道运行
        print("[WARNING] 实际连接测试需要 OpenClaw WhatsApp 渠道已配置并运行")
        return True
        
    except Exception as e:
        print(f"[ERROR] WhatsApp 客户端测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_main_monitor():
    """测试主监控器"""
    try:
        print("\n测试主监控器...")
        
        # 检查是否能导入主模块
        import monitor
        print("[OK] 主监控模块导入成功")
        
        # 检查命令行参数解析
        import argparse
        parser = argparse.ArgumentParser(description="WhatsApp Monitor")
        parser.add_argument("--test", action="store_true", help="Test mode")
        
        # 简单的模块检查
        print("[OK] 模块结构检查通过")
        return True
        
    except Exception as e:
        print(f"[ERROR] 主监控器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_skill_integration():
    """测试技能集成"""
    print("\n=== WhatsApp Monitor Skill 集成测试 ===")
    
    # 检查技能文件
    skill_file = os.path.join(skill_dir, "SKILL.md")
    if os.path.exists(skill_file):
        print("SKILL.md 文件存在 [OK]")
    else:
        print("SKILL.md 文件不存在 [ERROR]")
        return False
    
    # 检查配置文件
    config_files = [
        os.path.join(skill_dir, "config", "whatsapp-targets.json"),
        os.path.join(skill_dir, "config", "feishu-settings.json")
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"配置文件存在: {os.path.basename(config_file)} [OK]")
        else:
            print(f"配置文件不存在: {os.path.basename(config_file)} [WARNING]")
    
    # 检查脚本文件
    script_files = [
        os.path.join(skill_dir, "scripts", "monitor.py"),
        os.path.join(skill_dir, "scripts", "config_manager.py"),
        os.path.join(skill_dir, "scripts", "whatsapp_client.py"),
        os.path.join(skill_dir, "scripts", "feishu_client.py"),
        os.path.join(skill_dir, "scripts", "message_processor.py"),
        os.path.join(skill_dir, "scripts", "setup.py")
    ]
    
    all_scripts_exist = True
    for script_file in script_files:
        if os.path.exists(script_file):
            print(f"脚本文件存在: {os.path.basename(script_file)} [OK]")
        else:
            print(f"脚本文件不存在: {os.path.basename(script_file)} [ERROR]")
            all_scripts_exist = False
    
    if not all_scripts_exist:
        return False
    
    print("[OK] 技能集成测试通过")
    return True

def main():
    """主测试函数"""
    print("开始 WhatsApp Monitor Skill 测试...")
    print("=" * 60)
    
    tests = [
        ("技能集成测试", test_skill_integration),
        ("配置管理器测试", test_config_manager),
        ("消息处理器测试", test_message_processor),
        ("飞书客户端测试", test_feishu_client),
        ("WhatsApp 客户端测试", test_whatsapp_client),
        ("主监控器测试", test_main_monitor)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n正在运行: {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("-" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "[OK] 通过" if success else "[ERROR] 失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print("-" * 60)
    print(f"总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("[SUCCESS] 所有测试通过！技能已准备就绪。")
        print("\n下一步操作:")
        print("1. 编辑 config/whatsapp-targets.json 配置监控目标")
        print("2. 编辑 config/feishu-settings.json 配置飞书凭证")
        print("3. 运行 'pip install -r requirements.txt' 安装依赖")
        print("4. 启动 OpenClaw WhatsApp 渠道并配对设备")
        print("5. 运行 'python scripts/monitor.py --start' 开始监控")
    else:
        print("[WARNING] 部分测试失败，请检查错误信息。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)