#!/usr/bin/env python3
"""
Rumor Buster Setup Script
智能检测已安装的搜索引擎，支持修改现有配置或重新配置
"""

import os
import json
import sys
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.rumor-buster-config")

def print_header():
    print("=" * 60)
    print("🔧 Rumor Buster 设置")
    print("=" * 60)
    print()

def check_multi_search_engine_installed():
    """检查 multi-search-engine 技能是否安装"""
    skill_path = os.path.expanduser("~/.openclaw/workspace/skills/api-multi-search-engine")
    if os.path.exists(skill_path):
        return True
    # 也检查其他可能的安装路径
    alt_paths = [
        "/usr/local/lib/openclaw/skills/api-multi-search-engine",
        "/opt/openclaw/skills/api-multi-search-engine"
    ]
    for path in alt_paths:
        if os.path.exists(path):
            return True
    return False

def detect_kimi_search():
    """检测 kimi_search 是否可用"""
    print("🔍 检测 kimi_search...")
    try:
        # 尝试导入或调用 kimi_search
        # 这里通过检查命令是否存在来判断
        import subprocess
        result = subprocess.run(
            ["which", "kimi_search"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("  ✅ kimi_search 已安装")
            return True
    except:
        pass
    
    # 尝试通过 Python 导入检测
    try:
        # 如果 kimi_search 是 Python 模块
        import importlib
        spec = importlib.util.find_spec("kimi_search")
        if spec is not None:
            print("  ✅ kimi_search 已安装")
            return True
    except:
        pass
    
    print("  ❌ kimi_search 未安装")
    return False

def detect_multi_search_engines():
    """检测 multi-search-engine 中哪些引擎可用"""
    print("🔍 检测 multi-search-engine...")
    
    if not check_multi_search_engine_installed():
        print("  ❌ multi-search-engine 未安装")
        return []
    
    # 测试各引擎是否可用
    engines = {
        "chinese": [],
        "english": []
    }
    
    # 测试中文引擎
    chinese_engines = [
        ("sogou", "https://www.sogou.com/web?query=test"),
        ("sogou_wechat", "https://wx.sogou.com/weixin?type=2&query=test"),
        ("toutiao", "https://so.toutiao.com/search?keyword=test")
    ]
    
    print("  测试中文引擎...")
    for name, test_url in chinese_engines:
        try:
            import urllib.request
            req = urllib.request.Request(
                test_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            response = urllib.request.urlopen(req)
            if response.status == 200:
                engines["chinese"].append(name)
                print(f"    ✅ {name}")
        except:
            print(f"    ❌ {name}")
    
    # 测试英文引擎
    english_engines = [
        ("duckduckgo", "https://duckduckgo.com/html/?q=test"),
        ("startpage", "https://www.startpage.com/sp/search?query=test")
    ]
    
    print("  测试英文引擎...")
    for name, test_url in english_engines:
        try:
            import urllib.request
            req = urllib.request.Request(
                test_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            response = urllib.request.urlopen(req)
            if response.status == 200:
                engines["english"].append(name)
                print(f"    ✅ {name}")
        except:
            print(f"    ❌ {name}")
    
    if engines["chinese"] or engines["english"]:
        print(f"  ✅ multi-search-engine 可用")
    
    return engines

def detect_tavily_config():
    """检测 Tavily 配置"""
    print("🔍 检测 Tavily...")
    
    # 检查环境变量
    api_key = os.getenv("TAVILY_API_KEY", "")
    
    # 检查现有配置文件
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                existing_key = config.get("search_engines", {}).get("english", {}).get("tavily", {}).get("api_key", "")
                if existing_key and not api_key:
                    api_key = existing_key
        except:
            pass
    
    if api_key and api_key.startswith("tvly-"):
        print(f"  ✅ Tavily 已配置 ({api_key[:15]}...)")
        return {"available": True, "configured": True, "api_key": api_key}
    else:
        print("  ⏭️  Tavily 未配置（可选）")
        return {"available": False, "configured": False, "api_key": ""}

def detect_all_engines():
    """检测所有搜索引擎"""
    print("📊 检测已安装的搜索引擎...\n")
    
    result = {
        "chinese": {
            "kimi_search": {"available": False, "type": "native"},
            "multi_search_engine": {"available": False, "engines": []}
        },
        "english": {
            "tavily": {"available": False, "configured": False, "api_key": ""},
            "multi_search_engine": {"available": False, "engines": []}
        }
    }
    
    # 检测中文引擎
    kimi_available = detect_kimi_search()
    result["chinese"]["kimi_search"]["available"] = kimi_available
    
    multi_engines = detect_multi_search_engines()
    if multi_engines["chinese"] or multi_engines["english"]:
        result["chinese"]["multi_search_engine"]["available"] = True
        result["chinese"]["multi_search_engine"]["engines"] = multi_engines["chinese"]
        result["english"]["multi_search_engine"]["available"] = True
        result["english"]["multi_search_engine"]["engines"] = multi_engines["english"]
    
    # 检测 Tavily
    tavily_config = detect_tavily_config()
    result["english"]["tavily"] = tavily_config
    
    print()
    return result

def show_current_config(config):
    """显示当前配置"""
    print("\n📁 当前配置：\n")
    
    print("中文搜索引擎：")
    if config["chinese"]["kimi_search"]["available"]:
        print("  ✅ kimi_search")
    else:
        print("  ❌ kimi_search（未安装）")
    
    if config["chinese"]["multi_search_engine"]["available"]:
        engines = config["chinese"]["multi_search_engine"]["engines"]
        print(f"  ✅ multi-search-engine")
        for e in engines:
            print(f"     - {e}")
    else:
        print("  ❌ multi-search-engine（未安装）")
    
    print("\n英文搜索引擎：")
    if config["english"]["tavily"]["available"]:
        print(f"  ✅ Tavily（已配置）")
    else:
        print("  ⏭️  Tavily（未配置）")
    
    if config["english"]["multi_search_engine"]["available"]:
        engines = config["english"]["multi_search_engine"]["engines"]
        print(f"  ✅ multi-search-engine")
        for e in engines:
            print(f"     - {e}")
    
    print()

def configure_tavily():
    """配置 Tavily"""
    print("\n📚 Tavily 配置")
    print("-" * 40)
    print("Tavily 是专为 AI 设计的英文搜索引擎：")
    print("  ✅ 每月 1000 次免费查询")
    print("  ✅ AI 智能总结")
    print("  ✅ 覆盖 WHO、NIH、BBC 等国际权威来源")
    print()
    
    response = input("是否启用 Tavily？(yes/no，默认 no): ").strip().lower()
    if response in ["yes", "y"]:
        print("\n请按以下步骤申请 Tavily API Key：")
        print("  1. 访问 https://tavily.com/")
        print("  2. 注册账号并创建 API Key")
        print("  3. 复制 Key（格式：tvly-xxxxxx）")
        print()
        
        api_key = input("请粘贴 Tavily API Key: ").strip()
        
        if api_key.startswith("tvly-"):
            print("✅ API Key 格式正确")
            return {"available": True, "configured": True, "api_key": api_key}
        else:
            print("⚠️ API Key 格式不正确，应以 'tvly-' 开头")
            return {"available": False, "configured": False, "api_key": ""}
    else:
        print("⏭️  跳过 Tavily 配置")
        return {"available": False, "configured": False, "api_key": ""}

def save_config(engines, tavily_config=None):
    """保存配置文件"""
    if tavily_config:
        engines["english"]["tavily"] = tavily_config
    
    config = {
        "setup_completed": True,
        "setup_time": datetime.now().isoformat(),
        "version": "0.4.0",
        "search_engines": engines,
        "detection_log": {
            "last_detection": datetime.now().isoformat(),
            "detected_engines": []
        }
    }
    
    # 记录检测到的引擎
    detected = []
    if engines["chinese"]["kimi_search"]["available"]:
        detected.append("kimi_search")
    if engines["chinese"]["multi_search_engine"]["available"]:
        detected.extend(engines["chinese"]["multi_search_engine"]["engines"])
    if engines["english"]["multi_search_engine"]["available"]:
        detected.extend(engines["english"]["multi_search_engine"]["engines"])
    if engines["english"]["tavily"]["available"]:
        detected.append("tavily")
    
    config["detection_log"]["detected_engines"] = detected
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 配置已保存至: {CONFIG_FILE}")
    return config

def show_summary(engines):
    """显示配置摘要"""
    print("\n" + "=" * 60)
    print("✅ Rumor Buster 配置完成！")
    print("=" * 60)
    print("\n可用搜索引擎：\n")
    
    print("中文：")
    if engines["chinese"]["kimi_search"]["available"]:
        print("  • kimi_search")
    if engines["chinese"]["multi_search_engine"]["available"]:
        for e in engines["chinese"]["multi_search_engine"]["engines"]:
            print(f"  • {e}")
    
    print("\n英文：")
    if engines["english"]["tavily"]["available"]:
        print("  • Tavily")
    if engines["english"]["multi_search_engine"]["available"]:
        for e in engines["english"]["multi_search_engine"]["engines"]:
            print(f"  • {e}")
    
    print("\n" + "=" * 60)
    print("\n现在可以发送 /验证 \"消息内容\" 开始验证了！")

def full_setup():
    """完整配置流程"""
    print("🆕 开始全新配置\n")
    
    # 检测所有引擎
    engines = detect_all_engines()
    
    # 检查是否至少有一个搜索引擎可用
    has_chinese = (engines["chinese"]["kimi_search"]["available"] or 
                   engines["chinese"]["multi_search_engine"]["available"])
    has_english = (engines["english"]["multi_search_engine"]["available"])
    
    if not has_chinese and not has_english:
        print("❌ 错误：未检测到任何可用的搜索引擎")
        print("\n请安装以下至少一项：")
        print("  • multi-search-engine 技能（必需）")
        print("    安装命令: clawhub install api-multi-search-engine")
        print("  • kimi_search（可选，但推荐）")
        sys.exit(1)
    
    # 配置 Tavily（可选）
    tavily_config = configure_tavily()
    
    # 保存配置
    config = save_config(engines, tavily_config)
    
    # 显示摘要
    show_summary(config["search_engines"])

def modify_config(existing_config):
    """修改现有配置"""
    while True:
        print("\n请选择要修改的项目：")
        print("  1. 添加/修改 Tavily API Key")
        print("  2. 重新检测搜索引擎")
        print("  3. 返回主菜单")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            tavily_config = configure_tavily()
            existing_config["search_engines"]["english"]["tavily"] = tavily_config
            save_config(existing_config["search_engines"])
            print("✅ Tavily 配置已更新")
            
        elif choice == "2":
            print("\n🔄 重新检测搜索引擎...")
            engines = detect_all_engines()
            existing_config["search_engines"] = engines
            save_config(engines)
            print("✅ 搜索引擎检测完成")
            
        elif choice == "3":
            break
        else:
            print("⚠️ 无效选择")

def main():
    print_header()
    
    # 检查现有配置
    if os.path.exists(CONFIG_FILE):
        print("📁 检测到现有配置文件\n")
        
        with open(CONFIG_FILE, 'r') as f:
            existing_config = json.load(f)
        
        show_current_config(existing_config["search_engines"])
        
        print("请选择操作：")
        print("  1. 修改部分配置")
        print("  2. 重新配置（删除现有配置）")
        print("  3. 查看当前配置")
        print("  4. 退出")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == "1":
            modify_config(existing_config)
        elif choice == "2":
            confirm = input("\n⚠️  确定要删除现有配置并重新配置吗？(yes/no): ").strip().lower()
            if confirm in ["yes", "y"]:
                os.remove(CONFIG_FILE)
                print("🗑️  已删除现有配置\n")
                full_setup()
            else:
                print("已取消")
        elif choice == "3":
            show_current_config(existing_config["search_engines"])
        else:
            print("已退出")
    else:
        print("🆕 首次配置 Rumor Buster\n")
        full_setup()

if __name__ == "__main__":
    main()
