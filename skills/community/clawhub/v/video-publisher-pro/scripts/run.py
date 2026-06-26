# -*- coding: utf-8 -*-
import os
import sys
import argparse
import json

# 这是一个逻辑技能，核心是调用一个子代理来执行任务。
# 这个脚本的职责是接收参数，并构建发送给子代理的最终指令。

def read_prompt_template():
    """读取指令模板文件"""
    # 使用相对路径定位模板文件，确保技能的可移植性
    script_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_dir, '..', 'prompt_template.txt')
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误: 模板文件未找到，路径: {template_path}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="为 video-publisher-pro 技能准备并打印最终的指令。")
    parser.add_argument('--background', required=True, help='客户背景信息')
    parser.add_argument('--plan', required=True, help='本周计划或战略目标')
    parser.add_argument('--script', required=True, help='视频文案')
    parser.add_argument('--position', required=True, help='视频定位')

    args = parser.parse_args()

    # 读取模板
    prompt_template = read_prompt_template()

    # 将用户输入填充到模板中
    final_prompt = prompt_template.replace('[请在此处粘贴客户背景信息，包括：IP定位、核心价值观、目标用户画像、已发布视频的平均表现等]', args.background)
    final_prompt = final_prompt.replace('[请在此处粘贴本周的周计划或核心目标。这能帮助AI理解本条视频在整体策略中的位置和作用]', args.plan)
    final_prompt = final_prompt.replace('[请在此处粘贴完整的视频文案，最好能标注出关键情绪点或转折点]', args.script)
    final_prompt = final_prompt.replace('[请在此处填写这是第几条视频，并说明其在发布序列中的作用。例如：第一条，人设定位视频，用于账号冷启动；或：第三条，干货教学视频，用于建立专业信任]', args.position)

    # 实际场景中，这里会调用 openclaw sessions_spawn
    # 为简化演示，我们先将最终构建好的指令打印出来，以供模型在下一步中调用
    
    # 将最终的prompt封装为OpenClaw工具能识别的JSON格式
    output_for_openclaw = {
        "tool_code": f"sessions_spawn(task='{json.dumps(final_prompt)}', agentId='sub-agent-text-strategist')"
    }
    
    # 实际应用中会直接执行，这里我们打印出来给主模型看
    print(json.dumps(output_for_openclaw, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
