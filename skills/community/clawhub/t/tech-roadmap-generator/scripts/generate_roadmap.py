#!/usr/bin/env python3
"""
技术路线图自动生成器 - 核心渲染引擎
Tech Roadmap Generator - Core Rendering Engine

支持10种学术技术路线图模板，输出高质量SVG。
"""

import json
import argparse
import sys
import os
import re
import textwrap
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

# ============================================================
# 配色方案定义
# ============================================================

THEMES = {
    "classic": {
        "header": "#F5B875",       # 橙色标题栏
        "node": "#C8E6C9",          # 浅绿内容节点
        "stage_label": "#A5D6A7",   # 阶段标签
        "area_bg": "#FAFAFA",       # 区域背景
        "arrow": "#333333",         # 箭头
        "text": "#333333",          # 文字
        "border": "#888888",        # 边框
        "chapter_label": "#E8B4B4", # 章节标签
        "sub_header": "#FFCC80",    # 二级标题
    },
    "bluegray": {
        "header": "#7B9CB8",
        "node": "#E0E0E0",
        "stage_label": "#90CAF9",
        "area_bg": "#F0F4F8",
        "arrow": "#444444",
        "text": "#333333",
        "border": "#999999",
        "chapter_label": "#B39DDB",
        "sub_header": "#B0BEC5",
    },
    "navy": {
        "header": "#5B7F9A",
        "node": "#C8E6C9",
        "stage_label": "#90CAF9",
        "area_bg": "#F5F7FA",
        "arrow": "#2C3E50",
        "text": "#222222",
        "border": "#7B9CB8",
        "chapter_label": "#90A4AE",
        "sub_header": "#81C784",
    },
    "survey": {
        "header": "#5B9BD5",
        "node": "#FFF2CC",
        "stage_label": "#9CCC65",
        "area_bg": "#E8F5E9",
        "arrow": "#66BB6A",
        "text": "#333333",
        "border": "#AED581",
        "chapter_label": "#FFCC80",
        "sub_header": "#FFEB3B",
    },
}

# ============================================================
# 数据结构
# ============================================================

@dataclass
class Node:
    """内容节点"""
    text: str
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

@dataclass
class Stage:
    """研究阶段"""
    name: str
    items: List[str] = field(default_factory=list)
    sub_stages: List[Dict] = field(default_factory=list)  # 子阶段
    sub_items: List[List[str]] = field(default_factory=list)  # 每个item的子项
    header_text: str = ""
    left_label: str = ""
    right_label: str = ""

@dataclass
class RoadmapData:
    """路线图完整数据"""
    title: str = ""
    stages: List[Stage] = field(default_factory=list)
    conclusion: str = "结论与展望"
    theme: str = "classic"

# ============================================================
# SVG 渲染工具函数
# ============================================================

def svg_rect(x, y, w, h, fill, stroke="#333", stroke_width=1.5, rx=4, **attrs):
    """生成SVG矩形"""
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{extra}/>'

def svg_rounded_rect(x, y, w, h, fill, stroke="#333", stroke_width=1.2, rx=4):
    """圆角矩形"""
    return svg_rect(x, y, w, h, fill, stroke, stroke_width, rx)

def svg_text(x, y, text, size=12, color="#333", anchor="middle", bold=False, **attrs):
    """SVG文本"""
    weight = "bold" if bold else "normal"
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    # XML escape
    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Microsoft YaHei, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}"{extra}>{safe_text}</text>'

def svg_line(x1, y1, x2, y2, color="#333", width=1.5, **attrs):
    """SVG直线"""
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"{extra}/>'

def svg_arrow_down(cx, y1, y2, color="#333", head_size=10, width=2):
    """向下箭头"""
    return (
        f'<line x1="{cx:.1f}" y1="{y1:.1f}" x2="{cx:.1f}" y2="{y2-head_size:.1f}" stroke="{color}" stroke-width="{width}"/>'
        f'<polygon points="{cx:.1f},{y2:.1f} {cx-head_size/2:.1f},{y2-head_size:.1f} {cx+head_size/2:.1f},{y2-head_size:.1f}" fill="{color}"/>'
    )

def svg_arrow_right(x1, cx, y, color="#333", head_size=8, width=1.5):
    """向右箭头"""
    return (
        f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{cx-head_size:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="{width}"/>'
        f'<polygon points="{cx:.1f},{y:.1f} {cx-head_size:.1f},{y-head_size/2:.1f} {cx-head_size:.1f},{y+head_size/2:.1f}" fill="{color}"/>'
    )

def svg_dashed_rect(x, y, w, h, stroke="#888", dash="6,4", sw=1.5, **attrs):
    """虚线矩形"""
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"{extra}/>'

def measure_text(text, size=12, max_width=None):
    """估算文本尺寸（中文字符约等于字号宽度）"""
    if not text:
        return 0, size
    # 中文字符宽度 ≈ size，英文 ≈ size*0.55
    width = sum(size if ord(c) > 127 else size * 0.55 for c in text)
    if max_width and width > max_width:
        lines = len(textwrap.wrap(text, int(max_width / (size * 0.6))))
        return max_width, size * lines
    return width, size * 1.3

def wrap_text(text, max_chars=10):
    """将长文本按字符数换行"""
    if len(text) <= max_chars:
        return text
    result = []
    while text:
        if len(text) <= max_chars:
            result.append(text)
            break
        # 尝试在max_chars处断行
        result.append(text[:max_chars])
        text = text[max_chars:]
    return "\n".join(result)

# ============================================================
# 内容自动生成引擎
# ============================================================

def generate_content_from_title(title: str, template_id: str) -> RoadmapData:
    """根据研究主题自动生成路线图内容"""
    data = RoadmapData(title=title)

    # 提取关键词（简单处理）
    short_name = title.replace("研究", "").replace("分析", "")[:6]

    if template_id == "template-21":
        data.theme = "classic"
        data.stages = [
            Stage("提出问题", [f"{short_name}背景与意义", "国内外研究现状", f"研究对象界定", "研究方法设计"],
                  left_label="提出问题", right_label="第一章"),
            Stage("研究基础", [f"{short_name}相关理论", f"{short_name}内涵界定", f"{short_name}影响因素分析"],
                  left_label="研究基础", right_label="第二章"),
            Stage("分析问题", sub_stages=[
                {"name": f"{short_name}发展情况", "items": ["现状调查1", "现状调查2", "现状调查3"]},
                {"name": f"{short_name}问题分析", "items": ["维度一分析", "维度二分析", "维度三分析"]},
                {"name": "深层原因", "items": ["原因一", "原因二", "原因三"]}
            ], left_label="分析问题", right_label="第三章"),
            Stage("解决策略",
                  items=[f"外部环境优化", "核心机制创新", "保障体系完善", "实施路径设计"],
                  sub_items=[["政策1","制度2","资源3"], ["机制1","机制2"], ["体系1","体系2","体系3","体系4"], ["步骤1","步骤2","步骤3"]],
                  left_label="解决问题", right_label="第四章"),
        ]
        data.conclusion = "结论与展望"

    elif template_id == "template-18":
        data.theme = "navy"
        data.stages = [
            Stage("绪论", [f"{short_name}研究背景", f"研究目的与意义"], header_text="绪论"),
            Stage("现状分析", [f"{short_name}发展现状", f"主要表现", f"基本特征"],
                  sub_stages=[{"name":"发现现状","items":["表现1","表现2","表现3"]}],
                  header_text=f"{short_name}现状"),
            Stage("理论研究",
                  sub_stages=[
                      {"name": "原因分析", "items": ["因素一", "因素二", "因素三"]},
                      {"name": "逻辑关系", "items": ["逻辑1", "逻辑2", "逻辑3"]}
                  ], header_text="理论研究"),
            Stage("技术路径", [f"路径一{short_name}", f"路径二{short_name}", f"路径三{short_name}",
                              f"路径四{short_name}", f"路径五{short_name}", f"路径六{short_name}"],
                  header_text="技术路径"),
            Stage("结论", [f"主要结论1", f"主要结论2", f"主要结论3"], header_text="结论"),
        ]

    elif template_id == "template-19":
        data.theme = "bluegray"
        data.stages = [
            Stage("提出问题", [f"{short_name}背景与意义", f"研究现状综述", f"研究对象", f"研究方法"]),
            Stage("研究基础", [f"{short_name}概念界定", f"{short_name}理论基础", f"{short_name}框架构建"]),
            Stage(f"{short_name}特征与问题分析",
                  sub_stages=[
                      {"name": f"{short_name}情况", "items": ["基础1","基础2","基础3","基础4"]},
                      {"name": f"{short_name}分析", "items": ["基础1","基础2","基础3","基础4","基础5","基础6"]},
                      {"name": f"{short_name}关键问题", "items": ["基础1","基础2","基础3"]}
                  ]),
            Stage("解决策略",
                  items=[f"环境层面", f"机制层面", f"操作层面", f"评价层面"],
                  sub_items=[["策1","策2","策3"],["策1","策2"],["策1","策2","策3","策4"],["策1","策2","策3"]]),
        ]
        data.conclusion = "结论与展望"

    elif template_id == "template-27":
        data.theme = "classic"
        data.stages = [
            Stage("分析问题", [], header_text=f"{short_name}特征、影响及成因分析 @{short_name}", left_label="分析问题"),
            Stage("理论基础", [], header_text=f"生发{short_name}理论内涵", left_label="理论基础",
                  sub_stages=[{"name":"@小紅书；小白龙大智慧","items":["","",""]}]),
            Stage("实证检验",
                  items=["假设内容/数据基础1", "假设内容/数据基础2", "假设内容/数据基础3", "假设内容/数据基础4"],
                  header_text="实证内容1", left_label="实证检验"),
            Stage("引导政策",
                  header_text=f"政策建议@{short_name}；小白龙大智慧",
                  items=[f"完善{short_name}制度", f"改革{short_name}政策", f"推动{short_name}发展"],
                  left_label="引导政策"),
        ]
        data.conclusion = ""

    elif template_id == "template-24":
        data.theme = "navy"
        data.stages = [
            Stage("研究背景", header_text=f"研究背景：{short_name}",
                  items=["政策背景", "发展趋势", "问题重要性"]),
            Stage("提出问题", header_text=f"提出问题：{short_name} @{short_name}；小白龙大智慧"),
            Stage("分析问题", header_text=f"研究内容1：{short_name} @{short_name}；小白龙大智慧",
                  items=["", "", "", "", "", "具体问题1", "具体问题1"]),
            Stage("解决问题", header_text=f"{short_name}机理研究 @{short_name}; 小白龙大智慧"),
            Stage("政策建议", header_text=f"机理分析和政策建议 @{short_name}；小白龙大智慧",
                  items=["政策建议1", "政策建议2", "政策建议3"]),
        ]
        data.conclusion = ""

    elif template_id == "template-17":
        data.theme = "navy"
        data.stages = [
            Stage("绪论", [f"{short_name}研究背景", "研究目的与意义"], header_text="绪论",
                  right_label="文献分析法\n实际调研法\n深度访谈法"),
            Stage("现状分析", [f"{short_name}发展现状", "主要表现", "基本特征"], header_text="绪论",
                  right_label="文献分析法\n实际调研法\n深度访谈法"),
            Stage("理论研究",
                  sub_stages=[
                      {"name": "原因", "items": ["成因1", "成因2", "成因3"]},
                      {"name": "逻辑", "items": ["逻辑1", "逻辑2", "逻辑3"]}
                  ], header_text="理论研究",
                  right_label="案例研究法\n比较研究法\n专家咨询法\n归纳分析法"),
            Stage("技术路径", [f"路径一", f"路径二", f"路径三", f"路径四", f"路径五"],
                  header_text="技术路径",
                  right_label="案例研究法\n比较研究法\n专家咨询法"),
            Stage("结论", [f"结论一", f"结论二", f"结论三"], header_text="结论",
                  right_label="案例研究法\n比较研究法\n专家咨询法"),
        ]

    elif template_id == "template-16":
        data.theme = "classic"
        data.stages = [
            Stage("提出问题", [f"研究背景", f"研究目的", f"研究内容"], left_label="提出问题"),
            Stage("理论基础", [f"{short_name}理论1", f"{short_name}理论2", f"{short_name}理论3"],
                  header_text=f"{short_name}理论基础", left_label="理论基础"),
            Stage("现状分析", [f"现状维度1", f"现状维度2", f"现状维度3", f"现状维度4"],
                  header_text=f"{short_name}现状分析", left_label="现状分析"),
            Stage("案例分析", [f"案例一{short_name}", f"案例二{short_name}", f"案例三{short_name}"],
                  header_text=f"{short_name}案例分析", left_label="案例分析"),
            Stage("改进建议", [f"建议方向1", f"建议方向2", f"建议方向3", f"建议方向4", f"建议方向5"],
                  header_text=f"{short_name}改进建议", left_label="理论基础"),
        ]
        data.conclusion = f"{short_name}研究结论"

    elif template_id in ("template-15a", "template-15b"):
        data.theme = "navy"
        data.stages = [
            Stage("综述", header_text="绪论", left_label="综述"),
            Stage(f"{short_name}模型构建",
                  sub_stages=[
                      {"name": f"{short_name}理论基础", "items": [f"理论分支1", f"理论分支2", f"理论分支3", f"理论分支4"]},
                      {"name": f"{short_name}理论基础(下层)", "items": [f"子理论1", f"子理论2", f"子理论3"]}
                  ], left_label=f"{short_name}\n模型构建"),
            Stage("模型评价分析",
                  items=["评价维度1", "评价维度2", "评价维度3", "评价维度4"],
                  sub_items=[
                      ["理论1","理论2","理论3","理论4","理论5"],
                      ["理论1","理论2","理论3","theory4","th5"],
                      ["理论1","理论2","理论3","t4","t5"],
                      ["理论1","理论2"]
                  ],
                  left_label="模型评价分析"),
            Stage("策略应用",
                  items=[f"{short_name}原则", f"{short_name}策略", f"{short_name}模式"],
                  header_text=f"{short_name}理论基础",
                  left_label="策略应用"),
        ]
        data.conclusion = "结论"

    elif template_id == "template-survey":
        data.theme = "survey"
        data.stages = [
            Stage("初期准备", ["调查研究背", "查找文献", "确定研究方"], left_label="初期准备",
                  right_label="SPSS 分析"),
            Stage("问卷调查", ["设计问卷", "发放问卷", "收集问卷"], left_label="问卷调查",
                  right_label=f"剔 XXX 有\n效数据"),
            Stage("数据分析",
                  sub_stages=[
                      {"name": "信效度分析", "items": [f"信度 XXX 分析", f"效度 XX 分析"]},
                      {"name": "现状分析", "items": [f"XXX 值分析", f"XXX 偏差分析"]},
                      {"name": "差异比较", "items": [f"xxx 差异比较", f"xxx 差异比较"]},
                      {"name": "相关性分析", "items": [f"xxx 相关分析", f"多变 XXX 关分析"]},
                      {"name": "影响因素分析", "items": ["线性回归", "XX 分析"]}
                  ],
                  sub_items=[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
                  left_label="数据分析",
                  right_label="满足条件\n满足条件"),
        ]
        data.conclusion = "结合现实分析并反思总结"
        data.conclusion_right = "展望未来"

    return data

# ============================================================
# 模板渲染器
# ============================================================

class SVGRenderer:
    """SVG渲染基类"""

    def __init__(self, data: RoadmapData, width=1000):
        self.data = data
        self.width = width
        self.theme = THEMES.get(data.theme, THEMES["classic"])
        self.elements: List[str] = []
        self.height = 0
        self.margin = 20

    def add(self, elem):
        self.elements.append(elem)

    def render(self) -> str:
        svg_content = "\n".join(self.elements)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
<defs>
  <style>
    text {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; }}
  </style>
</defs>
<!-- 背景 -->
<rect width="100%" height="100%" fill="#FFFFFF"/>
{svg_content}
</svg>'''

    def save(self, path: str):
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.render())
        print(f"[OK] SVG saved to: {path}")
        return path


class Template21Renderer(SVGRenderer):
    """
    模板1: 四阶段经典版 (技术线路图-21彩色)
    结构: 左侧标签 + 虚线区域 + 右侧章节编号
    """

    def __init__(self, data: RoadmapData):
        super().__init__(data, width=1050)
        self.label_w = 50   # 左侧标签宽
        self.right_w = 55   # 右侧章节宽
        self.content_x = self.label_w + 15
        self.content_w = self.width - self.content_x - self.right_w - 15
        self.y = 15

    def draw_stage_area(self, stage: Stage, area_h: float):
        """绘制一个完整的阶段区域"""
        t = self.theme
        x = self.content_x
        y = self.y
        w = self.content_w

        # 虚线区域背景
        self.add(svg_dashed_rect(x, y, w, area_h, t["area_bg"], sw=1.2))

        # 左侧标签
        label_lines = stage.left_label or stage.name
        ly = y + area_h / 2
        self.add(svg_rounded_rect(3, ly - 25, self.label_w - 6, 50, t["stage_label"], t["border"]))
        for i, line in enumerate(label_lines.split("\n")):
            self.add(svg_text(3 + self.label_w/2, ly - 5 + (i - (len(label_lines.split("\n"))-1)/2) * 16,
                             line, size=12, color=t["text"], bold=True))

        # 右侧章节标签
        if stage.right_label:
            rx = self.width - self.right_w + 3
            self.add(svg_rounded_rect(rx, ly - 25, self.right_w - 6, 50, t["chapter_label"], t["border"]))
            for i, line in enumerate(stage.right_label.split("\n")):
                self.add(svg_text(rx + (self.right_w-6)/2, ly - 5 + (i - (len(stage.right_label.split("\n"))-1)/2) * 16,
                                 line, size=11, color=t["text"], bold=True))

        return y

    def render_roadmap(self):
        t = self.theme
        node_w = (self.content_w - 30) // 4  # 每个节点宽度
        node_h = 36
        self.y = 15

        stage_heights = []

        for si, stage in enumerate(self.data.stages):
            start_y = self.y

            # 计算此阶段高度
            if stage.header_text:
                # 有标题头
                header_h = 34
                items_h = 45
            else:
                header_h = 0
                items_h = 42

            sub_h = 0
            if stage.sub_stages:
                sub_h = len(stage.sub_stages) * 60 + 20
            elif stage.items:
                items_row = max(len(stage.items), 1)
                items_h = 45 if items_row <= 4 else 70

            if stage.sub_items and any(stage.sub_items):
                # 有子项的复杂布局
                sub_h = max(sub_h, 80)

            total_h = 10 + header_h + items_h + sub_h + 15

            # 绘制区域
            self.draw_stage_area(stage, total_h)

            cx = self.content_x + self.content_w / 2
            content_top = self.y + 10

            # 绘制标题头
            if stage.header_text:
                hw = min(len(stage.header_text) * 16 + 40, self.content_w - 30)
                hx = cx - hw / 2
                self.add(svg_rounded_rect(hx, content_top, hw, 30, t["header"], t["border"]))
                self.add(svg_text(cx, content_top + 21, stage.header_text, size=14, color=t["text"], bold=True))
                content_top += 38

            # 绘制子阶段或项目
            if stage.sub_stages:
                for sub in stage.sub_stages:
                    # 子标题
                    sub_title_w = len(sub["name"]) * 14 + 24
                    stx = cx - sub_title_w / 2
                    self.add(svg_rounded_rect(stx, content_top, sub_title_w, 28, t["header"], t["border"], rx=3))
                    self.add(svg_text(cx, content_top + 19, sub["name"], size=12, color=t["text"], bold=True))
                    content_top += 33

                    # 子项
                    n_items = len(sub["items"])
                    item_spacing = min(node_w + 8, (self.content_w - 40) / n_items)
                    total_item_w = n_items * node_w + (n_items - 1) * 8
                    start_x = cx - total_item_w / 2

                    for ji, item in enumerate(sub["items"]):
                        ix = start_x + ji * (node_w + 8)
                        self.add(svg_rounded_rect(ix, content_top, node_w, node_h, t["node"], t["border"]))
                        display_text = wrap_text(item, 8)
                        lines = display_text.count("\n") + 1
                        ty = content_top + node_h/2 + 4 + (lines - 1) * (-7)
                        self.add(svg_text(ix + node_w/2, ty, display_text, size=10, color=t["text"]))

                        # 连接线到子标题
                        if ji == 0 or ji == n_items - 1 or n_items <= 2:
                            pass  # 简化

                    content_top += node_h + 12

            elif stage.items:
                n_items = len(stage.items)
                if n_items > 4:
                    # 多行布局
                    cols = min(n_items, 4)
                    rows = (n_items + cols - 1) // cols
                    item_sp = (self.content_w - 30) / cols
                    node_w2 = item_sp - 8

                    for ri in range(rows):
                        row_start = cx - (min(cols, n_items - ri*cols) * item_sp) / 2
                        for ci in range(min(cols, n_items - ri*cols)):
                            idx = ri * cols + ci
                            if idx >= n_items:
                                break
                            ix = self.content_x + 18 + ci * item_sp
                            iy = content_top + ri * 48
                            self.add(svg_rounded_rect(ix, iy, node_w2, 34, t["node"], t["border"]))
                            self.add(svg_text(ix + node_w2/2, iy + 22, wrap_text(stage.items[idx], 8),
                                             size=10, color=t["text"]))
                    content_top += rows * 48 + 5
                else:
                    # 单行布局
                    item_spacing = (self.content_w - 30) / n_items
                    node_w2 = item_spacing - 10
                    start_x = self.content_x + 18

                    for ji, item in enumerate(stage.items):
                        ix = start_x + ji * item_spacing
                        self.add(svg_rounded_rect(ix, content_top, node_w2, node_h, t["node"], t["border"]))
                        self.add(svg_text(ix + node_w2/2, content_top + 23, wrap_text(item, 8),
                                         size=10, color=t["text"]))
                    content_top += node_h + 8

                # 处理有子项的情况（如"解决策略"阶段）
                if stage.sub_items and any(stage.sub_items):
                    content_top += 5
                    parent_n = len(stage.items)
                    p_spacing = (self.content_w - 30) / parent_n

                    for pi in range(parent_n):
                        px = self.content_x + 18 + pi * p_spacing
                        pw = p_spacing - 10
                        subs = stage.sub_items[pi] if pi < len(stage.sub_items) else []
                        if subs:
                            n_subs = len(subs)
                            sw = min(pw - 4, 52) if n_subs > 2 else pw - 4
                            sx = px + (pw - n_subs * sw - (n_subs-1)*3) / 2
                            for sci, sub in enumerate(subs):
                                sxi = sx + sci * (sw + 3)
                                sh = 32
                                sy = content_top
                                self.add(svg_rounded_rect(sxi, sy, sw, sh, t["node"], t["border"], rx=2))
                                self.add(svg_text(sxi + sw/2, sy + 21, wrap_text(sub, 5), size=9, color=t["text"]))
                                # 连接线
                                py_center = content_top - 10
                                self.add(svg_line(px + pw/2, py_center, sxi + sw/2, sy, t["arrow"], width=1))
                    content_top += 40

            self.y = start_y + total_h

            # 阶段间箭头
            if si < len(self.data.stages) - 1:
                arrow_y = self.y
                self.add(svg_arrow_down(self.content_x + self.content_w/2, arrow_y, arrow_y + 18,
                                         t["arrow"], head_size=12, width=2.5))
                self.y += 22

        # 结论部分
        if self.data.conclusion:
            self.y += 5
            cw = min(len(self.data.conclusion) * 18 + 60, self.content_w - 20)
            cx = self.content_x + self.content_w / 2
            self.add(svg_rounded_rect(cx - cw/2, self.y, cw, 36, t["stage_label"], t["border"]))
            self.add(svg_text(cx, self.y + 23, self.data.conclusion, size=14, color=t["text"], bold=True))
            self.y += 46

        self.height = self.y + 15


class Template18Renderer(SVGRenderer):
    """
    模板2: 研究脉络纵向版 (技术线路图-18彩色)
    结构: 左侧蓝色导航条 + 虚线区域 + 向下流程
    """

    def __init__(self, data: RoadmapData):
        super().__init__(data, width=750)
        self.nav_w = 55      # 左导航宽
        self.content_x = self.nav_w + 12
        self.content_w = self.width - self.content_x - 15
        self.y = 12

    def render_roadmap(self):
        t = self.theme
        node_w, node_h = 95, 38
        self.y = 12

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            # 计算高度
            h = 35  # 标题
            if stage.header_text:
                h += 34
            if stage.sub_stages:
                h += len(stage.sub_stages) * (38 + 40) + 10
            elif stage.items:
                n = len(stage.items)
                cols = min(n, 6)
                rows = (n + cols - 1) // cols
                h += rows * (node_h + 6) + 8
            h += 12

            # 左侧导航标签
            label_text = stage.left_label or stage.name
            nav_h = h - 10
            self.add(svg_rounded_rect(4, start_y + 5, self.nav_w - 8, nav_h, t["stage_label"], t["border"], rx=5))

            # 导航文字（竖排或横排）
            lines = label_text.split("\n")
            for i, ln in enumerate(lines):
                ny = start_y + 5 + nav_h/2 + (i - (len(lines)-1)/2) * 16
                self.add(svg_text(4 + (self.nav_w-8)/2, ny, ln, size=11, color=t["text"], bold=True))

            # 虚线区域
            ax = self.content_x
            self.add(svg_dashed_rect(ax, start_y, self.content_w, h, t["area_bg"]))

            ct = start_y + 10

            # 阶段标题
            if stage.header_text:
                hw = min(len(stage.header_text)*15+30, self.content_w-20)
                hx = ax + (self.content_w-hw)/2
                self.add(svg_rounded_rect(hx, ct, hw, 30, t["header"], t["border"]))
                self.add(svg_text(hx + hw/2, ct + 21, stage.header_text, size=13, color=t["text"], bold=True))
                ct += 38

            # 子阶段
            if stage.sub_stages:
                for sub in stage.sub_stages:
                    stw = len(sub["name"])*13+20
                    stx = ax + (self.content_w-stw)/2
                    self.add(svg_rounded_rect(stx, ct, stw, 26, t["sub_header"], t["border"], rx=3))
                    self.add(svg_text(stx + stw/2, ct + 17, sub["name"], size=11, color=t["text"], bold=True))
                    ct += 31

                    # 子项
                    items = sub["items"]
                    ni = len(items)
                    isp = min((self.content_w-30)/ni, node_w)
                    nw2 = isp - 6
                    tw = ni*nw2 + (ni-1)*4
                    tx = ax + (self.content_w-tw)/2
                    for jii, itm in enumerate(items):
                        ix = tx + jii*(nw2+4)
                        self.add(svg_rounded_rect(ix, ct, nw2, node_h-2, t["node"], t["border"]))
                        self.add(svg_text(ix+nw2/2, ct+(node_h-2)/2+4, wrap_text(itm, 7), size=9, color=t["text"]))
                    ct += node_h + 10

            elif stage.items:
                ni = len(stage.items)
                cols = min(ni, 6)
                rows = (ni+cols-1)//cols
                isp = (self.content_w-20)/cols
                nw2 = isp - 6
                for r in range(rows):
                    for c in range(cols):
                        idx = r*cols+c
                        if idx >= ni: break
                        ix = ax + 10 + c*isp
                        iy = ct + r*(node_h+4)
                        self.add(svg_rounded_rect(ix, iy, nw2, node_h-2, t["node"], t["border"]))
                        self.add(svg_text(ix+nw2/2, iy+(node_h-2)/2+4, wrap_text(stage.items[idx], 7), size=9, color=t["text"]))
                ct += rows*(node_h+4) + 8

            self.y = start_y + h

            # 箭头
            if si < len(self.data.stages)-1:
                ay = self.y
                self.add(svg_arrow_down(ax+self.content_w/2, ay, ay+16, t["arrow"], head_size=10, width=2.5))
                self.y += 20

        self.height = self.y + 12


class Template19Renderer(Template21Renderer):
    """
    模板3: 蓝灰学术版 (技术线路图-19彩色)
    复用模板1结构，仅更换主题色为bluegray
    """

    def __init__(self, data: RoadmapData):
        data.theme = "bluegray"
        super().__init__(data)


class Template17Renderer(Template18Renderer):
    """
    模板6: 带方法标注的研究脉络版 (技术路线图-17彩色)
    在模板2基础上增加右侧方法列
    """

    def __init__(self, data: RoadmapData):  # type: ignore
        super().__init__(data)
        self.width = 900
        self.method_w = 95
        self.content_w = self.width - self.content_x - self.method_w - 15

    def render_roadmap(self):
        t = self.theme
        node_w, node_h = 88, 36
        self.y = 12

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            h = 35
            if stage.header_text: h += 34
            if stage.sub_stages: h += len(stage.sub_stages)*(38+40)+10
            elif stage.items:
                n = len(stage.items); cols=min(n,5); rows=(n+cols-1)//cols; h+=rows*(node_h+6)+8
            h += 12

            # 左导航
            label_text = stage.left_label or stage.name
            self.add(svg_rounded_rect(4, start_y+5, self.nav_w-8, h-10, t["stage_label"], t["border"], rx=5))
            lines = label_text.split("\n")
            for i, ln in enumerate(lines):
                self.add(svg_text(4+(self.nav_w-8)/2, start_y+5+(h-10)/2+(i-(len(lines)-1)/2)*16, ln, size=10, color=t["text"], bold=True))

            # 主区域
            self.add(svg_dashed_rect(self.content_x, start_y, self.content_w+self.method_w, h, t["area_bg"]))

            ct = start_y + 10
            ax = self.content_x

            if stage.header_text:
                hw = min(len(stage.header_text)*14+30, self.content_w-20)
                hx = ax+(self.content_w-hw)/2
                self.add(svg_rounded_rect(hx, ct, hw, 28, t["header"], t["border"]))
                self.add(svg_text(hw/2+hx, ct+19, stage.header_text, size=12, color=t["text"], bold=True))
                ct += 34

            if stage.sub_stages:
                for sub in stage.sub_stages:
                    stw=len(sub["name"])*12+18; stx=ax+(self.content_w-stw)/2
                    self.add(svg_rounded_rect(stx, ct, stw, 24, t["sub_header"], t["border"], rx=3))
                    self.add(svg_text(stx+stw/2, ct+16, sub["name"], size=10, color=t["text"], bold=True))
                    ct+=28
                    items=sub["items"]; ni=len(items)
                    isp=min((self.content_w-25)/ni, node_w); nw2=isp-5
                    tw=ni*nw2+(ni-1)*3; tx=ax+(self.content_w-tw)/2
                    for jii,itm in enumerate(items):
                        ix=tx+jii*(nw2+3)
                        self.add(svg_rounded_rect(ix,ct,nw2,node_h-2,t["node"],t["border"]))
                        self.add(svg_text(ix+nw2/2,ct+(node_h-2)/2+4,wrap_text(itm,6),size=9,color=t["text"]))
                    ct+=node_h+8

            elif stage.items:
                ni=len(stage.items); cols=min(ni,5); rows=(ni+cols-1)//cols
                isp=(self.content_w-15)/cols; nw2=isp-5
                for r in range(rows):
                    for c in range(cols):
                        idx=r*cols+c
                        if idx>=ni:break
                        ix=ax+8+c*isp; iy=ct+r*(node_h+4)
                        self.add(svg_rounded_rect(ix,iy,nw2,node_h-2,t["node"],t["border"]))
                        self.add(svg_text(ix+nw2/2,iy+(node_h-2)/2+4,wrap_text(stage.items[idx],6),size=9,color=t["text"]))
                ct+=rows*(node_h+4)+8

            # 右侧方法标注
            if stage.right_label:
                mx = self.content_x + self.content_w + 8
                my = start_y + h/2
                mlines = stage.right_label.split("\n")
                mh = len(mlines) * 14 + 10
                self.add(svg_rounded_rect(mx, my-mh/2, self.method_w-6, mh, "#E3F2FD", t["border"], rx=3))
                for mi, ml in enumerate(mlines):
                    self.add(svg_text(mx+(self.method_w-6)/2, my-mh/2+12+mi*14, ml, size=9, color=t["text"]))

            self.y = start_y + h
            if si < len(self.data.stages)-1:
                ay=self.y
                self.add(svg_arrow_down(ax+self.content_w/2,ay,ay+15,t["arrow"],head_size=9,width=2.2))
                self.y+=18

        self.height=self.y+12


class Template16Renderer(SVGRenderer):
    """
    模板7: 六阶段标准版 (技术路线图-16彩色)
    大棕色箭头连接各阶段
    """

    def __init__(self, data: RoadmapData):  # type: ignore
        super().__init__(data, width=800)
        self.label_w = 52
        self.content_x = self.label_w + 10
        self.content_w = self.width - self.content_x - 10
        self.y = 12

    def render_roadmap(self):
        t = self.theme
        node_w, node_h = 110, 34
        self.y = 12

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            lh = 44  # 左标签高

            # 计算内容区高度
            ch = 8
            if stage.header_text:
                ch += 32
            if stage.items:
                n = len(stage.items); cols=min(n,4); rows=(n+cols-1)//cols
                ch += rows*(node_h+5)+5
            elif stage.sub_stages:
                ch += len(stage.sub_stages)*(32+36)+10
            ch += 8
            total_h = max(lh, ch) + 5

            # 左标签
            lbl = stage.left_label or stage.name
            self.add(svg_rounded_rect(3, start_y, self.label_w-6, lh, t["stage_label"], t["border"], rx=5))
            self.add(svg_text(3+(self.label_w-6)/2, start_y+lh/2+5, lbl, size=11, color=t["text"], bold=True))

            # 虚线区域
            self.add(svg_dashed_rect(self.content_x, start_y, self.content_w, total_h, t["area_bg"]))

            ct = start_y + 8
            ax = self.content_x

            if stage.header_text:
                hw=min(len(stage.header_text)*15+30, self.content_w-16)
                hx=ax+(self.content_w-hw)/2
                self.add(svg_rounded_rect(hx,ct,hw,30,t["header"],t["border"]))
                self.add(svg_text(hx+hw/2,ct+21,stage.header_text,size=13,color=t["text"],bold=True))
                ct+=36

            if stage.items:
                n=len(stage.items); cols=min(n,4); rows=(n+cols-1)//cols
                isp=(self.content_w-16)/cols; nw2=isp-6
                for r in range(rows):
                    for c in range(cols):
                        idx=r*cols+c
                        if idx>=n:break
                        ix=ax+8+c*isp; iy=ct+r*(node_h+5)
                        self.add(svg_rounded_rect(ix,iy,nw2,node_h,t["node"],t["border"]))
                        self.add(svg_text(ix+nw2/2,iy+node_h/2+4,wrap_text(stage.items[idx],8),size=10,color=t["text"]))
                ct+=rows*(node_h+5)+8

            elif stage.sub_stages:
                for sub in stage.sub_stages:
                    stw=len(sub["name"])*13+20; stx=ax+(self.content_w-stw)/2
                    self.add(svg_rounded_rect(stx,ct,stw,26,t["sub_header"],t["border"],rx=3))
                    self.add(svg_text(stx+stw/2,ct+17,sub["name"],size=11,color=t["text"],bold=True))
                    ct+=30
                    items=sub["items"]
                    ni=len(items); isp=(self.content_w-20)/ni; nw2=min(isp-5,node_w)
                    tw=ni*nw2+(ni-1)*4; tx=ax+(self.content_w-tw)/2
                    for jii,itm in enumerate(items):
                        ix=tx+jii*(nw2+4)
                        self.add(svg_rounded_rect(ix,ct,nw2,node_h-2,t["node"],t["border"]))
                        self.add(svg_text(ix+nw2/2,ct+(node_h-2)/2+4,wrap_text(itm,7),size=9,color=t["text"]))
                    ct+=node_h+8

            self.y = start_y + total_h

            # 大棕色箭头
            if si < len(self.data.stages) - 1:
                ay = self.y
                arr_color = "#8B572A"  # 棕色箭头
                cx = ax + self.content_w/2
                # 粗箭头
                self.add(f'<polygon points="{cx-12:.1f},{ay+2:.1f} {cx+12:.1f},{ay+2:.1f} {cx+12:.1f},{ay+14:.1f} {cx+18:.1f},{ay+14:.1f} {cx:.1f},{ay+26:.1f} {cx-18:.1f},{ay+14:.1f} {cx-12:.1f},{ay+14:.1f}" fill="{arr_color}"/>')
                self.y += 30

        # 结论
        if self.data.conclusion:
            self.y += 5
            cw=min(len(self.data.conclusion)*17+50,self.content_w-16)
            cx=self.content_x+self.content_w/2
            self.add(svg_rounded_rect(cx-cw/2,self.y,cw,34,t["stage_label"],t["border"]))
            self.add(svg_text(cx,self.y+22,self.data.conclusion,size=13,color=t["text"],bold=True))
            self.y+=44

        self.height=self.y+12


class TemplateSurveyRenderer(SVGRenderer):
    """
    模板10: 实证调研流程版 (技术路线图15.jpg)
    双轨并行：左主流程 + 右SPSS分析
    """

    def __init__(self, data: RoadmapData):  # type: ignore
        super().__init__(data, width=920)
        data.theme = "survey"
        self.theme = THEMES["survey"]
        self.left_w = 68     # 左标签
        self.right_w = 85    # 右结果列
        self.center_w = 480  # 中间主区域
        self.content_x = self.left_w + 8
        self.y = 10

    def render_roadmap(self):
        t = self.theme
        self.y = 10
        cx_left = self.content_x + self.center_w/2  # 中心区中心X
        right_x = self.content_x + self.center_w + 20  # 右列起点

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            lbl = stage.left_label or stage.name

            # 高度计算
            sh = 40  # 标签高
            ch = 10
            if stage.items and not stage.sub_stages:
                n=len(stage.items); ch += 34
            elif stage.sub_stages:
                ch += len(stage.sub_stages)*(28+32)+5
            ch += 10
            total_h = max(sh, ch) + 5

            # 左标签（绿色）
            self.add(svg_rounded_rect(3, start_y, self.left_w-6, sh, t["stage_label"], t["border"], rx=4))
            self.add(svg_text(3+(self.left_w-6)/2, start_y+sh/2+5, lbl, size=11, color=t["text"], bold=True))

            # 右标签
            if stage.right_label:
                rlines = stage.right_label.split("\n")
                rh = len(rlines)*16 + 10
                ry = start_y + total_h/2 - rh/2
                self.add(svg_rounded_rect(right_x, ry, self.right_w-6, rh, "#BBDEFB", t["border"], rx=3))
                for ri, rl in enumerate(rlines):
                    self.add(svg_text(right_x+(self.right_w-6)/2, ry+12+ri*16, rl, size=10, color=t["text"]))

            # 中间虚线区域
            self.add(svg_dashed_rect(self.content_x, start_y, self.center_w, total_h, t["area_bg"]))

            ct = start_y + 8
            ax = self.content_x

            # 单层项目（如初期准备、问卷调查）
            if stage.items and not stage.sub_stages:
                n=len(stage.items); isp=(self.center_w-20)/n; nw2=isp-8
                for jii, itm in enumerate(stage.items):
                    ix=ax+10+jii*isp
                    self.add(svg_rounded_rect(ix,ct,nw2,32,t["header"],"#1565C0",rx=3))
                    self.add(svg_text(ix+nw2/2,ct+21,wrap_text(itm,7),size=10,color="#fff",bold=True))
                ct += 42

            # 多层子阶段（如数据分析）
            elif stage.sub_stages:
                for sub in stage.sub_stages:
                    # 黄色子标题
                    stw=len(sub["name"])*13+20
                    stx=ax+10
                    self.add(svg_rounded_rect(stx,ct,stw,28,t["header"],"#F9A825",rx=3))
                    self.add(svg_text(stx+stw/2,ct+19,sub["name"],size=11,color=t["text"],bold=True))

                    # 灰色右侧项
                    items=sub.get("items",[])
                    ni=len(items)
                    ix2 = stx + stw + 12
                    iw2 = min(140, (self.center_w-stw-30)/max(ni,1))
                    for jii, itm in enumerate(items):
                        iix = ix2 + jii*iw2
                        self.add(svg_rounded_rect(iix,ct+2,iw2,24,"#E0E0E0","#999",rx=2))
                        self.add(svg_text(iix+iw2/2,ct+18,wrap_text(itm,10),size=9,color=t["text"]))
                    ct += 34

                    # 绿色向下箭头（连接下一级）
                    if stage.sub_stages.index(sub) < len(stage.sub_stages)-1:
                        arr_x = stx + stw/2
                        self.add(f'<polygon points="{arr_x-6:.1f},{ct+2:.1f} {arr_x+6:.1f},{ct+2:.1f} {arr_x+6:.1f},{ct+8:.1f} {arr_x+10:.1f},{ct+8:.1f} {arr_x:.1f},{ct+16:.1f} {arr_x-10:.1f},{ct+8:.1f} {arr_x-6:.1f},{ct+8:.1f}" fill="#AED581"/>')
                        ct += 18

            self.y = start_y + total_h

            # 绿色箭头连接
            if si < len(self.data.stages) - 1:
                ay = self.y
                # 从左标签指向下一个左标签
                self.add(svg_arrow_right(self.left_w-3, self.left_w/2+3, ay+total_h/2, "#AED581", head_size=8, width=2))
                # 中间区域向下箭头
                self.add(f'<polygon points="{cx_left-7:.1f},{ay+3:.1f} {cx_left+7:.1f},{ay+3:.1f} {cx_left+7:.1f},{ay+10:.1f} {cx_left+12:.1f},{ay+10:.1f} {cx_left:.1f},{ay+20:.1f} {cx_left-12:.1f},{ay+10:.1f} {cx_left-7:.1f},{ay+10:.1f}" fill="#AED581"/>')
                # 右列箭头
                if stage.right_label:
                    rx_c = right_x + (self.right_w-6)/2
                    self.add(svg_line(rx_c, ay+total_h/2+10, rx_c, ay+total_h+15, "#AED581", width=2))
                    self.add(f'<polygon points="{rx_c-5:.1f},{ay+total_h+15:.1f} {rx_c+5:.1f},{ay+total_h+15:.1f} {rx_c:.1f},{ay+total_h+23:.1f}" fill="#AED581"/>')

                self.y += 26

        # 底部结论条
        if self.data.conclusion:
            self.y += 8
            cw = self.center_w
            self.add(svg_rounded_rect(self.content_x, self.y, cw, 36, "#66BB6A", "#43A047"))
            self.add(svg_text(self.content_x+cw/2, self.y+23, self.data.conclusion, size=14, color="#fff", bold=True))
            # 右侧展望
            if hasattr(self.data, 'conclusion_right') and self.data.conclusion_right:
                rx = self.content_x + cw + 20
                self.add(svg_rounded_rect(rx, self.y, 100, 36, "#AED581", "#66BB6A"))
                self.add(svg_text(rx+50, self.y+23, self.data.conclusion_right, size=12, color=t["text"]))
            self.y += 46

        self.height = self.y + 12


class Template15Renderer(SVGRenderer):
    """
    模板8/9: 模型构建专用版 (技术路线图-15彩色)
    双层理论 + 网格评价分析
    """

    def __init__(self, data: RoadmapData):  # type: ignore
        super().__init__(data, width=850)
        data.theme = "navy"
        self.theme = THEMES["navy"]
        self.label_w = 55
        self.content_x = self.label_w + 8
        self.content_w = self.width - self.content_x - 8
        self.y = 10

    def render_roadmap(self):
        t = self.theme
        self.y = 10
        arrow_color = "#5B9BD5"  # 蓝色空心箭头

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            lbl = stage.left_label or stage.name

            # 计算高度
            sh = 50  # 左标签
            ch = 8
            if stage.header_text: ch += 32
            if stage.sub_stages:
                for sub in stage.sub_stages:
                    ch += 30 + 36  # sub-title + items
            elif stage.items and not stage.sub_stages:
                n=len(stage.items); cols=min(n,4); ch+=((n+cols-1)//cols)*(36+4)+4
            if stage.sub_items and any(stage.sub_items):
                ch += 80  # 网格子项区
            ch += 8
            total_h = max(sh, ch) + 3

            # 左标签
            lines = lbl.split("\n")
            lh = len(lines)*16 + 14
            self.add(svg_rounded_rect(3, start_y+2, self.label_w-6, lh, t["stage_label"], t["border"], rx=4))
            for li, ln in enumerate(lines):
                self.add(svg_text(3+(self.label_w-6)/2, start_y+12+li*16, ln, size=10, color=t["text"], bold=True))

            # 虚线区域
            self.add(svg_dashed_rect(self.content_x, start_y, self.content_w, total_h, t["area_bg"]))

            ct = start_y + 6
            ax = self.content_x

            # 标题头
            if stage.header_text:
                hw=min(len(stage.header_text)*14+30, self.content_w-16)
                hx=ax+(self.content_w-hw)/2
                self.add(svg_rounded_rect(hx,ct,hw,28,t["header"],t["border"]))
                self.add(svg_text(hx+hw/2,ct+19,stage.header_text,size=12,color=t["text"],bold=True))
                ct+=34

            # 子阶段（双层理论等）
            if stage.sub_stages:
                for sub in stage.sub_stages:
                    stw=len(sub["name"])*13+20; stx=ax+(self.content_w-stw)/2
                    self.add(svg_rounded_rect(stx,ct,stw,26,t["header"],t["border"],rx=3))
                    self.add(svg_text(stx+stw/2,ct+17,sub["name"],size=11,color=t["text"],bold=True))
                    ct+=30
                    items=sub["items"]; ni=len(items)
                    isp=(self.content_w-20)/ni; nw2=isp-6
                    tw=ni*nw2+(ni-1)*4; tx=ax+(self.content_w-tw)/2
                    for jii,itm in enumerate(items):
                        ix=tx+jii*(nw2+4)
                        self.add(svg_rounded_rect(ix,ct,nw2,32,t["node"],t["border"]))
                        self.add(svg_text(ix+nw2/2,ct+20,wrap_text(itm,7),size=9,color=t["text"]))
                    ct+=38

            # 普通项目
            elif stage.items:
                n=len(stage.items); cols=min(n,4); rows=(n+cols-1)//cols
                isp=(self.content_w-16)/cols; nw2=isp-6
                for r in range(rows):
                    for c in range(cols):
                        idx=r*cols+c
                        if idx>=len(stage.items): break
                        ix=ax+8+c*isp; iy=ct+r*40
                        self.add(svg_rounded_rect(ix,iy,nw2,34,t["node"],t["border"]))
                        self.add(svg_text(ix+nw2/2,iy+21,wrap_text(stage.items[idx],8),size=10,color=t["text"]))
                ct+=rows*40+6

            # 网格状子项（如模型评价分析）
            if stage.sub_items and any(stage.sub_items):
                ct += 5
                parents = stage.items[:len(stage.sub_items)] if stage.items else [f"项{i+1}" for i in range(len(stage.sub_items))]
                pp = len(parents)
                pw = (self.content_w-20)/pp - 4

                for pi in range(pp):
                    px = ax + 10 + pi*(pw+4)
                    subs = stage.sub_items[pi] if pi < len(stage.sub_items) else []
                    # 父节点
                    ph = 34
                    self.add(svg_rounded_rect(px, ct, pw, ph, t["node"], t["border"]))
                    plabel = parents[pi] if pi < len(parents) else f"评价{pi+1}"
                    self.add(svg_text(px+pw/2, ct+ph/2+4, wrap_text(plabel, 6), size=9, color=t["text"], bold=True))

                    # 右侧子网格
                    if subs:
                        ns = len(subs)
                        sw = min(55, (self.content_w-20-pp*pw-pp*4-20)/max(ns,1))
                        sx = px + pw + 6
                        for sci, sub in enumerate(subs):
                            sxi = sx + sci*(sw+3)
                            ssh = 28
                            self.add(svg_rounded_rect(sxi, ct+3, sw, ssh, t["node"], t["border"], rx=2))
                            self.add(svg_text(sxi+sw/2, ct+ssh/2+5, wrap_text(sub, 4), size=8, color=t["text"]))
                            # 连接线
                            self.add(svg_line(px+pw, ct+ph/2, sxi, ct+ssh/2+3, t["arrow"], width=0.8))

                ct += 45

            self.y = start_y + total_h

            # 蓝色空心箭头
            if si < len(self.data.stages) - 1:
                ay = self.y
                cx = ax + self.content_w/2
                aw = 14; ah = 22
                self.add(f'<polygon points="{cx-aw/2:.1f},{ay:.1f} {cx+aw/2:.1f},{ay:.1f} {cx+aw/2:.1f},{ay+ah-6:.1f} {cx+aw/2+5:.1f},{ay+ah-6:.1f} {cx:.1f},{ay+ah:.1f} {cx-aw/2-5:.1f},{ay+ah-6:.1f} {cx-aw/2:.1f},{ay+ah-6:.1f}" fill="none" stroke="{arrow_color}" stroke-width="2"/>')
                self.add(f'<polygon points="{cx-5:.1f},{ay+ah-6:.1f} {cx+5:.1f},{ay+ah-6:.1f} {cx:.1f},{ay+ah:.1f}" fill="{arrow_color}"/>')
                self.y += ah + 6

        # 结论
        if self.data.conclusion:
            self.y += 5
            cw=min(len(self.data.conclusion)*16+40, self.content_w-16)
            cx=self.content_x+self.content_w/2
            self.add(svg_rounded_rect(cx-cw/2,self.y,cw,32,t["header"],t["border"]))
            self.add(svg_text(cx,self.y+21,self.data.conclusion,size=13,color=t["text"],bold=True))
            self.y+=42

        self.height=self.y+12


# ============================================================
# 模板27和24的特殊渲染（使用通用渲染器适配）
# ============================================================

class Template27Renderer(SVGRenderer):
    """模板4: 政策导向流程版"""

    def __init__(self, data: RoadmapData):  # type: ignore
        super().__init__(data, width=900)
        self.label_w = 62
        self.content_x = self.label_w + 8
        self.content_w = self.width - self.content_x - 8
        self.y = 10

    def render_roadmap(self):
        t = self.theme
        self.y = 10

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            lbl = stage.left_label or stage.name

            sh = 36
            ch = 8
            if stage.header_text:
                hw = len(stage.header_text)*13+30; ch += 34
            if stage.items: ch += 40
            ch += 10
            total_h = max(sh, ch) + 4

            # 左标签
            self.add(svg_rounded_rect(3, start_y, self.label_w-6, sh, t["stage_label"], "#558B2F", rx=3))
            self.add(svg_text(3+(self.label_w-6)/2, start_y+sh/2+5, lbl, size=11, color=t["text"], bold=True))

            # 区域
            self.add(svg_dashed_rect(self.content_x, start_y, self.content_w, total_h, "#E3F2FD"))

            ct = start_y + 6
            ax = self.content_x

            if stage.header_text:
                hw=min(len(stage.header_text)*12+30, self.content_w-12)
                hx=ax+(self.content_w-hw)/2
                self.add(svg_rounded_rect(hx,ct,hw,28,"#E8EAF6","#7986CB",rx=2))
                self.add(svg_text(hx+hw/2,ct+19,stage.header_text,size=11,color=t["text"]))
                ct+=33

            if stage.items:
                n=len(stage.items); isp=(self.content_w-16)/n; nw2=isp-6
                for jii, itm in enumerate(stage.items):
                    ix=ax+8+jii*isp
                    self.add(svg_rounded_rect(ix,ct,nw2,32,"#FFF8E1","#CCA000",rx=2))
                    self.add(svg_text(ix+nw2/2,ct+20,wrap_text(itm,7),size=9,color=t["text"]))
                ct+=40

            # 子阶段特殊处理
            if stage.sub_stages:
                for sub in stage.sub_stages:
                    stw=len(sub["name"])*12+16
                    self.add(svg_rounded_rect(ax+10,ct,stw,26,t["header"],t["border"],rx=3))
                    self.add(svg_text(ax+10+stw/2,ct+17,sub["name"],size=10,color=t["text"],bold=True))
                    ct+=30
                    items=sub["items"]; ni=len(items)
                    for jii, itm in enumerate(items):
                        ix=ax+10+jii*100
                        iw=90
                        self.add(svg_rect(ix,ct,iw,28,"#fff","#999",rx=2))
                        self.add(svg_text(ix+iw/2,ct+18,itm,size=9,color=t["text"]))
                    ct+=34

                    # 内部箭头
                    if stage.sub_stages.index(sub) < len(stage.sub_stages)-1:
                        self.add(svg_arrow_right(ax+10+stw/2, ax+10+stw/2+stw+5, ct-8, "#FFB300", width=1.5))

            self.y = start_y + total_h

            # 流程箭头
            if si < len(self.data.stages) - 1:
                ay = self.y
                cx_l = (self.label_w-6)/2+3
                self.add(f'<polygon points="{cx_l-5:.1f},{ay:.1f} {cx_l+5:.1f},{ay:.1f} {cx_l+5:.1f},{ay+8:.1f} {cx_l+9:.1f},{ay+8:.1f} {cx_l:.1f},{ay+16:.1f} {cx_l-9:.1f},{ay+8:.1f} {cx_l-5:.1f},{ay+8:.1f}" fill="#AED581"/>')
                self.y += 20

        # 底部结论区
        if self.data.conclusion:
            pass  # 模板27通常无独立结论

        self.height = self.y + 12


class Template24Renderer(SVGRenderer):
    """模板5: 三栏综合框架版"""

    def __init__(self, data: RoadmapData):  # type: ignore
        super().__init__(data, width=1000)
        self.col_left_w = 85   # 左栏(框架)
        self.col_mid_w = 550   # 中栏(内容)
        self.col_right_w = 100 # 右栏(方法)
        self.content_x = self.col_left_w + 5
        self.y = 8

    def render_roadmap(self):
        t = self.theme
        self.y = 8
        mid_x = self.content_x + self.col_left_w + 8
        right_x = mid_x + self.col_mid_w + 8

        for si, stage in enumerate(self.data.stages):
            start_y = self.y
            lbl = stage.left_label or stage.name

            # 高度
            sh = 36
            ch = 8
            if stage.header_text: ch += 30
            if stage.items:
                n=len(stage.items)
                if n <= 3: ch += 36
                else: ch += 70
            ch += 8
            total_h = max(sh, ch) + 3

            # 左栏标签（橙色）
            self.add(svg_rounded_rect(5, start_y, self.col_left_w-8, sh, t["header"], t["border"], rx=4))
            self.add(svg_text(5+(self.col_left_w-8)/2, start_y+sh/2+5, lbl, size=11, color=t["text"], bold=True))

            # 中间虚线区
            self.add(svg_dashed_rect(mid_x, start_y, self.col_mid_w, total_h, t["area_bg"]))

            ct = start_y + 5

            if stage.header_text:
                hw=min(len(stage.header_text)*12+24, self.col_mid_w-12)
                hx=mid_x+(self.col_mid_w-hw)/2
                # 紫色/粉色标题
                hdr_color = "#E1BEE7" if si%2==0 else "#FFCCBC"
                hdr_border = "#9C27B0" if si%2==0 else "#E64A19"
                self.add(svg_rounded_rect(hx,ct,hw,26,hdr_color, hdr_border, rx=2))
                self.add(svg_text(hx+hw/2,ct+17,stage.header_text,size=10,color=t["text"],bold=True))
                ct+=30

            if stage.items:
                n=len(stage.items); cols=min(n,4); rows=(n+cols-1)//cols
                isp=(self.col_mid_w-12)/cols; nw2=isp-5
                for r in range(rows):
                    for c in range(cols):
                        idx=r*cols+c
                        if idx>=n:break
                        icolor = "#E3F2FD" if (idx%2==0) else "#FFF3E0"
                        ix=mid_x+6+c*isp; iy=ct+r*34
                        self.add(svg_rounded_rect(ix,iy,nw2,30,icolor,"#90A4AE",rx=2))
                        txt=wrap_text(stage.items[idx],7)
                        self.add(svg_text(ix+nw2/2,iy+19,txt,size=9,color=t["text"]))
                ct+=rows*34+5

            # 右栏方法
            methods_map = {
                0: ["文献分析", "问卷调查"],
                1: ["文献分析", "调查访谈", "......"],
                2: ["层次分析", "空间计量", "......"],
                3: ["多元回归", "DSEE"],
                4: ["案例分析", "问卷调查"],
            }
            methods = methods_map.get(si, ["......"])
            rlines = len(methods)
            rh = rlines*16 + 8
            ry = start_y + total_h/2 - rh/2
            self.add(svg_rounded_rect(right_x, ry, self.col_right_w-6, rh, "#FAFAFA", t["border"], rx=2))
            for ri, m in enumerate(methods):
                self.add(svg_text(right_x+(self.col_right_w-6)/2, ry+12+ri*16, m, size=9, color=t["text"]))

            # 蓝色下箭头（左侧）
            if si < len(self.data.stages) - 1:
                ay = self.y
                ax_c = 5 + (self.col_left_w-8)/2
                self.add(f'<polygon points="{ax_c-8:.1f},{ay+2:.1f} {ax_c+8:.1f},{ay+2:.1f} {ax_c+8:.1f},{ay+10:.1f} {ax_c+14:.1f},{ay+10:.1f} {ax_c:.1f},{ay+22:.1f} {ax_c-14:.1f},{ay+10:.1f} {ax_c-8:.1f},{ay+10:.1f}" fill="#42A5F5"/>')
                self.y = ay + total_h + 6
            else:
                self.y = start_y + total_h

        self.height = self.y + 12


# ============================================================
# 模板分发器
# ============================================================

RENDERER_MAP = {
    "template-21": Template21Renderer,
    "template-18": Template18Renderer,
    "template-19": Template19Renderer,
    "template-27": Template27Renderer,
    "template-24": Template24Renderer,
    "template-17": Template17Renderer,
    "template-16": Template16Renderer,
    "template-15a": Template15Renderer,
    "template-15b": Template15Renderer,
    "template-survey": TemplateSurveyRenderer,
}

TEMPLATE_NAMES = {
    "template-21": "四阶段经典版",
    "template-18": "研究脉络纵向版",
    "template-19": "蓝灰学术版",
    "template-27": "政策导向流程版",
    "template-24": "三栏综合框架版",
    "template-17": "带方法标注的研究脉络版",
    "template-16": "六阶段标准版",
    "template-15a": "模型构建专用版",
    "template-15b": "模型构建变体版",
    "template-survey": "实证调研流程版",
}


def list_templates():
    """列出所有可用模板"""
    print("=" * 55)
    print("  可用技术路线图模板列表")
    print("=" * 55)
    for tid, tname in TEMPLATE_NAMES.items():
        print(f"  [{tid[-2:]}] {tid:20s} → {tname}")
    print("=" * 55)


def generate(title: str, template_id: str = "template-21", output: str = "roadmap.svg",
             json_file: str = None):
    """主生成函数"""
    if template_id not in RENDERER_MAP:
        print(f"[ERROR] 未知模板: {template_id}")
        print("可用模板:", ", ".join(RENDERER_MAP.keys()))
        list_templates()
        sys.exit(1)

    # 加载数据
    if json_file and os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        data = RoadmapData(
            title=raw.get("title", title),
            conclusion=raw.get("conclusion", "结论与展望"),
            theme=raw.get("theme", "classic")
        )
        for sd in raw.get("stages", []):
            s = Stage(
                name=sd.get("name", ""),
                items=sd.get("items", []),
                sub_stages=sd.get("sub_stages", []),
                sub_items=sd.get("sub_items", []),
                header_text=sd.get("header_text", ""),
                left_label=sd.get("left_label", ""),
                right_label=sd.get("right_label", "")
            )
            data.stages.append(s)
        print(f"[INFO] 已加载自定义JSON: {json_file}")
    else:
        data = generate_content_from_title(title, template_id)
        print(f"[INFO] 自动生成内容 | 模板: {TEMPLATE_NAMES.get(template_id, template_id)}")

    # 渲染
    renderer_cls = RENDERER_MAP[template_id]
    renderer = renderer_cls(data)
    renderer.render_roadmap()

    # 保存
    output_path = renderer.save(output)
    print(f"[INFO] 画布尺寸: {renderer.width} x {renderer.height}px")
    return output_path


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="技术路线图自动生成器 - Tech Roadmap Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_roadmap.py --title "社区治理数字化研究" --template template-21 -o output.svg
  python generate_roadmap.py --title "企业数字化转型" --template template-16 -o roadmap.svg
  python generate_roadmap.py --list
  python generate_roadmap.py --title "问卷调研分析" --template template-survey -o survey.svg --json my_data.json
        """
    )
    parser.add_argument("--title", "-t", required=True, help="研究主题/论文题目")
    parser.add_argument("--template", "-T", default="template-21",
                        help="模板ID (默认: template-21). 使用 --list 查看所有模板")
    parser.add_argument("--output", "-o", default="roadmap.svg", help="输出SVG文件路径")
    parser.add_argument("--json", "-j", default=None, help="自定义内容JSON文件路径")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用模板")

    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    generate(args.title, args.template, args.output, args.json)


if __name__ == "__main__":
    main()
