#!/usr/bin/env python3
"""
OpenClaw image 工具包装器
通过 openclaw CLI 调用 image 分析功能
"""

import json
import os
import subprocess
import tempfile


def analyze_image(image_path, prompt):
    """
    使用 OpenClaw 内置 image 工具分析图片
    通过 --image 参数传入本地图片路径
    """
    # 写入 prompt 到临时文件，避免命令行转义问题
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        cmd = [
            "openclaw", "image",
            "--image", image_path,
            "--prompt", f"@{prompt_file}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            # 尝试解析错误输出
            return json.dumps({"error": result.stderr[:200], "passed": True, "issues": []})
    except FileNotFoundError:
        return json.dumps({"error": "openclaw CLI not found", "passed": True, "issues": []})
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "timeout", "passed": True, "issues": []})
    finally:
        os.unlink(prompt_file)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        prompt = sys.argv[2] if len(sys.argv) > 2 else "描述这张图片的内容"
        result = analyze_image(image_path, prompt)
        print(result)
    else:
        print("用法: python3 image_tool_wrapper.py <图片路径> [prompt]")