#!/usr/bin/env python3
"""Extract original figure references, URLs, and presentation-ready Chinese explanations.

Policy:
- Prefer original figure caption content.
- Convert English caption fragments into concise Chinese presentation notes.
- Use matching Results subsection mainly for title mapping and minimal contextual补充.
- Keep explanations close to the paper wording instead of over-interpreting.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

FIG_PAT = re.compile(
    r"(?:^|\n)\s*(?:!\[\]\((?P<url>https?://[^\)]+)\)\s*)?"
    r"(?P<label>Fig\.?|Figure|Table)\s*(?P<num>\d+[A-Za-z]?)\.?(?P<rest>.*?)"
    r"(?=(?:\n\s*!\[\]\(|\n\s*(?:Fig\.?|Figure|Table)\s*\d+[A-Za-z]?\.?|\Z))",
    re.I | re.S,
)
RESULTS_SECTION_PAT = re.compile(r"#\s*3\.[\s\S]+?(?=#\s*4\.|\Z)", re.I)
RESULT_SUBSECTION_PAT = re.compile(
    r"#\s*3\.(?P<num>\d+)\.\s*(?P<title>.+?)\n(?P<body>[\s\S]*?)(?=(?:#\s*3\.\d+\.|#\s*4\.|\Z))",
    re.I,
)


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str) -> Any:
    return json.loads(read_text(path))


def clean(s: str) -> str:
    s = s or ""
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\[A-Za-z]+\s*", " ", s)
    s = re.sub(r"\{[^{}]*\}", " ", s)
    s = re.sub(r"\[[0-9,–\- ]+\]", " ", s)
    s = re.sub(r"\(\s*[^()]*?(?:USA|UK|China|Abcam|Cell Signaling|Invitrogen|MilliporeSigma|Sigma|Thermo Fisher)[^()]*\)", " ", s, flags=re.I)
    s = re.sub(r"#\s*\d+(?:\.\d+)?\.? .*", " ", s)
    s = re.sub(r"#\s*\d+(?:\.\d+)?\.?.*", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def truncate_caption(s: str, max_len: int = 360) -> str:
    s = clean(s)
    if len(s) <= max_len:
        return s
    cut = s[:max_len]
    for sep in ['. ', '。']:
        if sep in cut:
            cut = cut[:cut.rfind(sep) + 1]
    return cut.strip()


def get_results_subsections(md: str) -> Dict[str, Dict[str, str]]:
    m = RESULTS_SECTION_PAT.search(md)
    text = m.group(0) if m else md
    out: Dict[str, Dict[str, str]] = {}
    for sm in RESULT_SUBSECTION_PAT.finditer(text):
        out[sm.group('num')] = {
            'title': clean(sm.group('title')),
            'body': clean(sm.group('body')),
        }
    return out


def infer_result_section(fig_num: str, results_map: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    fig_num_plain = re.sub(r'[^0-9]', '', str(fig_num))
    if not fig_num_plain:
        return {}
    direct_patterns = [
        rf"\bFig\.?\s*{fig_num_plain}(?:[A-Z]|\b)",
        rf"\bFigure\s*{fig_num_plain}(?:[A-Z]|\b)",
    ]
    for _, sec in results_map.items():
        body = sec.get('body', '')
        if any(re.search(p, body, re.I) for p in direct_patterns):
            return sec
    return results_map.get(fig_num_plain, {})


def zh_title(text: str) -> str:
    text = clean(text)
    if not text:
        return ''
    mapping = [
        (r'learning and memory|behavioral deficits|cognitive function', '行为学与认知功能改善'),
        (r'lymphocyte infiltration', '脑内淋巴细胞浸润减少'),
        (r'proteomic', '蛋白组学提示 AD 相关通路被抑制'),
        (r'amyloid|brain deposition', 'Aβ/淀粉样病理减轻'),
        (r'tau', 'Tau 病理缓解'),
        (r'inflammation', '神经炎症减轻'),
        (r'neurodegeneration|synaptic|neuronal networks', '神经元与突触损伤改善'),
        (r'mechanism', '机制总结'),
    ]
    lower = text.lower()
    for pat, rep in mapping:
        if re.search(pat, lower):
            return rep
    return text


def normalize_en_fragment(text: str) -> str:
    text = clean(text)
    if not text:
        return ''
    text = re.sub(r'^[A-Z]\s*[\.,:]\s*', '', text)
    text = re.sub(r'\b(?:representative|tracing graph|images?|photographs?)\b', ' ', text, flags=re.I)
    text = re.sub(r'\b(?:using|used to|after treatment|in the brains? of|in brains? of|in mouse brain|of APP/PS1 mice|of mice|in APP/PS1 mice)\b', ' ', text, flags=re.I)
    text = re.sub(r'\s+', ' ', text).strip(' ,;:.')
    return text


def title_to_cn(text: str) -> str:
    t = clean(text).lower()
    mapping = [
        (r'behavioral deficits|learning and memory|cognitive function', '行为学与认知功能改善'),
        (r'lymphocyte infiltration', '脑内淋巴细胞浸润减少'),
        (r'proteomic', '蛋白组学提示 AD 相关通路被抑制'),
        (r'brain deposition|amyloid', 'Aβ 沉积减轻'),
        (r'tau hyperphosphorylation|tau', 'Tau 过磷酸化减轻'),
        (r'neuroinflammation', '神经炎症减轻'),
        (r'integrity of neuronal networks|neurodegeneration|synaptic', '神经元与突触损伤改善'),
    ]
    for pat, rep in mapping:
        if re.search(pat, t):
            return rep
    return zh_title(text) or clean(text)


METHOD_HINTS = [
    (r'morris water maze', '采用 Morris 水迷宫评估学习记忆'),
    (r'open field', '采用开放场实验评估自主活动'),
    (r'y-?maze', '采用 Y 迷宫评估空间工作记忆'),
    (r'flow cytometry', '采用流式细胞术检测相关细胞群'),
    (r'western blot', '采用 Western blot 检测相关蛋白表达'),
    (r'immunohistochemical|immunohistochemistry', '采用免疫组化评估病理变化'),
    (r'immunofluorescence', '采用免疫荧光评估组织信号变化'),
    (r'elisa', '采用 ELISA 检测相关分子水平'),
    (r'proteomic|gsea|kegg|go analysis', '结合蛋白组学与通路分析评估整体分子变化'),
]

OBS_HINTS = [
    (r'behavioral deficits|learning and memory|cognitive function', '结果提示芬戈莫德可改善 APP/PS1 小鼠的学习记忆与认知表现'),
    (r'b lymphocytes|t lymphocytes|lymphocyte infiltration', '结果提示芬戈莫德减少外周淋巴细胞向脑内浸润'),
    (r'proteomic|downregulation of proteins|ad-associated pathways', '结果提示多条 AD 与免疫相关通路整体下调'),
    (r'amyloid|6e10|thioflavin|congo red|aβ40|aβ42|deposition', '结果提示脑内 Aβ 斑块负荷及淀粉样沉积下降'),
    (r'bace1|ctf-β|ctf-α|app metabolites|amyloidopathogenic', '结果提示 APP 加工偏向非淀粉样途径，Aβ 生成受到抑制'),
    (r'tau hyperphosphorylation|pt231|ser404|thr231|ser199|thr181', '结果提示 Tau 过磷酸化水平下降'),
    (r'gfap|cd68|tnf-α|tnf-alpha|neuroinflammation', '结果提示胶质活化和炎症水平下降'),
    (r'map2|caspase-3|neun|vamp1|snap25|psd95|psd93|neuronal networks', '结果提示神经元损伤、凋亡和突触损害得到缓解'),
]


def infer_method_text(*texts: str) -> str:
    blob = ' '.join(clean(t).lower() for t in texts if t)
    for pat, rep in METHOD_HINTS:
        if re.search(pat, blob):
            return rep
    return '该图展示作者用于验证该结论的关键实验结果'


def infer_observation_text(*texts: str) -> str:
    blob = ' '.join(clean(t).lower() for t in texts if t)
    for pat, rep in OBS_HINTS:
        if re.search(pat, blob):
            return rep
    return '图中比较了给药组与对照组的关键差异，并支持该部分核心结论'


def split_sentences(text: str) -> List[str]:
    text = clean(text)
    if not text:
        return []
    parts = re.split(r'(?<=[\.;])\s+|(?<=。)|(?<=；)', text)
    return [clean(p).strip('.;') for p in parts if clean(p)]


def zh_explain(caption: str, ref: str, result_title: str = '', result_body: str = '') -> List[str]:
    caption = normalize_en_fragment(caption)
    result_title = clean(result_title)
    result_body = normalize_en_fragment(result_body)
    points: List[str] = []

    module_cn = title_to_cn(result_title) if result_title else ''
    if module_cn:
        points.append(f'对应结果模块：{module_cn}。')

    points.append(f'实验信息：{infer_method_text(caption, result_body, result_title)}。')
    points.append(f'主要结果：{infer_observation_text(caption, result_body, result_title)}。')

    if result_body:
        short_body = truncate_caption(result_body, max_len=90)
        points.append(f'结果解读：该图与正文结果一致，支持作者在本节提出的核心结论。')
    else:
        points.append('结果解读：该图用于支撑本节核心结论，并与全文证据链保持一致。')

    cleaned = []
    for p in points:
        p = re.sub(r'\s+', ' ', p).strip()
        p = re.sub(r'。+', '。', p)
        p = re.sub(r'：\s*。', '：', p)
        if p and p not in cleaned:
            cleaned.append(p)
    return cleaned[:4]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--fulltext', required=True)
    ap.add_argument('--figures', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    md = read_text(args.fulltext)
    figures = read_json(args.figures)
    results_map = get_results_subsections(md)

    by_url: Dict[str, Dict[str, Any]] = {}
    for f in figures:
        if isinstance(f, dict) and f.get('url'):
            by_url[f['url']] = dict(f)

    found: List[Dict[str, Any]] = []
    used_urls = set()

    for m in FIG_PAT.finditer(md):
        url = m.group('url')
        num = m.group('num')
        raw_rest = m.group('rest') or ''
        ref = f"Figure {num}" if m.group('label').lower().startswith(('fig', 'figure')) else f"Table {num}"
        item = None
        if url and url in by_url:
            item = dict(by_url[url])
            used_urls.add(url)
        else:
            for f in figures:
                if isinstance(f, dict) and clean(str(f.get('figure_ref', ''))).lower() == ref.lower():
                    item = dict(f)
                    break
        if not item:
            continue

        result_ctx = infer_result_section(str(num), results_map)
        result_title = result_ctx.get('title', '')
        result_body = result_ctx.get('body', '')
        item['figure_ref'] = item.get('figure_ref') or ref
        item['original_caption'] = truncate_caption(raw_rest)
        item['evidence_snippet'] = truncate_caption(result_body or raw_rest, max_len=420)
        item['matched_result_title'] = result_title
        item['matched_result_title_zh'] = zh_title(result_title)
        item['matched_result_snippet'] = truncate_caption(result_body, max_len=420)
        item['explanation_points'] = zh_explain(raw_rest, item['figure_ref'], result_title, result_body)
        item['explanation_cn'] = '；'.join(item['explanation_points'])
        found.append(item)

    for f in figures:
        if not isinstance(f, dict):
            continue
        url = f.get('url')
        if url and url in used_urls:
            continue
        found.append({
            **f,
            'original_caption': '',
            'evidence_snippet': '',
            'matched_result_title': '',
            'matched_result_title_zh': '',
            'matched_result_snippet': '',
            'explanation_points': [],
            'explanation_cn': ''
        })

    Path(args.output).write_text(json.dumps(found, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
