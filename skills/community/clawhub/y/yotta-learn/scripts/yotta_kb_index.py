#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_kb_index.py — 元习知识库索引与查询（文件式分片倒排）。

切词：拉丁按符号边界 + 中文 bigram（2-gram，单字兜底）。
索引：每分类一个 index.json 分片 + 全局词表 index/global.json；
查询先查全局词表定位候选分类、只加载命中分片；索引漂移自动降级线性扫描。
零依赖（Python 3.8+ 标准库）；索引为派生数据，可随时重建。
"""
import hashlib
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

import yotta_kb as kb

_LATIN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_+#./-]*")
_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")


# ── 切词 ────────────────────────────────────────────────────────────────────

def tokenize_document(text):
    """文档切词：拉丁 token + 中文 bigram + 单字（供单字查询兜底）。"""
    text = (text or "").lower()
    tokens = []
    for m in _LATIN_RE.finditer(text):
        tok = m.group(0).strip(".-/+#")
        if tok:
            tokens.append(tok)
    for m in _CJK_RE.finditer(text):
        run = m.group(0)
        if len(run) == 1:
            tokens.append(run)
        else:
            tokens.extend(run[i:i + 2] for i in range(len(run) - 1))
            tokens.extend(run)
    return tokens


def tokenize_query(text):
    """查询切词：拉丁 token + 中文 bigram（单字查询回退到单字）。"""
    text = (text or "").lower()
    tokens = []
    for m in _LATIN_RE.finditer(text):
        tok = m.group(0).strip(".-/+#")
        if tok:
            tokens.append(tok)
    for m in _CJK_RE.finditer(text):
        run = m.group(0)
        if len(run) == 1:
            tokens.append(run)
        else:
            tokens.extend(run[i:i + 2] for i in range(len(run) - 1))
    return tokens


def _field_tokens(entry):
    title = Counter(tokenize_document(entry.title))
    tags = Counter(tokenize_document(" ".join(entry.tags)))
    body = Counter(tokenize_document(entry.body))
    return title, tags, body


# ── 索引构建 ────────────────────────────────────────────────────────────────

def dir_source_hash(entries_path):
    """条目目录指纹：文件名 + mtime_ns + size 汇总（不读文件内容）。"""
    h = hashlib.sha1()
    p = Path(entries_path)
    if p.is_dir():
        for f in sorted(p.glob("*.md")):
            try:
                st = f.stat()
            except OSError:
                continue
            h.update(("%s:%d:%d\n" % (f.name, st.st_mtime_ns, st.st_size)).encode("utf-8"))
    return h.hexdigest()


def build_category_shard(root, slug):
    d = kb.entries_dir(root, slug)
    terms = {}
    entries_meta = {}
    count = 0
    if d.is_dir():
        for f in sorted(d.glob("*.md")):
            entry = kb.load_entry(f)
            count += 1
            st = f.stat()
            entries_meta[entry.id] = {"mtime_ns": st.st_mtime_ns, "size": st.st_size}
            t, g, b = _field_tokens(entry)
            for term in set(t) | set(g) | set(b):
                posting = terms.setdefault(term, {})
                posting[entry.id] = [t.get(term, 0), g.get(term, 0), b.get(term, 0)]
    shard = {
        "schema": kb.INDEX_SCHEMA, "category": slug, "built_at": kb.now_iso(),
        "source_hash": dir_source_hash(d), "entry_count": count,
        "entries": entries_meta, "terms": terms,
    }
    kb.atomic_write_json(kb.category_index_path(root, slug), shard)
    return shard


def build_global_index(root):
    categories_meta = {}
    terms = {}
    for cat in kb.list_categories(root):
        slug = cat["slug"]
        shard_path = kb.category_index_path(root, slug)
        shard = None
        if shard_path.exists():
            try:
                shard = kb.load_json(shard_path, where="index.json(%s)" % slug,
                                     schema=kb.INDEX_SCHEMA)
            except kb.KbError:
                shard = None
        cur_hash = dir_source_hash(kb.entries_dir(root, slug))
        if shard is None or shard.get("source_hash") != cur_hash:
            shard = build_category_shard(root, slug)
        categories_meta[slug] = {"count": shard.get("entry_count", 0),
                                 "source_hash": shard.get("source_hash")}
        for term in shard.get("terms", {}):
            bucket = terms.setdefault(term, [])
            if slug not in bucket:
                bucket.append(slug)
    for bucket in terms.values():
        bucket.sort()
    g = {"schema": kb.GLOBAL_SCHEMA, "built_at": kb.now_iso(),
         "categories": categories_meta, "terms": terms}
    kb.atomic_write_json(kb.global_index_path(root), g)
    return g


def build_stats(root):
    by_status = {}
    by_category = {}
    total = 0
    for cat in kb.list_categories(root):
        slug = cat["slug"]
        n = 0
        d = kb.entries_dir(root, slug)
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                entry = kb.load_entry(f)
                total += 1
                n += 1
                by_status[entry.status] = by_status.get(entry.status, 0) + 1
        by_category[slug] = n
    terms = 0
    try:
        g = kb.load_json(kb.global_index_path(root), where="global.json",
                         schema=kb.GLOBAL_SCHEMA)
        if g:
            terms = len(g.get("terms", {}))
    except kb.KbError:
        terms = 0
    stats = {"schema": kb.STATS_SCHEMA, "built_at": kb.now_iso(),
             "total_entries": total, "by_status": by_status,
             "by_category": by_category, "terms": terms}
    kb.atomic_write_json(kb.stats_path(root), stats)
    return stats


def refresh(root, slugs=None):
    """增量刷新：重建受影响分类分片 + 全局词表 + 统计。"""
    if slugs:
        for slug in slugs:
            build_category_shard(root, slug)
    else:
        for cat in kb.list_categories(root):
            build_category_shard(root, cat["slug"])
    build_global_index(root)
    return build_stats(root)


def rebuild_all(root):
    return refresh(root)


def index_status(root):
    report = []
    drift = False
    for cat in kb.list_categories(root):
        slug = cat["slug"]
        shard_path = kb.category_index_path(root, slug)
        shard = None
        if shard_path.exists():
            try:
                shard = kb.load_json(shard_path, where="index.json(%s)" % slug,
                                     schema=kb.INDEX_SCHEMA)
            except kb.KbError:
                shard = None
        cur = dir_source_hash(kb.entries_dir(root, slug))
        is_drift = shard is None or shard.get("source_hash") != cur
        drift = drift or is_drift
        report.append({
            "slug": slug, "drift": is_drift,
            "built_at": (shard or {}).get("built_at", ""),
            "entries": (shard or {}).get("entry_count", 0),
        })
    g = None
    try:
        g = kb.load_json(kb.global_index_path(root), where="global.json",
                         schema=kb.GLOBAL_SCHEMA)
    except kb.KbError:
        g = None
    global_drift = g is None
    if g is not None:
        meta = g.get("categories", {})
        current = set(c["slug"] for c in kb.list_categories(root))
        if set(meta.keys()) != current:
            global_drift = True
        else:
            for slug, m in meta.items():
                if m.get("source_hash") != dir_source_hash(kb.entries_dir(root, slug)):
                    global_drift = True
                    break
    return {"categories": report, "global_drift": global_drift,
            "drift": drift or global_drift}


# ── 查询 ────────────────────────────────────────────────────────────────────

def _bonus(entry, now):
    bonus = {"verified": 1.0, "draft": 0.0, "deprecated": -1.0}.get(entry.status, 0.0)
    bonus += {"high": 0.5, "medium": 0.0, "low": -0.5}.get(entry.confidence, 0.0)
    decay = 1.0
    try:
        dt = datetime.fromisoformat(entry.updated)
        if dt.tzinfo is None:
            dt = dt.astimezone()
        age = max(0.0, (now - dt).total_seconds() / 86400.0)
        decay = 0.5 ** (age / 365.0)
    except (TypeError, ValueError):
        decay = 1.0
    return bonus * decay


def _result(entry, score, coverage):
    return {
        "id": entry.id, "title": entry.title, "category": entry.category,
        "status": entry.status, "confidence": entry.confidence,
        "score": round(score, 4), "coverage": round(coverage, 4),
        "updated": entry.updated, "tags": entry.tags,
    }


def _tag_match(entry, tags_lower):
    if not tags_lower:
        return True
    entry_tags = [t.lower() for t in entry.tags]
    return any(t in entry_tags for t in tags_lower)


def _linear_query(root, q_tokens, cat_slug, status_set, tags_lower, now):
    out = []
    slugs = [cat_slug] if cat_slug else [c["slug"] for c in kb.list_categories(root)]
    for slug in slugs:
        d = kb.entries_dir(root, slug)
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            entry = kb.load_entry(f)
            if entry.status not in status_set or not _tag_match(entry, tags_lower):
                continue
            t, g, b = _field_tokens(entry)
            score = 0.0
            coverage = 0
            for tok in q_tokens:
                s = 5 * t.get(tok, 0) + 3 * g.get(tok, 0) + 1 * b.get(tok, 0)
                if s > 0:
                    coverage += 1
                score += s
            if score <= 0:
                continue
            out.append(_result(entry, score + _bonus(entry, now),
                               coverage / float(len(q_tokens))))
    return out


def _global_stale(root, g):
    meta = g.get("categories", {})
    current = set(c["slug"] for c in kb.list_categories(root))
    if set(meta.keys()) != current:
        return True
    for slug, m in meta.items():
        if m.get("source_hash") != dir_source_hash(kb.entries_dir(root, slug)):
            return True
    return False


def query(root, text, category=None, statuses=None, tags=None, limit=10,
          include_draft=False, include_deprecated=False, now=None):
    """查询知识条目；索引漂移时自动降级线性扫描（结果附 mode / stale）。"""
    q_tokens = tokenize_query(text)
    if not q_tokens:
        raise kb.KbUsageError("查询词为空或无法切分")
    q_tokens = list(dict.fromkeys(q_tokens))
    cat_slug = None
    if category:
        cat_slug = kb.resolve_category(root, category)["slug"]
    if statuses:
        for s in statuses:
            if s not in kb.ENTRY_STATUSES:
                raise kb.KbUsageError("status 非法：%s（可用 %s）"
                                      % (s, " / ".join(kb.ENTRY_STATUSES)))
    else:
        statuses = ["verified", "draft"] if include_draft else ["verified"]
        if include_deprecated:
            statuses.append("deprecated")
    status_set = set(statuses)
    tags_lower = [t.lower() for t in (tags or []) if t]
    now = now or datetime.now().astimezone()

    g = None
    try:
        g = kb.load_json(kb.global_index_path(root), where="global.json",
                         schema=kb.GLOBAL_SCHEMA)
    except kb.KbError:
        g = None
    stale = g is None or _global_stale(root, g)
    results = []
    if stale:
        results = _linear_query(root, q_tokens, cat_slug, status_set, tags_lower, now)
    else:
        candidates = set()
        for tok in q_tokens:
            candidates.update(g.get("terms", {}).get(tok, []))
        if cat_slug:
            candidates &= {cat_slug}
        for slug in sorted(candidates):
            shard = None
            try:
                shard = kb.load_json(kb.category_index_path(root, slug),
                                     where="index.json(%s)" % slug,
                                     schema=kb.INDEX_SCHEMA)
            except kb.KbError:
                shard = None
            if shard is None or shard.get("source_hash") != dir_source_hash(kb.entries_dir(root, slug)):
                stale = True
                results.extend(_linear_query(root, q_tokens, slug, status_set,
                                             tags_lower, now))
                continue
            scores = {}
            coverage = {}
            for tok in q_tokens:
                post = shard.get("terms", {}).get(tok, {})
                for eid, tf in post.items():
                    scores[eid] = scores.get(eid, 0) + 5 * tf[0] + 3 * tf[1] + 1 * tf[2]
                    coverage[eid] = coverage.get(eid, 0) + 1
            for eid, base_score in scores.items():
                path = kb.entries_dir(root, slug) / (eid + ".md")
                if not path.is_file():
                    continue
                entry = kb.load_entry(path)
                if entry.status not in status_set or not _tag_match(entry, tags_lower):
                    continue
                results.append(_result(entry, base_score + _bonus(entry, now),
                                       coverage[eid] / float(len(q_tokens))))

    results.sort(key=lambda r: r["id"])
    results.sort(key=lambda r: r["updated"] or "", reverse=True)
    results.sort(key=lambda r: (-r["score"], -r["coverage"]))
    total = len(results)
    if limit and limit > 0:
        results = results[:limit]
    return {"query": text, "mode": "linear" if stale else "index",
            "stale": stale, "count": total, "results": results}


def stats(root):
    """实时统计（管理视图）：条目分布 + 索引健康 + 回收站。"""
    by_status = {}
    by_category = {}
    total = 0
    cats = kb.list_categories(root)
    for cat in cats:
        slug = cat["slug"]
        n = 0
        d = kb.entries_dir(root, slug)
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                entry = kb.load_entry(f)
                total += 1
                n += 1
                by_status[entry.status] = by_status.get(entry.status, 0) + 1
        by_category[slug] = {"name": cat["name"], "status": cat["status"], "entries": n}
    idx = index_status(root)
    return {
        "total": total, "by_status": by_status, "by_category": by_category,
        "categories": len(cats), "index_drift": idx["drift"],
        "trash": len(kb.list_trash(root)), "root": str(root),
    }
