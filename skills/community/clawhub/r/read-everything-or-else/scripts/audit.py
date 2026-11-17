#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit.py - 检查「说读完了」是不是真的读完了。

零依赖，Python 3.8+。

两种模式:

1) 打卡（读一条，记一条）
   python audit.py <WORKDIR> --done R0007 --quote "<原文逐字摘录>" --evidence "<你读到了什么>"
   python audit.py <WORKDIR> --skip R0007 --reason "<为什么跳过>"     # 算缺口
   python audit.py <WORKDIR> --fail R0007 --reason "<为什么读不了>"   # 算缺口

   --done 会当场把摘录拿去原文回查，抄错/编造立刻报错。不等最后。

2) 全量审计
   python audit.py <WORKDIR>
   生成 <WORKDIR>/COVERAGE.md，退出码 0 = 全部覆盖且摘录可回查，1 = 有缺口。

铁律: 退出码不为 0，就不许对用户说「全部看完了」。
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LEDGER_HEADER = "id\tstatus\tevidence\tquote\n"
STATUSES = ("done", "skipped", "failed")
MIN_QUOTE = 8          # 摘录至少 8 个非空白字符，太短没有校验意义
MIN_EVIDENCE_TEXT = 8  # 文本条目 evidence 下限
MIN_EVIDENCE_MEDIA = 20  # 非文本条目没有摘录可查，用更严的篇幅下限兜底


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s or "").lower()


def clean(s: str) -> str:
    return (s or "").replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def load_manifest(workdir: Path):
    mf = workdir / "manifest.tsv"
    if not mf.exists():
        raise SystemExit("[audit] 找不到 %s，先跑 scan.py" % mf)
    rows = {}
    with open(mf, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            parts += [""] * (len(header) - len(parts))
            rec = dict(zip(header, parts))
            rows[rec["id"]] = rec
    return rows


def load_ledger(workdir: Path):
    lf = workdir / "ledger.tsv"
    out = {}
    if not lf.exists():
        return out
    with open(lf, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            parts += [""] * (len(header) - len(parts))
            rec = dict(zip(header, parts))
            if rec.get("id"):
                out[rec["id"]] = rec
    return out


def save_ledger(workdir: Path, ledger):
    lf = workdir / "ledger.tsv"
    with open(lf, "w", encoding="utf-8", newline="") as f:
        f.write(LEDGER_HEADER)
        for k, v in ledger.items():
            f.write("\t".join(clean(v.get(c, "")) for c in
                              ("id", "status", "evidence", "quote")) + "\n")


def read_range(path: Path, start: int, end: int) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "big5"):
        try:
            text = raw.decode(enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    if end >= start and end > 0:
        lines = text.splitlines()
        return "\n".join(lines[start - 1:end])
    return text


def verify_quote(base: Path, rec, quote: str):
    """返回 (ok, msg)。ok=True 表示摘录确实出现在源文件对应区间内。"""
    nq = norm(quote)
    if len(nq) < MIN_QUOTE:
        return False, "摘录太短（去空白后 %d 字符，至少 %d）" % (len(nq), MIN_QUOTE)
    p = Path(rec["path"])
    if not p.is_absolute():
        cand = base / p
        if not cand.exists():
            cand = Path.cwd() / p
        p = cand
    if not p.exists():
        return False, "源文件不存在: %s" % p
    try:
        body = read_range(p, int(rec.get("start") or 0), int(rec.get("end") or 0))
    except OSError as e:
        return False, "读不了源文件: %s" % e
    if nq in norm(body):
        return True, "OK"
    return False, "摘录在源文件该区间内找不到——多半是转述、拼凑或凭记忆写的"


def check_stale(rec) -> str:
    """源文件改过 -> 返回 'STALE'，否则 ''."""
    if rec["kind"] != "text" or rec.get("sha1") in ("-", ""):
        return ""
    p = Path(rec["path"])
    try:
        body = read_range(p, int(rec["start"]), int(rec["end"]))
    except OSError:
        return ""
    h = hashlib.sha1(body.encode("utf-8", errors="replace")).hexdigest()[:12]
    return "" if h == rec["sha1"] else "STALE"


def count_lines(path: Path) -> int:
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return -1
    for enc in ("utf-8-sig", "utf-8", "gb18030", "big5"):
        try:
            return len(raw.decode(enc).splitlines())
        except (UnicodeDecodeError, LookupError):
            continue
    return len(raw.decode("utf-8", errors="replace").splitlines())


def grown_files(manifest) -> dict:
    """清单建好之后源文件变长了 → 新增行不在任何条目里，永远读不到。
    返回 {path: (清单覆盖到的最大行, 当前总行数)}"""
    cov = {}
    for rec in manifest.values():
        if rec.get("kind") != "text" or not rec.get("end"):
            continue
        try:
            e = int(rec["end"])
        except ValueError:
            continue
        cov[rec["path"]] = max(cov.get(rec["path"], 0), e)
    out = {}
    for path, maxend in cov.items():
        n = count_lines(Path(path))
        if n > maxend:
            out[path] = (maxend, n)
    return out


def do_record(workdir: Path, manifest, ledger, args):
    rid = args.done or args.skip or args.fail
    if rid not in manifest:
        print("[audit] 清单里没有 %s（先确认 id）" % rid)
        return 1
    rec = manifest[rid]
    status = "done" if args.done else ("skipped" if args.skip else "failed")
    evidence = clean(args.evidence or args.reason or "")
    quote = clean(args.quote or "")

    if status != "done":
        if not evidence:
            print("[audit] %s 记为 %s 必须给 --reason" % (rid, status))
            return 1
        ledger[rid] = {"id": rid, "status": status, "evidence": evidence, "quote": quote}
        save_ledger(workdir, ledger)
        print("[audit] %s -> %s（缺口，不计入覆盖）" % (rid, status))
        return 0

    min_len = MIN_EVIDENCE_TEXT if rec["kind"] == "text" else MIN_EVIDENCE_MEDIA
    if len(norm(evidence)) < min_len:
        print("[audit] %s 的 --evidence 太短（%d 字符，至少 %d），写清这一条到底讲了什么、你看到了什么"
              % (rid, len(norm(evidence)), min_len))
        return 1

    if rec["kind"] == "text":
        if not quote:
            print("[audit] %s 是文本条目，必须给 --quote（原文逐字摘录，不许转述）" % rid)
            return 1
        ok, msg = verify_quote(workdir, rec, quote)
        if not ok:
            print("[audit] %s 摘录回查失败: %s" % (rid, msg))
            print("[audit] 去 %s:L%s-%s 重读，摘一段连续原文再打卡"
                  % (rec["path"], rec.get("start"), rec.get("end")))
            return 1
    else:
        if not quote:
            quote = "n/a"

    ledger[rid] = {"id": rid, "status": "done", "evidence": evidence, "quote": quote}
    save_ledger(workdir, ledger)
    done = sum(1 for v in ledger.values() if v.get("status") == "done")
    tag = "摘录可回查" if rec["kind"] == "text" else "目检结论已记录"
    print("[audit] %s 通过 (%s) | 进度 %d/%d" % (rid, tag, done, len(manifest)))
    return 0


def do_audit(workdir: Path, manifest, ledger):
    total = len(manifest)
    missing, bad_quote, stale, skipped, failed, okhits = [], [], [], [], [], 0
    details = []
    grown = grown_files(manifest)

    for rid, rec in manifest.items():
        row = ledger.get(rid)
        label = rec.get("label") or rec["path"]
        if not row:
            missing.append((rid, label))
            details.append((rid, rec["kind"], label, "未读", "-"))
            continue
        st = row.get("status", "")
        if st == "skipped":
            skipped.append((rid, label, row.get("evidence", "")))
            details.append((rid, rec["kind"], label, "跳过", row.get("evidence", "")))
            continue
        if st == "failed":
            failed.append((rid, label, row.get("evidence", "")))
            details.append((rid, rec["kind"], label, "失败", row.get("evidence", "")))
            continue
        if st != "done":
            missing.append((rid, label))
            details.append((rid, rec["kind"], label, "状态未知", "-"))
            continue

        counted = False
        if rec["kind"] == "text":
            ok, msg = verify_quote(workdir, rec, row.get("quote", ""))
            if ok:
                okhits += 1
                counted = True
                details.append((rid, rec["kind"], label, "已读", "摘录 OK"))
            else:
                bad_quote.append((rid, label, msg))
                details.append((rid, rec["kind"], label, "已读但摘录存疑", msg))
        else:
            if len(norm(row.get("evidence", ""))) < MIN_EVIDENCE_MEDIA:
                bad_quote.append((rid, label, "非文本条目观察结论太短"))
                details.append((rid, rec["kind"], label, "已读但结论太短", "-"))
            else:
                okhits += 1
                counted = True
                details.append((rid, rec["kind"], label, "已读", "目检结论已记录"))

        # 时效性：读的是旧内容就不算通过
        reason = None
        if check_stale(rec):
            reason = "区间内容已变更，需重读"
        elif rec["path"] in grown:
            me, n = grown[rec["path"]]
            reason = "清单只到 L%d，源文件现 %d 行，新增部分未纳入" % (me, n)
        if reason:
            if counted:
                okhits -= 1
            stale.append((rid, label, reason))
            details[-1] = details[-1][:4] + (reason,)

    gaps = len(missing) + len(skipped) + len(failed) + len(bad_quote) + len(stale)
    passed = (gaps == 0)

    lines = []
    lines.append("# 覆盖报告\n")
    lines.append("- 清单条目: **%d**" % total)
    lines.append("- 已读通过: **%d**" % okhits)
    lines.append("- 未读: **%d**" % len(missing))
    lines.append("- 主动跳过: **%d**" % len(skipped))
    lines.append("- 读取失败: **%d**" % len(failed))
    lines.append("- 摘录存疑: **%d**" % len(bad_quote))
    lines.append("- 源文件已变更: **%d**" % len(stale))
    lines.append("- 覆盖率: **%.1f%%**" % (100.0 * okhits / total if total else 0))
    lines.append("")
    lines.append("## 结论: %s\n" % ("PASS - 可以声称全部看完" if passed else "FAIL - 不许声称全部看完"))

    def dump(title, items, fmt):
        if not items:
            return
        lines.append("## %s\n" % title)
        for it in items:
            lines.append(fmt(it))
        lines.append("")

    dump("未读条目", missing, lambda i: "- `%s` %s" % (i[0], i[1]))
    dump("主动跳过", skipped, lambda i: "- `%s` %s — 理由: %s" % (i[0], i[1], i[2]))
    dump("读取失败", failed, lambda i: "- `%s` %s — 理由: %s" % (i[0], i[1], i[2]))
    dump("摘录存疑（原文里找不到）", bad_quote, lambda i: "- `%s` %s — %s" % (i[0], i[1], i[2]))
    dump("源文件已变更 / 清单已过期", stale,
         lambda i: "- `%s` %s — %s（重扫 scan.py 后补读并重新打卡）" % (i[0], i[1], i[2]))

    lines.append("## 台账明细\n")
    lines.append("| id | 类型 | 位置 | 状态 | 校验 |")
    lines.append("|---|---|---|---|---|")
    for d in details:
        lines.append("| %s | %s | %s | %s | %s |" % d)

    rep = workdir / "COVERAGE.md"
    with open(rep, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")

    print("[audit] 清单 %d | 通过 %d | 未读 %d | 跳过 %d | 失败 %d | 摘录存疑 %d | 变更 %d"
          % (total, okhits, len(missing), len(skipped), len(failed), len(bad_quote), len(stale)))
    print("[audit] 覆盖率 %.1f%%" % (100.0 * okhits / total if total else 0))
    if passed:
        print("[audit] PASS - 全部覆盖且摘录可回查，可以声称全部看完")
    else:
        print("[audit] FAIL - 还有 %d 处缺口，禁止对用户说「全部看完了」" % gaps)
    print("[audit] 报告: %s" % rep)
    return 0 if passed else 1


def main():
    ap = argparse.ArgumentParser(description="逐条打卡 + 覆盖审计")
    ap.add_argument("workdir")
    ap.add_argument("--done", metavar="ID", help="标记某条已读")
    ap.add_argument("--skip", metavar="ID", help="标记某条主动跳过（算缺口）")
    ap.add_argument("--fail", metavar="ID", help="标记某条读取失败（算缺口）")
    ap.add_argument("--quote", help="原文逐字摘录，用于回查")
    ap.add_argument("--evidence", help="这一条到底讲了什么 / 你看到了什么")
    ap.add_argument("--reason", help="--skip / --fail 的理由")
    args = ap.parse_args()

    workdir = Path(args.workdir).resolve()
    manifest = load_manifest(workdir)
    ledger = load_ledger(workdir)

    if args.done or args.skip or args.fail:
        sys.exit(do_record(workdir, manifest, ledger, args))
    sys.exit(do_audit(workdir, manifest, ledger))


if __name__ == "__main__":
    main()
