# -*- coding: utf-8 -*-
"""微博配图生成器 - 支持4种风格"""
import argparse
import os
import sys
import subprocess
import platform

from PIL import Image, ImageDraw, ImageFont


def try_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",   # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/arial.ttf",   # Arial
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def warmth_card(text, output_path):
    """温暖生活风 - 橙色调，适合日常/职场话题"""
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), "#FFF8F0")
    draw = ImageDraw.Draw(img)

    # 顶部渐变条
    draw.rectangle([(0, 0), (W, 10)], fill="#FF8C42")
    draw.rectangle([(0, 0), (8, H)], fill="#FF8C42")
    draw.ellipse([(800, 1000), (W, H)], fill="#FFE4C4")

    title_font  = try_font(52)
    body_font   = try_font(30)
    small_font  = try_font(22)

    # 主标题
    draw.text((40, 60), "旅行前夜，你还在手忙脚乱？", font=title_font, fill="#2D2D2D")

    # 副标题
    draw.text((40, 140), "AI 5分钟搞定你的出行方案", font=body_font, fill="#FF6B35")

    # 分割线
    draw.line([(40, 200), (W - 40, 200)], fill="#FF8C42", width=2)

    # 三个场景（示例）
    scenarios = [
        "✈️  以前：翻攻略app，纠结4天定下来",
        "🤖  现在：把目的地丢给AI，5分钟后路线全出来",
        "📋  结果——景点路线、酒店推荐、餐厅预订清单全出炉",
    ]
    y = 230
    for line in scenarios:
        draw.text((40, y), line, font=body_font, fill="#333333")
        y += 60

    # 金句
    draw.line([(40, y + 20), (W - 40, y + 20)], fill="#FFD700", width=1)
    draw.text((40, y + 40), "不是策略变多了，是你多了一个", font=body_font, fill="#FF6B35")
    draw.text((40, y + 100), "比你更懂你时间的那个人", font=body_font, fill="#FF6B35")

    # 标签
    draw.text((40, H - 130), "#AI科普# #AI生活观察#", font=small_font, fill="#AAAAAA")
    draw.text((40, H - 95), "#生活# #职场# #效率# #日常#", font=small_font, fill="#AAAAAA")

    img.save(output_path, "PNG")
    print(f"[warmth] OK: {output_path}")


def tech_card(text, output_path):
    """科技感深色卡 - 深蓝底+金色字，适合AI工具/身份标签"""
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), "#1a1a2e")
    draw = ImageDraw.Draw(img)

    # 渐变背景
    for y in range(H):
        r = int(26 + (y / H) * 20)
        g = int(26 + (y / H) * 15)
        b = int(46 + (y / H) * 30)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 顶部半透明标题栏
    title_bar = Image.new("RGBA", (W, 120), (0, 0, 0, 180))
    img.paste(title_bar, (0, 0), title_bar)

    title_font  = try_font(52)
    sub_font    = try_font(38)
    body_font   = try_font(34)
    small_font  = try_font(28)

    # 标题
    title = "AI时代的三种打工人"
    tb = draw.textbbox((0, 0), title, font=title_font)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 35), title, fill="#f39c12", font=title_font)

    # 三种人卡片
    types = [
        ("① 被炼化者", "#e74c3c", "工作越努力，留下的数据素材越多\n离职后被AI炼化得越彻底"),
        ("② 观望者", "#f39c12", "听说AI能炼化同事\n开始担心会不会轮到自己"),
        ("③ 驾驭者", "#2ecc71", "主动把技能炼化成\n可交易的数字资产\n让知识产生被动收入"),
    ]
    y_start = 170
    for i, (title_text, color, desc) in enumerate(types):
        card_box = Image.new("RGBA", (W - 80, 290), (40, 40, 60, 220))
        img.paste(card_box, (40, y_start + i * 315), card_box)
        draw.text((80, y_start + i * 315 + 30), title_text, fill=color, font=sub_font)
        lines = desc.split("\n")
        for j, line in enumerate(lines):
            draw.text((100, y_start + i * 315 + 90 + j * 52), line, fill="#ecf0f1", font=body_font)

    # 底部结论
    conc_y = 1130
    conc_box = Image.new("RGBA", (W, 140), (0, 0, 0, 180))
    img.paste(conc_box, (0, conc_y), conc_box)
    draw.text(((W - 200) // 2, conc_y + 25), "同样的技术", fill="#3498db", font=body_font)
    draw.text(((W - 500) // 2, conc_y + 75), "有人恐惧被替代，有人把它变成杠杆", fill="#95a5a6", font=small_font)

    img.save(output_path, "PNG", quality=95)
    print(f"[tech] OK: {output_path}")


def midnight_card(text, output_path):
    """深夜风 - 深色背景+蓝绿渐变，适合深夜互动"""
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), color=(8, 12, 20))
    draw = ImageDraw.Draw(img)

    # 蓝绿渐变背景
    for y in range(H):
        ratio = y / H
        r = int(8 + ratio * 20)
        g = int(12 + ratio * 60)
        b = int(20 + ratio * 80)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 顶部装饰线
    draw.rectangle([40, 40, W - 40, 44], fill=(0, 200, 180))

    font_large  = try_font(72)
    font_medium = try_font(50)
    font_small  = try_font(38)

    # 主标题
    title_text = "🌙 深夜话题"
    tb = draw.textbbox((0, 0), title_text, font=font_large)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 80), title_text, font=font_large, fill=(0, 220, 200))

    # 问题文本（示例，可通过 --text 传入自定义）
    q_lines = [
        ("你有没有过这种经历——", False),
        ("明明跟AI聊得很顺畅，", False),
        ("却忍不住想：它到底是", False),
        ("「懂」我，还是只是", False),
        ("「算得准」？", False),
        ("", False),
        ("今晚不说对错，", True),
        ("评论区随便聊聊 🔥", True),
    ]
    y_pos = 240
    for line_text, highlight in q_lines:
        if not line_text:
            y_pos += 30
            continue
        tb = draw.textbbox((0, 0), line_text, font=font_medium)
        tw = tb[2] - tb[0]
        fill = (0, 220, 200) if highlight else (210, 225, 235)
        draw.text(((W - tw) // 2, y_pos), line_text, font=font_medium, fill=fill)
        y_pos += 68

    # 分割线
    y_pos += 15
    draw.rectangle([120, y_pos, W - 120, y_pos + 4], fill=(0, 200, 180))

    # 标签
    y_pos += 35
    tags = ["#深夜互动话题#", "#AI科普#", "#AI生活观察#"]
    for tag in tags:
        tb = draw.textbbox((0, 0), tag, font=font_small)
        tw = tb[2] - tb[0]
        draw.text(((W - tw) // 2, y_pos), tag, font=font_small, fill=(130, 190, 190))
        y_pos += 60

    # 底部装饰线
    draw.rectangle([40, H - 60, W - 40, H - 56], fill=(0, 200, 180))

    img.save(output_path, "PNG")
    print(f"[midnight] OK: {output_path}")


def contrast_card(left_title, right_title, left_items, right_items, output_path, center_text=""):
    """左右对比卡 - 适合工具实测，1080×675"""
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), (10, 12, 20))
    draw = ImageDraw.Draw(img)

    subtitle_font = try_font(36)
    body_font     = try_font(30)
    small_font    = try_font(24)

    # 顶部标识栏
    draw.rectangle([0, 0, W, 90], fill=(0, 180, 255))
    draw.text((30, 18), "AI工具实战", font=subtitle_font, fill=(255, 255, 255))

    # 主标题
    title_text = f"{left_title}  vs  {right_title}"
    tb = draw.textbbox((0, 0), title_text, font=subtitle_font)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 95), title_text, font=subtitle_font, fill=(255, 255, 255))

    # 左侧卡片（红色系 - 不推荐）
    draw.rounded_rectangle([50, 160, 570, H - 50], radius=16, fill=(35, 15, 15), outline=(200, 60, 60), width=2)
    draw.rounded_rectangle([50, 160, 210, 210], radius=8, fill=(200, 50, 50))
    draw.text((125, 172), f"✗ {left_title}", font=body_font, fill=(255, 255, 255), anchor="mt")
    y = 235
    for item in left_items:
        draw.text((70, y), item, font=body_font, fill=(220, 120, 120))
        y += 52

    # 右侧卡片（绿色系 - 推荐）
    draw.rounded_rectangle([630, 160, W - 50, H - 50], radius=16, fill=(10, 35, 20), outline=(40, 200, 100), width=2)
    draw.rounded_rectangle([630, 160, 810, 210], radius=8, fill=(30, 180, 80))
    draw.text((720, 172), f"✓ {right_title}", font=body_font, fill=(255, 255, 255), anchor="mt")
    y = 235
    for item in right_items:
        draw.text((655, y), item, font=body_font, fill=(100, 220, 150))
        y += 52

    # 底部效率条
    if center_text:
        draw.rounded_rectangle([350, H - 50, 850, H - 10], radius=12, fill=(255, 180, 0))
        tb = draw.textbbox((0, 0), center_text, font=small_font)
        tw = tb[2] - tb[0]
        draw.text(((W - tw) // 2, H - 42), center_text, font=small_font, fill=(20, 10, 0), anchor="mt")

    img.save(output_path, "PNG")
    print(f"[contrast] OK: {output_path}")


def copy_to_clipboard_win(image_path):
    """将图片复制到 Windows 剪贴板"""
    ps_cmd = f'''
Add-Type -AssemblyName System.Windows.Forms
$img = [System.Drawing.Image]::FromFile("{image_path.replace("/", "\\\\")}")
[System.Windows.Forms.Clipboard]::SetImage($img)
$img.Dispose()
Write-Output "CLIPBOARD_OK"
'''
    result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    if result.returncode == 0:
        print("[clipboard] OK")
    else:
        print(f"[clipboard] ERROR: {result.stderr}")


def main():
    parser = argparse.ArgumentParser(description="微博配图生成器")
    parser.add_argument("--text", type=str, default="", help="配图主文字（部分风格支持）")
    parser.add_argument("--style", type=str, default="warmth",
                        choices=["warmth", "tech", "midnight", "contrast"],
                        help="配图风格：warmth(温暖)|tech(科技)|midnight(深夜)|contrast(对比)")
    parser.add_argument("--output", type=str, required=True, help="输出图片路径")
    parser.add_argument("--left-title", type=str, default="手动", help="对比卡左侧标题（contrast风格）")
    parser.add_argument("--right-title", type=str, default="AI工具", help="对比卡右侧标题（contrast风格）")
    parser.add_argument("--left-item", type=str, nargs="+", default=[],
                        help="对比卡左侧项目（contrast风格）")
    parser.add_argument("--right-item", type=str, nargs="+", default=[],
                        help="对比卡右侧项目（contrast风格）")
    parser.add_argument("--center-text", type=str, default="",
                        help="对比卡底部中心文字（contrast风格）")
    parser.add_argument("--copy-clipboard", action="store_true",
                        help="生成后自动复制到剪贴板")

    args = parser.parse_args()

    # 确保输出目录存在
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if args.style == "warmth":
        warmth_card(args.text, args.output)
    elif args.style == "tech":
        tech_card(args.text, args.output)
    elif args.style == "midnight":
        midnight_card(args.text, args.output)
    elif args.style == "contrast":
        left_items = args.left_item or ["整理耗时：60分钟", "反复修改：3次以上", "精神消耗：极大"]
        right_items = args.right_item or ["整理耗时：10分钟", "反复修改：1次微调", "精神消耗：极低"]
        center_text = args.center_text or "效率提升 6 倍  |  每周省下 50分钟"
        contrast_card(args.left_title, args.right_title, left_items, right_items, args.output, center_text)

    if args.copy_clipboard:
        copy_to_clipboard_win(args.output)


if __name__ == "__main__":
    main()
