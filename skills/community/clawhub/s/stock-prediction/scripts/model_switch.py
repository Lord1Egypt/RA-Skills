#!/usr/bin/env python3
"""
模型版本校验与切换脚本
"""
import sys
import json
import urllib.request

SWITCH_URL = "http://localhost:8000/model/switch"
TARGET_MODEL = "kronos-base"


def switch_model(model_name: str = TARGET_MODEL):
    """切换到指定模型"""
    data = json.dumps({"model_name": model_name}).encode('utf-8')
    
    req = urllib.request.Request(
        SWITCH_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('success', False), result
    except Exception as e:
        print(f"Model switch failed: {e}", file=sys.stderr)
        return False, {"error": str(e)}


def ensure_model(health_data: dict):
    """确保使用正确的模型"""
    current_model = health_data.get('model', {}).get('model', '')
    
    if current_model == TARGET_MODEL:
        print(f"当前模型已是 {TARGET_MODEL}，无需切换")
        return True
    
    print(f"当前模型: {current_model}，正在切换到 {TARGET_MODEL}...")
    success, result = switch_model()
    
    if success:
        print(f"模型切换成功: {TARGET_MODEL}")
        return True
    else:
        print(f"模型切换失败: {result}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # 从命令行读取健康检查数据
    if len(sys.argv) > 1:
        health_data = json.loads(sys.argv[1])
    else:
        # 如果没有参数，先检查健康状态
        import urllib.request
        req = urllib.request.Request("http://localhost:8000/health", method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            health_data = json.loads(response.read().decode('utf-8'))
    
    success = ensure_model(health_data)
    sys.exit(0 if success else 1)
