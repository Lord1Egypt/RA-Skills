#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sf_hash.py — 框架语料的**规范化哈希**（`sf-c14n-v1`，零依赖）。

单一来源：`check_framework_artifact.py`（复算校验）与 `make_sidecar.py`（生成旁车）都只从这里取算法，
避免「生成一套、校验一套」。规则见 `contracts/S-data-envelope.md` §3.1。

sf-c14n-v1：
  1. 取主文件 `blocks[]` 中 **同一 `table`** 的全部 `records`，按出现顺序拼成一个 list；
  2. `json.dumps(list, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`；
  3. UTF-8 编码后取 SHA-256，写作 `sha256:<64 位小写十六进制>`。
"""
import hashlib
import json

CANONICALIZATION = "sf-c14n-v1"


def canonical_bytes(records):
    return json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def records_hash(records):
    return "sha256:" + hashlib.sha256(canonical_bytes(records)).hexdigest()


def records_by_table(blocks):
    """`blocks[]` → `{table: [records...]}`（保持首次出现顺序；同表多块按顺序合并）。"""
    out = {}
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        t = b.get("table")
        recs = b.get("records") or []
        out.setdefault(t, []).extend(recs if isinstance(recs, list) else [])
    return out
