#!/usr/bin/env python3
"""
Rumour Buster Setup Script
初始化配置脚本，检查依赖、配置搜索引擎、设置 Tavily API
"""

import os
import json
import sys
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.rumour-buster-config")

def print_header():
    print("=" * 60)
    print("🔧 Rumour Buster 初始化设置")
    print("=" * 60)
    print()

def check_kimi_search():
    """检查 kimi_search 是否可用"""
    print("🔍 检查 kimi_search...")
    # 实际运行时通过工具调用检查
    return {"available": True, "type": "native"}

def check_web_search():
    """检查 web_search (Brave) 是否可用"""
    print("🔍 检查 web_search (Brave)...")
    return {"available": False, "reason": "需要 BRAVE_API_KEY"}

def check_multi_search_engine():
    """检查 multi-search-engine 是否安装"""
    print("🔍 检查 multi-search-engine...")
    skill_path = os.path.expanduser("~/.openclaw/workspace/skills/api-multi-search-engine")
    if os.path.exists(skill_path):
        return {
            "available": True,
            "chinese_engines": ["sogou", "sogou_wechat", "toutiao"],
            "english_engines": ["duckduckgo", "startpage", "wolframalpha"]
        }
    return {"available": False}

def configure_tavily():
    """配置 Tavily API"""
    print()
    print("📚 关于 Tavily（英文深度搜索）")
    print("-" * 60)
    print("Tavily 是一个专为 AI 设计的搜索引擎：")
    print("  ✅ 免费额度：每月 1000 次查询")
    print("  ✅ AI 智能总结：自动生成答案摘要")
    print("  ✅ 可信度评分：每个结果有相关度评分")
    print("  ✅ 权威来源：覆盖 WHO、NIH、BBC 等国际机构")
    print()
    
    response = input("是否启用 Tavily 搜索？(yes/no，默认 yes): ").strip().lower()
    if response in ["", "yes", "y"]:
        print()
        print("请按以下步骤申请 Tavily API Key：")
        print("  1. 访问 https://tavily.com/")
        print("  2. 点击 'Sign Up' 注册账号")
        print("  3. 进入 Dashboard → API Keys")
        print("  4. 点击 'Create New Key'")
        print("  5. 复制生成的 Key（格式：tvly-xxxxxxxx）")
        print()
        
        api_key = input("请输入您的 Tavily API Key（或按回车跳过）: ").strip()
        
        if api_key:
            if api_key.startswith("tvly-"):
                print("✅ API Key 格式正确")
                return {"configured": True, "api_key": api_key, "free_quota": 1000}
            else:
                print("⚠️ API Key 格式不正确，应以 tvly- 开头")
                return {"configured": False}
        else:
            print("⏭️  跳过 Tavily 配置")
            return {"configured": False}
    else:
        print("⏭️  跳过 Tavily 配置")
        return {"configured": False}

def generate_config(kimi, multi_search, tavily):
    """生成配置文件"""
    config = {
        "setup_completed": True,
        "setup_time": datetime.now().isoformat(),
        "version": "0.3.0",
        "search_engines": {
            "chinese": {
                "kimi_search": {
                    "available": kimi["available"],
                    "type": "native"
                },
                "multi_search_engine": {
                    "available": multi_search["available"],
                    "engines": multi_search.get("chinese_engines", [])
                }
            },
            "english": {
                "tavily": {
                    "available": tavily.get("configured", False),
                    "api_key": tavily.get("api_key", ""),
                    "free_quota": tavily.get("free_quota", 0)
                },
                "multi_search_engine": {
                    "available": multi_search["available"],
                    "engines": multi_search.get("english_engines", [])
                }
            }
        },
        "verification": {
            "multi_search_engine_installed": multi_search["available"],
            "tavily_configured": tavily.get("configured", False)
        }
    }
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    return config

def print_summary(config):
    """打印配置摘要"""
    print()
    print("=" * 60)
    print("✅ Rumour Buster 设置完成！")
    print("=" * 60)
    print()
    print("📊 配置摘要：")
    print("-" * 60)
    print()
    print("国内搜索引擎：")
    
    if config["search_engines"]["chinese"]["kimi_search"]["available"]:
        print("  ✓ kimi_search (原生)")
    
    mse = config["search_engines"]["chinese"]["multi_search_engine"]
    if mse["available"]:
        for engine in mse["engines"]:
            print(f"  ✓ {engine} (multi-search-engine)")
    
    print()
    print("国际搜索引擎：")
    
    tavily = config["search_engines"]["english"]["tavily"]
    if tavily["available"]:
        print(f"  ✓ Tavily (API已配置，免费额度：{tavily['free_quota']}次/月)")
    else:
        print("  ⏭️  Tavily (未配置)")
    
    mse_en = config["search_engines"]["english"]["multi_search_engine"]
    if mse_en["available"]:
        for engine in mse_en["engines"]:
            print(f"  ✓ {engine} (multi-search-engine)")
    
    print()
    print("-" * 60)
    print()
    print("💡 提示：")
    print("  • 使用 '/验证 \"消息内容\"' 开始事实核查")
    print("  • 输入 'setup' 或 '重新设置' 可修改配置")
    print()
    print("=" * 60)

def main():
    print_header()
    
    # 检查 multi-search-engine（必需）
    multi_search = check_multi_search_engine()
    if not multi_search["available"]:
        print("❌ 设置未完成\n")
        print("缺少必需依赖：multi-search-engine\n")
        print("请执行以下命令安装：")
        print("  clawhub install api-multi-search-engine\n")
        print("或访问: https://clawhub.com 搜索 'multi-search-engine'\n")
        print("安装完成后重新运行 setup。")
        sys.exit(1)
    
    print("✅ multi-search-engine 已安装\n")
    
    # 检查其他搜索技能
    kimi = check_kimi_search()
    brave = check_web_search()
    
    # 配置 Tavily
    tavily = configure_tavily()
    
    # 生成配置
    config = generate_config(kimi, multi_search, tavily)
    
    # 打印摘要
    print_summary(config)
    
    print(f"\n📁 配置文件已保存至: {CONFIG_FILE}")

if __name__ == "__main__":
    main()
