#!/usr/bin/env python3
"""
周公解梦触发器
"""

import sys
import subprocess
import json

def zhougong_dream(dream_text=None, lang="zh"):
    """解梦函数"""
    if not dream_text:
        return "请提供梦境描述。格式：时间 + 环境 + 互动对象 + 做了什么"
    
    # 调用解梦脚本
    cmd = ["python", "scripts/zhougong_dream.py", "--dream", dream_text, "--lang", lang]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"解梦失败: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python trigger.py '梦境描述'")
        sys.exit(1)
    
    dream_text = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "zh"
    
    result = zhougong_dream(dream_text, lang)
    print(result)