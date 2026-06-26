#!/usr/bin/env python3
"""
代码搜索模块

根据基金/股票名称联网查询代码。
股票用 akshare 直接调用（无进度条）；基金用子进程隔离（防 tqdm 干扰）。

用法:
    python lookup_code.py "洛阳钼业"
    python lookup_code.py "有色金属ETF南方"
    python lookup_code.py "沪深300ETF"
"""

import json
import subprocess
import sys
from pathlib import Path

# ==================== 搜索逻辑 ====================

def search_stock(name: str) -> list[dict]:
    """搜索 A 股股票代码（akshare 直调，无进度条）"""
    try:
        import akshare as ak
        df = ak.stock_info_a_code_name()
    except Exception:
        return []

    exact = df[df["name"] == name]
    if len(exact) > 0:
        return [{"code": r["code"], "name": r["name"], "type": "股票", "exact": True}
                for _, r in exact.iterrows()]

    contains = df[df["name"].str.contains(name, na=False)]
    return [{"code": r["code"], "name": r["name"], "type": "股票", "exact": False}
            for _, r in contains.head(10).iterrows()]


def search_fund(name: str) -> list[dict]:
    """搜索基金代码（子进程隔离，彻底压制 tqdm 进度条）"""
    script = Path(__file__).resolve().parent / "_fund_loader.py"
    try:
        result = subprocess.run(
            [sys.executable, str(script), name],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=60,
        )
        if result.stdout.strip():
            data = json.loads(result.stdout.strip())
            return [{"code": r["code"], "name": r["name"], "type": "基金", "exact": r.get("exact", False)}
                    for r in data.get("results", [])]
    except Exception:
        pass
    return []


def search(name: str, type_hint: str = "auto") -> dict:
    """
    搜索代码，返回结构化结果。

    返回结构:
    {
        "found": bool,
        "results": [...],
        "primary": {...} or None,
        "type": "基金" or "股票" or None,
        "message": str
    }
    """
    if not name or not name.strip():
        return {"found": False, "results": [], "primary": None, "type": None, "message": "名称不能为空"}

    name = name.strip()

    stock_results = search_stock(name) if type_hint in ("auto", "stock") else []
    fund_results = search_fund(name) if type_hint in ("auto", "基金") else []

    all_results = stock_results + fund_results
    exact = [r for r in all_results if r.get("exact")]
    inexact = [r for r in all_results if not r.get("exact")]
    candidates = exact + inexact

    # 去重
    seen = set()
    unique = []
    for r in candidates:
        if r["code"] not in seen:
            seen.add(r["code"])
            unique.append(r)

    if not unique:
        return {
            "found": False, "results": [], "primary": None, "type": None,
            "message": f"未找到与「{name}」相关的股票或基金"
        }

    if len(unique) == 1:
        primary = unique[0]
        return {
            "found": True, "results": unique, "primary": primary,
            "type": primary["type"],
            "message": f"找到 {primary['type']}：{primary['name']}（{primary['code']}）",
        }

    types_in_results = list({r["type"] for r in unique})
    type_str = "、".join(types_in_results)
    primary = exact[0] if exact else unique[0]
    msg = f"找到 {len(unique)} 个结果，推荐：{primary['name']}（{primary['code']}）" if exact \
        else f"找到 {len(unique)} 个候选，请选择："

    return {
        "found": True, "results": unique, "primary": primary,
        "type": types_in_results[0] if len(types_in_results) == 1 else None,
        "message": msg,
    }


# ==================== CLI ====================

def main():
    if len(sys.argv) < 2:
        print("用法: python lookup_code.py <名称> [--type stock|fund]")
        sys.exit(1)

    name = sys.argv[1]
    type_hint = "auto"

    result = search(name, type_hint)

    # 输出纯 JSON（供 invest.py 调用）
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 人类可读部分（stderr，不干扰 JSON）
    print("\n─── 搜索结果 ───", file=sys.stderr)
    if not result["found"]:
        print(f"  ❌ {result['message']}", file=sys.stderr)
    elif len(result["results"]) == 1:
        r = result["results"][0]
        print(f"  ✅ 唯一结果：{r['name']}（{r['code']}）<{r['type']}>", file=sys.stderr)
    else:
        print(f"  📋 {result['message']}", file=sys.stderr)
        for i, r in enumerate(result["results"], 1):
            marker = "← 推荐" if r == result["primary"] else ""
            print(f"    {i}. {r['name']}（{r['code']}）<{r['type']}> {marker}", file=sys.stderr)


if __name__ == "__main__":
    main()