#!/usr/bin/env python3
"""
WDFW Puget Sound saltwater creel report — configurable salmon analyzer.

Scrapes https://wdfw.wa.gov/fishing/reports/creel/puget (no public API for the marine
areas) and reports catch-per-angler (CPUE), effort, trends, top launches, and a chart
for a CONFIGURABLE selection of salmon species and marine areas.

Configure via (highest priority last): built-in DEFAULTS -> config.json next to this
script (or --config PATH) -> CLI flags.

  species  : any of chinook, coho, chum, pink, sockeye   (combined into one CPUE metric)
  areas    : marine area codes as shown on WDFW, e.g. 8-2, 9, 10, 11
  until    : end date (YYYY-MM-DD); on/after which --email stops sending
  frequency: choose the report mode you schedule -> --daily (default) or --weekly

Modes:
  creel_report.py                          daily per-area digest -> stdout
  creel_report.py --weekly                 weekly launch report + chart -> stdout
  creel_report.py --weekly --email         build HTML report + email it
  creel_report.py --species coho,chum --areas 9,10 --weekly
  creel_report.py --config myconfig.json --weekly --email --until 2026-09-25
  creel_report.py --no-fetch ...           use stored data, skip scraping

Data is raw and revised by WDFW after QA/QC, so each run re-scrapes the trailing
`trailing_days` days and overwrites stored values. All 5 species are stored regardless
of selection, so changing species/areas needs no re-scrape.

Email creds (never committed): ~/.openclaw/creel_email.json
  {"smtp_host","smtp_port","smtp_user","smtp_pass","from","to"}
"""
import json, re, sys, os, ssl, smtplib, urllib.request, datetime, copy, time
from email.message import EmailMessage
from email.utils import formataddr
from html import unescape, escape

HERE = os.path.dirname(os.path.abspath(__file__))
STORE_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "memory", "creel"))
DAILY_JSON = os.path.join(STORE_DIR, "daily.json")
DIGEST_MD = os.path.join(STORE_DIR, "latest_digest.md")
WEEKLY_MD = os.path.join(STORE_DIR, "weekly_report.md")
CHART_PNG = os.path.join(STORE_DIR, "cpue_areas.png")
ALERT_STATE = os.path.join(STORE_DIR, "alert_state.json")
CREDS_FILE = os.path.expanduser("~/.openclaw/creel_email.json")
DEFAULT_CONFIG = os.path.join(HERE, "config.json")

PUGET_URL = "https://wdfw.wa.gov/fishing/reports/creel/puget"
MAX_PAGES = 12
UA = {"User-Agent": "Mozilla/5.0 (creel-report)"}
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

SPECIES = ["chinook", "coho", "chum", "pink", "sockeye"]  # the 5 Pacific salmon (page columns)
SPECIES_PRETTY = {"chinook": "Chinook", "coho": "Coho", "chum": "Chum",
                  "pink": "Pink", "sockeye": "Sockeye"}
# Okabe-Ito + Tol colorblind-friendly palette, cycled across selected areas
PALETTE = ["#E69F00", "#56B4E9", "#009E73", "#D55E00", "#0072B2", "#CC79A7",
           "#F0E442", "#000000", "#117733", "#AA4499", "#44AA99", "#882255"]

# --- your defaults (edit config.json or pass flags to change) ---
DEFAULTS = {
    "areas": ["8-2", "9", "10", "11"],
    "species": ["coho"],
    "trailing_days": 14,
    "top_launches": 3,
    "min_week_anglers": 20,
    "anomaly_mult": 1.5,
    "daily_min_anglers": 15,
    "until": None,
    # Proactive hot-bite alerts (OpenClaw heartbeat/cron feature). Toggle with enabled.
    "alerts": {"enabled": False, "spike_mult": 1.8, "min_anglers": 30, "min_cpue": 0.4,
               "cooldown_days": 2, "min_baseline_days": 2},
}


# ---------- config ----------
def resolve_config(args):
    cfg = copy.deepcopy(DEFAULTS)
    path = _flag_val(args, "--config") or (DEFAULT_CONFIG if os.path.exists(DEFAULT_CONFIG) else None)
    if path:
        with open(path) as f:
            loaded = json.load(f)
        for k, v in loaded.items():
            if k == "alerts" and isinstance(v, dict):
                cfg["alerts"].update(v)          # merge nested alert settings
            elif k in DEFAULTS:
                cfg[k] = v
    if _flag_val(args, "--areas"):
        cfg["areas"] = [a.strip() for a in _flag_val(args, "--areas").split(",") if a.strip()]
    if _flag_val(args, "--species"):
        cfg["species"] = [s.strip().lower() for s in _flag_val(args, "--species").split(",") if s.strip()]
    if _flag_val(args, "--until"):
        cfg["until"] = _flag_val(args, "--until")
    bad = [s for s in cfg["species"] if s not in SPECIES]
    if bad:
        raise SystemExit(f"unknown species {bad}; choose from {SPECIES}")
    if not cfg["areas"] or not cfg["species"]:
        raise SystemExit("config must have at least one area and one species")
    return cfg


def _flag_val(args, name):
    if name in args:
        i = args.index(name)
        return args[i + 1] if i + 1 < len(args) else None
    return None


def species_label(cfg):
    return "+".join(SPECIES_PRETTY[s] for s in cfg["species"])


# ---------- fetch / parse ----------
def fetch(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f"fetch failed for {url}: {last}")


def clean(s):
    return re.sub(r"\s+", " ", unescape(re.sub("<[^>]+>", "", s))).strip()


def parse_date(caption):
    m = re.search(r"([A-Z][a-z]{2}) (\d{1,2}), (\d{4})", caption)
    if not m or m.group(1) not in MONTHS:
        return None
    return f"{int(m.group(3)):04d}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"


def area_code(area_name):
    m = re.match(r"Area (\d+(?:-\d+)?)", area_name)
    return m.group(1) if m else None


def num(v):
    v = v.replace(",", "").replace(" ", "").strip()
    if v in ("", "-", "N/A"):
        return 0.0
    try:
        return float(v)
    except ValueError:
        return 0.0


def parse_puget(html):
    """Return {date: [row,...]} for every marine 'Area N' row, all species stored."""
    out = {}
    for tbl in re.findall(r"<table.*?</table>", html, re.S):
        cap = re.search(r"<caption[^>]*>(.*?)</caption>", tbl, re.S)
        if not cap:
            continue
        date = parse_date(clean(cap.group(1)))
        if not date:
            continue
        rows = out.setdefault(date, [])
        for tr in re.findall(r"<tr.*?</tr>", tbl, re.S):
            f = {}
            for fld, val in re.findall(
                    r'<td[^>]*class="[^"]*views-field-([a-z-]+)[^"]*"[^>]*>(.*?)</td>', tr, re.S):
                f[fld] = clean(val)
            name = f.get("catch-area-name")
            code = area_code(name) if name else None
            if not code:
                continue
            row = {"ramp": f.get("location-name", "").strip(), "area": code,
                   "area_name": name, "interviews": num(f.get("boats", "0")),
                   "anglers": num(f.get("anglers", "0"))}
            for sp in SPECIES:
                row[sp] = num(f.get(sp, "0"))
            rows.append(row)
    return out


def scrape_recent(trailing_days):
    collected = {}
    cutoff = (datetime.date.today() - datetime.timedelta(days=trailing_days)).isoformat()
    for p in range(MAX_PAGES):
        page = parse_puget(fetch(f"{PUGET_URL}?page={p}"))
        if not page:
            break
        new = False
        for date, rows in page.items():
            if date not in collected:
                collected[date] = rows
                new = True
        if min(collected) <= cutoff:
            break
        if not new:
            break
    return {d: r for d, r in collected.items() if d >= cutoff}


# ---------- storage ----------
def load_store():
    if not os.path.exists(DAILY_JSON):
        return {}
    with open(DAILY_JSON) as f:
        raw = json.load(f)
    return {d: v for d, v in raw.items() if isinstance(v, list)}


def save_store(store):
    os.makedirs(STORE_DIR, exist_ok=True)
    with open(DAILY_JSON, "w") as f:
        json.dump(store, f, indent=2, sort_keys=True)


# ---------- aggregation ----------
def target_catch(row, cfg):
    return sum(row.get(sp, 0.0) for sp in cfg["species"])


def sampled_dates(store):
    return [d for d in sorted(store) if any(r["anglers"] > 0 for r in store[d])]


def area_totals(rows, cfg):
    """{code: {anglers, interviews, catch}} for configured areas; catch = selected species sum."""
    out = {}
    for r in rows:
        if r["area"] not in cfg["areas"]:
            continue
        a = out.setdefault(r["area"], {"anglers": 0.0, "interviews": 0.0, "catch": 0.0})
        a["anglers"] += r["anglers"]
        a["interviews"] += r["interviews"]
        a["catch"] += target_catch(r, cfg)
    return out


def cpue(catch, anglers):
    return round(catch / anglers, 3) if anglers else 0.0


def window_dates(dates, end, span):
    lo = (datetime.date.fromisoformat(end) - datetime.timedelta(days=span - 1)).isoformat()
    return [d for d in dates if lo <= d <= end]


def area_labels(store, cfg):
    """Build friendly labels from scraped area names: 'Area 10 (Seattle-Bremerton)'."""
    names = {}
    for d in sorted(store):
        for r in store[d]:
            if r["area"] in cfg["areas"] and r.get("area_name"):
                names[r["area"]] = r["area_name"]
    out = {}
    for code in cfg["areas"]:
        nm = names.get(code, "")
        m = re.match(r"Area \S+,\s*(.+)", nm)
        out[code] = f"Area {code} ({m.group(1).strip()})" if m else f"Area {code}"
    return out


# ---------- daily digest ----------
def daily_digest(store, cfg):
    dates = sampled_dates(store)
    if not dates:
        return "No creel samples in the stored window yet."
    labels = area_labels(store, cfg)
    slabel = species_label(cfg)

    def totals(d):
        return area_totals(store[d], cfg)

    def day_anglers(d):
        return sum(a["anglers"] for a in totals(d).values())

    substantive = [d for d in dates if day_anglers(d) >= cfg["daily_min_anglers"]]
    latest = substantive[-1] if substantive else dates[-1]
    newest = sorted(store)[-1]
    prior = [d for d in dates if d < latest]
    L = totals(latest)

    def ref_for(code, target):
        cand = [d for d in prior if totals(d).get(code) and totals(d)[code]["anglers"] > 0]
        if not cand:
            return None
        t = datetime.date.fromisoformat(target)
        return min(cand, key=lambda d: abs((datetime.date.fromisoformat(d) - t).days))

    wow_target = (datetime.date.fromisoformat(latest) - datetime.timedelta(days=7)).isoformat()

    lines = [f"🎣 *Puget Sound {slabel} Creel — {latest}*",
             f"Areas {', '.join(cfg['areas'])} · {slabel} · _raw data, revised after QA/QC_"]
    if newest != latest:
        lines.append(f"_(Latest sampled day; {newest} not fully posted yet.)_")
    lines.append("")

    flags = []
    for code in cfg["areas"]:
        if code not in L:
            continue
        cur = cpue(L[code]["catch"], L[code]["anglers"])
        base = [cpue(totals(d)[code]["catch"], totals(d)[code]["anglers"])
                for d in prior if totals(d).get(code) and totals(d)[code]["anglers"] > 0]
        b = sum(base) / len(base) if base else None
        if b and b > 0 and cur >= b * cfg["anomaly_mult"] and cur >= 0.05:
            flags.append(f"  ⚠️ {labels[code]}: CPUE {cur:.2f} vs {b:.2f} avg ({cur / b:.1f}×)")
    if flags:
        lines.append("*What changed:*")
        lines += flags + [""]

    lines.append("*By area (latest day), best first:*")
    order = sorted(cfg["areas"],
                   key=lambda c: cpue(L[c]["catch"], L[c]["anglers"]) if c in L else -1,
                   reverse=True)
    for code in order:
        if code not in L:
            lines.append(f"• *{labels[code]}* — no samples")
            continue
        cur = cpue(L[code]["catch"], L[code]["anglers"])
        pd = ref_for(code, latest)
        wd = ref_for(code, wow_target)
        pc = cpue(totals(pd)[code]["catch"], totals(pd)[code]["anglers"]) if pd else None
        wc = cpue(totals(wd)[code]["catch"], totals(wd)[code]["anglers"]) if wd else None
        dod = f"{cur - pc:+.2f}" if pc is not None else "n/a"
        wow = f"{cur - wc:+.2f}" if wc is not None else "n/a"
        lines.append(f"• *{labels[code]}*: {int(L[code]['anglers'])} anglers, "
                     f"{int(L[code]['catch'])} {slabel} · CPUE {cur:.2f} (DoD {dod}, WoW {wow})")
    lines.append("")

    win = window_dates(dates, latest, 7)
    lines.append(f"*7-day avg ({slabel}/angler, {win[0]}..{win[-1]}), best first:*")
    agg7 = {}
    for code in cfg["areas"]:
        c = a = 0.0
        for d in win:
            t = totals(d).get(code)
            if t:
                c += t["catch"]
                a += t["anglers"]
        agg7[code] = (c, a)
    tc = sum(c for c, a in agg7.values())
    ta = sum(a for c, a in agg7.values())
    for code in sorted(cfg["areas"], key=lambda c: cpue(*agg7[c]) if agg7[c][1] > 0 else -1,
                       reverse=True):
        c, a = agg7[code]
        lines.append(f"• *{labels[code]}*: {cpue(c, a):.2f}  ({int(c)} / {int(a)} anglers)"
                     if a > 0 else f"• *{labels[code]}*: no samples")
    lines.append(f"• *All areas*: {cpue(tc, ta):.2f}  ({int(tc)} {slabel} / {int(ta)} anglers)")
    lines.append("")
    lines.append(f"_History: {len(dates)} sampled days stored._")
    return "\n".join(lines)


# ---------- proactive hot-bite alerts (OpenClaw heartbeat/cron) ----------
def _load_alert_state():
    if os.path.exists(ALERT_STATE):
        with open(ALERT_STATE) as f:
            return json.load(f)
    return {}


def _save_alert_state(s):
    os.makedirs(STORE_DIR, exist_ok=True)
    with open(ALERT_STATE, "w") as f:
        json.dump(s, f, indent=2, sort_keys=True)


def watch_alerts(store, cfg):
    """Return alert lines for areas whose latest CPUE spikes vs recent baseline.
    Gated by cfg['alerts']['enabled']; de-duped via a state file + cooldown so it never nags."""
    a = cfg.get("alerts", {})
    if not a.get("enabled"):
        return []
    dates = sampled_dates(store)
    if not dates:
        return []
    labels, slabel = area_labels(store, cfg), species_label(cfg)

    def totals(d):
        return area_totals(store[d], cfg)

    subs = [d for d in dates if sum(x["anglers"] for x in totals(d).values()) >= cfg["daily_min_anglers"]]
    latest = subs[-1] if subs else dates[-1]
    prior = [d for d in dates if d < latest]
    state = _load_alert_state()
    spike, min_ang = a.get("spike_mult", 1.8), a.get("min_anglers", 30)
    cooldown, min_base = a.get("cooldown_days", 2), a.get("min_baseline_days", 2)

    hits = []
    for code in cfg["areas"]:
        t = totals(latest).get(code)
        if not t or t["anglers"] < min_ang:
            continue
        cur = cpue(t["catch"], t["anglers"])
        bvals = [cpue(totals(d)[code]["catch"], totals(d)[code]["anglers"])
                 for d in prior if totals(d).get(code) and totals(d)[code]["anglers"] > 0]
        if len(bvals) < min_base:
            continue
        b = sum(bvals) / len(bvals)
        if not (b > 0 and cur >= b * spike and cur >= a.get("min_cpue", 0.4)):
            continue
        st = state.get(code)
        if st:
            since = (datetime.date.fromisoformat(latest) - datetime.date.fromisoformat(st["date"])).days
            if since < cooldown and cur <= st["value"] * 1.15:
                continue  # already alerted recently and not meaningfully hotter
        hits.append((code, cur, b, int(t["catch"]), int(t["anglers"])))
        state[code] = {"date": latest, "value": cur}

    if not hits:
        return []
    _save_alert_state(state)
    lines = [f"🔥 {slabel} hot-bite alert — {latest}"]
    for code, cur, b, catch, ang in hits:
        lines.append(f"• {labels[code]}: CPUE {cur:.2f} (vs {b:.2f} recent avg, {cur / b:.1f}×) "
                     f"— {catch} {slabel} / {ang} anglers")
    lines.append("Might be worth getting out while it's hot.")
    return lines


# ---------- weekly launch report ----------
def weekly_data(store, cfg):
    dates = sampled_dates(store)
    if not dates:
        return None
    latest = dates[-1]
    recent = window_dates(dates, latest, 7)
    prior_end = (datetime.date.fromisoformat(latest) - datetime.timedelta(days=7)).isoformat()
    prior = window_dates(dates, prior_end, 7)

    def agg(days, key):
        acc = {}
        for d in days:
            for r in store[d]:
                if r["area"] not in cfg["areas"]:
                    continue
                k = key(r)
                a = acc.setdefault(k, {"anglers": 0.0, "catch": 0.0, "days": set(), "area": r["area"]})
                a["anglers"] += r["anglers"]
                a["catch"] += target_catch(r, cfg)
                if r["anglers"] > 0:
                    a["days"].add(d)
        return acc

    rec_l = agg(recent, lambda r: (r["ramp"], r["area"]))
    pri_l = agg(prior, lambda r: (r["ramp"], r["area"]))
    launches = []
    for k, a in rec_l.items():
        if a["anglers"] < cfg["min_week_anglers"]:
            continue
        rc = cpue(a["catch"], a["anglers"])
        pa = pri_l.get(k)
        pc = cpue(pa["catch"], pa["anglers"]) if pa and pa["anglers"] > 0 else None
        wow = (rc - pc) if pc is not None else None
        score = rc + (max(wow, 0) if wow is not None else 0)
        launches.append({"ramp": k[0], "area": k[1], "cpue": rc, "wow": wow,
                         "catch": int(a["catch"]), "anglers": int(a["anglers"]),
                         "days": len(a["days"]), "score": score})
    launches.sort(key=lambda x: x["score"], reverse=True)

    rec_a = agg(recent, lambda r: r["area"])
    pri_a = agg(prior, lambda r: r["area"])
    area_agg = {}
    for code in cfg["areas"]:
        a = rec_a.get(code)
        if not a:
            area_agg[code] = None
            continue
        rc = cpue(a["catch"], a["anglers"])
        pa = pri_a.get(code)
        pc = cpue(pa["catch"], pa["anglers"]) if pa and pa["anglers"] > 0 else None
        area_agg[code] = {"anglers": int(a["anglers"]), "catch": int(a["catch"]),
                          "cpue": rc, "wow": (rc - pc) if pc is not None else None}

    rc_all = sum(rec_a[c]["catch"] for c in rec_a)
    ra_all = sum(rec_a[c]["anglers"] for c in rec_a)
    pc_all = sum(pri_a[c]["catch"] for c in pri_a)
    pa_all = sum(pri_a[c]["anglers"] for c in pri_a)
    overall = {"anglers": int(ra_all), "catch": int(rc_all), "cpue": cpue(rc_all, ra_all),
               "wow": (cpue(rc_all, ra_all) - cpue(pc_all, pa_all)) if pa_all > 0 else None}

    return launches, area_agg, {"latest": latest, "recent": recent, "prior": prior,
                                "overall": overall, "labels": area_labels(store, cfg)}


def weekly_text(store, cfg):
    data = weekly_data(store, cfg)
    if not data:
        return "No creel samples in the stored window yet."
    launches, area_agg, meta = data
    labels, slabel = meta["labels"], species_label(cfg)
    n = cfg["top_launches"]
    lines = [f"Puget Sound {slabel} — Launch Report ({meta['latest']})",
             f"Recent week: {meta['recent'][0]}..{meta['recent'][-1]} | "
             f"Areas {', '.join(cfg['areas'])} | {slabel}", ""]
    lines.append(f"TOP {n} LAUNCHES (hot bite + catch/angler):")
    if not launches:
        lines.append(f"  (No launch met the {cfg['min_week_anglers']}-angler/week sample floor.)")
    for i, x in enumerate(launches[:n], 1):
        wow = f"{x['wow']:+.2f} WoW" if x["wow"] is not None else "WoW n/a"
        dtxt = f"{x['days']} day" + ("s" if x["days"] != 1 else "")
        lines.append(f"  {i}. {x['ramp']} — {labels[x['area']]}")
        lines.append(f"       CPUE {x['cpue']:.2f} ({wow}) · "
                     f"{x['catch']} {slabel} / {x['anglers']} anglers over {dtxt}")
    lines.append("")
    lines.append("BY AREA (recent week, aggregated, best first):")
    for code in sorted(cfg["areas"],
                       key=lambda c: area_agg[c]["cpue"] if area_agg[c] else -1, reverse=True):
        a = area_agg[code]
        if not a:
            lines.append(f"  {labels[code]}: no samples")
            continue
        wow = f"{a['wow']:+.2f} WoW" if a["wow"] is not None else "WoW n/a"
        lines.append(f"  {labels[code]}: {a['anglers']} anglers, {a['catch']} {slabel} · "
                     f"CPUE {a['cpue']:.2f} ({wow})")
    o = meta["overall"]
    owow = f"{o['wow']:+.2f} WoW" if o["wow"] is not None else "WoW n/a"
    lines.append(f"  ALL AREAS (7-day avg): {o['anglers']} anglers, {o['catch']} {slabel} · "
                 f"CPUE {o['cpue']:.2f} ({owow})")
    return "\n".join(lines)


def make_cpue_chart(store, cfg, path=CHART_PNG):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import datetime as dt
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"chart skipped (matplotlib unavailable): {e}\n")
        return None
    dates = sampled_dates(store)
    if len(dates) < 2:
        return None
    labels, slabel = area_labels(store, cfg), species_label(cfg)
    totals_by_day = {d: area_totals(store[d], cfg) for d in dates}
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for i, code in enumerate(cfg["areas"]):
        # only this area's actual sample days, connected across gaps (no NaN breaks)
        pts = [(dt.date.fromisoformat(d), totals_by_day[d][code]["catch"] / totals_by_day[d][code]["anglers"])
               for d in dates
               if totals_by_day[d].get(code) and totals_by_day[d][code]["anglers"] > 0]
        if not pts:
            continue
        axs, ays = zip(*pts)
        ax.plot(axs, ays, marker="o", markersize=4, linewidth=2,
                color=PALETTE[i % len(PALETTE)], label=labels[code])
    ax.set_title(f"Puget Sound {slabel} — catch per angler by area")
    ax.set_ylabel(f"{slabel} per angler (CPUE)")
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.legend(fontsize=8, loc="upper left")
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def weekly_html(store, cfg, creds=None):
    data = weekly_data(store, cfg)
    if not data:
        return "<p>No creel samples in the stored window yet.</p>", "Puget Sound creel — no data"
    launches, area_agg, meta = data
    labels, slabel, n = meta["labels"], species_label(cfg), cfg["top_launches"]
    subject = f"Puget Sound {slabel} — Launch Report ({meta['latest']})"
    h = [f"<h2>🎣 {escape(subject)}</h2>",
         f"<p style='color:#555'>Recent week {meta['recent'][0]}–{meta['recent'][-1]} · "
         f"Areas {escape(', '.join(cfg['areas']))} · {escape(slabel)} · raw data, revised after QA/QC</p>",
         f"<h3>Top {n} launches — recommended</h3>"]
    if launches[:n]:
        h.append("<ol>")
        for x in launches[:n]:
            wow = f"{x['wow']:+.2f} WoW" if x["wow"] is not None else "WoW n/a"
            dtxt = f"{x['days']} day" + ("s" if x["days"] != 1 else "")
            h.append(f"<li><b>{escape(x['ramp'])}</b> — {escape(labels[x['area']])}<br>"
                     f"<span style='color:#0a6'>CPUE {x['cpue']:.2f}</span> ({wow}) · "
                     f"{x['catch']} {escape(slabel)} / {x['anglers']} anglers over {dtxt}</li>")
        h.append("</ol>")
    else:
        h.append(f"<p><i>No launch met the {cfg['min_week_anglers']}-angler/week sample floor.</i></p>")
    h.append("<h3>By area (recent week, aggregated)</h3>")
    h.append("<p style='color:#555;font-size:13px'><i>Catch/angler (a.k.a. CPUE, "
             "\"catch per unit effort\") is fish caught divided by number of anglers "
             "interviewed — a fair measure of how good the fishing is regardless of how "
             "many people showed up.</i></p>")
    h.append("<table cellpadding='6' style='border-collapse:collapse' border='1'>")
    h.append(f"<tr><th>Area</th><th>Anglers</th><th>{escape(slabel)}</th><th>Catch/angler</th><th>WoW</th></tr>")
    for code in sorted(cfg["areas"],
                       key=lambda c: area_agg[c]["cpue"] if area_agg[c] else -1, reverse=True):
        a = area_agg[code]
        if not a:
            h.append(f"<tr><td>{escape(labels[code])}</td><td colspan='4'>no samples</td></tr>")
            continue
        wow = f"{a['wow']:+.2f}" if a["wow"] is not None else "n/a"
        h.append(f"<tr><td>{escape(labels[code])}</td><td align='right'>{a['anglers']}</td>"
                 f"<td align='right'>{a['catch']}</td><td align='right'>{a['cpue']:.2f}</td>"
                 f"<td align='right'>{wow}</td></tr>")
    o = meta["overall"]
    owow = f"{o['wow']:+.2f}" if o["wow"] is not None else "n/a"
    h.append(f"<tr style='font-weight:bold;background:#f2f2f2'><td>All areas (7-day avg)</td>"
             f"<td align='right'>{o['anglers']}</td><td align='right'>{o['catch']}</td>"
             f"<td align='right'>{o['cpue']:.2f}</td><td align='right'>{owow}</td></tr>")
    h.append("</table>")
    h.append("<h3>Catch/angler by area (trend)</h3>")
    h.append("<img src='cid:cpuechart' alt='CPUE by area' "
             "style='max-width:100%;height:auto;border:1px solid #ddd'>")
    h.append("<p style='color:#888;font-size:12px'>Source: WDFW Puget Sound creel reports "
             "(HTML scrape). Auto-generated.</p>")
    if creds:
        footer = email_footer_html(creds)
        if footer:
            h.append(footer)
    return "\n".join(h), subject


# ---------- email ----------
def _addr_list(v):
    """Accept a string, comma-separated string, or list -> clean list of addresses."""
    if not v:
        return []
    if isinstance(v, str):
        v = v.split(",")
    return [a.strip() for a in v if a and a.strip()]


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")


def load_subscribers(url):
    """Fetch a published CSV (e.g. Google Form -> Sheet) and extract unique emails.
    Layout-agnostic: pulls every email-looking cell. Fails soft (returns [] on error)."""
    if not url:
        return []
    try:
        raw = fetch(url)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"list fetch failed ({url}), skipping: {e}\n")
        return []
    seen, out = set(), []
    for m in EMAIL_RE.finditer(raw):
        e = m.group(0)
        if e.lower() not in seen:
            seen.add(e.lower())
            out.append(e)
    return out


def load_mailerlite_subscribers(token, group_id):
    """Fetch active subscriber emails from a MailerLite group (paginated). Fails soft."""
    if not (token and group_id):
        return []
    emails, seen = [], set()
    url = f"https://connect.mailerlite.com/api/groups/{group_id}/subscribers?limit=100"
    try:
        while url:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}",
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode())
            for x in d.get("data", []):
                if x.get("status") == "active":
                    e = (x.get("email") or "").strip()
                    if e and e.lower() not in seen:
                        seen.add(e.lower())
                        emails.append(e)
            url = (d.get("links") or {}).get("next")
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"MailerLite group fetch failed: {e}\n")
        return []
    return emails


def load_brevo_list_subscribers(api_key, list_id):
    """Fetch non-blacklisted contact emails from a Brevo list (paginated). Fails soft."""
    if not (api_key and list_id):
        return []
    emails, seen, offset, limit = [], set(), 0, 500

    def _get(url, tries=6):
        last = None
        for _ in range(tries):
            try:
                req = urllib.request.Request(url, headers={"api-key": api_key, "accept": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    return json.loads(r.read().decode())
            except Exception as e:  # retry transient failures incl. rotating-IP 401s
                last = e
                time.sleep(1.5)
        raise last

    try:
        while True:
            url = (f"https://api.brevo.com/v3/contacts/lists/{list_id}/contacts"
                   f"?limit={limit}&offset={offset}")
            d = _get(url)
            batch = d.get("contacts", [])
            for x in batch:
                if x.get("emailBlacklisted"):
                    continue
                e = (x.get("email") or "").strip()
                if e and e.lower() not in seen:
                    seen.add(e.lower())
                    emails.append(e)
            if len(batch) < limit:
                break
            offset += limit
    except Exception as e:  # noqa: BLE001
        # hard failure: don't silently send to an empty list — signal the caller to abort
        raise RuntimeError(f"Brevo list fetch failed ({list_id}): {e}") from e
    return emails


def load_creds():
    if not os.path.exists(CREDS_FILE):
        raise RuntimeError(f"email creds file missing: {CREDS_FILE}")
    with open(CREDS_FILE) as f:
        return json.load(f)


def email_footer_html(creds):
    """Subscribe / unsubscribe links for the email footer (shown when configured)."""
    parts = []
    if creds.get("subscribe_form_url"):
        parts.append(f"<a href='{escape(creds['subscribe_form_url'])}'>Subscribe</a>")
    if creds.get("brevo_unsubscribe"):
        # Brevo replaces this tag per-recipient with a managed unsubscribe URL
        parts.append("<a href='{{ unsubscribe }}'>Unsubscribe</a>")
    elif creds.get("unsubscribe_form_url"):
        parts.append(f"<a href='{escape(creds['unsubscribe_form_url'])}'>Unsubscribe</a>")
    if not parts:
        return ""
    return ("<p style='color:#888;font-size:12px;margin-top:14px'>"
            "You're getting this because you signed up for the Puget Sound creel report. "
            + " · ".join(parts) + "</p>")


def resolve_recipients(c):
    """Build (to, cc, bcc): static lists + subscribers CSV, minus unsubscribes.
    Your own 'to' addresses are always kept, even if they appear on the unsubscribe list."""
    to = _addr_list(c.get("to"))
    cc = _addr_list(c.get("cc"))
    bcc = _addr_list(c.get("bcc"))
    # subscriber source priority: Brevo list -> MailerLite group -> Google Sheet CSV
    if c.get("brevo_api_key") and c.get("brevo_list_id"):
        subscribers = load_brevo_list_subscribers(c["brevo_api_key"], c["brevo_list_id"])
    elif c.get("mailerlite_api_token") and c.get("mailerlite_group_id"):
        subscribers = load_mailerlite_subscribers(c["mailerlite_api_token"], c["mailerlite_group_id"])
    else:
        subscribers = load_subscribers(c.get("subscribers_url"))
    unsub = {e.lower() for e in load_subscribers(c.get("unsubscribe_url"))}
    keep = {a.lower() for a in to}                 # owner addresses are never unsubscribed
    drop = unsub - keep

    cc = [e for e in cc if e.lower() not in drop]
    existing = {a.lower() for a in to + cc}
    merged_bcc = []
    for e in bcc + subscribers:
        k = e.lower()
        if k in existing or k in drop:
            continue
        existing.add(k)
        merged_bcc.append(e)
    return to, cc, merged_bcc


BATCH_SIZE = 75        # BCC recipients per message (keeps each under Gmail's ~100/msg cap)
DAILY_CAP = 290        # safety ceiling under Brevo free's 300/day limit
BATCH_PAUSE_SEC = 2    # small gap between messages


def _build_message(html, subject, creds, to, cc, bcc, image_path, text_body=None):
    c = creds
    addr = c.get("from", c["smtp_user"])
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((c.get("from_name", "Puget Sound Salmon Report"), addr))
    msg["Reply-To"] = addr
    if to:
        msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)  # send_message uses these then strips the header
    if not c.get("brevo_unsubscribe"):   # when Brevo manages unsubscribe, let it add the header
        unsub_link = c.get("unsubscribe_form_url") or c.get("unsubscribe_url")
        if unsub_link:
            msg["List-Unsubscribe"] = f"<{unsub_link}>"   # improves inbox placement
    # real plaintext alternative (mismatched/stub text is a spam signal)
    msg.set_content(text_body or "View this email in an HTML-capable client.")
    msg.add_alternative(html, subtype="html")
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img = f.read()
        msg.get_payload()[1].add_related(img, maintype="image", subtype="png", cid="<cpuechart>")
    return msg


def _plan_batches(to, cc, bcc, from_addr):
    """First message carries visible To/Cc + first BCC chunk; later messages are BCC-only."""
    chunks = [bcc[i:i + BATCH_SIZE] for i in range(0, len(bcc), BATCH_SIZE)] or [[]]
    batches = []
    for idx, chunk in enumerate(chunks):
        if idx == 0:
            batches.append((to or [from_addr], cc, chunk))
        else:
            batches.append(([from_addr], [], chunk))
    return batches


def send_email(html, subject, creds, image_path=None, override_to=None, dry_run=False,
               text_body=None):
    """Send the report, batching BCC to respect Gmail limits.
    override_to: send ONLY to this address (test mode, ignores the subscriber list).
    dry_run: print the batch plan and send nothing."""
    c = creds
    if override_to:
        to, cc, bcc = [override_to], [], []
    else:
        to, cc, bcc = resolve_recipients(c)
    if not (to or cc or bcc):
        raise RuntimeError("no recipients (set 'to', 'cc', 'bcc', or 'subscribers_url')")

    total = len(to) + len(cc) + len(bcc)
    if total > DAILY_CAP:
        raise RuntimeError(f"{total} recipients exceeds daily cap {DAILY_CAP}; "
                           "split the send or use an ESP.")
    from_addr = c.get("from", c["smtp_user"])
    batches = _plan_batches(to, cc, bcc, from_addr)

    if dry_run:
        for i, (t, cc2, b) in enumerate(batches, 1):
            print(f"  batch {i}: To={len(t)} Cc={len(cc2)} Bcc={len(b)}")
        print(f"DRY RUN: would send {len(batches)} message(s) to {total} recipient(s); no mail sent.")
        return total

    port = int(c.get("smtp_port", 465))
    host = c.get("smtp_host", "smtp.gmail.com")
    ctx = ssl.create_default_context()

    def _run(server):
        server.login(c["smtp_user"], c["smtp_pass"])
        for i, (t, cc2, b) in enumerate(batches):
            server.send_message(_build_message(html, subject, creds, t, cc2, b, image_path, text_body))
            if i < len(batches) - 1:
                time.sleep(BATCH_PAUSE_SEC)

    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=ctx, timeout=60) as s:
            _run(s)
    else:
        with smtplib.SMTP(host, port, timeout=60) as s:
            s.starttls(context=ctx)
            _run(s)
    return total


# ---------- main ----------
def main():
    args = sys.argv[1:]
    cfg = resolve_config(args)
    no_fetch = "--no-fetch" in args
    weekly = "--weekly" in args
    watch = "--watch" in args
    do_email = "--email" in args
    test_to = _flag_val(args, "--test")   # send only to this address (safe test)
    dry_run = "--dry-run" in args

    if cfg["until"] and datetime.date.today().isoformat() > cfg["until"]:
        print(f"Report window ended (after {cfg['until']}); nothing sent.")
        return

    os.makedirs(STORE_DIR, exist_ok=True)
    store = load_store()
    if not no_fetch:
        store.update(scrape_recent(cfg["trailing_days"]))
        save_store(store)

    if watch:
        msgs = watch_alerts(store, cfg)
        print("\n".join(msgs) if msgs else "NO_ALERT")
        return

    if weekly:
        text = weekly_text(store, cfg)
        with open(WEEKLY_MD, "w") as f:
            f.write(text + "\n")
        chart = make_cpue_chart(store, cfg)
        if do_email:
            creds = load_creds()
            html, subject = weekly_html(store, cfg, creds)
            nrec = send_email(html, subject, creds, image_path=chart,
                              override_to=test_to, dry_run=dry_run, text_body=text)
            if not dry_run:
                tag = f" (TEST → {test_to})" if test_to else ""
                print(f"Weekly {species_label(cfg)} report emailed to {nrec} recipient(s){tag}"
                      + (" with chart." if chart else " (chart unavailable)."))
        else:
            print(text)
            if chart:
                print(f"\nChart: {chart}")
    else:
        digest = daily_digest(store, cfg)
        with open(DIGEST_MD, "w") as f:
            f.write(digest + "\n")
        print(digest)


if __name__ == "__main__":
    main()
