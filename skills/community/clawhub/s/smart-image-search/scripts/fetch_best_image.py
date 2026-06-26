#!/usr/bin/env python3
import json
import os
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

import search_best_image as sbi
from image_quality import inspect_file, url_quality_hints
from query_params import parse_query_params

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/53736"


def guess_ext(url: str, content_type: str | None) -> str:
    if content_type:
        ct = content_type.lower()
        if "jpeg" in ct or "jpg" in ct:
            return ".jpg"
        if "png" in ct:
            return ".png"
        if "gif" in ct:
            return ".gif"
        if "webp" in ct:
            return ".webp"
    m = re.search(r"\.([a-zA-Z0-9]{2,5})(?:$|\?)", url)
    if m:
        ext = "." + m.group(1).lower()
        if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def download(url: str, query: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.bing.com/"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type")
    ext = guess_ext(url, content_type)
    safe = re.sub(r"[^\w\-\u4e00-\u9fff]+", "_", query).strip("_") or "image"
    out_dir = Path("/home/mumu/clawd/tmp/search-image")
    out_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=f"{safe}_", suffix=ext, dir=out_dir)
    os.close(fd)
    with open(tmp_path, "wb") as f:
        f.write(data)
    return tmp_path, len(data), content_type


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fetch_best_image.py <query>", file=sys.stderr)
        return 1
    query = " ".join(sys.argv[1:]).strip()
    result = {"query": query}
    params = parse_query_params(query)
    search_query = params["core_query"]
    original, compact, tokens = sbi.normalize_query(search_query)
    intent_info = sbi.detect_intent(search_query)
    if params.get("intent_override"):
        intent_info = {
            "intent": params["intent_override"],
            "confidence": "override",
            "matched_keywords": params.get("removed_tokens", []),
        }
    subject_subtype = sbi.detect_subject_subtype(search_query, params)
    candidate_queries = [search_query]
    if intent_info["intent"] == "official":
        candidate_queries = sbi.official_directed_queries(search_query, subject_subtype.get("type"))

    engines = []
    for q in candidate_queries:
        for fn in (sbi.extract_bing, sbi.extract_baidu, sbi.extract_sogou):
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
            score, why = sbi.score_candidate(item, original, compact, tokens, intent_info["intent"], subject_subtype.get("type"))
            if intent_info["intent"] == "official" and engine.get("search_query") != search_query:
                score += 3
                why.append("official-directed-query")
            candidates.append({**item, "score": score, "why": why, "matched_query": engine.get("search_query", search_query)})
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    candidates = sbi.apply_entity_gating(candidates, tokens, intent_info["intent"])
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    confidence = sbi.classify_confidence(candidates)
    search = {
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
    result["search"] = search
    best = search.get("best_image")
    if not best:
        result["ok"] = False
        result["reason"] = "no-image-found"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    url_q = url_quality_hints(best["image_url"])
    if not url_q.accept:
        result.update({
            "ok": False,
            "reason": "rejected-by-url-quality",
            "image_url": best.get("image_url"),
            "engine": best.get("engine"),
            "score": best.get("score"),
            "quality": url_q.as_dict(),
            "subject_subtype": subject_subtype,
        })
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    try:
        path, size, content_type = download(best["image_url"], query)
        file_q = inspect_file(path, search.get("intent", {}).get("intent", "portrait"))
        if not file_q.accept:
            result.update({
                "ok": False,
                "reason": "rejected-by-file-quality",
                "path": path,
                "size": size,
                "content_type": content_type,
                "image_url": best["image_url"],
                "engine": best.get("engine"),
                "score": best.get("score"),
                "why": best.get("why"),
                "quality": file_q.as_dict(),
                "page_url": best.get("page_url", ""),
                "title": best.get("title", ""),
                "subject_subtype": subject_subtype,
            })
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        result.update({
            "ok": True,
            "path": path,
            "size": size,
            "content_type": content_type,
            "image_url": best["image_url"],
            "engine": best.get("engine"),
            "score": best.get("score") + url_q.score_delta + file_q.score_delta,
            "why": best.get("why"),
            "quality": {
                "url": url_q.as_dict(),
                "file": file_q.as_dict(),
            },
            "page_url": best.get("page_url", ""),
            "title": best.get("title", ""),
            "subject_subtype": subject_subtype,
        })
    except Exception as e:
        result.update({
            "ok": False,
            "reason": "download-failed",
            "error": str(e),
            "image_url": best.get("image_url"),
            "engine": best.get("engine"),
            "score": best.get("score"),
            "subject_subtype": subject_subtype,
        })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
