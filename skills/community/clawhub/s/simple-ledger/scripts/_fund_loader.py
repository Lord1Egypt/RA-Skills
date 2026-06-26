#!/usr/bin/env python3
"""基金搜索辅助脚本（子进程级别隔离，输出纯 JSON）"""
import sys
import json
from pathlib import Path

def search(name):
    import akshare as ak
    df = ak.fund_name_em()
    name_lower = name.lower()
    exact = df[df["基金简称"] == name]
    if len(exact) > 0:
        return [{"code": r["基金代码"], "name": r["基金简称"], "exact": True}
                for _, r in exact.iterrows()]
    contains = df[df["基金简称"].str.contains(name, na=False)]
    return [{"code": r["基金代码"], "name": r["基金简称"], "exact": False}
            for _, r in contains.head(10).iterrows()]

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    results = search(name) if name else []
    print(json.dumps({"results": results}, ensure_ascii=False))