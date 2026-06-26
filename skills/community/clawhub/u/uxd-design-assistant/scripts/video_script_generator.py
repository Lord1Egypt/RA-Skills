#!/usr/bin/env python3
"""
视频脚本生成器 - 为UXD作品展示生成讲解视频分镜脚本
用法: python3 video_script_generator.py --duration <秒数> --scene <场景描述> [--output <文件>]
"""

import argparse
import sys
from datetime import datetime


def generate_video_script(duration: int, scene: str) -> str:
    """生成视频分镜脚本"""
    
    # 根据总时长确定镜头数量和分配
    if duration <= 60:
        shot_count = 6
        intro_shots = 1
        outro_shots = 1
    elif duration <= 180:
        shot_count = 10
        intro_shots = 2
        outro_shots = 2
    else:
        shot_count = 15
        intro_shots = 3
        outro_shots = 2
    
    middle_shots = shot_count - intro_shots - outro_shots
    avg_duration = duration / shot_count
    
    intro_scenes = ["黑幕+标题文字动画", "产品logo特写", "用户场景速览"]
    outro_scenes = ["用户满意笑容", "产品成果展示", "团队成员", "致谢字幕"]
    shot_types = ["屏幕录制", "原型展示", "数据图表", "访谈片段"]
    transitions = ["淡入淡出", "滑动", "缩放", "溶解"]
    
    output = [
        f"# 视频分镜脚本",
        f"",
        f"**项目**: {scene}",
        f"**总时长**: {duration}秒（约{duration//60}分{duration%60}秒）",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"---",
        f"",
        f"## 开场镜头 ({intro_shots}个镜头, 约{intro_shots * avg_duration:.0f}秒)",
        f"",
    ]
    
    for i in range(1, intro_shots + 1):
        shot_duration = avg_duration * (0.8 + 0.4 * (i == 1))
        scene_desc = intro_scenes[i-1] if i <= len(intro_scenes) else "相关画面"
        composition = ["居中特写", "三分法", "黄金分割"][i-1]
        output.append(f"### 镜头 {i} [{shot_duration:.0f}秒]")
        output.append(f"**画面**: 场景={scene_desc}，构图={composition}，文字=「{scene}」")
        output.append(f"**旁白**: \"在{scene}中，您是否曾经遇到这样的困扰...\"")
        output.append("")
    
    output.append(f"## 主体内容 ({middle_shots}个镜头, 约{middle_shots * avg_duration:.0f}秒)")
    output.append("")
    
    phases = ["用户研究", "洞察分析", "设计原型", "测试验证"]
    for i in range(1, middle_shots + 1):
        phase_idx = (i - 1) * 4 // max(middle_shots, 1)
        phase = phases[phase_idx] if phase_idx < len(phases) else phases[-1]
        shot_type = shot_types[(i-1) % len(shot_types)]
        trans = transitions[(i-1) % len(transitions)]
        output.append(f"### 镜头 {intro_shots + i} [{avg_duration:.0f}秒]")
        output.append(f"**画面**: 内容={phase}相关内容，画面类型={shot_type}，切换={trans}")
        output.append(f"**旁白**: \"[配合画面的讲解文字，约{avg_duration * 0.8:.0f}秒]\"")
        output.append("")
    
    output.append(f"## 结尾镜头 ({outro_shots}个镜头, 约{outro_shots * avg_duration:.0f}秒)")
    output.append("")
    
    for i in range(1, outro_shots + 1):
        scene_desc = outro_scenes[i-1] if i <= len(outro_scenes) else "回顾总览"
        output.append(f"### 镜头 {intro_shots + middle_shots + i} [{avg_duration:.0f}秒]")
        output.append(f"**画面**: 场景={scene_desc}，文字=感谢观看 / Thank You")
        output.append(f"**旁白**: \"感谢观看，期待您的反馈\"")
        output.append("")
    
    output.append("## 技术参数")
    output.append("| 参数 | 值 |")
    output.append("|------|-----|")
    output.append("| 分辨率 | 1920x1080 (Full HD) |")
    output.append("| 帧率 | 30fps |")
    output.append("| 画幅比 | 16:9 |")
    output.append("| 格式 | MP4 (H.264) |")
    output.append("")
    output.append("## 制作清单")
    output.append("- [ ] 收集/录制各镜头素材")
    output.append("- [ ] 录制旁白音频")
    output.append("- [ ] 制作字幕")
    output.append("- [ ] 选取背景音乐")
    output.append("- [ ] 视频剪辑合成")
    output.append("- [ ] 校对时间轴")
    output.append("- [ ] 输出最终版本")
    output.append("")
    output.append("## 注意事项")
    output.append("1. 旁白语速: 中文约200-250字/分钟")
    output.append("2. 每个镜头首尾留0.5秒缓冲，便于剪辑")
    output.append("3. 旁白音量占比70%，音乐占比30%")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="视频脚本生成器")
    parser.add_argument("--duration", type=int, required=True, help="视频总时长（秒）")
    parser.add_argument("--scene", required=True, help="视频主题/场景描述")
    parser.add_argument("--output", help="输出文件路径（可选）")
    
    args = parser.parse_args()
    
    if args.duration < 30:
        print("警告: 视频时长过短(<30秒)，可能无法充分展示内容", file=sys.stderr)
    elif args.duration > 600:
        print("警告: 视频时长超过10分钟，建议拆分多个视频", file=sys.stderr)
    
    script = generate_video_script(args.duration, args.scene)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✅ 视频脚本已保存到: {args.output}")
    else:
        print(script)


if __name__ == "__main__":
    main()
