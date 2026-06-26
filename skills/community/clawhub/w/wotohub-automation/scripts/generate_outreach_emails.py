#!/usr/bin/env python3
from typing import Optional
"""
generate_outreach_emails.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

Lightweight fallback outreach email generator.

Primary outreach copy should come from the model layer.
This script exists only to provide a conservative, reusable fallback draft
when model-generated outreach is unavailable or explicitly skipped.

Do not treat this script as the default persuasion or personalization engine.
Quality-first policy: for real outreach, prefer model-first drafts before send;
use this fallback only when model drafts are unavailable and the operator accepts fallback quality.
"""
import argparse
import json
import re
from pathlib import Path

from html_email_utils import plain_text_to_html, normalize_html_body, html_to_plain_text

# ─── Reusable content fragments ────────────────────────────────────────────

# ─── Language configuration ──────────────────────────────────────────────────

# Default language (used when --lang is not specified)
DEFAULT_LANG = 'en'

# All translatable strings: key → {lang: translation}
# Only strings that differ by language need to go here;
# the HOOK/ANGLE/PROOF pools stay in English as the base.
_TRANSLATIONS = {
    'en': {
        'subject_collab':   'Collab idea: {product} x {name}',
        'subject_partner':  'Partnership opportunity: {product} x {name}',
        'subject_tag':      '{tag} collab: {product} — {name}',
        'offer_sample':     'We can offer product support and samples.',
        'offer_paid':       'We can offer a paid collaboration.',
        'offer_affiliate':  'We can offer product support plus an affiliate structure.',
        'cta':              "If this feels like a fit, I'd be happy to send product details, sample info, and next steps.",
        'audience_hint':    '',
        'subject_prefix':   'Collab idea: {product}',
        'greeting':         'Hi {name},',
        'body_intro':       'I think {product} could be a strong fit for your audience.',
        'body_angle':       'One reason is {benefit}.',
        'body_details':     "{offer} I'd love to share more details — product specs, sample info, and campaign options.",
        'signoff':          'Best regards,',
    },
    'es': {
        'subject_collab':   'Propuesta de colaboración: {product} — {name}',
        'subject_partner':  'Oportunidad de colaboración: {product} x {name}',
        'subject_tag':      'Colaboración {tag}: {product} — {name}',
        'offer_sample':     'Podemos ofrecer el producto en muestra.',
        'offer_paid':       'Podemos ofrecer una colaboración remunerada.',
        'offer_affiliate':  'Podemos ofrecer el producto más una estructura de afiliado.',
        'cta':              'Si te parece interesante, me encantaría compartir más detalles.',
        'audience_hint':    'Tu audiencia ',
        'subject_prefix':    'Propuesta de colaboración: {product} — {name}',
        'greeting':         'Hola {name},',
        'body_intro':       'Creo que {product} puede encajar muy bien con tu audiencia.',
        'body_angle':       'Uno de los motivos es {benefit}.',
        'body_details':     '{offer} Si te interesa, con gusto puedo compartirte detalles del producto, muestras y opciones de campaña.',
        'signoff':          'Saludos,',
    },
    'ja': {
        'subject_collab':   'コラボレーション提案：{product} — {name}様',
        'subject_partner':  'コラボレーションのご提案：{product} × {name}',
        'subject_tag':      '{tag}コラボレーション：{product} — {name}様',
        'offer_sample':     'サンプル提供が可能です。',
        'offer_paid':       '有料コラボレーションのご提案です。',
        'offer_affiliate':  'サンプル＋アソシエイト報酬でのご案内です。',
        'cta':              'ご興味があれば、詳細やサンプルについてご連絡いたします。',
        'audience_hint':    '',  # not used for ja body (body stays English)
        'subject_prefix':    'コラボレーションのご連絡：{product}',
        'greeting':         '{name}様',
        'body_intro':       '{product} はあなたのオーディエンスと相性が良いと感じています。',
        'body_angle':       '特に {benefit} が魅力だと考えています。',
        'body_details':     '{offer} ご興味がありましたら、製品情報、サンプル、進行案の詳細をお送りします。',
        'signoff':          'よろしくお願いいたします。',
    },
    'ko': {
        'subject_collab':   '협업 제안: {product} — {name}님',
        'subject_partner':  '협업 기회: {product} × {name}님',
        'subject_tag':      '{tag} 협업: {product} — {name}님',
        'offer_sample':     '샘플 제품 제공이 가능합니다.',
        'offer_paid':       '유료 협업 제안입니다.',
        'offer_affiliate':  '샘플 + 제휴 구조로 안내드립니다.',
        'cta':              '관심 있으시면 상세 내용과 샘플에 대해 안내드리겠습니다.',
        'audience_hint':    '',  # not used for ko body (body stays English)
        'subject_prefix':    '협업 제안: {product}',
        'greeting':         '안녕하세요 {name}님,',
        'body_intro':       '{product} 이(가) 고객님의 오디언스와 잘 맞을 것이라고 생각합니다.',
        'body_angle':       '그 이유 중 하나는 {benefit} 입니다.',
        'body_details':     '{offer} 관심 있으시면 제품 정보, 샘플, 캠페인 옵션을 자세히 공유드리겠습니다.',
        'signoff':          '감사합니다.',
    },
}

# Fields inside each translation dict that need {name}/{product}/{tag} interpolation
_INTERPOLATED_FIELDS = frozenset([
    'subject_collab', 'subject_partner', 'subject_tag', 'subject_prefix',
])


def _t(key: str, lang: str, **kwargs) -> str:
    """Return translated string for key, falling back to English."""
    lang_map = _TRANSLATIONS.get(lang, _TRANSLATIONS['en'])
    text = lang_map.get(key, _TRANSLATIONS['en'].get(key, key))
    # Interpolate any {placeholders}
    try:
        return text.format(**kwargs)
    except KeyError:
        return text


def _lang_param(lang: Optional[str]) -> str:
    """Normalise and return a valid lang code, defaulting to English.

    Policy: subject and body must default to English unless the caller
    explicitly requests another supported language.
    """
    if lang is None:
        return DEFAULT_LANG
    lang = str(lang).strip().lower()
    if not lang:
        return DEFAULT_LANG
    if lang in _TRANSLATIONS:
        return lang
    return DEFAULT_LANG


_HOOK_POOL = {
    # Influencer has strong sales data
    'high_gmv': [
        "I came across your channel and was impressed by your recent sales results — {fans_fmt} followers with consistently strong conversions.",
        "Your track record really stands out: great engagement AND solid sales numbers. I think our {product} could be a natural next fit.",
    ],
    # Influencer creates product-led / commerce content
    'seller': [
        "I noticed you regularly feature products in your content, which is exactly the kind of creator we're looking to partner with.",
        "Your content has a strong commerce angle — products just work well on your channel. Our {product} might be a great fit.",
    ],
    # Influencer has relevant tags/category alignment
    'category': [
        "Our {product} sits right within the {tag_hint} space, and your content caught my eye as a strong fit.",
        "Given your focus on {tag_hint}, I think there's a really natural connection to what we're building with {product}.",
    ],
    # Influencer has high engagement rate
    'engagement': [
        "Your engagement rate is seriously impressive — your audience clearly trusts your recommendations.",
        "With that kind of engagement, you clearly know what works for your viewers. I think {product} could be a hit.",
    ],
    # Default fallback
    'default': [
        "I came across your content and think there could be a great collaboration opportunity with our {product}.",
        "Our team has been researching creators who align well with {product}, and your channel came up as a strong match.",
    ],
}

_ANGLE_POOL = {
    # Maps product selling-point keys to natural value-prop phrases
    'vlog camera':        "it's designed for on-the-go vlogging with smooth stabilization",
    '4k video':           "stunning 4K video quality that looks great on camera",
    'gimbal stabilizer':  "built-in gimbal stabilization for buttery-smooth footage",
    'face tracking':      "smart face/object tracking so you never lose focus",
    'portable camcorder': "compact and portable — easy to take anywhere",
    '4k':                 "crisp 4K resolution that elevates any video",
    'wireless':           "fully wireless for total freedom while filming",
    'night vision':       "excellent low-light performance for any environment",
    'action camera':      "built tough for adventure and action shots",
    'webcam':             "a clear, reliable webcam upgrade for creators",
    'microphone':         "professional audio quality that completes the setup",
    'smartwatch':         "smart features that fit naturally into everyday life",
    'electric toothbrush':"a genuinely better daily brushing experience",
    'whitening':          "visible whitening results users can actually see",
    'serum':              "lightweight formula that absorbs instantly",
    'face cream':         "hydrating formula that works for daily use",
    'lifestyle':          "designed to fit seamlessly into everyday routines",
}

_PROOF_POOL = {
    'has_product':   "You've already been successfully featuring similar products — that's exactly the kind of background we're after.",
    'high_fans':     "With a reach of {fans_fmt} viewers, a single well-placed feature could drive real momentum.",
    'high_gmv':      "Your recent GMV numbers show your audience converts — that's something we get really excited about.",
    'high_engagement': "Your engagement rate shows your community is actively listening — rare and valuable.",
    'video_title':   "I noticed some of your recent titles like '{video_title}' — the content angle is a great match for what we have.",
}

# ─── Helpers ────────────────────────────────────────────────────────────────


def _pick(lst: list[str], **kwargs) -> str:
    import random
    txt = random.choice(lst).format(**kwargs)
    return txt


def _history_summary(item: dict) -> dict:
    history = item.get('historyAnalysis') or {}
    matched_terms = history.get('matchedTerms') or []
    samples = history.get('contentSamples') or []
    return {
        'matched_terms': matched_terms,
        'sample': samples[0] if samples else '',
        'has_history': bool(history.get('hasHistorySignals')),
    }


def _ensure_sentence(text: str) -> str:
    text = (text or '').strip()
    if not text:
        return ''
    if text[-1] in '.!?':
        return text
    return text + '.'


def _best_hook(item: dict, product_name: str, tag_hint: str, fans_fmt: str) -> str:
    """Select the most relevant hook based on what we know about this influencer."""
    gmv = item.get('gmv30d') or item.get('gmv')
    fans = item.get('fansNum') or 0
    try:
        fans = int(float(fans))
    except Exception:
        fans = 0
    try:
        gmv = float(gmv)
    except Exception:
        gmv = 0
    interactive = item.get('interactiveRateAvg') or 0
    try:
        interactive = float(interactive)
        if interactive < 1:
            interactive *= 100
    except Exception:
        interactive = 0

    history = _history_summary(item)

    # Conservative fallback priority order only.
    if gmv > 10000:
        return _pick(_HOOK_POOL['high_gmv'], fans_fmt=fans_fmt, product=product_name)
    if item.get('hasProduct') or history['matched_terms'] or history['has_history']:
        return _pick(_HOOK_POOL['seller'], product=product_name)
    if interactive >= 4:
        return _pick(_HOOK_POOL['engagement'], fans_fmt=fans_fmt, product=product_name)
    if tag_hint and tag_hint != 'content':
        return _pick(_HOOK_POOL['category'], tag_hint=tag_hint, product=product_name)
    return _pick(_HOOK_POOL['default'], product=product_name)


def _build_angles(sp_list: list[str]) -> tuple[str, str]:
    """Translate selling-point keys into natural language value props."""
    props = []
    for sp in sp_list[:3]:
        props.append(_ANGLE_POOL.get(sp.lower(), sp))
    if not props:
        return ("a product I think your audience would genuinely appreciate", "")
    main = props[0]
    secondary = props[1] if len(props) > 1 else ""
    return (main, secondary)


def _collect_proof(item: dict, fans_fmt: str) -> str:
    """Build a social-proof line from whatever signals this influencer has."""
    parts = []
    gmv = item.get('gmv30d') or item.get('gmv')
    fans = item.get('fansNum') or 0
    try:
        fans = int(float(fans))
    except Exception:
        fans = 0
    try:
        gmv = float(gmv)
    except Exception:
        gmv = 0
    interactive = item.get('interactiveRateAvg') or 0
    try:
        interactive = float(interactive)
        if interactive < 1:
            interactive *= 100
    except Exception:
        interactive = 0
    video_title = (item.get('video_title') or '')[:50]
    history = _history_summary(item)
    if not video_title and history['sample']:
        video_title = history['sample'][:50]

    if item.get('hasProduct') or history['matched_terms']:
        parts.append(_PROOF_POOL['has_product'])
    if fans >= 50000:
        parts.append(_PROOF_POOL['high_fans'].format(fans_fmt=fans_fmt))
    if gmv > 5000:
        parts.append(_PROOF_POOL['high_gmv'])
    elif interactive >= 3:
        parts.append(_PROOF_POOL['high_engagement'])
    if video_title and len(video_title) > 10:
        parts.append(_PROOF_POOL['video_title'].format(video_title=video_title))

    return " ".join(parts) if parts else ""


def _tag_hint(tags: list[str]) -> str:
    """Flatten tags to a readable phrase, e.g. ['3C产品', '科技/技术'] → '3C / Tech'."""
    if not tags:
        return ""
    cleaned = []
    for t in tags[:3]:
        t = t.strip()
        if not t:
            continue
        # Simple zh→en cleanup for common tags
        t = t.replace('3C产品', '3C').replace('科技/技术', 'Tech').replace('家用用品', 'Home').replace('美妆', 'Beauty')
        cleaned.append(t)
    return " / ".join(cleaned) if cleaned else ""


_PRODUCT_KEYWORD_MAP = {
    'electric toothbrush': ['toothbrush', 'oral', 'dental', 'whitening', 'water flosser'],
    'toothbrush': ['toothbrush', 'oral', 'dental', 'whitening', 'water flosser'],
    'mouthwash': ['oral', 'dental', 'mouthwash'],
    'toothpaste': ['oral', 'dental', 'toothpaste'],
    'serum': ['skincare', 'beauty', 'serum'],
    'face cream': ['skincare', 'beauty', 'cream'],
    'skincare set': ['skincare', 'beauty'],
    'smartwatch': ['tech', 'fitness', 'smartwatch', 'wearable'],
}


def _clean_phrase(text: Optional[str]) -> str:
    text = str(text or '').strip()
    text = re.sub(r'\s+', ' ', text)
    return text.strip(' ,.-_')


def _shorten_text(text: str, max_len: int = 48) -> str:
    text = _clean_phrase(text)
    if len(text) <= max_len:
        return text
    shortened = text[:max_len].rsplit(' ', 1)[0].strip()
    return (shortened or text[:max_len]).strip(' ,.-_')


def _normalize_product_name(product_name: Optional[str], selling_points: Optional[list[str]]= None) -> str:
    raw = _clean_phrase(product_name)
    if not raw:
        raw = 'our product'
    low = raw.lower()

    direct_map = {
        '电动牙刷': 'electric toothbrush',
        '牙刷': 'toothbrush',
        '漱口水': 'mouthwash',
        '牙膏': 'toothpaste',
        '护肤套装': 'skincare set',
        '精华': 'serum',
        '面霜': 'face cream',
        '智能手表': 'smartwatch',
    }
    for key, value in direct_map.items():
        if key in raw:
            return value

    heuristic_pairs = [
        ('electric toothbrush', ['toothbrush', 'oral care', 'whitening', 'electric toothbrush']),
        ('mouthwash', ['mouthwash']),
        ('toothpaste', ['toothpaste']),
        ('serum', ['serum']),
        ('face cream', ['face cream', 'moisturizer']),
        ('skincare set', ['skincare']),
        ('smartwatch', ['smartwatch', 'watch']),
    ]
    for canonical, markers in heuristic_pairs:
        if any(m in low for m in markers):
            return canonical

    for sp in selling_points or []:
        sp_low = str(sp or '').lower()
        for canonical, markers in heuristic_pairs:
            if any(m in sp_low for m in markers):
                return canonical

    if any(token in raw for token in ['推广一款', '美国市场', '主打', '价格', '$']) or len(raw) > 48:
        return _shorten_text(raw, 32)
    return _shorten_text(raw, 32)


def _relevant_tag_hint(tags: list[str], product_name: str) -> str:
    tag_hint = _tag_hint(tags)
    if not tag_hint:
        return ''
    normalized = tag_hint.lower()
    keywords = []
    for key, vals in _PRODUCT_KEYWORD_MAP.items():
        if key in product_name.lower():
            keywords.extend(vals)
    if keywords and not any(k in normalized for k in keywords):
        return ''
    if len(tag_hint) > 24:
        return ''
    return tag_hint


def _finalize_subject(subject: str, max_len: int = 78) -> str:
    subject = _clean_phrase(subject)
    if len(subject) <= max_len:
        return subject
    if ' x ' in subject:
        left, right = subject.rsplit(' x ', 1)
        left = _shorten_text(left, max_len - len(right) - 4)
        return f'{left} x {right}'
    if ' — ' in subject:
        left, right = subject.rsplit(' — ', 1)
        left = _shorten_text(left, max_len - len(right) - 4)
        return f'{left} — {right}'
    return _shorten_text(subject, max_len)


# ─── Core generator ────────────────────────────────────────────────────────


def generate_email(item: dict, product: dict, cooperation: str, lang: str = 'en', sender_name: Optional[str]= None) -> dict:
    """
    Assemble a lightweight fallback outreach email from reusable fragments.
    This is a backup draft generator, not the primary model-driven copy engine.

    item fields used:
        nickname, fansNum, tagList, hasProduct, gmv30d,
        interactiveRateAvg, video_title

    product fields used:
        productName, sellingPoints (list of strings)

    lang: email language code ('en', 'es', 'ja', 'ko'). Default: 'en'.
    """
    import random
    random.seed()   # re-seed each call for variation

    name        = item.get('nickname') or 'there'
    fans        = item.get('fansNum') or 0
    tags        = item.get('tagList') or []
    sp_list     = product.get('sellingPoints') or []
    product_name = _normalize_product_name(product.get('productName'), sp_list)
    lang        = _lang_param(lang)

    try:
        fans_int = int(float(fans))
    except Exception:
        fans_int = 0
    fans_fmt = f"{fans_int:,}" if fans_int else "your"

    tag_hint  = _relevant_tag_hint(tags, product_name)
    main_prop, secondary_prop = _build_angles(sp_list)
    hook      = _best_hook(item, product_name, tag_hint, fans_fmt)
    proof     = _collect_proof(item, fans_fmt)

    # ── Subject (language-aware) ─────────────────────────────────────────────
    if item.get('hasProduct'):
        subject = _t('subject_partner', lang, product=product_name, name=name)
    elif tag_hint and tag_hint != 'content':
        subject = _t('subject_tag', lang, tag=tag_hint, product=product_name, name=name)
    else:
        subject = _t('subject_collab', lang, product=product_name, name=name)
    subject = _finalize_subject(subject)

    # ── Offer & CTA (language-aware) ────────────────────────────────────────
    offer = _t(f'offer_{cooperation}', lang, product=product_name, name=name)
    cta   = _t('cta', lang, product=product_name, name=name)
    audience_hint = _t('audience_hint', lang, fans_fmt=fans_fmt)

    # ── Body ────────────────────────────────────────────────────────────────
    if lang == 'en':
        lines = [
            f"Hi {name},",
            "",
            _ensure_sentence(hook),
            "",
        ]

        if main_prop:
            angle_line = f"I've been especially impressed with {main_prop}."
            if secondary_prop:
                angle_line += f" And {secondary_prop}."
            lines.append(angle_line)
            lines.append("")

        if proof:
            lines.append(_ensure_sentence(proof))
            lines.append("")

        lines.append(_t('body_details', lang, offer=offer))
        lines.append("")
        lines.append(cta)
        if sender_name and sender_name.strip():
            lines.append("")
            lines.append(_t('signoff', lang))
            lines.append(sender_name.strip())
    else:
        lines = [
            _t('greeting', lang, name=name),
            "",
            _t('body_intro', lang, product=product_name),
        ]
        if main_prop:
            lines.append("")
            lines.append(_t('body_angle', lang, benefit=main_prop))
        lines.append("")
        lines.append(_t('body_details', lang, offer=offer))
        lines.append("")
        lines.append(cta)
        if sender_name and sender_name.strip():
            lines.append("")
            lines.append(_t('signoff', lang))
            lines.append(sender_name.strip())

    body = "\n".join(lines)
    limited_body = _word_limit(body)
    html_body = normalize_html_body(plain_text_to_html(limited_body))
    plain_text_body = html_to_plain_text(html_body)
    return {
        'subject': subject,
        'body': limited_body,
        'htmlBody': html_body,
        'plainTextBody': plain_text_body,
        'wordCount': len(plain_text_body.split()),
        'lang': lang,
    }


def _choose_offer(cooperation: str) -> str:
    if cooperation == 'paid':
        return "We can offer a paid collaboration."
    if cooperation == 'affiliate':
        return "We can offer product support plus an affiliate structure."
    return "We can offer product support and samples."


def _choose_cta(cooperation: str) -> str:
    if cooperation == 'paid':
        return "If this sounds interesting, I'd be happy to share rates, product details, and the campaign brief."
    if cooperation == 'affiliate':
        return "If this feels like a fit, I'd be happy to send product details, sample info, and affiliate terms."
    return "If this feels like a fit, I'd be happy to send product details, sample info, and next steps."


def _word_limit(text: str, max_words: int = 250) -> str:
    """Trim to max words while preserving paragraph breaks.

    Joining with plain ``split()`` collapsed the greeting/body/signoff into a
    single line, which then broke downstream identity guardrails that inspect
    the opening salutation.
    """
    lines = [str(line).rstrip() for line in str(text or '').splitlines()]
    kept_lines: list[str] = []
    count = 0
    truncated = False
    for line in lines:
        tokens = line.split()
        if not tokens:
            kept_lines.append('')
            continue
        remaining = max_words - count
        if remaining <= 0:
            truncated = True
            break
        if len(tokens) <= remaining:
            kept_lines.append(' '.join(tokens))
            count += len(tokens)
            continue
        kept_lines.append(' '.join(tokens[:remaining]).rstrip() + '...')
        count += remaining
        truncated = True
        break
    result = '\n'.join(kept_lines).strip()
    if not result and text:
        return str(text).strip()
    return result


# ─── CLI ───────────────────────────────────────────────────────────────────


# ─── Chinese → English product term translation map (module-level, one-time) ───
_TERM_MAP = {
    '电动牙刷': 'electric toothbrush', '牙刷': 'toothbrush',
    '牙膏': 'toothpaste', '漱口水': 'mouthwash',
    '护肤套装': 'skincare set', '精华': 'serum', '面霜': 'face cream',
    '假发': 'wig', '智能手表': 'smartwatch', '儿童智能手表': 'kids smartwatch',
    '美白': 'whitening', '清洁力': 'deep cleaning',
    '智能刷牙体验': 'smart brushing experience',
    '日常清洁': 'daily cleaning', '便携': 'portability',
    '护理习惯': 'care routine', '保湿': 'hydration',
    '抗衰': 'anti-aging', '安全定位': 'safety tracking',
    '高颜值': 'aesthetic appeal',
}


def normalize_product(data: dict, args) -> dict:
    summary = (data.get('analysis') or {}).get('productSummary') or {}
    product_name = args.product_name or summary.get('productName') or 'our product'
    selling_points = args.selling_point or summary.get('sellingPoints') or []
    translated = [_TERM_MAP.get(x, x) for x in selling_points]
    normalized_name = _TERM_MAP.get(product_name, product_name)
    normalized_name = _normalize_product_name(normalized_name, translated)
    return {
        'productName': normalized_name,
        'sellingPoints': translated,
    }


def load_json(path: str):
    return json.loads(Path(path).read_text())


def load_model_drafts(path: Optional[str]) -> Optional[dict]:
    if not path:
        return None
    raw = Path(path).read_text().strip()
    if not raw:
        return None
    return json.loads(raw)


def _draft_source_label(draft: Optional[dict]) -> str:
    if not isinstance(draft, dict):
        return ""
    source = str(draft.get('draftSource') or draft.get('source') or '').strip().lower()
    style = str(draft.get('style') or '').strip().lower()
    if source:
        return source
    if style == 'model-first':
        return 'host-model'
    return ''


def _match_model_draft(model_drafts: Optional[dict], item: dict) -> Optional[dict]:
    if not isinstance(model_drafts, dict):
        return None
    candidates = []
    for key in ('besId', 'bEsId', 'bloggerId', 'id'):
        value = item.get(key)
        if value not in (None, ''):
            candidates.append(str(value))
    if not candidates:
        return None

    items = model_drafts.get('items') if isinstance(model_drafts.get('items'), list) else None
    if items:
        for draft in items:
            if not isinstance(draft, dict):
                continue
            draft_keys = {str(draft.get(k)) for k in ('bloggerId', 'besId', 'bEsId') if draft.get(k) not in (None, '')}
            if any(c in draft_keys for c in candidates):
                return draft
    draft_map = model_drafts.get('drafts') if isinstance(model_drafts.get('drafts'), dict) else None
    if draft_map:
        for c in candidates:
            if c in draft_map and isinstance(draft_map[c], dict):
                return draft_map[c]
    return None


def extract_items(data: dict) -> tuple[list[dict], dict]:
    if 'search' in data and isinstance(data['search'], dict):
        data = data['search']
    result = data.get('result', {}) if isinstance(data, dict) else {}
    payload = data.get('payload', {}) if isinstance(data, dict) else {}
    search_data = result.get('data', {}) if isinstance(result, dict) else {}
    if isinstance(search_data, dict) and isinstance(search_data.get('bloggerList'), list):
        return search_data['bloggerList'], payload
    return [], payload


def main():
    import json
    ap = argparse.ArgumentParser(
        description='Generate generic personalized outreach emails from WotoHub search results')
    ap.add_argument('--input', required=True)
    ap.add_argument('--product-name')
    ap.add_argument('--selling-point', action='append')
    ap.add_argument('--cooperation', choices=['sample', 'paid', 'affiliate'], default='sample')
    ap.add_argument('--limit', type=int, default=10)
    ap.add_argument('--lang', choices=['en', 'es', 'ja', 'ko'], default='en',
                    help='email language; defaults to English and only switches when the user explicitly requests another supported language')
    ap.add_argument('--sender-name', help='邮件署名；生成前应先向用户确认，禁止使用占位署名')
    ap.add_argument('--model-drafts-file', help='模型生成的 outreach drafts JSON 文件；有则优先消费')
    ap.add_argument('--output')
    ap.add_argument('--allow-fallback-drafts', action='store_true', help='允许在没有 host model drafts 时生成脚本 fallback 草稿；默认关闭')
    args = ap.parse_args()

    if not args.sender_name or not args.sender_name.strip():
        print(json.dumps({
            'success': False,
            'needsSenderName': True,
            'message': 'Generating outreach emails requires the user\'s confirmed sender name before drafting.',
            'nextStep': 'Ask the user what sender name/signature should appear in the email closing.'
        }, ensure_ascii=False, indent=2))
        return

    data = load_json(args.input)
    items, payload = extract_items(data)
    product = normalize_product(data, args)
    model_drafts = load_model_drafts(args.model_drafts_file)

    emails = []
    used_model_draft = False
    for item in items[:args.limit]:
        blogger_id = item.get('besId') or item.get('bloggerId') or ''
        matched_draft = _match_model_draft(model_drafts, item)
        if matched_draft:
            subject = matched_draft.get('subject') or ''
            body = matched_draft.get('body') or matched_draft.get('replyBody') or ''
            if subject and body:
                used_model_draft = True
                html_body = normalize_html_body(matched_draft.get('htmlBody') or body)
                plain_text_body = matched_draft.get('plainTextBody') or html_to_plain_text(html_body)
                normalized_lang = _lang_param(args.lang)
                emails.append({
                    'bloggerId': blogger_id,
                    'nickname': item.get('nickname'),
                    'emailAvailable': bool(item.get('hasEmail')),
                    'style': matched_draft.get('style') or 'model-first',
                    'draftSource': _draft_source_label(matched_draft) or 'host-model',
                    'language': normalized_lang,
                    'subject': subject,
                    'body': plain_text_body,
                    'htmlBody': html_body,
                    'plainTextBody': plain_text_body,
                    'wordCount': len(str(plain_text_body).split()),
                    'fansNum': item.get('fansNum'),
                    'link': item.get('link'),
                    'wotohubLink': f"https://www.wotohub.com/kocNewDetail?id={blogger_id}" if blogger_id else None,
                    'tagList': item.get('tagList') or [],
                })
                continue

        if not args.allow_fallback_drafts:
            continue

        email_data = generate_email(item, product, args.cooperation, lang=args.lang, sender_name=args.sender_name)
        emails.append({
            'bloggerId': blogger_id,
            'nickname': item.get('nickname'),
            'emailAvailable': bool(item.get('hasEmail')),
            'style': 'fallback-light',
            'draftSource': 'fallback-script',
            'language': args.lang,
            'subject': email_data['subject'],
            'body': email_data['plainTextBody'],
            'htmlBody': email_data['htmlBody'],
            'plainTextBody': email_data['plainTextBody'],
            'wordCount': email_data['wordCount'],
            'fansNum': item.get('fansNum'),
            'link': item.get('link'),
            'wotohubLink': f"https://www.wotohub.com/kocNewDetail?id={blogger_id}" if blogger_id else None,
            'tagList': item.get('tagList') or [],
        })

    normalized_lang = _lang_param(args.lang)

    generation_mode = 'model-first' if used_model_draft else ('fallback-light' if args.allow_fallback_drafts else 'host-drafts-required')

    result = {
        'language': normalized_lang,
        'maxWords': 250,
        'generationMode': generation_mode,
        'notes': [
            'Primary outreach copy should come from the host model layer.',
            'Fallback script drafts are only a safety net and should not be treated as the preferred semantic copy engine.',
            'Quality-first policy: for real outreach, prepare and use host model drafts before send whenever possible.',
            'When allowFallbackDrafts=false, this generator will not silently create fallback drafts.',
            'English is the default output language unless the caller explicitly requests another supported language.',
            'A confirmed sender name is required before generating drafts.'
        ],
        'product': product,
        'count': len(emails),
        'hostDraftsProvided': bool(model_drafts),
        'allowFallbackDrafts': bool(args.allow_fallback_drafts),
        'emails': emails,
    }
    if not emails and not model_drafts and not args.allow_fallback_drafts:
        result['needsHostDrafts'] = True
        result['message'] = 'No host model drafts provided. Fallback draft generation is disabled by default.'
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
