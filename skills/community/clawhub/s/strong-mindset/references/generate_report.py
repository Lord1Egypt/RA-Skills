#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""强者思维评估报告 / 测评报告 → 自包含单文件 HTML 生成器（竖屏 MBTI 风）。

读取一份 JSON 规格（argv[1] 文件路径，或 stdin），写出 .html 文件（argv[2] 路径）。
无 argv[2] 时打印到 stdout。

竖屏版特征：单栏手机视图（max-width 480px，居中、可长滚），顶部居中大号分数环，
段位徽章 + 主画像句 + 定性画像标签 chips + 能力维度条 + 评语 + 最短路改进 + 免责声明。

JSON 规格：
{
  "title":     "强者思维 · 评估报告",
  "subtitle":  "STRONG-MINDSET REPORT",   # 可选
  "date":      "2026-08-01",              # 可选，默认今天
  "score":     82,                        # 总强者指数 1-100（必填）
  "tier":      "强者型",                   # 可选，缺省按分数自动推导
  "persona":   "你是「强者型」……",          # 可选，缺省自动推导主画像句
  "tags":      ["强者型","边界模糊","杠杆在手"], # 可选，缺省自动推导画像标签
  "verdict":   "整体属强者视角……",          # 一句话结论（与 persona 二选一展示，并存也行）
  "mode":      "eval",                    # "eval"(评估) | "quiz"(测评)
  "dimensions":[ {"name":"反应控制","score":90}, ... ],
  "sections":  [ {"label":"一句话定性","text":"……"}, ... ], # 评估模式诊断明细
  "improvement":"资源杠杆是最大短板……"                      # 最短路改进块
}

配色（按分数自动切换主色）：
  80-100 赤红 #A32D2D 强者型 | 60-79 暗金 #BA7517 准强者
  40-59 商务蓝 #185FA5 摇摆型 | 20-39 灰 #5F5E5A 弱者惯性 | 1-19 深灰 #444441 待觉醒
维度条：最低且 <60 的维度用暗金高亮，标「最短」提示最短板。
"""
import sys, json, datetime, math

# ---- 维度 → 画像标签映射（强者思维腔调，定性不羞辱） ----
LOW_TAG = {
    "反应控制": "反应过激",
    "利益保护": "边界模糊",
    "关系筛选": "来者不拒",
    "行动落地": "执行滞后",
    "自省深度": "省察不足",
    "表达穿透": "表达失焦",
    "资源杠杆": "杠杆闲置",
    "格局人设": "格局待开",
}
HIGH_TAG = {
    "反应控制": "情绪绝缘",
    "利益保护": "边界铁壁",
    "关系筛选": "筛人精准",
    "行动落地": "执行利落",
    "自省深度": "省察敏锐",
    "表达穿透": "表达穿透",
    "资源杠杆": "杠杆在手",
    "格局人设": "格局打开",
}
PERSONA_TAIL = {
    "强者型": "你已能在多数冲突里保持清醒，剩的是把优势规模化。",
    "准强者": "你已有强者骨架，差的是在高压下不松劲。",
    "摇摆型": "你时强时弱——问题不在能力，在一致性。",
    "弱者惯性": "你还停在「等被安排」的惯性里，先把一步迈出去。",
    "待觉醒": "你还没开始用强者视角看世界，这份报告就是起点。",
}


def color_for(score):
    if score >= 80: return "#A32D2D"
    if score >= 60: return "#BA7517"
    if score >= 40: return "#185FA5"
    if score >= 20: return "#5F5E5A"
    return "#444441"


def tier_for(score):
    if score >= 80: return "强者型"
    if score >= 60: return "准强者"
    if score >= 40: return "摇摆型"
    if score >= 20: return "弱者惯性"
    return "待觉醒"


def derive_persona(score, dims):
    """自动推导 主画像句 + 定性标签列表。

    修正：
      - 低分段（<60）最高维也不到及格线，不吹「已是武器」，改用通用段位尾句。
      - HIGH_TAG 只在最高维 >=60 时使用，否则用中性描述。
      - 最短板标签始终给，但画像句在低分时走 PERSONA_TAIL。
    """
    tier = tier_for(score)
    tags = [tier]
    persona = ""
    if dims:
        scores = [d.get("score", 0) for d in dims]
        lo = min(dims, key=lambda d: d.get("score", 0))
        hi = max(dims, key=lambda d: d.get("score", 0))
        lo_name, lo_s = lo.get("name", ""), lo.get("score", 0)
        hi_name, hi_s = hi.get("name", ""), hi.get("score", 0)
        low_tag = LOW_TAG.get(lo_name, "待补强")
        # 最高维 >=60 才配正向标签，否则用中性
        high_tag = (HIGH_TAG.get(hi_name, "已成型") if hi_s >= 60 else "相对突出")
        tags.append(low_tag)
        tags.append(high_tag)
        # 整体不及格或最高维也 <60 时，不吹武器
        if score < 60 or hi_s < 60:
            persona = "你是「" + tier + "」——" + PERSONA_TAIL.get(tier, "")
        else:
            persona = (
                "你是「" + tier + "」——" + hi_name + "（" + str(hi_s) + "）已是你的武器，"
                "但" + lo_name + "（" + str(lo_s) + "）仍拖后腿：典型的「" + low_tag + "」。"
            )
    else:
        persona = "你是「" + tier + "」——" + PERSONA_TAIL.get(tier, "")
    return persona, tags


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build(spec):
    score = int(round(spec.get("score", 0)))
    score = max(1, min(100, score))
    tier = spec.get("tier") or tier_for(score)
    color = color_for(score)
    date = spec.get("date") or datetime.date.today().isoformat()
    title = esc(spec.get("title", "强者思维 · 评估报告"))
    subtitle = esc(spec.get("subtitle", "STRONG-MINDSET REPORT"))
    verdict = esc(spec.get("verdict", ""))
    dims = spec.get("dimensions", []) or []
    sections = spec.get("sections", []) or []
    improvement = esc(spec.get("improvement", ""))
    mode = spec.get("mode", "eval")
    dim_title = "八维诊断" if mode == "eval" else "七维诊断"
    kind = "自评" if mode == "quiz" else "评估"

    persona = spec.get("persona")
    tags = spec.get("tags")
    if (not persona) or (not tags):
        dp, dt = derive_persona(score, dims)
        persona = persona or dp
        if not tags:
            tags = dt
    persona = esc(persona)
    tags = [esc(t) for t in (tags or [])]

    # 维度条
    dims_html = ""
    if dims:
        scores = [d.get("score", 0) for d in dims]
        min_score = min(scores) if scores else 0
        # 只标记第一个出现的最低维为「最短」，避免并列时重复标记
        marked_low = False
        for d in dims:
            name = esc(d.get("name", ""))
            ds = int(round(d.get("score", 0)))
            ds = max(0, min(100, ds))
            is_low = (ds == min_score and ds < 60 and not marked_low)
            if is_low:
                marked_low = True
            # 最短板用暗金；当主色恰好也是暗金（准强者档）时改用深红区分
            bar_color = "#BA7517" if is_low else color
            if is_low and color == "#BA7517":
                bar_color = "#A32D2D"
            marker = ' <span class="mini">最短</span>' if is_low else ""
            dims_html += (
                '<div class="dim">'
                '<div class="dim-head"><span>' + name + marker + '</span>'
                '<span class="dim-val" style="color:' + (bar_color if is_low else "#222") + ';">' + str(ds) + '</span></div>'
                '<div class="bar"><div class="bar-fill" style="width:' + str(ds) + '%;background:' + bar_color + ';"></div></div>'
                '</div>'
            )

    # 评语块
    comments_html = ""
    if mode == "eval":
        for s in sections:
            label = esc(s.get("label", ""))
            text = esc(s.get("text", ""))
            if not text:
                continue
            comments_html += (
                '<div class="blk">'
                '<p class="blk-label">' + label + '</p>'
                '<p class="blk-text">' + text + '</p>'
                '</div>'
            )
    else:
        if verdict:
            comments_html += (
                '<div class="blk"><p class="blk-label">总评</p>'
                '<p class="blk-text">' + verdict + '</p></div>'
            )

    improve_html = ""
    if improvement:
        improve_html = (
            '<div class="improve">'
            '<p class="improve-label">最短路改进</p>'
            '<p class="improve-text">' + improvement + '</p>'
            '</div>'
        )

    # 分数环
    r = 58
    C = 2 * math.pi * r
    dash = C * score / 100.0

    tags_html = "".join(
        '<span class="tag' + (' tag-main' if i == 0 else '') + '">' + t + '</span>'
        for i, t in enumerate(tags)
    )

    html = (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + title + '</title>\n<style>\n'
        '* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }\n'
        'body { margin:0; background: linear-gradient(160deg,#ECECEC,#F6F6F6); '
        'font-family:"Microsoft YaHei","PingFang SC",sans-serif; color:#222; padding:18px 12px 36px; }\n'
        '.card { max-width:460px; margin:0 auto; background:#fff; border-radius:20px; '
        'padding:22px 20px 24px; box-shadow:0 6px 24px rgba(0,0,0,.08); }\n'
        '.brand { font-size:11px; letter-spacing:3px; color:#aaa; margin:0; }\n'
        '.title { font-size:20px; margin:4px 0 0; color:#1a1a1a; font-weight:700; }\n'
        '.topbar { display:flex; justify-content:space-between; align-items:flex-start; '
        'border-bottom:2px solid ' + color + '; padding-bottom:12px; }\n'
        '.date { font-size:11px; color:#bbb; margin-top:6px; }\n'
        '.hero { display:flex; flex-direction:column; align-items:center; margin:22px 0 6px; }\n'
        '.ring-wrap { position:relative; width:148px; height:148px; }\n'
        '.ring-center { position:absolute; top:0; left:0; width:148px; height:148px; '
        'display:flex; flex-direction:column; align-items:center; justify-content:center; }\n'
        '.score-num { font-size:46px; font-weight:800; color:' + color + '; line-height:1; }\n'
        '.score-cap { font-size:12px; color:#999; margin-top:4px; letter-spacing:1px; }\n'
        '.badge { display:inline-block; margin-top:12px; padding:5px 16px; background:' + color + '; '
        'color:#fff; font-size:14px; font-weight:600; border-radius:20px; letter-spacing:1px; }\n'
        '.persona { font-size:13.5px; color:#444; line-height:1.75; margin:14px 4px 0; text-align:center; }\n'
        '.tags { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin:16px 0 4px; }\n'
        '.tag { font-size:12px; padding:5px 12px; background:#F1F1F1; color:#666; border-radius:16px; }\n'
        '.tag-main { background:' + color + '; color:#fff; font-weight:600; }\n'
        '.mini { font-size:10px; background:#BA7517; color:#fff; padding:1px 5px; border-radius:8px; margin-left:4px; vertical-align:middle; }\n'
        '.sec-title { font-size:14px; font-weight:600; margin:24px 0 10px; color:#222; '
        'padding-left:10px; border-left:4px solid ' + color + '; }\n'
        '.dim { margin:11px 0; }\n'
        '.dim-head { display:flex; justify-content:space-between; font-size:13px; color:#444; margin-bottom:5px; }\n'
        '.dim-val { font-weight:700; }\n'
        '.bar { height:9px; background:#EEE; border-radius:6px; overflow:hidden; }\n'
        '.bar-fill { height:9px; border-radius:6px; }\n'
        '.blk { margin-top:14px; padding:13px 14px; background:#F8F8F8; border-radius:12px; '
        'border-left:3px solid ' + color + '; }\n'
        '.blk-label { font-size:13px; font-weight:600; margin:0 0 5px; color:' + color + '; }\n'
        '.blk-text { font-size:13px; color:#555; margin:0; line-height:1.75; }\n'
        '.improve { margin-top:18px; padding:14px; background:#FBF3E6; border-radius:12px; }\n'
        '.improve-label { font-size:13px; font-weight:600; margin:0 0 5px; color:#8a5a12; }\n'
        '.improve-text { font-size:13px; color:#555; margin:0; line-height:1.75; }\n'
        '.foot { margin-top:22px; padding-top:14px; border-top:1px solid #eee; '
        'font-size:11px; color:#bbb; line-height:1.65; }\n'
        '</style>\n</head>\n<body>\n<div class="card">\n'
        '  <div class="topbar">\n'
        '    <div><p class="brand">' + subtitle + '</p><h1 class="title">' + title + '</h1></div>\n'
        '    <span class="date">' + date + '</span>\n'
        '  </div>\n'
        '  <div class="hero">\n'
        '    <div class="ring-wrap">\n'
        '      <svg width="148" height="148" viewBox="0 0 148 148" role="img" aria-label="强者指数 ' + str(score) + ' 分">\n'
        '        <circle cx="74" cy="74" r="58" fill="none" stroke="#EEE" stroke-width="12"></circle>\n'
        '        <circle cx="74" cy="74" r="58" fill="none" stroke="' + color + '" stroke-width="12" stroke-linecap="round" '
        'stroke-dasharray="' + ("%.1f" % dash) + ' ' + ("%.1f" % C) + '" transform="rotate(-90 74 74)"></circle>\n'
        '      </svg>\n'
        '      <div class="ring-center"><span class="score-num">' + str(score) + '</span>'
        '<span class="score-cap">强者指数</span></div>\n'
        '    </div>\n'
        '    <span class="badge">段位 · ' + tier + '</span>\n'
        '    <p class="persona">' + persona + '</p>\n'
        '  </div>\n'
        '  <div class="tags">' + tags_html + '</div>\n'
    )
    if dims_html:
        html += '  <p class="sec-title">' + dim_title + '</p>\n' + dims_html + '\n'
    if comments_html:
        html += '  <p class="sec-title">评语</p>\n' + comments_html + '\n'
    if improve_html:
        html += improve_html + '\n'
    html += (
        '  <div class="foot">本报告基于「强者思维」框架的经验性' + kind + '，用于自我觉察与内容创作参考，'
        '并非心理测量学工具，不构成任何专业建议。</div>\n'
        '</div>\n</body>\n</html>\n'
    )
    return html


def main():
    data = None
    if len(sys.argv) > 1 and sys.argv[1] != "--out":
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    out = None
    if len(sys.argv) > 2:
        out = sys.argv[2]
    elif "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    html = build(data)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("OK " + out + " (" + str(len(html)) + " bytes)")
    else:
        sys.stdout.write(html)


if __name__ == "__main__":
    main()
