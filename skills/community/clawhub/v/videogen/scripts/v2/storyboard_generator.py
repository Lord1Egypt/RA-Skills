#!/usr/bin/env python3
"""
videogen v2 — Enhanced Storyboard Generator
多阶段分镜生成器（参考 waoowaoo 多 phase 架构）

Phase 1: 脚本 → 分镜计划（确定镜头数量、景别、场景类型）
Phase 2: 运镜+表演指导（并行：cinematography + acting）
Phase 3: 细节补充 + 视频 Prompt 生成

增强版分镜字段：
  - panel_number: 镜号
  - scene_type: 场景类型（剧情/知识讲解/数据展示）
  - shot_type: 景别（特写/中景/全景/远景）
  - camera_move: 镜头运动（推/拉/摇/移/固定）
  - description: 画面描述
  - video_prompt: 视频生成 Prompt（镜头控制+主体描述+场景氛围+动态元素+风格）
  - narration: 旁白/台词
  - duration: 预计时长(秒)
  - transition: 转场方式
"""

import json
import sys
import time
import os
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

# ─── 分镜数据结构 ───

@dataclass
class StoryboardPanel:
    """单个分镜面板"""
    panel_number: int        # 镜号 1, 2, 3...
    scene_type: str         # scene_type: 剧情场景 / 知识讲解 / 数据展示 / 过渡页
    shot_type: str          # shot_type: 特写 / 中景 / 全景 / 远景 / POV主观
    camera_move: str         # camera_move: 固定 / 推 / 拉 / 摇 / 移 / 跟随
    description: str         # 画面文字描述（给PPT生成/绘图AI用）
    video_prompt: str        # Hailuo 视频生成 Prompt
    narration: str           # 旁白/台词
    duration: int            # 镜头时长(秒)
    transition: str          # 转场: 硬切 / 淡入淡出 / 溶解 / 滑入


@dataclass
class ContentSegment:
    """配音/脚本段落"""
    segment_id: int
    narration: str          # 旁白文本
    duration: float          # 预计朗读时长(秒)


# ─── Prompt 模板（视频号竖屏 9:16）───

# 景别映射
SHOT_TYPES = {
    "extreme_closeup": "特写",
    "closeup": "近景/中景",
    "medium": "中景",
    "wide": "全景",
    "establishing": "远景/建立景",
    "pov": "POV主观视角",
}

CAMERA_MOVES = {
    "fixed": "固定镜头",
    "push_in": "推进（推镜头）",
    "pull_out": "拉出（拉镜头）",
    "pan_left": "左摇",
    "pan_right": "右摇",
    "tilt_up": "上摇",
    "tilt_down": "下摇",
    "dolly": "移动摄影",
    "follow": "跟随",
}

SCENE_TYPES = {
    "drama": "剧情场景",
    "knowledge": "知识讲解",
    "data": "数据展示",
    "过渡页": "过渡页",
}


# ─── 视频 Prompt 生成（参考书籍：镜头控制+主体描述+场景氛围+动态元素+风格）───

def build_video_prompt(panel: StoryboardPanel, mode: str) -> str:
    """
    构建 Hailuo 视频生成 Prompt。
    公式：镜头控制 + 主体描述 + 场景氛围 + 动态元素 + 风格
    """
    shot_map = {
        "特写": "close-up shot, shallow depth of field",
        "近景/中景": "medium close-up shot",
        "中景": "medium shot",
        "全景": "wide shot, full body visible",
        "远景/建立景": "establishing shot, wide angle",
        "POV主观视角": "POV first-person perspective",
    }
    camera_map = {
        "固定镜头": "static camera",
        "推进（推镜头）": "slow push-in, cinematic",
        "拉出（拉镜头）": "slow pull-out",
        "左摇": "pan left slowly",
        "右摇": "pan right slowly",
        "上摇": "tilt up",
        "下摇": "tilt down",
        "移动摄影": "dolly tracking shot",
        "跟随": "follow shot, smooth motion",
    }

    shot_desc = shot_map.get(panel.shot_type, "medium shot")
    camera_desc = camera_map.get(panel.camera_move, "static camera")

    # 风格化描述
    if mode == "A":
        style = "modern minimalist style, clean presentation, tech aesthetic, 9:16 vertical video"
    elif mode == "C":
        style = "cinematic drama, emotional lighting, anime/comic style, 9:16 vertical format"
    else:
        style = "modern cinematic, clean aesthetic, engaging visual, 9:16 vertical video"

    # 动态元素
    dynamic = ""
    if panel.scene_type == "剧情场景":
        dynamic = "subtle character movement, natural breathing, gentle ambient motion"
    elif panel.scene_type == "数据展示":
        dynamic = "data visualization animation, chart elements fade in smoothly"
    else:
        dynamic = "subtle motion, elegant transition, clean movement"

    prompt = f"{shot_desc}, {camera_desc}, {panel.description}, {dynamic}, {style}"
    # 限制长度
    if len(prompt) > 500:
        prompt = prompt[:497] + "..."
    return prompt


# ─── Mode A: 纯干货型分镜生成 ───

def generate_mode_a_storyboard(topic: str, narration_segments: list[ContentSegment]) -> list[StoryboardPanel]:
    """
    Mode A — 纯干货型：直接逻辑驱动
    结构：开场痛点(3s) → 核心要点1(12s) → 核心要点2(12s) → 核心要点3(12s) → 金句收尾(9s)
    """
    panels = []
    panel_num = 1

    # 读取topic提取核心关键词
    core_keywords = topic[:30] if topic else "核心观点"

    # ── 开场钩子：3s ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="过渡页",
        shot_type="远景/建立景",
        camera_move="固定镜头",
        description=f"大字标题：{core_keywords}，深色背景，简洁大气",
        video_prompt="",
        narration="",
        duration=3,
        transition="淡入淡出",
    ))
    panel_num += 1

    # ── 核心要点循环 ──
    narration_by_duration = {s.segment_id: s.narration for s in narration_segments}
    if not narration_segments:
        # 默认：生成3个要点
        narration_segments = [
            ContentSegment(1, "观点一", 12),
            ContentSegment(2, "观点二", 12),
            ContentSegment(3, "观点三", 12),
        ]

    for seg in narration_segments[:3]:
        # 数据/图表页
        panels.append(StoryboardPanel(
            panel_number=panel_num,
            scene_type="数据展示",
            shot_type="中景",
            camera_move="固定镜头",
            description=f"图表页：{seg.narration}，清晰的数据可视化，深蓝背景+金色数字",
            video_prompt="",
            narration=seg.narration,
            duration=10,
            transition="硬切",
        ))
        panel_num += 1

        # 讲解页（AI点缀）
        panels.append(StoryboardPanel(
            panel_number=panel_num,
            scene_type="知识讲解",
            shot_type="中景",
            camera_move="推进（推镜头）",
            description=f"讲解画面：{seg.narration}的核心内容，极简背景",
            video_prompt="",
            narration=f"【旁白】{seg.narration}",
            duration=seg.duration - 10 if seg.duration > 10 else 3,
            transition="溶解",
        ))
        panel_num += 1

    # ── 金句收尾 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="过渡页",
        shot_type="特写",
        camera_move="固定镜头",
        description="金句收尾：大字金句，白色字体，光芒效果，关注引导",
        video_prompt="",
        narration="感谢观看，关注我获取更多干货",
        duration=5,
        transition="淡入淡出",
    ))

    # 生成 video_prompt
    for p in panels:
        if not p.video_prompt:
            p.video_prompt = build_video_prompt(p, "A")

    return panels


# ─── Mode B: 剧情+科普型分镜生成 ───

def generate_mode_b_storyboard(topic: str, narration_segments: list[ContentSegment]) -> list[StoryboardPanel]:
    """
    Mode B — 剧情+科普型：情感开场 + 干货展开
    结构：剧情钩子(8s) → 问题拆解(15s) → 核心干货1(12s) → 核心干货2(12s) → 升华收尾(10s)
    """
    panels = []
    panel_num = 1

    # 提取话题关键词
    core = topic[:20] if topic else "核心主题"

    # ── 剧情钩子（8s）─ 用强情绪画面 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="特写",
        camera_move="固定镜头",
        description=f"一个普通人在{core}场景中的困境表情，昏暗灯光，情绪强烈",
        video_prompt="",
        narration="（音乐铺垫）",
        duration=3,
        transition="淡入淡出",
    ))
    panel_num += 1

    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="中景",
        camera_move="跟随",
        description=f"角色在关键场景中做出选择/行动，情绪饱满，叙事感强",
        video_prompt="",
        narration="【旁白引入】",
        duration=5,
        transition="滑入",
    ))
    panel_num += 1

    # ── 问题拆解（15s）─ 干净科普 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="知识讲解",
        shot_type="中景",
        camera_move="固定镜头",
        description=f"问题拆解页：{core}的核心矛盾，简洁图表+关键词",
        video_prompt="",
        narration="【问题拆解】",
        duration=15,
        transition="溶解",
    ))
    panel_num += 1

    # ── 核心干货（×2）─ 剧情+知识交替 ──
    if not narration_segments:
        narration_segments = [
            ContentSegment(1, "第一个核心干货", 12),
            ContentSegment(2, "第二个核心干货", 12),
        ]

    for seg in narration_segments[:2]:
        # 剧情演绎
        panels.append(StoryboardPanel(
            panel_number=panel_num,
            scene_type="剧情场景",
            shot_type="中景",
            camera_move="推进（推镜头）",
            description=f"角色在场景中实践/展示{seg.narration}，自然光，真实感强",
            video_prompt="",
            narration=f"【剧情】",
            duration=5,
            transition="硬切",
        ))
        panel_num += 1

        # 知识要点
        panels.append(StoryboardPanel(
            panel_number=panel_num,
            scene_type="知识讲解",
            shot_type="全景",
            camera_move="固定镜头",
            description=f"关键要点：{seg.narration}，图表/数据支持，视觉清晰",
            video_prompt="",
            narration=f"【干货】{seg.narration}",
            duration=7,
            transition="溶解",
        ))
        panel_num += 1

    # ── 升华收尾 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="特写",
        camera_move="固定镜头",
        description=f"角色蜕变/成功后的表情/状态，金句大字，光影感强",
        video_prompt="",
        narration="【升华金句】",
        duration=5,
        transition="淡入淡出",
    ))
    panel_num += 1

    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="过渡页",
        shot_type="远景/建立景",
        camera_move="固定镜头",
        description="关注引导页，简洁有力",
        video_prompt="",
        narration="关注我，继续分享更多...",
        duration=3,
        transition="淡入淡出",
    ))

    # 生成 video_prompt
    for p in panels:
        if not p.video_prompt:
            p.video_prompt = build_video_prompt(p, "B")

    return panels


# ─── Mode C: 漫剧型分镜生成 ───

def generate_mode_c_storyboard(topic: str) -> list[StoryboardPanel]:
    """
    Mode C — 漫剧/剧情型：完整故事弧线
    结构：起(8s) → 承(12s) → 转(20s) → 合(8s) + 金句收尾
    """
    panels = []
    panel_num = 1

    core = topic[:20] if topic else "故事主题"

    # ── 起始：建立人物处境 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="远景/建立景",
        camera_move="固定镜头",
        description=f"建立场景：普通人平凡的一天，压抑感，灰色调",
        video_prompt="",
        narration="【旁白】他曾经...",
        duration=4,
        transition="淡入淡出",
    ))
    panel_num += 1

    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="中景",
        camera_move="跟随",
        description=f"关键事件爆发：{core}的至暗时刻，情绪强烈",
        video_prompt="",
        narration="【转折点】",
        duration=4,
        transition="硬切",
    ))
    panel_num += 1

    # ── 承接：内心挣扎 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="特写",
        camera_move="固定镜头",
        description="角色面部特写：迷茫/痛苦的情绪流露",
        video_prompt="",
        narration="【内心独白】",
        duration=4,
        transition="溶解",
    ))
    panel_num += 1

    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="中景",
        camera_move="推进（推镜头）",
        description="做出决定/行动的一刻，光线开始变化",
        video_prompt="",
        narration="【决定】",
        duration=4,
        transition="滑入",
    ))
    panel_num += 1

    # ── 转折：行动/改变（最多镜头）──
    # 行动序列
    for i in range(3):
        panels.append(StoryboardPanel(
            panel_number=panel_num,
            scene_type="剧情场景",
            shot_type="中景",
            camera_move="移动摄影" if i == 1 else "固定镜头",
            description=f"行动场景{i+1}：努力/学习/坚持的片段，节奏加快",
            video_prompt="",
            narration=f"【行动{i+1}】",
            duration=4,
            transition="硬切",
        ))
        panel_num += 1

    # ── 结局：蜕变成功 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="剧情场景",
        shot_type="中景",
        camera_move="拉出（拉镜头）",
        description="蜕变完成：新的状态/场景，温暖色调，光影希望感",
        video_prompt="",
        narration="【结果】",
        duration=4,
        transition="溶解",
    ))
    panel_num += 1

    # ── 金句升华 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="过渡页",
        shot_type="特写",
        camera_move="固定镜头",
        description="金句大字：励志核心观点，金色光效，有力量感",
        video_prompt="",
        narration="【金句】",
        duration=4,
        transition="淡入淡出",
    ))
    panel_num += 1

    # ── 关注引导 ──
    panels.append(StoryboardPanel(
        panel_number=panel_num,
        scene_type="过渡页",
        shot_type="远景/建立景",
        camera_move="固定镜头",
        description="账号引导，关注按钮",
        video_prompt="",
        narration="关注我...",
        duration=3,
        transition="淡入淡出",
    ))

    # 生成 video_prompt
    for p in panels:
        if not p.video_prompt:
            p.video_prompt = build_video_prompt(p, "C")

    return panels


# ─── 主入口 ───

def generate_storyboard(
    topic: str,
    mode: str,
    narration_segments: Optional[list[ContentSegment]] = None,
    total_duration: int = 60,
) -> dict:
    """
    统一入口：根据 mode 生成增强分镜
    
    Args:
        topic: 选题/主题
        mode: "A" | "B" | "C"
        narration_segments: 配音段落列表（可选）
        total_duration: 目标总时长(秒)
    
    Returns:
        dict: {
            "mode": str,
            "panels": list[dict],  # asdict(StoryboardPanel)
            "summary": {
                "total_panels": int,
                "total_duration": int,
                "mode": str,
            }
        }
    """
    if narration_segments is None:
        # 根据目标时长估算段落
        seg_count = max(2, min(5, total_duration // 20))
        narration_segments = [
            ContentSegment(i, f"核心要点{i}", 12) for i in range(1, seg_count + 1)
        ]

    if mode == "A":
        panels = generate_mode_a_storyboard(topic, narration_segments)
    elif mode == "B":
        panels = generate_mode_b_storyboard(topic, narration_segments)
    elif mode == "C":
        panels = generate_mode_c_storyboard(topic)
    else:
        panels = generate_mode_a_storyboard(topic, narration_segments)

    # 计算实际总时长
    actual_duration = sum(p.duration for p in panels)

    return {
        "mode": mode,
        "topic": topic,
        "panels": [asdict(p) for p in panels],
        "summary": {
            "total_panels": len(panels),
            "total_duration": actual_duration,
            "mode": mode,
            "mode_description": {
                "A": "纯干货型",
                "B": "剧情+科普型",
                "C": "漫剧/剧情型",
            }.get(mode, ""),
        }
    }


def save_storyboard(result: dict, output_path: str):
    """保存分镜结果到 JSON 文件"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"分镜已保存: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("用法: python storyboard_generator.py <topic> <mode> [output_json]")
        print("  mode: A=纯干货, B=剧情+科普, C=漫剧型")
        sys.exit(1)

    topic = sys.argv[1]
    mode = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else "minimax-output/storyboard.json"

    result = generate_storyboard(topic, mode)
    save_storyboard(result, output)

    # 打印摘要
    print(f"\n=== 分镜生成完成 ===")
    print(f"模式: Mode {result['mode']} ({result['summary']['mode_description']})")
    print(f"总镜头数: {result['summary']['total_panels']}")
    print(f"预计时长: {result['summary']['total_duration']}s")

    # 打印分镜表
    print(f"\n{'镜号':>4} {'场景':8} {'景别':8} {'时长':>4}s {'转场':8} 画面描述")
    print("-" * 90)
    for p in result["panels"]:
        desc = p["description"][:30]
        print(f"{p['panel_number']:>4} {p['scene_type']:8} {p['shot_type']:8} "
              f"{p['duration']:>4}s {p['transition']:8} {desc}")


if __name__ == "__main__":
    main()
