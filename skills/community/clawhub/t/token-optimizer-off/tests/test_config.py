#!/usr/bin/env python3
"""测试 OpenClaw 配置加载"""
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from compress_session import load_openclaw_config

def test_config():
    """测试配置加载"""
    print("=== 测试 OpenClaw 配置加载 ===\n")
    
    try:
        config = load_openclaw_config()
        
        print("✅ 配置加载成功！\n")
        print("配置详情:")
        print(f"  Memory Dir: {config['memory_dir']}")
        print(f"  API URL: {config.get('api_url', '未配置')}")
        print(f"  Model: {config.get('model', '未配置')}")
        print(f"  API Key: {'已配置' if config.get('api_key') else '未配置'}")
        print(f"  Max Tokens: {config['max_tokens']}")
        print(f"  Max Chars: {config['max_chars']}")
        
        if not config.get('api_key'):
            print("\n⚠️  警告: 未找到 API Key")
            print("   请确保 OpenClaw 已正确配置 AI 服务")
            print("   配置文件: ~/.openclaw/config.json")
            return False
        
        print("\n✅ 所有配置正常！")
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

if __name__ == '__main__':
    success = test_config()
    sys.exit(0 if success else 1)
