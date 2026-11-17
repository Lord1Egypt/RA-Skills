#!/usr/bin/env python3
"""Archive one produced piece of content into the asset DB."""
import argparse
import datetime
import json
import os
import sys

import content_db as cdb

_METRIC_KEYS = ["views", "likes", "comments", "shares", "completion_rate", "notes"]


def _empty_metrics():
    return {k: None for k in _METRIC_KEYS}


def _load_index(data_root):
    path = os.path.join(data_root, "index.json")
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except ValueError:
            pass
    return {"updated": "", "entries": []}


def _write_index(data_root, index):
    index["updated"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(os.path.join(data_root, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def _index_entry(meta):
    return {
        "id": meta["id"], "created": meta["created"], "topic": meta["topic"],
        "title": meta["title"], "series": meta.get("series", ""),
        "tags": meta.get("tags", []), "status": meta["status"],
        "platform": meta.get("platform", []), "metrics": meta.get("metrics", {}),
    }


def rebuild_index(data_root):
    content_dir = os.path.join(data_root, "content")
    if not os.path.isdir(content_dir):
        return {"updated": "", "entries": []}
    index = {"updated": "", "entries": []}
    for name in sorted(os.listdir(content_dir)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(content_dir, name), encoding="utf-8") as f:
            meta, _ = cdb.parse_frontmatter(f.read())
        if meta:
            index["entries"].append(_index_entry(meta))
    _write_index(data_root, index)
    return index


def _append_series_member(data_root, series, member_id, created):
    series_dir = os.path.join(data_root, "series")
    os.makedirs(series_dir, exist_ok=True)
    path = os.path.join(series_dir, cdb.slugify(series) + ".md")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            meta, body = cdb.parse_frontmatter(f.read())
    else:
        meta = {"name": series, "slug": cdb.slugify(series),
                "created": created, "positioning": "", "members": []}
        body = "（系列备注:形态约定、开场固定话术、已覆盖角度等）\n"
    members = meta.get("members", [])
    if member_id not in members:
        members.append(member_id)
    meta["members"] = members
    with open(path, "w", encoding="utf-8") as f:
        f.write(cdb.dump_frontmatter(meta) + "\n" + body)


def archive(topic, title, script_body, platform, tags,
            series="", created=None, data_root=None):
    data_root = data_root or cdb.resolve_data_root()
    created = created or datetime.date.today().isoformat()
    content_dir = os.path.join(data_root, "content")
    os.makedirs(content_dir, exist_ok=True)
    base_id = "%s-%s" % (created, cdb.slugify(topic))
    content_id = base_id
    md_path = os.path.join(content_dir, content_id + ".md")
    n = 2
    while os.path.exists(md_path):
        content_id = "%s-%d" % (base_id, n)
        md_path = os.path.join(content_dir, content_id + ".md")
        n += 1
    meta = {
        "id": content_id, "created": created, "platform": platform,
        "topic": topic, "title": title, "series": series or "",
        "tags": tags, "status": "pending", "publish_date": "",
        "metrics": _empty_metrics(),
    }
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(cdb.dump_frontmatter(meta) + "\n" + script_body.rstrip() + "\n")
    index = _load_index(data_root)
    index["entries"] = [e for e in index["entries"] if e["id"] != content_id]
    index["entries"].append(_index_entry(meta))
    _write_index(data_root, index)
    if series:
        _append_series_member(data_root, series, content_id, created)
    return md_path


def main(argv):
    p = argparse.ArgumentParser(description="Archive content into the asset DB")
    p.add_argument("--topic", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--script", required=True, help="script body file path, or - for stdin")
    p.add_argument("--platform", default="", help="comma-separated")
    p.add_argument("--tags", default="", help="comma-separated")
    p.add_argument("--series", default="")
    args = p.parse_args(argv)
    body = sys.stdin.read() if args.script == "-" else open(args.script, encoding="utf-8").read()
    platform = [x.strip() for x in args.platform.split(",") if x.strip()]
    tags = [x.strip() for x in args.tags.split(",") if x.strip()]
    path = archive(args.topic, args.title, body, platform, tags, series=args.series)
    print("archived:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
