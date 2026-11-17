#!/usr/bin/env python3
"""
小红书风格卡片生成器 —— 统一简洁布局

布局参考：米白/浅米色背景、顶部「标签 + 引号装饰」、中间大字居中文案、
底部短横线 + 左页码 / 右账号。支持多主题配色与自定义 footer 参数。
新增「图文卡片」布局：顶部简笔画 + 窄列居中文字 + 底部署名。

用法:
  python3 card_generator.py --theme warm --lines "周五了\n你还活着吗" --subtitle "关于活着" --page-number 1 --total-pages 6 --account "@雨夜心灯" -o card.png
  python3 card_generator.py --layout image-text --illustration door.svg --theme warm_illust --lines "周五了。\n把工牌摘下来" --account "@雨夜心灯" -o card.png
  python3 card_generator.py --all-themes --demo --output-dir ./demo
"""

import os
import sys
import json
import math
import base64
import subprocess
import tempfile
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).parent
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

# ─── 主题配置 ──────────────────────────────────────────────────────
# 每个主题：背景、文字、点缀、装饰元素、字体
# 来源：text-to-elegant-image 仓库 18 种（其中小红书拆 A/B 两模式）+ 4 种年轻人风格 + warm 原创 + warm_illust 图文 = 25 种
# 现为 29 种：在上述基础上增加 4 种照片背景氛围主题（cinematic / film / journal / history）
THEMES = {
    # ── 原创风格 ──────────────────────────────────────────────
    "warm": {
        "name": "温暖哲思",
        "bg": "#F7F3ED",
        "bg_gradient": None,
        "text": "#3A3229",
        "muted": "#8C8070",
        "accent": "#C4A882",
        "accent2": "#D9C6B0",
        "font_main": "'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif",
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#C4A882",
        "deco": "warm",
        "letter_spacing": 4,
        "google_fonts": [],
    },
    "warm_illust": {
        "name": "温暖简笔哲思",
        "bg": "#FAF7F2",
        "bg_gradient": None,
        "text": "#3A3A3A",
        "muted": "#9A9A9A",
        "accent": "#D4A84B",
        "accent2": "#F5E6C8",
        "font_main": "'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif",
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#D4A84B",
        "deco": "warm_illust",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # ── 照片背景风格（需配合 --background 使用） ──────────────
    # 这三个主题不自带素材，背景图由用户提供或 AI 生成后通过 --background 传入
    "cinematic": {
        "name": "暗色电影感",
        "bg": "#0C0C0E",
        "bg_gradient": None,
        "text": "#F5F1E8",
        "muted": "#C9C2B6",
        "accent": "#D9B47A",
        "accent2": "#6E655A",
        "font_main": "'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif",
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#D9B47A",
        "deco": "none",
        "letter_spacing": 5,
        "google_fonts": [],
        "photo": True,
        "scrim": 0.55,
        "scrim_color": "#000000",
        "grain": 0.0,
        "desaturate": 1.0,
    },
    # 历史/古风口播专用：沿用 cinematic 的暗色电影感，主文案换本机隶书。
    # 字体全部为本机可用字体，不依赖 Google Fonts 联网。
    "history": {
        "name": "古风电影感",
        "bg": "#0A0806",
        "bg_gradient": None,
        "text": "#F3E7CE",
        "muted": "#C4B49A",
        "accent": "#C9A227",
        "accent2": "#6E655A",
        # 默认报隶：横扁厚重、碑刻感，配秦汉史/翻案解说比行楷更庄重且更清晰。
        # 行楷飘逸但笔画细，更像古装剧片头，需要时用 --font-main "'Xingkai SC', serif" 切。
        "font_main": ("'Baoli SC', 'STBaoliSC-Regular', '报隶-简', "
                      "'Weibei SC Bold', '魏碑-简', "
                      "'Xingkai SC', 'STXingkaiSC-Bold', '行楷-简', "
                      "'Libian SC', '隶变-简', 'Kaiti SC', 'Songti SC', serif"),
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#C9A227",
        "deco": "none",
        "letter_spacing": 3,
        "google_fonts": [],
        "photo": True,
        "scrim": 0.58,
        "scrim_color": "#000000",
        "grain": 0.0,
        "desaturate": 1.0,
    },
    "film": {
        "name": "胶片颗粒",
        "bg": "#14110E",
        "bg_gradient": None,
        "text": "#EFE9DE",
        "muted": "#BDB3A4",
        "accent": "#C8783C",
        "accent2": "#6B5B4A",
        "font_main": "'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif",
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#C8783C",
        "deco": "none",
        "letter_spacing": 4,
        "google_fonts": [],
        "photo": True,
        "scrim": 0.5,
        "scrim_color": "#100B06",
        "grain": 0.09,
        "desaturate": 0.72,
    },
    "journal": {
        "name": "书页氛围",
        "bg": "#17110A",
        "bg_gradient": None,
        "text": "#F3E9D6",
        "muted": "#C4B49A",
        "accent": "#C9A227",
        "accent2": "#7A6A50",
        "font_main": "'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif",
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#C9A227",
        "deco": "none",
        "letter_spacing": 6,
        "google_fonts": [],
        "photo": True,
        "scrim": 0.52,
        "scrim_color": "#1A120B",
        "grain": 0.04,
        "desaturate": 0.9,
    },
    # ── 年轻人风格（新增，非仓库原始） ────────────────────────
    "y2k": {
        "name": "Y2K 千禧潮酷",
        "bg": "#0B0B15",
        "bg_gradient": "linear-gradient(160deg, #1A0B2E 0%, #2D1B4E 40%, #0B3D4C 100%)",
        "text": "#FFFFFF",
        "muted": "#B8B8D1",
        "accent": "#FF00CC",
        "accent2": "#00FFFF",
        "font_main": "'PingFang SC', 'Helvetica Neue', 'Arial', 'Heiti SC', sans-serif",
        "font_tag": "'PingFang SC', 'Helvetica Neue', sans-serif",
        "quote_color": "#00FFFF",
        "deco": "stars",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    "doodle": {
        "name": "手绘涂鸦",
        "bg": "#FFFEF7",
        "bg_gradient": None,
        "text": "#2C2C2C",
        "muted": "#6B6B6B",
        "accent": "#FF6B35",
        "accent2": "#FFD23F",
        "font_main": "'ZCOOL KuaiLe', 'Caveat', 'PingFang SC', 'Microsoft YaHei', cursive",
        "font_tag": "'ZCOOL KuaiLe', 'Caveat', 'PingFang SC', cursive",
        "quote_color": "#FF6B35",
        "deco": "doodles",
        "letter_spacing": 2,
        "google_fonts": ["ZCOOL KuaiLe", "Caveat:wght@400;700"],
    },
    "pop": {
        "name": "渐变波普",
        "bg": "#FFF0F5",
        "bg_gradient": "linear-gradient(135deg, #FFF0F5 0%, #E6F3FF 50%, #FFF9E6 100%)",
        "text": "#1A1A2E",
        "muted": "#5A5A6E",
        "accent": "#FF3366",
        "accent2": "#3366FF",
        "font_main": "'PingFang SC', 'Arial Black', 'Impact', 'Heiti SC', sans-serif",
        "font_tag": "'PingFang SC', 'Arial Black', sans-serif",
        "quote_color": "#FF3366",
        "deco": "dots",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    "minimal": {
        "name": "极简日系",
        "bg": "#FAFAFA",
        "bg_gradient": None,
        "text": "#1A1A1A",
        "muted": "#888888",
        "accent": "#1A1A1A",
        "accent2": "#E0E0E0",
        "font_main": "'Songti SC', 'STSong', 'Noto Serif SC', serif",
        "font_tag": "'PingFang SC', sans-serif",
        "quote_color": "#CCCCCC",
        "deco": "none",
        "letter_spacing": 5,
        "google_fonts": [],
    },
    # ── text-to-elegant-image 仓库 18 种风格 ──────────────────
    # 01 赛博科技
    "cyberpunk": {
        "name": "赛博科技",
        "bg": "#050812",
        "bg_gradient": "linear-gradient(180deg, #050812 0%, #0C1220 100%)",
        "text": "#F0F4F8",
        "muted": "#7A8FA6",
        "accent": "#00F0FF",
        "accent2": "#B900FF",
        "font_main": "'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif",
        "font_tag": "'PingFang SC', 'Helvetica Neue', sans-serif",
        "quote_color": "#00F0FF",
        "deco": "cyberpunk",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # 02 极简优雅
    "elegant": {
        "name": "极简优雅",
        "bg": "#FDFDFD",
        "bg_gradient": None,
        "text": "#2C2C2C",
        "muted": "#8E8E8E",
        "accent": "#D32F2F",
        "accent2": "#EAEAEA",
        "font_main": "'Songti SC', 'Noto Serif CJK SC', 'Source Han Serif CN', Georgia, serif",
        "font_tag": "'Songti SC', 'Noto Serif CJK SC', serif",
        "quote_color": "#D32F2F",
        "deco": "none",
        "letter_spacing": 4,
        "google_fonts": [],
    },
    # 03 Apple 质感
    "apple": {
        "name": "Apple 质感",
        "bg": "#F5F5F7",
        "bg_gradient": None,
        "text": "#1D1D1F",
        "muted": "#6E6E73",
        "accent": "#0066CC",
        "accent2": "#E8E8ED",
        "font_main": "-apple-system, 'BlinkMacSystemFont', 'PingFang SC', 'Segoe UI', Helvetica, Arial, sans-serif",
        "font_tag": "-apple-system, 'PingFang SC', sans-serif",
        "quote_color": "#0066CC",
        "deco": "none",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # 04 轻科技
    "cowork": {
        "name": "轻科技",
        "bg": "#F5F5F7",
        "bg_gradient": None,
        "text": "#1D1D1F",
        "muted": "#6E6E73",
        "accent": "#0066CC",
        "accent2": "#0077ED",
        "font_main": "-apple-system, 'SF Pro Display', 'SF Pro Text', 'PingFang SC', sans-serif",
        "font_tag": "-apple-system, 'SF Pro Text', 'PingFang SC', sans-serif",
        "quote_color": "#0066CC",
        "deco": "none",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # 05 报纸杂志
    "newspaper": {
        "name": "报纸杂志",
        "bg": "#F0EDE4",
        "bg_gradient": None,
        "text": "#1A1A1A",
        "muted": "#555550",
        "accent": "#8B1A1A",
        "accent2": "#C8C4BA",
        "font_main": "'Georgia', 'Songti SC', 'Noto Serif CJK SC', serif",
        "font_tag": "'Georgia', 'Songti SC', serif",
        "quote_color": "#8B1A1A",
        "deco": "newspaper",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # 06 Bloomberg 终端
    "bloomberg": {
        "name": "Bloomberg 终端",
        "bg": "#0A0A0A",
        "bg_gradient": None,
        "text": "#E8E8E8",
        "muted": "#777777",
        "accent": "#FF6B00",
        "accent2": "#00CC44",
        "font_main": "'Courier New', 'Courier', 'Lucida Console', monospace",
        "font_tag": "'PingFang SC', 'Microsoft YaHei', sans-serif",
        "quote_color": "#FF6B00",
        "deco": "bloomberg",
        "letter_spacing": 2,
        "google_fonts": [],
    },
    # 07 水墨卷轴
    "ink": {
        "name": "水墨卷轴",
        "bg": "#F5F0E8",
        "bg_gradient": None,
        "text": "#2A2018",
        "muted": "#7A6A50",
        "accent": "#8B1A1A",
        "accent2": "#1A1008",
        "font_main": "'Songti SC', 'Noto Serif CJK SC', 'Source Han Serif CN', 'STSong', Georgia, serif",
        "font_tag": "'Songti SC', 'STSong', serif",
        "quote_color": "#8B1A1A",
        "deco": "ink",
        "letter_spacing": 5,
        "google_fonts": [],
    },
    # 08 蒸汽朋克
    "steampunk": {
        "name": "蒸汽朋克",
        "bg": "#1A1008",
        "bg_gradient": "linear-gradient(135deg, #1E1408 0%, #150F06 50%, #1E1408 100%)",
        "text": "#E8D4A0",
        "muted": "#A08040",
        "accent": "#C8A830",
        "accent2": "#B87333",
        "font_main": "'Rye', 'Noto Serif SC', 'Songti SC', 'STSong', Georgia, serif",
        "font_tag": "'Rye', 'Noto Serif SC', 'Songti SC', serif",
        "quote_color": "#C8A830",
        "deco": "steampunk",
        "letter_spacing": 3,
        "google_fonts": ["Rye", "Noto Serif SC"],
    },
    # 09-A 小红书 · 简洁正式
    "xhs": {
        "name": "小红书·简洁",
        "bg": "#FFFFFF",
        "bg_gradient": None,
        "text": "#1A1A1A",
        "muted": "#999999",
        "accent": "#FF2442",
        "accent2": "#FF6B8A",
        "font_main": "-apple-system, 'BlinkMacSystemFont', 'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif",
        "font_tag": "-apple-system, 'PingFang SC', sans-serif",
        "quote_color": "#FF2442",
        "deco": "xhs",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # 09-B 小红书 · 丰富活泼
    "xhs_rich": {
        "name": "小红书·丰富",
        "bg": "#FFF5F7",
        "bg_gradient": "linear-gradient(160deg, #FFF7F9 0%, #FFEFF3 55%, #FFE6EB 100%)",
        "text": "#1A1A1A",
        "muted": "#8E8E93",
        "accent": "#FF2442",
        "accent2": "#FF8FA8",
        "font_main": "-apple-system, 'BlinkMacSystemFont', 'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif",
        "font_tag": "-apple-system, 'PingFang SC', sans-serif",
        "quote_color": "#FF2442",
        "deco": "xhs_rich",
        "letter_spacing": 3,
        "google_fonts": [],
    },
    # 10 莫兰迪灰
    "morandi": {
        "name": "莫兰迪灰",
        "bg": "#E8E4DD",
        "bg_gradient": None,
        "text": "#4A453E",
        "muted": "#94897C",
        "accent": "#7C8B7E",
        "accent2": "#9A8C82",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#7C8B7E",
        "deco": "none",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 11 玻璃拟态
    "glass": {
        "name": "玻璃拟态",
        "bg": "#EDEBFF",
        "bg_gradient": "linear-gradient(135deg, #E6E9FF 0%, #F3E9FF 35%, #E9F7FF 70%, #FFF0F7 100%)",
        "text": "#1F2433",
        "muted": "#5B6072",
        "accent": "#6D5EF7",
        "accent2": "#4EC8E8",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#6D5EF7",
        "deco": "glass",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 12 故宫
    "palace": {
        "name": "故宫金红",
        "bg": "#0E0604",
        "bg_gradient": "linear-gradient(180deg, #0E0604 0%, #160A06 50%, #0E0604 100%)",
        "text": "#F0E6C8",
        "muted": "#9A8060",
        "accent": "#C8A45A",
        "accent2": "#C0392B",
        "font_main": "'Ma Shan Zheng', 'ZCOOL XiaoWei', 'Noto Serif SC', 'Songti SC', 'STSong', Georgia, serif",
        "font_tag": "'ZCOOL XiaoWei', 'Songti SC', serif",
        "quote_color": "#C8A45A",
        "deco": "palace",
        "letter_spacing": 6,
        "google_fonts": ["Ma Shan Zheng", "ZCOOL XiaoWei"],
    },
    # 13 清新绿
    "fresh": {
        "name": "清新绿",
        "bg": "#F1F7F0",
        "bg_gradient": None,
        "text": "#1F3A29",
        "muted": "#6B8475",
        "accent": "#2E9E5B",
        "accent2": "#6FB98F",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#2E9E5B",
        "deco": "fresh",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 14 大地原木
    "earthy": {
        "name": "大地原木",
        "bg": "#F3ECE1",
        "bg_gradient": None,
        "text": "#3D2E22",
        "muted": "#8A7460",
        "accent": "#B5683C",
        "accent2": "#8A8B5C",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#B5683C",
        "deco": "none",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 15 紫梦幻
    "dreamy": {
        "name": "紫梦幻",
        "bg": "#F6F2FB",
        "bg_gradient": None,
        "text": "#2E2541",
        "muted": "#7C7295",
        "accent": "#8B5CF6",
        "accent2": "#C084FC",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#8B5CF6",
        "deco": "dreamy",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 16 马卡龙
    "macaron": {
        "name": "马卡龙",
        "bg": "#FDF2F4",
        "bg_gradient": None,
        "text": "#4A2F38",
        "muted": "#9C7B85",
        "accent": "#EB6F8E",
        "accent2": "#F5A9C0",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#EB6F8E",
        "deco": "macaron",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 17 暗色极简
    "carbon": {
        "name": "暗色极简",
        "bg": "#14161A",
        "bg_gradient": None,
        "text": "#D6DAE0",
        "muted": "#8A929E",
        "accent": "#4FB8C4",
        "accent2": "#6CCFA8",
        "font_main": "'Inter', 'SF Mono', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'SF Mono', 'PingFang SC', sans-serif",
        "quote_color": "#4FB8C4",
        "deco": "carbon",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
    # 18 活力渐变
    "vivid": {
        "name": "活力渐变",
        "bg": "#FBF9FF",
        "bg_gradient": None,
        "text": "#1E1B2E",
        "muted": "#6B6480",
        "accent": "#7C3AED",
        "accent2": "#EC4899",
        "font_main": "'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif",
        "font_tag": "'Inter', 'PingFang SC', sans-serif",
        "quote_color": "#7C3AED",
        "deco": "vivid",
        "letter_spacing": 3,
        "google_fonts": ["Inter:wght@300;400;500;600"],
    },
}

# ─── SVG 构建 ───────────────────────────────────────────────────────

def escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def estimate_line_width(line, font_size, letter_spacing):
    """估算单行文字在 SVG 中的像素宽度（含 letter-spacing）"""
    # 中文字符占宽约 0.95em，英文/数字/标点约 0.55em
    char_w = font_size * 0.95
    half_w = font_size * 0.55
    width = 0
    for ch in line:
        if ord(ch) > 127:
            width += char_w
        else:
            width += half_w
    # letter-spacing 加在每字之后，最后一个字符不加
    if len(line) > 1:
        width += (len(line) - 1) * letter_spacing
    # 预留 8% 安全边距（不同字体渲染差异）
    return width * 1.08


def compute_font_size(lines, width, height, theme, text_width_ratio=0.78):
    """根据行数、字数和卡片尺寸计算合适字号"""
    n = len(lines) if lines else 1
    max_chars = max(len(line) for line in lines) if lines else 4

    # 最大字号上限（行数越多，上限越低）
    max_sizes = {1: 130, 2: 120, 3: 95, 4: 78, 5: 64}
    max_size = max_sizes.get(n, 56)
    min_size = 38

    # 可用宽度由 text_width_ratio 控制（图文布局更窄）
    usable_width = width * text_width_ratio
    # 可用高度：顶部标签到底部 footer 之间
    usable_height = height * 0.62

    letter_spacing = theme.get("letter_spacing", 4)

    # 先按字数给一个经验上限
    if max_chars >= 14:
        max_size = min(max_size, int(usable_width / (max_chars * 1.0)))
    elif max_chars >= 10:
        max_size = min(max_size, int(usable_width / (max_chars * 1.05)))
    elif max_chars >= 7:
        max_size = min(max_size, int(usable_width / (max_chars * 1.1)))

    # 再按高度限制
    line_height_at = lambda s: s * 1.6
    max_by_height = int(usable_height / (n * 1.6))
    max_size = min(max_size, max_by_height)

    # 从候选字号向下找，确保每行都不溢出
    for size in range(max_size, min_size - 1, -1):
        all_fit = all(
            estimate_line_width(line, size, letter_spacing) <= usable_width
            for line in lines
        )
        if all_fit:
            return max(size, min_size)
    return min_size


# ─── 照片背景 ──────────────────────────────────────────────────────

def load_background(path):
    """加载背景照片并转 base64 data URI（内嵌进 SVG，避免 file:// 被拦截）"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"背景图不存在: {path}")
    ext = p.suffix.lower()
    mimes = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    if ext not in mimes:
        raise ValueError(f"不支持的背景图格式: {ext}（请用 .png / .jpg / .webp）")
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mimes[ext]};base64,{b64}"


def resolve_theme(theme_key, options):
    """返回主题配置副本。当传入 --background 但主题非照片主题时，
    自动把文字/辅助色反转为亮色，保证压在照片上仍可读。"""
    t = dict(THEMES[theme_key])
    # 显式指定的字体优先级最高（--font-main / gen_cards.py 透传），覆盖主题自带字体。
    # 小字（标签/页码/署名）仍用主题的 font_tag，避免隶书小字号糊成一片。
    if options.get("font_main"):
        t["font_main"] = options["font_main"]
    if not options.get("background"):
        return t
    if t.get("photo"):
        return t
    # 非照片主题 + 照片背景 → 自动亮色反转
    t["text"] = "#F7F4EE"
    t["muted"] = "#D5CFC5"
    t["accent2"] = "#8A8278"
    t["bg_gradient"] = None
    t["deco"] = "none"
    t.setdefault("scrim", 0.55)
    t.setdefault("scrim_color", "#000000")
    t.setdefault("grain", 0.0)
    t.setdefault("desaturate", 1.0)
    t["photo"] = True
    return t


def build_photo_layers(width, height, options, t):
    """构建照片背景图层：defs（滤镜/渐变） + 照片 + 暗色遮罩 + 可选颗粒。
    返回 svg 片段列表，需插入在正文内容之前。"""
    bg_uri = options.get("background")
    if not bg_uri:
        return []

    scrim = options.get("scrim")
    if scrim is None:
        scrim = t.get("scrim", 0.55)
    scrim = max(0.0, min(0.92, float(scrim)))
    scrim_color = t.get("scrim_color", "#000000")

    blur = float(options.get("blur") or 0)
    desaturate = options.get("desaturate")
    if desaturate is None:
        desaturate = t.get("desaturate", 1.0)
    desaturate = max(0.0, min(1.0, float(desaturate)))

    grain = options.get("grain")
    if grain is None:
        grain = t.get("grain", 0.0)
    grain = max(0.0, min(0.4, float(grain)))

    defs = []
    # 照片滤镜：模糊 + 降饱和
    fx_nodes = []
    if blur > 0:
        fx_nodes.append(f'<feGaussianBlur stdDeviation="{blur}"/>')
    if desaturate < 1.0:
        fx_nodes.append(f'<feColorMatrix type="saturate" values="{desaturate:.3f}"/>')
    photo_filter_attr = ""
    if fx_nodes:
        defs.append(
            f'<filter id="photoFx" x="-15%" y="-15%" width="130%" height="130%" '
            f'color-interpolation-filters="sRGB">{"".join(fx_nodes)}</filter>'
        )
        photo_filter_attr = ' filter="url(#photoFx)"'

    # 暗色遮罩渐变：上下两端更重（压住标签与页脚），中段维持基准强度
    top = min(0.95, scrim + 0.16)
    bottom = min(0.95, scrim + 0.20)
    defs.append(
        f'<linearGradient id="scrimGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{scrim_color}" stop-opacity="{top:.3f}"/>'
        f'<stop offset="30%" stop-color="{scrim_color}" stop-opacity="{scrim:.3f}"/>'
        f'<stop offset="70%" stop-color="{scrim_color}" stop-opacity="{scrim:.3f}"/>'
        f'<stop offset="100%" stop-color="{scrim_color}" stop-opacity="{bottom:.3f}"/>'
        f'</linearGradient>'
    )

    # 文字投影：照片背景下保证边缘清晰
    defs.append(
        '<filter id="txtShadow" x="-25%" y="-25%" width="150%" height="150%" '
        'color-interpolation-filters="sRGB">'
        '<feDropShadow dx="0" dy="2" stdDeviation="7" flood-color="#000000" flood-opacity="0.6"/>'
        '</filter>'
    )

    if grain > 0:
        defs.append(
            '<filter id="grainFx" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>'
            '<feColorMatrix type="saturate" values="0"/>'
            '</filter>'
        )

    layers = [f'<defs>{"".join(defs)}</defs>']

    # 照片：slice 等价于 center-crop；模糊时向外扩边，避免边缘透出底色
    pad = int(blur * 3) if blur > 0 else 0
    layers.append(
        f'<image x="{-pad}" y="{-pad}" width="{width + pad * 2}" height="{height + pad * 2}" '
        f'href="{bg_uri}" preserveAspectRatio="xMidYMid slice"{photo_filter_attr}/>'
    )
    layers.append(f'<rect width="{width}" height="{height}" fill="url(#scrimGrad)"/>')

    if grain > 0:
        layers.append(
            f'<rect width="{width}" height="{height}" filter="url(#grainFx)" '
            f'opacity="{grain:.3f}" style="mix-blend-mode: overlay"/>'
        )

    return layers


def build_svg(theme, width, height, content, options):
    """生成统一布局的 SVG"""
    t = resolve_theme(theme, options)
    tag = content.get("tag", "人生随笔")
    lines = content.get("lines", ["未命名卡片"])
    subtitle = content.get("subtitle", "")
    page_number = content.get("page_number", 1)
    total_pages = content.get("total_pages", 1)
    account = content.get("account", "")

    show_tag = options.get("show_tag", True)
    show_subtitle = options.get("show_subtitle", True)
    show_page = options.get("show_page_number", True)
    show_account = options.get("show_account", True)

    # 文字位置：默认垂直居中（text_y_ratio=0.5）。可由 gen_cards.py 的
    # segments[].text_pos 或自动留白检测结果覆盖；x_ratio / anchor 支持靠边排版。
    y_ratio = max(0.0, min(1.0, float(options.get("text_y_ratio", 0.5))))
    x_ratio = max(0.0, min(1.0, float(options.get("text_x_ratio", 0.5))))
    anchor = options.get("text_anchor") or "middle"
    if anchor not in ("start", "middle", "end"):
        anchor = "middle"

    # 靠边排版时可用宽度随之收窄，避免文字溢出画面
    if anchor == "start":
        width_ratio = max(0.35, min(0.78, (1.0 - x_ratio) * 0.92))
    elif anchor == "end":
        width_ratio = max(0.35, min(0.78, x_ratio * 0.92))
    else:
        # text 布局原本固定 0.78，保持既有字号不变；image-text 布局才用可配比例
        width_ratio = (0.78 if options.get("layout", "text") == "text"
                       else options.get("text_width_ratio", 0.78))

    # anchor=start/end 时把起点收进可行域：极端 x_ratio 会让「下限 0.35 的宽度」
    # 从 0.9W 往右延伸到 1.25W（或往左到 -0.25W），文字整块溢出画面。
    if anchor == "start":
        x_ratio = min(x_ratio, max(0.10, 0.98 - width_ratio))
    elif anchor == "end":
        x_ratio = max(x_ratio, min(0.90, width_ratio + 0.02))
    else:
        # 居中排版时文字块向左右各延伸 width_ratio/2，x 太靠边会被画布裁掉
        half = width_ratio / 2
        x_ratio = min(max(x_ratio, half + 0.01), 0.99 - half)

    font_size = compute_font_size(lines, width, height, t, text_width_ratio=width_ratio)
    letter_spacing = t.get("letter_spacing", 4)

    line_height = font_size * 1.6
    text_block_h = len(lines) * line_height
    start_y = height * y_ratio - text_block_h / 2 - 20
    # 安全区：避开顶部标签(y=130)与底部页码(footer_y=height-130)
    min_start = 175 if show_tag else 100
    bottom_pad = 260 if subtitle else 185
    max_start = height - bottom_pad - text_block_h
    if max_start >= min_start:
        clamped = max(min_start, min(max_start, start_y))
        # y_ratio 太小/太大时会被安全区吃掉，表现为「换了参数但图没变」。
        # 打一行提示，别让它静默失效。
        if abs(clamped - start_y) > 1:
            effective = (clamped + text_block_h / 2 + 20) / height
            print("[warn] --text-y-ratio %.2f 超出安全区，实际生效 %.2f"
                  % (y_ratio, effective), file=sys.stderr)
        start_y = clamped
    else:
        # 两界交叉（矮画布 / 多行大字）时原来整段跳过 clamp，文字会压到页脚。
        # 空间不够也至少从安全区顶部起排，别让下半块盖住页码。
        start_y = min_start
    text_x = width * x_ratio

    # 背景（渐变由 build_html 的 CSS 处理，SVG 侧用纯色）
    bg_style = f"fill: {t['bg']}"
    bg_rect = f'<rect width="{width}" height="{height}" style="{bg_style}"/>'

    # 装饰元素
    decorations = build_decorations(theme, width, height, t)

    # 顶部标签
    tag_y = 130
    tag_parts = []
    if show_tag and tag:
        quote_left = f'<text x="{width/2 - 70}" y="{tag_y}" text-anchor="end" font-size="28" fill="{t["quote_color"]}" font-family="{t["font_tag"]}">"</text>'
        tag_text = f'<text x="{width/2}" y="{tag_y}" text-anchor="middle" font-size="24" fill="{t["muted"]}" font-family="{t["font_tag"]}" letter-spacing="6">{escape(tag)}</text>'
        quote_right = f'<text x="{width/2 + 70}" y="{tag_y}" text-anchor="start" font-size="28" fill="{t["quote_color"]}" font-family="{t["font_tag"]}">"</text>'
        tag_parts = [quote_left, tag_text, quote_right]

    # 主文案
    text_parts = []
    for i, line in enumerate(lines):
        y = start_y + i * line_height + font_size * 0.85
        # 如果只有一行，可以稍微粗一点
        weight = "500" if len(lines) <= 2 else "400"
        text_parts.append(
            f'<text x="{text_x}" y="{y}" text-anchor="{anchor}" font-size="{font_size}" '
            f'fill="{t["text"]}" font-family="{t["font_main"]}" font-weight="{weight}" '
            f'letter-spacing="{letter_spacing}">{escape(line)}</text>'
        )

    # 副标题
    subtitle_y = start_y + text_block_h + 70
    subtitle_parts = []
    if show_subtitle and subtitle:
        subtitle_parts.append(
            f'<text x="{width/2}" y="{subtitle_y}" text-anchor="middle" font-size="26" '
            f'fill="{t["muted"]}" font-family="{t["font_tag"]}" letter-spacing="3">— {escape(subtitle)} —</text>'
        )

    # 底部分隔线
    footer_y = height - 130
    footer_parts = [
        f'<line x1="{width * 0.1}" y1="{footer_y - 30}" x2="{width * 0.9}" y2="{footer_y - 30}" '
        f'stroke="{t["accent2"]}" stroke-width="1"/>'
    ]

    # 页码
    if show_page:
        page_text = f"No.{page_number:02d} / {total_pages:02d}"
        footer_parts.append(
            f'<text x="{width * 0.1}" y="{footer_y + 18}" text-anchor="start" font-size="22" '
            f'fill="{t["muted"]}" font-family="{t["font_tag"]}" letter-spacing="1">{page_text}</text>'
        )

    # 账号
    if show_account and account:
        footer_parts.append(
            f'<text x="{width * 0.9}" y="{footer_y + 18}" text-anchor="end" font-size="22" '
            f'fill="{t["muted"]}" font-family="{t["font_tag"]}" letter-spacing="1">{escape(account)}</text>'
        )

    # 组合
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        bg_rect,
    ]
    photo_layers = build_photo_layers(width, height, options, t)
    svg_parts.extend(photo_layers)
    svg_parts.extend(decorations)

    foreground = []
    foreground.extend(tag_parts)
    foreground.extend(text_parts)
    foreground.extend(subtitle_parts)
    foreground.extend(footer_parts)

    if photo_layers:
        # 照片背景下整组前景加投影，保证文字在任意画面上都清晰
        svg_parts.append('<g filter="url(#txtShadow)">')
        svg_parts.extend(foreground)
        svg_parts.append('</g>')
    else:
        svg_parts.extend(foreground)

    svg_parts.append('</svg>')

    return "\n".join(svg_parts)


def load_illustration(path):
    """加载插画文件：SVG 提取首个 <g> 内容；PNG/JPG 转 base64 data URI"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"插画文件不存在: {path}")
    ext = p.suffix.lower()
    if ext == ".svg":
        content = p.read_text(encoding="utf-8")
        # 提取第一个 <g> 元素（含嵌套），用于嵌入到新的卡片 SVG 中
        try:
            root = ET.fromstring(content.encode("utf-8"))
            ns = {"svg": "http://www.w3.org/2000/svg"}
            g = root.find(".//svg:g", ns)
            if g is None:
                g = root.find(".//{http://www.w3.org/2000/svg}g")
            if g is not None:
                # 移除原 SVG 里的 transform（如 translate(540,400)），
                # 避免与卡片里的 translate 叠加导致偏移
                if "transform" in g.attrib:
                    del g.attrib["transform"]
                # 移除可能冲突的命名空间前缀
                ET.register_namespace("", "http://www.w3.org/2000/svg")
                inner = ET.tostring(g, encoding="unicode")
                return ("svg_inner", inner)
        except ET.ParseError:
            pass
        # 解析失败则整体作为 foreignObject / image 使用（不常见）
        return ("svg_raw", content)
    elif ext in (".png", ".jpg", ".jpeg"):
        mime = "image/png" if ext == ".png" else "image/jpeg"
        data = p.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return ("raster", f"data:{mime};base64,{b64}")
    else:
        raise ValueError(f"不支持的插画格式: {ext}（请用 .svg / .png / .jpg）")


def build_image_text_svg(theme, width, height, content, options, illustration):
    """生成「图文卡片」布局：顶部插画 + 窄列居中文字 + 底部署名"""
    t = resolve_theme(theme, options)
    lines = content.get("lines", ["未命名卡片"])
    account = content.get("account", "")
    text_width_ratio = options.get("text_width_ratio", 0.65)

    # 字号按窄列计算
    font_size = compute_font_size(lines, width, height, t, text_width_ratio=text_width_ratio)
    letter_spacing = t.get("letter_spacing", 4)
    line_height = font_size * 1.7
    text_block_h = len(lines) * line_height

    # 布局比例（以 1080x1440 为基准，按高度缩放）
    illustration_y = int(height * 0.28)
    text_start_y = int(height * 0.54)
    # footer_y 固定基准，但需保证不压到文字（文字实际底部 + 安全间距）
    last_line_baseline = text_start_y + (len(lines) - 1) * line_height + font_size * 0.85
    text_block_bottom = last_line_baseline + font_size * 0.25
    footer_y = max(int(height * 0.82), int(text_block_bottom + 50))

    illust_type, illust_payload = illustration
    if illust_type == "svg_inner":
        # 将提取到的 <g> 居中放置在插画区；保留原 transform
        illustration_block = f'<g transform="translate({width/2}, {illustration_y})">{illust_payload}</g>'
    elif illust_type == "svg_raw":
        illustration_block = f'<g transform="translate({width/2}, {illustration_y})">{illust_payload}</g>'
    else:  # raster
        max_w = int(width * 0.55)
        max_h = int(height * 0.32)
        illustration_block = (
            f'<image x="{width/2 - max_w/2}" y="{illustration_y - max_h/2}" '
            f'width="{max_w}" height="{max_h}" href="{illust_payload}" '
            f'preserveAspectRatio="xMidYMid meet"/>'
        )

    text_parts = []
    max_text_width = width * text_width_ratio
    for i, line in enumerate(lines):
        y = text_start_y + i * line_height + font_size * 0.85
        text_parts.append(
            f'<text x="{width/2}" y="{y}" text-anchor="middle" font-size="{font_size}" '
            f'fill="{t["text"]}" font-family="{t["font_main"]}" font-weight="400" '
            f'letter-spacing="{letter_spacing}">{escape(line)}</text>'
        )

    footer_parts = []
    if account:
        line_x1 = width * 0.42
        line_x2 = width * 0.58
        footer_parts.append(
            f'<line x1="{line_x1}" y1="{footer_y}" x2="{line_x2}" y2="{footer_y}" '
            f'stroke="{t["accent"]}" stroke-width="2"/>'
        )
        footer_parts.append(
            f'<text x="{width/2}" y="{footer_y + 40}" text-anchor="middle" font-size="22" '
            f'fill="{t["muted"]}" font-family="{t["font_tag"]}" letter-spacing="6">{escape(account)}</text>'
        )

    decorations = build_decorations(theme, width, height, t)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{t["bg"]}"/>',
    ]
    photo_layers = build_photo_layers(width, height, options, t)
    svg_parts.extend(photo_layers)
    svg_parts.extend(decorations)

    # 插画独立于阴影组之外：投影只服务于压在照片上的文字，不应作用于插画本身
    svg_parts.append(illustration_block)
    foreground = text_parts + footer_parts
    if photo_layers:
        svg_parts.append('<g filter="url(#txtShadow)">')
        svg_parts.extend(foreground)
        svg_parts.append('</g>')
    else:
        svg_parts.extend(foreground)

    svg_parts.append('</svg>')

    return "\n".join(svg_parts)


def build_decorations(theme, width, height, t):
    """根据主题添加装饰元素"""
    decos = []
    deco = t.get("deco", "none")

    if deco == "stars" or theme == "y2k":
        # Y2K 星星和十字装饰
        decos.append(f'<polygon points="{width-120},80 {width-115},95 {width-100},100 {width-115},105 {width-120},120 {width-125},105 {width-140},100 {width-125},95" fill="{t["accent2"]}" opacity="0.8"/>')
        decos.append(f'<polygon points="120,180 125,195 140,200 125,205 120,220 115,205 100,200 115,195" fill="{t["accent"]}" opacity="0.7"/>')
        decos.append(f'<text x="{width-90}" y="{height-160}" font-size="48" fill="{t["accent"]}" opacity="0.5">✦</text>')
        decos.append(f'<text x="90" y="{height-140}" font-size="36" fill="{t["accent2"]}" opacity="0.5">✦</text>')
    elif deco == "doodles" or theme == "doodle":
        decos.append(f'<path d="M {width-140},70 Q {width-120},90 {width-140},110 Q {width-160},90 {width-140},70" fill="none" stroke="{t["accent"]}" stroke-width="3" stroke-linecap="round"/>')
        decos.append(f'<path d="M 110,120 L 130,140 M 130,120 L 110,140" stroke="{t["accent2"]}" stroke-width="4" stroke-linecap="round"/>')
        decos.append(f'<circle cx="{width-100}" cy="{height-140}" r="8" fill="none" stroke="{t["accent"]}" stroke-width="3"/>')
        decos.append(f'<path d="M 90,{height-130} Q 110,{height-150} 130,{height-130}" fill="none" stroke="{t["accent2"]}" stroke-width="3" stroke-linecap="round"/>')
    elif deco == "dots" or theme == "pop":
        for cx, cy, r, color in [
            (width - 100, 100, 18, t["accent"]),
            (width - 70, 140, 10, t["accent2"]),
            (100, height - 120, 14, t["accent"]),
            (140, height - 90, 8, t["accent2"]),
            (width - 130, height - 100, 12, t["accent"]),
        ]:
            decos.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.85"/>')
    elif deco == "warm" or theme == "warm":
        decos.append(f'<circle cx="{width-90}" cy="90" r="3" fill="{t["accent"]}" opacity="0.5"/>')
        decos.append(f'<circle cx="{width-110}" cy="110" r="2" fill="{t["accent"]}" opacity="0.4"/>')
        decos.append(f'<circle cx="90" cy="{height-100}" r="3" fill="{t["accent"]}" opacity="0.5"/>')
    elif deco == "warm_illust" or theme == "warm_illust":
        # 温暖简笔哲思：极淡琥珀色光晕 + 小点，不抢插画风头
        decos.append(f'<circle cx="{width-120}" cy="120" r="4" fill="{t["accent"]}" opacity="0.25"/>')
        decos.append(f'<circle cx="{width-145}" cy="145" r="2.5" fill="{t["accent"]}" opacity="0.18"/>')
        decos.append(f'<circle cx="120" cy="{height-120}" r="3" fill="{t["accent"]}" opacity="0.22"/>')
    elif deco == "palace" or theme == "palace":
        seal_x, seal_y, seal_r = width - 100, 100, 28
        decos.append(f'<rect x="{seal_x - seal_r}" y="{seal_y - seal_r}" width="{seal_r * 2}" height="{seal_r * 2}" fill="{t["accent2"]}" opacity="0.85" rx="3"/>')
        decos.append(f'<text x="{seal_x}" y="{seal_y + 8}" text-anchor="middle" font-size="22" fill="{t["accent"]}" font-family="{t["font_main"]}">印</text>')
        decos.append(f'<path d="M 40,40 L 80,40 M 40,40 L 40,80" stroke="{t["accent"]}" stroke-width="2" opacity="0.6"/>')
        decos.append(f'<path d="M {width-40},40 L {width-80},40 M {width-40},40 L {width-40},80" stroke="{t["accent"]}" stroke-width="2" opacity="0.6"/>')
        decos.append(f'<path d="M 40,{height-40} L 80,{height-40} M 40,{height-40} L 40,{height-80}" stroke="{t["accent"]}" stroke-width="2" opacity="0.6"/>')
        decos.append(f'<path d="M {width-40},{height-40} L {width-80},{height-40} M {width-40},{height-40} L {width-40},{height-80}" stroke="{t["accent"]}" stroke-width="2" opacity="0.6"/>')
    elif deco == "cyberpunk" or theme == "cyberpunk":
        # 网格线 + 发光点
        for i in range(0, width, 60):
            decos.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{height}" stroke="{t["accent"]}" stroke-width="0.5" opacity="0.06"/>')
        for j in range(0, height, 60):
            decos.append(f'<line x1="0" y1="{j}" x2="{width}" y2="{j}" stroke="{t["accent"]}" stroke-width="0.5" opacity="0.06"/>')
        decos.append(f'<circle cx="{width-80}" cy="80" r="4" fill="{t["accent"]}" opacity="0.8"/>')
        decos.append(f'<circle cx="{width-100}" cy="100" r="2" fill="{t["accent2"]}" opacity="0.6"/>')
        decos.append(f'<circle cx="80" cy="{height-80}" r="3" fill="{t["accent"]}" opacity="0.7"/>')
    elif deco == "newspaper" or theme == "newspaper":
        # 双线边框
        decos.append(f'<rect x="30" y="30" width="{width-60}" height="{height-60}" fill="none" stroke="{t["accent2"]}" stroke-width="1"/>')
        decos.append(f'<rect x="36" y="36" width="{width-72}" height="{height-72}" fill="none" stroke="{t["accent2"]}" stroke-width="0.5"/>')
    elif deco == "bloomberg" or theme == "bloomberg":
        # 扫描线
        for j in range(0, height, 4):
            decos.append(f'<line x1="0" y1="{j}" x2="{width}" y2="{j}" stroke="{t["accent"]}" stroke-width="0.3" opacity="0.04"/>')
        decos.append(f'<rect x="0" y="0" width="4" height="{height}" fill="{t["accent"]}" opacity="0.6"/>')
    elif deco == "ink" or theme == "ink":
        # 水墨晕圈
        decos.append(f'<ellipse cx="{width-100}" cy="100" rx="60" ry="40" fill="{t["accent2"]}" opacity="0.04"/>')
        decos.append(f'<ellipse cx="100" cy="{height-100}" rx="50" ry="35" fill="{t["accent"]}" opacity="0.05"/>')
        # 印章
        decos.append(f'<rect x="{width-80}" y="{height-80}" width="40" height="40" fill="{t["accent"]}" opacity="0.8" rx="2"/>')
        decos.append(f'<text x="{width-60}" y="{height-55}" text-anchor="middle" font-size="18" fill="{t["bg"]}" font-family="{t["font_main"]}">墨</text>')
    elif deco == "steampunk" or theme == "steampunk":
        # 齿轮装饰
        cx, cy, r = width - 90, 90, 25
        gear = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["accent"]}" stroke-width="2" opacity="0.5"/>'
        for a in range(0, 360, 45):
            rad = math.radians(a)
            x1 = cx + math.cos(rad) * r
            y1 = cy + math.sin(rad) * r
            x2 = cx + math.cos(rad) * (r + 8)
            y2 = cy + math.sin(rad) * (r + 8)
            gear += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["accent"]}" stroke-width="3" opacity="0.5"/>'
        decos.append(gear)
        decos.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t["accent2"]}" opacity="0.4"/>')
        # 铜管装饰
        decos.append(f'<rect x="60" y="{height-60}" width="80" height="6" fill="{t["accent2"]}" opacity="0.3" rx="3"/>')
    elif deco == "xhs" or theme == "xhs":
        # 小红书·简洁：45°极淡斜纹（纸张质感）+ 少量小圆点，保持呼吸感
        stripes = []
        step = 26
        x = -height
        while x < width + height:
            stripes.append(
                f'<line x1="{x}" y1="0" x2="{x + height}" y2="{height}" '
                f'stroke="{t["accent"]}" stroke-width="1" opacity="0.035"/>'
            )
            x += step
        decos.append("".join(stripes))
        decos.append(f'<circle cx="{width-70}" cy="70" r="6" fill="{t["accent"]}" opacity="0.15"/>')
        decos.append(f'<circle cx="{width-90}" cy="90" r="4" fill="{t["accent2"]}" opacity="0.2"/>')
        decos.append(f'<circle cx="70" cy="{height-70}" r="5" fill="{t["accent"]}" opacity="0.15"/>')
    elif deco == "xhs_rich" or theme == "xhs_rich":
        # 小红书·丰富：手账圆点纹 + 毛玻璃光晕 + 三段渐变波浪线
        dots = []
        gap = 46
        y = gap
        while y < height:
            x = gap
            while x < width:
                dots.append(
                    f'<circle cx="{x}" cy="{y}" r="2.2" fill="{t["accent"]}" opacity="0.10"/>'
                )
                x += gap
            y += gap
        decos.append("".join(dots))
        # 毛玻璃光晕
        decos.append(f'<circle cx="{width-110}" cy="150" r="90" fill="{t["accent2"]}" opacity="0.13"/>')
        decos.append(f'<circle cx="90" cy="{height-180}" r="110" fill="{t["accent"]}" opacity="0.07"/>')
        # 顶部三段渐变波浪线（模式B 标志性装饰）
        wx = width // 2 - 26
        wy = 150
        decos.append(f'<rect x="{wx}" y="{wy}" width="28" height="5" rx="2.5" fill="{t["accent"]}" opacity="0.9"/>')
        decos.append(f'<rect x="{wx+32}" y="{wy}" width="14" height="5" rx="2.5" fill="{t["accent"]}" opacity="0.5"/>')
        decos.append(f'<rect x="{wx+50}" y="{wy}" width="7" height="5" rx="2.5" fill="{t["accent"]}" opacity="0.25"/>')
    elif deco == "glass" or theme == "glass":
        # 模糊光斑
        decos.append(f'<circle cx="{width-120}" cy="120" r="40" fill="{t["accent"]}" opacity="0.08"/>')
        decos.append(f'<circle cx="120" cy="{height-120}" r="50" fill="{t["accent2"]}" opacity="0.08"/>')
        decos.append(f'<circle cx="{width-80}" cy="{height-200}" r="30" fill="{t["accent"]}" opacity="0.06"/>')
    elif deco == "fresh" or theme == "fresh":
        # 叶子装饰
        decos.append(f'<ellipse cx="{width-80}" cy="80" rx="12" ry="6" fill="{t["accent"]}" opacity="0.2" transform="rotate(-30 {width-80} 80)"/>')
        decos.append(f'<ellipse cx="80" cy="{height-80}" rx="10" ry="5" fill="{t["accent2"]}" opacity="0.25" transform="rotate(30 80 {height-80})"/>')
    elif deco == "dreamy" or theme == "dreamy":
        # 闪烁星点
        decos.append(f'<circle cx="{width-90}" cy="90" r="3" fill="{t["accent"]}" opacity="0.4"/>')
        decos.append(f'<circle cx="{width-110}" cy="70" r="2" fill="{t["accent2"]}" opacity="0.5"/>')
        decos.append(f'<circle cx="90" cy="{height-90}" r="2" fill="{t["accent"]}" opacity="0.4"/>')
        decos.append(f'<circle cx="70" cy="{height-110}" r="3" fill="{t["accent2"]}" opacity="0.3"/>')
    elif deco == "macaron" or theme == "macaron":
        # 甜美小圆点
        for cx, cy, r in [
            (width - 80, 80, 10), (width - 100, 100, 6),
            (80, height - 80, 8), (100, height - 100, 5),
        ]:
            decos.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["accent2"]}" opacity="0.3"/>')
    elif deco == "carbon" or theme == "carbon":
        # 代码风格小方块
        decos.append(f'<rect x="{width-90}" y="70" width="6" height="6" fill="{t["accent"]}" opacity="0.4"/>')
        decos.append(f'<rect x="{width-78}" y="70" width="6" height="6" fill="{t["accent2"]}" opacity="0.3"/>')
        decos.append(f'<rect x="{width-66}" y="70" width="6" height="6" fill="{t["accent"]}" opacity="0.2"/>')
        decos.append(f'<rect x="70" y="{height-80}" width="6" height="6" fill="{t["accent2"]}" opacity="0.3"/>')
    elif deco == "vivid" or theme == "vivid":
        # 渐变光斑
        decos.append(f'<circle cx="{width-100}" cy="100" r="25" fill="{t["accent"]}" opacity="0.1"/>')
        decos.append(f'<circle cx="100" cy="{height-100}" r="20" fill="{t["accent2"]}" opacity="0.1"/>')
        decos.append(f'<circle cx="{width-60}" cy="{height-180}" r="15" fill="{t["accent2"]}" opacity="0.08"/>')
    # none / morandi / apple / cowork / earthy / elegant 无装饰
    return decos


def build_html(theme, width, height, content, options, illustration=None):
    """把 SVG 包装成 HTML 供 Chrome 渲染"""
    t = resolve_theme(theme, options)
    layout = options.get("layout", "text")
    if layout == "image-text":
        if illustration is None:
            raise ValueError("image-text 布局必须提供 --illustration 插画文件")
        svg = build_image_text_svg(theme, width, height, content, options, illustration)
    else:
        svg = build_svg(theme, width, height, content, options)

    # 如果主题有渐变背景，用 CSS 实现更稳
    bg_css = f"background: {t['bg']};"
    if t["bg_gradient"]:
        bg_css = f"background: {t['bg_gradient']};"

    # Google Fonts CDN 加载：多镜像 fallback，确保国内可用
    # 策略：同时加载 Google 原始 CDN + 国内镜像，谁先到用谁
    # 镜像列表按优先级排序：国内镜像优先（Chrome headless 在国内访问 Google 不稳定）
    google_fonts = t.get("google_fonts", [])
    fonts_links = []
    if google_fonts:
        families = "&".join(f"family={f.replace(' ', '+')}" for f in google_fonts)
        # 多镜像：<link> 标签并行加载，浏览器自动用最先返回的 CSS
        # 1. fonts.loli.net — 国内社区镜像，API 完全兼容
        # 2. fonts.googleapis.cn — Google 官方中国镜像
        # 3. fonts.googleapis.com — Google 原始（海外 fallback）
        mirrors = [
            ("fonts.loli.net", "https://fonts.loli.net"),
            ("fonts.googleapis.cn", "https://fonts.googleapis.cn"),
            ("fonts.googleapis.com", "https://fonts.googleapis.com"),
        ]
        for domain, base_url in mirrors:
            fonts_links.append(
                f'<link href="{base_url}/css2?{families}&display=swap" rel="stylesheet">'
            )

        # 额外保险：JS 检测字体是否加载成功，失败则动态注入镜像 CSS
        font_names_js = json.dumps([f.split(":")[0].strip() for f in google_fonts])
        fonts_js = f'''<script>
(function() {{
    var fontNames = {font_names_js};
    var mirrors = [
        'https://fonts.loli.net/css2?{families}&display=swap',
        'https://fonts.googleapis.cn/css2?{families}&display=swap'
    ];
    // 等 3 秒后检查字体是否加载成功
    setTimeout(function() {{
        fontNames.forEach(function(name) {{
            try {{
                var loaded = document.fonts.check('16px "' + name + '"');
                if (!loaded) {{
                    console.log('Font not loaded: ' + name + ', injecting mirror');
                    var link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.href = mirrors[0];
                    document.head.appendChild(link);
                }}
            }} catch(e) {{}}
        }});
    }}, 3000);
}})();
</script>'''

    fonts_link = "\n    ".join(fonts_links)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>card</title>
    {fonts_link}
    {fonts_js if google_fonts else ""}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {width}px;
            height: {height}px;
            {bg_css}
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        svg {{
            width: {width}px;
            height: {height}px;
            display: block;
        }}
    </style>
</head>
<body>
{svg}
</body>
</html>'''
    return html


# ─── PNG 渲染 ──────────────────────────────────────────────────────

def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def render_png(html_content, output_path, width=1080, height=1440):
    """用 Chrome headless 将 HTML 渲染为 PNG"""
    tmp_html = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    tmp_html.write(html_content)
    tmp_html.close()

    try:
        chrome = find_chrome()
        if not chrome:
            print("[ERROR] 未找到 Chrome/Chromium", file=sys.stderr)
            return False

        # 直接用 Chrome screenshot
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=10000",
            f"--window-size={width},{height}",
            "--screenshot=" + os.path.abspath(output_path),
            "file://" + tmp_html.name,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] 渲染失败: {result.stderr}", file=sys.stderr)
            return False

        return True
    finally:
        os.unlink(tmp_html.name)


# ─── Demo 内容 ─────────────────────────────────────────────────────

DEMO_CONTENT = {
    "tag": "人生随笔",
    "lines": [
        "我们花了太多时间",
        "去理解世界",
        "却太少时间去理解自己"
    ],
    "subtitle": "关于自省",
    "page_number": 5,
    "total_pages": 6,
    "account": "@雨夜心灯",
}

# ─── CLI ───────────────────────────────────────────────────────────

def parse_lines(value):
    if value is None:
        return []
    return [line.strip() for line in value.replace("\\n", "\n").split("\n") if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="小红书风格统一卡片生成器")
    parser.add_argument("--theme", default="warm", help=f"主题 ({'/'.join(THEMES.keys())})")
    parser.add_argument("--all-themes", action="store_true", help="生成全部主题示例")
    parser.add_argument("--list-themes", action="store_true", help="打印全部主题清单后退出")
    parser.add_argument("--demo", action="store_true", help="使用示例内容")
    parser.add_argument("--content", help="JSON 文件路径")
    parser.add_argument("--tag", help="顶部标签")
    parser.add_argument("--lines", help="主文案，用 \\n 分隔")
    parser.add_argument("--subtitle", help="副标题")
    parser.add_argument("--page-number", type=int, help="当前页码")
    parser.add_argument("--total-pages", type=int, help="总页数")
    parser.add_argument("--account", help="账号名")
    parser.add_argument("--hide-tag", action="store_true", help="隐藏顶部标签")
    parser.add_argument("--hide-subtitle", action="store_true", help="隐藏副标题")
    parser.add_argument("--hide-page-number", action="store_true", help="隐藏页码")
    parser.add_argument("--hide-account", action="store_true", help="隐藏账号")
    parser.add_argument("--layout", choices=["text", "image-text"], default="text", help="布局：text（默认纯文字）或 image-text（顶部插画+文字）")
    parser.add_argument("--illustration", help="image-text 布局的插画文件路径（.svg / .png / .jpg）")
    parser.add_argument("--image-text-width", type=float, default=0.65, help="image-text 文字区宽度占比（0.5-0.8，默认 0.65）")
    # ── 照片背景（AI 生成或用户自备，技能不内置素材） ──
    parser.add_argument("--background", help="满幅背景照片路径（.png/.jpg/.webp），自动 center-crop 铺满")
    parser.add_argument("--scrim", type=float, help="暗色遮罩强度 0-0.92（默认取主题预设，通常 0.5-0.55）")
    parser.add_argument("--blur", type=float, default=0, help="背景高斯模糊半径，默认 0（建议 2-6）")
    parser.add_argument("--desaturate", type=float, nargs="?", const=0.65,
                        help="背景降饱和 0-1，1=原色。不带值时取 0.65")
    parser.add_argument("--grain", type=float, help="胶片颗粒强度 0-0.4（默认取主题预设）")
    # ── 古风字体与文字位置（历史题材口播视频用） ──
    parser.add_argument("--font-main", help="覆盖主题的 font_main（CSS font-family 字符串）。优先级高于主题自带字体")
    parser.add_argument("--text-y-ratio", type=float, default=0.5,
                        help="文字块中心在卡片高度的相对位置 0-1，默认 0.5（居中）")
    parser.add_argument("--text-x-ratio", type=float, default=0.5,
                        help="文字锚点在卡片宽度的相对位置 0-1，默认 0.5（居中）")
    parser.add_argument("--text-anchor", choices=["start", "middle", "end"], default="middle",
                        help="文字对齐方式，默认 middle")
    parser.add_argument("--width", type=int, default=1080, help="输出宽度")
    parser.add_argument("--height", type=int, default=1440, help="输出高度")
    parser.add_argument("--output", "-o", help="输出 PNG 路径")
    parser.add_argument("--output-dir", default="output", help="all-themes 输出目录")
    args = parser.parse_args()

    if args.list_themes:
        print(f"共 {len(THEMES)} 种主题：")
        for key, cfg in THEMES.items():
            print(f"  {key:<12} {cfg['name']}")
        return

    # 内容
    if args.content:
        with open(args.content, "r", encoding="utf-8") as f:
            content = json.load(f)
    elif args.demo:
        content = DEMO_CONTENT.copy()
    else:
        content = {}
        if args.tag: content["tag"] = args.tag
        if args.lines: content["lines"] = parse_lines(args.lines)
        if args.subtitle: content["subtitle"] = args.subtitle
        if args.page_number is not None: content["page_number"] = args.page_number
        if args.total_pages is not None: content["total_pages"] = args.total_pages
        if args.account: content["account"] = args.account

    # 默认值
    content.setdefault("tag", "人生随笔")
    content.setdefault("lines", ["未命名卡片"])
    content.setdefault("subtitle", "")
    content.setdefault("page_number", 1)
    content.setdefault("total_pages", 1)
    content.setdefault("account", "")

    # 显示选项（默认全显示，--hide-* 隐藏）
    options = {
        "show_tag": not args.hide_tag,
        "show_subtitle": not args.hide_subtitle,
        "show_page_number": not args.hide_page_number,
        "show_account": not args.hide_account,
        "layout": args.layout,
        "text_width_ratio": max(0.5, min(0.8, args.image_text_width)),
        "scrim": args.scrim,
        "blur": args.blur,
        "desaturate": args.desaturate,
        "grain": args.grain,
        "font_main": args.font_main,
        "text_y_ratio": args.text_y_ratio,
        "text_x_ratio": args.text_x_ratio,
        "text_anchor": args.text_anchor,
    }

    # 加载背景照片（转 base64 内嵌，避免 Chrome file:// 限制）
    if args.background:
        try:
            options["background"] = load_background(args.background)
        except (FileNotFoundError, ValueError, OSError) as e:
            print(f"背景图加载失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # 照片主题缺少背景图会静默退化为纯色卡片，这里显式告警
        picked = list(THEMES.keys()) if args.all_themes else [args.theme]
        hit = [k for k in picked if THEMES.get(k, {}).get("photo")]
        if hit:
            print(
                f"警告: 主题 {', '.join(hit)} 为照片背景主题，未提供 --background，"
                f"将退化为纯色底卡片。如需照片效果请加 --background <图片路径>。",
                file=sys.stderr,
            )

    # 加载插画
    illustration = None
    if args.layout == "image-text":
        if not args.illustration:
            parser.error("image-text 布局需要 --illustration 指定插画文件")
        illustration = load_illustration(args.illustration)

    if args.all_themes:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        results = []
        for theme in THEMES:
            out_path = str(out_dir / f"{theme}.png")
            print(f"生成 {theme} ...")
            html = build_html(theme, args.width, args.height, content, options, illustration=illustration)
            if render_png(html, out_path, args.width, args.height):
                results.append((theme, out_path))
        print(f"\n完成！共生成 {len(results)} 张")
        for theme, path in results:
            print(f"  {theme:10s} → {path}")
    else:
        if args.theme not in THEMES:
            print(f"未知主题: {args.theme}")
            print(f"可用: {', '.join(THEMES.keys())}")
            sys.exit(1)

        out_path = args.output or f"output/{args.theme}.png"
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)

        html = build_html(args.theme, args.width, args.height, content, options, illustration=illustration)
        if not render_png(html, out_path, args.width, args.height):
            print(f"[ERROR] 渲染失败，未生成图片: {out_path}", file=sys.stderr)
            sys.exit(1)
        # render_png 成功也可能没有落盘（--output 传了目录、路径不可写等），
        # 不校验的话上层会拿一个不存在的路径继续发小红书。
        if not os.path.isfile(out_path):
            print(f"[ERROR] 渲染返回成功但文件不存在: {out_path}", file=sys.stderr)
            sys.exit(1)
        print(f"输出: {out_path}")


if __name__ == "__main__":
    main()
