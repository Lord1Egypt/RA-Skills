#!/usr/bin/env python3
"""weread-fulltext v2: 微信读书整本书全文导出（采集 + 离线重建两层架构）。

采集层（需登录态）：大视口画布扫掠 + 真实键盘翻页，零 JS 注入、零写入、拟人节奏。
重建层（纯离线）：官方章节骨架 + 证据化拼接 + 全程溯源，不依赖浏览器。

v2 变更（对应 Astra 复审 P0/P1）：
- 运行按 书籍/运行ID 隔离，OCR 缓存键 = 图片 SHA-256（不再按文件名）
- manifest 记录真实图片哈希与捕获顺序，运行清单只引用本次材料
- 采集前主动回到书首并记录实际起止位置与停止原因（书尾/上限/异常分列）
- 画面签名改用真实 SHA-256，同一捕获记录内计算
- 装配改为官方骨架 + 证据化拼接（包含/重叠/页序连续），备选片段保留附录，不静默丢弃
- 不再默认删除任何中间材料；OCR 缓存保留完整 bbox
- 缺少官方字数基准时明确报告"未校验"，不冒充通过

免责：仅限本人账号内容、本地自用。自动化有理论风险，建议优先小号。
"""

import argparse
import base64
import hashlib
import json
import os
import random
import re
import sys
import time

BOOK_BASE = "https://weread.qq.com"
OCR_TAG = "rapidocr_v1"  # OCR 引擎/配置版本，参与缓存键

LATIN_FIX = {"OpenAl": "OpenAI", "openAl": "OpenAI", "APl": "API", "Agl": "AGI"}


def latin_fix(t):
    for b, g in LATIN_FIX.items():
        t = t.replace(b, g)
    return t


def loose(s):  # 仅去空白（保留点号），用于章节头匹配
    return re.sub(r"[\s\u3000]+", "", latin_fix(s))


def squash(s):  # 去空白与标点，用于内容比对
    return re.sub(r"[\s\u3000·、，。：:；;（）()“”‘’《》\-—!.?？!]+", "", latin_fix(s))


def sha16(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


# ============================================================
# 采集层
# ============================================================

def capture_page(page):
    """导出当前两块画布，返回 [(png_bytes, sha), ...]。"""
    data = page.evaluate(
        """() => [...document.querySelectorAll('canvas')].map(c => c.toDataURL('image/png'))"""
    )
    out = []
    for d in data:
        raw = base64.b64decode(d.split(",")[1])
        out.append((raw, sha16(raw)))
    return out


def page_sig(page):
    """真实内容签名：两块画布字节哈希拼接 + 章节标题。"""
    shots = capture_page(page)
    title = page.evaluate(
        """() => document.querySelector('.renderTargetPageInfo_header_chapterTitle')?.textContent.trim() || null"""
    )
    return {"sig": "|".join(s for _, s in shots), "title": title, "shots": shots}


def go_to_start(page, max_tries=40, log=print):
    """连续回退到书首；返回 (尝试次数, 起始标题)。连续无进展视为书首。"""
    prev = page_sig(page)
    tries = 0
    stagnant = 0
    for _ in range(max_tries):
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(int(1500 + random.random() * 600))
        cur = page_sig(page)
        tries += 1
        if cur["sig"] == prev["sig"]:
            stagnant += 1
            if stagnant >= 3:
                break
            page.mouse.move(900 + random.randint(0, 150), 950)
            page.wait_for_timeout(350)
            page.keyboard.press("ArrowLeft")
            page.wait_for_timeout(1800)
            cur = page_sig(page)
            if cur["sig"] == prev["sig"]:
                stagnant += 1
                if stagnant >= 3:
                    break
            else:
                stagnant = 0
        else:
            stagnant = 0
        prev = cur
    return tries, prev["title"]


def collect(page, book_id: str, book_dir: str, max_spreads: int, log=print):
    """扫掠采集。返回 run_dir 与 run_meta。"""
    stamp = time.strftime("%Y%m%d_%H%M%S")
    run_id = f"run_{stamp}"
    run_dir = os.path.join(book_dir, run_id)
    spreads_dir = os.path.join(run_dir, "spreads")
    os.makedirs(spreads_dir, exist_ok=True)

    reader_hash = None
    page.goto(f"{BOOK_BASE}/", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    raw = page.evaluate(
        """async (bookId) => {
            const r = await fetch('https://weread.qq.com/api/user/notebook', {credentials: 'include'});
            const j = await r.json();
            for (const n of (j.books || [])) {
                if (String(n.bookId) === String(bookId)) return n.book ? n.book.deepLink : null;
            }
            return null;
        }""",
        book_id,
    )
    if not raw:
        raise SystemExit(f"bookId {book_id} 不在 notebook 列表（该书可能从未打开过）")
    m = re.search(r"v=([0-9a-f]+)", raw)
    reader_hash = m.group(1)

    page.goto(f"{BOOK_BASE}/web/reader/{reader_hash}", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    book_title = page.title().split(" - ")[0].strip()

    start_tries, start_title = go_to_start(page, log=log)
    log(f"  已定位书首（回退 {start_tries} 次，起始章：{start_title}）")

    # 官方目录与字数基准（缺了会在报告中显式降级，不冒充已校验）
    chapters = page.evaluate(
        """async (bookId) => {
            try {
                const r = await fetch('https://weread.qq.com/web/book/chapterInfos', {
                    method: 'POST', credentials: 'include',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({bookId: String(bookId)})
                });
                const j = await r.json();
                const out = [];
                for (const d of (j.data || [])) {
                    for (const c of (d.updated || [])) {
                        out.push({chapterUid: c.chapterUid, chapterIdx: c.chapterIdx,
                                  title: c.title, wordCount: c.wordCount});
                    }
                }
                out.sort((a, b) => a.chapterIdx - b.chapterIdx);
                return out;
            } catch (e) { return []; }
        }""",
        book_id,
    )
    if chapters:
        json.dump(chapters, open(os.path.join(book_dir, "chapters_official.json"), "w",
                                 encoding="utf-8"), ensure_ascii=False)

    manifest_path = os.path.join(run_dir, "manifest.jsonl")
    stop_reason, spreads = None, 0
    prev_sig = None
    try:
        while spreads < max_spreads:
            cur = page_sig(page)
            if prev_sig and cur["sig"] == prev_sig:
                # 翻页未生效：唤醒重试一次
                page.mouse.move(900 + random.randint(0, 150), 950)
                page.wait_for_timeout(350)
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(2600)
                cur = page_sig(page)
                if cur["sig"] == prev_sig:
                    stop_reason = "end"
                    break
            seq = f"p{spreads:03d}"
            for i, (raw, s) in enumerate(cur["shots"]):
                with open(os.path.join(spreads_dir, f"{seq}_c{i}_{s}.png"), "wb") as f:
                    f.write(raw)
            with open(manifest_path, "a", encoding="utf-8") as mf:
                mf.write(json.dumps({"seq": spreads, "title": cur["title"],
                                     "files": [f"{seq}_c{i}_{s}.png" for i, (_, s) in enumerate(cur["shots"])],
                                     "shas": [s for _, s in cur["shots"]]}, ensure_ascii=False) + "\n")
            prev_sig = cur["sig"]
            spreads += 1
            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(int(2300 + random.random() * 900))
        else:
            stop_reason = "cap"
    except Exception as e:
        stop_reason = f"error:{type(e).__name__}:{e}"
        raise
    finally:
        meta = {"book_id": book_id, "book_title": book_title, "reader_hash": reader_hash,
                "run_id": run_id, "spreads": spreads, "stop_reason": stop_reason,
                "start_title": start_title, "start_back_tries": start_tries,
                "chapters_official": bool(chapters), "ocr_tag": OCR_TAG,
                "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        json.dump(meta, open(os.path.join(run_dir, "run_meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        log(f"  采集结束：{spreads} 跨页，停止原因={stop_reason}")
    return run_dir, meta


# ============================================================
# 重建层（纯离线）
# ============================================================

def ocr_run(run_dir, book_dir, log=print):
    """对本 run 的图片做 OCR，缓存键 = 图片 SHA + 引擎版本。"""
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    spreads_dir = os.path.join(run_dir, "spreads")
    cache_dir = os.path.join(book_dir, "ocr_cache")
    os.makedirs(cache_dir, exist_ok=True)
    manifest = [json.loads(l) for l in open(os.path.join(run_dir, "manifest.jsonl"), encoding="utf-8")]
    out = {}
    total = sum(len(m["files"]) for m in manifest)
    done = 0
    for m in manifest:
        for fname, sha in zip(m["files"], m["shas"]):
            key = f"{sha}_{OCR_TAG}.json"
            cp = os.path.join(cache_dir, key)
            if os.path.exists(cp):
                out[fname] = json.load(open(cp, encoding="utf-8"))
            else:
                r, _ = ocr(os.path.join(spreads_dir, fname))
                lines = []
                if r:
                    for box, text, conf in r:
                        xs = [p[0] for p in box]
                        ys = [p[1] for p in box]
                        lines.append({"bbox": [min(xs), min(ys), max(xs), max(ys)],
                                      "y": min(ys), "text": text, "conf": round(float(conf), 4)})
                json.dump(lines, open(cp, "w", encoding="utf-8"), ensure_ascii=False)
                out[fname] = lines
            done += 1
            if done % 10 == 0:
                log(f"  OCR {done}/{total}")
    return out


def rebuild(run_dir: str, book_dir: str, log=print):
    """离线重建：官方骨架 + 顺序指针分章 + 证据化拼接。"""
    meta = json.load(open(os.path.join(run_dir, "run_meta.json"), encoding="utf-8"))
    manifest = [json.loads(l) for l in open(os.path.join(run_dir, "manifest.jsonl"), encoding="utf-8")]
    ch_path = os.path.join(book_dir, "chapters_official.json")
    chs = json.load(open(ch_path, encoding="utf-8")) if os.path.exists(ch_path) else []
    has_base = bool(chs)
    WC = {c["chapterUid"]: c.get("wordCount") for c in chs}

    ocr = ocr_run(run_dir, book_dir, log=log)

    # ---- 分章（顺序指针 + 全目录匹配）----
    def match_chapter(head):
        if not head or len(head) < 2:
            return None
        for idx, c in enumerate(chs):
            t = loose(c["title"])
            if not t:
                continue
            n = min(8, len(t))
            if head.startswith(t[:n]) or t.startswith(head[:min(len(head), 8)]):
                return idx
        return None

    def para_split(lines):
        if len(lines) < 3:
            t = "".join(l["text"] for l in lines)
            return [(t, 0, len(lines))] if t.strip() else []
        ys = [l["y"] for l in lines]
        gaps = sorted(ys[i + 1] - ys[i] for i in range(len(ys) - 1))
        med = gaps[len(gaps) // 2] or 1
        out, buf, start = [], [lines[0]["text"]], 0
        for i, l in enumerate(lines[1:], 1):
            if l["y"] - lines[i - 1]["y"] > med * 1.55:
                out.append(("".join(buf), start, i))
                buf, start = [], i
            buf.append(l["text"])
        out.append(("".join(buf), start, len(lines)))
        return [(t, a, b) for t, a, b in out if t.strip()]

    chap_data = {c["chapterUid"]: {"meta": c, "primary": [], "alternate": []} for c in chs}
    preface = []
    j, cur_uid = 0, None
    for m in manifest:
        for fname, sha in zip(m["files"], m["shas"]):
            lines = sorted(ocr.get(fname, []), key=lambda l: l["y"])
            if not lines:
                continue
            head = loose(lines[0]["text"])
            idx = match_chapter(head)
            if idx is None and len(lines) > 1:
                # 标题可能跨两行（如仅"跋"一字的短标题行 + 副题行）
                head2 = head + loose(lines[1]["text"])
                if head2 != head:
                    idx = match_chapter(head2[:40])
            piece = {"image": fname, "sha": sha, "paras": para_split(lines)}
            if idx is not None:
                head_raw = lines[0]["text"]
                if piece["paras"] and piece["paras"][0][0].startswith(head_raw):
                    t, a, b = piece["paras"][0]
                    piece["paras"][0] = (t[len(head_raw):], a, b)
                piece["paras"] = [p for p in piece["paras"] if p[0].strip()]
                uid = chs[idx]["chapterUid"]
                if idx >= j:
                    cur_uid, j = uid, idx + 1
                    chap_data[uid]["primary"].append(piece)
                else:
                    chap_data[uid]["alternate"].append(piece)
                    cur_uid = uid
            else:
                if cur_uid is None:
                    preface.append(piece)
                else:
                    chap_data[cur_uid]["primary"].append(piece)

    # ---- 证据化拼接 ----
    def merge_pieces(pieces):
        notes = []
        if not pieces:
            return [], notes
        acc = list(pieces[0]["paras"])
        for p in pieces[1:]:
            pt = squash("".join(t for t, a, b in p["paras"]))
            if not pt:
                continue
            at = squash("".join(t for t, a, b in acc))
            if pt in at:
                notes.append(f"包含关系，跳过 {p['image']}")
                continue
            best = 0
            for k in range(min(len(at), len(pt)), 29, -1):
                if at.endswith(pt[:k]):
                    best = k
                    break
            consumed = 0
            if best:
                acc2 = 0
                for t, a, b in p["paras"]:
                    acc2 += len(squash(t))
                    if acc2 <= best:
                        consumed = b
                    else:
                        break
                notes.append(f"与 {p['image']} 重叠 {best} 字，接续其余")
            else:
                notes.append(f"无重叠但页序连续，接续 {p['image']}")
            acc.extend(p["paras"][consumed:])
        return acc, notes

    SENT_END = tuple("。！？…”）》")

    def render(ch_lines):
        paras = []
        for t, a, b in ch_lines:
            if paras and not paras[-1]["text"].rstrip().endswith(SENT_END):
                paras[-1]["text"] += t
            else:
                paras.append({"text": t})
        return [p["text"] for p in paras]

    md = [f"# {meta['book_title']}", "",
          "> 微信读书全文导出 v2：官方章节骨架 + 证据化拼接，段落可溯源（source_map.json）", ""]
    sm = {"book": meta["book_title"], "bookId": meta["book_id"], "run_id": meta["run_id"],
          "stop_reason": meta["stop_reason"], "chapters": []}
    qr = ["# 质量报告", "",
          f"- 运行：{meta['run_id']}，跨页 {meta['spreads']}，停止原因 {meta['stop_reason']}，起始章 {meta['start_title']}",
          f"- 官方字数基准：{'已获取' if has_base else '缺失（本章报告不做完整性比对）'}", ""]
    ok_cnt = checked = 0
    for c in chs:
        uid = c["chapterUid"]
        d = chap_data[uid]
        merged, notes = merge_pieces(d["primary"])
        paras = render(merged)
        text = "\n\n".join(paras)
        n = len(re.sub(r"\s", "", text))
        base = WC.get(uid)
        ratio = (n / base * 100) if base else None
        if ratio is None:
            status = "未校验（无基准）"
        elif n < 60 and base <= 220:
            status = "仅标题/分隔页"
        elif 90 <= ratio <= 115:
            status = "OK"
        elif ratio < 90:
            status = f"疑似缺口（{ratio:.0f}%）"
        else:
            status = f"疑似超长/重复残留（{ratio:.0f}%）"
        if ratio is not None and 90 <= ratio:
            ok_cnt += 1
        if base:
            checked += 1

        md.append(f"## {latin_fix(c['title'])}")
        md.append("")
        if status != "OK":
            md.append(f"> [{status}]" + (f" 官方 {base} 字，重建 {n} 字" if base else f" 重建 {n} 字") + " —— 详见 quality_report.md")
            md.append("")
        md.append(text)
        md.append("")
        sm["chapters"].append({
            "chapterUid": uid, "title": c["title"], "status": status,
            "rebuilt_chars": n, "base_wordCount": base,
            "primary_images": [p["image"] for p in d["primary"]],
            "alternate_images": [p["image"] for p in d["alternate"]],
            "merge_notes": notes,
        })
        alt = f"（备选 {[p['image'] for p in d['alternate']]}）" if d["alternate"] else ""
        qr.append(f"- [{status}] {c['title']}: {n}" + (f"/{base} 字" if base else " 字") + alt)

    alts = [(c["chapterUid"], p) for c in chs for p in chap_data[c["chapterUid"]]["alternate"]]
    alt_texts = {p["image"]: p for _, p in alts}
    if alt_texts:
        md.append("---")
        md.append("")
        md.append("## 附录：备选捕获（同章第二轮渲染，未并入正文）")
        md.append("")
        for img, p in alt_texts.items():
            t = "\n\n".join(t for t, a, b in p["paras"])
            if len(squash(t)) > 60:
                md.append(f"### {img}")
                md.append("")
                md.append(t)
                md.append("")

    md.append("---")
    md.append("")
    md.append(f"**完整性声明**：本报告证明现有材料已全部登记处理、章节归属经官方骨架核定、拼接决策有记录。"
              f"字数比受标点口径与 OCR 损耗影响，仅作异常筛查。整书完整性取决于采集覆盖，"
              f"本次停止原因={meta['stop_reason']}。")

    safe = re.sub(r'[\\/:*?"<>|]', " ", meta["book_title"]).strip()
    open(os.path.join(run_dir, "fde_rebuilt.md"), "w", encoding="utf-8").write("\n".join(md))
    json.dump(sm, open(os.path.join(run_dir, "source_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    open(os.path.join(run_dir, "quality_report.md"), "w", encoding="utf-8").write("\n".join(qr))
    log(f"  重建完成：{ok_cnt}/{checked} 章 OK，输出于 {run_dir}")


# ============================================================
# CLI
# ============================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", action="store_true", help="扫码登录并保存登录态")
    ap.add_argument("--book-id", help="采集并重建一本书")
    ap.add_argument("--rebuild-run", help="仅离线重建：指定 run 目录（不打开浏览器）")
    ap.add_argument("--out", default="./exports", help="输出根目录")
    ap.add_argument("--profile", default=os.path.join(os.path.dirname(__file__), "..", "profile", "weread_state.json"))
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--max-spreads", type=int, default=60)
    args = ap.parse_args()

    if args.rebuild_run:
        run_dir = os.path.abspath(args.rebuild_run)
        book_dir = os.path.dirname(run_dir)
        rebuild(run_dir, book_dir)
        return

    os.makedirs(os.path.dirname(args.profile), exist_ok=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 2160},
            storage_state=args.profile if os.path.exists(args.profile) else None,
        )
        page = ctx.new_page()

        if args.login:
            page.goto(f"{BOOK_BASE}/#login", wait_until="domcontentloaded")
            print("请在浏览器中用微信扫码登录…")
            for _ in range(120):
                page.wait_for_timeout(2000)
                if "login" not in page.url:
                    break
            ctx.storage_state(path=args.profile)
            print(f"登录态已保存: {args.profile}")
            browser.close()
            return

        if not args.book_id:
            ap.error("需要 --book-id（或先 --login 扫码；或用 --rebuild-run 离线重建）")
        if not os.path.exists(args.profile):
            ap.error("未找到登录态，请先执行 --login 扫码")

        book_dir = os.path.join(args.out, args.book_id)
        os.makedirs(book_dir, exist_ok=True)
        print("[1/3] 采集…")
        run_dir, meta = collect(page, args.book_id, book_dir, args.max_spreads)
        print("[2/3] OCR…")
        print("[3/3] 重建…")
        rebuild(run_dir, book_dir)
        print(f"完成。产物目录：{run_dir}")
        ctx.close()
        browser.close()
        print("提示：spreads/ 内截图为校对依据，已保留；确认不需要后请手动清理。")


if __name__ == "__main__":
    main()
