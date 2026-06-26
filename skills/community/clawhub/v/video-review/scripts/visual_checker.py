#!/usr/bin/env python3
"""
视觉检测模块 - 集成 OpenClaw image 工具
逐帧调用 vision 模型检测视觉问题
"""

import os
import sys

# 视觉问题关键词列表（用于 image 工具的 prompt）
PROMPT_TEMPLATE = """你是一个严格的内容安全审核员。请仔细分析这张视频帧画面。

检测以下问题并输出 JSON：
{
  "passed": true/false,
  "issues": [
    {
      "category": "暴露/低俗 | 公职人员 | 机关标志 | 人民币 | 血腥暴力 | 阴暗画风 | 封建迷信 | 未成年保护",
      "description": "具体描述发现的问题",
      "severity": "轻微 | 严重",
      "suggestion": "处理建议"
    }
  ]
}

判断标准：
- 暴露：女性角色衣着暴露（大面积深V、低胸、透视、过于紧身低胸），或刻意展示性暗示部位 → 严重
- 公职人员：出现警察制服/警徽/警衔、军人/军装、国徽/法槌/法院标识、检察院/公安局楼等 → 必须标记
- 机关标志：国徽、法院标志、警察局标识、政府楼外观（含明显国旗/党旗/国徽雕塑）→ 必须标记
- 人民币：人民币纸币/硬币完整图案（任何面值）→ 必须标记
- 血腥暴力：割腕/自残血痕（中景及以上特写）、虐待/家暴殴打过程、极度狰狞死状 → 严重
- 阴暗画风：整体色调极度阴暗压抑（80%以上画面黑色/深灰）、明显灵异惊悚氛围 → 轻微
- 封建迷信：现实题材中明确出现算命/看相/做法/巫蛊/香灰碗等 → 严重
- 未成年保护：未成年人吸烟/饮酒/纹身、校园霸凌现场、早恋明示 → 严重

如果通过，返回：
{"passed": true, "issues": []}

只输出 JSON，不要输出其他内容。
"""


def check_frame(frame_path, frame_num, timestamp):
    """
    调用 OpenClaw image 工具检测单帧
    返回 issues 列表
    """
    from subprocess import run, PIPE

    # 调用 OpenClaw image 工具
    # 这里用 exec 方式调用 python 脚本间接调用 image 工具
    # 实际通过 subprocess 执行 openclaw CLI
    cmd = [
        "python3", "-c",
        f'''
import sys
sys.path.insert(0, "/Users/suran/.openclaw/workspace/skills/video-audit-skill/scripts")
from image_tool_wrapper import analyze_image
result = analyze_image("{frame_path}", "{PROMPT_TEMPLATE}")
print(result)
'''
    ]

    try:
        result = run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            import json
            output = result.stdout.strip()
            # 尝试解析 JSON
            try:
                data = json.loads(output)
                if not data.get("passed"):
                    issues = data.get("issues", [])
                    for iss in issues:
                        iss["frame_num"] = frame_num
                        iss["timestamp"] = timestamp
                        iss["frame_file"] = os.path.basename(frame_path)
                    return issues
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"image 工具调用失败: {e}", file=sys.stderr)

    return []


def batch_check_frames(frames_dir, frames_list, interval=2):
    """
    批量检测多帧，收集所有问题
    """
    all_issues = []

    for i, frame_file in enumerate(frames_list):
        frame_path = os.path.join(frames_dir, frame_file)
        timestamp_sec = i * interval
        mins = timestamp_sec // 60
        secs = timestamp_sec % 60
        timestamp = f"00:{mins:02d}:{secs:02d}"

        issues = check_frame(frame_path, i, timestamp)
        all_issues.extend(issues)

        # 控制频率，避免并发过高
        import time
        time.sleep(0.3)

    return all_issues


if __name__ == "__main__":
    # 测试用
    import json

    test_frame = sys.argv[1] if len(sys.argv) > 1 else "/tmp/test.png"
    if os.path.exists(test_frame):
        result = check_frame(test_frame, 0, "00:00:00")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("测试帧不存在")