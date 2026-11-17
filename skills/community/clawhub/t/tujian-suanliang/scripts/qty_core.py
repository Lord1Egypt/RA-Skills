#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""土建算量：一张结构图 → 一次索引 → 秒级按层出混凝土方量与钢筋估算带。

分工：解图交给已发布的 cad-file-reader（本脚本不自己解析 DWG）；本脚本只做
索引、楼层切分、口径计算与计划单输出。缓存命中时完全不碰图纸。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse, bisect, collections, csv, hashlib, io, json, os, re, sqlite3, subprocess, sys, time
from pathlib import Path

from contract_guard import GuardError, guard_contract, stamp_result
import contract_support as cs
import entry_gate as eg

SKILL_NAME = "tujian-suanliang"
SKILL_VERSION = "0.9.44"

_RULES_PATH = Path(__file__).resolve().parents[1] / "rules" / "口径.json"
_RULES_TEXT = _RULES_PATH.read_text(encoding="utf-8")
RULES = json.loads(_RULES_TEXT)
RULES_SHA = hashlib.sha256(_RULES_TEXT.encode("utf-8")).hexdigest()[:8]   # 口径指纹，换人复算能对上
CACHE_VERSION = "0.4.0"
MEMBER_PATTERNS = {
    "柱": re.compile(r"^(KZ|ZHZ|LZ|XZ|GZ|GAZ|WAZ|YAZ)\d+[a-zA-Z]?"),
    "梁": re.compile(r"^(WKL|KL|JZL|XL|L|KZL|JL|QL|LL)\d+[a-zA-Z]?"),
    "板": re.compile(r"^(LB|WB|XB|YKB|B|C)\d+[a-zA-Z]?"),
    "墙": re.compile(r"^(Q|QZ|YBZ|GBZ|AZ|BZ)\d+[a-zA-Z]?"),
}
STEEL_GRADE_RE = re.compile(r"^Q[2-5]\d{2}[A-Z]?$")   # Q235/Q345/Q355B 是钢材牌号，不是墙编号
# 混凝土强度等级（GB 50010 序列 C15~C80）：结构图上到处都是 C30/C35/C40，
# 而"板"的编号前缀恰好含 C，会把强度等级误判成板编号、把板数量与规格清单灌水。
# 取舍：真实存在"板编号 C30"时会漏，但"多出一堆假板"的危害远大于"漏一块板"。
CONCRETE_GRADE_RE = re.compile(r"^C(1[5-9]|[2-7]\d|80)$")
SIZE_RE = re.compile(r"(?<!\d)(\d{2,4})\s*[x×X]\s*(\d{2,4})(?!\d)")   # 前后不许再粘数字，防"XL4 600x800"被读成4600x800
THK_RE = re.compile(r"h\s*=\s*(\d{2,3})")
SPAN_RE = re.compile(r"\((\d{1,2})([AB]?)\)")
TITLE_RE = re.compile(r"(图|表)$")
# 图签栏栏目名不是图名：图签里"绘    图""设    计"带填空空格，且落在图框外角落，
# 若当图名收进来，会挤进真图名清单、被楼层切分当成一层去取数。
TITLE_BLOCK_RE = re.compile(r"绘\s*图|制\s*图|描\s*图|晒\s*图|设\s*计|校\s*对|审\s*核|审\s*定|"
                            r"项目负责人|专业负责人|工种负责人|建设单位|设计单位|工程名称|项目名称|子项名称|"
                            r"图\s*号|图\s*别|日\s*期|比\s*例|会\s*签|签\s*名|出图专用章|注册(师|章)")


TITLE_R_LADDER = (30000.0, 60000.0, 120000.0, 160000.0)   # 图名邻域半径档位，见 find_titles


def is_title_noise(t):
    """图签/标题栏文字排除：填空空格（绘    图）、栏目名（设计单位、图号…）、
    说明句（"H为结构标高，详层高表"）都不是图名。"""
    if re.search(r"\s{2,}", t):
        return True
    if "，" in t or "。" in t:          # 带逗号句号的是一句话，不是图名
        return True
    return bool(TITLE_BLOCK_RE.search(t))


# 图面证据点：只用来判断"图名这一带是不是真的图面"，不进构件分类、不改算量口径。
# 基础图/板带图没有柱梁板墙编号（只有 JCL/CT 基础编号、截面、配筋），
# 只认编号会让 members≈0，整张图一个真图名都认不出来、楼层切分直接失效。
EVID_BASE_RE = re.compile(r"^(CT|JC|DJ|ZJ|ZH|JCL|JZL|AL|TB|PT)\d+[a-zA-Z]?")
# DWG 里直径符号常写成转义 %%13 或 %%c（"%%1328@200" 就是 Φ28@200），只认 Φ 会漏掉整本文字
EVID_REBAR_RE = re.compile(r"(?:%%1[0-9]{2}|%%[cC]|[Φφ]|C)\s*\d{1,2}\s*@\s*\d{2,4}"
                           r"|\d+\s*(?:%%1[0-9]{2}|%%[cC]|[Φφ]|C)\s*\d{1,2}")


def is_evidence(txt):
    """该文字能否作为"这里是图面"的证据：构件编号 / 基础编号 / 截面尺寸 / 配筋。"""
    t = (txt or "").strip()
    if not t:
        return False
    head = t.split("/")[0]
    if any(p.match(head) for p in MEMBER_PATTERNS.values()):
        return True
    if EVID_BASE_RE.match(head):
        return True
    return bool(SIZE_RE.search(t) or EVID_REBAR_RE.search(t))
ELEV_ROW = re.compile(r"[+±]?\d{1,3}\.\d{2,3}")


def log(msg):
    print(msg, file=sys.stderr)


# --------------------------------------------------------------- 底座与索引
def cad_base() -> Path:
    if os.environ.get("CAD_SKILL_DIR"):
        return Path(os.environ["CAD_SKILL_DIR"])
    here = Path(__file__).resolve().parent.parent
    for d in (here.parent / "cad-file-reader",
              *sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader")),
              Path.home() / ".claude/skills/cad-file-reader",
              Path.home() / ".codex/skills/cad-file-reader"):
        if d.is_dir():
            return d
    raise SystemExit("找不到底座技能 cad-file-reader：设 CAD_SKILL_DIR 指向它")


def base_script(name: str) -> Path:
    """定位 cad-file-reader 入口；缺失时给出可执行的处理建议。"""
    p = cad_base() / "scripts" / name
    if not p.exists():
        raise SystemExit(f"底座 cad-file-reader 缺少 {name}；请升级到 0.25.0+ 或设 CAD_SKILL_DIR")
    return p


def file_key(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def cache_dir(path: Path, override=None) -> Path:
    key = path.name + "-" + file_key(path)
    if override:
        return Path(override) / key
    local = path.parent / ".cadidx" / key
    try:
        local.mkdir(parents=True, exist_ok=True)
        return local
    except Exception:
        import tempfile
        base = Path(os.environ.get("QTY_CACHE_DIR") or (Path(tempfile.gettempdir()) / "tujian-suanliang-cache"))
        log(f"[缓存] 图纸目录不可写，改用 {base}")
        return base / key


def cache_mb(out: Path) -> float:
    return round(sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1048576, 1)


def cad_reader_version() -> str:
    """读取 cad-file-reader 版本，用于报告底座兼容性。"""
    try:
        data = json.loads((cad_base() / "manifest.json").read_text(encoding="utf-8"))
        return str(data.get("version") or "")
    except Exception:
        return ""


def run_measurement_candidates(out: Path) -> bool:
    """调用 cad-file-reader 0.25+ 的测量候选层；只作复核证据，不参与本技能算量。"""
    detail = out / "detail.json"
    if not detail.exists():
        return False
    measure_out = out / "measurement-candidates"
    target = measure_out / "cad-measurement-candidates.json"
    if target.exists():
        validate_measurement_candidates(out)
        return True
    try:
        script = base_script("cad_measure.sh")
    except SystemExit as exc:
        log(f"[测量] 底座缺少测量候选入口（不阻断出量）：{exc}")
        return False
    r = subprocess.run(
        ["bash", str(script), str(detail), "--out-dir", str(measure_out)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        log("[测量] 底座测量候选失败（不阻断出量）：" + (r.stderr.strip().splitlines()[-1][:180] if r.stderr.strip() else f"exit={r.returncode}"))
        return False
    log("[测量] 已生成 cad-file-reader 长度/面积/体积测量候选，仅供复核")
    validate_measurement_candidates(out)
    return True


def validate_measurement_candidates(out: Path) -> bool:
    """用 cad-file-reader cad_validate.sh 校验测量候选；失败不阻断出量，但写入校验状态。"""
    target = out / "measurement-candidates" / "cad-measurement-candidates.json"
    if not target.exists():
        return False
    try:
        script = base_script("cad_validate.sh")
    except SystemExit as exc:
        log(f"[测量校验] 底座缺少校验入口（不阻断出量）：{exc}")
        return False
    r = subprocess.run(["bash", str(script), str(target)], capture_output=True, text=True)
    errors = []
    for ln in r.stdout.splitlines():
        if not ln.strip():
            continue
        try:
            rec = json.loads(ln)
            errors.extend(rec.get("errors") or [])
        except Exception:
            continue
    ok = r.returncode == 0 and not errors
    (out / "measurement-candidates" / "cad-validate.json").write_text(
        json.dumps({"ok": ok, "errors": errors[:20], "exit": r.returncode},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    if not ok:
        log("[测量校验] cad-file-reader 测量候选校验未通过（不阻断出量）：" + "；".join(errors[:3]))
    return ok


def run_compare_baseline(out: Path, baseline: str) -> bool:
    """用 cad-file-reader cad_compare.sh 对比基线/当前图纸变化候选；不阻断出量，只提示重算范围。"""
    detail = out / "detail.json"
    if not detail.exists() or not baseline:
        return False
    try:
        script = base_script("cad_compare.sh")
    except SystemExit as exc:
        log(f"[图纸对比] 底座缺少对比入口（不阻断出量）：{exc}")
        return False
    dst = out / "cad-compare"
    dst.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["bash", str(script), baseline, str(detail), "--out-dir", str(dst), "--tolerance", "1.0", "--max-changes", "5000"],
        capture_output=True, text=True,
    )
    ok = r.returncode == 0
    if not ok:
        log("[图纸对比] cad_compare 失败（不阻断出量）：" + (r.stderr.strip().splitlines()[-1][:180] if r.stderr.strip() else "exit=%s" % r.returncode))
    else:
        log("[图纸对比] 已生成基线→当前图纸变化候选：%s（建议按变化清单决定重算范围）" % dst)
    return ok


def run_normative(out: Path) -> bool:
    """调用 cad-file-reader 0.5+ 的规范/图集元数据辅助；失败不阻断出量。"""
    scan = out / "scan.json"
    detail = out / "detail.json"
    if not scan.exists():
        return False
    try:
        script = base_script("cad_normative.sh")
    except SystemExit as exc:
        log(f"[规范] 底座缺少规范辅助入口（不阻断出量）：{exc}")
        return False
    args = ["bash", str(script), "--scan", str(scan),
            "--rules", str(cad_base() / "rules"), "--format", "all", "-o", str(out / "normative")]
    if detail.exists():
        # 插在 --scan 的值之后。原写法 args[3:3] 会把 --detail 插到 "--scan" 与其值之间，
        # 使 --scan 拿到 "--detail" 当作值、真正的 scan 路径被挤到后面，参数错位。
        args[4:4] = ["--detail", str(detail)]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        err = r.stderr.strip().splitlines()
        log("[规范] 底座规范辅助失败（不阻断出量）：" + (err[-1][:180] if err else f"exit={r.returncode}"))
        return False
    log("[规范] 已生成 cad-file-reader 规范/图集辅助缓存")
    return True


def build_index(dwg: Path, out: Path, with_geom: bool, keep_detail: bool = False,
                with_normative: bool = True, compare_baseline: str = "") -> Path:
    db = out / "index.sqlite"
    norm_file = out / "normative.json"
    if db.exists():
        try:
            row = sqlite3.connect(db).execute("SELECT v FROM meta WHERE k='built'").fetchone()
            built = json.loads(row[0]) if row else {}
        except Exception:
            built = {}
        if built.get("version") == CACHE_VERSION and (built.get("geom") or not with_geom):
            if with_normative and not norm_file.exists() and (out / "detail.json").exists():
                built["normative"] = run_normative(out)
            if (out / "detail.json").exists() and not (out / "measurement-candidates" / "cad-measurement-candidates.json").exists():
                built["measurement_candidates"] = run_measurement_candidates(out)
            elif (out / "measurement-candidates" / "cad-measurement-candidates.json").exists():
                validate_measurement_candidates(out)
            return db
        log("[索引] 缓存不可用（缺几何线段或版本变了），重建…")
        db.unlink(missing_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    if not (out / "detail.json").exists():
        raise SystemExit(
            "[tujian] 缓存缺 detail.json：本技能已不自行解图。请先让 cad-file-reader "
            "产出 cad-contract/v1 契约（含 text_records/geometry_segments），再把契约 JSON 交给本入口。")
    has_norm = False
    if with_normative and not norm_file.exists():
        has_norm = run_normative(out)
    has_measure = run_measurement_candidates(out)
    if compare_baseline:
        run_compare_baseline(out, compare_baseline)
    db = fill_db(out, db, with_geom, has_norm, has_measure)
    if not keep_detail:                       # 明细 JSON 是解图中间产物，索引建好就没用了
        det = out / "detail.json"
        if det.exists():
            freed = round(det.stat().st_size / 1048576, 1)
            det.unlink()
            log(f"[缓存] 回收明细 JSON 省 {freed}MB（要重算明细再加 --keep-detail；缓存共 {cache_mb(out)}MB）")
    return db


def fill_db(out: Path, db: Path, with_geom: bool, has_norm: bool = False, has_measure: bool = False) -> Path:
    t0 = time.time()
    detail = json.loads((out / "detail.json").read_text(encoding="utf-8"))
    con = sqlite3.connect(db)
    con.executescript("""
      CREATE VIRTUAL TABLE t USING rtree(id, x1, x2, y1, y2);
      CREATE TABLE text(id INTEGER PRIMARY KEY, text TEXT, layer TEXT, kind TEXT, sheet INTEGER, x REAL, y REAL);
      CREATE VIRTUAL TABLE s USING rtree(id, x1, x2, y1, y2);
      CREATE TABLE seg(id INTEGER PRIMARY KEY, xa REAL, ya REAL, xb REAL, yb REAL, layer TEXT);
      CREATE TABLE sheet(id INTEGER PRIMARY KEY, bbox TEXT, texts INTEGER);
      CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
    """)
    rows, ids = [], []
    for i, rec in enumerate(detail.get("text_records") or []):
        x, y = rec.get("x"), rec.get("y")
        if x is None or y is None:
            continue
        rows.append((i, rec.get("text") or "", rec.get("layer") or "", rec.get("kind") or "", rec.get("sheet"), x, y))
        ids.append((i, x, x, y, y))
    con.executemany("INSERT INTO t VALUES(?,?,?,?,?)", ids)
    con.executemany("INSERT INTO text VALUES(?,?,?,?,?,?,?)", rows)
    segs = (detail.get("geometry_segments") or [[]])[0]
    slayers = (detail.get("geometry_layers") or [[]])[0]
    sids = []
    for i, sg in enumerate(segs):
        try:
            x1, y1, x2, y2 = float(sg[0]), float(sg[1]), float(sg[2]), float(sg[3])
        except Exception:
            continue
        lay = str(slayers[i]) if isinstance(slayers, list) and i < len(slayers) else ""
        sids.append((i, min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)))
        con.execute("INSERT OR REPLACE INTO seg VALUES(?,?,?,?,?,?)", (i, x1, y1, x2, y2, lay))
    con.executemany("INSERT INTO s VALUES(?,?,?,?,?)", sids)
    for sh in (detail.get("meta") or {}).get("sheets") or []:
        con.execute("INSERT OR REPLACE INTO sheet VALUES(?,?,?)", (sh.get("id"), json.dumps(sh.get("bbox")), sh.get("texts")))
    con.execute("INSERT OR REPLACE INTO meta VALUES('detail',?)",
                (json.dumps({k: detail.get(k) for k in ("members", "spec", "spec_src", "concrete", "slab_thk", "rebar_summary", "axis", "files", "notes")}),))
    con.execute("INSERT OR REPLACE INTO meta VALUES('built',?)",
                (json.dumps({"secs": round(time.time() - t0, 1), "version": CACHE_VERSION,
                             "geom": bool(with_geom and sids), "texts": len(rows), "segs": len(sids),
                             "normative": has_norm, "measurement_candidates": has_measure,
                             "cad_reader_version": cad_reader_version(),
                             "measurement_validated": bool(
                                 (out / "measurement-candidates" / "cad-validate.json").exists()
                                 and json.loads((out / "measurement-candidates" / "cad-validate.json").read_text(encoding="utf-8")).get("ok"))
                             }),))
    con.commit()
    built = json.loads(con.execute("SELECT v FROM meta WHERE k='built'").fetchone()[0])
    con.close()
    log(f"[索引] 完成：{built['texts']} 条文字 / {built['segs']} 条线段，解图 {built['secs']}s（之后查询不再解图）")
    return db


def load_profile(out: Path) -> dict:
    f = out / "profile.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def save_profile(out: Path, data: dict) -> None:
    (out / "profile.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def load(db: Path):
    con = sqlite3.connect(db)
    meta = json.loads(con.execute("SELECT v FROM meta WHERE k='detail'").fetchone()[0])
    built = json.loads(con.execute("SELECT v FROM meta WHERE k='built'").fetchone()[0])
    rows = con.execute("SELECT id,text,layer,kind,sheet,x,y FROM text").fetchall()
    segs = con.execute("SELECT xa,ya,xb,yb,layer FROM seg").fetchall()
    sheets = {r[0]: json.loads(r[1]) for r in con.execute("SELECT id,bbox FROM sheet").fetchall() if r[1]}
    con.close()
    return meta, built, rows, segs, sheets


# --------------------------------------------------------------- 楼层切分
def find_titles(rows, min_refs=10, radius=None, pattern=None):
    """真图名判据：图名附近确有构件标注。不依赖图层命名，换设计院可用。"""
    rx = re.compile(pattern) if pattern else None
    cand = []
    for _i, txt, _layer, _kind, sheet, x, y in rows:
        t = txt.strip()
        if 5 <= len(t) <= 40 and TITLE_RE.search(t) and not is_title_noise(t) and (not rx or rx.search(t)):
            cand.append((t, x, y, sheet))
    members = [(x, y) for _i, txt, _l, _k, _s, x, y in rows if is_evidence(txt)]
    if not cand or not members:
        return [], {"cand": len(cand), "members": len(members), "real": 0, "noise": 0}
    step = 20000.0
    grid = {}
    for x, y in members:
        grid.setdefault((int(x // step), int(y // step)), []).append((x, y))

    def near(x, y, r):
        return sum(1 for cx in range(int((x - r) // step), int((x + r) // step) + 1)
                   for cy in range(int((y - r) // step), int((y + r) // step) + 1)
                   for mx, my in grid.get((cx, cy), ()) if abs(mx - x) <= r and abs(my - y) <= r)

    # 邻域半径按图名各自定：从 30m 起一档档放大，取第一个凑够 min_refs 条证据的档。
    # 不能用"到最近一条证据的距离"定尺度——图名旁边偶然飘来一条尺寸标注就会把半径压到 30m，
    # 真正的图面证据全在更远处，于是主图名反而认不出来（C 区框架梁图就是这样丢的）。
    # 上限 160m：放到最大还凑不够 min_refs，说明这条文字只是说明/图签里带"图"字，不是图名。
    ladder = (float(radius),) if radius else TITLE_R_LADDER
    best = {}
    for t, x, y, sh in cand:
        n, r = 0, ladder[0]
        for rr in ladder:
            n = near(x, y, rr)
            r = rr
            if n >= min_refs:
                break
        if n >= min_refs and (t not in best or best[t]["refs"] < n):
            best[t] = {"title": t, "x": x, "y": y, "refs": n, "sheet": sh, "r": round(r)}
    return list(best.values()), {"radius": round(ladder[0]), "cand": len(cand), "real": len(best), "members": len(members)}


def frame_box(hits, sheets, rows=None, fallback_radius=60000.0):
    """该层范围 = 命中真图名所在图框的并集；图框查不到时以图名坐标为圆心取方框。"""
    box = None
    for h in hits or []:
        b = (sheets or {}).get(h.get("sheet"))
        if not b:
            b = next((sh for sh in (sheets or {}).values()
                      if sh[0] - 1000 <= h["x"] <= sh[2] + 1000 and sh[1] - 1000 <= h["y"] <= sh[3] + 1000), None)
        if not b:
            b = (h["x"] - fallback_radius, h["y"] - fallback_radius, h["x"] + fallback_radius, h["y"] + fallback_radius)
        box = (min(box[0], b[0]) if box else b[0], min(box[1], b[1]) if box else b[1],
               max(box[2], b[2]) if box else b[2], max(box[3], b[3]) if box else b[3])
    if box and frame_too_broad(box, sheets, rows):
        return None
    return box


def frame_too_broad(box, sheets, rows=None):
    """这个"图框"是不是坐标聚类粘成的一大片（不是真图幅）。

    不能只看绝对尺寸：车库顶板梁图整张就一幅 260 m×250 m 的大平面图，
    一刀切 200 m 会把真图幅判掉、退回"图名 ±20 m"的小窗口，全层标注取不到。
    判据：
      - 图上只有一个图框：就是它；
      - 该框装下全图 ≥60% 文字：这张图本来就这一幅，尺寸大是真的；
      - 否则比同图其它图框的中位跨度大 4 倍以上（或超 200 m）才当作聚类失败。
    """
    if box is None:
        return True
    spans = [max(b[2] - b[0], b[3] - b[1]) for b in (sheets or {}).values() if b and len(b) == 4]
    if len(spans) < 2:
        return False
    if rows:
        inside = sum(1 for r in rows if in_box(box, r[5], r[6], 0.0))
        if inside >= 0.6 * len(rows):
            return False
    spans.sort()
    med = spans[(len(spans) - 1) // 2]      # 取下位中位数：图框少的时候不被那个大框自己拉高
    return max(box[2] - box[0], box[3] - box[1]) > max(med * 4.0, 200000.0)


def window_box(hits, titles, lo=20000.0, hi=60000.0, k=0.6, radius=None):
    """以图名为中心的取数窗口：半径＝图名到最近同名外图名距离的中位数×0.6，夹在 20~60 m。
    图纸没有图框块（很多图都这样）时，这是唯一可靠的范围；人工给了 radius 就按人工的来。"""
    if radius:
        r = float(radius)
    else:
        ds = []
        for h in hits or []:
            d = min((abs(h["x"] - o["x"]) + abs(h["y"] - o["y"]) for o in titles if o is not h), default=None)
            if d:
                ds.append(d)
        if not ds:                       # 只有一个图名时没有"相邻图名"可参照，取上限半径
            r = hi
        else:
            ds.sort()
            r = min(max(ds[len(ds) // 2] * k, lo), hi)
    x0 = min(h["x"] for h in hits) - r; x1 = max(h["x"] for h in hits) + r
    y0 = min(h["y"] for h in hits) - r; y1 = max(h["y"] for h in hits) + r
    return (x0, y0, x1, y1)


def scope(rows, titles, label, sheets, regex=False, radius=None):
    """该层范围：优先图框；图框也没有时按"最近真图名归属"，只收属于命中图名的记录。

    radius：人工指定取数半径（mm）。图名与图面分处两处、图框又识别不出主图幅时
    （C 区墙柱图图名落在 40 m 小图框里，图面在别的图幅），用人工半径兜底。
    """
    hits = [t for t in titles if (re.search(label, t["title"]) if regex else label in t["title"])]
    if not hits:
        return None, [], [], None
    box = None
    if radius:
        box = window_box(hits, titles, radius=float(radius))
    if box is None:
        box = frame_box(hits, sheets, rows)
    if not box:
        box = window_box(hits, titles)
    if box:
        kept = [r for r in rows if in_box(box, r[5], r[6], 0.0)]
    else:
        kept = [r for r in rows if nearest_title(r, titles) in hits]
    ks = {id(r) for r in kept}
    return hits, kept, [r for r in rows if id(r) not in ks], box


CODE_RE = re.compile(r"([A-Z]{1,4}\d{1,4}[a-zA-Z]?)(?=$|[\s/(（）,，、:：*＋+～~-])")   # 分隔符里不含 x/×，否则"XL4600x800"会把编号读成 XL4600


def member_key(txt):
    """构件号单独切出来：只并字母之间的空格（K Z1→KZ1），数字与后面的截面之间必须断开。

    否则 "XL4 600x800" 去掉空格变成 XL4600x800，构件号会被读成 XL4600。
    """
    t = re.sub(r"(?<=[A-Za-z])\s+(?=[A-Za-z])", "", (txt or "").strip())
    m = CODE_RE.match(t)
    if m:
        return m.group(1)
    # 编号与尺寸之间没留空格时（"LB1h=130"、"XL4600x800"）：把"编号数字"和"尺寸数字"切开
    m = re.match(r"([A-Z]{1,4})(\d{1,3})(\d{3,4})[x×X](\d{2,4})", t)
    if m:
        return m.group(1) + m.group(2)
    m = re.match(r"([A-Z]{1,4})(\d{1,3})h\s*=", t, re.I)
    return m.group(1) + m.group(2) if m else None


def nearest_title(rec, titles):
    _i, _t, _l, _k, _s, x, y = rec
    best, bd = None, None
    for h in titles:
        d = (h["x"] - x) ** 2 + (h["y"] - y) ** 2
        if bd is None or d < bd:
            best, bd = h, d
    return best


def in_box(box, x, y, pad=0.0):
    return box and box[0] - pad <= x <= box[2] + pad and box[1] - pad <= y <= box[3] + pad


# --------------------------------------------------------------- 构件与量
def parse_members(rows, dedupe_mm=1500.0):
    out = {c: {} for c in MEMBER_PATTERNS}
    for _i, txt, layer, _kind, _sheet, x, y in rows:
        raw = txt or ""                            # 尺寸/标号必须在带空格的原文上找
        key = member_key(raw.split("/")[0])
        if not key:
            continue
        for cat, pat in MEMBER_PATTERNS.items():
            if cat == "墙" and STEEL_GRADE_RE.match(key):
                continue
            if cat == "板" and CONCRETE_GRADE_RE.match(key):
                continue
            if not pat.match(key):
                continue
            e = out[cat].setdefault(key, {"code": key, "positions": [], "b": None, "h": None, "thk": None,
                                          "spans": None, "cant": "", "grades": [], "layers": set(), "raws": [],
                                          "sec_votes": collections.Counter(), "thk_votes": collections.Counter()})
            e["positions"].append((x, y))
            e["layers"].add(layer)
            if len(e["raws"]) < 3:
                e["raws"].append(txt.strip())
            sm = SIZE_RE.search(raw)
            if sm:
                e["b"], e["h"] = int(sm.group(1)), int(sm.group(2))
                e["sec_votes"][(int(sm.group(1)), int(sm.group(2)))] += 1
            hm = THK_RE.search(raw)
            if hm:
                e["thk"] = int(hm.group(1))
                e["thk_votes"][int(hm.group(1))] += 1
            sp = SPAN_RE.search(raw)
            if sp and sp.group(1):
                e["spans"] = int(sp.group(1))
                e["cant"] = {"A": "一端悬挑", "B": "两端悬挑"}.get(sp.group(2), "")
            gm = re.search(r"C(\d{2})", raw)
            if gm:
                e["grades"].append("C" + gm.group(1))
    for d in out.values():
        for e in d.values():
            if len(e["sec_votes"]) > 1:                       # 同一编号在图上有多种截面标注 → 取多数并记冲突
                (e["b"], e["h"]), n = e["sec_votes"].most_common(1)[0]
                e["conflict"] = "截面 " + "、".join(f"{a}x{b}×{c}" for (a, b), c in e["sec_votes"].most_common())
            elif e["sec_votes"]:
                (e["b"], e["h"]) = next(iter(e["sec_votes"]))
            if len(e["thk_votes"]) > 1:
                e["thk"], n = e["thk_votes"].most_common(1)[0]
                e["conflict"] = (e.get("conflict", "") + " 厚 " + "、".join(f"{a}×{c}" for a, c in e["thk_votes"].most_common())).strip()
            elif e["thk_votes"]:
                e["thk"] = next(iter(e["thk_votes"]))
            uniq = []
            for x, y in e["positions"]:
                if not any(abs(x - ux) <= dedupe_mm and abs(y - uy) <= dedupe_mm for ux, uy in uniq):
                    uniq.append((x, y))
            e["count"] = max(len(uniq), 1)
            e["layers"] = sorted(e["layers"])
    pos = [(_i, txt, x, y) for _i, txt, _l, _k, _s, x, y in rows
           if (SIZE_RE.search(txt) or THK_RE.search(txt)) and len(txt.strip()) <= 14]
    return out, pos


def bind_sizes(members, pos, radius=3000.0):
    """把 b×h / h=130 这类数字按坐标就近绑到构件编号上（图面常是两条文字）。"""
    pos = sorted(((x, y, txt.strip()) for _i, txt, x, y in pos), key=lambda r: r[0])
    xs = [r[0] for r in pos]
    for cat, d in members.items():
        for e in d.values():
            x, y = e["positions"][0]
            for j in range(bisect.bisect_left(xs, x - radius), len(pos)):
                if pos[j][0] > x + radius:
                    break
                _x, _y, txt = pos[j]
                if abs(_y - y) > radius:
                    continue
                sm, hm = SIZE_RE.search(txt), THK_RE.search(txt)
                if sm and cat in ("梁", "柱", "墙") and not e["b"]:
                    e["b"], e["h"] = int(sm.group(1)), int(sm.group(2))
                elif hm and cat == "板" and not e["thk"]:
                    e["thk"] = int(hm.group(1))
                elif cat == "墙" and not e["thk"]:
                    wm = re.search(r"(?<![\d.x×])(2\d{2}|3\d{2}|4\d{2})(?![\d.])", txt)
                    if wm and "h=" not in txt and "x" not in txt.lower():
                        e["thk"] = int(wm.group(1))


# --------------------------------------------------------------- 表格绑定（柱表/墙身表）
HDR_COLS = {"墙厚": "thk", "墙身厚度": "thk", "厚度": "thk", "截面尺寸": "sec", "截面": "sec",
            "柱截面": "sec", "标高": "elev", "剪力墙水平钢筋": "rebar", "水平分布筋": "rebar",
            "垂直分布筋": "rebar2", "约束边缘构件": "ec", "边缘构件纵向钢筋": "rebar3", "纵筋": "rebar3"}
ROW_TOL = 250.0


def norm_hdr(t):
    return re.sub(r"[\s*＊:：()（）]", "", t or "")


def row_buckets(rows):
    b = {}
    for i, txt, layer, _k, _s, x, y in rows:
        t = (txt or "").strip()
        if t:
            b.setdefault((layer, round(y / ROW_TOL)), []).append((x, t, i))
    for v in b.values():
        v.sort()
    return b


def member_code(t):
    code = member_key(re.split(r"[/（(]", t or "")[0])
    if not code:
        return None, None
    for cat, pat in MEMBER_PATTERNS.items():
        if cat == "墙" and STEEL_GRADE_RE.match(code):
            continue
        if cat == "板" and CONCRETE_GRADE_RE.match(code):
            continue
        if pat.match(code):
            return cat, code
    return None, None


def label_range(label):
    m = re.search(r"(-?\d{1,3}\.\d{1,3})\s*[~～]\s*(-?\d{1,3}\.\d{1,3})", label or "")
    return None if not m else f"{float(m.group(1)):.3f}~{float(m.group(2)):.3f}"


def same_range(a, b):
    def nums(v):
        return [round(float(x), 2) for x in re.findall(r"-?\d+\.?\d*", v or "")]
    na, nb = nums(a), nums(b)
    return len(na) >= 2 and len(nb) >= 2 and abs(na[0] - nb[0]) < 0.02 and abs(na[1] - nb[1]) < 0.02


def schedule_bind(members, rows, rng=None):
    """柱截面/墙厚常在表里而不是构件旁边：①柱表竖排（同列往下找 400X400）②墙身表有表头（按列名取墙厚）。
    表里带标高段的行，只有与本层图名区间一致才用；对不上就不绑，进缺项，不拿别层的截面凑。"""
    bound, tbl_ids, notes = 0, set(), []
    idx = {}
    for cat, d in members.items():
        for key, e in d.items():
            idx.setdefault(key, (cat, e))
    buckets = row_buckets(rows)
    # ② 有表头的表
    for (layer, band), items in buckets.items():
        names = {norm_hdr(t): x for x, t, _i in items}
        if names.get("编号") is None:
            continue
        cols = {HDR_COLS[n]: names[n] for n in HDR_COLS if n in names}
        if not cols:
            continue
        cols["code"] = names["编号"]
        span = max(cols.values()) - min(cols.values())
        for b2 in range(band - 60, band + 61):
            if b2 == band:
                continue
            row = buckets.get((layer, b2))
            if not row:
                continue
            y = b2 * ROW_TOL
            cells = {}
            for x, t, i in row:
                if abs(x - cols["code"]) > span:
                    continue
                near = min(cols.items(), key=lambda kv: abs(kv[1] - x))
                if abs(near[1] - x) <= 6000:
                    cells.setdefault(near[0], (t, i))
            cat, key = member_code(cells.get("code", ("",))[0]) if "code" in cells else (None, None)
            if not key or key not in idx:
                continue
            elev = cells.get("elev", ("",))[0]
            if rng and elev and not same_range(rng, elev):
                notes.append(f"{key} 表内标高段 {elev} 与本层 {rng} 不符，未取")
                continue
            _cat, e = idx[key]
            got = []
            if cells.get("sec") and not e["b"]:
                m = SIZE_RE.search(cells["sec"][0])
                if m:
                    e["b"], e["h"] = int(m.group(1)), int(m.group(2))
                    got.append(f"截面{e['b']}x{e['h']}")
            if cells.get("thk") and not e["thk"]:
                m = re.search(r"(?<!\d)(1\d{2}|2\d{2}|3\d{2}|4\d{2}|5\d{2}|6\d{2})(?!\d)", cells["thk"][0])
                if m:
                    e["thk"] = int(m.group(1))
                    got.append(f"墙厚{e['thk']}")
            if got:
                e["src"] = "表行绑定（表头列名对上）"
                if len(e["raws"]) < 4:
                    e["raws"].append("｜".join(f"{t}" for _t, _i in cells.values()))
                tbl_ids.update(i for _t, i in cells.values())
                bound += 1
    # ① 竖排柱表：编号正下方同列 1~4 行内找 b×h / 墙厚
    byx = {}
    for i, txt, layer, _k, _s, x, y in rows:
        t = (txt or "").strip()
        if t:
            byx.setdefault((layer, round(x / 150)), []).append((y, t, i))
    for v in byx.values():
        v.sort(reverse=True)
    for cat, d in members.items():
        for key, e in d.items():
            if e["b"] or e["thk"]:
                continue
            for (x, y) in e["positions"][:3]:
                col = byx.get((e["layers"][0] if e["layers"] else "", round(x / 150)), [])
                ys = [yy for yy, _t, _i in col if abs(yy - y) < 0.5]
                if not ys:
                    continue
                below = [(yy, t, i) for yy, t, i in col if yy <= ys[0] + 1 and yy > ys[0] - 1600]
                for yy, t, i in below[1:5]:
                    m = SIZE_RE.search(t)
                    if m and cat in ("柱", "梁", "墙"):
                        e["b"], e["h"] = int(m.group(1)), int(m.group(2))
                        e["src"] = "柱表竖排绑定（同列下方一行）"
                        tbl_ids.add(i)
                        bound += 1
                        break
                    thk = re.search(r"(?<!\d)(1\d{2}|2\d{2}|3\d{2})(?!\d)", t)
                    if thk and cat == "墙" and len(t) <= 4:
                        e["thk"] = int(thk.group(1))
                        e["src"] = "墙身表竖排绑定（同列下方一行）"
                        tbl_ids.add(i)
                        bound += 1
                        break
                if e["b"] or e["thk"]:
                    break
    return bound, tbl_ids, notes

def parse_member_size(spec):
    """人工给一次的构件尺寸：`KZ1=500x900,Q2=250`（柱/梁给截面，墙给厚）。
    图上取不到截面时用，读一次本图之后所有层沿用；来源会写进每行"依据"，不冒充图面直读。"""
    out = {}
    for part in re.split(r"[,，;；\s]+", spec or ""):
        m = re.fullmatch(r"([A-Z]{1,4}\d{1,4}[a-zA-Z]?)\s*=\s*(\d{2,4})(?:\s*[x×X]\s*(\d{2,4}))?", part.strip())
        if not m:
            continue
        code, a, b = m.group(1).upper(), int(m.group(2)), m.group(3)
        out[code] = (a, int(b)) if b else int(a)
    return out


def apply_member_size(members, mapping, src):
    n = 0
    for cat, d in members.items():
        for key, e in d.items():
            v = mapping.get(key.upper())
            if v is None:
                continue
            if cat == "墙" and not e["thk"] and isinstance(v, int):
                e["thk"], e["src"], n = v, src + "→墙厚", n + 1
            elif cat in ("柱", "梁") and not e["b"] and isinstance(v, tuple):
                e["b"], e["h"], e["src"], n = v[0], v[1], src + "→截面", n + 1
    return n



# --------------------------------------------------------------- 默认值 / 轴网 / 层高


def default_thk(spec):
    """图面说明里的板厚主档，仅在找不到就近板厚时兜底，并标"推定"。"""
    ths = (spec or {}).get("板厚") or {}
    if not ths:
        return None
    top = max(ths.items(), key=lambda kv: kv[1])
    try:
        return int(re.sub(r"\D", "", top[0])), top[1], len(ths)
    except ValueError:
        return None


def axis_grid(segs, box=None, min_len_mm=3000.0, cluster_mm=400.0, cover=0.5):
    """从图面线段复原正交轴网：把线段裁到本层范围内，按坐标聚成轴线，相邻轴线间距当跨距。
    长度门槛用"本层范围尺寸"而不是散点包络，避免被跨图框的长线干扰；不认图层名。"""
    if not segs:
        return None, {"原因": "索引时未加 --with-geom，线段没入库"}
    if box:
        bx0, by0, bx1, by1 = box
        segs = [s for s in segs if in_box(box, (s[0] + s[2]) / 2, (s[1] + s[3]) / 2, 500)]
    if len(segs) < 6:
        return None, {"原因": "该层范围内线段太少", "线段": len(segs)}
    W = (bx1 - bx0) if box else (max(c for s in segs for c in (s[0], s[2])) - min(c for s in segs for c in (s[0], s[2])))
    H = (by1 - by0) if box else (max(c for s in segs for c in (s[1], s[3])) - min(c for s in segs for c in (s[1], s[3])))
    v, h = {}, {}

    def near_bucket(store, coord, tol):
        """按坐标就近聚轴，不用固定格网取整；7500mm 不会被吸到 7600mm。"""
        for k in store:
            if abs(k - coord) <= tol:
                return k
        return coord

    for x1, y1, x2, y2, _layer in segs:
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        if dx <= cluster_mm and dy >= min_len_mm:
            a, b = min(y1, y2), max(y1, y2)
            if box:
                a, b = max(a, by0), min(b, by1)
            if b - a >= min_len_mm:
                key = near_bucket(v, (x1 + x2) / 2, cluster_mm)
                v.setdefault(key, []).append((a, b))
        elif dy <= cluster_mm and dx >= min_len_mm:
            a, b = min(x1, x2), max(x1, x2)
            if box:
                a, b = max(a, bx0), min(b, bx1)
            if b - a >= min_len_mm:
                key = near_bucket(h, (y1 + y2) / 2, cluster_mm)
                h.setdefault(key, []).append((a, b))

    def longest(ivs):
        ivs.sort()
        cur, best = list(ivs[0]), ivs[0][1] - ivs[0][0]
        for a, b in ivs[1:]:
            if a <= cur[1] + cluster_mm * 3:
                cur[1] = max(cur[1], b)
            else:
                best = max(best, cur[1] - cur[0]); cur = [a, b]
        return max(best, cur[1] - cur[0])

    vx = sorted(k for k, iv in v.items() if longest(iv) >= H * cover)
    hy = sorted(k for k, iv in h.items() if longest(iv) >= W * cover)
    if len(vx) < 2 or len(hy) < 2:
        return None, {"原因": "范围内轴线太少（可能是钢结构/非标轴网）", "竖轴": len(vx), "横轴": len(hy),
                      "本层范围m": f"{W/1000:.0f}x{H/1000:.0f}"}

    def spans(coords):
        """按轴线顺序合并相邻等跨；不同跨距保留先后序列，不压成主导跨。"""
        out = []
        for a, b in zip(coords, coords[1:]):
            g = round(b - a)
            if not 800 <= g <= 30000:
                continue
            if out and abs(g - out[-1][1]) <= 50:
                out[-1][0] += 1
            else:
                out.append([1, g])
        return out

    sx, sy = spans(vx), spans(hy)
    if not sx or not sy:
        return None, {"原因": "轴间距异常", "竖轴": len(vx), "横轴": len(hy)}
    return ",".join("+".join(f"{n}x{g}" for n, g in x) for x in (sx, sy)), {
        "x向轴数": len(vx), "y向轴数": len(hy), "x向跨距mm": [g for g, _ in sx][:10],
        "y向跨距mm": [g for g, _ in sy][:10], "跨度序列x": sx, "跨度序列y": sy,
        "本层范围m": f"{W/1000:.0f}x{H/1000:.0f}"}


def parse_label_span(label):
    """图名里直接写了标高区间（"标高5.350~9.550墙柱平法施工图"）→ 这段柱的实际高度就是区间差，最可信。"""
    m = re.search(r"(-?\d{1,3}\.\d{1,3})\s*[~～]\s*(-?\d{1,3}\.\d{1,3})", label or "")
    if not m:
        return None
    a, b = float(m.group(1)), float(m.group(2))
    return round((b - a) * 1000) if b > a else None


def story_from_tables(rows, sheets, label, titles, basis="below"):
    """先看图名自己标的标高区间，再看层高表；两个都有又不一致时报警。"""
    sp = parse_label_span(label)
    # 图名是区间时，表里能对上的是"低端那一行往上注的层高"，所以交叉核对用 above
    tbl, tinfo = story_from_table(rows, sheets, label, titles, "above" if sp else basis)
    if sp and (sp < RULES["层高校验"]["合理区间mm"][0] or sp > RULES["层高校验"]["合理区间mm"][1]):
        return tbl, tinfo                      # 区间差不是层高（比如把板厚写进图名了），退回表
    if sp:
        info = dict(tinfo)
        info.update({"来源表": "图名标高区间", "算法": "图名自标区间差", "匹配标高": None})
        if tbl and abs(tbl - sp) > RULES["层高校验"]["表注与标高差容差mm"]:
            info["需核对"] = f"图名区间高 {sp}mm 与层高表算出的 {tbl}mm 不一致，取了图名区间；请核对表内分区标高"
        elif tbl:
            info["层高表核对"] = tbl
        return sp, info
    return tbl, tinfo


def story_from_table(rows, sheets, label, titles, basis="below"):
    """从"层高表/标高表/混凝土强度等级表"按图名里的标高反查层高；配不上返回 None，不拿全图数字猜。"""
    m = re.search(r"标高\s*\+?(-?\d+(?:\.\d+)?)", label or "")   # 区间图名取的是低端标高，正好和表里那一行对上
    elev = float(m.group(1)) if m else None
    cand = [x for x in titles if re.search(r"层高表|标高表|强度等级|混凝土等级", x["title"])]
    if not cand or elev is None:
        return None, {"原因": "没找到层高表，或图名里没有标高"}
    box = None
    for c in cand:
        b = (sheets or {}).get(c.get("sheet"))
        if b:
            box = (min(box[0], b[0]) if box else b[0], min(box[1], b[1]) if box else b[1],
                   max(box[2], b[2]) if box else b[2], max(box[3], b[3]) if box else b[3])
    if not box:                       # 没有图框就取"表名周围的窗口"，仍要求标高能对上
        box = window_box(cand, cand, lo=15000.0, hi=60000.0)
    if not box:
        return None, {"原因": "层高表没有范围可取"}
    lines = {}
    for _i, txt, _layer, _kind, _sheet, x, y in rows:
        s = txt.strip()
        if not in_box(box, x, y, 500):
            continue
        mm = re.fullmatch(r"([+±-]?\d{1,3})\.(\d{2,3})", s)
        if mm:
            val = float(mm.group(1).replace("+", "").replace("±", "") + "." + mm.group(2))
            lines.setdefault(round(y / 200) * 200, []).append((val, len(mm.group(2))))
    pairs = []
    for _y, items in sorted(lines.items()):
        el = sorted(v for v, d in items if d == 3)
        hh = sorted(v for v, d in items if d == 2)
        if el:
            pairs.append((el[0], hh[0] if hh else None))
    if not pairs:
        return None, {"原因": "表内没读出标高数字", "来源表": cand[0]["title"]}
    # 只按标高排序：表里常有"只标标高、没有层高列"的行，第二轮是 None，
    # 直接 sort 元组会在标高相等时比 None<None / None<float 抛 TypeError（真图已复现）。
    pairs.sort(key=lambda pair: pair[0])
    diffs = [abs(e - elev) for e, _ in pairs]
    i = min(range(len(pairs)), key=lambda k: diffs[k])
    if diffs[i] <= 0.02:                      # 取最接近的一行（表里常有 -0.050/-0.060 这种挨着的标高）
        e, hh = pairs[i]
        lo, hi = RULES["层高校验"]["合理区间mm"]
        info_warn = None
        above = round(hh * 1000) if hh else (round((pairs[i + 1][0] - e) * 1000) if i + 1 < len(pairs) else None)
        below, blayer, bnote = None, None, None
        for j in range(i - 1, -1, -1):     # 往下找第一个"像层高"的标高（跳过降板/找坡/台阶这类小数差）
            d = round((e - pairs[j][0]) * 1000)
            if lo <= d <= hi:
                below, blayer, bnote = d, pairs[j][0], pairs[j][1]
                break
        if bnote:
            if abs(round(bnote * 1000) - below) > RULES["层高校验"]["表注与标高差容差mm"]:
                info_warn = (f"下层 {blayer} 行表注层高 {round(bnote * 1000)}mm 与标高差 {below}mm 不符，"
                             f"取了标高差；表内可能混排多套分区标高，用 --story-height-mm 定死")
        info = {"来源表": cand[0]["title"], "匹配标高": e, "本层往上的层高": above,
                "本层以下柱段高": below, "表注层高": hh, "下层标高": blayer, "下层表注层高": bnote}
        if locals().get("info_warn"):
            info["需核对"] = info_warn
        if basis == "above" and above:
            return above, {**info, "算法": "表内层高列（本层往上那一段）"}
        if below:
            return below, {**info, "算法": "本层标高−下层标高＝跟着本层顶板一起浇的柱墙段高"}
        if above:
            return above, {**info, "算法": "本层已是表内最低标高，只能用往上那一段（柱段高需另核）"}
        return None, {**info, "原因": f"标高 {elev} 是表内最高一行且本层以下没有更低标高可减"}
    return None, {"原因": f"表里没有标高 {elev}（最近的是 {round(pairs[i][0], 3)}，差 {round(diffs[i] * 1000)}mm）",
                  "表内标高": [round(e, 3) for e, _ in pairs][:12], "来源表": cand[0]["title"]}


# --------------------------------------------------------------- 说明摘录 / 断行拼接 / 后浇带
GRADE_ORDER = ["C15", "C20", "C25", "C30", "C35", "C40", "C45", "C50"]
NOTE_PATTERNS = [
    ("后浇带宽mm", re.compile(r"宽(?:度)?均?为?\s*(\d{3,4})\s*(?:mm|毫米)?[。，、）)]?")),
    ("后浇带类型", re.compile(r"(沉降后浇带|温度后浇带|伸缩后浇带)")),
    ("封闭用混凝土", re.compile(r"(高一级|微膨胀|补偿收缩)")),
    ("保留时间", re.compile(r"保留时间不少于\s*([0-9两一二三四五六七八九十]+)\s*个?月")),
]
HJD_RE = re.compile(r"后浇带|加强带|施工缝")
OPEN_CODE_RE = re.compile(r"^(JD|KD|KB|LD|YJ|SJT|LT|洞口?|留洞|预留洞|预埋洞)", re.I)


def openings(rows, min_area=None):
    """可算面积的洞口标注（编号与尺寸常写在同一条文字里）→ 合计扣减面积。

    结构平面图往往只画洞不注尺寸（本批两张真图各命中 1 处 / 0 处），所以只扣算得出的，
    算不出的只报个数，要按建施扣就用 --openings-m2 给一个数。
    """
    min_area = RULES["起扣面积_m2"] if min_area is None else min_area
    tot, items, naked = 0.0, [], 0
    seen = set()
    for i, txt, layer, _k, _s, x, y in rows:
        raw = (txt or "").strip()
        t = raw.replace(" ", "")
        if not t or not OPEN_CODE_RE.match(t):
            continue
        m = SIZE_RE.search(raw)
        if not m:
            naked += 1
            continue
        a, b = int(m.group(1)), int(m.group(2))
        ar = a * b / 1e6
        key = (round(x), round(y), a, b)
        if key in seen:
            continue
        seen.add(key)
        if ar >= min_area:
            tot += ar
            items.append(f"{t}={round(ar, 2)}㎡")
    return round(tot, 2), items[:12], naked


def join_lines(rows, row_tol_mm=400.0, max_step_mm=2000.0, char_w_mm=350.0):
    """同图层、同一行、左右紧接的文字片段拼回整句（说明被拆段、中间夹符号时关键词才搜得到）。

    字宽按 char_w_mm 估（注记字号常见 300~500），只看"上一片估到的右边界"到"下一片插入点"的间隙，
    间隙超 max_step_mm 就不拼——宁可少拼，不把两个不相干标注粘成一句。
    """
    groups = {}
    for i, txt, layer, kind, sheet, x, y in rows:
        s = (txt or "").strip()
        if len(s) < 2:
            continue
        groups.setdefault((layer, round(y / row_tol_mm)), []).append((x, s))
    out = []
    for (layer, _band), items in groups.items():
        items.sort()
        cur, end = items[0][1], items[0][0] + len(items[0][1]) * char_w_mm
        for x, s in items[1:]:
            if x - end <= max_step_mm and len(cur) + len(s) <= 300:
                cur += s
            else:
                out.append((cur, layer))
                cur = s
            end = max(end, x) + len(s) * char_w_mm
        out.append((cur, layer))
    return out


def notes_facts(rows, joined, box=None):
    """从图纸文字里摘出影响报量的说明条款（只摘命中原文，不解释、不改写；本层图框内优先）。"""
    hits = [r for r in rows if r[1] and HJD_RE.search(r[1])]
    pool = [(re.sub(r"\s+", " ", r[1]).strip(), r[2]) for r in hits]
    inb = [t for t, r in zip(pool, hits) if box and in_box(box, r[5], r[6], 500)]
    frag = [(re.sub(r"\s+", " ", t).strip(), l) for t, l in joined if t and HJD_RE.search(t)]
    pool = (inb + pool + frag) if inb else (pool + frag)
    facts = {}
    types = []
    for t, _l in pool:
        for key, pat in NOTE_PATTERNS:
            if key == "后浇带类型":
                for m in pat.finditer(t):
                    if m.group(1) not in types:
                        types.append(m.group(1))
                continue
            if key in facts:
                continue
            m = pat.search(t)
            if m:
                facts[key] = {"值": m.group(1), "原文": t[:120]}
    if types and "后浇带类型" not in facts:
        facts["后浇带类型"] = {"值": "、".join(types),
                             "原文": next((t for t, _ in pool if types[0] in t), pool[0][0])[:120]}
    if pool:
        facts.setdefault("后浇带", {"值": "命中 %d 处（%s）" % (len(pool), "本层图框内" if inb else "全图，含结构说明页"),
                                "原文": pool[0][0][:120]})
    return facts


def parse_strip_width(raw):
    """带宽可能是 float 参数、也可能是说明里的中文句；统一取数，不让小数点被当非数字吃掉。"""
    if isinstance(raw, (int, float)):
        return float(raw) if raw else None
    m = re.search(r"(\d{3,4})", str(raw or ""))
    return float(m.group(1)) if m else None


def bump_grade(grade):
    """后浇带封闭按说明常用"高一级"：C35→C40；对不上档位时只写"高一级"。父级是推定的，结果仍标推定。"""
    raw = (grade or "")
    est = "推定" in raw
    g = raw.replace("（推定）", "").strip().upper()
    if g in GRADE_ORDER:
        out = GRADE_ORDER[min(GRADE_ORDER.index(g) + 1, len(GRADE_ORDER) - 1)]
    else:
        out = "高一级（需按说明核对）"
    return out + ("（推定）" if est or g not in GRADE_ORDER else "")


def strip_split(rows, length_m, width_mm, facts, w_src="图面说明原文"):
    """后浇带：按板厚档分摊出"封闭带"一笔（高一级微膨胀），先浇区同步扣掉，总量守恒。"""
    slab = [r for r in rows if r["构件类别"] == "板"]
    if not slab or not length_m or not width_mm:
        return rows, None
    areas = {}
    for r in slab:
        t = int(re.sub(r"\D", "", r["截面/尺寸"]) or 0)
        if t:
            areas[id(r)] = (r, t, r["混凝土m3"] / (t / 1000.0))
    tot_a = sum(v[2] for v in areas.values())
    if not tot_a:
        return rows, None
    strip_area = length_m * width_mm / 1000.0
    vol = 0.0
    thick = {}
    for _k, (r, t, a) in areas.items():
        share_area = strip_area * a / tot_a
        v = round(share_area * t / 1000.0, 2)
        r["混凝土m3"] = round(r["混凝土m3"] - v, 2)
        vol += v
        thick[t] = thick.get(t, 0) + v
    main = max(areas.values(), key=lambda v: v[2])[0]
    est = "推定" in (main["标号"] or "")
    grade = bump_grade(main["标号"] or "")
    src = facts.get("封闭用混凝土", {}).get("原文") or facts.get("后浇带", {}).get("原文") or "人工输入"
    rows.append(_row("板", "后浇带封闭带", "%g宽×%gm" % (width_mm, length_m), len(thick), vol,
                     grade, False, f"带长{length_m:g}m×宽{width_mm:g}mm={round(strip_area,1)}㎡ × 板厚分摊"
                                  f"（{ '、'.join(f'{t}mm:{round(v,1)}m³' for t, v in sorted(thick.items())) }）；先浇区已同额扣除",
                     "-", src))
    return rows, {"面积m2": round(strip_area, 1), "体积m3": round(vol, 2), "宽mm": width_mm, "宽来源": w_src,
                  "长m": length_m, "长来源": "人工输入（平面图量一次）", "封闭标号": grade,
                  "分摊档": len(thick), "依据": src[:80]}


# --------------------------------------------------------------- 墙长 / 分摊 / 出量


def wall_length(segs, box, layers, tol=200.0):
    """该层图框内、墙标注所在图层上的墙线总长(m)。图层为空时直接返回 0——绝不退回"全部图层"凑数。"""
    if not segs or not box or not layers:
        return 0.0
    v, h = {}, {}
    up = {l.upper() for l in layers}
    for x1, y1, x2, y2, layer in segs:
        if not in_box(box, (x1 + x2) / 2, (y1 + y2) / 2, tol):
            continue
        lu = layer.upper()
        if not (lu in up or "WALL" in lu or "墙" in layer):
            continue
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        if dx <= tol and dy > 200:
            v.setdefault(round((x1 + x2) / 2 / tol), []).append((min(y1, y2), max(y1, y2)))
        elif dy <= tol and dx > 200:
            h.setdefault(round((y1 + y2) / 2 / tol), []).append((min(x1, x2), max(x1, x2)))
    total = 0.0
    for bucket in (v, h):
        for iv in bucket.values():
            iv.sort()
            cur = list(iv[0])
            for a, b in iv[1:]:
                if a <= cur[1] + tol:
                    cur[1] = max(cur[1], b)
                else:
                    total += cur[1] - cur[0]; cur = [a, b]
            total += cur[1] - cur[0]
    return round(total / 1000.0, 1)


def grid_geom(axis_grid_str):
    """`8x8000,6x7500` / `3x8400+2x7800,6x7500` → 轴网包络。"""
    dirs = []
    for part in [x for x in (axis_grid_str or "").split(",") if x.strip()]:
        total, count, ok = 0.0, 0, True
        for seg in part.strip().split("+"):
            m = re.fullmatch(r"(\d+)\s*[xX*]\s*(\d+(?:\.\d+)?)", seg.strip())
            if not m:
                ok = False
                break
            n, g = int(m.group(1)), float(m.group(2))
            total += n * g; count += n
        if ok and count:
            dirs.append({"跨数": count, "跨距mm": total / count, "总长mm": total})
    if len(dirs) < 2:
        return None
    ax, ay = dirs
    Lx, Ly = ax["总长mm"] / 1000, ay["总长mm"] / 1000
    return {"Lx_m": round(Lx, 1), "Ly_m": round(Ly, 1), "ax": ax, "ay": ay,
            "面积m2": round(Lx * Ly, 1), "格数": ax["跨数"] * ay["跨数"]}


def distribute(total, weights):
    s = sum(weights.values()) or 1
    return {k: round(total * v / s, 2) for k, v in weights.items()}


def _row(cat, key, size, n, vol, grade, est_grade, basis, layers, raws):
    lo, hi = RULES["构件"][cat]["含筋率区间kg_per_m3"]
    vol = round(float(vol), 2)
    grade_text = grade + ("（推定）" if est_grade else "") if grade else RULES["标号"]["未标记者默认"]
    return {"构件类别": cat, "编号/档位": key, "截面/尺寸": size, "数量": n, "混凝土m3": vol,
            "标号": grade_text,
            "钢筋估算kg带": f"{round(vol*lo)}~{round(vol*hi)}", "依据": basis, "图层": layers, "原文": raws}


def norm_check(rows):
    """常规尺寸与标注完整性校核；只提示需核对，不改写图面数据或工程量。"""
    cfg = RULES.get("规范校核") or {}
    issues = []
    for r in rows:
        msgs = []
        cat = r.get("构件类别") or "-"
        key = str(r.get("编号/档位") or "-")

        def add(msg):
            if msg not in msgs:
                msgs.append(msg)

        try:
            vol = float(r.get("混凝土m3") or 0)
            if vol <= 0:
                add("混凝土体积非正值，先核对几何参数")
        except (TypeError, ValueError):
            add("混凝土体积不是数字，先核对计算依据")
        try:
            n = float(r.get("数量") or 0)
            if n <= 0:
                add("构件数量非正值，先核对图面统计")
        except (TypeError, ValueError):
            add("构件数量不是数字，先核对图面统计")

        grade = str(r.get("标号") or "").strip()
        if not grade or "未标注" in grade or "需核对" in grade:
            add("混凝土强度等级未标注，按结构总说明/层高表核对")
        else:
            gm = re.search(r"C\s*(\d{2})", grade.upper())
            lo, hi = (cfg.get("混凝土强度等级", {}).get("常规区间") or [20, 80])
            lo = int(re.search(r"\d+", str(lo)).group())
            hi = int(re.search(r"\d+", str(hi)).group())
            if not gm:
                add("混凝土强度等级格式异常，按图纸原文核对")
            elif not lo <= int(gm.group(1)) <= hi:
                add(f"混凝土强度等级 C{gm.group(1)} 超出常规提示区间 C{lo}~C{hi}，按图纸核对")
            elif "推定" in grade:
                add("混凝土强度等级为推定来源，报量前核对")

        size = str(r.get("截面/尺寸") or "")
        m = SIZE_RE.search(size)
        if cat == "柱" and m:
            lo, hi = cfg.get("柱截面边长mm", [150, 2000])
            for label, val in (("宽", int(m.group(1))), ("高", int(m.group(2)))):
                if not lo <= val <= hi:
                    add(f"柱{label} {val}mm 超出常规提示区间 {lo}~{hi}mm，按图纸核对")
        elif cat == "梁" and m:
            lo, hi = cfg.get("梁宽mm", [100, 1200])
            if not lo <= int(m.group(1)) <= hi:
                add(f"梁宽 {m.group(1)}mm 超出常规提示区间 {lo}~{hi}mm，按图纸核对")
            lo, hi = cfg.get("梁高mm", [150, 3000])
            if not lo <= int(m.group(2)) <= hi:
                add(f"梁高 {m.group(2)}mm 超出常规提示区间 {lo}~{hi}mm，按图纸核对")
        elif cat == "板" and "后浇带" not in key:
            tm = re.search(r"(?<!\d)(\d{2,4})\s*mm", size, re.I)
            lo, hi = cfg.get("板厚mm", [50, 600])
            if tm and not lo <= int(tm.group(1)) <= hi:
                add(f"板厚 {tm.group(1)}mm 超出常规提示区间 {lo}~{hi}mm，按图纸核对")
        elif cat == "墙":
            tm = re.search(r"t\s*=\s*(\d{2,4})", size, re.I)
            lo, hi = cfg.get("墙厚mm", [80, 1000])
            if tm and not lo <= int(tm.group(1)) <= hi:
                add(f"墙厚 {tm.group(1)}mm 超出常规提示区间 {lo}~{hi}mm，按图纸核对")

        r["规范校核"] = "通过" if not msgs else "⚠️ " + "；".join(msgs)
        if msgs:
            issues.append({"构件类别": cat, "编号/档位": key, "提示": "；".join(msgs)})
    return issues


def volumes(members, story_mm, axis_grid_str, wall_len_m=0.0, default_thk=None, open_area_m2=0.0):
    """柱/墙按图面逐型直读；板/梁按轴网包络 × 档占比分摊。缺依据的进缺项清单，不猜数。"""
    rows, missing = [], []
    col, beam, slab, wall = (members["柱"], members["梁"], members["板"], members["墙"])
    for key, e in sorted(col.items()):
        if not (e["b"] and e["h"] and story_mm):
            missing.append(("柱", key, "缺柱截面（柱表未绑定）或缺层高", e["raws"][:1])); continue
        rows.append(_row("柱", key, f"{e['b']}x{e['h']}", e["count"],
                         (e["b"] / 1000) * (e["h"] / 1000) * (story_mm / 1000) * e["count"],
                         (e["grades"] or [None])[-1], not e["grades"],
                         f"截面×层高{story_mm:g}mm×{e['count']}根" + ("｜" + e.get("src","") if e.get("src") else "")
                         + ("｜⚠️" + e.get("conflict","") if e.get("conflict") else ""),
                         "、".join(e["layers"][:2]), "｜".join(e["raws"])))
    for key, e in sorted(wall.items()):
        if not e["thk"]:
            missing.append(("墙", key, "缺墙厚（附近没找到 200/250/300 一类标注）", e["raws"][:1])); continue
        if not (wall_len_m and story_mm):
            missing.append(("墙", key, "缺墙线长（索引加 --with-geom）或缺层高", e["raws"][:1])); continue
        n_all = sum(x["count"] for x in wall.values()) or 1
        ln = round(wall_len_m * e["count"] / n_all, 1)
        rows.append(_row("墙", key, f"t={e['thk']}", e["count"], ln * story_mm / 1000 * e["thk"] / 1000,
                         (e["grades"] or [None])[-1], not e["grades"],
                         f"墙线总长{wall_len_m}m 按标注数分摊 {ln}m×层高×厚"
                         + ("｜" + e.get("src","") if e.get("src") else "")
                         + ("｜⚠️" + e.get("conflict","") if e.get("conflict") else ""),
                         "、".join(e["layers"][:2]), "｜".join(e["raws"])))
    g = grid_geom(axis_grid_str)
    if not g:
        missing.append(("板", "-", '缺轴网参数：自动识别失败时给 --axis-grid "8x8000,6x7500"', []))
        missing.append(("梁", "-", '缺轴网参数：自动识别失败时给 --axis-grid "8x8000,6x7500"', []))
        return rows, missing
    def conf_note(d):
        items = [f"{k}（{e['conflict']}）" for k, e in sorted(d.items()) if e.get("conflict")]
        return ("｜⚠️同型多标注取多数: " + "、".join(items[:4]) + ("…" if len(items) > 4 else "")) if items else ""
    slab_conf, beam_conf = conf_note(slab), conf_note(beam)
    tw = {}
    for key, e in slab.items():
        thk = e["thk"] or (default_thk[0] if default_thk else None)
        if not thk:
            missing.append(("板", key, "缺板厚", e["raws"][:1])); continue
        k = f"{thk}mm"
        tw[k] = tw.get(k, 0) + e["count"]
    slab_area = max(g["面积m2"] - (open_area_m2 or 0.0), 0.0)
    for thk_s, area in sorted(distribute(slab_area, tw).items()):
        t_mm = int(re.sub(r"\D", "", thk_s))
        rows.append(_row("板", f"板厚档 {thk_s}", thk_s, tw[thk_s], area * t_mm / 1000,
                         None, True, f"轴网包络 {g['Lx_m']}×{g['Ly_m']}m"
                                     + (f" −洞口 {open_area_m2:g}㎡" if open_area_m2 else "")
                                     + f" 分摊 {area}㎡ × 板厚{t_mm}" + slab_conf,
                         "-", "按图面板厚标注位置数加权分摊"))
    blen = round(g["Lx_m"] * (g["ay"]["跨数"] + 1) + g["Ly_m"] * (g["ax"]["跨数"] + 1), 1)
    sw = {}
    for key, e in beam.items():
        if not (e["b"] and e["h"]):
            missing.append(("梁", key, "缺梁截面（原位标注未绑定）", e["raws"][:1])); continue
        k = f"{e['b']}x{e['h']}"
        sw[k] = sw.get(k, 0) + e["count"]
    for sec_s, ln in sorted(distribute(blen, sw).items()):
        b, hh = [int(x) for x in re.split(r"[x×X]", sec_s)]
        rows.append(_row("梁", f"截面档 {sec_s}", sec_s, sw[sec_s], ln * b / 1000 * hh / 1000,
                         None, True, f"轴线总长 {blen}m 分摊 {ln}m × {sec_s}" + beam_conf,
                         "-", "按图面梁截面标注位置数加权分摊"))
    return rows, missing


def plan_rows(rows, loss=None):
    agg = {}
    for r in rows:
        k = (r["构件类别"], r["标号"])
        a = agg.setdefault(k, {"构件类别": k[0], "标号": k[1], "混凝土m3": 0.0, "型数": 0,
                               "钢筋估算kg带低": 0, "钢筋估算kg带高": 0})
        a["混凝土m3"] += r["混凝土m3"]; a["型数"] += 1
        lo, hi = r["钢筋估算kg带"].split("~")
        a["钢筋估算kg带低"] += int(lo); a["钢筋估算kg带高"] += int(hi)
    loss = RULES["损耗率"][".default"] if loss is None else loss
    for a in agg.values():
        a["混凝土m3"] = round(a["混凝土m3"], 2)
        a["订货量m3"] = round(a["混凝土m3"] * (1 + loss), 2)
        a["钢筋估算t"] = f"{round(a['钢筋估算kg带低']/1000,2)}~{round(a['钢筋估算kg带高']/1000,2)}"
    return sorted(agg.values(), key=lambda x: (x["构件类别"], x["标号"]))


# --------------------------------------------------------------- 输出
def write_out(rows, plan, missing, ctx, out_base: Path, fmt="all"):
    out_base.parent.mkdir(parents=True, exist_ok=True)
    prov = ctx.get("provenance") or {}
    sidecar = {
        "schema": "suanliang-result/v1",
        "skill": SKILL_NAME,
        "skill_version": _skill_version(),
        "status": "ok" if rows else "empty",
        "drawing": ctx.get("drawing"),
        "floor": ctx.get("label"),
        "row_count": len(rows or []),
        "plan": plan or [],
        "missing_count": len(missing or []),
        "missing": [
            {"member": c, "id": k, "why": why}
            for c, k, why, _raw in (missing or [])
        ],
        "provenance": prov.get("provenance", "manual"),
        "contract_id": prov.get("contract_id", ""),
        "source_sha256": prov.get("source_sha256", ""),
        "contract_sha256": prov.get("contract_sha256", ""),
        "reader_version": prov.get("reader_version", ""),
        "final_quantity": bool(prov.get("final_quantity")),
        "formal_ledger_eligible": bool(prov.get("formal_ledger_eligible")),
        "run_manifest": ctx.get("run_manifest") or {},
        "site_handoff": "site_handoff.json",
    }
    cs.write_json(str(out_base) + ".json", sidecar)
    if fmt in ("all", "csv"):
        for name, data in (("明细", rows), ("计划", plan)):
            if data:
                with Path(str(out_base) + f"-{name}.csv").open("w", newline="", encoding="utf-8-sig") as f:
                    w = csv.DictWriter(f, fieldnames=list(data[0].keys()), extrasaction="ignore")
                    w.writeheader(); w.writerows(data)
    md = io.StringIO()
    md.write(f"# 混凝土与钢筋计划口径速算｜{ctx['drawing']}\n\n")
    md.write(f"**楼层**：`{ctx['label']}` → 纳入文字 {ctx['kept']} 条 / 排除 {ctx['dropped']} 条 / 真图名 {ctx['titles']} 个"
             f"｜层高 {ctx['story'] or '未取到'} mm（{ctx['story_src']}｜{ctx.get('story_algo','')}）｜轴网 {ctx['grid'] or '未取到'}（{ctx['grid_src']}）"
             f"｜墙线长 {ctx['wall_len'] or 0} m｜范围 {ctx['box_src']}\n\n")
    if ctx.get("story_warn"):
        md.write(f"> ⚠️ **层高需核对**：{ctx['story_warn']}\n\n")
    if ctx.get("box_warn"):
        md.write(f"> ⚠️ **取数范围偏小**：{ctx['box_warn']}\n\n")
    md.write(f"**本次查询 {ctx['query_secs']} s**；索引 {'命中缓存（未解图）' if ctx['cached'] else '本次新建 ' + str(ctx['index_secs']) + ' s'}"
             f"｜口径 {ctx['rules']['版本']}（{ctx['rules']['指纹']}）\n\n")
    op = ctx.get("openings") or {}
    if op.get("合计m2") or op.get("只编号无尺寸"):
        md.write(f"**洞口**：图面可算 {op.get('图面可算', 0)} ㎡（{len(op.get('明细', []))} 处）"
                 f" + 人工补扣 {op.get('人工补扣', 0)} ㎡ → 板面积已减 {op.get('合计m2', 0)} ㎡；"
                 f"另有 {op.get('只编号无尺寸', 0)} 处只画不注尺寸（结构图常见，要扣请照建施给 --openings-m2）"
                 + (f"｜{'、'.join(op['明细'][:6])}" if op.get("明细") else "") + "\n\n")
    if plan:
        md.write("| 构件类别 | 标号 | 型数/档 | 净量m³ | 订货量m³ | 钢筋估算t（含量带） |\n|---|---|---|---|---|---|\n")
        for p in plan:
            md.write(f"| {p['构件类别']} | {p['标号']} | {p['型数']} | {p['混凝土m3']} | {p['订货量m3']} | {p['钢筋估算t']} |\n")
        md.write(f"\n**合计毛量 {round(sum(p['混凝土m3'] for p in plan),2)} m³"
                 f"（含损耗 {round(sum(p['订货量m3'] for p in plan),2)} m³）；"
                 f"钢筋估算带 {round(sum(p['钢筋估算kg带低'] for p in plan)/1000,2)}~"
                 f"{round(sum(p['钢筋估算kg带高'] for p in plan)/1000,2)} t**\n\n")
    conf = [r for r in rows if "⚠️" in (r.get("依据") or "")]
    if conf:
        md.write(f"> ⚠️ **{len(conf)} 行的尺寸在图上有多种标注**，取的是出现次数最多的那个，明细里「依据」列写了全部候选，"
                 f"报量前照图核一下：{('、'.join(sorted({r['编号/档位'] for r in conf})[:6]))}"
                 f"{'…' if len(conf) > 6 else ''}\n\n")
    norm_checks = ctx.get("norm_checks") or []
    if rows:
        md.write("## 规范校核（提示，不改量）\n\n")
        md.write(f"明细 {len(rows)} 行，其中 {len(norm_checks)} 行需核对。校核按常规区间与标注完整性提示；"
                 "不改变工程量，也不替代规范条文判断。\n\n")
        if norm_checks:
            md.write("| 构件类别 | 编号/档位 | 提示 |\n|---|---|---|\n")
            for c in norm_checks[:40]:
                md.write(f"| {c['构件类别']} | {c['编号/档位']} | {c['提示']} |\n")
            if len(norm_checks) > 40:
                md.write(f"\n其余 {len(norm_checks)-40} 条见明细「规范校核」列。\n")
        md.write("\n")
    if ctx.get("strip"):
        st = ctx["strip"]
        md.write(f"## 后浇带拆分\n\n带长 {st['长m']:g} m（{st['长来源']}）× 宽 {st['宽mm']:g} mm"
                 f"（{st['宽来源']}）= {st['面积m2']} ㎡ → "
                 f"封闭带 **{st['体积m3']} m³**（{st['封闭标号']}，按{st['分摊档']}个板厚档分摊）；"
                 f"上表板量已扣除＝先浇区。依据：{st['依据']}\n\n")
    if ctx.get("notes"):
        if ctx.get("strip") and any(x in str(ctx["notes"]) for x in ("底板", "外墙", "承台")):
            md.write("⚠️ 说明里后浇带还贯穿了墙/基础底板等构件，那些构件的封闭量本表未拆，需另计（见下表原文）。\n\n")
    if ctx.get("notes"):
        md.write("## 说明摘录（自动命中原文，未改写）\n\n| 条款 | 值 | 原文 |\n|---|---|---|\n")
        for k, v in ctx["notes"].items():
            md.write(f"| {k} | {v.get('值','')} | {str(v.get('原文',''))[:90]} |\n")
        md.write("\n")
    if missing:
        md.write(f"## 缺项清单（{len(missing)} 条，不猜数）\n\n| 构件 | 编号 | 缺什么 | 原文示例 |\n|---|---|---|---|\n")
        for c, k, why, raw in missing[:40]:
            md.write(f"| {c} | {k} | {why} | {(raw[0] if raw else '-')} |\n")
        md.write("\n")
    refs = RULES.get("规范引用") or {}
    ref_items = refs.get("引用") or []
    if ref_items:
        ref_txt = "；".join(f"{x.get('id','')} {x.get('name','')}" for x in ref_items[:12])
        md.write(f"> **规范/图集引用**：{ref_txt}｜{refs.get('说明','')}；"
                 f"{refs.get('知识库边界','')}\n\n")
    md.write(f"> **口径声明**：{RULES['不确定度']['声明']}；损耗率 "
             f"{round((RULES['损耗率']['.default'] if ctx['loss'] is None else ctx['loss'])*100,1)}%；"
             f"钢筋列＝净量 × 含筋率区间，是**带**不是逐根翻样；每行 `依据/图层/原文` 可回图核对。\n")
    Path(str(out_base) + ".md").write_text(md.getvalue(), encoding="utf-8")
    if fmt in ("all", "xlsx") and plan:
        try:
            import openpyxl
            from openpyxl.styles import Font
        except Exception:
            log("[输出] 无 openpyxl，已给 CSV/MD")
            return
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = "计划"
        tot_net = round(sum(p["混凝土m3"] for p in plan), 2)
        tot_ord = round(sum(p["订货量m3"] for p in plan), 2)
        lo = round(sum(p["钢筋估算kg带低"] for p in plan) / 1000, 2)
        hi = round(sum(p["钢筋估算kg带高"] for p in plan) / 1000, 2)
        ws.append([f"摘要：{ctx['label']}｜净量 {tot_net}m³｜订货 {tot_ord}m³｜钢筋 {lo}~{hi}t"
                   f"｜层高 {ctx['story'] or '未取到'}mm｜口径 {ctx['rules']['版本']}（{ctx['rules']['指纹']}）"])
        ws.append([])
        ws.append(["构件类别", "标号", "型数/档", "净量m3", "订货量m3", "钢筋估算t"])
        for p in plan:
            ws.append([p["构件类别"], p["标号"], p["型数"], p["混凝土m3"], p["订货量m3"], p["钢筋估算t"]])
        ws.append([]); ws.append(["合计毛量m3", round(sum(p["混凝土m3"] for p in plan), 2)])
        ws.append(["合计订货m3", round(sum(p["订货量m3"] for p in plan), 2)])
        ws.append(["口径", RULES["不确定度"]["声明"]])
        if rows:
            ws2 = wb.create_sheet("明细"); ws2.append(list(rows[0].keys()))
            for r in rows:
                ws2.append(list(r.values()))
        ws3 = wb.create_sheet("口径与依据")
        ws3.column_dimensions["A"].width = 20
        ws3.column_dimensions["B"].width = 110
        ws3.freeze_panes = "A2"
        ws3.append(["项目", "值"]); ws3.append(["楼层图名", ctx["label"]])
        op = ctx.get("openings") or {}
        if op:
            ws3.append(["洞口扣减", f"图面可算{op.get('图面可算',0)}㎡ + 人工{op.get('人工补扣',0)}㎡ = {op.get('合计m2',0)}㎡"
                                   f"（另有{op.get('只编号无尺寸',0)}处只画不注尺寸）"])
        ws3.append(["口径版本", f"{ctx['rules']['版本']}（指纹 {ctx['rules']['指纹']}）"])
        if ref_items:
            ws3.append(["规范/图集引用", "；".join(f"{x.get('id','')} {x.get('name','')}" for x in ref_items[:12])])
            ws3.append(["引用边界", f"{refs.get('说明','')}｜{refs.get('知识库边界','')}"])
        norm_checks = ctx.get("norm_checks") or []
        ws3.append(["规范校核", f"{max(len(rows) - len(norm_checks), 0)}/{len(rows)} 行通过；{len(norm_checks)} 行需核对"])
        for c in norm_checks[:20]:
            ws3.append([f"⚠️ 校核·{c['构件类别']}·{c['编号/档位']}", c['提示']])
        ws3.append(["层高mm（来源）", f'{ctx["story"] or "未取到"}（{ctx["story_src"]}｜{ctx.get("story_algo","")}）'])
        if ctx.get("story_warn"):
            ws3.append(["⚠️ 层高需核对", ctx["story_warn"]])
        conf = [r for r in rows if "⚠️" in (r.get("依据") or "")]
        if conf:
            ws3.append(["⚠️ 尺寸多标注", f"{len(conf)} 行取多数，候选见明细'依据'列："
                                      + "、".join(sorted({r["编号/档位"] for r in conf})[:8])])
        ws3.append(["轴网（来源）", f'{ctx["grid"] or "未取到"}（{ctx["grid_src"]}）'])
        if ctx.get("strip"):
            st = ctx["strip"]
            ws3.append(["后浇带", f'带长{st["长m"]:g}m×宽{st["宽mm"]:g}mm（{st["宽来源"]}）='
                                 f'{st["面积m2"]}㎡ → 封闭带{st["体积m3"]}m³（{st["封闭标号"]}），先浇区已同额扣除'])
        for k, v in (ctx.get("notes") or {}).items():
            ws3.append([f"说明·{k}", f'{v.get("值","")}｜{str(v.get("原文",""))[:90]}'])
        for c, _k, why, raw in (missing or [])[:40]:
            ws3.append([f"缺项·{c}", f'{why}｜{(raw[0] if raw else "")[:70]}'])
        for c in ws3[1]:
            c.font = Font(bold=True)
        ws.freeze_panes = "A4"
        for col, w in zip("ABCDEF", (10, 16, 10, 12, 12, 16)):
            ws.column_dimensions[col].width = w
        for row in ws.iter_rows(min_row=4, min_col=4, max_col=5):
            for c in row:
                c.number_format = "0.00"
        ws["A1"].font = Font(bold=True)
        for c in ws[3]:
            c.font = Font(bold=True)
        wb.save(str(out_base) + ".xlsx")


# --------------------------------------------------------------- 契约入口
def _skill_version() -> str:
    try:
        return str(json.loads((Path(__file__).resolve().parents[1] / "manifest.json")
                              .read_text(encoding="utf-8")).get("version") or SKILL_VERSION)
    except Exception:
        return SKILL_VERSION


def contract_cache_dir(contract: Path, guard: dict, override=None) -> Path:
    """契约缓存按 contract_sha256 分目录，绝不复用原 DWG 的文件哈希缓存。"""
    digest = guard.get("contract_sha256") or file_key(contract)
    key = "contract-" + digest[:16]
    if override:
        return Path(override) / key
    local = contract.parent / ".cadidx" / key
    try:
        local.mkdir(parents=True, exist_ok=True)
        return local
    except Exception:
        import tempfile
        base = Path(os.environ.get("QTY_CACHE_DIR") or (Path(tempfile.gettempdir()) / "tujian-suanliang-cache"))
        log(f"[缓存] 契约目录不可写，改用 {base}")
        base.mkdir(parents=True, exist_ok=True)
        return base / key


def _contract_payload(doc: dict) -> dict:
    payload = doc.get("contract") if isinstance(doc.get("contract"), dict) else doc
    return payload if isinstance(payload, dict) else {}


def materialize_contract(contract: Path, guard: dict, out: Path) -> Path:
    """把契约 payload 落成 detail.json；不调用 cad_scan，不重新解图。"""
    doc = json.loads(contract.read_text(encoding="utf-8"))
    payload = _contract_payload(doc)
    missing = [key for key in ("text_records", "geometry_segments") if key not in payload]
    if missing:
        print("[tujian] 契约缺 %s，无法重建索引；请回 cad-file-reader 重新生成。"
              % ", ".join(missing), file=sys.stderr)
        raise SystemExit(5)
    out.mkdir(parents=True, exist_ok=True)
    cs.write_json(out / "detail.json", payload)
    cs.write_json(out / "scan.json", payload)
    cs.write_json(out / "contract.json", doc)
    cs.write_json(out / "provenance.json", {
        "provenance": guard.get("provenance") or "manual",
        "mode": guard.get("mode") or "manual",
        "contract_id": guard.get("contract_id") or "",
        "source_sha256": guard.get("source_sha256") or "",
        "contract_sha256": guard.get("contract_sha256") or "",
        "formal_ledger_eligible": bool(guard.get("formal_ledger_eligible")),
        "contract_file": str(contract),
    })
    return out


def resolve_contract_source(a):
    """返回 (缓存目录, guard)；只接受 cad-contract/v1 JSON，拒绝直接 DWG。"""
    raw = Path(a.dwg).expanduser()
    if not raw.is_file():
        print("[tujian] 输入不存在：%s" % raw, file=sys.stderr)
        raise SystemExit(2)
    if raw.suffix.lower() != ".json":
        print("[tujian] 已按识图契约红线拒绝直接图纸：%s\n"
              "请先用 cad-file-reader 产出 cad-contract/v1 契约（cad_scan / cad_contract），"
              "再把契约 JSON 交给本入口；本技能不自行解析 DWG/DXF。" % raw.name,
              file=sys.stderr)
        raise SystemExit(2)
    try:
        guard = guard_contract(raw, allow_manual=bool(getattr(a, "allow_manual", False)))
    except GuardError as exc:
        print("[GuardError %d] %s" % (exc.code, exc.message), file=sys.stderr)
        if exc.hint:
            print("修复: %s" % exc.hint, file=sys.stderr)
        raise SystemExit(exc.code) from None
    out = contract_cache_dir(raw, guard, getattr(a, "cache_dir", None))
    materialize_contract(raw, guard, out)
    log("[契约] provenance=%s contract_id=%s %s" % (
        guard.get("provenance"), guard.get("contract_id") or "-",
        "" if guard.get("mode") == "formal" else "（手工降级：final_quantity=false）"))
    return out, guard


# --------------------------------------------------------------- 命令
def cmd_index(a):
    out, guard = resolve_contract_source(a)
    db = build_index(Path(a.dwg).expanduser(), out, a.with_geom, True,
                     compare_baseline=getattr(a, "compare_baseline", ""))
    print(json.dumps({"ok": True, "db": str(db),
                      "provenance": guard.get("provenance"),
                      "contract_id": guard.get("contract_id") or "",
                      "final_quantity": bool(guard.get("formal_ledger_eligible"))},
                     ensure_ascii=False))
    return 0


def cmd_floors(a):
    out, guard = resolve_contract_source(a)
    t0 = time.time()
    db = build_index(Path(a.dwg).expanduser(), out, a.with_geom, True)
    _meta, _built, rows, _segs, _sheets = load(db)
    titles, info = find_titles(rows, a.min_refs, a.radius_mm, a.title_pattern)
    log(f"真图名 {info['real']} 个（候选 {info['cand']}，构件文字 {info['members']}，半径 {info.get('radius')} mm）"
        f"；用时 {round(time.time()-t0,2)}s")
    for t in sorted(titles, key=lambda x: -x["refs"]):
        print(f"| {t['title']} | {int(t['x'])},{int(t['y'])} | {t['refs']} |")
    return 0


def cmd_floor(a):
    out, guard = resolve_contract_source(a)
    dwg = Path(a.dwg).expanduser()
    t0 = time.time()
    db = build_index(dwg, out, a.with_geom, True)
    index_secs = round(time.time() - t0, 1)
    cached = index_secs < 0.6
    meta, built, rows, segs, sheets = load(db)
    titles, info = find_titles(rows, a.min_refs, a.radius_mm, a.title_pattern)
    hits, kept, dropped, fbox = scope(rows, titles, a.floor_label, sheets, a.floor_regex,
                                      getattr(a, "window_radius_mm", None))
    if hits is None:
        print(json.dumps({"ok": False, "status": "not-found", "query": a.floor_label,
                          "图上真图名": [t["title"] for t in titles][:80]}, ensure_ascii=False, indent=1))
        return 3
    prof = load_profile(out)
    members, pos = parse_members(kept, a.dedupe_mm)
    bind_sizes(members, pos, a.bind_radius_mm)
    nbound, tbl_ids, tnotes = schedule_bind(members, kept, label_range(a.floor_label))
    msz = parse_member_size(a.member_size or prof.get("member_sizes") or "")
    msz_src = "人工参数" if a.member_size else "本图已存配置"
    if msz:
        if not a.member_size:
            log(f"[尺寸] 沿用本图人工配置 {len(msz)} 型")
        nman = apply_member_size(members, msz, msz_src)
        if nman:
            log(f"[尺寸] 人工参数补上 {nman} 型截面/墙厚")
    if nbound:
        log(f"[表格绑定] 从柱表/墙身表补上 {nbound} 个构件的截面或墙厚（表内编号不计进根数）")
        kept2 = [r for r in kept if r[0] not in tbl_ids]
        members, pos = parse_members(kept2, a.dedupe_mm)
        bind_sizes(members, pos, a.bind_radius_mm)
        schedule_bind(members, kept, label_range(a.floor_label))
        if msz:
            apply_member_size(members, msz, msz_src)
    for n in tnotes[:6]:
        log("        " + n)
    dft = default_thk(meta.get("spec"))
    grid = a.axis_grid or prof.get("axis_grid")
    ginfo = {"人工参数": a.axis_grid} if a.axis_grid else ({"本图配置": prof.get("axis_grid")} if grid else {})
    if grid and not a.axis_grid:
        log(f"[轴网] 沿用本图已存配置：{grid}")
    if not grid and a.try_auto_grid:
        grid, ginfo = axis_grid(segs, fbox)
        log(f"[轴网] 自动尝试：{grid or '失败 → ' + ginfo.get('原因','')}")
        if not grid:
            log("        天正轴网常是自定义实体、解不出线段；给一次 --axis-grid 即可，本图之后自动沿用")
    story, sinfo = a.story_height_mm, {"来源": "人工参数"}
    if not story and a.auto_story:
        story, sinfo = story_from_tables(rows, sheets, a.floor_label, titles, a.story_basis)
        log(f"[层高] 本层自动：{str(story) + 'mm' if story else '失败 → ' + sinfo.get('原因','')}"
            + ("｜" + sinfo["算法"] if story else ""))
        if story and sinfo.get("需核对"):
            log("⚠️ " + sinfo["需核对"])
    if not story and prof.get("story_height_mm"):
        story, sinfo = prof["story_height_mm"], {"来源": "本图上次配置（可能不是本层值，需核对）"}
        log(f"[层高] 退回上次配置 {story}mm（该值来自别的层，请核对）")
    wlen = wall_length(segs, fbox, {l for e in members["墙"].values() for l in e["layers"]})
    op_area, op_items, op_naked = openings(kept)
    op_manual = a.openings_m2 or 0.0
    pre_missing = []
    if op_manual and not 0 <= op_manual < 100000:
        pre_missing.append(("板", "-", f"洞口面积 {op_manual}㎡ 不合理（0~100000），本层未扣洞口", []))
        op_manual = 0.0
    op_total = round(op_area + op_manual, 2)
    rows_out, missing = volumes(members, story, grid, wlen, dft, op_total)
    missing.extend(pre_missing)
    joined = join_lines(kept if len(kept) > 50 else rows)
    facts = notes_facts(rows, joined, fbox)
    strip = None
    if rows_out:
        if a.strip_length_m:
            w_src, w_raw = "--strip-width-mm", a.strip_width_mm
            if not w_raw:
                w_src, w_raw = "图面说明原文", (facts.get("后浇带宽mm") or {}).get("值")
            if not w_raw:
                w_src, w_raw = f"未标注，按默认 {RULES['后浇带']['默认带宽mm']}mm（推定）", RULES["后浇带"]["默认带宽mm"]
                missing.append(("后浇带", "-", "说明里没读到带宽，已按默认800mm推定，报量前核对一下",
                                [(facts.get("后浇带") or {}).get("原文", "")]))
            wmm = parse_strip_width(w_raw)
            if wmm and not 100 <= wmm <= 3000:
                missing.append(("后浇带", "-", f"带宽 {wmm:g}mm 不合理（应在 100~3000），本层未拆分",
                                [str(w_raw)]))
                wmm = None
            if wmm:
                rows_out, strip = strip_split(rows_out, a.strip_length_m, wmm, facts, w_src)
                if strip:
                    log(f"[后浇带] 带长 {a.strip_length_m:g}m × 宽 {wmm:g}mm（{w_src}）→ 封闭带 {strip['体积m3']}m³"
                        f"（{strip['封闭标号']}，先浇区已同额扣除）")
                else:
                    log("[后浇带] 本层没出板量（多是梁层/墙层），未拆分；带长给板层用")
        elif facts:
            missing.append(("后浇带", "-", "说明里有后浇带但未拆分：报量时加 --strip-length-m 本层带长合计(m)",
                            [(facts.get("后浇带") or facts.get("后浇带宽mm", {})).get("原文", "")]))
    norm_checks = norm_check(rows_out)
    plan = plan_rows(rows_out, a.loss)
    write_out(rows_out, plan, missing, {"drawing": dwg.name, "label": a.floor_label, "kept": len(kept),
              "dropped": len(dropped), "titles": info.get("real"), "story": story,
              "story_src": sinfo.get("来源表") or sinfo.get("来源") or "人工参数",
              "story_algo": sinfo.get("算法", ""), "story_warn": sinfo.get("需核对", ""),
              "box_src": ("图框 %dm×%dm" % ((fbox[2]-fbox[0])//1000, (fbox[3]-fbox[1])//1000)) if fbox else "未取到",
              # 图名与图面分处两处时图框会框错（只框到图名周边一小块），
              # 这时取到的文字占全图比例极低，明说比静默出个偏小的量好
              "box_warn": ("只纳入全图 %d%% 的文字，图名与图面可能不在同一个图框里；"
                           "人工给 --window-radius-mm 直接定取数半径" % (100 * len(kept) // max(len(rows), 1)))
                          if rows and len(kept) < 0.1 * len(rows) else "",
              "grid": grid, "grid_src": ("图面自动" if ginfo.get("x向轴数") else
                             ("人工参数" if a.axis_grid else ("本图上次配置" if grid else "未取到"))),
              "wall_len": wlen, "cached": cached, "index_secs": index_secs, "notes": facts, "strip": strip,
              "openings": {"图面可算": op_area, "人工补扣": op_manual, "合计m2": op_total,
                           "明细": op_items, "只编号无尺寸": op_naked},
              "norm_checks": norm_checks,
              "rules": {"版本": RULES.get("version"), "指纹": RULES_SHA},
              "query_secs": round(time.time() - t0, 2), "loss": a.loss,
              "provenance": cs.provenance_fields(guard),
              "run_manifest": cs.run_manifest(SKILL_NAME, _skill_version(), guard)},
              Path(a.out).expanduser().resolve().parent / Path(a.out).expanduser().name, a.fmt)
    members = []
    for i, row in enumerate(rows_out or [], 1):
        volume = row.get("混凝土m3")
        weight = round(float(volume) * 2.5, 2) if isinstance(volume, (int, float)) else None
        members.append(cs.handoff_member(
            "TUJIAN-%04d" % i,
            weight_t=weight, length_m=None,
            section=str(row.get("截面/尺寸") or ""),
            grade=str(row.get("标号") or ""),
            zone=str(a.floor_label or ""),
            weight_basis=("total" if weight is not None else "unknown"),
            weight_formula=("volume_m3*2.5" if weight is not None else ""),
            quantity_m3=volume, quantity_basis="concrete_volume"))
    cs.write_handoff(Path(a.out).expanduser().resolve().parent, a.floor_label,
                     "concrete", guard, members)
    if op_naked or op_total:
        log(f"[洞口] 图面可算 {op_area}㎡（{len(op_items)} 处）+ 人工 {op_manual}㎡ → 板面积扣 {op_total}㎡；"
            f"另有 {op_naked} 个洞口只画不注尺寸（结构图常见，要扣用 --openings-m2）")
    if grid or story:
        save_profile(out, {"axis_grid": grid, "story_height_mm": story,
                           "member_sizes": (a.member_size or prof.get("member_sizes") or ""),
                           "note": "一次配置，本图之后所有楼层查询沿用；--axis-grid/--story-height-mm/--member-size 可覆盖"})
    log(f"[耗时] {round(time.time()-t0,2)}s（索引{'命中' if cached else '新建'}）→ {a.out}.md/.csv/.xlsx")
    return 4 if (missing and not rows_out) else 0


def main(argv=None):
    # --check-deps 必须在子命令解析前拦下：子解析器 required=True 会把
    # `qty_core.py --check-deps` 当成"缺子命令"直接 exit 2，导致依赖体检
    # 永远跑不到真正的检查逻辑（s5 实测）。
    raw = list(sys.argv[1:] if argv is None else argv)
    if "--check-deps" in raw:
        status = cs.check_deps()
        print(cs.format_deps(status))
        return eg.dependency_exit_code()
    ap = argparse.ArgumentParser(description="土建算量：按层出混凝土方量与钢筋估算带")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("index"); p.add_argument("dwg"); p.add_argument("--cache-dir")
    p.add_argument("--with-geom", dest="with_geom", action="store_true", default=True)
    p.add_argument("--no-geom", dest="with_geom", action="store_false")
    p.add_argument("--compare-baseline", dest="compare_baseline", default="",
                   help="基线 detail.json；给出后自动用 cad_compare.sh 输出图纸变化候选，不阻断出量")
    p.add_argument("--allow-manual", action="store_true",
                   help="允许消费手工 cad-contract/v1 契约；结果强制 final_quantity=false")
    p.set_defaults(func=cmd_index)
    p.add_argument("--keep-detail", dest="keep_detail", action="store_true",
                   help="保留解图明细 JSON（占空间大，重建索引时才用得上）")
    p = sub.add_parser("floors"); p.add_argument("dwg"); p.add_argument("--cache-dir")
    p.add_argument("--min-refs", type=int, default=10); p.add_argument("--radius-mm", type=float)
    p.add_argument("--title-pattern")
    p.add_argument("--with-geom", dest="with_geom", action="store_true", default=True)
    p.add_argument("--no-geom", dest="with_geom", action="store_false")
    p.add_argument("--allow-manual", action="store_true",
                   help="允许消费手工 cad-contract/v1 契约；结果强制 final_quantity=false")
    p.set_defaults(func=cmd_floors)
    p.add_argument("--keep-detail", dest="keep_detail", action="store_true")
    p = sub.add_parser("floor"); p.add_argument("dwg"); p.add_argument("--floor-label", required=True)
    p.add_argument("--floor-regex", action="store_true"); p.add_argument("--story-height-mm", type=float)
    p.add_argument("--axis-grid"); p.add_argument("--loss", type=float); p.add_argument("-o", "--out", required=True)
    p.add_argument("--dedupe-mm", type=float, default=1500.0); p.add_argument("--bind-radius-mm", type=float, default=3000.0)
    p.add_argument("--fmt", default="all", choices=["all", "csv", "md", "xlsx"]); p.add_argument("--cache-dir")
    p.add_argument("--with-geom", dest="with_geom", action="store_true", default=True)
    p.add_argument("--no-geom", dest="with_geom", action="store_false")
    p.add_argument("--min-refs", type=int, default=10)
    p.add_argument("--radius-mm", type=float); p.add_argument("--title-pattern")
    p.add_argument("--window-radius-mm", dest="window_radius_mm", type=float,
                   help="人工指定本层取数半径(mm)：图名与图面分处两处、图框又识别不出主图幅时用，"
                        "给了就不再猜图框，直接以图名为心按这个半径取数")
    p.add_argument("--try-auto-grid", dest="try_auto_grid", action="store_true", default=True,
                   help="默认从普通线段复原轴网（支持混合跨距）；失败会写进缺项清单")
    p.add_argument("--no-auto-grid", dest="try_auto_grid", action="store_false")
    p.add_argument("--strip-length-m", dest="strip_length_m", type=float,
                   help="本层后浇带中心线总长(m)，平面图上量一次；给了才拆出封闭带那一笔")
    p.add_argument("--strip-width-mm", dest="strip_width_mm", type=float,
                   help="带宽；不给就从说明里读（说明常写 宽度均为800）")
    p.add_argument("--openings-m2", dest="openings_m2", type=float,
                   help="按建施/洞表人工补扣的洞口面积合计(㎡)，从板面积里减掉")
    p.add_argument("--member-size", dest="member_size",
                   help="人工给一次的构件尺寸：KZ1=500x900,Q2=250（柱梁给截面、墙给厚），存进本图配置")
    p.add_argument("--story-basis", choices=["below", "above"], default="below",
                   help="层高取哪一段：below=本层标高减下层标高（跟着本层顶板一起浇的柱墙段，报计划用这个）；above=本层往上那一段")
    p.add_argument("--keep-detail", dest="keep_detail", action="store_true",
                   help="保留解图明细 JSON（默认建完索引就回收，一张 21.7MB 图能省 ~35MB）")
    p.add_argument("--no-auto-story", dest="auto_story", action="store_false")
    p.add_argument("--allow-manual", action="store_true",
                   help="允许消费手工 cad-contract/v1 契约；结果强制 final_quantity=false")
    p.set_defaults(func=cmd_floor, auto_story=True)
    ap.add_argument("--check-deps", action="store_true",
                    help="只检查 cad-file-reader / lis-skill-bus / Python 前置，不读图纸")
    a = ap.parse_args(raw)
    # 入口闸门：缺 cad-file-reader / lis-skill-bus 先停；直接给图纸一律拒收。
    try:
        eg.require_reader()
        eg.require_bus()
        eg.reject_drawing_input(getattr(a, "dwg", None))
    except eg.GateError as exc:
        return eg.print_gate_error(exc)
    return a.func(a) or 0


if __name__ == "__main__":
    sys.exit(main())
