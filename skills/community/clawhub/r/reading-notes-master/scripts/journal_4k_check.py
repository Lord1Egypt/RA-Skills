#!/usr/bin/env python3
"""journal_4k_check.py — 期刊 4K 复刻四门验收（v2.11）
同一把尺量两次：度量方法与 magcorpus/analyze_mags.py 完全同参数
（字体清洗 ^[A-Z]{6}\\+ / 栏数 30pt bin 聚类 / 覆盖率上限 1.6）。

用法:
  python3 journal_4k_check.py <rendered.pdf> --profile NG --json report.json
  python3 journal_4k_check.py <rendered.png> --profile HBR      # 位图走 J4 像素门
  python3 journal_4k_check.py --list

退出码: 0 = 四门全过 | 1 = 有 WARN | 2 = 有 FAIL
门禁:
  J1 字体 DNA   产物字体族命中官方前缀或替代字体前缀, serif+sans 两栈齐备
  J2 色板签名   签名色 >=1 出现在矢量填充 top8 (RGB 距离 <=36); 满版刊降级像素主色
  J3 栅格边距   边距比例差 <=12pp / 栏数差 <=1 / 图密度分型不换型
  J4 4K 像素    位图长边>=3840 且短边>=2160; 矢量 PDF 等效, 内嵌位图逐图反推有效 DPI
"""
import argparse, json, math, re, statistics, sys
from collections import Counter
from pathlib import Path

try:
    import pymupdf as fitz  # PyMuPDF >= 1.24
except ImportError:
    try:
        import fitz  # 旧版回退
    except ImportError:
        print("FAIL: 需要 PyMuPDF (pip install pymupdf)", file=sys.stderr)
        sys.exit(2)

# ---------------- 16 个复刻档案（实测值固化自 magcorpus/mags_metrics.json；v2.13 增补 2 条）----------------
# 【v2.13 认知修正】常规周刊与特辑是两条不同契约，不得混用：
#   旧 TIME_SPECIAL 卡实测描述的是「Time Special Edition（满版特辑）」，却被当作常规周刊用，
#   是已确认的根因错误。现保留该键向后兼容，另立 TIME_WEEKLY（常规周刊）与
#   TIME_SPECIAL_EDITION（特辑语义别名）两条独立卡；常规周刊任务一律用 TIME_WEEKLY。
# fonts_serif / fonts_sans: 前缀匹配列表（官方在前, 替代在后, 任一命中即过 J1）
# sig_colors: 签名色（J2 任一命中即过）; fills 记录降级来源 degraded=True
# margin_l/r: 文本边距比例(相对页宽); cols: 栏数; density: 拼贴流/满版流/克制流/文字主导(coverage 基准)
PROFILES = {
    "NG": dict(name="National Geographic 主刊", page_pt=(496, 720), dpi=384,
               fonts_serif=["GrosvenorBook", "SourceSerif4", "Source Serif", "Tiempos", "Georgia"],
               fonts_sans=["Geograph", "GTWalsheim", "GT Walsheim", "Regional", "Inter", "Helvetica"],
               sig_colors=["#FFD201", "#E77741", "#B9E5FA", "#ED1B2E"],
               margin_l=51.6, margin_r=27.0, cols=3, density="collage", cov_ref=0.68),
    "BBW": dict(name="Bloomberg Businessweek", page_pt=(568, 757), dpi=366,
                fonts_serif=["BWText", "Tiempos", "Georgia", "Lora"],
                fonts_sans=["BWHaas", "HelveticaNow", "Inter", "Helvetica", "Archivo"],
                sig_colors=["#AD6B42", "#F4838D", "#E11A22", "#DCCD45"],
                margin_l=38.3, margin_r=37.7, cols=5, density="collage", cov_ref=0.68),
    "BARRONS": dict(name="Barron's", page_pt=(756, 765), dpi=366,
                    fonts_serif=["FarnhamText", "Century", "Georgia", "PTSerif", "PT Serif"],
                    fonts_sans=["B4Retina", "TitlingGothicFB", "RobotoCondensed", "Roboto Condensed", "Archivo"],
                    sig_colors=["#375177", "#FDDECF", "#D6E5E4"],
                    margin_l=38.7, margin_r=44.5, cols=2, density="restraint", cov_ref=0.23),
    "SCIENCE": dict(name="Science (AAAS)", page_pt=(594, 756), dpi=366,
                    fonts_serif=["MillerDaily", "SourceSerif4", "Source Serif", "Tiempos", "Georgia"],
                    fonts_sans=["BentonSans", "Akkurat", "BarlowCondensed", "Barlow Condensed", "Archivo"],
                    sig_colors=["#253D92", "#C72426", "#58595B"],
                    margin_l=44.4, margin_r=44.3, cols=3, density="restraint", cov_ref=0.40),
    "SCIAM": dict(name="Scientific American", page_pt=(585, 774), dpi=357,
                  fonts_serif=["MartinaPlantijn", "Plantijn", "Lora", "Georgia"],
                  fonts_sans=["GTAmerica", "GT America", "Inter", "Apres", "Helvetica"],
                  sig_colors=["#FFCA38", "#001722", "#8C0C42"],
                  margin_l=35.2, margin_r=41.6, cols=2, density="balance", cov_ref=0.56),
    "SCI_NEWS": dict(name="Science News", page_pt=(558, 774), dpi=357,
                     fonts_serif=["Wulkan", "PTSerif", "PT Serif", "Lora", "Garamond"],
                     fonts_sans=["HelveticaNeue", "Helvetica Neue", "WixMadefor", "Inter"],
                     sig_colors=["#9FBDE3", "#005B91", "#13254B"],
                     margin_l=30.7, margin_r=45.4, cols=3, density="photo", cov_ref=0.83),
    "NEW_SCIENTIST": dict(name="New Scientist", page_pt=(575, 757), dpi=366,
                          fonts_serif=["TheAntiquaB", "Antiqua", "Lora", "Georgia"],
                          fonts_sans=["EnzoPro", "Enzo", "MundoSans", "Mundo", "Archivo", "Inter"],
                          sig_colors=["#CC1D4C", "#25AE48", "#0079C1", "#F36F21"],
                          margin_l=36.1, margin_r=36.3, cols=5, density="balance", cov_ref=0.46),
    "VOGUE": dict(name="Vogue Singapore（满版降级卡）", page_pt=(624, 808), dpi=342,
                  fonts_serif=["SaolText", "Saol", "PlayfairDisplay", "Playfair Display", "Didot"],
                  fonts_sans=["PPNeueMachina", "NeueMachina", "SpaceGrotesk", "Space Grotesk", "FancyCutPro"],
                  sig_colors=[], sig_degraded=True,
                  margin_l=13.5, margin_r=69.9, cols=1, density="fullbleed", cov_ref=1.0),
    "COSMO": dict(name="Cosmopolitan UK", page_pt=(567, 737), dpi=375,
                  fonts_serif=["ChronicleText", "Chronicle", "Lora", "Georgia"],
                  fonts_sans=["BasisGrotesque", "Basis Grotesque", "Archivo", "Inter"],
                  sig_colors=["#FF447E", "#309156"],
                  margin_l=16.3, margin_r=64.9, cols=2, density="fullbleed", cov_ref=0.98),
    # ---- v2.13：常规周刊 vs 特辑拆为两条互不覆盖的独立契约 ----
    # TIME_WEEKLY：Time 美国版常规周刊。74 页、每页字符中位数 3043、
    #   图像覆盖中位数 0.35、正文 10/8.8pt、文字主导（text-led）。
    #   J3 参数按 measure_pdf() 对原刊实测：margin_l=25.3、margin_r=45.3、
    #   cols_est=2、cov_avg=0.471、内嵌位图有效 DPI=300。
    #   切勿用「正文 x0 / 页宽 ≈ 5.3%」充当 margin_l：四门量的是
    #   12 个采样页各自 median(x0) 再跨页取 median，与视觉左边距不是一回事。
    "TIME_WEEKLY": dict(name="Time 美国版常规周刊", page_pt=(567.03, 756.0), dpi=300,
                        fonts_serif=["HaffnerTIME", "HaffnerTIMEDisplay"],
                        fonts_sans=["ITCFranklinGothicStd", "FranklinGothic"],
                        sig_colors=["#231F20", "#000000", "#ED1C24", "#FFFFFF"], sig_degraded=False,
                        margin_l=25.3, margin_r=45.3, cols=2, density="text-led", cov_ref=0.471),
    # TIME_SPECIAL：保留原键与取值向后兼容。注意——本卡实际描述的是「Time 特辑（满版降级卡）」，
    #   不适用于常规周刊（常规周刊请用 TIME_WEEKLY）；仅用于满版特辑的旧调用。
    "TIME_SPECIAL": dict(name="Time 特辑（满版降级卡）", page_pt=(576, 783), dpi=353,
                         fonts_serif=["HaffnerTIME", "Haffner", "Playfair", "Georgia"],
                         fonts_sans=["ITCFranklinGothic", "FranklinGothic", "Franklin Gothic", "Archivo"],
                         sig_colors=[], sig_degraded=True,
                         margin_l=28.3, margin_r=11.4, cols=3, density="fullbleed", cov_ref=1.0),
    # TIME_SPECIAL_EDITION：TIME_SPECIAL 的语义别名（同参数），供新代码按语义取名。
    "TIME_SPECIAL_EDITION": dict(name="Time Special Edition（满版特辑）", page_pt=(576, 783), dpi=353,
                                 fonts_serif=["HaffnerTIME", "Haffner", "Playfair", "Georgia"],
                                 fonts_sans=["ITCFranklinGothic", "FranklinGothic", "Franklin Gothic", "Archivo"],
                                 sig_colors=[], sig_degraded=True,
                                 margin_l=28.3, margin_r=11.4, cols=3, density="fullbleed", cov_ref=1.0),
    "SPECTATOR": dict(name="The Spectator", page_pt=(596, 784), dpi=353,
                      fonts_serif=["TimesNewRoman", "Times New Roman", "GoudyOldSty", "Goudy", "Times"],
                      fonts_sans=["FuturaPT", "Futura", "Jost", "CenturyGothic"],
                      sig_colors=["#001346", "#C9252B", "#00A650"],
                      margin_l=36.0, margin_r=36.1, cols=1, density="balance", cov_ref=0.45),
    "OBSERVER": dict(name="The Observer", page_pt=(820, 1018), dpi=272,
                     fonts_serif=["SoleSerifText", "SoleSerif", "CaslonIonic", "Caslon", "SourceSerif4", "Source Serif"],
                     fonts_sans=["PreloPro", "Prelo", "WorkSans", "Work Sans", "Inter"],
                     sig_colors=["#38512F", "#9B005C", "#EA8187"],
                     margin_l=43.1, margin_r=44.0, cols=3, density="restraint", cov_ref=0.38),
    "HIW": dict(name="How It Works", page_pt=(652, 842), dpi=329,
                fonts_serif=[], serif_degraded=True,
                fonts_sans=["Saira", "SairaCondensed", "Khand", "Kanit", "Barlow"],
                sig_colors=["#CD489C", "#F3612A", "#A088C3"],
                margin_l=31.5, margin_r=48.1, cols=3, density="balance", cov_ref=0.60),
    "QNWZ": dict(name="青年文摘（Type3 中文降级卡）", page_pt=(612, 792), dpi=349,
                 fonts_serif=[], serif_degraded=True, fonts_sans=[], sans_degraded=True, sig_degraded=True,
                 sig_colors=[],
                 margin_l=44.4, margin_r=52.5, cols=2, density="restraint", cov_ref=0.15),
}

DENSITY_TOL = {"collage": (5, None), "fullbleed": (0.90, 1.6), "restraint": (None, 0.60),
               "balance": (0.30, 0.90), "photo": (0.60, 1.15),
               "text-led": (None, 0.60)}  # cov 区间下/上限 (None=不设); text-led 为 v2.13 TIME_WEEKLY 新增分型(文字主导/低图像覆盖), 避免 J3 查表 KeyError

# ---------------- 度量（与 analyze_mags.py 同参数）----------------
def clean_font(n):
    return re.sub(r"^[A-Z]{6}\+", "", n)

def hx(c):
    if c is None: return None
    if isinstance(c, int): return f"#{c:06X}"
    if isinstance(c, (list, tuple)):
        return "#" + "".join(f"{int(round(v*255)):02X}" for v in c[:3])
    return str(c)

def rgb(hexs):
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i+2], 16) for i in (0, 2, 4))

def color_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(rgb(a), rgb(b))))

def sample_pages(n, k=12):
    # 与 analyze_mags.py 完全同参：12 页采样（同一把尺子量两次的前提）
    if n <= k: return list(range(n))
    picks = {0, 1, 2, 3, n//2, n//2+1, 3*n//4, n//4, n-2, n-1}
    step = max(1, n // k)
    i = 0
    while len(picks) < k and i < n:
        picks.add(i); i += step
    return sorted(picks)[:k]

def measure_pdf(path):
    doc = fitz.open(str(path))
    fonts, sizes, tcolors = Counter(), Counter(), Counter()
    vfill = Counter()
    imgs_pp, cov_pp = [], []
    x0s, x1s, pws = [], [], []
    img_dpis = []
    page_ids = sample_pages(doc.page_count)
    for pno in page_ids:
        page = doc[pno]
        W, H = page.rect.width, page.rect.height
        pws.append(W)
        d = page.get_text("dict")
        xs0, xs1 = [], []
        for blk in d.get("blocks", []):
            if blk.get("type") == 1: continue
            for ln in blk.get("lines", []):
                for sp in ln.get("spans", []):
                    t = sp.get("text", "").strip()
                    if not t: continue
                    fonts[clean_font(sp["font"])] += len(t)
                    sizes[round(sp["size"], 1)] += len(t)
                    tcolors[hx(sp.get("color"))] += len(t)
                    xs0.append(sp["bbox"][0]); xs1.append(sp["bbox"][2])
        if xs0:
            x0s.append(statistics.median(xs0)); x1s.append(statistics.median(xs1))
        try:
            for dr in page.get_drawings()[:200]:
                if dr.get("fill"): vfill[hx(dr["fill"])] += 1
        except Exception:
            pass
        rects = []
        try:
            for img in page.get_images(full=True):
                for r in page.get_image_rects(img[0]):
                    rects.append(r)
                    # 只对主图（显示宽 >= 25% 页宽）反推有效 DPI；小贴片是装饰元素不设门
                    if r.width >= W * 0.25 and img[2]:
                        eff = img[2] / (r.width / 72.0)  # px 源宽 / 显示宽 in
                        if eff < 10000: img_dpis.append(round(eff))
        except Exception:
            pass
        imgs_pp.append(len(rects))
        area = sum(r.width * r.height for r in rects if r)
        cov_pp.append(min(1.6, area / (W * H)) if W and H else 0)
    doc.close()
    bins = Counter(int(x // 30) for x in x0s)
    cols_est = sum(1 for _, c in bins.most_common(8) if c >= max(1, len(x0s) * 0.15))
    return dict(
        page_pt=(round(statistics.median(pws)), None), n_pages=len(pws),
        fonts_top=[f for f, _ in fonts.most_common(10)],
        text_colors=[h for h, _ in tcolors.most_common(6)],
        fills_top=[h for h, _ in vfill.most_common(12)],
        margin_l_ratio=round(statistics.median(x0s) / statistics.median(pws) * 100, 1) if x0s else None,
        margin_r_ratio=round((statistics.median(pws) - statistics.median(x1s)) / statistics.median(pws) * 100, 1) if x1s else None,
        cols_est=cols_est,
        imgs_per_page=round(statistics.mean(imgs_pp), 2) if imgs_pp else 0,
        cov_avg=round(statistics.mean(cov_pp), 3) if cov_pp else 0,
        img_dpis=sorted(set(img_dpis))[:8],
        size_buckets=dict(sizes),
    )

def measure_png(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是 PNG 文件（PNG 路径仅支持 .png；PDF 请直接传入）")
    w = int.from_bytes(head[16:20], "big"); h = int.from_bytes(head[20:24], "big")
    return dict(png=(w, h))

# ---------------- 四门判定 ----------------
def check(prof, m, min_long, min_short):
    gates, degraded = [], []

    def add(gate, status, detail):
        gates.append(dict(gate=gate, status=status, detail=detail))

    # J1 字体 DNA
    ftop = m.get("fonts_top", [])
    serif_hit = [f for f in ftop for p in prof["fonts_serif"] if f.startswith(p)]
    sans_hit = [f for f in ftop for p in prof["fonts_sans"] if f.startswith(p)]
    if prof.get("sans_degraded"):
        degraded.append("J1 profile 为 Type3/中文降级卡, 字体门转人工核对")
        add("J1", "WARN", f"降级卡: 产物字体 top3 = {ftop[:3]}")
    elif prof.get("serif_degraded"):
        ok = bool(sans_hit)
        add("J1", "PASS" if ok else "FAIL",
            f"单栈卡(sans): 命中 {sans_hit[:2] or '无'}; serif 栈按豁免")
        if not ok: pass
    else:
        ok = bool(serif_hit) and bool(sans_hit)
        add("J1", "PASS" if ok else "FAIL",
            f"serif 命中 {serif_hit[:2] or '无'} / sans 命中 {sans_hit[:2] or '无'} (top5: {ftop[:5]})")

    # J2 色板签名
    if prof.get("sig_degraded"):
        degraded.append("J2 满版/双色降级卡, 色板门转像素或人工")
        add("J2", "WARN", f"降级卡: 产物文字色 {m.get('text_colors', [])[:4]}")
    else:
        cand = m.get("fills_top", []) or m.get("text_colors", [])
        hit = None
        for sig in prof["sig_colors"]:
            for c in cand:
                if c and color_dist(sig, c) <= 36:
                    hit = (sig, c); break
            if hit: break
        add("J2", "PASS" if hit else "FAIL",
            f"签名色命中 {hit or '无'} (产物填充 top6: {cand[:6]})")

    # J3 栅格边距
    ml, mr, cols, cov = (m.get("margin_l_ratio"), m.get("margin_r_ratio"),
                         m.get("cols_est"), m.get("cov_avg"))
    if ml is None:
        add("J3", "FAIL", "产物无可提取文本层（图片型产物?）")
    else:
        dl = abs(ml - prof["margin_l"])
        dr = abs(mr - prof["margin_r"]) if mr is not None else 99
        cok = dl <= 12 and dr <= 12
        lok = abs((cols or 0) - prof["cols"]) <= 1
        if prof["density"] == "collage":
            ipp = m.get("imgs_per_page", 0)
            dok, dnote = ipp >= 5, f"拼贴流图/页 {ipp} (门 >=5)"
        else:
            lo, hi = DENSITY_TOL[prof["density"]]
            dok = (lo is None or cov >= lo) and (hi is None or cov <= hi)
            dnote = f"覆盖 {cov:.0%} vs {prof['density']} 区间[{lo},{hi}]"
        status = "PASS" if (cok and lok and dok) else "FAIL"
        add("J3", status,
            f"L {ml}% vs {prof['margin_l']}% (Δ{dl:.1f}pp) / R Δ{dr:.1f}pp / "
            f"栏 {cols} vs {prof['cols']} / {dnote}")

    # J4 4K 像素
    if "png" in m:
        w, h = m["png"]
        ok = max(w, h) >= min_long and min(w, h) >= min_short
        add("J4", "PASS" if ok else "FAIL", f"PNG {w}x{h} (门 {min_long}x{min_short})")
    else:
        dpis = m.get("img_dpis", [])
        # 目标 DPI = max(profile 设计 DPI, min_long 反推 DPI)；profile 卡为该刊设计下限
        tgt = max(prof["dpi"], math.ceil(min_long / (max(prof["page_pt"]) / 72.0)))
        weak = [d for d in dpis if d < tgt * 0.9]
        if not dpis:
            add("J4", "PASS", f"vector-only 等效 4K (profile DPI 目标 {tgt})")
        elif not weak:
            add("J4", "PASS", f"内嵌位图有效 DPI {dpis} 全部 >= {tgt}*0.9")
        else:
            add("J4", "FAIL", f"位图 DPI 不足: {weak} < {tgt}*0.9 (需先 superres.sh 4x 超分再入版)")
    return gates, degraded

# ---------------- 主流程 ----------------
def main():
    ap = argparse.ArgumentParser(description="期刊 4K 复刻四门验收 (v2.11)")
    ap.add_argument("target", nargs="?", help="渲染产物 .pdf / .png")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="复刻档案卡")
    ap.add_argument("--json", dest="jsonout", help="验收报告输出路径")
    ap.add_argument("--min-long", type=int, default=3840)
    ap.add_argument("--min-short", type=int, default=2160)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for k, p in sorted(PROFILES.items()):
            print(f"{k:14s} {p['name']:28s} {p['page_pt'][0]}x{p['page_pt'][1]}pt "
                  f"dpi={p['dpi']} cols={p['cols']} {p['density']}")
        return

    if not args.target or not args.profile:
        ap.error("需要 <target> 与 --profile（或 --list）")
    prof = PROFILES[args.profile]
    path = Path(args.target)
    if not path.exists():
        print(f"FAIL: 文件不存在 {path}", file=sys.stderr); sys.exit(2)

    if path.suffix.lower() == ".pdf":
        m = measure_pdf(path)
        m["page_pt"] = (m["page_pt"][0], None)
    else:
        m = measure_png(path)

    gates, degraded = check(prof, m, args.min_long, args.min_short)
    report = dict(target=str(path), profile=args.profile, profile_name=prof["name"],
                  gates=gates, degraded_notes=degraded, metrics=m,
                  min_long=args.min_long, min_short=args.min_short)
    if args.jsonout:
        Path(args.jsonout).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"== 期刊 4K 复刻验收 · {args.profile} ({prof['name']}) · {path.name}")
    for g in gates:
        mark = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}[g["status"]]
        print(f"  {mark} {g['gate']}  {g['detail']}")
    for n in degraded:
        print(f"  [note] {n}")
    st = [g["status"] for g in gates]
    code = 2 if "FAIL" in st else (1 if "WARN" in st else 0)
    print(f"== 结果: {'FAIL' if code == 2 else ('WARN' if code == 1 else 'ALL PASS')} (exit {code})"
          + (f" · 报告 -> {args.jsonout}" if args.jsonout else ""))
    sys.exit(code)

if __name__ == "__main__":
    main()
