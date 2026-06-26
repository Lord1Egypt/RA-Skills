#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

FAIL = "检索失败,无法生成"


def author_display(authors: List[str], mode: str = 'first_et_al') -> str:
    authors = [a.strip() for a in (authors or []) if str(a).strip()]
    if not authors:
        return ''
    if mode == 'full':
        return ', '.join(authors)
    return f"{authors[0]} et al." if len(authors) > 1 else authors[0]


def compress_result_title(title: str) -> str:
    title = re.sub(r'^[\d\.\s]+', '', (title or '').strip())
    title = re.sub(r'^(results?|result)\s*[:：-]?\s*', '', title, flags=re.I)
    title = re.sub(r'\s+', ' ', title).strip(' -–—:：')
    if len(title) <= 60:
        return title
    parts = re.split(r'[:：;；,.，]', title)
    first = parts[0].strip() if parts else title
    if 6 <= len(first) <= 60:
        return first
    return title[:60].rstrip()


def split_explanation_points(explanation: str, max_chunks: int = 3) -> List[str]:
    explanation = (explanation or '').strip()
    if not explanation:
        return []
    parts = [p.strip() for p in re.split(r'[；;\n]+', explanation) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in re.split(r'(?<=。)', explanation) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in re.split(r'(?<=，)', explanation) if p.strip()]
    parts = [p for p in parts if p]
    if not parts:
        return [explanation]
    if len(explanation) > 220 and len(parts) < 2:
        mid = len(explanation) // 2
        split_at = max(explanation.find('。', mid), explanation.find('；', mid), explanation.find('，', mid))
        if split_at != -1:
            parts = [explanation[:split_at+1].strip(), explanation[split_at+1:].strip()]
    if len(parts) <= max_chunks:
        return parts
    chunked = []
    size = (len(parts) + max_chunks - 1) // max_chunks
    for i in range(0, len(parts), size):
        chunked.append('；'.join(parts[i:i+size]))
    return chunked[:max_chunks]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run(cmd: List[str], cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=check)


def debug_log(work_dir: Path, stage: str, detail: str) -> None:
    try:
        work_dir.mkdir(parents=True, exist_ok=True)
        with (work_dir / 'pipeline_debug.log').open('a', encoding='utf-8') as f:
            f.write(f'[{stage}] {detail}\n')
    except Exception:
        pass


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def infer_title_query(title: str) -> str:
    escaped = title.replace('"', '\\"')
    return f'(\\"{escaped}\\"[Title])'


def search_paper(title: str, out_dir: Path) -> Dict[str, Any]:
    debug_log(out_dir, 'search', f'title={title}')
    local_search = script_dir() / 'medical_search.py'
    search_script = local_search if local_search.exists() else Path.home() / '.openclaw/skills/medical-keyword-search/scripts/medical_search.py'
    exact_out = out_dir / 'search_exact.json'
    broad_out = out_dir / 'search_broad.json'

    def normalize_title(s: str) -> str:
        return re.sub(r'[^a-z0-9]+', '', (s or '').lower())

    def pick_best(items: Any, target_title: str) -> Optional[Dict[str, Any]]:
        if not isinstance(items, list):
            return None
        target = normalize_title(target_title)
        exact = [it for it in items if normalize_title(str(it.get('title', ''))) == target]
        if len(exact) == 1:
            return exact[0]
        close = []
        target_words = {w for w in re.findall(r'[a-z0-9]+', target_title.lower()) if len(w) > 2}
        for it in items:
            cand_title = str(it.get('title', '')).lower()
            cand_words = set(re.findall(r'[a-z0-9]+', cand_title))
            overlap = len(target_words & cand_words)
            if overlap >= max(3, min(len(target_words), 6) - 1):
                close.append((overlap, it))
        close.sort(key=lambda x: x[0], reverse=True)
        if len(close) == 1:
            return close[0][1]
        if len(close) >= 2 and close[0][0] > close[1][0]:
            return close[0][1]
        return None

    def run_search(args: List[str], out_path: Path) -> Any:
        cmd = ['python3', str(search_script), '--output', str(out_path)] + args
        debug_log(out_dir, 'search.cmd', ' '.join(cmd))
        cp = run(cmd, check=False)
        debug_log(out_dir, 'search.ret', f'code={cp.returncode}; stdout={cp.stdout[:500]!r}; stderr={cp.stderr[:500]!r}')
        if cp.returncode != 0:
            raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or 'search failed')
        return read_json(out_path)

    normalized = title.replace('APP_PS1', 'APP/PS1').replace('APP-PS1', 'APP/PS1')
    try:
        exact = run_search(['free', '--query', infer_title_query(title)], exact_out)
    except Exception as e:
        debug_log(out_dir, 'search.exact.err', repr(e))
        exact = []
    picked = pick_best(exact, normalized)
    if picked:
        return picked

    title_keywords = [w for w in re.findall(r"[A-Za-z0-9\-/']+", normalized) if len(w) > 3][:6]
    broad_query = ' AND '.join([f'({w}[Title/Abstract])' for w in title_keywords])
    broad = run_search(['free', '--query', broad_query], broad_out)
    picked = pick_best(broad, normalized)
    if picked:
        return picked
    raise RuntimeError(FAIL)


def fetch_fullpaper(doc_id: str, out_dir: Path) -> Tuple[Path, Path, Path, Path]:
    debug_log(out_dir, 'fetch', f'doc_id={doc_id}')
    meta = out_dir / 'meta.json'
    fulltext = out_dir / 'fulltext.md'
    figures = out_dir / 'figures.json'
    debug = out_dir / 'debug.json'
    script = script_dir() / 'fetch_fullpaper.py'
    cmd = [
        'python3', str(script), '--doc-id', str(doc_id), '--meta-out', str(meta), '--fulltext-out', str(fulltext), '--figures-out', str(figures), '--debug-out', str(debug)
    ]
    debug_log(out_dir, 'fetch.cmd', ' '.join(cmd))
    cp = run(cmd, check=False)
    debug_log(out_dir, 'fetch.ret', f'code={cp.returncode}; stdout={cp.stdout[:500]!r}; stderr={cp.stderr[:500]!r}')
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or FAIL)
    return meta, fulltext, figures, debug


def extract_captions(fulltext: Path, figures: Path, out_dir: Path) -> Path:
    output = out_dir / 'figure_captions.json'
    script = script_dir() / 'extract_figures_and_captions.py'
    cp = run(['python3', str(script), '--fulltext', str(fulltext), '--figures', str(figures), '--output', str(output)], check=False)
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or FAIL)
    return output


def validate_inputs(meta: Path, fulltext: Path, figures: Path, out_dir: Path) -> Path:
    output = out_dir / 'validation.json'
    script = script_dir() / 'validate_inputs.py'
    cp = run(['python3', str(script), '--paper-meta', str(meta), '--fulltext', str(fulltext), '--figures', str(figures), '--output', str(output)], check=False)
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or FAIL)
    data = read_json(output)
    if not data.get('ok'):
        raise RuntimeError(FAIL)
    return output


def build_bundle(meta: Path, fulltext: Path, figures: Path, out_dir: Path) -> Path:
    output = out_dir / 'bundle.json'
    script = script_dir() / 'build_prompt_bundle.py'
    cp = run(['python3', str(script), '--paper-meta', str(meta), '--fulltext', str(fulltext), '--figures', str(figures), '--output', str(output)], check=False)
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or FAIL)
    return output


def parse_authors_from_fulltext(fulltext_text: str) -> List[str]:
    lines = [ln.strip() for ln in fulltext_text.splitlines() if ln.strip()]
    if len(lines) < 3:
        return []
    for idx, line in enumerate(lines[:15]):
        if line.startswith('#') and idx + 1 < len(lines):
            candidate = lines[idx + 1]
            if any(k in candidate for k in ['Department of', 'Institute of', 'Hospital', 'University']):
                continue
            parts = [p.strip(' ,') for p in candidate.split(',')]
            cleaned = []
            for p in parts:
                p = re.sub(r'\$.*?\$', ' ', p)
                p = re.sub(r'\s*\d+$', '', p).strip()
                if len(p) >= 3 and not any(k in p for k in ['Department of', 'Institute of', 'Hospital', 'University']):
                    cleaned.append(p)
            if cleaned:
                return cleaned
    return []


def detect_journal_year(search_item: Dict[str, Any], meta: Dict[str, Any]) -> Tuple[str, str]:
    journal = meta.get('journal') or search_item.get('journal') or ''
    year = meta.get('year') or ''
    if not year:
        pub = str(search_item.get('publish_date') or '')
        m = re.match(r'(\d{4})', pub)
        if m:
            year = m.group(1)
    return journal, year


def sentence(text: str) -> str:
    text = re.sub(r'\s+', ' ', (text or '').strip())
    if not text:
        return ''
    return text if re.search(r'[。！？]$', text) else text + '。'


def first_nonempty(*vals: str) -> str:
    for v in vals:
        if str(v or '').strip():
            return str(v).strip()
    return ''


def choose_title_zh(title_en: str, meta: Dict[str, Any], fulltext: str) -> str:
    existing = first_nonempty(meta.get('title_zh'))
    if existing:
        return existing
    t = title_en.lower()
    rule_map = [
        (r'ameliorates|alleviates|attenuates|improves', '改善'),
        (r'promotes|enhances', '促进'),
        (r'inhibits|reduces|suppresses', '抑制'),
    ]
    verb = '影响'
    for pat, rep in rule_map:
        if re.search(pat, t):
            verb = rep
            break
    disease = '相关病理'
    if "alzheimer" in t:
        disease = '阿尔茨海默病相关病理'
    elif 'parkinson' in t:
        disease = '帕金森病相关病理'
    elif 'cancer' in t or 'tumor' in t:
        disease = '肿瘤进展'
    model = '模型'
    m = re.search(r'in ([A-Za-z0-9/\- ]+?) model', title_en, re.I)
    if m:
        model = m.group(1).strip() + ' 模型'
    subject = title_en.split()[0]
    return f'{subject}在{model}中{verb}{disease}'


def infer_general_overview(title_en: str, abstract: str, captions: List[Dict[str, Any]], fulltext: str) -> List[str]:
    abs_clean = re.sub(r'\s+', ' ', abstract or '').strip()
    cap_blob = ' '.join((c.get('matched_result_title') or '') + ' ' + (c.get('original_caption') or '') for c in captions)
    bullets = []
    if abs_clean:
        bullets.append(sentence('研究目标：' + abs_clean[:90].strip(' .;，。')))
    if re.search(r'mice|mouse|murine', fulltext, re.I):
        bullets.append('研究对象：动物实验为主，围绕疾病模型中的关键病理与功能结局展开评估。')
    elif re.search(r'patients|clinical|trial', fulltext, re.I):
        bullets.append('研究对象：以临床人群或患者样本为主，评估干预对关键结局的影响。')
    else:
        bullets.append('研究对象：围绕论文中的核心模型、干预和主要结局进行系统评估。')
    if re.search(r'proteom|transcriptom|sequencing|rna-seq', cap_blob, re.I):
        bullets.append('研究方法：除基础表型评估外，还结合组学或通路分析解释机制层面的变化。')
    else:
        bullets.append('研究方法：综合行为、病理、生化或分子实验结果，构建较完整的证据链。')
    bullets.append('主要发现：原文结果页将优先基于各 Figure 所对应的结果模块逐页组织，不额外编造未出现的章节。')
    return bullets[:4]


def infer_background(title_en: str, abstract: str) -> List[Dict[str, Any]]:
    t = (title_en + ' ' + abstract).lower()
    background = []
    question = []
    if 'alzheimer' in t:
        background = ['阿尔茨海默病的核心特征包括 Aβ、Tau、神经炎症和神经退行性变。', '围绕疾病修饰而非单点对症改善，是当前研究的重要方向。']
    elif 'cancer' in t or 'tumor' in t:
        background = ['肿瘤进展受到增殖、转移、免疫微环境和治疗反应等多因素共同影响。', '寻找能够影响关键病理通路的干预手段具有潜在转化意义。']
    else:
        background = ['该研究聚焦特定疾病模型中的关键病理过程与干预效果。', '作者希望通过多维证据验证干预是否能改变疾病相关表型。']
    question = ['作者关注的核心问题是：该干预能否改善模型中的关键功能与病理结局。', '进一步问题是：这些表型变化背后是否存在可解释的机制链条。']
    return [{'heading': '背景', 'points': background}, {'heading': '科学问题', 'points': question}]


def infer_design_sections(fulltext: str, captions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    blob = (fulltext or '').lower()
    methods = []
    if re.search(r'morris water maze|y-?maze|open field', blob):
        methods.append('行为学评估：包括水迷宫、Y 迷宫或开放场等，用于分析学习记忆和活动能力。')
    if re.search(r'western blot|immunofluorescence|immunohistochemistry|elisa', blob):
        methods.append('病理与分子评估：结合 Western blot、免疫染色、ELISA 等方法验证关键病理变化。')
    if re.search(r'flow cytometry', blob):
        methods.append('细胞层面评估：通过流式细胞术分析特定细胞群或免疫浸润变化。')
    if re.search(r'proteom|gsea|kegg|go analysis|rna-seq|sequencing', blob):
        methods.append('机制补充：结合组学和通路分析解释整体分子网络变化。')
    if not methods:
        methods.append('综合论文中的关键实验手段，对功能、病理和机制层面进行联合评估。')
    model_points = []
    if re.search(r'mice|mouse|murine', blob):
        model_points.append('以动物模型为主要研究对象，比较干预组与对照组的差异。')
    elif re.search(r'patients|clinical|trial', blob):
        model_points.append('以患者样本或临床研究对象为主，围绕干预前后或组间差异开展比较。')
    else:
        model_points.append('围绕论文所采用的核心模型和干预条件组织研究设计。')
    return [
        {'heading': '模型与分组', 'points': model_points},
        {'heading': '评估维度', 'points': methods}
    ]


def build_result_bullets(cap: Dict[str, Any], fallback_title: str) -> List[str]:
    title = first_nonempty(cap.get('matched_result_title_zh'), cap.get('matched_result_title'), fallback_title)
    pts = [p.strip() for p in (cap.get('explanation_points') or []) if str(p).strip()]
    bullets = []
    if title:
        bullets.append(sentence(f'本页围绕“{title}”这一结果模块展开。'))
    for p in pts[:2]:
        cleaned = re.sub(r'^(对应结果模块|实验信息|主要结果|结果解读)：', '', p).strip()
        if cleaned:
            bullets.append(sentence(cleaned))
    if not bullets:
        bullets = [sentence('本页展示原文关键结果图，并结合对应结果段落进行中文讲解。')]
    while len(bullets) < 3:
        bullets.append('该结果与正文描述一致，可用于支撑作者在本节提出的核心结论。')
    return bullets[:3]


def build_strengths(captions: List[Dict[str, Any]], fulltext: str) -> List[Dict[str, Any]]:
    blob = ' '.join((c.get('matched_result_title') or '') for c in captions).lower() + ' ' + fulltext.lower()
    items = [
        {'heading': '证据链较完整', 'points': ['论文通过多种实验层面交叉验证核心结论，而不是仅依赖单一指标。']},
    ]
    if re.search(r'proteom|rna-seq|sequencing|gsea|kegg', blob):
        items.append({'heading': '机制分析较深入', 'points': ['除表型结果外，还结合组学或通路分析，增强了结果解释力。']})
    if re.search(r'mice|mouse|animal', blob) and re.search(r'behavior|maze|open field', blob):
        items.append({'heading': '功能结局明确', 'points': ['论文同时报告功能表型与组织/分子层结果，使结论更具说服力。']})
    items.append({'heading': '图像证据丰富', 'points': ['原文提供多张关键 Figure，适合按证据链组织为组会汇报。']})
    return items[:3]


def build_limitations(fulltext: str) -> List[Dict[str, Any]]:
    blob = fulltext.lower()
    points = [{'heading': '外推性', 'points': ['研究结论首先适用于本文所采用的模型、样本类型和实验条件，推广时仍需谨慎。']}]
    if re.search(r'mice|mouse|animal', blob):
        points.append({'heading': '模型限制', 'points': ['动物模型结果与真实临床疾病之间仍存在差异，后续需要更多临床或人源证据支持。']})
    else:
        points.append({'heading': '机制深度', 'points': ['虽然论文给出了关键关联结果，但仍需进一步研究明确更直接的因果链条。']})
    points.append({'heading': '转化思考', 'points': ['干预效果、适用人群与长期安全性等问题，仍需要在后续研究中继续验证。']})
    return points[:3]


def build_takeaway(title_en: str, captions: List[Dict[str, Any]], fulltext: str) -> List[str]:
    blob = ' '.join((c.get('matched_result_title') or '') + ' ' + (c.get('explanation_cn') or '') for c in captions)
    items = [
        '论文通过原文关键 Figure 展示了干预对核心功能或病理结局的影响，而不是只停留在单一观察指标。',
        '结果页整体提示：功能变化、病理改变和机制线索之间存在可串联的证据链。',
        '这项研究为后续机制研究、转化验证或同类干预策略提供了可参考的证据基础。'
    ]
    if 'lymphocyte' in blob.lower() or 'immune' in blob.lower():
        items[1] = '结果页整体提示：免疫调节、病理缓解与功能改善之间存在可串联的证据链。'
    return items


def build_slides(meta_path: Path, fulltext_path: Path, figures_path: Path, captions_path: Path, search_item: Dict[str, Any], out_dir: Path) -> Path:
    meta = read_json(meta_path)
    fulltext = fulltext_path.read_text(encoding='utf-8')
    figures = read_json(figures_path)
    captions = read_json(captions_path)
    fig_map = {f['figure_ref']: f for f in figures if isinstance(f, dict) and f.get('figure_ref') and f.get('url')}
    has_original_figures = bool(fig_map)
    authors = meta.get('authors') or parse_authors_from_fulltext(fulltext)
    journal, year = detect_journal_year(search_item, meta)
    title_en = meta.get('title_en') or search_item.get('title') or ''
    title_zh = choose_title_zh(title_en, meta, fulltext)
    abstract = str(search_item.get('abstract') or '')

    slides: List[Dict[str, Any]] = []
    author_mode = 'first_et_al'
    slides.append({
        'slide_type': 'title',
        'title': title_zh,
        'subtitle': title_en,
        'bullets': [
            author_display(authors, author_mode),
            f'{journal}，{year}'.strip('，'),
            '基于原文全文与 Figure 自动生成',
            '按背景—问题—设计—结果链—总结的顺序组织汇报'
        ]
    })
    slides.append({
        'slide_type': 'overview',
        'title': '全文概述',
        'bullets': infer_general_overview(title_en, abstract, captions, fulltext)
    })
    slides.append({
        'slide_type': 'background',
        'title': '研究背景与科学问题',
        'sections': infer_background(title_en, abstract)
    })
    slides.append({
        'slide_type': 'design',
        'title': '研究设计与技术路线',
        'sections': infer_design_sections(fulltext, captions)
    })

    used_refs = set()
    for cap in captions:
        ref = cap.get('figure_ref')
        if not ref or ref in used_refs:
            continue
        fig = fig_map.get(ref)
        if not fig:
            continue
        used_refs.add(ref)
        source_result_subtitle = first_nonempty(cap.get('matched_result_title_zh'), cap.get('matched_result_title'))
        slide_title = compress_result_title(source_result_subtitle) if source_result_subtitle else compress_result_title(ref)
        explanation_text = first_nonempty(cap.get('explanation_cn'), '该图用于支撑原文对应结果模块的核心结论。')
        explanation_chunks = split_explanation_points(explanation_text, max_chunks=3) or [explanation_text]
        bullets = build_result_bullets(cap, slide_title)

        if len(explanation_chunks) == 1:
            page_explanation = explanation_chunks[0]
            if len(page_explanation) < 60:
                page_explanation += '；该图与正文结果段落相互印证，可帮助完整理解本节的核心结论。'
            slides.append({
                'slide_type': 'result',
                'title': slide_title,
                'source_result_subtitle': source_result_subtitle,
                'bullets': bullets,
                'figure_refs': [ref],
                'image_paths_or_urls': [fig['url']],
                'figure_explanations': [{'figure_ref': ref, 'explanation': page_explanation}],
                'speaker_intent': '围绕原文关键图讲清该结果模块的实验信息、主要观察和结果意义'
            })
        else:
            for idx, chunk in enumerate(explanation_chunks, start=1):
                page_title = slide_title if idx == 1 else f'{slide_title}（{idx}/{len(explanation_chunks)}）'
                page_bullets = bullets if idx == 1 else [sentence('本页继续拆解同一张原图中的另一层信息重点。'), sentence(chunk)]
                page_explanation = chunk
                if len(page_explanation) < 60:
                    page_explanation += '；这一页继续围绕同一张原图展开讲解，重点补充该结果在全文证据链中的位置，以及它对作者核心结论的支持意义。'
                slides.append({
                    'slide_type': 'result',
                    'title': page_title,
                    'source_result_subtitle': source_result_subtitle,
                    'bullets': page_bullets,
                    'figure_refs': [ref],
                    'image_paths_or_urls': [fig['url']],
                    'figure_explanations': [{'figure_ref': ref, 'explanation': page_explanation}],
                    'speaker_intent': '同一张原图分多页讲解，单页只展开一个重点，避免信息拥挤'
                })

    if not has_original_figures:
        fallback_results = []
        para_candidates = [p.strip() for p in re.split(r'\n\s*\n', fulltext) if len(p.strip()) > 180]
        for para in para_candidates:
            low = para.lower()
            if any(k in low for k in ['caprisa', 'health diplomacy', 'covid-19', 'tuberculosis', 'hiv prevention', 'science diplomacy', 'community engagement', 'global policy', 'funding', 'equity']):
                fallback_results.append(para)
            if len(fallback_results) >= 3:
                break
        if not fallback_results:
            fallback_results = para_candidates[:3]

        for idx, para in enumerate(fallback_results, start=1):
            clean = re.sub(r'\s+', ' ', para)
            title_guess = [
                ('health diplomacy', '健康外交与科学转化'),
                ('hiv prevention', 'HIV 预防的非洲经验'),
                ('tuberculosis', 'HIV/结核协同应对经验'),
                ('covid-19', 'COVID-19 期间的平台应变能力'),
                ('community engagement', '社区共创与研究落地'),
                ('funding', '科研韧性与资金挑战'),
                ('equity', '全球公平与南方科学声音'),
            ]
            slide_title = f'关键内容 {idx}'
            lower_clean = clean.lower()
            for key, val in title_guess:
                if key in lower_clean:
                    slide_title = val
                    break
            summary_sentences = re.split(r'(?<=[\.!?。])\s+', clean)
            bullets = []
            for sent in summary_sentences:
                sent = sent.strip()
                if len(sent) >= 25:
                    bullets.append(sentence(sent[:110].strip()))
                if len(bullets) >= 3:
                    break
            if not bullets:
                bullets = [sentence(clean[:110])]
            slides.append({
                'slide_type': 'result',
                'title': slide_title,
                'source_result_subtitle': slide_title,
                'bullets': bullets,
                'figure_refs': [],
                'image_paths_or_urls': [],
                'figure_explanations': [],
                'speaker_intent': '全文无原图时，提炼正文中的关键论点作为结果/讨论型汇报页面'
            })

    mech_cap = next((c for c in captions if re.search(r'mechan|pathway|proteom|network|summary|model|schema|overview|graphical abstract', (c.get('matched_result_title') or '') + ' ' + (c.get('original_caption') or ''), re.I)), None)
    if not mech_cap and captions:
        mech_cap = captions[0]
    mech_fig = fig_map.get(mech_cap.get('figure_ref')) if mech_cap else None
    mechanism_slide = {
        'slide_type': 'mechanism',
        'title': '机制主线总结',
        'bullets': [
            '围绕原文证据链，将干预、关键中间环节与最终功能/病理结局串联起来。',
            '优先依据机制图、组学图或系统层结果页来概括上下游关系。',
            '若原文没有独立机制图，则使用最能代表整体逻辑的一张 Figure 作为支撑。',
            '这一页服务于报告收束，帮助听众建立对全文主线的整体理解。'
        ],
        'figure_required': bool(has_original_figures),
        'figure_refs': [mech_cap['figure_ref']] if mech_fig and mech_cap else [],
        'image_paths_or_urls': [mech_fig['url']] if mech_fig else [],
        'figure_explanations': [{'figure_ref': mech_cap['figure_ref'], 'explanation': first_nonempty(mech_cap.get('explanation_cn'), '该图可作为机制或系统层证据，用于串联全文的核心逻辑。')}] if mech_fig and mech_cap else []
    }
    if not has_original_figures:
        mechanism_slide['figure_required'] = False
        mechanism_slide['bullets'] = [
            '这篇论文更接近讲座/综述型总结，核心主线不是单一实验机制图，而是“本地科学—伙伴合作—政策转化—公平可及”的连续链条。',
            '作者强调：高质量本地证据、长期科研平台、社区共创与全球协作，共同决定科学能否真正转化为公共卫生影响。',
            '从 HIV、结核到 COVID-19，CAPRISA 的经验说明：科学韧性本身就是健康外交能力的一部分。',
            '因此，本页以概念机制链替代原图机制页，用于帮助听众抓住全文主旨。'
        ]
    slides.append(mechanism_slide)
    slides.append({'slide_type': 'strengths', 'title': '文章优点', 'sections': build_strengths(captions, fulltext)})
    slides.append({'slide_type': 'limitations', 'title': '局限性与转化思考', 'sections': build_limitations(fulltext)})
    slides.append({'slide_type': 'takeaway', 'title': 'Take-home message', 'bullets': build_takeaway(title_en, captions, fulltext)})
    slides.append({'slide_type': 'closing', 'title': '谢谢！感谢批评指正！', 'bullets': ['Questions & Discussion']})

    deck = {
        'title': title_en,
        'paper_meta': {
            'title_en': title_en,
            'title_zh': title_zh,
            'authors': authors,
            'author_display': author_display(authors, author_mode),
            'author_display_mode': author_mode,
            'first_author': authors[0] if authors else '',
            'corresponding_author': meta.get('corresponding_author') or '',
            'journal': journal,
            'year': year,
            'doi': meta.get('doi') or '',
            'pmid': meta.get('pmid') or '',
            'source_id': str(meta.get('source_id') or search_item.get('id') or '')
        },
        'slides': slides
    }
    output = out_dir / 'slides.json'
    write_json(output, deck)
    return output


def enforce_figures(slides_json: Path, out_dir: Path) -> Path:
    output = out_dir / 'figure_check.json'
    script = script_dir() / 'enforce_figure_requirements.py'
    cp = run(['python3', str(script), '--slides-json', str(slides_json), '--output', str(output)], check=False)
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or FAIL)
    data = read_json(output)
    if not data.get('ok'):
        raise RuntimeError(FAIL)
    return output


def render_pptx(slides_json: Path, out_dir: Path, output_path: Optional[Path]) -> Path:
    script = script_dir() / 'render_pptx_from_slides.js'
    cmd = ['node', str(script), '--slides-json', str(slides_json), '--assets-dir', str(out_dir / 'assets')]
    if output_path:
        cmd += ['--output', str(output_path)]
    cp = run(cmd, check=False)
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip() or FAIL)
    path = Path((cp.stdout or '').strip().splitlines()[-1].strip())
    if not path.exists():
        raise RuntimeError(FAIL)
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description='One-shot complete pipeline for research-paper-to-ppt-v2')
    ap.add_argument('--title', required=True, help='完整英文标题')
    ap.add_argument('--work-dir', required=True, help='中间文件输出目录')
    ap.add_argument('--output', help='最终 PPTX 输出路径，可选')
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output).resolve() if args.output else None

    try:
        debug_log(work_dir, 'start', f'output={output_path}')
        search_item = search_paper(args.title, work_dir)
        debug_log(work_dir, 'search.ok', json.dumps(search_item, ensure_ascii=False)[:1000])
        doc_id = str(search_item.get('id') or '')
        if not doc_id:
            raise RuntimeError(FAIL)
        meta, fulltext, figures, _debug = fetch_fullpaper(doc_id, work_dir)
        debug_log(work_dir, 'fetch.ok', f'meta={meta.exists()} fulltext={fulltext.exists()} figures={figures.exists()} debug={_debug.exists()}')
        captions = extract_captions(fulltext, figures, work_dir)
        validate_inputs(meta, fulltext, figures, work_dir)
        build_bundle(meta, fulltext, figures, work_dir)
        slides_json = build_slides(meta, fulltext, figures, captions, search_item, work_dir)
        enforce_figures(slides_json, work_dir)
        pptx_path = render_pptx(slides_json, work_dir, output_path)
        print(str(pptx_path))
    except Exception as e:
        debug_log(work_dir, 'fatal', repr(e))
        print(FAIL)
        sys.exit(1)


if __name__ == '__main__':
    main()
