"""
演讲稿生成器 - 为每张PPT生成演讲稿
"""
from pathlib import Path
import json


def generate_speaker_notes(outline_path, output_path=None):
    """
    根据PPT大纲生成演讲稿

    Args:
        outline_path: presentation_outline.json 路径
        output_path: 输出的markdown文件路径
    """
    with open(outline_path, 'r', encoding='utf-8') as f:
        outline = json.load(f)

    slides = outline.get('slides', [])

    notes = []
    notes.append("# 演讲稿 / Speaker Notes\n")
    notes.append(f"**总时长**: {len(slides) * 1.5:.0f}-{len(slides) * 2:.0f} 分钟")
    notes.append(f"**每页平均**: 1.5-2 分钟\n")
    notes.append("---\n")

    for i, slide in enumerate(slides, 1):
        slide_type = slide.get('type', 'content')
        title = slide.get('title', f'Slide {i}')

        notes.append(f"## Slide {i}: {title}")

        if slide_type == 'title':
            duration = "30秒"
            points = [
                "- 自我介绍(姓名、课程)",
                "- 简短介绍项目主题",
                "- 用一句话概括做了什么"
            ]
        elif slide_type == 'qa':
            duration = "3-5分钟"
            points = [
                "- 感谢听众",
                "- 邀请提问",
                "- 准备好回答预期问题"
            ]
        elif slide_type in ('chart', 'figure'):
            duration = "2分钟"
            points = [
                "- 解释图表代表什么",
                "- 指出关键数据点/趋势",
                "- 解释这个结果意味着什么"
            ]
        else:
            duration = "1.5分钟"
            if slide.get('points'):
                points = [f"- 详细解释: {p}" for p in slide['points']]
            else:
                points = ["- [根据内容填写具体要说的话]"]

        notes.append(f"**类型**: {slide_type} | **建议时长**: {duration}")
        notes.append("\n**演讲要点**:")
        notes.extend(points)
        notes.append("\n**过渡句**: [Next, I'll talk about...]\n")
        notes.append("---\n")

    # Tips section
    notes.append("## 🎯 演讲技巧提醒\n")
    notes.append("1. **开场**: 先吸引注意力,用一个问题或有趣的数据开头")
    notes.append("2. **节奏**: 每页1.5-2分钟,不要赶也不要拖")
    notes.append("3. **眼神**: 看听众,不要看PPT")
    notes.append("4. **语速**: 比平时说话稍慢,关键词加重语气")
    notes.append("5. **站姿**: 不要前后摇晃,手自然放")
    notes.append('6. **结尾**: 清晰总结，不要用"that\'s it"结束')

    # Write output
    full_text = "\n".join(notes)

    if output_path is None:
        output_path = Path(outline_path).parent / "speaker_notes.md"

    Path(output_path).write_text(full_text, encoding='utf-8')
    print(f"  ✅ 演讲稿已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        generate_speaker_notes(sys.argv[1])
    else:
        print("Usage: python generate_notes.py <outline.json>")
