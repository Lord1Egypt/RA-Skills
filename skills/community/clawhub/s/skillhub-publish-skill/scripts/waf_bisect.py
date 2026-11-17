#!/usr/bin/env python3
"""SkillHub 上传体 WAF 定位工具（腾讯云 WAF 566）。

用途：上传 skill 到 SkillHub 时报「提交失败 / Failed to fetch」时，
判断究竟是被服务端 WAF 按「内容」拦了，还是包结构/字段问题。

判据（唯一可信）：
    向发布端点 POST 同一份 multipart，
      401 {"error":"unauthorized"}  -> 请求已到达应用层 = 内容安全（只是没登录态）
      566                           -> 被腾讯云 WAF 拦截 = 内容命中规则
      其他 4xx                       -> 业务校验问题

三个步骤：
    --step all    1) 完整上传体发一次  2) 逐文件发  3) 对命中文件 ddmin 出最小触发行集合

用法：
    python waf_bisect.py --repo <skill目录> --files SKILL.md manifest.yaml scripts/a.py
    python waf_bisect.py --repo <dir> --files SKILL.md --step check      # 只做全量判定
    python waf_bisect.py --repo <dir> --files SKILL.md --step bisect     # 只做 ddmin

注意：规则是「累计评分制」，单文件/单行测试通过不代表整包安全，
      每次改完内容都要重跑 --step check 确认全量为 401。
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

ENDPOINT = "https://api.skillhub.cn/api/v1/community/skills/publish"
ORIGIN = "https://skillhub.cn"
PROBE_PAYLOAD = {
    "slug": "waf-bisect-probe",
    "displayName": "probe",
    "version": "1.0.0",
    "summaryZh": "probe",
}
SLEEP = 0.18            # 两次请求间隔，避免被限流
PROXY = None            # 例如 "http://127.0.0.1:10808"；默认直连

_cache = {}
_nreq = [0]


def _opener():
    handlers = urllib.request.ProxyHandler({} if not PROXY
                                          else {"http": PROXY, "https": PROXY})
    return urllib.request.build_opener(handlers)


def post_files(parts):
    """parts: [(filename, bytes), ...] -> HTTP status"""
    boundary = "----waf" + uuid.uuid4().hex
    body = ("--%s\r\nContent-Disposition: form-data; name=\"payload\"\r\n\r\n%s\r\n"
            % (boundary, json.dumps(PROBE_PAYLOAD, ensure_ascii=False))).encode()
    for name, data in parts:
        body += ("--%s\r\nContent-Disposition: form-data; name=\"files\"; "
                 "filename=\"%s\"\r\nContent-Type: application/octet-stream\r\n\r\n"
                 % (boundary, name)).encode()
        body += data + b"\r\n"
    body += ("--%s--\r\n" % boundary).encode()

    req = urllib.request.Request(ENDPOINT, data=body, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=" + boundary)
    req.add_header("Origin", ORIGIN)
    req.add_header("Referer", ORIGIN + "/dashboard/publish")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124")
    try:
        with _opener().open(req, timeout=45) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return "FAIL"


def blocked(content, label="SKILL.md"):
    """True = 被 WAF 拦（566）。带缓存，避免重复请求。"""
    key = hashlib.md5(content).hexdigest()
    if key in _cache:
        return _cache[key]
    st = post_files([(label, content)])
    _nreq[0] += 1
    res = (st == 566)
    _cache[key] = res
    if _nreq[0] % 10 == 0:
        print("      ...已发 %d 次请求" % _nreq[0], flush=True)
    time.sleep(SLEEP)
    return res


def read(repo, rel):
    with open(os.path.join(repo, rel.replace("/", os.sep)), "rb") as f:
        return f.read()


def step_check(repo, files):
    parts = [(os.path.basename(r), read(repo, r)) for r in files]
    total = sum(len(d) for _, d in parts)
    st = post_files(parts)
    verdict = {401: "PASS（已到应用层，内容安全）",
               566: "*** 被 WAF 拦截（内容问题）***"}.get(st, "未知状态，看上面返回码")
    print("完整上传体  %d 个文件 / %d 字节  -> HTTP %s  %s" % (len(parts), total, st, verdict))
    return st


def step_perfile(repo, files):
    print("\n逐个文件单独发（401 = 安全，566 = 命中）：")
    hits = []
    for rel in files:
        st = post_files([(os.path.basename(rel), read(repo, rel))])
        print("   %-42s -> %-6s %s" % (rel, st, "<<< 命中" if st == 566 else ""))
        if st == 566:
            hits.append(rel)
        time.sleep(SLEEP)
    return hits


def step_ddmin(repo, rel):
    """对单个文件做 ddmin，输出最小触发行集合。"""
    path = os.path.join(repo, rel.replace("/", os.sep))
    lines = open(path, "rb").read().split(b"\n")
    print("\n对 %s 做 ddmin（共 %d 行）..." % (rel, len(lines)))
    if not blocked(b"\n".join(lines), os.path.basename(rel)):
        print("   该文件单独不发不命中（说明是跨文件累计评分，需回看 step_check 的组合）。")
        return
    cur = list(range(len(lines)))
    n = 2
    while len(cur) >= 2:
        size = (len(cur) + n - 1) // n
        chunks = [cur[i:i + size] for i in range(0, len(cur), size)]
        reduced = False
        for c in chunks:
            drop = set(c)
            rest = [i for i in cur if i not in drop]
            if not rest:
                continue
            if blocked(b"\n".join(lines[i] for i in rest), os.path.basename(rel)):
                cur = rest
                n = max(n - 1, 2)
                reduced = True
                break
        if not reduced:
            if n >= len(cur):
                break
            n = min(len(cur), n * 2)

    print("\n   最小触发行（%d 行，累计 %d 次请求）：" % (len(cur), _nreq[0]))
    for i in cur:
        print("     L%-4d %s" % (i + 1, lines[i].decode("utf-8", "replace")[:120]))
    print("\n   下一步：改掉这些行里的高危 token，然后重跑 --step check 确认全量 401。")
    print("   常见高危：美元符号+双花括号连写（模板注入特征）、格式化元组 % (..)、")
    print("             注释里照抄危险 token 也算命中。")


def main():
    ap = argparse.ArgumentParser(description="SkillHub 上传体 WAF 定位")
    ap.add_argument("--repo", required=True, help="skill 目录")
    ap.add_argument("--files", nargs="+", required=True,
                    help="参与上传的文件（相对 repo 的路径）")
    ap.add_argument("--step", choices=["all", "check", "perfile", "bisect"],
                    default="all")
    args = ap.parse_args()

    files = [f.replace("\\", "/") for f in args.files]
    for f in files:
        if not os.path.exists(os.path.join(args.repo, f.replace("/", os.sep))):
            sys.exit("找不到文件: %s" % f)

    print("端点:", ENDPOINT)
    if args.step in ("all", "check"):
        st = step_check(args.repo, files)
        if st != 566:
            print("\n内容安全，无需继续。若仍报 Failed to fetch，才去查包结构/字段。")
            return
        if args.step == "check":
            return

    if args.step == "bisect":
        hits = files
    else:
        hits = step_perfile(args.repo, files)
        if not hits:
            print("\n单文件都不命中 -> 跨文件累计评分。对最大的那个文件跑 --step bisect。")
            return

    for rel in hits:
        step_ddmin(args.repo, rel)


if __name__ == "__main__":
    main()
