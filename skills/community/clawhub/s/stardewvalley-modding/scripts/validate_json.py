#!/usr/bin/env python3
"""
验证 JSON 文件格式
"""
import sys
import json
import os

def validate_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {filepath} - 格式正确")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {filepath} - JSON 错误: {e}")
        return False
    except Exception as e:
        print(f"❌ {filepath} - 错误: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 验证当前目录所有 JSON
        for f in os.listdir('.'):
            if f.endswith('.json'):
                validate_json(f)
    else:
        validate_json(sys.argv[1])
