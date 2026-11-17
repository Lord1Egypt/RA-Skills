#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delivery_guard.py — 交付门禁（fail-closed）

为什么存在
----------
LLM（包括我）在没有外部锚点时，会把自己的覆盖不足当成"已完成"上报。
这不是个例，是被实测过的普遍规律：
  · self-critique 的假阳性率被实测到 84%（Valmeekam et al., arXiv 2310.08118）
  · 无外部反馈的内在自纠正会让推理准确率下降（Huang et al., arXiv 2310.01798, ICLR 2024）
  · self-refine 会放大 self-bias，而非纠正它（Xu et al., arXiv 2402.11436）

本脚本把人无法自证的部分抽出来，交给确定性检查：
  · 声明过的尺寸 / 计数 / 文件存在性
  · 废弃措辞残留（必须 0 命中）
  · 图文一致性（图里的断言必须能在指定文件中找到）
  · 交付目录覆盖率（每个文件都要被清单覆盖）
  · 图像客观属性（尺寸、灰度分布）

不做的检查：任何"另一个模型说它对"的判断。
Ground truth 只接受文件字节、字符串计数、像素统计。

severity：blocking vs advisory
------------------------------
每条检查可标 severity（默认 blocking）：
  blocking  非 PASS 即阻断交付（退出码 1/2）
  advisory  只记录、标注、不阻断（不影响退出码），报告里打 [WARN]

为什么需要 advisory：**存量包定稿于新规矩之前**（例：浅色系配图规矩 2026-10-06 才立，
而 XCGS 包 10-05 已发布且是深色封面）。若把新规矩一律按 blocking 套到老包上，
扫描结果会清一色 FAIL —— 既不是老包错了，也看不出新包有没有问题。
advisory 让"历史差距"和"本次错误"分开呈现。
⚠️ severity 拼错会直接报 FAIL，不静默降级：否则「以为配了观察项、实际仍在阻塞」。

三态与退出码
------------
  PASS          检查通过
  FAIL          检查不通过                    -> 退出码 1（仅 blocking）
  INCONCLUSIVE  检查无法执行（缺依赖/缺文件）  -> 退出码 2（仅 blocking）
                "检查不了" 绝不等于 "通过"。默认 fail-closed。

退出码：0 无 blocking 问题 ／ 1 有 blocking FAIL ／ 2 无 FAIL 但有 blocking INCONCLUSIVE ／ 3 配置或内部错误
        退出码 0 时仍可能有 advisory 未达标项 —— 那些要人工看，不该被当成"全过"。

用法
----
  python delivery_guard.py --config guard.toml
  python delivery_guard.py --config guard.toml --json report.json
  python delivery_guard.py --config guard.toml --allow-inconclusive
  python delivery_guard.py --selftest          # 负向测试：证明它真的会抓错

依赖：仅标准库。图像灰度检查需要 Pillow；缺失时该项返回 INCONCLUSIVE（不会假装通过）。
"""

from __future__ import annotations

import argparse
import glob as globmod
import hashlib
import json
import re
import sys
import time
import tomllib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VERSION = "1.2.0"

CJK = re.compile(r"[\u4e00-\u9fff]")

# --------------------------------------------------------------------------
# 工具函数
# --------------------------------------------------------------------------


def expand(root: Path, pattern: str) -> list[Path]:
    """按 glob 展开（相对 root），返回排序后的路径列表。"""
    if not pattern:
        return []
    p = Path(pattern)
    if p.is_absolute():
        return sorted(Path(x) for x in globmod.glob(str(p), recursive=True))
    hits = sorted(root.glob(pattern))
    return [h for h in hits if h.is_file() and h.name != "__pycache__"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_html(raw: str) -> str:
    """去 script/style/标签/实体，得到渲染后大致可见的文本。"""
    s = re.sub(r"(?is)<script\b.*?</script\s*>", " ", raw)
    s = re.sub(r"(?is)<style\b.*?</style\s*>", " ", s)
    s = re.sub(r"(?is)<!--.*?-->", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ")
    s = (
        s.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&amp;", "&")
    )
    return s


def visible_text(path: Path, strip: bool = True) -> str:
    """取文件文本。

    strip=True  -> 去掉 script/style/标签/实体，得到"渲染后可见"的文字（比正文用）
    strip=False -> 返回原始文本，含 class/属性/注释（数 HTML 结构标记时必须用这个）

    注意：数 `class="figcap"` 这类属性时必须 strip=False，否则属性会被一起去掉，
    计数永远为 0 —— 这个坑在 1.0.0 自测里被实际抓到过。
    """
    raw = read_text(path)
    if strip and path.suffix.lower() in {".html", ".htm"}:
        return strip_html(raw)
    return raw


def png_dimensions(path: Path) -> tuple[int, int]:
    """读 PNG IHDR 拿宽高，纯标准库。"""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是 PNG 文件")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG 缺少 IHDR")
    w = int.from_bytes(head[16:20], "big")
    h = int.from_bytes(head[20:24], "big")
    return w, h


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------
# 检查器注册表
# --------------------------------------------------------------------------

CHECKS: dict[str, callable] = {}


def check(kind: str):
    def deco(fn):
        CHECKS[kind] = fn
        return fn

    return deco


def norm(s: str) -> str:
    """归一化：去空白，供跨文件比对用。"""
    return re.sub(r"\s+", "", s)


# ---- 文件存在性 ---------------------------------------------------------


@check("file_exists")
def c_file_exists(c: dict, root: Path):
    pats = c.get("files") or [c.get("file")]
    missing = []
    for pat in pats:
        if not pat:
            continue
        if not expand(root, pat):
            missing.append(pat)
    if missing:
        return "FAIL", f"找不到文件：{', '.join(missing)}"
    return "PASS", f"{len(pats)} 个路径均存在"


# ---- 计数 ---------------------------------------------------------------


@check("grep_count")
def c_grep_count(c: dict, root: Path):
    pat = c["file"]
    needle = c["pattern"]
    expect = c.get("expect")
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    strip = c.get("strip_tags", True)
    total = 0
    per = []
    for f in files:
        n = visible_text(f, strip).count(needle)
        total += n
        per.append(f"{f.name}:{n}")
    detail = f"命中 {total}" + (f"（期望 {expect}）" if expect is not None else "") + " ｜ " + ", ".join(per)
    if expect is None:
        return "PASS", detail
    return ("PASS" if total == expect else "FAIL"), detail


@check("count_files")
def c_count_files(c: dict, root: Path):
    pat = c.get("glob") or c.get("file")
    expect = c.get("expect")
    files = [f for f in expand(root, pat) if not f.name.startswith("_")]
    detail = f"匹配 {len(files)} 个（期望 {expect}）｜ " + ", ".join(f.name for f in files[:12])
    if expect is None or len(files) == expect:
        return "PASS", detail
    return "FAIL", detail


# ---- 残留 ---------------------------------------------------------------


@check("grep_zero")
def c_grep_zero(c: dict, root: Path):
    pat = c.get("file") or c.get("glob")
    needles = c.get("patterns") or []
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    # 默认扫原始文本（含属性/注释）：目标是"0 残留"，宁可多抓不可漏。
    # 若因 CSS/JS 误报，再显式设 strip_tags = true。
    strip = c.get("strip_tags", False)
    # ignore_patterns：合法「否定用法」的豁免（正则，命中片段会被先移除）。
    #
    # 为什么必须有 —— 两轮内撞了两次同一类坑：
    #   ① "这条不设上限"   描述罚则性质，合法，却撞上废弃词「不设上限」
    #   ② "年审是循环，不是第四律"  恰恰是在强调"不是第四律"，
    #      而发布口径要求正文不得出现「四律」—— 裸词匹配把正确写法判成了残留
    # 结论：当被禁词本身可能出现在否定句中时，裸词匹配 100% 误报。
    # 误报多了，门禁的阻断结论就没人信了 —— 这比漏报更致命。
    ignores = [re.compile(p) for p in (c.get("ignore_patterns") or [])]
    hits = []
    for f in files:
        txt = visible_text(f, strip)
        for ig in ignores:
            txt = ig.sub("", txt)
        for n in needles:
            k = txt.count(n)
            if k:
                hits.append(f"{f.name} ← {n!r} ×{k}")
    if hits:
        return "FAIL", "废弃表述残留：" + "；".join(hits)
    extra = f"（已豁免 {len(ignores)} 条合法否定用法）" if ignores else ""
    return "PASS", f"{len(needles)} 个废弃表述在 {len(files)} 个文件中 0 命中{extra}"


# ---- 图文一致性 ---------------------------------------------------------


@check("text_present")
def c_text_present(c: dict, root: Path):
    """图内断言 → 正文必须能支撑。断言的每条文本都要在目标文件里找到（归一化比对）。"""
    pat = c["file"]
    texts = c.get("texts") or []
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    blob = norm(" ".join(visible_text(f) for f in files))
    missing = [t for t in texts if norm(t) not in blob]
    if missing:
        shown = "；".join(repr(m) for m in missing[:6])
        return "FAIL", f"{len(missing)}/{len(texts)} 条断言在 {pat} 中找不到支撑：{shown}"
    return "PASS", f"{len(texts)} 条断言全部在 {pat} 中有对应文字"


# ---- 中文引号纪律 -------------------------------------------------------


@check("no_ascii_quote")
def c_no_ascii_quote(c: dict, root: Path):
    """只报告「含中文的行」里的 ASCII 直引号 —— 英文行自动豁免。"""
    pat = c.get("file") or c.get("glob")
    allow = [re.compile(p) for p in (c.get("allow_patterns") or [])]
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    bad = []
    for f in files:
        for i, line in enumerate(visible_text(f).splitlines(), 1):
            if not CJK.search(line):
                continue
            if '"' not in line and "'" not in line:
                continue
            if any(a.search(line) for a in allow):
                continue
            snippet = line.strip()[:60]
            bad.append(f"{f.name}:{i} {snippet!r}")
    if bad:
        shown = "；".join(bad[:5])
        more = f"（共 {len(bad)} 处）" if len(bad) > 5 else ""
        return "FAIL", f"中文行里出现 ASCII 直引号{more}：{shown}"
    return "PASS", f"{len(files)} 个文件的中文行均未出现 ASCII 直引号"


# ---- 读者可见标题 -------------------------------------------------------


@check("visible_heading")
def c_visible_heading(c: dict, root: Path):
    """渲染级检查：每个 HTML 文件必须含读者打开即见的标题。

    背景（2026-10-11 实证漏检）：知乎粘贴版把标题只写在 <head><title>，
    标签页标题在预览/粘贴时不可见，正文"无题目"直接交给了用户。
    教训：源码里有 ≠ 读者看得见。本检查锚定的是"可见结构"：
      ① <h1>~<h6> 且去标签后非空；或
      ② pattern 正则命中（用于黄框内大字标题 span 这类自定义样式）。
    """
    pat = c.get("file") or c.get("glob")
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    min_count = int(c.get("min_count", 1))
    extra_pat = re.compile(c["pattern"]) if c.get("pattern") else None
    bad, rows = [], []
    for f in files:
        raw = read_text(f)
        heads = [
            m.group(1).strip()
            for m in re.finditer(r"(?is)<h([1-6])\b[^>]*>(.*?)</h\1\s*>", raw)
        ]
        heads = [re.sub(r"(?s)<[^>]+>", "", h) for h in heads]
        heads = [h for h in heads if h]
        n = len(heads) + (1 if (extra_pat and extra_pat.search(raw)) else 0)
        title_show = heads[0][:40] if heads else ("<自定义样式标题>" if n else "（无）")
        rows.append(f"{f.name} 标题×{n}")
        if n < min_count:
            bad.append(f"{f.name} 可见标题 {n} 个（要求 ≥{min_count}）：{title_show}")
    if bad:
        return "FAIL", "；".join(bad)
    return "PASS", f"{len(files)} 个文件均含读者可见标题 ｜ " + "；".join(rows)


# ---- 图像 ---------------------------------------------------------------


@check("png_size")
def c_png_size(c: dict, root: Path):
    pat = c["file"]
    ew, eh = c.get("width"), c.get("height")
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    bad, ok = [], []
    for f in files:
        try:
            w, h = png_dimensions(f)
        except Exception as e:
            bad.append(f"{f.name} 读取失败({e})")
            continue
        if (ew and w != ew) or (eh and h != eh):
            bad.append(f"{f.name} 实际 {w}×{h}，期望 {ew}×{eh}")
        else:
            ok.append(f"{f.name} {w}×{h}")
    if bad:
        return "FAIL", "；".join(bad)
    return "PASS", "；".join(ok)


@check("png_lightness")
def c_png_lightness(c: dict, root: Path):
    """浅色系量化判据：平均亮度 / 暗像素占比 / 亮像素占比。"""
    pat = c.get("file") or c.get("glob")
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    try:
        from PIL import Image  # noqa
    except Exception:
        return "INCONCLUSIVE", "未安装 Pillow，无法执行灰度统计（不视为通过）"

    min_avg = float(c.get("min_avg_lum", 180))
    max_dark = float(c.get("max_dark_ratio", 0.15))
    min_bright = float(c.get("min_bright_ratio", 0.60))

    from PIL import Image

    rows, bad = [], []
    for f in files:
        try:
            im = Image.open(f).convert("L")
        except Exception as e:
            bad.append(f"{f.name} 打开失败({e})")
            continue
        hist = im.histogram()
        total = sum(hist) or 1
        avg = sum(i * n for i, n in enumerate(hist)) / total
        dark = sum(hist[:100]) / total
        bright = sum(hist[201:]) / total
        rows.append(f"{f.name} avg={avg:.1f} dark={dark:.1%} bright={bright:.1%}")
        if avg < min_avg or dark > max_dark or bright < min_bright:
            bad.append(
                f"{f.name} 不达标（avg {avg:.1f}<{min_avg:.0f} 或 dark {dark:.1%}>{max_dark:.0%} 或 bright {bright:.1%}<{min_bright:.0%}）"
            )
    if bad:
        return "FAIL", "；".join(bad) + " ｜ " + "；".join(rows)
    return "PASS", "；".join(rows)


# ---- 覆盖率 -------------------------------------------------------------


@check("coverage")
def c_coverage(c: dict, root: Path):
    """交付目录里每个文件都必须被清单覆盖；清单里声明的每个文件也必须真实存在。"""
    sub = c.get("dir", ".")
    allowed = c.get("expect") or []
    base = (root / sub) if sub not in (".", "") else root
    if not base.exists():
        return "INCONCLUSIVE", f"目录不存在：{base}"
    actual = []
    for p in sorted(base.rglob("*")):
        if p.is_dir() or p.name.startswith("."):
            continue
        if "__pycache__" in p.parts:
            continue
        actual.append(str(p.relative_to(base)).replace("\\", "/"))

    def covered(rel: str) -> bool:
        if rel.startswith("_") or "/_" in rel:  # _superseded / _cover-test 等归档区豁免
            return True
        for e in allowed:
            if globmod.fnmatch.fnmatch(rel, e) or rel == e:
                return True
        return False

    uncovered = [a for a in actual if not covered(a)]
    declared_missing = []
    for e in allowed:
        if "*" in e or "?" in e:
            if not any(globmod.fnmatch.fnmatch(a, e) for a in actual):
                declared_missing.append(e)
        elif e not in actual:
            declared_missing.append(e)

    probs = []
    if uncovered:
        probs.append(f"目录中有 {len(uncovered)} 个文件未被清单覆盖：{', '.join(uncovered[:8])}")
    if declared_missing:
        probs.append(f"清单声明但实际不存在：{', '.join(declared_missing[:8])}")
    if probs:
        return "FAIL", "；".join(probs)
    return "PASS", f"{len(actual)} 个文件全部被清单覆盖"


# ---- 指纹登记 -----------------------------------------------------------


@check("sha256")
def c_sha256(c: dict, root: Path):
    pat = c.get("file") or c.get("glob")
    files = expand(root, pat)
    if not files:
        return "INCONCLUSIVE", f"未匹配到文件：{pat}"
    lines = [f"{sha256_of(f)[:16]}… {f.name}" for f in files]
    return "PASS", "；".join(lines)


# --------------------------------------------------------------------------
# 运行
# --------------------------------------------------------------------------


VALID_SEVERITY = ("blocking", "advisory")


class Result:
    __slots__ = ("cid", "kind", "status", "detail", "why", "severity")

    def __init__(self, cid, kind, status, detail, why="", severity="blocking"):
        self.cid, self.kind, self.status = cid, kind, status
        self.detail, self.why, self.severity = detail, why, severity

    @property
    def blocks(self) -> bool:
        """只有 blocking 项的非 PASS 才阻断交付。

        severity 存在的理由：存量包定稿于新规矩之前，套新规矩必然冲突。
        若全是 blocking，扫描结果清一色 FAIL，等于没有信息量。
        advisory = "记录事实、供人判断"，不冒充交付阻断。
        """
        return self.severity == "blocking" and self.status != "PASS"


def run(cfg: dict, root: Path) -> list[Result]:
    out: list[Result] = []
    for i, c in enumerate(cfg.get("check", []), 1):
        cid = c.get("id") or f"check{i}"
        kind = c.get("kind", "")
        why = c.get("why", "")
        sev = c.get("severity", "blocking")
        if sev not in VALID_SEVERITY:
            # severity 拼错必须报错，不能静默降级 —— 否则「以为配了观察项、实际在阻塞」
            out.append(
                Result(
                    cid,
                    kind,
                    "FAIL",
                    f"severity 取值非法 {sev!r}（只允许 blocking / advisory）",
                    why,
                    "blocking",
                )
            )
            continue
        fn = CHECKS.get(kind)
        if fn is None:
            out.append(Result(cid, kind, "FAIL", f"未知检查类型 {kind!r}（配置错误）", why, sev))
            continue
        try:
            status, detail = fn(c, root)
        except Exception as e:  # 检查器自身异常 -> 不猜，报 INCONCLUSIVE
            status, detail = "INCONCLUSIVE", f"执行异常：{type(e).__name__}: {e}"
        out.append(Result(cid, kind, status, detail, why, sev))
    return out


ICON = {"PASS": "[PASS] ", "FAIL": "[FAIL] ", "INCONCLUSIVE": "[ ??? ]"}
ADVISORY_ICON = {"PASS": "[PASS] ", "FAIL": "[WARN] ", "INCONCLUSIVE": "[ ~~~ ]"}


def print_report(name: str, results: list[Result], cfg_hash: str) -> int:
    n_pass = sum(r.status == "PASS" for r in results)
    blk_fail = [r for r in results if r.blocks and r.status == "FAIL"]
    blk_inc = [r for r in results if r.blocks and r.status == "INCONCLUSIVE"]
    adv = [r for r in results if r.severity == "advisory" and r.status != "PASS"]

    print(f"\n=== 交付门禁 · {name} ===")
    print(f"config:{cfg_hash[:12]}  guard:v{VERSION}  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 78)
    for r in results:
        table = ICON if r.severity == "blocking" else ADVISORY_ICON
        tag = "" if r.severity == "blocking" else "  ［观察项·不阻塞］"
        print(f"{table[r.status]} {r.cid:<28} {r.detail}{tag}")
        if r.status != "PASS" and r.why:
            print(f"{'':>10}↳ 为什么重要：{r.why}")
    print("-" * 78)
    print(
        f"PASS {n_pass}   BLOCKING: FAIL {len(blk_fail)} / 无法执行 {len(blk_inc)}   "
        f"ADVISORY(观察项) {len(adv)}"
    )

    if blk_fail:
        print("结论：不许交付（存在 blocking FAIL）")
        return 1
    if blk_inc:
        print("结论：不许交付（存在无法执行的 blocking 检查；加 --allow-inconclusive 可临时放行，但需人工确认已补查）")
        return 2
    if adv:
        print(f"结论：门禁通过 —— 但请注意 {len(adv)} 个观察项未达标（不阻塞交付，需人工判断是否处理）")
        print("      观察项通常代表「新规矩 vs 历史产物」的差距，不是本次引入的错误。")
        return 0
    print("结论：门禁通过（仅代表这些确定性检查通过，不等于内容正确）")
    return 0


# --------------------------------------------------------------------------
# 负向自测：证明它真的会抓错
# --------------------------------------------------------------------------

SELFTEST_OK = """<!DOCTYPE html><html><body>
<h1>样例</h1><p>正文一。</p><p class="figcap">图注一</p><p>正文二。</p>
<p class="figcap">图注二</p><p>正文三。</p><p class="figcap">图注三</p>
</body></html>"""

SELFTEST_BAD = """<!DOCTYPE html><html><body>
<h1>样例</h1><p>正文一。</p><p class="figcap">图注一</p><p>正文二。</p>
<p>正文三。</p><p>这是一句"三条法律后果"的废弃表述。</p>
</body></html>"""

SELFTEST_TOML = """
[package]
name = "selftest"
root = "."

[[check]]
id = "figcap-count"
kind = "grep_count"
file = "sample.html"
pattern = 'class="figcap"'
strip_tags = false
expect = 3
why = "每张内文图必须有一个对位点（数属性必须 strip_tags=false）"

[[check]]
id = "stale"
kind = "grep_zero"
file = "sample.html"
patterns = ["三条法律后果"]
why = "改稿要改全链，废弃措辞必须 0 残留"

[[check]]
id = "img-num"
kind = "count_files"
glob = "fig*.png"
expect = 3
why = "配置声明的配图数必须可数"

[[check]]
id = "light"
kind = "png_lightness"
glob = "fig*.png"
why = "浅色系量化判据"

# 观察项：故意必然命中，用来验证「advisory 会 FAIL 但不阻塞」确实生效
[[check]]
id = "advisory-demo"
kind = "grep_zero"
file = "sample.html"
patterns = ["正文"]
severity = "advisory"
why = "演示观察项语义：命中也不阻断交付"
"""


def selftest() -> int:
    import os
    import tempfile

    print("=== delivery_guard 负向自测 ===")
    print("思路：三组样本各自必须给出预期结果 ——")
    print("  [A] 合规样本：blocking 问题 0 项，但观察项确实 FAIL 且不阻塞")
    print("  [B] 植入 4 类错误的样本：全部被抓出，0 例 false accept")
    print("  [C] severity 拼错的配置：必须报错，不得静默降级\n")

    # 为什么不用系统 %TEMP%：沙箱环境下，子进程写系统临时目录会被整树硬杀
    # （2026-10-11 实测：subprocess 跑 --selftest 时父进程连带被杀，无任何堆栈）。
    # 改用用户数据盘上已验证可写的目录。
    try:
        workbase = Path(os.environ.get("DG_SELFTEST_DIR") or Path.home() / "Workbuddy")
        workbase.mkdir(parents=True, exist_ok=True)
        probe = workbase / ".dg_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except Exception:
        workbase = Path(tempfile.gettempdir())

    with tempfile.TemporaryDirectory(prefix="dg_selftest_", dir=str(workbase)) as td:
        root = Path(td)
        (root / "guard.toml").write_text(SELFTEST_TOML, encoding="utf-8")

        # 场景 A 用三张浅色图（应当全过）；深色图稍后在场景 B 才换进来
        try:
            from PIL import Image

            for n in (1, 2, 3):
                Image.new("RGB", (2240, 1260), (245, 248, 253)).save(root / f"fig{n}.png")
            pil_ok = True
        except Exception:
            pil_ok = False

        cfg = tomllib.loads(SELFTEST_TOML)
        failures: list[str] = []

        # --- 场景 A：合规样本 ---
        #     期望：blocking 问题 0 项；advisory 项确实 FAIL 但不阻塞
        (root / "sample.html").write_text(SELFTEST_OK, encoding="utf-8")
        res_a = run(cfg, root)
        a_blocking = [r for r in res_a if r.blocks]
        a_adv = [r for r in res_a if r.severity == "advisory" and r.status != "PASS"]
        print(f"[A] 合规样本 -> blocking 问题 {len(a_blocking)} 项；观察项未达标 {len(a_adv)} 项")
        for r in res_a:
            table = ICON if r.severity == "blocking" else ADVISORY_ICON
            print(f"      {table[r.status]} {r.cid:<16} {r.severity:<9} {r.detail}")
        if a_blocking:
            failures.append("场景A：合规样本不应出现 blocking 问题")
        if not pil_ok:
            print("      （未装 Pillow，灰度检查按预期落为 INCONCLUSIVE）")

        # 核心断言：观察项必须「真的在抓错」+「真的不阻塞」。
        # 这两条任一失效，severity 就是个装饰品。
        adv_demo = next((r for r in res_a if r.cid == "advisory-demo"), None)
        if adv_demo is None:
            failures.append("场景A：配置里找不到 advisory-demo 检查项")
        else:
            if adv_demo.status != "FAIL":
                failures.append(
                    f"场景A：advisory-demo 应为 FAIL，实际 {adv_demo.status} —— 观察项没有真的在抓错"
                )
            if adv_demo.blocks:
                failures.append("场景A：advisory 项 blocks 必须为 False —— 否则观察项会静默阻塞交付")
        if not a_adv:
            failures.append("场景A：观察项统计为 0，severity 分类可能未生效")

        # --- 场景 B：植入 4 类错误 ---
        #   ① figcap 3 -> 1（漏对位点）② 出现废弃表述 ③ 少一张配图 ④ 混入深色图
        (root / "sample.html").write_text(SELFTEST_BAD, encoding="utf-8")
        (root / "fig2.png").unlink()
        if pil_ok:
            from PIL import Image

            Image.new("RGB", (2240, 1260), (12, 20, 40)).save(root / "fig3.png")
        res_b = run(cfg, root)
        got = {r.cid for r in res_b if r.status == "FAIL"}
        got_blocking = {r.cid for r in res_b if r.blocks and r.status == "FAIL"}
        print(f"\n[B] 植入错误样本 -> FAIL {len(got)} 项（其中 blocking {len(got_blocking)} 项）")
        for r in res_b:
            table = ICON if r.severity == "blocking" else ADVISORY_ICON
            print(f"      {table[r.status]} {r.cid:<16} {r.severity:<9} {r.detail}")

        # 少了 1 个 figcap(3->2) + 出现废弃表述 + 深色图 -> 应命中 3 项
        expect_hit = {"figcap-count", "stale", "img-num"}
        if pil_ok:
            expect_hit.add("light")
        missed = expect_hit - got_blocking
        if missed:
            failures.append(f"场景B：应命中的检查未命中 -> {sorted(missed)}")
        # 关键：不能有 false accept（真错了却说 PASS）
        false_accept = {r.cid for r in res_b if r.cid in expect_hit and r.status != "FAIL"}
        if false_accept:
            failures.append(f"场景B：出现 false accept -> {sorted(false_accept)}")
        # 观察项绝不能混进 blocking 集合
        if "advisory-demo" in got_blocking:
            failures.append("场景B：advisory 项被算成了 blocking")

        # --- 场景 C：severity 拼错必须报错 ---
        #     为什么测：拼错的 severity 若被静默忽略 -> 退化成 blocking，
        #     于是「我配的是观察项」和「实际它在阻塞交付」完全不同却看不出来。
        BAD_SEV = """
[package]
name = "sevtest"
root = "."
[[check]]
id = "typo-severity"
kind = "file_exists"
files = ["sample.html"]
severity = "warn"
why = "warn 不是合法值（合法值只有 blocking / advisory）"
"""
        res_c = run(tomllib.loads(BAD_SEV), root)
        c_blocking = [r for r in res_c if r.blocks and r.status == "FAIL"]
        print(f"\n[C] severity 拼错 -> blocking FAIL {len(c_blocking)} 项")
        for r in res_c:
            print(f"      {ICON[r.status]} {r.cid:<16} {r.detail}")
        if not c_blocking:
            failures.append("场景C：severity 拼错却未报 FAIL —— 静默降级会让观察项悄悄变成阻塞项")

        # --- 场景 D：ignore_patterns 免除合法否定用法，但不放行真残留 ---
        #     两个方向都要测：「该豁免的豁免」+「不该豁免的照抓」。
        #     只测一边的话，把豁免实现成"一键放行"照样能通过自测。
        IGN_TOML = """
[package]
name = "igntest"
root = "."

[[check]]
id = "ignored"
kind = "grep_zero"
file = "sample.html"
patterns = ["四律"]
ignore_patterns = ["不是四律", "而非四律"]
why = "被禁词出现在否定句里属合法用法（实证：年审是循环，不是第四律）"
"""
        ign_cfg = tomllib.loads(IGN_TOML)

        (root / "sample.html").write_text(
            "<html><body><p>年审是循环，不是四律。</p></body></html>", encoding="utf-8"
        )
        res_d = run(ign_cfg, root)
        d_fail = [r for r in res_d if r.status == "FAIL"]
        print(f"\n[D] ignore_patterns：合法否定用法 -> FAIL {len(d_fail)} 项")
        for r in res_d:
            print(f"      {ICON[r.status]} {r.cid:<16} {r.detail}")
        if d_fail:
            failures.append("场景D：合法的否定用法被判为残留（ignore_patterns 未生效）")

        (root / "sample.html").write_text(
            "<html><body><p>我们把它总结为四律体系。</p></body></html>", encoding="utf-8"
        )
        res_d2 = run(ign_cfg, root)
        d2_fail = [r for r in res_d2 if r.status == "FAIL"]
        print(f"    ignore_patterns：真残留 -> FAIL {len(d2_fail)} 项")
        for r in res_d2:
            print(f"      {ICON[r.status]} {r.cid:<16} {r.detail}")
        if not d2_fail:
            failures.append("场景D：真残留被豁免放行 —— 豁免绝不能变成一键放行开关")

        # --- 场景 E：visible_heading —— 读者可见标题（2026-10-11 漏检教训）---
        #     两个方向：有 h1 -> PASS；标题只在 <head><title>（读者看不见）-> FAIL。
        VH_TOML = """
[package]
name = "vhtest"
root = "."
[[check]]
id = "vh"
kind = "visible_heading"
file = "sample.html"
min_count = 1
why = "读者打开必须能立刻看到题目"
"""
        vh_cfg = tomllib.loads(VH_TOML)

        (root / "sample.html").write_text(
            "<html><head><title>T</title></head><body><h1>真正的题目</h1><p>正文</p></body></html>",
            encoding="utf-8",
        )
        res_e = run(vh_cfg, root)
        e_fail = [r for r in res_e if r.status == "FAIL"]
        print(f"\n[E] visible_heading：正文含 h1 -> FAIL {len(e_fail)} 项")
        if e_fail:
            failures.append("场景E：正文有 h1 却被判无标题")

        (root / "sample.html").write_text(
            "<html><head><title>标签页标题（读者看不见）</title></head><body><p>直接正文</p></body></html>",
            encoding="utf-8",
        )
        res_e2 = run(vh_cfg, root)
        e2_fail = [r for r in res_e2 if r.status == "FAIL"]
        print(f"    visible_heading：标题只在 <head><title> -> FAIL {len(e2_fail)} 项")
        for r in res_e2:
            print(f"      {ICON[r.status]} {r.cid:<16} {r.detail}")
        if not e2_fail:
            failures.append("场景E：head 标题冒充可见标题被放行 —— 正是 2026-10-11 实际翻车的形态")

    print("\n" + "=" * 60)
    if failures:
        print("自测未通过：")
        for f in failures:
            print("  ·", f)
        return 3
    print("自测通过：合规样本 blocking 问题 0 项；植入的 4 类错误全部被抓出，0 例 false accept；"
          "观察项 FAIL 但不阻塞；severity 拼错会报错；合法否定用法被豁免、真残留照抓；"
          "可见标题缺失（head 冒充）会被抓出。")
    return 0


# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="交付门禁（fail-closed）")
    ap.add_argument("--config", help="TOML 配置文件")
    ap.add_argument("--json", help="把结果写成 JSON")
    ap.add_argument("--allow-inconclusive", action="store_true", help="允许 INCONCLUSIVE 不阻塞（不推荐）")
    ap.add_argument("--selftest", action="store_true", help="负向自测：证明它会抓错")
    ap.add_argument("--version", action="version", version=f"delivery_guard {VERSION}")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.config:
        ap.print_help()
        return 3

    cfg_path = Path(args.config).resolve()
    if not cfg_path.exists():
        print(f"配置不存在：{cfg_path}")
        return 3
    raw = cfg_path.read_bytes()
    try:
        cfg = tomllib.loads(raw.decode("utf-8"))
    except Exception as e:
        print(f"配置解析失败：{e}")
        return 3

    pkg = cfg.get("package", {})
    name = pkg.get("name", cfg_path.stem)
    root = Path(pkg.get("root", "."))
    if not root.is_absolute():
        root = (cfg_path.parent / root).resolve()

    results = run(cfg, root)
    code = print_report(name, results, hashlib.sha256(raw).hexdigest())

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                {
                    "package": name,
                    "root": str(root),
                    "guard_version": VERSION,
                    "config_sha256": hashlib.sha256(raw).hexdigest(),
                    "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "summary": {
                        "pass": sum(r.status == "PASS" for r in results),
                        "fail": sum(r.blocks and r.status == "FAIL" for r in results),
                        "inconclusive": sum(r.blocks and r.status == "INCONCLUSIVE" for r in results),
                        "advisory_not_pass": sum(
                            r.severity == "advisory" and r.status != "PASS" for r in results
                        ),
                        "exit_code": code,
                    },
                    "checks": [
                        {
                            "id": r.cid,
                            "kind": r.kind,
                            "severity": r.severity,
                            "status": r.status,
                            "blocks": r.blocks,
                            "detail": r.detail,
                            "why": r.why,
                        }
                        for r in results
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"JSON 报告：{args.json}")

    if args.allow_inconclusive and code == 2:
        print("（--allow-inconclusive 已放行 INCONCLUSIVE，请人工确认这些项已补查）")
        return 0
    return code


if __name__ == "__main__":
    sys.exit(main())
