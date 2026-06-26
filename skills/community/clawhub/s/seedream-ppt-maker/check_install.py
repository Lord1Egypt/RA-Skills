#!/usr/bin/env python3
"""
seedream-ppt-maker 安装检查脚本
检查依赖和 API Key 配置
"""

import os
import sys
import json
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...\n")
    
    issues = []
    
    # 1. 检查 baoyu-infographic
    skill_root = Path(__file__).parent
    baoyu_root = skill_root.parent / "baoyu-infographic"
    
    if baoyu_root.exists():
        layouts_dir = baoyu_root / "references" / "layouts"
        styles_dir = baoyu_root / "references" / "styles"
        layouts_count = len(list(layouts_dir.glob("*.md"))) if layouts_dir.exists() else 0
        styles_count = len(list(styles_dir.glob("*.md"))) if styles_dir.exists() else 0
        print(f"✅ baoyu-infographic 已安装")
        print(f"   布局: {layouts_count} 种")
        print(f"   风格: {styles_count} 种")
    else:
        print(f"❌ baoyu-infographic 未安装")
        print(f"   安装命令: clawhub install baoyu-infographic")
        issues.append("baoyu-infographic 未安装")
    
    # 2. 检查 python-pptx
    try:
        import pptx
        print(f"✅ python-pptx 已安装")
    except ImportError:
        print(f"❌ python-pptx 未安装")
        print(f"   安装命令: pip install python-pptx")
        issues.append("python-pptx 未安装")
    
    # 3. 检查 requests
    try:
        import requests
        print(f"✅ requests 已安装")
    except ImportError:
        print(f"❌ requests 未安装")
        print(f"   安装命令: pip install requests")
        issues.append("requests 未安装")
    
    return issues

def check_api_key():
    """检查 Seedream API Key"""
    print("\n🔍 检查 API Key...\n")
    
    config_path = Path.home() / ".openclaw" / "config.json"
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'volces' in config and 'apiKey' in config['volces']:
            api_key = config['volces']['apiKey']
            print(f"✅ 火山方舟 API Key 已配置")
            print(f"   Key: {api_key[:20]}...")
            
            # 测试 API
            print("\n📡 测试 Seedream API...")
            try:
                import requests
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                data = {
                    "model": "doubao-seedream-5-0-260128",
                    "prompt": "test",
                    "size": "2560x1440"
                }
                response = requests.post(
                    "https://ark.cn-beijing.volces.com/api/v3/images/generations",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                if response.status_code == 200:
                    print(f"✅ Seedream API 正常工作")
                else:
                    print(f"⚠️  Seedream API 返回错误: {response.status_code}")
                    print(f"   响应: {response.text[:100]}")
            except Exception as e:
                print(f"⚠️  API 测试失败: {e}")
            
            return []
        else:
            print(f"❌ 火山方舟 API Key 未配置")
            print(f"   配置方法:")
            print(f"   1. 打开 ~/.openclaw/config.json")
            print(f"   2. 添加:")
            print(f'      {"volces": {"apiKey": "你的API Key"}}')
            return ["API Key 未配置"]
    else:
        print(f"❌ ~/.openclaw/config.json 不存在")
        print(f"   创建配置文件:")
        print(f'   {"volces": {"apiKey": "你的API Key"}}')
        return ["配置文件不存在"]

def main():
    """主检查流程"""
    print("="*50)
    print("seedream-ppt-maker 安装检查")
    print("="*50 + "\n")
    
    dep_issues = check_dependencies()
    api_issues = check_api_key()
    
    all_issues = dep_issues + api_issues
    
    print("\n" + "="*50)
    if all_issues:
        print(f"❌ 发现 {len(all_issues)} 个问题:")
        for issue in all_issues:
            print(f"   - {issue}")
        print("\n请先解决以上问题再使用此 skill")
    else:
        print("✅ 所有依赖和配置检查通过")
        print("\n现在可以使用 seedream-ppt-maker skill 了!")
    print("="*50)
    
    return len(all_issues) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)