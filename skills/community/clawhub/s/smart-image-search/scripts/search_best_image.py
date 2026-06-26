#!/usr/bin/env python3
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Tuple
from query_params import parse_query_params

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
WEAK_WORDS = {"image", "images", "photo", "photos", "official", "logo", "emblem", "mascot", "poster", "wallpaper", "hd", "4k", "avatar", "meme"}
INTENT_KEYWORDS = {
    "meme": ["meme", "reaction image", "funny image", "emoji"],
    "official": ["official", "logo", "emblem", "mascot", "brand mark", "poster"],
    "wallpaper": ["wallpaper", "hd", "high resolution", "4k", "landscape", "portrait"],
    "avatar": ["avatar", "profile picture", "icon"],
}
SITE_ASSET_PATTERNS = [
    "logo_cb", "common/logo", "common_ued", "favicon", "sprite", "site-logo", "deploy/pc/common",
]
OFFICIAL_DOMAIN_TOKENS = ["edu", "gov", "official", "baike", "wiki", "wikipedia"]
OFFICIAL_RELATED_TOKENS = ["school", "university", "college", "academy", "logo", "emblem", "mascot", "campus", "gate"]
AGGREGATOR_PATTERNS = [
    "nipic", "photophoto", "58pic", "588ku", "logo9", "huitu", "huaban", "duitang", "gallery", "wallpaper",
    "stock", "sucai", "photophoto.cn"
]
NEWS_PATTERNS = ["news", "entertainment", "sohu", "toutiao", "video"]
CAMPUS_KEYWORDS = ["campus", "gate", "building", "landscape", "aerial", "map"]
EMBLEM_KEYWORDS = ["emblem", "logo", "crest", "badge", "mark"]
MASCOT_KEYWORDS = ["mascot", "character", "official character", "brand character", "ip character"]
POSTER_KEYWORDS = ["poster", "promotional art", "campaign art", "banner"]
EMBLEM_PREFERRED = ["emblem", "logo", "crest", "badge", ".svg", ".png", "vi", "visual identity"]
EMBLEM_PENALTY = ["personal homepage", "homepage", "campus map", "gate", "campus", "banner", "news"]
MASCOT_PREFERRED = ["mascot", "character", "official character", "brand character", "ip character", "plush", "figure"]
MASCOT_PENALTY = ["news", "report", "livestream", "event coverage", "press release"]
IMPLICIT_MASCOT_NAMES: List[str] = []


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, "ignore")


def normalize_query(query: str) -> Tuple[str, str, List[str]]:
    original = query.strip()
    compact = original.replace(" ", "")
    raw_tokens = [t.strip() for t in re.split(r"\s+", original) if t.strip()]
    tokens = [t for t in raw_tokens if t not in WEAK_WORDS]
    if compact and compact not in tokens and compact not in WEAK_WORDS:
        tokens.append(compact)
    return original, compact, tokens


def detect_subject_subtype(query: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    matched: List[str] = []
    removed = list((params or {}).get("removed_tokens") or [])
    haystack = [query] + removed
    merged = " ".join(haystack)

    if any(x.lower() in merged.lower() for x in EMBLEM_KEYWORDS):
        matched = [x for x in EMBLEM_KEYWORDS if x.lower() in merged.lower()]
        return {"type": "emblem", "confidence": "high", "matched_keywords": matched}
    if any(x in merged for x in IMPLICIT_MASCOT_NAMES):
        matched = [x for x in IMPLICIT_MASCOT_NAMES if x in merged]
        return {"type": "mascot", "confidence": "medium", "matched_keywords": matched}
    if any(x.lower() in merged.lower() for x in MASCOT_KEYWORDS):
        matched = [x for x in MASCOT_KEYWORDS if x.lower() in merged.lower()]
        return {"type": "mascot", "confidence": "high", "matched_keywords": matched}
    if any(x.lower() in merged.lower() for x in POSTER_KEYWORDS):
        matched = [x for x in POSTER_KEYWORDS if x.lower() in merged.lower()]
        return {"type": "poster", "confidence": "high", "matched_keywords": matched}
    if any(x.lower() in merged.lower() for x in CAMPUS_KEYWORDS):
        matched = [x for x in CAMPUS_KEYWORDS if x.lower() in merged.lower()]
        return {"type": "campus", "confidence": "high", "matched_keywords": matched}
    if any(x in query.lower() for x in ["university", "college", "school", "academy"]):
        return {"type": "campus", "confidence": "default", "matched_keywords": []}
    return {"type": None, "confidence": "default", "matched_keywords": []}


def detect_intent(query: str) -> Dict[str, Any]:
    q = query.lower().strip()
    hits: List[Tuple[str, str]] = []
    for intent, kws in INTENT_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in q:
                hits.append((intent, kw))
    if hits:
        intent = hits[0][0]
        return {"intent": intent, "confidence": "high", "matched_keywords": [kw for i, kw in hits if i == intent]}
    if any(x in query.lower() for x in ["school", "university", "college", "academy", "mascot", "emblem", "logo"]):
        return {"intent": "official", "confidence": "medium", "matched_keywords": []}
    return {"intent": "portrait", "confidence": "default", "matched_keywords": []}


def official_directed_queries(core_query: str, subject_subtype: str | None = None) -> List[str]:
    q = core_query.strip()
    ql = q.lower()
    schoolish = any(x in ql for x in ["university", "college", "school", "academy", "campus"])
    queries = [q, f"{q} official"]
    if subject_subtype == "emblem":
        queries.extend([f"{q} emblem", f"{q} logo", f"{q} crest", f"{q} brand mark", f"{q} visual identity"])
    elif subject_subtype == "mascot":
        queries.extend([f"{q} mascot", f"{q} official character", f"{q} brand character", f"{q} IP character"])
    elif subject_subtype == "poster":
        queries.extend([f"{q} official poster", f"{q} promotional art"])
    else:
        queries.extend([f"{q} campus", f"{q} gate", f"{q} emblem", f"{q} logo", f"{q} mascot"])
    queries.append(f"{q} site:wikipedia.org")
    if schoolish:
        queries.append(f"{q} site:edu")
    seen = set()
    out = []
    for item in queries:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_bing(query: str, limit: int = 12) -> Dict[str, Any]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"https://www.bing.com/images/search?q={encoded}"
    text = fetch(url)
    blocks = re.findall(r'm="({&quot;sid&quot;:.*?})"', text)
    results = []
    seen = set()
    for block in blocks:
        raw = html.unescape(block)
        img = re.search(r'"murl":"(.*?)"', raw)
        page = re.search(r'"purl":"(.*?)"', raw)
        title = re.search(r'"t":"(.*?)"', raw)
        if not img:
            continue
        image_url = img.group(1)
        if image_url in seen:
            continue
        seen.add(image_url)
        results.append({
            "engine": "bing",
            "image_url": image_url,
            "page_url": page.group(1) if page else "",
            "title": html.unescape(title.group(1)) if title else "",
        })
        if len(results) >= limit:
            break
    return {"engine": "bing", "search_url": url, "ok": True, "results": results}


def extract_baidu(query: str, limit: int = 12) -> Dict[str, Any]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"https://image.baidu.com/search/index?tn=baiduimage&word={encoded}"
    text = fetch(url)
    if "百度安全验证" in text or "security verification" in text.lower():
        return {"engine": "baidu", "search_url": url, "ok": False, "blocked": True, "block_reason": "security-verification", "results": []}
    results = []
    seen = set()
    for img in re.findall(r'"thumbURL":"(.*?)"', text):
        image_url = html.unescape(img).replace('\\/', '/')
        if image_url in seen:
            continue
        seen.add(image_url)
        results.append({"engine": "baidu", "image_url": image_url, "page_url": "", "title": ""})
        if len(results) >= limit:
            break
    return {"engine": "baidu", "search_url": url, "ok": bool(results), "results": results}


def extract_sogou(query: str, limit: int = 12) -> Dict[str, Any]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"https://pic.sogou.com/pics?query={encoded}"
    text = fetch(url)
    urls = re.findall(r'https?://[^"\']+?\.(?:jpg|jpeg|png|gif|webp)', text, re.I)
    results = []
    seen = set()
    filtered = 0
    for image_url in urls:
        low = image_url.lower()
        if any(pat in low for pat in SITE_ASSET_PATTERNS):
            filtered += 1
            continue
        if image_url in seen:
            continue
        seen.add(image_url)
        results.append({"engine": "sogou", "image_url": image_url, "page_url": url, "title": ""})
        if len(results) >= limit:
            break
    return {"engine": "sogou", "search_url": url, "ok": bool(results), "results": results, "filtered_site_assets": filtered}


def strong_entity_tokens(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t and t not in WEAK_WORDS and len(t) >= 2]


def entity_consistency_score(original: str, compact: str, tokens: List[str], hay: str, intent: str) -> Tuple[int, List[str]]:
    score = 0
    why: List[str] = []
    strong_tokens = strong_entity_tokens(tokens)
    matches = [t for t in strong_tokens if t.lower() in hay]

    if compact and compact.lower() in hay:
        score += 10
        why.append("entity:compact-full-match")
    elif original and original.lower() in hay:
        score += 8
        why.append("entity:full-match")

    if len(matches) >= 2:
        score += 8
        why.append("entity:multi-token-match")
    elif len(matches) == 1:
        score += 3
        why.append("entity:single-token-match")
    elif strong_tokens:
        score -= 12
        why.append("entity:no-strong-token-match")

    if intent == "official" and strong_tokens:
        if len(matches) == 0:
            score -= 10
            why.append("official:entity-mismatch")
        elif len(matches) == 1 and len(strong_tokens) >= 2:
            score -= 4
            why.append("official:partial-entity-match")
    return score, why


def score_candidate(c: Dict[str, Any], original: str, compact: str, tokens: List[str], intent: str, subject_subtype: str | None = None) -> Tuple[int, List[str]]:
    hay = " ".join([c.get("title", ""), c.get("image_url", ""), c.get("page_url", "")]).lower()
    score = 0
    why: List[str] = []
    entity_score, entity_why = entity_consistency_score(original, compact, tokens, hay, intent)
    score += entity_score
    why.extend(entity_why)
    for tok in tokens:
        if tok.lower() in hay:
            score += 2
            why.append(f"token:{tok}")
    if c.get("engine") == "bing":
        score += 2
        why.append("bing-structured")

    if any(domain in hay for domain in ["baike", "bilibili", "zhihu", "weibo", "edu.cn", "official", "gov.cn", "nwpu.edu.cn"]):
        score += 3
        why.append("semantically-related-domain")

    if any(bad in hay for bad in ["news", "finance", "auto", "house", "sports"]):
        score -= 4
        why.append("query-drift")
    if any(bad in hay for bad in SITE_ASSET_PATTERNS):
        score -= 30
        why.append("site-asset")
    if "thumb" in hay:
        score -= 2
        why.append("thumbnail-signal")

    if intent == "meme":
        if any(good in hay for good in ["表情", "斗图", "搞笑", "meme", "qiubiaoqing"]):
            score += 8
            why.append("intent:meme-match")
        if any(bad in hay for bad in ["official", "edu.cn", "官网"]):
            score -= 3
            why.append("intent:meme-penalty-official")
    elif intent == "official":
        if any(good in hay for good in OFFICIAL_DOMAIN_TOKENS):
            score += 18
            why.append("intent:official-domain-match")
        if any(good in hay for good in OFFICIAL_RELATED_TOKENS):
            score += 8
            why.append("intent:official-related-match")
        if any(bad in hay for bad in AGGREGATOR_PATTERNS):
            score -= 18
            why.append("intent:official-penalty-aggregator")
        if any(bad in hay for bad in NEWS_PATTERNS):
            score -= 12
            why.append("intent:official-penalty-news")
        if any(bad in hay for bad in ["表情", "斗图", "搞笑", "qiubiaoqing"]):
            score -= 8
            why.append("intent:official-penalty-meme")

        if subject_subtype == "campus":
            if any(good in hay for good in CAMPUS_KEYWORDS):
                score += 8
                why.append("subtype:campus-match")
            if any(bad in hay for bad in EMBLEM_KEYWORDS + MASCOT_KEYWORDS):
                score -= 4
                why.append("subtype:campus-penalty-noncampus")
        elif subject_subtype == "emblem":
            if any(good in hay for good in EMBLEM_KEYWORDS):
                score += 10
                why.append("subtype:emblem-match")
            if any(good in hay for good in EMBLEM_PREFERRED):
                score += 8
                why.append("subtype:emblem-preferred-signal")
            if any(bad in hay for bad in CAMPUS_KEYWORDS):
                score -= 4
                why.append("subtype:emblem-penalty-campus")
            if any(bad in hay for bad in EMBLEM_PENALTY):
                score -= 8
                why.append("subtype:emblem-penalty-nonbrand")
        elif subject_subtype == "mascot":
            if any(good in hay for good in MASCOT_KEYWORDS):
                score += 10
                why.append("subtype:mascot-match")
            if any(good in hay for good in MASCOT_PREFERRED):
                score += 8
                why.append("subtype:mascot-preferred-signal")
            if any(name.lower() in hay for name in IMPLICIT_MASCOT_NAMES):
                score += 8
                why.append("subtype:mascot-implicit-name")
            if any(bad in hay for bad in MASCOT_PENALTY):
                score -= 10
                why.append("subtype:mascot-penalty-news")
        elif subject_subtype == "poster":
            if any(good in hay for good in POSTER_KEYWORDS):
                score += 8
                why.append("subtype:poster-match")
    elif intent == "wallpaper":
        if any(good in hay for good in ["壁纸", "高清", "4k", "hd", "uhd"]):
            score += 8
            why.append("intent:wallpaper-match")
    elif intent == "avatar":
        if any(good in hay for good in ["头像", "avatar"]):
            score += 8
            why.append("intent:avatar-match")
    else:
        if any(good in hay for good in ["写真", "高清", "照片", "人物", "portrait"]):
            score += 3
            why.append("intent:portrait-match")
        if any(bad in hay for bad in ["表情包", "斗图", "搞笑"]):
            score -= 2
            why.append("intent:portrait-penalty-meme")

    return score, why


def apply_entity_gating(candidates: List[Dict[str, Any]], tokens: List[str], intent: str) -> List[Dict[str, Any]]:
    strong_tokens = strong_entity_tokens(tokens)
    if intent != "official" or len(strong_tokens) < 2:
        return candidates

    gated = []
    fallback = []
    for c in candidates:
        why = list(c.get("why") or [])
        hay = " ".join([c.get("title", ""), c.get("image_url", ""), c.get("page_url", "")]).lower()
        match_count = sum(1 for t in strong_tokens if t.lower() in hay)
        item = {**c, "entity_match_count": match_count}
        if match_count >= 2:
            why.append("entity-gate:pass")
            item["why"] = why
            gated.append(item)
        elif match_count == 1:
            why.append("entity-gate:fallback-only")
            item["why"] = why
            item["score"] = item.get("score", 0) - 8
            fallback.append(item)
        else:
            why.append("entity-gate:reject")
            item["why"] = why
            item["score"] = item.get("score", 0) - 20
            fallback.append(item)
    return gated if gated else fallback


def classify_confidence(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not candidates:
        return {"level": "low", "top_score": None, "second_score": None, "reason": "no-candidates"}
    top = candidates[0].get("score", 0)
    second = candidates[1].get("score", 0) if len(candidates) > 1 else -999
    gap = top - second
    level = "low"
    reason = "weak-top-score"
    if top >= 22 and gap >= 6:
        level = "high"
        reason = "strong-top-match"
    elif top >= 12:
        level = "medium"
        reason = "usable-but-not-dominant"
    if any(x in (candidates[0].get("why") or []) for x in ["site-asset", "thumbnail-signal", "intent:official-penalty-aggregator"]):
        if level == "high":
            level = "medium"
            reason = "downgraded-top-result-risk"
        elif level == "medium":
            level = "low"
            reason = "downgraded-top-result-risk"
    return {"level": level, "top_score": top, "second_score": second, "gap": gap, "reason": reason}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: search_best_image.py <query>", file=sys.stderr)
        return 1
    query = " ".join(sys.argv[1:]).strip()
    params = parse_query_params(query)
    search_query = params["core_query"]
    original, compact, tokens = normalize_query(search_query)
    intent_info = detect_intent(search_query)
    if params.get("intent_override"):
        intent_info = {
            "intent": params["intent_override"],
            "confidence": "override",
            "matched_keywords": params.get("removed_tokens", []),
        }
    subject_subtype = detect_subject_subtype(search_query, params)
    intent = intent_info["intent"]

    candidate_queries = [search_query]
    if intent == "official":
        candidate_queries = official_directed_queries(search_query, subject_subtype.get("type"))

    engines = []
    for q in candidate_queries:
        for fn in (extract_bing, extract_baidu, extract_sogou):
            try:
                item = fn(q)
                item["search_query"] = q
                engines.append(item)
            except Exception as e:
                engines.append({"engine": fn.__name__.replace("extract_", ""), "search_query": q, "ok": False, "error": str(e), "results": []})
    candidates = []
    seen_pairs = set()
    for engine in engines:
        for item in engine.get("results", []):
            key = (item.get("image_url"), item.get("page_url"))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            score, why = score_candidate(item, original, compact, tokens, intent, subject_subtype.get("type"))
            if intent == "official" and engine.get("search_query") != search_query:
                score += 3
                why.append("official-directed-query")
            candidates.append({**item, "score": score, "why": why, "matched_query": engine.get("search_query", search_query)})
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    candidates = apply_entity_gating(candidates, tokens, intent)
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    confidence = classify_confidence(candidates)
    out = {
        "query": query,
        "parsed_params": params,
        "search_query": search_query,
        "normalized": {"original": original, "compact": compact, "tokens": tokens},
        "intent": intent_info,
        "subject_subtype": subject_subtype,
        "confidence": confidence,
        "engines": engines,
        "best_image": candidates[0] if candidates else None,
        "top_candidates": candidates[:5],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
