# -*- coding: utf-8 -*-
"""
风格选型的「人话层」+ 可视对比页生成器（演示文稿版）。

问题：选型卡原先只给 `A23（赛博朋克）` 这样的编号 + 一串 hex 色值，
客户看不出这风格到底长什么样、什么气质、适合什么场合。

本模块做三件事：
  1. describe_style()  —— 把 style-system.json 的 token 翻成中文判断依据
                          （色系 / 形状 / 气质 / 场景 / 不建议）
  2. diff_note()        —— 候选相对推荐款的一句话说差异
  3. build_preview_html() —— 每个候选用真实色值画一小段「演示文稿小样」
                          （迷你封面 + 内容卡），并排对比，让客户「看见」

数据源：assets/style-system.json（49 风格机器可读 token）。
设计约束：色系判定由色值**计算**得出（HSL），不查表——风格资产增删时描述不腐坏。
"""
import colorsys
import html as _html
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE_SYSTEM = os.path.join(HERE, '..', 'assets', 'style-system.json')


def _esc(s):
    """HTML 转义，防止用户输入（标题/偏好）注入标签或事件属性。"""
    return _html.escape(str(s or ''), quote=True)


# ---------------------------------------------------------------- 颜色 → 中文

def _hex_to_rgb(h: str):
    h = (h or '').strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    except ValueError:
        return None


def _hsl(h: str):
    rgb = _hex_to_rgb(h)
    if not rgb:
        return None
    hh, ll, ss = colorsys.rgb_to_hls(*rgb)
    return hh * 360.0, ss, ll


_HUE_NAMES = [
    (12, '红'), (38, '橙'), (62, '黄'), (95, '黄绿'), (150, '绿'),
    (185, '青'), (215, '天蓝'), (255, '蓝'), (285, '蓝紫'),
    (320, '紫'), (345, '洋红'), (360, '红'),
]


def _hue_name(hue: float) -> str:
    for bound, name in _HUE_NAMES:
        if hue <= bound:
            return name
    return '红'


def _sat_word(s: float) -> str:
    if s < 0.12:
        return '无彩色'
    if s < 0.40:
        return '低饱和'
    if s < 0.68:
        return '中饱和'
    return '高饱和'


def _bg_word(light: float) -> str:
    if light >= 0.97:
        return '纯白底'
    if light >= 0.90:
        return '浅底'
    if light >= 0.72:
        return '米/浅灰底'
    if light >= 0.45:
        return '中灰底'
    if light >= 0.12:
        return '深底'
    return '近黑底'


def _series_mode(series: List[str]) -> str:
    hues, grays = [], 0
    for c in series[:8]:
        v = _hsl(c)
        if not v:
            continue
        h, s, _ = v
        if s < 0.15:
            grays += 1
        else:
            hues.append(h)
    if not hues or grays >= len(series) - 1:
        return '灰阶系列'

    def circ(a, b):
        d = abs(a - b) % 360
        return min(d, 360 - d)
    spread = max((circ(hues[0], h) for h in hues), default=0)
    if spread <= 25:
        return '同色系深浅'
    if len(hues) <= 3:
        return '少量撞色'
    return '多彩并列'


def _first_int(s: Any, default: int = 0) -> int:
    m = re.search(r'\d+', str(s or ''))
    return int(m.group()) if m else default


def _radius(style: Dict[str, Any]) -> int:
    v = (style.get('shapes') or {}).get('圆角')
    if v is None:
        return 0
    return min(_first_int(v, 0), 20)


def _title_px(style: Dict[str, Any]) -> int:
    rng = str((style.get('typography') or {}).get('size_range') or '')
    nums = [int(x) for x in re.findall(r'\d+', rng)]
    return max(nums) if nums else 32


def _title_weight(style: Dict[str, Any]) -> int:
    ws = (_first_int(w, 400) for w in (style.get('typography') or {}).get('weights') or [])
    return max(ws) if ws else 700


def _weight_word(w: int) -> str:
    if w >= 800:
        return '超粗'
    if w >= 700:
        return '粗'
    if w >= 500:
        return '中等'
    return '常规'


def describe_form(style: Dict[str, Any]) -> str:
    r = _radius(style)
    if r <= 2:
        corner = '直角'
    elif r <= 8:
        corner = f'小圆角 {r}px'
    elif r <= 16:
        corner = f'圆角 {r}px'
    else:
        corner = '大圆角（胶囊感）'
    return f'{corner} · 标题 {_title_px(style)}px {_weight_word(_title_weight(style))}'


def describe_style(style: Dict[str, Any]) -> Dict[str, Any]:
    tokens = style.get('tokens') or {}
    bg = tokens.get('bg', '#FFFFFF')
    ac = tokens.get('ac', '#000000')
    ink = tokens.get('ink', '#000000')
    series = style.get('series') or []

    bg_v = _hsl(bg) or (0, 0, 1)
    ac_v = _hsl(ac) or (0, 0, 0)
    bg_word = _bg_word(bg_v[2])
    accent_name = _hue_name(ac_v[0]) if ac_v[1] >= 0.12 else '黑/灰'
    sat_word = _sat_word(ac_v[1])
    smode = _series_mode(series)

    if bg_v[1] < 0.10:
        base = f'{bg_word} + {accent_name}强调'
    else:
        base = f'{bg_word}（带{_hue_name(bg_v[0])}调） + {accent_name}强调'
    palette = f'{base}，{smode}'

    taboos = [t for t in (style.get('taboos') or []) if t]

    return {
        'palette': palette,
        'accent_name': accent_name,
        'sat_word': sat_word,
        'series_mode': smode,
        'form': describe_form(style),
        'radius': _radius(style),
        'title_px': _title_px(style),
        'title_weight': _title_weight(style),
        'mood': style.get('mood', ''),
        'school': style.get('school', ''),
        'scenes': (style.get('scenes') or [])[:4],
        'avoid': taboos[:2],
        'is_dark': bg_v[2] < 0.45,
        'swatches': [
            {'role': '底色', 'hex': bg},
            {'role': '文字', 'hex': ink},
            {'role': '强调', 'hex': ac},
            {'role': '卡片', 'hex': tokens.get('card', bg)},
            {'role': '分隔', 'hex': tokens.get('line', bg)},
        ] + [{'role': f'图表{i + 1}', 'hex': c} for i, c in enumerate(series[:6])],
    }


def diff_note(base: Dict[str, Any], other: Dict[str, Any]) -> str:
    bd = describe_style(base)
    od = describe_style(other)
    bits = []

    b_bg = (_hsl((base.get('tokens') or {}).get('bg', '')) or (0, 0, 1))[2]
    o_bg = (_hsl((other.get('tokens') or {}).get('bg', '')) or (0, 0, 1))[2]
    if abs(b_bg - o_bg) >= 0.03:
        bits.append('底色更亮' if o_bg > b_bg else '底色更暗')

    if bd['accent_name'] != od['accent_name']:
        bits.append(f"强调色由{bd['accent_name']}换成{od['accent_name']}")
    if bd['series_mode'] != od['series_mode']:
        bits.append(f"数据系列改为{od['series_mode']}")
    if abs(bd['radius'] - od['radius']) >= 3:
        bits.append('更圆润' if od['radius'] > bd['radius'] else '更硬朗')
    if abs(bd['title_px'] - od['title_px']) >= 6:
        bits.append('标题更大' if od['title_px'] > bd['title_px'] else '标题更小')
    if abs(bd['title_weight'] - od['title_weight']) >= 100:
        bits.append('字更粗' if od['title_weight'] > bd['title_weight'] else '字更细')

    if not bits:
        mb, mo = (base.get('mood') or '').strip(), (other.get('mood') or '').strip()
        if mo and mo != mb:
            return f'配色接近，差别在手法：{mo}'
        return '配色与手法都接近，可按预览观感定'
    return '、'.join(bits)


# ---------------------------------------------------------------- 可视对比页

def build_preview_html(candidates: List[Dict[str, Any]],
                       profile: Optional[Dict[str, Any]] = None,
                       title: str = '演示风格候选') -> str:
    """
    生成候选风格并排对比页。每一列不是配色表，而是用该风格真实色值
    画的一小段「演示文稿小样」：迷你封面（章节标签 + 大标题 + 副标题）
    + 迷你内容卡。客户看一眼就知道「这是不是我想要的样子」。
    刻意不引外部库：手绘即可，换来整页轻量、断网可开、可邮件发送。
    """
    prof = profile or {}
    title = _esc(title)
    cond = ' · '.join([_esc(x) for x in [prof.get('tone', ''), prof.get('scene', ''),
                                         prof.get('purpose', '')] if x]) or '未指定偏好'

    cols = []
    base = candidates[0] if candidates else None
    for idx, c in enumerate(candidates, 1):
        toks = c.get('tokens') or {}
        series = c.get('series') or []
        d = describe_style(c)
        diff = c.get('diff_from_recommend') or (
            diff_note(base, c) if idx > 1 else '')

        bg = toks.get('bg', '#FFFFFF')
        ink = toks.get('ink', '#111111')
        ac = toks.get('ac', '#333333')
        card = toks.get('card', bg)
        line = toks.get('line', '#DDDDDD')
        mu = toks.get('mu', ink)
        # HTML 转义：防 style 属性注入
        bg, ink, ac = _esc(bg), _esc(ink), _esc(ac)
        card, line, mu = _esc(card), _esc(line), _esc(mu)

        rad = d['radius']
        tw = d['title_weight']
        tpx = max(13, min(20, round(d['title_px'] * 0.34)))

        sw = ''.join(
            f'<span class="sw"><b style="background:{_esc(s["hex"])}"></b>'
            f'<em>{_esc(s["role"])}</em><code>{_esc(s["hex"])}</code></span>'
            for s in d['swatches']
        )
        scenes = ''.join(f'<span class="chip">{_esc(t)}</span>' for t in d['scenes']) or '—'
        avoid = ''.join(f'<li>{_esc(t)}</li>' for t in d['avoid']) or '<li>无特别限制</li>'
        reason = ''.join(f'<li>{_esc(r)}</li>' for r in (c.get('reasons') or [])[:3])

        cols.append(f"""
    <section class="col{" pick" if idx == 1 else ""}">
      <div class="badge">{idx}</div>
      <header>
        <h2>{_esc(c.get('label', ''))}</h2>
        <div class="sub">{_esc(c.get('en', ''))} · 编号 {_esc(c.get('code', ''))}
          {f"· {_esc(c.get('family_label', ''))}" if c.get('family_label') else ""}</div>
      </header>
      <p class="mood">{_esc(d['mood'])}</p>
      {f'<p class="diff">与「{_esc(base.get("label", ""))}」的区别：{_esc(diff)}</p>' if diff else ''}

      <div class="stage" style="background:{bg};color:{ink};border-radius:{rad}px">
        <div class="eyebrow" style="color:{ac}">CHAPTER 01</div>
        <div class="t" style="font-weight:{tw};font-size:{tpx}px">年度经营分析</div>
        <div class="s" style="color:{mu}">2025 全年 · 示例演示</div>
        <div class="mini-card" style="background:{card};border-color:{line};border-radius:{rad}px">
          <div class="c-h" style="color:{ac}">核心要点</div>
          <div class="c-p">用这套风格做的演示文稿，观感大概就是这样</div>
        </div>
      </div>

      <dl>
        <dt>色系</dt><dd>{_esc(d['palette'])}</dd>
        <dt>形状</dt><dd>{_esc(d['form'])}</dd>
        <dt>适合</dt><dd class="chips">{scenes}</dd>
        <dt>不建议</dt><dd><ul class="avoid">{avoid}</ul></dd>
        {f'<dt>入选理由</dt><dd><ul class="avoid">{reason}</ul></dd>' if reason else ''}
      </dl>

      <div class="sw-row">{sw}</div>
    </section>""")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  *{{box-sizing:border-box}}
  body{{margin:0;padding:32px 28px 48px;background:#F1F3F5;color:#1B1F23;
       font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}}
  .head{{max-width:1400px;margin:0 auto 26px}}
  .head h1{{font-size:22px;margin:0 0 6px;font-weight:650}}
  .head p{{margin:0;color:#5B6570;font-size:13.5px;line-height:1.7}}
  .head .hint{{margin-top:10px;padding:9px 13px;background:#FFF;border-left:3px solid #2F6FEB;
              border-radius:0 6px 6px 0;font-size:13px;color:#39424C}}
  .grid{{max-width:1400px;margin:0 auto;display:grid;gap:20px;
        grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}}
  .col{{position:relative;background:#FFF;border:1px solid #DEE2E6;border-radius:12px;
       padding:18px 18px 14px;display:flex;flex-direction:column;gap:12px}}
  .col.pick{{border-color:#2F6FEB;box-shadow:0 2px 14px rgba(47,111,235,.16)}}
  .badge{{position:absolute;top:-11px;left:16px;width:24px;height:24px;border-radius:50%;
         background:#5B6570;color:#FFF;font-size:13px;font-weight:600;
         display:flex;align-items:center;justify-content:center}}
  .col.pick .badge{{background:#2F6FEB}}
  .col header h2{{margin:0;font-size:17px;font-weight:650}}
  .col header .sub{{color:#6B7684;font-size:12px;margin-top:3px}}
  .mood{{margin:0;font-size:13px;color:#3C4650;line-height:1.6;
        padding-left:9px;border-left:2px solid #D6DBE0}}
  .diff{{margin:0;font-size:12px;color:#2F6FEB;line-height:1.55;
        background:#F2F6FE;border-radius:5px;padding:6px 9px}}
  .stage{{padding:14px 13px 12px;overflow:hidden}}
  .stage .eyebrow{{font-size:9px;letter-spacing:.2em;margin-bottom:7px;font-weight:600}}
  .stage .t{{line-height:1.15;margin-bottom:6px}}
  .stage .s{{font-size:10.5px}}
  .mini-card{{border:1px solid;padding:9px 10px;margin-top:11px}}
  .mini-card .c-h{{font-size:11px;font-weight:650;margin-bottom:3px}}
  .mini-card .c-p{{font-size:10px;line-height:1.5;opacity:.85}}
  dl{{margin:0;font-size:12.5px;line-height:1.65;display:grid;
     grid-template-columns:58px 1fr;gap:4px 10px}}
  dt{{color:#6B7684}}
  dd{{margin:0;color:#242B33}}
  dd.chips{{display:flex;flex-wrap:wrap;gap:4px}}
  .chip{{background:#EEF1F4;border-radius:4px;padding:1px 7px;font-size:11.5px}}
  ul.avoid{{margin:0;padding-left:15px;color:#4A545E}}
  ul.avoid li{{margin:1px 0}}
  .sw-row{{display:flex;flex-wrap:wrap;gap:6px;padding-top:10px;border-top:1px dashed #E3E7EB}}
  .sw{{display:flex;flex-direction:column;align-items:center;gap:2px;width:52px}}
  .sw b{{width:100%;height:20px;border-radius:4px;border:1px solid rgba(0,0,0,.10)}}
  .sw em{{font-size:10px;color:#6B7684;font-style:normal}}
  .sw code{{font-size:9px;color:#9AA3AC;font-family:Consolas,monospace}}
</style>
</head>
<body>
  <div class="head">
    <h1>{title}</h1>
    <p>共 {len(candidates)} 个候选。每一列都用该风格的<strong>真实色值</strong>画了一小段演示文稿，
       看观感即可，不必记编号。</p>
    <div class="hint">你的偏好：{cond}　·　回复「1 / 2 / 3」选定，或说明想改的方向（如「要更亮」「别太花」）。</div>
  </div>
  <div class="grid">{"".join(cols)}
  </div>
</body>
</html>"""


# ---------------------------------------------------------------- CLI

def load_system():
    with open(STYLE_SYSTEM, encoding='utf-8') as f:
        return json.load(f)


def _cli():
    import argparse
    p = argparse.ArgumentParser(description='生成演示风格候选对比页')
    p.add_argument('--codes', required=True, help='风格编号，逗号分隔，如 A23,A46,A7')
    p.add_argument('--tone', default='', help='调性偏好，如 深色')
    p.add_argument('--scene', default='', help='场景偏好，如 产品发布')
    p.add_argument('--purpose', default='', help='用途，如 数据汇报')
    p.add_argument('--output', required=True, help='输出 html 路径')
    p.add_argument('--title', default='演示风格候选', help='页面标题')
    args = p.parse_args()

    system = load_system()
    codes = [c.strip().upper() for c in args.codes.split(',') if c.strip()]
    candidates = []
    for c in codes:
        if c in system:
            candidates.append(system[c])
        else:
            print(f'[警告] 未知风格编号 {c}，已跳过', file=sys.stderr)
    if not candidates:
        print('没有有效候选', file=sys.stderr)
        sys.exit(1)

    html = build_preview_html(candidates, {'tone': args.tone, 'scene': args.scene,
                                           'purpose': args.purpose}, args.title)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'对比页已生成：{args.output}（{len(candidates)} 个候选）')


if __name__ == '__main__':
    _cli()
