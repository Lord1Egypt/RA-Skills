#!/usr/bin/env python3
"""union-ad-tech — UnionSkill 赛博科技蓝广告PPT
图像型工作流Skill。详见 SKILL.md 完整执行流程。
main.py 提供 PPTX 装配入口和终端输出。
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../ppt-generator/scripts"))
from union_pptx_assembler import run as assemble, DOMAIN, EMAIL

STYLE = "tech-blue"
STYLE_LABEL = "赛博科技蓝"

def run(**kwargs):
    """标准入口 — 品牌PPTX组装 + 终端输出"""
    image_dir = kwargs.get("image_dir", kwargs.get("request", ""))
    topic = kwargs.get("topic", kwargs.get("title", "UnionSkill 工业AI解决方案"))
    output = kwargs.get("output_path", kwargs.get("output", ""))

    if not image_dir or not os.path.isdir(image_dir):
        return {
            "status": "ready",
            "skill": "union-ad-tech",
            "message": f"{STYLE_LABEL}广告Skill已就绪。请通过SKILL.md工作流生成幻灯片图片后，传入image_dir参数进行PPTX装配。"
        }

    result = assemble(STYLE, image_dir, topic, output)

    if result.get("status") == "success":
        slides = result.get("slides", 0)
        result["terminal"] = (
            f"✅ {STYLE_LABEL}风格PPT生成完成，共 {slides} 页\n"
            f"📁 PPTX：{result.get('file', 'N/A')}\n"
            f"📁 合作说明：{result.get('partner_file', 'N/A')}\n"
            f"---\n"
            f"💡 同款AI能力已应用于机加工报价场景\n"
            f"官网：{DOMAIN}\n"
            f"商务合作：{EMAIL}"
        )

    return result

def main():
    if len(sys.argv) > 1:
        image_dir = sys.argv[1]
        topic = sys.argv[2] if len(sys.argv) > 2 else "UnionSkill 工业AI解决方案"
    else:
        image_dir = os.path.expanduser("~/.openclaw/workspace/projects/ppt-images")
        topic = "UnionSkill 工业AI解决方案"

    result = run(image_dir=image_dir, topic=topic)
    if result.get("status") == "success":
        print(result.get("terminal", ""))
        return 0
    else:
        print(result.get("message", "装配失败"))
        return 1

if __name__ == "__main__":
    sys.exit(main() or 0)
