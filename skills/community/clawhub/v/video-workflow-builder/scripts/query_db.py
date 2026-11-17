#!/usr/bin/env python3
"""Query the content asset DB: dedup search, series listing, top ranking."""
import argparse
import json
import os
import sys

import content_db as cdb
import archive_content as ac


def load_entries(data_root=None):
    data_root = data_root or cdb.resolve_data_root()
    path = os.path.join(data_root, "index.json")
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f).get("entries", [])
        except ValueError:
            pass
    return ac.rebuild_index(data_root).get("entries", [])


def search(keyword, data_root=None):
    kw = keyword.lower()
    out = []
    for e in load_entries(data_root):
        hay = " ".join([e.get("topic", ""), e.get("title", ""),
                        " ".join(e.get("tags", []))]).lower()
        if kw in hay:
            out.append(e)
    return out


def list_series(name, data_root=None):
    members = [e for e in load_entries(data_root) if e.get("series") == name]
    return sorted(members, key=lambda e: e.get("created", ""))


def top(n, by="views", data_root=None):
    def key(e):
        v = (e.get("metrics") or {}).get(by)
        return v if isinstance(v, (int, float)) else float("-inf")
    return sorted(load_entries(data_root), key=key, reverse=True)[:n]


def _print(entries):
    for e in entries:
        print("%s | %s | %s | series=%s | status=%s" % (
            e.get("created", ""), e.get("id", ""), e.get("title", ""),
            e.get("series", "") or "-", e.get("status", "")))


def main(argv):
    p = argparse.ArgumentParser(description="Query the content asset DB")
    p.add_argument("--search")
    p.add_argument("--series")
    p.add_argument("--top", type=int)
    p.add_argument("--by", default="views")
    args = p.parse_args(argv)
    if args.search is not None:
        _print(search(args.search))
    elif args.series is not None:
        _print(list_series(args.series))
    elif args.top is not None:
        _print(top(args.top, by=args.by))
    else:
        _print(sorted(load_entries(), key=lambda e: e.get("created", ""), reverse=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
