"""报告组装器 CLI。report_spec.json + 图表 HTML → 单文件 HTML 报告。

组装策略（与 template.py 的产物契约对齐）：
- 图表 HTML 自包含（ECharts JS 已内联），但报告不整块内联各图表 HTML——
  那会让每张图各带一份 ~MB 级 echarts.min.js。改为：报告 <head> 只内联一份
  ECharts（+ wordcloud/liquidfill 插件按需），从各图表 HTML 中提取
  `var chartOption = {...};`（锚点：起始 `var chartOption = `，
  终止 `\nchart.setOption(chartOption);`），在报告章节容器内重新 init。
  注意：提取片段须剥离末尾 `;`（源码行尾分号），否则拼入对象字面量会
  产生 JS 语法错误导致图表全部不渲染。
- spreadsheet 图表无 chartOption：提取 <table>...</table> 原样嵌入。
- 图表编辑：复刻 smart-charts 单图页的编辑能力，每张图卡带一条编辑栏：
  * 图表标题芯片（contentEditable，Enter 确认 / Escape 取消，局部
    setOption 合并 title.text）；
  * 系列名/轴名芯片（同 smart-charts 重命名面板：legend.data 与 radar
    data[0].name 同步、waterfall 垫底系列排除、轴名按 id 局部合并不回写
    拖拽位置、NO_SERIES_CHART_TYPES 不渲染"系列"分组）；
  * 「确定」按钮定稿：应用当前命名，编辑栏收起为"已定稿"状态条，
    图号标记"已定稿"；状态条带「重新编辑」按钮，可随时恢复编辑。
- 页面视觉：编辑部风格设计系统（REPORT_SHELL 三主题），与图表引擎主题联动。
- 错误输出与 cli.py 同构：结构化 JSON（error/code/code_name/details.suggestion），
  退出码 1；报告层错误码 5xxx，引擎错误码沿用 exceptions.ErrorCode。
"""

import sys
import os
import re
import json
import argparse
import subprocess
import html as html_module
from pathlib import Path
from datetime import datetime

if __name__ == '__main__' and __package__ is None:
    import _bootstrap  # noqa: F401 — 单点 sys.path 引导，见 _bootstrap.py
    from scripts.exceptions import SmartChartsError, ChartError, ErrorCode, JSONArgumentParser
    from scripts.themes import THEMES
    from scripts.texts import TEXTS
    from scripts.ledger import LedgerResolver, LedgerError, matches_any, ClaimsResolver, validate_claims
else:
    from .exceptions import SmartChartsError, ChartError, ErrorCode, JSONArgumentParser
    from .themes import THEMES
    from .texts import TEXTS
    from .ledger import LedgerResolver, LedgerError, matches_any, ClaimsResolver, validate_claims


# 报告层错误码（5xxx，不改动引擎的 exceptions.py）
_REPORT_SPEC_INVALID = 5001
_CHART_HTML_INVALID = 5002
_REPORT_ASSEMBLE_ERROR = 5003
_LEDGER_MISMATCH = 5004
_RAW_NUMBER_IN_PLACEHOLDER_MODE = 5005  # placeholder 模式下存在必溯源形态的裸数字
_EXPORT_ERROR = 5006                      # docx/pptx/svg 导出任一步失败
_EXPORT_DEPENDENCY_MISSING = 5007        # 缺少 python-docx / python-pptx / resvg-py / node
_CLAIM_EVIDENCE_INVALID = 5008           # 论点台账形式校验失败（论点缺论据/论据不可解析）

_STATIC_DIR = Path(__file__).resolve().parent.parent / 'assets'

# chartOption 提取锚点（template.py _save_html 的固定产物结构）
_OPT_START = 'var chartOption = '
_OPT_END = '\nchart.setOption(chartOption);'

_ASPECT_RE = re.compile(r'aspect-ratio:\s*([0-9.]+)')
_MIN_WIDTH_RE = re.compile(r'min-width:\s*(\d+)px')
_SAFE_ID_RE = re.compile(r'[^a-zA-Z0-9_-]')

_SERIF = '"Songti SC", "STSong", "Noto Serif SC", "Source Han Serif SC", Georgia, "Times New Roman", serif'
_SANS = "'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', system-ui, sans-serif"

# 编辑部风格设计系统：三主题报告壳，与图表引擎主题画布色对齐
# paper=页面底色  card=卡片底色  chart_card=图卡底色(须与图表画布色一致)
REPORT_SHELL = {
    'default': {  # 纸墨蓝 · 暖纸底 + 墨蓝强调（配 Okabe-Ito 图表色板）
        'paper': '#F6F4EF', 'paper_deep': '#EEEAE0', 'card': '#FFFFFF',
        'chart_card': '#FFFFFF', 'ink': '#26292E', 'ink_soft': '#5C6066',
        'ink_faint': '#9A9A9E', 'hairline': '#E7E3D8', 'accent': '#0E6BA8',
        'accent_deep': '#0A5691', 'accent_tint': '#EAF3F9',
        'locked': '#4E7A62',
    },
    'classic': {  # 冷灰蓝 · 冷静商务（配引擎 classic 蓝紫主色）
        'paper': '#F1F4F9', 'paper_deep': '#E3E9F2', 'card': '#FFFFFF',
        'chart_card': '#FFFFFF', 'ink': '#1F2A3D', 'ink_soft': '#5A6B82',
        'ink_faint': '#93A1B5', 'hairline': '#DFE5EE', 'accent': '#3D5FA8',
        'accent_deep': '#2C4A88', 'accent_tint': '#EDF1FA',
        'locked': '#4E7A62',
    },
    'dark': {  # 深空蓝 · 深色演示场景（配引擎 dark 画布 #262640）
        'paper': '#101319', 'paper_deep': '#1A1F2B', 'card': '#161B24',
        'chart_card': '#262640', 'ink': '#E8EBF2', 'ink_soft': '#A8B0C0',
        'ink_faint': '#6E7889', 'hairline': '#2A3140', 'accent': '#5B8FF9',
        'accent_deep': '#7C9DFF', 'accent_tint': 'rgba(91, 143, 249, 0.10)',
        'locked': '#5FA77F',
    },
}


def _emit_error(code: int, code_name: str, message: str, suggestion: str,
                details: dict = None) -> None:
    payload = {
        'error': message,
        'code': code,
        'code_name': code_name,
        'details': {'suggestion': suggestion, **(details or {})},
    }
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def _spec_error(message: str, suggestion: str, details: dict = None):
    return _emit_error(_REPORT_SPEC_INVALID, 'REPORT_SPEC_INVALID', message,
                       suggestion, details)


def _safe_section_id(raw: str, idx: int) -> str:
    sid = _SAFE_ID_RE.sub('-', str(raw).strip())[:40]
    return sid if sid else f'section-{idx + 1}'


def _resolve_chart_path(chart_path: str, charts_dir: Path, spec_dir: Path) -> Path:
    """解析图表路径：原样 → charts_dir 下 → spec 同目录下。"""
    candidates = [
        Path(chart_path),
        charts_dir / chart_path,
        spec_dir / chart_path,
    ]
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def _extract_chart_payload(html_text: str, source: Path) -> dict:
    """从图表 HTML 提取可嵌入负载。

    返回 {'kind': 'echarts', 'option_js': str, 'aspect': float, 'min_width': int|None,
           'plugins': set[str]}
    或 {'kind': 'table', 'table_html': str}（spreadsheet）。
    """
    start = html_text.find(_OPT_START)
    if start != -1:
        end = html_text.find(_OPT_END, start)
        if end == -1:
            _emit_error(_CHART_HTML_INVALID, 'CHART_HTML_INVALID',
                        f'图表 HTML 缺少 setOption 锚点，无法提取 chartOption: {source.name}',
                        '该文件可能不是 cli.py 生成的图表 HTML；请用 Step 3 批量生成的产物重新组装',
                        {'given': str(source)})
            raise SystemExit(1)
        # 源码为 `var chartOption = {...};` —— 剥离末尾分号，否则拼入
        # 对象字面量会产生 JS 语法错误，导致报告图表全部不渲染
        option_js = html_text[start + len(_OPT_START):end].strip()
        while option_js.endswith(';'):
            option_js = option_js[:-1].rstrip()
        if not option_js.startswith('{') or not option_js.endswith('}'):
            _emit_error(_CHART_HTML_INVALID, 'CHART_HTML_INVALID',
                        f'图表 HTML 的 chartOption 不是对象字面量: {source.name}',
                        '图表文件可能损坏；请重新生成该图表后再组装',
                        {'given': str(source)})
            raise SystemExit(1)
        aspect_m = _ASPECT_RE.search(html_text)
        minw_m = _MIN_WIDTH_RE.search(html_text)
        plugins = set()
        if '"type": "wordCloud"' in option_js:
            plugins.add('wordcloud')
        if '"type": "liquidFill"' in option_js:
            plugins.add('liquidfill')
        return {
            'kind': 'echarts',
            'option_js': option_js,
            'aspect': float(aspect_m.group(1)) if aspect_m else 900 / 560,
            'min_width': int(minw_m.group(1)) if minw_m else None,
            'plugins': plugins,
        }

    # spreadsheet：无 chartOption，提取整张表
    t_start = html_text.find('<table>')
    t_end = html_text.find('</table>')
    if t_start != -1 and t_end != -1:
        return {'kind': 'table', 'table_html': html_text[t_start:t_end + len('</table>')]}

    _emit_error(_CHART_HTML_INVALID, 'CHART_HTML_INVALID',
                f'无法从图表 HTML 中识别可嵌入内容（既无 chartOption 也无表格）: {source.name}',
                '确认该文件是 cli.py 生成的图表 HTML（echarts 或 spreadsheet 类型）',
                {'given': str(source)})
    raise SystemExit(1)


def _paras(text: str) -> str:
    """多段文本 → 多个 <p>；\n\n 分段，逐段 HTML 转义。"""
    if not text:
        return ''
    chunks = [c.strip() for c in re.split(r'\n\s*\n', str(text)) if c.strip()]
    return ''.join(f'<p>{html_module.escape(c).replace(chr(10), "<br>")}</p>' for c in chunks)


def _ghost_text(title: str, subtitle: str) -> str:
    """封面幽灵大字：取标题/副标题中的年份，否则 REPORT。"""
    m = re.search(r'(?:19|20)\d{2}', f'{title} {subtitle}')
    return m.group(0) if m else 'REPORT'



# ---------------- 事实台账校验与占位符替换 ----------------
# 两种模式：
#   placeholder（默认推荐用于 v1.1+）：文本用 {{id}} 引用台账条目，替换时校验；未知 id 报 5004，
#         裸数字（必溯源形态）报 5005；fmt 精度下降也会被捕获。
#   scan（兼容旧 spec）：保留 v1.0 的"扫描数字→匹配台账值"机制，并吸收 Level 1 修订
#         （%/个百分点/倍强制入账；年份后缀白名单修复"2025全年"误报与"2025万元"漏报）。
#
# 通用豁免：日期（年/月份/季度/Q[1-4]）、图号、章节引用（§1），
# 以及"裸小整数 + 计数语境"（如"59 名学生"、"3 个类别"），不被强制溯源。
# 容差：按显示位数四舍五入，文本 98.6 可命中台账 98.56。

_DATE_PATTERNS = [
    re.compile(r"\d{4}-\d{2}(-\d{2})?"),                                    # 2025-01 / 2025-06-30
    re.compile(r"(?:从|至|截至|于|在|自|到)\s*(?:19|20)\d{2}"),                 # 从 2025 / 至 2026
    re.compile(r"(?:19|20)\d{2}\s*(?:年|年度|全年|上半年|下半年|期间|以来|至今|Q[1-4])"),  # 2025 年 / 2025 全年
    re.compile(r"\d{1,2}\s*月(?![度内例])"),                                    # 6 月
    re.compile(r"Q[1-4]|第?[1-4一二三四]季度"),
    re.compile(r"图\s*\d+"),
    re.compile(r"§\w+"),
]


def _scan_text_for_required_numbers(text: str):
    """保留为 legacy 兼容入口：Level 1 修订规则下的必溯源数字切片。

    实际生产用 LedgerResolver.required_numbers；此处仅供 / 向后兼容的辅助函数
    或被 main 之外的测试复用。
    """
    return LedgerResolver.required_numbers(text)


def _verify_ledger(ns, spec: dict, normalized: list, resolver: LedgerResolver | None) -> dict:
    """台账校验入口。--ledger-mode 决定走 placeholder 还是 scan 路径。

    返回统计 dict（citations / misses）。失败抛 LedgerError（已被 main 统一收口）。
    """
    if resolver is None:
        return None
    ledger_vals = resolver.values_for_matching()

    # 待校验的文本字段（标题/副题/摘要/章节标题/叙事/图注/附录）
    fields = []
    for key in ('title', 'subtitle', 'executive_summary'):
        fields.append((key, spec.get(key) or ''))
    for s in normalized:
        fields.append((f"{s['id']}.title", s['title']))
        fields.append((f"{s['id']}.narrative", s['narrative']))
        fields.append((f"{s['id']}.annotation", s['annotation']))
    appendix = spec.get('appendix') or {}
    for key in ('methodology', 'caveats'):
        fields.append((f"appendix.{key}", appendix.get(key) or ''))

    if ns.ledger_mode == 'placeholder':
        return _verify_placeholder(ns, fields, resolver)
    return _verify_scan(ns, fields, ledger_vals)


def _verify_placeholder(ns, fields, resolver: LedgerResolver) -> dict:
    """placeholder 模式：未知 id → 5004；必溯源形态的裸数字 → 5005。

    注：替换已在 assemble() 早期完成；此处主要跑"残留裸数字"扫描并记录 citations。
    """
    citations = sum(len(v) for v in resolver.citations.values())
    misses = []
    for where, text in fields:
        for display, value, ctx in LedgerResolver.required_numbers(text):
            # 必溯源形态的裸数字：若 value 不在 ledger 中则报错
            if not matches_any(value, resolver.values_for_matching()):
                misses.append({'where': where, 'number': display, 'context': ctx})
    if misses:
        _emit_error(
            _RAW_NUMBER_IN_PLACEHOLDER_MODE, 'RAW_NUMBER_IN_PLACEHOLDER_MODE',
            f"发现 {len(misses)} 个必溯源形态的裸数字（placeholder 模式下须改用 {{{{id}}}} 引用）",
            f"把这些数字入账后用 {{{{ledger_id}}}} 替换；或临时降级为 --ledger-mode scan",
            {'misses': misses[:20], 'misses_total': len(misses)},
        )
        raise SystemExit(1)
    return {'checked': True, 'mode': 'placeholder', 'entries': len(resolver.entries),
            'citations': citations, 'misses': 0}


def _verify_scan(ns, fields, ledger_vals) -> dict:
    """scan 模式（兼容 + Level 1 修订）：只校验未被占位符占据的必溯源数字。"""
    misses = []
    total = 0
    for where, text in fields:
        for display, value, ctx in LedgerResolver.required_numbers(text):
            total += 1
            if not matches_any(value, ledger_vals):
                misses.append({'where': where, 'number': display, 'context': ctx})
    if misses:
        _emit_error(
            _LEDGER_MISMATCH, 'LEDGER_MISMATCH',
            f"发现 {len(misses)} 个未溯源数字（正文/摘要引用的数字必须先入 ledger.json）",
            "把这些数字入账（value 与文本同量纲，如 98.6%/2670 万元 → 98.6/2670），"
            "或改用台账中已有的数值重写该句；派生数字（差值/占比变化）也要入账",
            {'misses': misses[:20], 'misses_total': len(misses)},
        )
        if ns.ledger_check == 'strict':
            raise SystemExit(1)
    return {'checked': True, 'mode': 'scan', 'entries': len(ledger_vals) and len(ledger_vals) or 0,
            'citations': total, 'misses': len(misses)}


# ---------------- 多格式导出（HTML/DOCX/PPTX） ----------------

def _build_export_manifest(payloads: dict, theme: str) -> list:
    """把章节图表 option 整理成 export_charts.js 的 manifest。

    主题决定 SVG 背景色（白底，避免暗色文字隐形）。
    """
    bg = '#FFFFFF'
    for k, v in REPORT_SHELL.items():
        if k == theme:
            bg = v.get('chart_card', '#FFFFFF')
            break
    manifest = []
    for sid, pl in payloads.items():
        if pl.get('kind') != 'echarts':
            continue
        manifest.append({
            'id': sid,
            'option_js': pl['option_js'],
            'width': 900,
            'height': 560,
            'plugins': sorted(pl.get('plugins') or []),
            'background': bg,
        })
    return manifest


def _run_node_export(skill_root: Path, manifest: list, out_dir: Path, timeout: int = 60):
    """调 export_charts.js 生成 SVG。返回 (success: bool, items: list, stderr_tail: str)。"""
    manifest_path = out_dir / '_manifest.json'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
    env = os.environ.copy()
    env['NODE_PATH'] = str(skill_root / 'scripts')
    try:
        proc = subprocess.run(
            ['node', str(skill_root / 'scripts' / 'export_charts.js'),
             str(manifest_path), str(out_dir)],
            env=env, capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError as e:
        return False, [], f"未找到 node 可执行文件: {e}"
    except subprocess.TimeoutExpired:
        return False, [], f"node 子进程超时（{timeout}s）"
    parsed = {}
    try:
        if proc.stdout.strip():
            parsed = json.loads(proc.stdout)
    except json.JSONDecodeError:
        parsed = {'charts': [], 'summary': {}, '_raw_stdout': proc.stdout[:300]}
    items = parsed.get('charts') or []
    return proc.returncode == 0, items, (proc.stderr or '')[-300:]


def _rasterize_svgs(svg_dir: Path, png_dir: Path, width: int = 1200) -> dict:
    """SVG 文件 → PNG；返回 {section_id: png_path or None}。失败逐图记录但不抛。"""
    from scripts.rasterize import svg_to_png_bytes, RasterizerError
    out = {}
    png_dir = Path(png_dir); png_dir.mkdir(parents=True, exist_ok=True)
    for svg_path in sorted(Path(svg_dir).glob('*.svg')):
        sid = svg_path.stem
        try:
            png = svg_to_png_bytes(svg_path.read_text(encoding='utf-8'), width=width)
            png_path = png_dir / f'{sid}.png'
            png_path.write_bytes(png)
            out[sid] = str(png_path)
        except RasterizerError as e:
            out[sid] = None
    return out


def _safe_spec_text(spec, normalized, original):
    """placeholder 替换时若出错，给出原文副本 + 错误位置便于排查。

    placeholder 替换必须 mutate normalized/sections 副本用于下游 HTML/DOCX/PPTX 输出；
    失败时报错位置精确到 which field。
    """
    return original


def _apply_placeholder_substitution(spec: dict, normalized: list,
                                    resolver: LedgerResolver) -> tuple:
    """对 spec/normalized 中所有文本字段做占位符替换；返回 (新spec, 新sections) 不破坏原 dict。

    任何占位符解析错误（5004）由 LedgerError 抛出，main 收口统一报。
    """
    new_spec = dict(spec)
    for k in ('title', 'subtitle', 'executive_summary'):
        if k in new_spec:
            new_spec[k] = resolver.resolve_text(new_spec.get(k) or '', k)
    appendix = dict(new_spec.get('appendix') or {})
    for k in ('methodology', 'caveats'):
        if k in appendix:
            appendix[k] = resolver.resolve_text(appendix.get(k) or '', f'appendix.{k}')
    if appendix:
        new_spec['appendix'] = appendix

    new_sections = []
    for s in normalized:
        ns = dict(s)
        ns['title'] = resolver.resolve_text(s.get('title') or '', f"{s['id']}.title")
        ns['narrative'] = resolver.resolve_text(s.get('narrative') or '', f"{s['id']}.narrative")
        ns['annotation'] = resolver.resolve_text(s.get('annotation') or '', f"{s['id']}.annotation")
        new_sections.append(ns)
    return new_spec, new_sections


def _ledger_appendix_html(resolver: LedgerResolver) -> str:
    """HTML 报告附录：关键数据溯源表（4 列）。"""
    if not resolver or not resolver.entries:
        return ''
    rows = []
    for e in resolver.entries:
        rows.append(
            f"<tr><td>{html_module.escape(e.metric)}</td>"
            f"<td>{html_module.escape(str(e.value))}</td>"
            f"<td>{html_module.escape(e.unit)}</td>"
            f"<td>{html_module.escape(e.source)}</td></tr>"
        )
    return (
        '<section id="ledger-appendix" class="card section appendix">'
        '<div class="sec-head"><span class="sec-num">L</span>'
        '<h2>附录·关键数据溯源</h2></div>'
        '<div class="sec-rule"><i></i></div>'
        '<p>本表列出正文引用的关键数字及其在数据台账中的出处，便于读者复核口径。</p>'
        '<div class="table-box"><table>'
        '<thead><tr><th>指标</th><th>数值</th><th>单位</th><th>出处</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></section>'
    )


def _claims_appendix_html(claims_resolver: ClaimsResolver | None) -> str:
    """HTML 报告附录：论点与论据链表（论点 → 论据 → 章节）。"""
    if not claims_resolver or not claims_resolver.claims:
        return ''
    rows = []
    for c in claims_resolver.claims:
        ev = '、'.join(c.evidence)
        rows.append(
            f"<tr><td>{html_module.escape(c.claim)}</td>"
            f"<td>{html_module.escape(ev)}</td>"
            f"<td>{html_module.escape(c.section or '—')}</td></tr>"
        )
    return (
        '<section id="claims-appendix" class="card section appendix">'
        '<div class="sec-head"><span class="sec-num">C</span>'
        '<h2>附录·论点与论据</h2></div>'
        '<div class="sec-rule"><i></i></div>'
        '<p>本表列出报告的分析主张及其论据（事实台账条目 / 图表章节），'
        '论据链接已经过程序校验（论点必有论据、论据真实可定位）。</p>'
        '<div class="table-box"><table>'
        '<thead><tr><th>论点</th><th>论据</th><th>章节</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></section>'
    )


def _emit_export_error(code: int, code_name: str, message: str,
                       suggestion: str, details: dict = None):
    payload = {
        'error': message, 'code': code, 'code_name': code_name,
        'details': {'suggestion': suggestion, **(details or {})},
    }
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def build_parser() -> JSONArgumentParser:
    parser = JSONArgumentParser(
        prog='report_assembler.py',
        description='Smart Report：report_spec.json + 图表 HTML → 单文件 HTML 报告（可选 docx/pptx）',
    )
    parser.add_argument('--spec', required=True, help='report_spec.json 路径')
    parser.add_argument('--charts-dir', dest='charts_dir', default=None,
                        help='图表 HTML 所在目录（spec 中 chart_path 的相对解析基准）')
    parser.add_argument('--output', default='./smart_report_output/report.html',
                        help='报告输出路径（默认 ./smart_report_output/report.html）；--format 含其他格式时按同 stem 派生 .docx / .pptx')
    parser.add_argument('--ledger', default=None,
                        help='事实台账 ledger.json 路径；传入即启用数字溯源校验（推荐始终启用）')
    parser.add_argument('--claims', default=None,
                        help='论点台账 claims.json 路径；传入即启用论据链形式校验'
                             '（每个论点必须声明论据、论据必须可解析为台账事实或含图章节）')
    parser.add_argument('--claims-check', dest='claims_check', default='basic',
                        choices=['basic', 'coverage'],
                        help='论点校验级别：basic（默认）= 论点有论据 + 论据可解析 + 论点数字可溯源；'
                             'coverage = basic + 每张图必须被至少一个论点引用'
                             ' + 每段叙事（narrative 非空）必须被至少一个论点的 section 指向')
    parser.add_argument('--ledger-mode', dest='ledger_mode', default='scan',
                        choices=['scan', 'placeholder'],
                        help='台账校验模式：scan=扫描数字匹配台账值（兼容旧 spec，默认）；'
                             'placeholder=文本用 {{id}} 引用台账条目，替换时校验（推荐，可根治漏检/张冠李戴）')
    parser.add_argument('--ledger-check', dest='ledger_check', default='strict',
                        choices=['strict', 'warn'],
                        help='scan 模式下未溯源数字的处理：strict（默认，失败）/ warn（仅警告）')
    parser.add_argument('--format', dest='formats', default='html',
                        help='导出格式，逗号分隔，默认 html：html|docx|pptx 或 all；非 html 格式需 node ≥ 16 与 resvg-py（docx/pptx 还需要 python-docx / python-pptx）')
    parser.add_argument('--export-dir', dest='export_dir', default=None,
                        help='中间产物目录（SVG/PNG manifest），默认在 --output 同级 <stem>_assets 下；可自定义')
    return parser


def _build_css(shell: dict) -> str:
    """编辑部风格设计系统。token 用 __NAME__ 占位替换，避免 f-string 转义地狱。"""
    css = """
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
::selection { background: __ACCENT__; color: #fff; }
body {
  margin: 0; padding: 44px 20px 64px;
  background: __PAPER__;
  background-image: radial-gradient(900px 380px at 50% -180px, __PAPER_DEEP__, transparent 70%);
  color: __INK__;
  font-family: __SANS_TOKEN__;
  font-size: 15px; line-height: 1.85;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 880px; margin: 0 auto; }
section { scroll-margin-top: 24px; }
.card {
  background: __CARD__; border: 1px solid __HAIRLINE__; border-radius: 14px;
  margin-bottom: 28px;
  box-shadow: 0 1px 2px rgba(20, 24, 32, 0.03), 0 10px 28px rgba(20, 24, 32, 0.05);
}

/* ---------- 封面 ---------- */
.cover { position: relative; overflow: hidden; padding: 46px 46px 42px; }
.cover::before {
  content: ''; position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(620px 260px at 92% -50px, __ACCENT_TINT__, transparent 65%),
    radial-gradient(520px 240px at -70px 105%, __PAPER_DEEP__, transparent 60%);
}
.cover::after {
  content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 5px;
  background: linear-gradient(90deg, __ACCENT__, __ACCENT_DEEP__);
}
.cover > * { position: relative; }
.brand-row { display: flex; align-items: center; gap: 12px; margin-bottom: 38px; }
.brand { font-size: 12px; font-weight: 700; letter-spacing: 5px; color: __ACCENT__; }
.brand-sub { font-size: 12px; letter-spacing: 5px; color: __INK_FAINT__; }
.brand-rule { flex: 1; height: 1px; background: __HAIRLINE__; }
.cover-title {
  font-family: __SERIF_TOKEN__; font-size: clamp(26px, 5vw, 38px); line-height: 1.4;
  font-weight: 700; color: __INK__; margin: 0 0 14px; letter-spacing: 1px;
}
.cover-sub { font-size: 14px; color: __INK_SOFT__; margin: 0 0 32px; line-height: 1.9; max-width: 660px; }
.cover-meta {
  display: flex; gap: 22px; flex-wrap: wrap; font-size: 12px; color: __INK_FAINT__;
  border-top: 1px solid __HAIRLINE__; padding-top: 16px; letter-spacing: 1px;
}
.cover-meta b { color: __INK_SOFT__; font-weight: 600; font-family: __SERIF_TOKEN__; font-size: 14px; }
.cover-ghost {
  position: absolute; right: 28px; bottom: 26px; font-family: __SERIF_TOKEN__;
  font-size: 112px; line-height: 1; font-weight: 700; color: __INK__;
  opacity: 0.05; pointer-events: none; user-select: none;
}

/* ---------- 目录 ---------- */
.toc { padding: 28px 46px 24px; }
.block-label { font-size: 12px; font-weight: 700; letter-spacing: 5px; color: __ACCENT__; margin: 0 0 12px; }
.toc-item { display: flex; align-items: baseline; gap: 12px; padding: 8px 0; text-decoration: none; }
.toc-num { font-family: __SERIF_TOKEN__; font-weight: 700; color: __ACCENT__; font-size: 15px; min-width: 26px; }
.toc-title { font-size: 14px; color: __INK__; transition: color 0.15s; }
.toc-item:hover .toc-title { color: __ACCENT__; }
.toc-line { flex: 1; border-bottom: 1px dotted __INK_FAINT__; opacity: 0.45; transform: translateY(-4px); }

/* ---------- 执行摘要 ---------- */
.summary { padding: 28px 46px 30px; border-top: 3px solid __ACCENT__; }
.summary p { margin: 0 0 12px; text-align: justify; }
.summary p:last-child { margin: 0; }

/* ---------- 章节 ---------- */
.section { padding: 36px 46px 38px; }
.sec-head { display: flex; align-items: baseline; gap: 14px; }
.sec-num { font-family: __SERIF_TOKEN__; font-size: 27px; font-weight: 700; color: __ACCENT__; line-height: 1; }
.section h2 {
  font-family: __SERIF_TOKEN__; font-size: 21px; font-weight: 700; margin: 0;
  color: __INK__; letter-spacing: 0.5px; line-height: 1.5;
}
.sec-rule { position: relative; height: 1px; background: __HAIRLINE__; margin: 15px 0 18px; }
.sec-rule i { position: absolute; left: 0; top: -1.5px; width: 46px; height: 3px; border-radius: 2px; background: __ACCENT__; }
.section p { margin: 0 0 13px; text-align: justify; }

/* ---------- 图卡 ---------- */
.fig {
  position: relative; margin: 22px 0 8px; padding: 24px 16px 10px;
  background: __CHART_CARD__; border: 1px solid __HAIRLINE__; border-radius: 12px;
}
.fig-tag {
  position: absolute; top: -11px; left: 16px; background: __ACCENT__; color: #fff;
  font-size: 11px; letter-spacing: 3px; padding: 3px 13px; border-radius: 999px; font-weight: 600;
  transition: background 0.3s;
}
.fig.fig-locked .fig-tag { background: __LOCKED__; }
.chart-scroll { width: 100%; position: relative; overflow-x: auto; overflow-y: hidden; }
.chart-canvas { width: 100%; min-height: 320px; }

/* ---------- 图表编辑栏（标题/系列/轴芯片 + 定稿） ---------- */
.fig-edit {
  display: flex; flex-wrap: wrap; align-items: center; gap: 5px 10px;
  margin: 12px 6px 8px; padding: 10px 10px 12px; border-top: 1px dashed __HAIRLINE__;
}
.fe-label { font-size: 11px; font-weight: 700; letter-spacing: 3px; color: __ACCENT__; margin-right: 2px; }
.fe-hint { width: 100%; font-size: 11px; color: __INK_FAINT__; line-height: 1.6; margin: 0; }
.fe-group-label { font-size: 12px; color: __INK_SOFT__; margin: 0 2px 0 6px; }
.fe-chip {
  display: inline-block; padding: 2px 10px; border: 1px dashed __HAIRLINE__;
  border-radius: 10px; color: __INK_SOFT__; cursor: text; outline: none;
  background: __PAPER__; font-size: 12px; line-height: 1.7; min-width: 30px;
  max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.fe-chip:hover, .fe-chip:focus { border-color: __ACCENT__; background: __CARD__; color: __INK__; }
.fe-confirm {
  margin-left: auto; padding: 4px 18px; background: __ACCENT__; color: #fff;
  border: none; border-radius: 999px; cursor: pointer; font-size: 12px;
  letter-spacing: 2px; font-weight: 600; align-self: center;
}
.fe-confirm:hover { background: __ACCENT_DEEP__; }

/* ---------- 定稿状态条 ---------- */
.fig-done {
  display: none; align-items: center; gap: 10px;
  margin: 12px 6px 8px; padding: 8px 10px; border-top: 1px dashed __HAIRLINE__;
}
.fd-label { font-size: 11px; font-weight: 700; letter-spacing: 3px; color: __LOCKED__; }
.fe-redo {
  margin-left: auto; padding: 3px 14px; background: transparent; color: __ACCENT__;
  border: 1px solid __ACCENT__; border-radius: 999px; cursor: pointer; font-size: 12px;
  letter-spacing: 1px;
}
.fe-redo:hover { background: __ACCENT__; color: #fff; }

/* ---------- 图注 ---------- */
.annotation {
  display: flex; gap: 10px; margin-top: 15px; padding: 12px 16px;
  background: __PAPER__; border: 1px solid __HAIRLINE__; border-radius: 10px;
  font-size: 13px; color: __INK_SOFT__; line-height: 1.75;
}
.ann-tag { flex: none; font-size: 12px; font-weight: 700; color: __ACCENT__; letter-spacing: 2px; padding-top: 1px; }
.annotation p { margin: 0 0 6px; text-align: left; }
.annotation p:last-child { margin: 0; }

/* ---------- 附录 ---------- */
.appendix h3 { font-size: 13px; letter-spacing: 3px; color: __ACCENT__; margin: 20px 0 8px; font-weight: 700; }
.appendix p { font-size: 13.5px; color: __INK_SOFT__; }

/* ---------- 表格（spreadsheet 图表） ---------- */
.table-box { max-height: 60vh; overflow: auto; border: 1px solid __HAIRLINE__; border-radius: 10px; margin: 16px 0; }
table { border-collapse: collapse; width: 100%; font-size: 13px; color: __INK__; background: __CARD__; }
th {
  position: sticky; top: 0; background: __PAPER__; color: __INK_SOFT__; font-weight: 600;
  padding: 8px 12px; text-align: left; white-space: nowrap;
  border-bottom: 1px solid __HAIRLINE__; z-index: 1;
}
td { padding: 6px 12px; border-bottom: 1px solid __HAIRLINE__; white-space: nowrap; }
tbody tr:hover { background: __ACCENT_TINT__; }

/* ---------- 页脚 ---------- */
.report-footer { text-align: center; font-size: 11px; letter-spacing: 3px; color: __INK_FAINT__; padding: 8px 0 0; }

@media (max-width: 640px) {
  body { padding: 16px 10px 40px; }
  .card { border-radius: 12px; }
  .cover, .toc, .summary, .section { padding-left: 22px; padding-right: 22px; }
  .cover { padding-top: 32px; }
  .chart-canvas { min-height: 250px; }
  .cover-ghost { font-size: 72px; }
  .fe-confirm { margin-left: 0; }
}
@media print {
  body { padding: 0; background: __CARD__; }
  .card { box-shadow: none; page-break-inside: avoid; margin-bottom: 18px; }
  .fig { page-break-inside: avoid; }
  .fig-edit { display: none !important; }
  .fig-done { display: none !important; }
}
"""
    tokens = dict(shell)
    tokens['SERIF_TOKEN'] = _SERIF
    tokens['SANS_TOKEN'] = _SANS
    for key, value in tokens.items():
        css = css.replace(f'__{key.upper()}__', value)
    return css


def _build_init_js() -> str:
    """图表 init + 编辑栏脚本。

    编辑栏复刻 smart-charts 单图页的编辑能力（template.py）：
    - 图表标题芯片：contentEditable，改后局部 setOption 合并 title.text；
    - 系列名/轴名芯片：Enter 确认 / Escape 取消，blur 应用；系列改名同步
      legend.data 与 data[0].name（radar），局部 setOption 不触碰 graphic；
      轴名是可拖拽 graphic（id 前缀 axisName-），改名只改文字不回写位置；
    - 无系列概念的图表（NO_SERIES_CHART_TYPES）不渲染"系列"分组；
    - 「确定」定稿：编辑栏收起 → "已定稿"状态条（含「重新编辑」按钮），
      图号标记"已定稿"；重新编辑可恢复编辑栏，命名保留（option 已就地更新）。
    文案复用 texts.TEXTS（zh），编辑栏语境文案在本模块补充。
    """
    t = TEXTS['zh']
    hint = ('点击名称可修改（Enter 确认，Esc 还原）：标题、系列名、轴名均可编辑；'
            '轴名还可在图上直接拖拽调整位置；完成后点击「确定」定稿')
    confirm_btn = '确定'
    finalized = '已定稿'
    redo_btn = '重新编辑'
    group_title = '标题'
    group_series = t['rename_group_series']
    group_axis = t['rename_group_axis']

    return f"""var __SR_NO_SERIES = ['pie','heatmap','treemap','graph','gauge','sankey','funnel','sunburst','wordcloud','histogram','boxplot','bubble','venn','mindmap','orgchart','liquid','spreadsheet'];
(function() {{
  Object.keys(__SR_OPTIONS).forEach(function(id) {{
    var dom = document.getElementById('chart-' + id);
    if (!dom) return;
    var opt = __SR_OPTIONS[id];
    var chart = echarts.init(dom);
    chart.setOption(opt);
    window.addEventListener('resize', function() {{ chart.resize(); }});
    new ResizeObserver(function() {{ chart.resize(); }}).observe(dom);

    var panel = document.getElementById('fedit-' + id);
    var fig = dom.closest('.fig');
    if (!panel) return;

    // ---- 收集可编辑条目（同 template.py 规则） ----
    var titleEntry = (opt.title && opt.title.text) ? opt.title : null;
    var seriesEntries = [], axisEntries = [];
    var st = (opt.series && opt.series[0] && opt.series[0].type) || '';
    if (__SR_NO_SERIES.indexOf(st) === -1) {{
      (opt.series || []).forEach(function(s) {{
        if (s.name && String(s.name).indexOf('__waterfall_base__') !== 0) seriesEntries.push(s);
      }});
    }}
    (opt.graphic || []).forEach(function(el) {{
      if (el.id && String(el.id).indexOf('axisName-') === 0) axisEntries.push(el);
    }});
    if (!titleEntry && !seriesEntries.length && !axisEntries.length) {{ panel.remove(); return; }}

    // ---- 构建编辑栏：提示 → 标题 → 系列 → 轴 → 确定 ----
    var hintEl = document.createElement('p');
    hintEl.className = 'fe-hint';
    hintEl.textContent = {json.dumps(hint, ensure_ascii=False)};
    panel.appendChild(hintEl);

    function addGroup(labelText, entries, apply) {{
      if (!entries.length) return;
      var label = document.createElement('span');
      label.className = 'fe-group-label';
      label.textContent = labelText + '·';
      panel.appendChild(label);
      entries.forEach(function(obj) {{
        var chip = document.createElement('span');
        chip.className = 'fe-chip';
        var original = apply('get', obj);
        chip.title = chip.textContent = original;
        chip.contentEditable = 'true';
        chip.addEventListener('keydown', function(e) {{
          if (e.key === 'Enter') {{ e.preventDefault(); chip.blur(); }}
          if (e.key === 'Escape') {{ chip.textContent = original; chip.blur(); }}
        }});
        chip.addEventListener('blur', function() {{
          var v = chip.textContent.trim();
          if (v && v !== original) {{ apply('set', obj, v); original = v; chip.title = v; }}
          else {{ chip.textContent = original; }}
        }});
        panel.appendChild(chip);
      }});
    }}

    addGroup({json.dumps(group_title, ensure_ascii=False)}, titleEntry ? [titleEntry] : [], function(op, el, v) {{
      if (op === 'get') return el.text;
      el.text = v;
      // 局部合并：只更新标题文本，不触碰其余属性
      chart.setOption({{ title: {{ text: v }} }});
    }});
    addGroup({json.dumps(group_series, ensure_ascii=False)}, seriesEntries, function(op, s, v) {{
      if (op === 'get') return s.name;
      var old = s.name;
      s.name = v;
      // radar 等图 series.data[0].name 与 series.name 同名，同步更新避免 tooltip 显示旧名
      var syncedData = false;
      if (s.data && s.data.length && s.data[0] && s.data[0].name === old) {{
        s.data[0].name = v;
        syncedData = true;
      }}
      // legend.data 若显式列出系列名（如 waterfall），同步替换，否则改名后图例失配消失
      if (opt.legend && opt.legend.data) {{
        opt.legend.data = opt.legend.data.map(function(n) {{ return n === old ? v : n; }});
      }}
      // 局部合并：只更新系列名与图例，不触碰 graphic（保留轴名拖拽位置）
      chart.setOption({{ series: opt.series.map(function(x) {{
                          if (x === s && syncedData) {{ return {{ name: x.name, data: x.data }}; }}
                          return {{ name: x.name }};
                        }}),
                         legend: opt.legend }});
    }});
    addGroup({json.dumps(group_axis, ensure_ascii=False)}, axisEntries, function(op, el, v) {{
      if (op === 'get') return el.style.text;
      el.style.text = v;
      // 按 id 局部合并，只改文字，不重置拖拽后的位置
      chart.setOption({{ graphic: [{{ id: el.id, style: {{ text: v }} }}] }});
    }});

    // ---- 「确定」定稿 / 「重新编辑」恢复 ----
    var tag = fig ? fig.querySelector('.fig-tag') : null;
    if (tag) tag.dataset.base = tag.textContent;

    var doneBar = document.createElement('div');
    doneBar.className = 'fig-done';
    var fdLabel = document.createElement('span');
    fdLabel.className = 'fd-label';
    fdLabel.textContent = {json.dumps(finalized, ensure_ascii=False)};
    var redoBtn = document.createElement('button');
    redoBtn.className = 'fe-redo';
    redoBtn.type = 'button';
    redoBtn.textContent = {json.dumps(redo_btn, ensure_ascii=False)};
    doneBar.appendChild(fdLabel);
    doneBar.appendChild(redoBtn);
    panel.insertAdjacentElement('afterend', doneBar);

    var btn = document.createElement('button');
    btn.className = 'fe-confirm';
    btn.type = 'button';
    btn.textContent = {json.dumps(confirm_btn, ensure_ascii=False)};
    btn.addEventListener('click', function() {{
      if (fig) fig.classList.add('fig-locked');
      if (tag) tag.textContent = tag.dataset.base + ' · {finalized}';
      panel.style.display = 'none';
      doneBar.style.display = 'flex';
    }});
    panel.appendChild(btn);

    redoBtn.addEventListener('click', function() {{
      if (fig) fig.classList.remove('fig-locked');
      if (tag) tag.textContent = tag.dataset.base;
      doneBar.style.display = 'none';
      panel.style.display = '';
    }});
  }});
}})();"""


def _parse_formats(raw: str) -> list:
    """解析 --format，支持 html|docx|pptx|all 的逗号分隔列表。"""
    s = (raw or 'html').strip().lower()
    if s == 'all':
        return ['html', 'docx', 'pptx']
    items = [x.strip() for x in s.split(',') if x.strip()]
    valid = {'html', 'docx', 'pptx'}
    bad = [x for x in items if x not in valid]
    if bad:
        _spec_error(f"--format 包含未知值: {bad}",
                    f'只接受 {sorted(valid)} 或 all，逗号分隔',
                    {'given': raw, 'unknown': bad})
        raise SystemExit(1)
    if 'html' not in items:
        items = ['html'] + items  # HTML 总是产出
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x); out.append(x)
    return out


def assemble(ns) -> dict:
    formats = _parse_formats(ns.formats)

    spec_path = Path(ns.spec).expanduser()
    if not spec_path.is_file():
        _spec_error(f'report_spec 文件不存在: {ns.spec}',
                    '检查 --spec 路径；spec 是 Step 6 由 agent 写出的 JSON 文件',
                    {'given': ns.spec})
        raise SystemExit(1)
    try:
        spec = json.loads(spec_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        _spec_error(f'report_spec 不是合法 JSON: {e}',
                    '用 json.dumps 生成 spec（ensure_ascii=False），避免手写拼接',
                    {'given': ns.spec})
        raise SystemExit(1)

    # --- spec 校验 ---
    title = str(spec.get('title') or '').strip()
    sections = spec.get('sections')
    if not title:
        _spec_error('report_spec 缺少 title', 'title 必填：结论式主标题，数字取自事实台账')
        raise SystemExit(1)
    if not isinstance(sections, list) or not sections:
        _spec_error('report_spec 缺少 sections（或为空数组）',
                    'sections 至少 1 节；每节含 id/title/narrative，chart_path 可为 null（纯文字节）')
        raise SystemExit(1)

    theme_name = spec.get('theme') or 'default'
    if theme_name not in THEMES:
        _spec_error(f'未知主题: {theme_name!r}',
                    'theme 取 default / classic / dark，且须与图表生成阶段（--theme）一致')
        raise SystemExit(1)
    shell = REPORT_SHELL[theme_name]

    seen_ids = set()
    normalized = []
    for idx, sec in enumerate(sections):
        if not isinstance(sec, dict) or not str(sec.get('title') or '').strip():
            _spec_error(f'sections 第 {idx} 项缺少 title 或不是对象',
                        '每节必须含非空 title（结论式标题）；参考 references/REPORT.md 的 spec 规范')
            raise SystemExit(1)
        sid = _safe_section_id(sec.get('id') or '', idx)
        while sid in seen_ids:
            sid = f'{sid}-{idx}'
        seen_ids.add(sid)
        normalized.append({
            'id': sid,
            'title': str(sec['title']).strip(),
            'narrative': sec.get('narrative') or '',
            'chart_path': sec.get('chart_path'),
            'annotation': sec.get('annotation') or '',
        })

    # --- 事实台账加载 + 模式分发 ---
    resolver: LedgerResolver | None = None
    if ns.ledger:
        try:
            resolver = LedgerResolver.load(ns.ledger)
        except LedgerError as e:
            _emit_error(e.code, e.code_name, e.message, '见 details', e.details)
            raise SystemExit(1)

    # --- 论点台账加载 + 形式校验（论点 → 论据链，改进方案 改进 3）---
    # 形式校验（机械可判定）：论点必有论据、论据可解析（ledger 事实 id / 含图章节 id /
    # 图表文件 stem）、论点文本数字可溯源；coverage 级另要求每张图被至少一个论点引用。
    # 实质校验（论据是否真支撑论点）是 LLM 职责，代码不做。
    claims_resolver: ClaimsResolver | None = None
    claims_stat: dict | None = None
    if ns.claims:
        section_ids = {s['id'] for s in normalized} | {'summary'}
        charted_section_ids = {s['id'] for s in normalized if s['chart_path']}
        chart_stems = {Path(str(s['chart_path'])).stem for s in normalized if s['chart_path']}
        narrative_section_ids = {s['id'] for s in normalized if (s.get('narrative') or '').strip()}
        try:
            claims_resolver = ClaimsResolver.load(ns.claims)
            claims_stat = validate_claims(
                claims_resolver, resolver, section_ids,
                charted_section_ids, chart_stems, mode=ns.claims_check,
                narrative_section_ids=narrative_section_ids)
        except LedgerError as e:
            _emit_error(e.code, e.code_name, e.message,
                        '按 details.violations 修正 claims.json 后重试', e.details)
            raise SystemExit(1)

    # placeholder 模式：先替换（错误早抛），再扫残留裸数字
    if resolver is not None and ns.ledger_mode == 'placeholder':
        try:
            spec, normalized = _apply_placeholder_substitution(spec, normalized, resolver)
            # 替换后用同一 _verify_ledger 入口走 placeholder 分支
            ledger_stat = _verify_ledger(ns, spec, normalized, resolver)
        except LedgerError as e:
            _emit_error(e.code, e.code_name, e.message,
                        '修正占位符写法或补齐 ledger.json 后重试', e.details)
            raise SystemExit(1)
    elif resolver is not None and ns.ledger_mode == 'scan':
        ledger_stat = _verify_ledger(ns, spec, normalized, resolver)
    else:
        ledger_stat = None

    # placeholder 替换会生成新 spec；封面标题等一律以替换后的 spec 为准
    title = str(spec.get('title') or title).strip()

    # --- 图表提取 ---
    spec_dir = spec_path.resolve().parent
    charts_dir = Path(ns.charts_dir).expanduser() if ns.charts_dir else spec_dir
    payloads = {}
    plugins_needed = set()
    charts_count = 0
    for sec in normalized:
        if not sec['chart_path']:
            continue
        src = _resolve_chart_path(str(sec['chart_path']), charts_dir, spec_dir)
        if src is None:
            _spec_error(f'章节 {sec["id"]} 的 chart_path 找不到文件: {sec["chart_path"]}',
                        'chart_path 相对 --charts-dir 解析；也可传绝对路径。'
                        '先用 cli.py --charts-file 批量生成，再把 stdout 的 html_path 填入 spec',
                        {'section': sec['id'], 'given': str(sec['chart_path']),
                         'charts_dir': str(charts_dir)})
            raise SystemExit(1)
        try:
            html_text = src.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as e:
            _emit_error(_CHART_HTML_INVALID, 'CHART_HTML_INVALID',
                        f'读取图表 HTML 失败: {src} ({e})',
                        '确认文件存在且为 UTF-8 编码的图表 HTML',
                        {'given': str(src)})
            raise SystemExit(1)
        payload = _extract_chart_payload(html_text, src)
        if payload['kind'] == 'echarts' and resolver is not None and ns.ledger_mode == 'placeholder':
            # P1-9/10：图表内文字（title 等）纳入台账溯源，{{id}} 回写为真实数字
            try:
                payload['option_js'] = resolver.resolve_text(payload['option_js'], f"{sec['id']}.chart")
            except LedgerError as e:
                _emit_error(e.code, e.code_name, e.message,
                            '修正图表内 {{id}} 占位符写法或补齐 ledger.json 后重试', e.details)
                raise SystemExit(1)
        payloads[sec['id']] = payload
        if payload['kind'] == 'echarts':
            plugins_needed |= payload['plugins']
        charts_count += 1

    # --- 报告 HTML ---
    has_echarts = any(pl['kind'] == 'echarts' for pl in payloads.values())
    echarts_js = ''
    plugin_js = ''
    if has_echarts:
        echarts_js = (_STATIC_DIR / 'echarts.min.js').read_text(encoding='utf-8')
        if 'wordcloud' in plugins_needed:
            plugin_js += (_STATIC_DIR / 'echarts-wordcloud.min.js').read_text(encoding='utf-8')
        if 'liquidfill' in plugins_needed:
            plugin_js += (_STATIC_DIR / 'echarts-liquidfill.min.js').read_text(encoding='utf-8')
    head_scripts = ''
    if has_echarts:
        head_scripts = f'<script>{echarts_js}</script>'
        if plugin_js:
            head_scripts += f'\n<script>{plugin_js}</script>'

    esc_title = html_module.escape(title)
    subtitle = str(spec.get('subtitle') or '').strip()
    esc_subtitle = html_module.escape(subtitle)
    summary = spec.get('executive_summary') or ''
    appendix = spec.get('appendix') or {}
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    ghost = _ghost_text(title, subtitle)
    css = _build_css(shell)

    # --- 目录（摘要 + 编号章节 + 附录 + 台账溯源） ---
    toc_rows = []
    if str(summary).strip():
        toc_rows.append(('<span class="toc-num">§</span>', '摘要', '#summary'))
    for i, s in enumerate(normalized):
        toc_rows.append((f'<span class="toc-num">{i + 1:02d}</span>',
                         html_module.escape(s['title']), f'#{s["id"]}'))
    appendix_bits = []
    if str(appendix.get('methodology') or '').strip():
        appendix_bits.append(('数据与方法', appendix['methodology']))
    if str(appendix.get('caveats') or '').strip():
        appendix_bits.append(('口径与局限', appendix['caveats']))
    if appendix_bits:
        toc_rows.append(('<span class="toc-num">A</span>', '附录', '#appendix'))
    if resolver is not None and resolver.entries:
        toc_rows.append(('<span class="toc-num">L</span>', '关键数据溯源', '#ledger-appendix'))
    if claims_resolver is not None and claims_resolver.claims:
        toc_rows.append(('<span class="toc-num">C</span>', '论点与论据', '#claims-appendix'))
    toc_items = ''.join(
        f'<a class="toc-item" href="{href}">{num}'
        f'<span class="toc-title">{label}</span><span class="toc-line"></span></a>'
        for num, label, href in toc_rows
    )

    # --- 章节（正文节编号 01..，图编号 图1..） ---
    section_html = []
    fig_idx = 0
    for i, s in enumerate(normalized):
        chart_block = ''
        payload = payloads.get(s['id'])
        if payload:
            fig_idx += 1
            if payload['kind'] == 'echarts':
                min_w = f'; min-width: {payload["min_width"]}px' if payload['min_width'] else ''
                chart_block = (
                    f'<figure class="fig"><span class="fig-tag">图 {fig_idx}</span>'
                    f'<div class="chart-scroll"><div id="chart-{s["id"]}" '
                    f'class="chart-canvas" style="aspect-ratio: {payload["aspect"]:.4f};{min_w}">'
                    f'</div></div>'
                    f'<div class="fig-edit" id="fedit-{s["id"]}"></div>'
                    f'</figure>'
                )
            else:
                chart_block = (
                    f'<figure class="fig"><span class="fig-tag">图 {fig_idx}</span>'
                    f'<div class="table-box">{payload["table_html"]}</div></figure>'
                )
        ann = ''
        if s['annotation']:
            ann = (f'<div class="annotation"><span class="ann-tag">图注</span>'
                   f'<div>{_paras(s["annotation"])}</div></div>')
        section_html.append(
            f'<section id="{s["id"]}" class="card section">\n'
            f'<div class="sec-head"><span class="sec-num">{i + 1:02d}</span>'
            f'<h2>{html_module.escape(s["title"])}</h2></div>\n'
            f'<div class="sec-rule"><i></i></div>\n'
            f'{_paras(s["narrative"])}\n{chart_block}\n{ann}\n</section>'
        )

    # --- 摘要 / 附录 / 台账溯源 ---
    summary_html = ''
    if str(summary).strip():
        summary_html = (
            '<section id="summary" class="card section summary">\n'
            f'<div class="block-label">执行摘要</div>\n{_paras(summary)}\n</section>'
        )
    appendix_html = ''
    if appendix_bits:
        parts = ''.join(
            f'<h3>{label}</h3>\n{_paras(text)}' for label, text in appendix_bits
        )
        appendix_html = (
            '<section id="appendix" class="card section appendix">\n'
            '<div class="sec-head"><span class="sec-num">A</span><h2>附录</h2></div>\n'
            f'<div class="sec-rule"><i></i></div>\n{parts}\n</section>'
        )
    ledger_html = _ledger_appendix_html(resolver) if resolver else ''
    claims_html = _claims_appendix_html(claims_resolver)

    # --- 图表 init 脚本 ---
    opt_lines = [f'  {json.dumps(s_id)}: {payloads[s_id]["option_js"]}'
                 for s_id, pl in payloads.items() if pl['kind'] == 'echarts']
    init_js = ''
    if opt_lines:
        init_js = (
            'var __SR_OPTIONS = {\n' + ',\n'.join(opt_lines) + '\n};\n'
            + _build_init_js()
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc_title}</title>
{head_scripts}
<style>{css}</style>
</head>
<body>
<div class="wrap">
  <header class="card cover">
    <div class="brand-row">
      <span class="brand">SMART REPORT</span>
      <span class="brand-sub">数据报告</span>
      <span class="brand-rule"></span>
    </div>
    <h1 class="cover-title">{esc_title}</h1>
    <p class="cover-sub">{esc_subtitle}</p>
    <div class="cover-meta">
      <span><b>{len(normalized)}</b>&nbsp;章</span>
      <span><b>{charts_count}</b>&nbsp;图</span>
      <span>{now}</span>
    </div>
    <div class="cover-ghost">{ghost}</div>
  </header>
  <nav class="card toc">
    <div class="block-label">目录</div>
    {toc_items}
  </nav>
  {summary_html}
  {''.join(section_html)}
  {appendix_html}
  {ledger_html}
  {claims_html}
  <footer class="report-footer">SMART REPORT &middot; 由 SMART CHARTS 引擎驱动 &middot; ECHARTS 离线渲染</footer>
</div>
<script>
{init_js}
</script>
</body>
</html>"""

    out_path = Path(ns.output).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')

    report = {
        'success': True,
        'report_path': str(out_path.resolve()),
        'sections_count': len(normalized),
        'charts_count': charts_count,
        'theme': theme_name,
        'formats': formats,
    }
    if ledger_stat is not None:
        report['ledger'] = ledger_stat
    if claims_stat is not None:
        report['claims'] = claims_stat

    # --- 多格式导出（docx / pptx） ---
    export_artifacts: dict = {}
    export_errors: dict = {}
    non_html_formats = [f for f in formats if f != 'html']
    if non_html_formats:
        skill_root = Path(__file__).resolve().parent.parent
        export_root = Path(ns.export_dir).expanduser() if ns.export_dir \
            else out_path.parent / (out_path.stem + '_assets')
        export_root.mkdir(parents=True, exist_ok=True)
        svg_dir = export_root / 'svg'
        png_dir = export_root / 'png'
        manifest = _build_export_manifest(payloads, theme_name)
        if manifest:
            ok, items, err_tail = _run_node_export(skill_root, manifest, svg_dir)
            if not ok and not items:
                # node 子进程全失败 → 所有非 html 格式都报 5006
                for fmt in non_html_formats:
                    export_errors[fmt] = f"node SSR 失败: {err_tail or '未知错误'}"
            else:
                # P0-4：SSR/rasterize 逐图对账，任一图失败必须在 export_errors 点名 section_id
                expected_sids = [m['id'] for m in manifest]
                ssr_failed = sorted(it.get('id') for it in items if not it.get('success'))
                png_map = _rasterize_svgs(svg_dir, png_dir)
                chart_pngs: dict[str, str] = {sid: p for sid, p in png_map.items() if p}
                raster_failed = sorted(sid for sid, p in png_map.items() if not p)
                missing = sorted(sid for sid in expected_sids if sid not in chart_pngs)
                if missing:
                    detail = []
                    if ssr_failed:
                        detail.append(f"SSR 失败章节: {', '.join(ssr_failed)}")
                    if raster_failed:
                        detail.append(f"光栅化失败章节: {', '.join(raster_failed)}")
                    export_errors['partial'] = (
                        f"导出图片数 {len(chart_pngs)} < 含图章节数 {len(expected_sids)}"
                        + ("；" + "；".join(detail) if detail else "")
                    )
                # spreadsheet 表格不进 png_map，docx/pptx builder 按 payload 自行处理
                for sec in normalized:
                    sid = sec['id']
                    pl = payloads.get(sid)
                    if pl and pl['kind'] == 'table' and sid not in chart_pngs:
                        # docx/pptx 直接消费 payload['table_html']
                        pass

                # 输出路径：派生自 --output 同 stem
                stem = out_path.stem
                if 'docx' in non_html_formats:
                    try:
                        from scripts.docx_export import build_docx
                        docx_path = build_docx(spec, normalized, chart_pngs, resolver,
                                               str(out_path.with_suffix('.docx')))
                        export_artifacts['docx'] = str(docx_path.resolve())
                    except Exception as e:
                        export_errors['docx'] = f'{type(e).__name__}: {e}'[:300]
                if 'pptx' in non_html_formats:
                    try:
                        from scripts.pptx_export import build_pptx
                        pptx_path = build_pptx(spec, normalized, chart_pngs, resolver,
                                               str(out_path.with_suffix('.pptx')))
                        export_artifacts['pptx'] = str(pptx_path.resolve())
                    except Exception as e:
                        export_errors['pptx'] = f'{type(e).__name__}: {e}'[:300]
        else:
            for fmt in non_html_formats:
                export_errors[fmt] = '无可导出的 ECharts 图表（仅 spreadsheet 或全纯文字节）'

    if export_artifacts:
        report['exports'] = export_artifacts
    if export_errors:
        report['export_errors'] = export_errors

    return {'report': report}


def main():
    ns = build_parser().parse_args()
    try:
        result = assemble(ns)
        print(json.dumps(result, ensure_ascii=False))
        # 仅当 HTML 失败时已抛 SystemExit；exports 部分失败只放进 stdout 的 export_errors，不阻断 0 退出
    except SystemExit:
        raise
    except SmartChartsError as e:
        _emit_error(_REPORT_ASSEMBLE_ERROR, 'REPORT_ASSEMBLE_ERROR',
                    f'报告组装失败: {e.message}', '按 details.suggestion 修正 spec 后重试',
                    e.details)
        raise SystemExit(1)
    except Exception as e:  # 兜底：未知异常也走结构化 JSON
        _emit_error(_REPORT_ASSEMBLE_ERROR, 'REPORT_ASSEMBLE_ERROR',
                    f'报告组装未捕获异常: {e}',
                    '把完整 stderr JSON 反馈给维护者排查',
                    {'type': type(e).__name__})
        raise SystemExit(1)


if __name__ == '__main__':
    main()
