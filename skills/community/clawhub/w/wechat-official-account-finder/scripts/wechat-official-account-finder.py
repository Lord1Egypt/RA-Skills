#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公众号找号 —— 曼格云 skill（统一底座，source=wechat-official-account-finder）

用法：
  python scripts/wechat-official-account-finder.py --list
  python scripts/wechat-official-account-finder.py --estimate <端点> [参数]
  python scripts/wechat-official-account-finder.py <端点> [k=v ...] [--yes] [--format json|markdown|excel] [--report] [--output=路径] [--pages=N]
"""
import os
import sys
import json
from platform_contract import snapshot

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wm_core import WM, estimate, print_estimate, require_key, load_key, key_url, Formatter, EP, EXIT_INPUT, EXIT_OK

SLUG = "wechat-official-account-finder"
SOURCE = "clawhub"
KEY_URL = key_url(SOURCE)
ENDPOINTS = ['mp-search-accounts', 'mp-account-profile']
REQ_NAMES = {"url", "ghid", "keyword", "query", "secUid", "accountId",
             "shareUrl", "objectId", "exportId", "videoId", "fileUrl", "videoUrl", "biz"}


def parse(argv):
    params = {}
    fmt = "markdown"
    report = False
    output = None
    yes = False
    pages = 1
    file_path = None
    positional = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--file":
            i += 1
            if i < len(argv):
                file_path = argv[i]
        elif a.startswith("--file="):
            file_path = a.split("=", 1)[1]
        elif a == "--format":
            i += 1
            if i < len(argv):
                fmt = argv[i]
        elif a.startswith("--format="):
            fmt = a.split("=", 1)[1]
        elif a == "--output":
            i += 1
            if i < len(argv):
                output = argv[i]
        elif a.startswith("--output="):
            output = a.split("=", 1)[1]
        elif a == "--pages":
            i += 1
            try:
                pages = max(1, int(argv[i]))
            except (ValueError, IndexError):
                pages = 1
        elif a.startswith("--pages="):
            try:
                pages = max(1, int(a.split("=", 1)[1]))
            except ValueError:
                pages = 1
        elif a == "--report":
            report = True
        elif a == "--yes" or a == "-y":
            yes = True
        elif "=" in a:
            k, v = a.split("=", 1)
            params[k] = v
        else:
            positional.append(a)
        i += 1
    endpoint = next((p for p in positional if p in EP), None)
    for name, value in list(params.items()):
        kind = EP.get(endpoint, {}).get("param_types", {}).get(name, "string")
        if kind in ("integer", "number"):
            params[name] = int(value) if kind == "integer" else float(value)
        elif kind in ("boolean", "array", "object"):
            params[name] = json.loads(value)
    return positional, params, fmt, report, output, yes, pages, file_path


def main():
    snapshot_path = next((arg.split("=", 1)[1] for arg in sys.argv[1:] if arg.startswith("--snapshot=")), None)
    checkpoint_path = next((arg.split("=", 1)[1] for arg in sys.argv[1:] if arg.startswith("--checkpoint=")), None)
    argv = [arg for arg in sys.argv[1:] if not arg.startswith(("--snapshot=", "--checkpoint="))]
    positional, params, fmt, report, output, yes, pages, file_path = parse(argv)
    is_help = not positional or positional[0] in ("-h", "--help", "--list")
    is_est = bool(positional) and positional[0] == "--estimate"

    if is_help:
        print("可用端点：")
        for k in ENDPOINTS:
            e = EP[k]
            print("  {:32s} {:4s} {}".format(k, e["method"], e["name"]))
        print("")
        print("示例: python scripts/wechat-official-account-finder.py <端点> --yes url=链接 --format excel")
        sys.exit(EXIT_OK)

    if is_est:
        print_estimate(estimate([(k, params) for k in positional[1:]], pages=pages), title="公众号找号 费用预估")
        sys.exit(EXIT_OK)

    key = positional[0]
    if key not in ENDPOINTS:
        print("该 skill 不含端点 {!r}，可用：{}".format(key, ", ".join(ENDPOINTS)), file=sys.stderr)
        sys.exit(EXIT_INPUT)
    ep = EP[key]
    unknown = set(params) - set(ep.get("params", []))
    if unknown:
        raise ValueError("当前接口不支持参数：" + ", ".join(sorted(unknown)))
    if file_path and not any(p in ep.get("params", []) for p in ("videoUrl", "audioUrl")):
        raise ValueError("当前接口不接受本地文件")
    for field in ("videoUrl", "audioUrl"):
        if field in params and not str(params[field]).startswith("https://"):
            raise ValueError("媒体地址必须是 HTTPS；上传本地媒体请明确使用 --file")

    # 说明：参数合法性交由服务端校验（返回中文错误更明确），此处不做强校验，
    # 避免把可选项（如 ghid 与 url 二选一）误判为必填导致误退。

    # 付费前强制预估（零调用零扣费）
    require_key(SLUG, SOURCE)
    est = estimate([(key, params)], pages=pages)
    print_estimate(est, title="公众号找号 费用预估")
    if (est["total"] > 0 or file_path) and not yes:
        print("WM_NEED_CONFIRM=1")
        print("以上为预估费用。用户确认后加 --yes 执行：")
        rest = " ".join(a for a in sys.argv[1:] if a not in ("--yes", "-y"))
        print("  python scripts/wechat-official-account-finder.py --yes {rest}".format(key=key, rest=rest))
        sys.exit(EXIT_OK)

    wm = WM(SLUG, source=SOURCE)

    if pages > 1 or checkpoint_path:
        rows = wm.paginate(key, max_pages=pages, checkpoint=checkpoint_path, **params)
        data = {"count": len(rows), "items": rows, "partial": bool(wm.partial_error), "error": wm.partial_error}
    else:
        data = wm.call(key, **params)
    wm.finish()

    fmtri = Formatter(SLUG)
    path, n = fmtri.present(data, ep["name"], fmt=fmt, report=report, output=output)
    print("WM_OUTPUT_FILE=" + path)
    print("WM_ROWS=" + str(n))
    if snapshot_path:
        print("WM_SNAPSHOT=" + json.dumps(snapshot(snapshot_path, {"skill": SLUG, "endpoint": key, "params": params, "pages": pages}, data), ensure_ascii=False))
    if wm.partial_error:
        print("WM_PARTIAL=1: " + wm.partial_error, file=sys.stderr)
    if fmt == "markdown" and not report:
        print("")
        print(fmtri.preview(data, ep["name"], n=5))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print("无法执行：" + str(error), file=sys.stderr)
        sys.exit(EXIT_INPUT)
