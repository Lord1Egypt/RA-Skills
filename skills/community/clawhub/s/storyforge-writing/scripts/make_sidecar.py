#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_sidecar.py — 按 `sf-c14n-v1` 生成/刷新旁车 `<stem>.provenance.json`（零依赖）。

用法：
  python scripts/make_sidecar.py <framework.json>            # 只打印将写入的旁车（dry-run）
  python scripts/make_sidecar.py <framework.json> --write    # 写入 <stem>.provenance.json

行为（只做**机械可复算**的部分，证据判断留给作者/agent）：
  · 每张表一条 blockProvenance：`table` / `recordCount` / `contentHash` 由主文件**复算**；
  · 已有旁车中的 `evidenceGrade` / `sources` / `notes` **原样保留**（按 table 匹配）；
  · 新表默认 `evidenceGrade: "UNKNOWN"`、`sources: []`、**不写 notes** ——
    这样校验器会报 `EVIDENCE_SILENT_ABSENT`，逼作者把来源补上或显式声明原因（不替人编证据）；
  · 主文件里已不存在的表：从旁车移除并在 stderr 提示；
  · 顶层写 `hashCanonicalization: "sf-c14n-v1"`，此后哈希不一致即 ERROR（可复算）。
"""
import datetime
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from sf_hash import CANONICALIZATION, records_by_table, records_hash  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 1 or not os.path.isfile(args[0]):
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    path = args[0]
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    by_table = records_by_table(d.get("blocks"))
    stem = os.path.splitext(os.path.basename(path))[0]
    out_p = os.path.join(os.path.dirname(os.path.abspath(path)), stem + ".provenance.json")
    old = {}
    if os.path.isfile(out_p):
        with open(out_p, encoding="utf-8") as fh:
            old = json.load(fh)
    prev = {it.get("table"): it for it in (old.get("blockProvenance") or old.get("blocks") or [])
            if isinstance(it, dict)}
    items = []
    for t, recs in by_table.items():
        it = dict(prev.get(t) or {"evidenceGrade": "UNKNOWN", "sources": []})
        it.update({"table": t, "recordCount": len(recs), "contentHash": records_hash(recs)})
        items.append({k: it[k] for k in ("table", "recordCount", "contentHash", "evidenceGrade", "sources")}
                     | {k: v for k, v in it.items()
                        if k not in ("table", "recordCount", "contentHash", "evidenceGrade", "sources")})
    for t in sorted(set(prev) - set(by_table), key=str):
        print("提示：旁车中的表 %s 已不在主文件中，已移除" % t, file=sys.stderr)
    side = {k: v for k, v in old.items() if k not in ("blocks", "blockProvenance")}
    side.update({
        "storyforgeFramework": d.get("storyforgeFramework", side.get("storyforgeFramework")),
        "generatedAt": datetime.date.today().isoformat(),
        "hashAlgorithm": "sha256",
        "hashCanonicalization": CANONICALIZATION,
        "recordsFile": os.path.basename(path),
        "blockProvenance": items,
    })
    if "baseline" in d and "baseline" not in side:
        side["baseline"] = d["baseline"]
    text = json.dumps(side, ensure_ascii=False, indent=2) + "\n"
    if write:
        with open(out_p, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("已写入 %s（%d 张表）" % (out_p, len(items)))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
