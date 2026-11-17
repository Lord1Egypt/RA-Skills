# -*- coding: utf-8 -*-
"""NG 杂志竖版笔记 · 生成器骨架模板 (v2.6)

★ 为什么用 Python 生成器而不是手写 HTML：
  60 页 × 平均 8KB/页 ≈ 500KB HTML，直接 Write 会被单文件 token 上限截断。
  拆成 3~6 个生成器片段（每个 ≤20KB），各产出 _mag_xx.html，由 build 流水线合并。

★ 拆分模式（实测 60 页项目）：
  gen_mag_a1.py → P01–P13（前置+PART I）    gen_mag_a2.py → P14–P23（PART II）
  gen_mag_b1.py → P24–P32（PART III）        gen_mag_b2.py → P33–P41（PART IV）
  gen_mag_c1.py → P42–P50（PART V 前半）     gen_mag_c2.py → P51–P60（PART V 后半+收尾）
  每片 9~10 页 ≈ 18KB，安全上限 20KB；单片超 20KB 再对半拆。

★ 三函数模板 + pages.append 模式（复制到每个生成器顶部，只改 BRAND）：
"""
# ── 头部（每个生成器相同）──────────────────────────────
BRAND = 'READING NOTES · 书名拼音或英文'   # 眉区左侧刊名，全大写
P = []                                     # 页面缓冲

def HD(sec, page):
    """页眉：刊名 | PART 0X · 章名 | P01"""
    return ('<header class="hd"><span class="hl-brand">' + BRAND + '</span>'
            '<span class="hl-sec">' + sec + '</span>'
            '<span class="hl-brand" style="letter-spacing:.10em">P' + f"{page:02d}" + '</span></header>')

def FT(page):
    """页脚：黑条 + 黄星 + 页码"""
    return ('<footer class="ft"><span class="star">★</span>'
            '<span class="fp">' + f"{page:02d}" + '</span></footer>')

def FOLIO(page):
    """金句页/满版页的浅色页码（无黑条时用）"""
    return '<div class="folio">' + f"{page:02d}" + '</div>'

# ── 页面写法（普通内容页骨架）──────────────────────────
P.append(
    HD('PART 01 · 猫科猛兽', 6) + FT(6) +
    '<section class="page">'
    '<div class="bd">'
    '<div class="kicker">01 · 章内小节号</div>'
    '<h2 class="art-title yl">文章标题<span class="yl">（黄底下划词）</span></h2>'
    '<p class="deck">导语 1~2 句，18px 斜体感，界定本页讨论范围。</p>'
    '…… 器型区（statgrid / entrygrid / anat / chartbox / tl / pricerow …）……'
    '<div class="note">注：数据出处或补充说明。</div>'
    '</div></section>'
)
# 注意：HD/FT 在 section 外面（.hd 是 absolute 定位到页面顶部），
#       section 内只放 .bd。满版页/金句页不用 .bd，见手册 §4。

# ── 尾部（每个生成器相同）──────────────────────────────
from pathlib import Path
out = Path(__file__).resolve().parent / '_mag_c1.html'   # 改成自己的片段名
out.write_text('\n'.join(P), encoding='utf-8')
print('c1 ok', len(P))    # 运行后核对页数
