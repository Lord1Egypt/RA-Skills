#!/usr/bin/env python3
"""
styling-studio 素材总览生成器（全量视图 · 图片占位）

数据源：references/styling-studio-requirements.md
  - 素材库 12 表全量条目 + 诊断色卡 → 全量卡片（编号全程连续）
  - 有 SVG 的条目：图卡（缩略图 + 金色编号 + 载体标签）
  - 无 SVG 的条目：图片占位卡（占位图形 + 灰色编号 + 载体标签——写实类运行时可生图）
  - 库外细分条目（如 T-01b）自动插到其基码条目之后
SVG 内容：从 references/svg-bundle-*.md（平铺于 references/ 根层）按 seed 注释提取，内联进卡片（总览仍为单文件自包含）

输出：references/styling-studio-gallery.html（大区 → 品类小区 → 卡片网格，含搜索）

用法：
    python scripts/styling-studio-build-gallery.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ = ROOT / 'references' / 'styling-studio-requirements.md'
OUT = ROOT / 'references' / 'styling-studio-gallery.html'

text = REQ.read_text(encoding='utf-8')

# ---------- 1) 素材库全量条目 ----------
lib = text.split('【美甲素材库')[1].split('【预置 SVG 素材清单')[0]
CATS = [
    ('美甲', 'N', '图案款式组'), ('美睫', 'E', '图案款式组'), ('美发', 'H', '图案款式组'), ('纹身', 'T', '图案款式组'),
    ('舞蹈', 'D', '姿态组'), ('瑜伽', 'Y', '姿态组'),
    ('美容', 'S', '流程样式组'), ('祛痘', 'A', '流程样式组'), ('纤体', 'B', '流程样式组'),
    ('服装', 'O', '穿搭造型组'), ('饰品', 'J', '穿搭造型组'), ('妆容', 'M', '穿搭造型组'),
]
items_by_cat = {c: [] for c, _, _ in CATS}
for line in lib.splitlines():
    m = re.match(r'^\|\s*([NEHDTYSABOJM])-(\d+[a-z]?)\s*\|(.+)$', line)
    if not m:
        continue
    letter, num, rest = m.group(1), m.group(2), m.group(3)
    cat = next((c for c, p, _ in CATS if p == letter), None)
    if not cat:
        continue
    parts = [p.strip() for p in rest.strip().strip('|').split('|')]
    name = parts[0]
    carrier = None
    for p in parts[1:4]:
        if p in ('提示词', 'SVG', '双', '文本'):
            carrier = p
            break
    items_by_cat[cat].append((f'{letter}-{num}', name, carrier))

# ---------- 2) SVG 映射（条目 → 文件 / 名称），含色卡 ----------
seg = text.split('**【预置 SVG 素材清单')[1].split('**素材使用说明**')[0]
svg_meta, palette, looks = {}, [], []
for line in seg.splitlines():
    s = line.strip()
    if not s.startswith('| SS-'):
        continue
    cols = [c.strip() for c in s.strip('|').split('|')]
    fn, code, name = cols[0], cols[1], cols[2]
    if fn.startswith('SS-look-'):
        looks.append((code, name, fn))
    elif code.startswith('P-'):
        palette.append((code, name, fn))
    else:
        svg_meta[code] = (fn, name)

total_items = sum(len(v) for v in items_by_cat.values())
svg_total = len(svg_meta) + len(palette) + len(looks)

# ---------- 2b) 从品类打包文件（.md）载入种子 SVG 内容 ----------
seed_svg = {}
for bundle in sorted((ROOT / 'references').glob('svg-bundle-*.md')):
    btext = bundle.read_text(encoding='utf-8')
    for m in re.finditer(r'<!--\s*seed:\s*(\S+?)\s*[｜|][^\n]*?-->\s*(<svg[\s\S]*?</svg>)', btext):
        seed_svg[m.group(1)] = m.group(2)

# ---------- 3) 构造各品类展示序列（含库外细分条目插入） ----------
display_by_cat = {}
for cat, letter, _ in CATS:
    entries = items_by_cat[cat]
    lib_codes = {code for code, _, _ in entries}
    extras = {}
    for code, (fn, name) in svg_meta.items():
        if code.startswith(letter + '-') and code not in lib_codes:
            base = re.match(rf'{letter}-(\d+)', code)
            if base:
                base_code = f'{letter}-{int(base.group(1)):02d}'
                extras.setdefault(base_code, []).append((code, name, fn))
    seq = []
    for code, name, carrier in entries:
        seq.append({'code': code, 'name': name, 'carrier': carrier, 'svg': svg_meta.get(code)})
        for e_code, e_name, e_fn in extras.pop(code, []):
            seq.append({'code': e_code, 'name': e_name, 'carrier': 'SVG', 'svg': (e_fn, e_name)})
    for rest in extras.values():
        for e_code, e_name, e_fn in rest:
            seq.append({'code': e_code, 'name': e_name, 'carrier': 'SVG', 'svg': (e_fn, e_name)})
    seq.sort(key=lambda it: (int(re.match(r'[A-Z]-(\d+)', it['code']).group(1)), it['code']))
    display_by_cat[cat] = seq

# ---------- 4) 生成 HTML ----------
GROUP_ORDER = ['图案款式组', '姿态组', '流程样式组', '穿搭造型组', '场景组合组', '诊断配套']

PH_ICON = ('<svg class="phicon" viewBox="0 0 100 80" aria-hidden="true">'
           '<rect x="12" y="12" width="76" height="56" rx="7"/>'
           '<circle cx="34" cy="34" r="7"/>'
           '<path d="M16 62 L42 42 L58 56 L72 44 L84 58"/></svg>')


def figure_card(idx, code, name, fn, carrier):
    tag = carrier or 'SVG'
    svg = seed_svg.get(fn) or PH_ICON
    return (
        f'<div class="card" data-k="{html.escape(f"{code} {name} {tag} {fn}")}">'
        f'<span class="no">{idx:02d}</span><span class="tag">{html.escape(tag)}</span>'
        f'<div class="thumb">{svg}</div>'
        f'<div class="meta"><b>{html.escape(code)}</b>{html.escape(name)}</div>'
        f'</div>'
    )


def placeholder_card(code, name):
    return (
        f'<div class="card dim" data-k="{html.escape(f"{code} {name} 知识")}">'
        f'<span class="tag tag-dim">知识</span>'
        f'<div class="thumb ph">{PH_ICON}</div>'
        f'<div class="meta"><b>{html.escape(code)}</b>{html.escape(name)}</div>'
        f'</div>'
    )


idx = 0
blocks = []
for group in GROUP_ORDER:
    cats_in = [(c, l) for c, l, g in CATS if g == group]
    body = []
    g_start = idx + 1
    g_items = g_svg = 0
    if group == '场景组合组':
        blocks.append('<section class="group">')
        blocks.append(f'<h2>{group}<span class="count">{len(looks)} 个（{idx + 1:02d} ~ {idx + len(looks):02d}）</span></h2>')
        blocks.append('<section class="subgroup">')
        blocks.append(f'<h3>组合卡<span class="count">{idx + 1:02d} ~ {idx + len(looks):02d} ・ {len(looks)} 个</span></h3>')
        blocks.append('<div class="grid">')
        for code, name, fn in looks:
            idx += 1
            blocks.append(figure_card(idx, code, name, fn, '组合'))
        blocks.append('</div></section></section>')
        continue

    if group == '诊断配套':
        for code, name, fn in palette:
            idx += 1
            body.append(figure_card(idx, code, name, fn, 'SVG'))
        g_items = len(palette); g_svg = len(palette)
        blocks.append('<section class="group">')
        blocks.append(f'<h2>{group}<span class="count">{g_items} 条 · SVG {g_svg} ｜ {g_start:02d} ~ {idx:02d}</span></h2>')
        blocks.append('<section class="subgroup">')
        blocks.append(f'<h3>诊断底座<span class="count">{g_start:02d} ~ {idx:02d} ・ {g_items} 条 ・ SVG {g_svg}</span></h3>')
        blocks.append('<div class="grid">')
        blocks.extend(body)
        blocks.append('</div></section></section>')
        continue

    for cat, letter in cats_in:
        seq = display_by_cat[cat]
        c_start = idx + 1
        cards = []
        n_fig = n_know = 0
        for it in seq:
            if it['svg']:
                idx += 1
                cards.append(figure_card(idx, it['code'], it['name'], it['svg'][0], it['carrier']))
                n_fig += 1
            else:
                cards.append(placeholder_card(it['code'], it['name']))
                n_know += 1
        body.append('<section class="subgroup">')
        know_txt = f' ・ 知识 {n_know}' if n_know else ''
        body.append(f'<h3>{cat}<span class="count">{c_start:02d} ~ {idx:02d} ・ 图 {n_fig}{know_txt}</span></h3>')
        body.append('<div class="grid">')
        body.extend(cards)
        body.append('</div></section>')
        g_items += n_fig; g_svg += n_fig
    blocks.append('<section class="group">')
    blocks.append(f'<h2>{group}<span class="count">{g_items} 个（{g_start:02d} ~ {idx:02d}）</span></h2>')
    blocks.extend(body)
    blocks.append('</section>')

total_cards = idx

doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>素材总览 · styling-studio（全量 {total_cards} 条 / SVG {svg_total} 个）</title>
<style>
  :root {{ --bg:#FAF7F2; --card:#FFFFFF; --line:#EADFD3; --ink:#3A3A3A; --sub:#8A7868; --accent:#B8935A; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:14px/1.6 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }}
  header {{ position:sticky; top:0; z-index:2; backdrop-filter:blur(8px); background:rgba(250,247,242,.92); border-bottom:1px solid var(--line); padding:12px 22px; display:flex; gap:14px; align-items:center; flex-wrap:wrap; }}
  header h1 {{ font-size:17px; margin:0; }}
  header .stat {{ color:var(--sub); font-size:12.5px; }}
  #q {{ margin-left:auto; padding:7px 12px; border:1px solid var(--line); border-radius:8px; background:#fff; width:230px; outline:none; font-size:13px; }}
  main {{ max-width:1180px; margin:0 auto; padding:14px 22px 60px; }}
  .group {{ margin-top:12px; }}
  h2 {{ font-size:16px; margin:30px 0 6px; border-left:3px solid var(--accent); padding-left:10px; }}
  h2 .count {{ color:var(--sub); font-weight:400; font-size:12px; margin-left:8px; }}
  .subgroup {{ margin:14px 0 4px; }}
  h3 {{ font-size:13px; margin:14px 0 8px; color:var(--sub); font-weight:600; letter-spacing:.5px; }}
  h3 .count {{ font-weight:400; font-size:11px; margin-left:6px; opacity:.85; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px; }}
  .card {{ position:relative; display:block; text-decoration:none; color:inherit; background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; transition:box-shadow .15s, transform .15s; }}
  .card:hover {{ box-shadow:0 6px 18px rgba(110,87,72,.12); transform:translateY(-2px); }}
  .no {{ position:absolute; top:6px; left:6px; z-index:1; background:rgba(184,147,90,.92); color:#fff; font-size:10px; padding:1px 7px; border-radius:8px; letter-spacing:.5px; }}
  .no-dim {{ background:rgba(160,148,134,.55); }}
  .tag {{ position:absolute; top:6px; right:6px; z-index:1; background:#F0E7DB; color:#8A7868; font-size:10px; padding:1px 7px; border-radius:8px; }}
  .tag-dim {{ background:#F2EEE8; color:#A89B8C; }}
  .thumb {{ aspect-ratio:5/6; display:flex; align-items:center; justify-content:center; background:#FDFBF8; padding:6px; }}
  .thumb svg {{ width:100%; height:100%; display:block; }}
  .card.dim {{ border-style:dashed; }}
  .card.dim .thumb {{ background:#F7F3ED; }}
  .phicon {{ width:52%; max-height:64%; }}
  .phicon rect, .phicon circle, .phicon path {{ fill:none; stroke:#C3B7A6; stroke-width:3; stroke-linejoin:round; stroke-linecap:round; }}
  .meta {{ padding:7px 9px 8px; font-size:12px; }}
  .meta b {{ color:var(--accent); margin-right:4px; font-weight:600; }}
  .card.dim .meta b {{ color:#A89B8C; }}
  footer {{ text-align:center; color:var(--sub); font-size:12px; padding:20px; }}
  .hide {{ display:none !important; }}
</style>
</head>
<body>
<header>
  <h1>素材总览 · 全量视图</h1>
  <span class="stat">素材图 {svg_total} 个 ｜ 知识条目以灰卡占位（不占图编号）｜ 五大区 + 场景组合组 ｜ 图编号 01 ~ {svg_total} 连续</span>
  <input id="q" placeholder="搜索：编号 / 名称 / 载体…">
</header>
<main>
{chr(10).join(blocks)}
</main>
<footer>styling-studio · 图编号连续；知识类灰卡占位（写实效果可运行时生图）</footer>
<script>
const q = document.getElementById('q');
q.addEventListener('input', () => {{
  const k = q.value.trim().toLowerCase();
  document.querySelectorAll('.subgroup').forEach(sec => {{
    let visible = 0;
    sec.querySelectorAll('.card').forEach(c => {{
      const show = !k || c.dataset.k.toLowerCase().includes(k);
      c.classList.toggle('hide', !show);
      if (show) visible++;
    }});
    sec.classList.toggle('hide', visible === 0);
  }});
  document.querySelectorAll('.group').forEach(g => {{
    const any = [...g.querySelectorAll('.subgroup')].some(s => !s.classList.contains('hide'));
    g.classList.toggle('hide', !any);
  }});
}});
</script>
</body>
</html>
'''

OUT.write_text(doc, encoding='utf-8')
print(f'已生成 {OUT.name}：图卡 {total_cards} 个（编号 01 ~ {total_cards} 连续）+ 知识占位卡')
for c, _, _ in CATS:
    seq = display_by_cat[c]
    print(f'  {c}: {len(seq)} 条（图 {sum(1 for it in seq if it["svg"])}）')
