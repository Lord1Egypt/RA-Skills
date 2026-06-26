#!/usr/bin/env python3
"""方法B：随机组字 + Tavily搜索撞域。

用法：
  python3 search_char.py                        # 随机取2字→搜→打印结果
  python3 search_char.py --dry-run              # 只取字不搜索（调试用）
  python3 search_char.py --query 键绒           # 用指定词搜索（跳过随机取字）

返回JSON: {chars, query, results:[{title,url,snippet}], chosen, domain}
"""
import argparse, json, os, pathlib, random, re, subprocess, sys, urllib.request

CHAR_FILE = pathlib.Path(__file__).parent.parent / "references" / "common-chinese-chars.txt"
TAVILY_SCRIPT = pathlib.Path.home() / ".hermes" / "skills" / "openclaw-imports" / "openclaw-tavily-search" / "scripts" / "tavily_search.py"

def load_chars():
    txt = CHAR_FILE.read_text(encoding="utf-8", errors="ignore")
    seen = set()
    uniq = []
    for c in txt:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq

def pick_chars(chars):
    i, j = random.sample(range(len(chars)), 2)
    return chars[i], chars[j]

def make_query(a, b):
    """试两种组合，选看起来更有故事的"""
    c1, c2 = a + b, b + a
    return c1 if random.random() > 0.5 else c2

def tavily_search(query, max_results=3):
    """调用Tavily脚本搜索"""
    if not TAVILY_SCRIPT.exists():
        return None
    result = subprocess.run(
        [sys.executable, str(TAVILY_SCRIPT), "--query", query,
         "--max-results", str(max_results), "--format", "brave"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout)
        return data.get("results", [])
    except json.JSONDecodeError:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="只取字不搜索")
    parser.add_argument("--query", type=str, help="指定搜索词（跳过随机取字）")
    args = parser.parse_args()

    if args.query:
        query = args.query
        chars_a, chars_b = None, None
    else:
        chars = load_chars()
        chars_a, chars_b = pick_chars(chars)
        query = make_query(chars_a, chars_b)

    output = {
        "chars": {"a": chars_a, "b": chars_b},
        "query": query,
        "results": [],
        "chosen": None,
        "domain": None,
        "status": "skipped" if args.dry_run else "pending"
    }

    if args.dry_run:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    results = tavily_search(query)
    if results is None or len(results) == 0:
        output["status"] = "search_failed"
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    output["results"] = results[:3]
    output["status"] = "found"
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
