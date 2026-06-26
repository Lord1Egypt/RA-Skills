# -*- coding: utf-8 -*-
"""
Video Transition 使用示例
"""

from video_transition import (
    apply_transition,
    concat_with_transitions,
    add_fade_to_video,
    add_fade_to_clips,
    list_transitions
)


def example_1_basic_transition():
    """示例1：基本转场效果"""
    print("=" * 50)
    print("示例1：两个视频之间的转场")
    print("=" * 50)
    
    apply_transition(
        video1="intro.mp4",
        video2="main.mp4",
        output="merged.mp4",
        transition="fade",      # 淡入淡出
        duration=0.5            # 转场时长 0.5 秒
    )
    
    print("完成：merged.mp4")


def example_2_concat_with_transitions():
    """示例2：合并多个视频并添加转场"""
    print("=" * 50)
    print("示例2：合并多个视频")
    print("=" * 50)
    
    video_paths = [
        "clip1.mp4",
        "clip2.mp4",
        "clip3.mp4",
        "clip4.mp4"
    ]
    
    concat_with_transitions(
        video_paths=video_paths,
        output_path="final.mp4",
        transition_duration=0.5,
        transitions=["fade", "slideleft", "slideright", "circleopen"]
    )
    
    print("完成：final.mp4")


def example_3_add_fade():
    """示例3：添加淡入淡出"""
    print("=" * 50)
    print("示例3：为视频添加淡入淡出")
    print("=" * 50)
    
    add_fade_to_video(
        video_path="input.mp4",
        output_path="output.mp4",
        fade_in=0.3,    # 淡入 0.3 秒
        fade_out=0.3    # 淡出 0.3 秒
    )
    
    print("完成：output.mp4")


def example_4_batch_fade():
    """示例4：批量添加淡入淡出"""
    print("=" * 50)
    print("示例4：批量处理")
    print("=" * 50)
    
    output_paths = add_fade_to_clips(
        input_dir="clips/",
        output_dir="faded/",
        fade_in=0.3,
        fade_out=0.3
    )
    
    print(f"处理了 {len(output_paths)} 个视频")


def example_5_list_transitions():
    """示例5：列出所有转场效果"""
    print("=" * 50)
    print("支持的转场效果")
    print("=" * 50)
    
    transitions = list_transitions()
    for name, desc in transitions.items():
        print(f"  {name}: {desc}")


if __name__ == "__main__":
    print("\n视频转场工具示例\n")
    
    # 列出所有转场效果
    example_5_list_transitions()
    
    # 其他示例（需要实际视频文件）
    # example_1_basic_transition()
    # example_2_concat_with_transitions()
    # example_3_add_fade()
    # example_4_batch_fade()
