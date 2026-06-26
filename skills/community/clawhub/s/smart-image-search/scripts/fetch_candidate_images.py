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

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


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


def download(url: str, query: str, idx: int):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.bing.com/"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type")
    ext = guess_ext(url, content_type)
    safe = re.sub(r"[^\w\-\u4e00-\u9fff]+", "_", query).strip("_") or "image"
    out_dir = Path("/home/mumu/clawd/tmp/search-image")
    out_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=f"{safe}_{idx}_", suffix=ext, dir=out_dir)
    os.close(fd)
    with open(tmp_path, "wb") as f:
        f.write(data)
    return tmp_path, len(data), content_type


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fetch_candidate_images.py <query> [count]", file=sys.stderr)
        return 1
    query = sys.argv[1].strip()
    cli_count = int(sys.argv[2]) if len(sys.argv) > 2 else None

    params = parse_query_params(query)
    search_query = params["core_query"]
    count = cli_count or params.get("count") or 3
    count = max(1, min(5, count))

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

    picked = candidates[:count]
    downloads = []
    for idx, item in enumerate(picked, start=1):
        try:
            url_q = url_quality_hints(item["image_url"])
            if not url_q.accept:
                downloads.append({
                    "ok": False,
                    "index": idx,
                    "reason": "rejected-by-url-quality",
                    "quality": url_q.as_dict(),
                    **item,
                })
                continue
            path, size, content_type = download(item["image_url"], query, idx)
            file_q = inspect_file(path, intent_info["intent"])
            if not file_q.accept:
                downloads.append({
                    "ok": False,
                    "index": idx,
                    "reason": "rejected-by-file-quality",
                    "path": path,
                    "size": size,
                    "content_type": content_type,
                    "quality": file_q.as_dict(),
                    **item,
                })
                continue
            downloads.append({
                "ok": True,
                "index": idx,
                "path": path,
                "size": size,
                "content_type": content_type,
                "quality": {
                    "url": url_q.as_dict(),
                    "file": file_q.as_dict(),
                },
                **item,
            })
        except Exception as e:
            downloads.append({
                "ok": False,
                "index": idx,
                "error": str(e),
                **item,
            })
    out = {
        "query": query,
        "parsed_params": params,
        "search_query": search_query,
        "intent": intent_info,
        "subject_subtype": subject_subtype,
        "confidence": confidence,
        "top_candidates": picked,
        "downloads": downloads,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
