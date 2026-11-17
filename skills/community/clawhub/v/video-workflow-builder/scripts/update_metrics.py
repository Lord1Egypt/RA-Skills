#!/usr/bin/env python3
"""Backfill post-publish metrics for an archived content item."""
import argparse
import os
import sys

import content_db as cdb
import archive_content as ac


def update(content_id, metrics, publish_date="", data_root=None):
    data_root = data_root or cdb.resolve_data_root()
    md_path = os.path.join(data_root, "content", content_id + ".md")
    if not os.path.isfile(md_path):
        raise FileNotFoundError("no such content: %s" % md_path)
    with open(md_path, encoding="utf-8") as f:
        meta, body = cdb.parse_frontmatter(f.read())
    current = meta.get("metrics") or {}
    for k, v in metrics.items():
        if v is not None:
            current[k] = v
    meta["metrics"] = current
    if publish_date:
        meta["publish_date"] = publish_date
    meta["status"] = "published"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(cdb.dump_frontmatter(meta) + "\n" + body.rstrip() + "\n")
    ac.rebuild_index(data_root)
    return md_path


def main(argv):
    p = argparse.ArgumentParser(description="Backfill metrics for content")
    p.add_argument("--id", required=True)
    p.add_argument("--publish-date", default="")
    p.add_argument("--views", type=int)
    p.add_argument("--likes", type=int)
    p.add_argument("--comments", type=int)
    p.add_argument("--shares", type=int)
    p.add_argument("--completion-rate", type=float)
    p.add_argument("--notes")
    args = p.parse_args(argv)
    metrics = {
        "views": args.views, "likes": args.likes, "comments": args.comments,
        "shares": args.shares, "completion_rate": args.completion_rate,
        "notes": args.notes,
    }
    path = update(args.id, metrics, publish_date=args.publish_date)
    print("updated:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
