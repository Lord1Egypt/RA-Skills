#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HBR 商业杂志横版生成器骨架（reading-notes-master v2.7 · templates/hbr-magazine/）

从 88 页《哈佛商业评论 2025 年度精选》实战引擎沉淀（engine_mag.py 276 行）。
页面节奏（每章 11 页固定，实测零溢出）：
    章隔页 → 编辑开篇 → 大图表 → 巨型统计 → 文本×3 → 照片特写 → 金句 → 编辑(翻面) → 文本
全书结构：前置(封面+目录×2+总览+口径+金句+金句墙) + 7章×11 + 后置附录 = 88 页
成品页数 = 原书 1/3~1/2（单期均页口径，见 references/hbr-magazine-layout.md §5）。

拆分硬纪律（防 Write 截断）：
  88 页 ≈ 106KB HTML → 拆 6~8 个生成器，每片 9~13 页、≤20KB；
  每片 = CONFIG + 本骨架同款函数头 + P=[] + N 个 P.append(...) + 尾部合并写出。
  用系统 python3 跑生成器（纯标准库）；build 才用带 Chrome 的环境。

资产目录约定（相对生成器所在目录）：
  ../assets/mag/     照片/图表位图（jpg，长边 ≤1700px，q76 预压缩）
  ../assets/scrim/   遮罩 PNG（4 个，由 scrim/make_scrims.py 生成）
改路径只改 CONFIG 的 PH/COV 两个函数。
"""
import html as H
import os

# ============================================================ CONFIG（每项目改这里）
BOOK_CN = "哈佛商业评论"          # 刊名（封面/目录/folio）
BOOK_EN = "HARVARD BUSINESS REVIEW"
EDITION = "2025 年度精选版"        # 年份徽章文字
FOLIO_R = "BEST OF 2025"          # 页眉右标
ASSET = os.path.join("..", "assets", "mag")      # 照片/图表资产目录
COVER_ASSET = os.path.join("..", "assets", "mag")  # 封面/期号资产目录


def ph(name):
    """照片/图表资产 → url() 相对路径（jpg）"""
    return ASSET + "/" + name + ".jpg"


def cov(name):
    """封面/期号资产 → url() 相对路径（jpg）"""
    return COVER_ASSET + "/" + name + ".jpg"


def scrim(kind):
    """遮罩 PNG → url() 相对路径（kind: mc/md/mp/mq）"""
    return "../assets/scrim/scrim_%s.png" % kind


# ============================================================ 基础件
def esc(s):
    return H.escape(str(s), quote=False)


def t(s):
    """标题换行：\\n → <br/>"""
    return str(s).replace("\n", "<br/>")


def folio(left, right=FOLIO_R):
    """页眉（绝对定位，在 .page 内）"""
    return '<div class="folio"><span>%s</span><span>%s</span></div>' % (left, right)


def pageno(no, section=""):
    """页脚页码 + 章节名（绝对定位，在 .page 内）"""
    return '<div class="pageno"><b>%s</b><i>%s</i></div>' % (no, section)


# ============================================================ ① 封面：全出血 + 刊名 + 封面条
def mag_cover(bg, title, deck, photos, kicker="BEST OF HBR · 2025", year_bar=None, foot_r="全年 12 期 · 88 页"):
    strip = "".join(
        '<div class="mc-cell" style="background-image:url(%s)"></div>' % cov(p) for p in photos
    )
    return '''<div class="page fullbleed mag-cover" style="background-image:url(%s)">
  <div class="mc-scrim"></div>
  <div class="mc-mast">
    <div class="mc-mast-l">%s</div>
    <div class="mc-mast-r">%s<br/>BUSINESS<br/>REVIEW</div>
  </div>
  <div class="mc-year">%s</div>
  <h1 class="mc-title">%s</h1>
  <div class="mc-rule"></div>
  <p class="mc-deck">%s</p>
  <div class="mc-strip">%s</div>
  <div class="mc-foot"><span>%s</span><span>%s</span></div>
</div>''' % (ph(bg), BOOK_CN, BOOK_EN, year_bar or (EDITION + " · BEST OF"), t(title), deck, strip, kicker, foot_r)


# ============================================================ ② 章隔页：全出血 + 150pt 巨号
def mag_divider(num_cn, num_en, title_cn, title_en, photo, caption, tag="CHAPTER"):
    return '''<div class="page fullbleed mag-div" style="background-image:url(%s)">
  <div class="md-scrim"></div>
  <div class="md-top">
    <span class="md-tag">%s</span>
    <span class="md-num">%s</span>
  </div>
  <div class="md-vert">%s</div>
  <div class="md-bottom">
    <h1 class="md-title">%s</h1>
    <div class="md-sub">%s</div>
    <div class="md-cap">%s</div>
  </div>
</div>''' % (ph(photo), tag, num_cn, num_en, title_cn, title_en, caption)


# ============================================================ ③ 编辑开篇：非对称图文（图 310pt + 文）
def mag_editorial(no, kicker, title, deck, body_html, photo, section,
                  side="left", stat=None, photo_cap=""):
    """side: left=图在左（默认）/ right=图在右（me-flip，每章第二篇用翻面）"""
    stat_html = ""
    if stat:
        stat_html = '<div class="me-stat"><b>%s</b><span>%s</span></div>' % (stat[0], stat[1])
    cls = "mag-ed" + (" me-flip" if side == "right" else "")
    return '''<div class="page %s">
  <div class="me-photo" style="background-image:url(%s)">
    <span class="me-pcap">%s</span>
  </div>
  <div class="me-body">
    <div class="me-kick">%s</div>
    <h1 class="me-title">%s</h1>
    <p class="me-deck">%s</p>
    %s
    <div class="me-text">%s</div>
  </div>
  %s
</div>''' % (cls, ph(photo), photo_cap, kicker, t(title), deck, stat_html, body_html,
            pageno(no, section))


# ============================================================ ④ 整页大图表（原刊图表全宽呈现）
def mag_chart(no, kicker, title, sub, chart_photo, insight, source, section, note=""):
    note_html = '<div class="mc-note">%s</div>' % note if note else ""
    return '''<div class="page mag-chart">
  <div class="mch-head">
    <div class="mch-kick">%s</div>
    <h1 class="mch-title">%s</h1>
    <div class="mch-sub">%s</div>
  </div>
  <div class="mch-stage" style="background-image:url(%s)"></div>
  <div class="mch-foot">
    <div class="mch-insight"><b>解读</b>%s</div>
    %s
    <div class="mch-src">资料来源：%s</div>
  </div>
  %s
</div>''' % (kicker, t(title), sub, ph(chart_photo), insight, note_html, source, pageno(no, section))


# ============================================================ ④b 整页大图表（SVG 重绘版）
def mag_chart_svg(no, kicker, title, sub, chart_svg, insight, source, section, note=""):
    note_html = '<div class="mc-note">%s</div>' % note if note else ""
    return '''<div class="page mag-chart">
  <div class="mch-head">
    <div class="mch-kick">%s</div>
    <h1 class="mch-title">%s</h1>
    <div class="mch-sub">%s</div>
  </div>
  <div class="mch-svgstage">%s</div>
  <div class="mch-foot">
    <div class="mch-insight"><b>解读</b>%s</div>
    %s
    <div class="mch-src">资料来源：%s</div>
  </div>
  %s
</div>''' % (kicker, t(title), sub, chart_svg, insight, note_html, source, pageno(no, section))


# ============================================================ ⑤ 巨型统计页：100pt 数字
def mag_stat(no, kicker, num, unit, desc, title, body_html, photo, section):
    return '''<div class="page mag-stat">
  <div class="ms-photo" style="background-image:url(%s)"></div>
  <div class="ms-body">
    <div class="ms-kick">%s</div>
    <div class="ms-num">%s<i>%s</i></div>
    <div class="ms-desc">%s</div>
    <div class="ms-rule"></div>
    <h2 class="ms-title">%s</h2>
    <div class="ms-text">%s</div>
  </div>
  %s
</div>''' % (ph(photo), kicker, num, unit, desc, t(title), body_html, pageno(no, section))


# ============================================================ ⑥ 大字文本页：双栏极简
def mag_text(no, kicker, title, body_html, section, lead=None):
    lead_html = '<p class="mt-lead">%s</p>' % lead if lead else ""
    return '''<div class="page mag-text">
  <div class="mt-kick">%s</div>
  <h1 class="mt-title">%s</h1>
  %s
  <div class="mt-text">%s</div>
  %s
</div>''' % (kicker, t(title), lead_html, body_html, pageno(no, section))


# ============================================================ ⑦ 照片特写页：全出血 + 小注
def mag_photo(no, photo, caption, kicker, section):
    return '''<div class="page fullbleed mag-photo" style="background-image:url(%s)">
  <div class="mp-scrim"></div>
  <div class="mp-cap">
    <span class="mp-kick">%s</span>
    <span class="mp-txt">%s</span>
  </div>
  %s
</div>''' % (ph(photo), kicker, caption, pageno(no, section))


# ============================================================ ⑧ 金句页：全出血 + 居中金句
def mag_quote(no, quote, src, note, photo):
    return '''<div class="page fullbleed mag-quote" style="background-image:url(%s)">
  <div class="mq-scrim"></div>
  <div class="mq-inner">
    <div class="mq-mark">"</div>
    <div class="mq-quote">%s</div>
    <div class="mq-src">%s</div>
    <div class="mq-note">%s</div>
  </div>
</div>''' % (ph(photo), t(quote), src, note)


# ============================================================ ⑨ 目录：分组细线（双栏平衡由 build 处理）
def mag_toc(no, sections, cont=False):
    """sections: [(组名, [(标题, 作者/出处, 页码), ...]), ...]"""
    rows = ""
    for sec, items in sections:
        rows += '<div class="toc-sec"><div class="toc-sec-t">%s</div>' % sec
        for title, au, pg in items:
            rows += ('<div class="toc-row"><span class="toc-dot"></span>'
                     '<span class="toc-t">%s</span><span class="toc-au">%s</span>'
                     '<span class="toc-pg">%s</span></div>') % (title, au, pg)
        rows += "</div>"
    head = "目录 · CONTENTS" + ("（续）" if cont else "")
    return '''<div class="page mag-toc">
  <div class="toc-head"><span>%s</span><span>BEST OF %s</span></div>
  <div class="toc-body">%s</div>
  %s
</div>''' % (head, BOOK_EN.split()[0], rows, pageno(no, "目录"))


# ============================================================ ⑩ 期号总览：4×3 卡片网格
def mag_issuemap(no, title, sub, issues):
    """issues: [(期号, 主题, 描述, 标签, hot_bool, 封面图), ...]  ≤12 张"""
    cards = ""
    for lab, theme, desc, tags, hot, img in issues:
        hot_html = '<span class="im-hot">HOT</span>' if hot else ""
        cards += '''<div class="im-card">
          <div class="im-img" style="background-image:url(%s)"></div>
          <div class="im-lab">%s%s</div>
          <div class="im-theme">%s</div>
          <div class="im-desc">%s</div>
          <div class="im-tags">%s</div>
        </div>''' % (cov(img), lab, hot_html, theme, desc, tags)
    return '''<div class="page mag-imap">
  <div class="im-head"><div class="im-kick">THE YEAR AT A GLANCE</div>
    <h1 class="im-title">%s</h1>
    <div class="im-sub">%s</div>
  </div>
  <div class="im-grid">%s</div>
  %s
</div>''' % (title, sub, cards, pageno(no, "特辑"))


# ============================================================ SVG 大图表组件（杂志式细线）
def svg_bigbar(rows, w=560, h=None, hi_idx=(0,), lab_w=170, note_w=110,
               color="#C9C5BE", hi="#E41824"):
    """rows: [(label, value, note)] 大横幅条形图；hi_idx 高亮行（刊名红）"""
    n = len(rows)
    rh = 34
    h = h or n * rh + 10
    mx = max(v for _, v, _ in rows) * 1.02
    parts = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (w, h)]
    for i, (lb, v, note) in enumerate(rows):
        y = i * rh + 6
        bw = (v / mx) * (w - lab_w - note_w)
        c = hi if i in hi_idx else color
        parts.append('<text x="0" y="%d" font-size="10" fill="#231F20">%s</text>' % (y + 16, esc(lb)))
        parts.append('<rect x="%d" y="%d" width="%.1f" height="20" fill="%s"/>' % (lab_w, y, bw, c))
        parts.append('<text x="%.1f" y="%d" font-size="11" font-weight="700" fill="#231F20">%s</text>'
                     % (lab_w + bw + 8, y + 15, v))
        if note:
            parts.append('<text x="%d" y="%d" font-size="8" text-anchor="end" fill="#8A8580">%s</text>'
                         % (w, y + 15, esc(note)))
    parts.append("</svg>")
    return "".join(parts)


def svg_bigstat_ring(pct, w=200, h=200, color="#E41824", track="#E8E4DC", label=""):
    """巨型圆环进度图"""
    import math
    r = 78
    cx = cy = w / 2
    circ = 2 * math.pi * r
    off = circ * (1 - pct / 100)
    parts = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (w, h)]
    parts.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="16"/>' % (cx, cy, r, track))
    parts.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="16"'
                 ' stroke-dasharray="%.1f" stroke-dashoffset="%.1f"'
                 ' transform="rotate(-90 %d %d)" stroke-linecap="round"/>'
                 % (cx, cy, r, color, circ, off, cx, cy))
    parts.append('<text x="%d" y="%d" font-size="34" font-weight="800" text-anchor="middle" fill="#231F20">%d%%</text>'
                 % (cx, cy + 8, pct))
    if label:
        parts.append('<text x="%d" y="%d" font-size="9" text-anchor="middle" fill="#8A8580">%s</text>'
                     % (cx, cy + 30, esc(label)))
    parts.append("</svg>")
    return "".join(parts)


def svg_steps_big(items, w=560, h=210, dark=False):
    """items: [(num, title, desc)] 大版步骤带；desc >22 字截断"""
    n = len(items)
    bg = "#17141A" if dark else "#F4F1EA"
    ln = "#3A3640" if dark else "#D8D4CC"
    tx = "#F4F1EA" if dark else "#231F20"
    parts = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (w, h)]
    parts.append('<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg))
    cw = (w - 24) / n
    parts.append('<line x1="12" y1="52" x2="%d" y2="52" stroke="%s" stroke-width="1"/>' % (w - 12, ln))
    for i, (num, title, desc) in enumerate(items):
        cx = 12 + cw * i + cw / 2
        c = "#F37060" if i % 2 == 0 else "#F09C18"
        parts.append('<circle cx="%.0f" cy="52" r="17" fill="%s"/>' % (cx, c))
        parts.append('<text x="%.0f" y="57" font-size="12" font-weight="800" fill="#fff" text-anchor="middle">%s</text>'
                     % (cx, num))
        parts.append('<text x="%.0f" y="92" font-size="9.5" font-weight="700" fill="%s" text-anchor="middle">%s</text>'
                     % (cx, tx, esc(title)))
        d = esc(desc)
        if len(d) > 11:
            parts.append('<text x="%.0f" y="108" font-size="7.5" fill="#8A8580" text-anchor="middle">%s</text>' % (cx, d[:11]))
            parts.append('<text x="%.0f" y="120" font-size="7.5" fill="#8A8580" text-anchor="middle">%s</text>' % (cx, d[11:22]))
        else:
            parts.append('<text x="%.0f" y="108" font-size="7.5" fill="#8A8580" text-anchor="middle">%s</text>' % (cx, d))
    parts.append("</svg>")
    return "".join(parts)


# ============================================================ 主生产（示例：每片复制本骨架改中段）
# 页面地图先行：每片动笔前在注释里写下页码范围与页型序列，例如：
#   P01–P13  前置 5 + PART I（章隔+编辑+图表+统计+文本×3+照片+金句+编辑翻面+文本）
P = []

# ---- 示例页（删掉，换成你的页面地图）----
P.append(mag_cover(
    bg="cover_bg",
    title="低增长时代的\n确定性经营",
    deck="从 12 期原刊凝练的经营智慧：战略减法、分布式组织、董事会 AI 与数据变现。",
    photos=["cov_01", "cov_02", "cov_03", "cov_04", "cov_05", "cov_06"],
))
P.append(mag_divider("01", "CHAPTER ONE", "战略与竞争", "STRATEGY & COMPETITION",
                     photo="divider_bg", caption="增长不再是唯一的叙事。"))
P.append(mag_editorial(9, "封面特写 · THE BIG IDEA", "增长不是创造价值的\n唯一方式",
                       "172 家零增长稳定企业给出另一种答案。",
                       "<p>乌尔里希·皮登团队研究逾 1 万家公司 20 年表现……</p>",
                       photo="ed_bg", section="战略与竞争", stat=("172", "家 · 零增长却跑赢的稳定企业"),
                       photo_cap="平衡的艺术：零增长企业的资产配置"))
P.append(mag_stat(11, "数字 · BY THE NUMBERS", "12", "%", "严重市值崩盘概率，仅为平均公司的一半",
                  "稳定企业：把韧性当作\n估值资产来经营",
                  "<p>四种零增长价值策略中，类债券分红策略以极低股息波动率换取稳定溢价……</p>",
                  photo="stat_bg", section="战略与竞争"))
P.append(mag_chart(10, "大图表 · THE MODEL", "营业收入公式：\n乘法思维取代加法思维",
                   "原刊把营收拆为乘法的结构指标。",
                   chart_photo="chart_formula", insight="每一层都有负责人与可下钻的动作方案。",
                   source="中文版第 5 期", section="战略与竞争"))
P.append(mag_photo(15, "photo_bg", "张文中“物美管理学”的战略五要素。", "特写 · 中文版第 1 期", "战略与竞争"))
P.append(mag_quote(16, "约束本身就是创新的催化剂。", "《增长不是创造价值的唯一方式》· 英 11-12 月刊",
                   "172 家稳定企业证明：不扩张规模也能创造价值。", "quote_bg"))

OUT = "_mag.html"
if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(P))
    print("written %s: %d pages, %.1f KB" % (OUT, len(P), os.path.getsize(OUT) / 1024))
