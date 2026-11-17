#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anchor_verify.py — L2 锚点校验器（v1.0.0）

作用
----
把「独立验证者」（L2，通常是另一个 LLM）声称的**逐字引用**，
拿去它所引的页面上做**机器全量核查**。

为什么需要它
------------
L2 的产出本质上仍是「另一个模型的意见」——直接采信就等于
「用一个不可靠判官检验另一个不可靠产出」。
缓解办法不是"再换个模型"，而是：**把 L2 的判断力降级为"找锚点"的能力，
再把"锚点真不真"交给确定性检查。**

本工具就是这个确定性检查。它只回答一个问题：
    「这句话，真的逐字出现在它给的这个页面上吗？」
它**不**判断事实真假、不判断结论对错——那仍属 L1/人工。

SECURITY & NETWORK DISCLOSURE
-----------------------------
This is the ONLY networked component of the zhihu-content-pack skill.
It performs outbound HTTP(S) GET requests **exclusively** to the anchor URLs
explicitly listed in the operator-supplied anchors file, solely to verify
that quoted text appears verbatim on the cited page.

- Rate-limited (--delay, default 0.6s) and time-bounded (--timeout, default 45s).
- No telemetry, no analytics, no crash reporting.
- No credentials, cookies, or account metadata are read, stored, or transmitted.
- Nothing is uploaded anywhere; results are written only to operator-specified local files.

三态（沿用 fail-closed 哲学）
----------------------------
  HIT          片段逐字存在于页面（或经宽松归一后存在，标 loose）
  MISS         抓到了页面，但片段不在里面        -> 危险信号
  UNABLE       页面抓不到/是 PDF/超时            -> **绝不等于通过**

退出码：0 无 MISS/无 UNKNOWN ／ 1 存在 MISS ／ 2 无 MISS 但有 UNABLE ／ 3 输入或内部错误

零依赖：仅标准库（urllib / html / re / json）。不联网调模型、不耗积分。
"""

import argparse
import html
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VERSION = "1.1.0"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# 「疑似动态渲染」判据：抓到页面但可见文本过短，说明正文由 JS 异步加载。
# 此时 MISS 极可能是技术性误判，须标出来提醒人工确认，不得直接当成「引用不实」。
DYNAMIC_VISIBLE_THRESHOLD = 600


# ---------------------------------------------------------------- 归一化

def strip_markup(s: str) -> str:
    """去 script/style/标签 + 解 HTML 实体。"""
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return html.unescape(s)


def norm(s: str) -> str:
    """严格归一：只去空白。保留标点与引号原样。

    去空白是必须的——网页经 markdown/HTML 渲染后，链接、标签会把
    「委托TC260」变成「委托 TC260」，逐字比对会假失败。
    """
    return re.sub(r"\s+", "", strip_markup(s))


_QUOTE_MAP = {
    "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
    "\u300c": '"', "\u300d": '"', "\u300e": '"', "\u300f": '"',
    "\uff02": '"', "\uff07": "'",
}
_PUNCT_MAP = {
    "\uff0c": ",", "\u3002": ".", "\uff1a": ":", "\uff1b": ";",
    "\u3001": ",", "\uff08": "(", "\uff09": ")", "\uff05": "%",
}


def norm_loose(s: str) -> str:
    """宽松归一：在严格基础上再统一引号与常见全角标点。

    仅用于「严格不中」后的二次尝试，命中会显式标注 loose —— 
    因为宽松会牺牲一部分严格性，不能与严格命中同权呈现。
    """
    s = norm(s)
    for a, b in _QUOTE_MAP.items():
        s = s.replace(a, b)
    for a, b in _PUNCT_MAP.items():
        s = s.replace(a, b)
    return s


# ---------------------------------------------------------------- 抓取

def make_ssl_ctx(insecure: bool):
    if not insecure:
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def iri_to_uri(url: str) -> str:
    """把含非 ASCII 字符的 URL 转成可请求的 URI。

    实测踩坑（v1.0.0 首次实跑）：URL 里带中文（如 `?q=示例科技有限公司`）
    会抛 `UnicodeEncodeError: 'ascii' codec can't encode` —— 
    urllib 不会自动 percent-encode，必须自己转，否则整条锚点被误报成「抓不到」。
    """
    try:
        p = urllib.parse.urlsplit(url)
        return urllib.parse.urlunsplit((
            p.scheme,
            p.netloc.encode("idna").decode("ascii") if p.netloc else p.netloc,
            urllib.parse.quote(p.path, safe="/%:@!$&'()*+,;="),
            urllib.parse.quote(p.query, safe="=&%+:/?@!$'()*+,;"),
            urllib.parse.quote(p.fragment, safe="=&%+:/?@"),
        ))
    except Exception:
        return url


def extract_pdf(raw: bytes):
    """用 pypdf（可选依赖）提取 PDF 文本。失败返回 None。

    v1.0.0 首次实跑时，PDF 类锚点全部落为「抓不到」——
    实测证明这类页面**可以核验**（samr.gov.cn 的《强制性国家标准管理办法》PDF
    成功逐字命中 B16），所以值得接一个可选解析器。
    没有 pypdf 时优雅退回 UNABLE，不报错。
    """
    try:
        import io

        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        return None


def fetch(url: str, timeout: int, insecure: bool = False):
    """返回 (text, ctype, err)。err 非空表示 UNABLE。"""
    url = iri_to_uri(url)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    })
    ctx = make_ssl_ctx(insecure)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            ctype = r.headers.get("Content-Type", "") or ""
            raw = r.read()
    except urllib.error.HTTPError as e:
        return "", "", f"HTTP {e.code}"
    except Exception as e:  # 超时/SSL/DNS/连接
        return "", "", f"{type(e).__name__}: {e}"

    if "pdf" in ctype.lower() or url.lower().endswith(".pdf"):
        text = extract_pdf(raw)
        if text is None:
            return "", ctype, "PDF：未装 pypdf 或解析失败（pip install pypdf 可解）"
        return text, ctype, ""

    charset = None
    m = re.search(r"charset=([\w\-]+)", ctype, re.I)
    if m:
        charset = m.group(1).strip()
    for enc in ([charset] if charset else []) + ["utf-8", "gb18030", "latin-1"]:
        try:
            return raw.decode(enc), ctype, ""
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", "replace"), ctype, ""


# ---------------------------------------------------------------- 校验

def check_quotes(page: str, quotes: list) -> list:
    """对一条断言的多个 quote 逐一判定。"""
    strict = norm(page)
    loose = norm_loose(page)
    out = []
    for q in quotes:
        qs, ql = norm(q), norm_loose(q)
        if not qs:
            out.append({"quote": q, "status": "UNABLE", "how": "", "detail": "空片段"})
            continue
        if qs in strict:
            out.append({"quote": q, "status": "HIT", "how": "strict", "detail": ""})
        elif ql in loose:
            out.append({"quote": q, "status": "HIT", "how": "loose", "detail": "引号/标点归一后命中"})
        else:
            out.append({"quote": q, "status": "MISS", "how": "", "detail": "抓到了页面，但片段不在其中"})
    return out


ICON = {"HIT": "[ OK ]", "MISS": "[MISS]", "UNABLE": "[ ?  ]"}


def run(anchors: list, timeout: int, delay: float, insecure: bool, cache_dir=None):
    # URL 去重：同一页面只抓一次
    urls = []
    for a in anchors:
        if a["url"] not in urls:
            urls.append(a["url"])

    pages, errs, ctypes = {}, {}, {}
    for i, u in enumerate(urls, 1):
        if i > 1 and delay:
            time.sleep(delay)
        text, ctype, err = fetch(u, timeout, insecure)
        pages[u], errs[u], ctypes[u] = text, err, ctype
        mark = "OK" if not err else ("PDF" if "PDF" in err else "ERR")
        print(f"  [{i}/{len(urls)}] {mark:<3} {u[:96]}"
              + ("" if not err else f"   <- {err}"))

    results = []
    for a in anchors:
        u = a["url"]
        if errs[u]:
            chk = [{"quote": q, "status": "UNABLE", "how": "", "detail": errs[u]} for q in a["quotes"]]
            vis = 0
        else:
            chk = check_quotes(pages[u], a["quotes"])
            vis = len(re.sub(r"\s+", "", strip_markup(pages[u])))
        results.append({**a, "checks": chk, "page_visible_len": vis})
    return results


def summarize(results: list) -> dict:
    n_q = sum(len(r["checks"]) for r in results)
    n_hit = sum(c["status"] == "HIT" for r in results for c in r["checks"])
    n_loose = sum(c["how"] == "loose" for r in results for c in r["checks"])
    n_miss = sum(c["status"] == "MISS" for r in results for c in r["checks"])
    n_una = sum(c["status"] == "UNABLE" for r in results for c in r["checks"])
    # 疑似动态渲染导致的 MISS：页面抓到了，但可见文本极短
    n_miss_dyn = sum(
        1 for r in results
        if r.get("page_visible_len", 0) < DYNAMIC_VISIBLE_THRESHOLD
        for c in r["checks"] if c["status"] == "MISS"
    )

    # 按验证者判定分组，看"支持"里有多少锚点其实不中
    by_verdict = {}
    for r in results:
        v = r["verdict"]
        d = by_verdict.setdefault(v, {"claims": 0, "quotes": 0, "hit": 0, "miss": 0, "unable": 0})
        d["claims"] += 1
        for c in r["checks"]:
            d["quotes"] += 1
            d["hit"] += c["status"] == "HIT"
            d["miss"] += c["status"] == "MISS"
            d["unable"] += c["status"] == "UNABLE"
    return {"quotes": n_q, "hit": n_hit, "loose": n_loose,
            "miss": n_miss, "miss_dynamic": n_miss_dyn,
            "unable": n_una, "by_verdict": by_verdict}


def print_report(name, results, summary):
    print(f"\n=== L2 锚点校验 · {name} ===")
    print(f"anchor_verify v{VERSION}  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 92)
    for r in results:
        st = [c["status"] for c in r["checks"]]
        ok = st.count("HIT")
        tag = f"{ok}/{len(st)}"
        print(f"{r['id']:<5} L2判定={r['verdict']:<5} 锚点命中={tag:<5} {r['url'][:64]}")
        for c in r["checks"]:
            if c["status"] != "HIT":
                print(f"        {ICON[c['status']]} {c['quote'][:70]}")
                if c["detail"]:
                    print(f"               ↳ {c['detail']}")
                if c["status"] == "MISS" and r.get("page_visible_len", 0) < DYNAMIC_VISIBLE_THRESHOLD:
                    print(f"               ⚠ 该页静态可见文本仅 {r['page_visible_len']} 字 "
                          f"—— 疑似 JS 动态渲染，此 MISS 可能是技术性误判，**须人工确认后再定性**")
    print("-" * 92)
    s = summary
    print(f"引用片段 {s['quotes']} 条  |  逐字命中 {s['hit']}  |  未命中 {s['miss']}  |  抓不到 {s['unable']}")
    if s["loose"]:
        print(f"  其中经宽松归一（引号/标点）才命中的：{s['loose']} 条")
    if s["miss_dynamic"]:
        print(f"  ⚠ 其中 {s['miss_dynamic']} 条 MISS 落在疑似动态渲染页上（不等于引用不实）")
    print("\n按 L2 判定分组：")
    for v, d in s["by_verdict"].items():
        print(f"  {v:<6} 断言 {d['claims']:>2} 条 / 锚点 {d['quotes']:>2} 条 → "
              f"命中 {d['hit']:>2}  未命中 {d['miss']:>2}  抓不到 {d['unable']:>2}")

    hard_miss = s["miss"] - s["miss_dynamic"]
    if hard_miss:
        print(f"\n结论：存在 {hard_miss} 条实质 MISS —— L2 有引用与其所引页面不符，"
              f"**该部分结论不得采信**，需人工复核。")
        return 1
    if s["miss"] and not hard_miss:
        print(f"\n结论：{s['miss']} 条 MISS 全部落在疑似动态渲染页上 —— 属**无法机器核验**，"
              f"不等于引用不实；须人工打开页面确认后才能定性。")
        return 2
    if s["unable"]:
        print(f"\n结论：无 MISS，但有 {s['unable']} 条 UNABLE —— 有锚点未能机器核验"
              f"（反爬/超时/PDF），**不得视为通过**，需人工补核。")
        return 2
    print("\n结论：全部锚点机器核验通过（仅代表「引用真实存在于所引页面」，"
          "不代表「断言本身为真」——后者仍需 L1 与人工）。")
    return 0


# ---------------------------------------------------------------- 自测

SELFTEST_PAGE = """
<html><head><title>t</title><style>.a{color:red}</style><script>var x="不需要的";</script></head>
<body>
  <p>这条<strong>应该</strong>命中。</p>
  <p>委托<a href="#">TC260</a>（全国网络安全标准化技术委员会）执行</p>
  <p>“中文引号也”要命中，标点，也要命中。</p>
  <p>罚款百分之二十至百分之五十</p>
</body></html>
"""


def selftest() -> int:
    print("=== anchor_verify 负向自测 ===")
    print("思路：拿一段已知内容的假页面，验证「该中的中、不该中的不中」。\n")
    fails = []

    page = SELFTEST_PAGE

    # 1) 被标签打断 + 空白差异 -> 必须 HIT（证明归一化有效）
    c = check_quotes(page, ["委托 TC260（全国网络安全标准化技术委员会）执行"])[0]
    print(f"[1] 标签/空白打断  -> {c['status']} ({c['how']})")
    if c["status"] != "HIT":
        fails.append("标签/空白打断的片段应当 HIT")

    # 2) 完全不在页面里 -> 必须 MISS（证明不会假命中）
    c = check_quotes(page, ["这段话根本不在页面上"])[0]
    print(f"[2] 页面内不存在    -> {c['status']}")
    if c["status"] != "MISS":
        fails.append("不存在的片段应当 MISS")

    # 3) 中文引号 vs ASCII 引号 -> 严格不中、宽松应中，且必须标 loose
    c = check_quotes(page, ['"中文引号也"要命中'])[0]
    print(f"[3] 引号形态差异    -> {c['status']} ({c['how']})")
    if c["status"] != "HIT" or c["how"] != "loose":
        fails.append("引号差异应判 HIT 且标注 loose")

    # 4) 全角标点差异 -> 宽松应中
    c = check_quotes(page, ["标点,也要命中。"])[0]
    print(f"[4] 全角标点差异    -> {c['status']} ({c['how']})")
    if c["status"] != "HIT":
        fails.append("全角标点差异应能经宽松归一命中")

    # 5) 关键：数字篡改必须 MISS（防"看着像就放行"）
    c = check_quotes(page, ["罚款百分之三十至百分之五十"])[0]
    print(f"[5] 数字被篡改      -> {c['status']}")
    if c["status"] != "MISS":
        fails.append("数字篡改必须 MISS —— 否则校验器形同虚设")

    # 6) script/style 内容不应进入正文比对
    c = check_quotes(page, ["var x="])[0]
    print(f"[6] script 内文本    -> {c['status']}")
    if c["status"] != "MISS":
        fails.append("script 内文本不该被当成页面正文命中")

    # 7) 中文 URL 必须转成 ASCII URI —— v1.0.0 首次实跑踩的坑
    u = iri_to_uri("https://x.test/search?q=示例科技有限公司")
    ok = all(ord(c) < 128 for c in u) and "%" in u
    print(f"[7] 中文 URL 转义    -> {'OK' if ok else 'FAIL'}  {u[:64]}")
    if not ok:
        fails.append("中文 URL 未转义 → UnicodeEncodeError → 锚点被误报为「抓不到」")

    print()
    if fails:
        for f in fails:
            print(f"  [FAIL] {f}")
        print("\n自测未通过。")
        return 1
    print("自测通过：归一化、宽松回退、数字篡改拦截、script 排除、中文 URL 转义 共 7 项断言全对。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="L2 锚点校验器：机器核查验证者引用的真实性")
    ap.add_argument("--anchors", help="锚点 JSON 文件")
    ap.add_argument("--name", default="", help="报告标题")
    ap.add_argument("--json", dest="json_out", help="输出 JSON 报告路径")
    ap.add_argument("--timeout", type=int, default=45)
    ap.add_argument("--delay", type=float, default=0.6, help="相邻请求间隔秒（限流友好）")
    ap.add_argument("--insecure", action="store_true", help="跳过 TLS 校验（证书异常的政府站点）")
    ap.add_argument("--version", action="version", version=f"anchor_verify {VERSION}")
    ap.add_argument("--selftest", action="store_true", help="跑负向自测，证明它会抓错")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest())
    if not a.anchors:
        ap.error("需要 --anchors（或用 --selftest）")

    p = Path(a.anchors)
    if not p.exists():
        print(f"锚点文件不存在：{p}", file=sys.stderr)
        sys.exit(3)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        anchors = data["anchors"] if isinstance(data, dict) else data
    except Exception as e:
        print(f"锚点文件解析失败：{e}", file=sys.stderr)
        sys.exit(3)

    print(f"锚点条目 {len(anchors)} 条，开始抓取页面…")
    results = run(anchors, a.timeout, a.delay, a.insecure)
    summary = summarize(results)
    code = print_report(a.name or p.stem, results, summary)

    if a.json_out:
        Path(a.json_out).write_text(json.dumps({
            "tool": f"anchor_verify {VERSION}",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "anchors_file": p.as_posix(),
            "summary": summary,
            "results": results,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON 报告已写入：{a.json_out}")

    sys.exit(code)


if __name__ == "__main__":
    main()
