#!/usr/bin/env python3
r"""check_html.py — static sanity checks for a trip-planner HTML output.

Usage:
    python3 check_html.py <output>.html
    py       check_html.py <output>.html      # Windows

Checks (each FAIL must be fixed before presenting the file):
  1. <div> balance            open vs close, and exactly one .page wrapper
  2. Leaflet + map wiring      leaflet.js/.css CDN present, a <div id="map">,
                               a TRIP object, and an OSM tile URL
  3. Map coordinates           every stop in TRIP has numeric lat & lng
  4. No leftover KaTeX math    the template descends from study-notes; stray
                               $$...$$ / KaTeX CDN means math snuck in
  5. Self-contained           no http(s) <img src> (images must be base64);
                               only leaflet/openstreetmap may be remote
  6. Travel components landed  >=3 .hotel cards (or an explicit
                               data-hotels="user-booked" marker), a .budget
                               table, and a .checklist wired to localStorage.
                               Step 5 being silently dropped is the skill's
                               most common real-run failure — this catches it.
  7. Mobile adaptation         a viewport meta tag AND a max-width media
                               query block (phones must not get the raw
                               desktop layout).
  8. Review provenance         a hotel card asserting a rating / 点评数 /
                               review verdict must carry a dated browse
                               provenance marker (实查于 YYYY-MM-DD) — catches
                               fabricated "4.8 · 3,201 条（已核）" cards.
  9. Price-compare honesty      a .cheapest ✓最低 row that is itself an
                               estimate, or a dead platform (去哪儿/美团/…)
                               used as a price source = fake comparison.
  10. Hotel price 2nd source   a priced hotel card must engage 飞猪 (or
                               Booking/Agoda) — 携程-only is single-source;
                               高德 is reviews-only and doesn't count.
  11. Weather not fabricated    the same specific per-day temperature
                               repeated across day cards (a forecast you
                               cannot have for dates >14 days out).

  NOTE: checks 8–10 are structural BACKSTOPS for the most common fabrication
  patterns, not a fabrication detector — a determined agent can still evade a
  regex. The load-bearing rule is the 数据诚信契约 in SKILL.md (verify-this-
  session or hedge-without-invented-specifics; 宁可不写, 绝不编).

Exit code: 0 = clean, 1 = one or more FAILs.  Pure standard library.
"""
import re
import sys


def line_of(text, pos):
    return text[:pos].count("\n") + 1


def strip_non_markup(html):
    """Remove <style>, <script>, and <!-- --> regions so their contents (CSS
    comments that mention `<div ...>`, JS that builds a `<div>` string, etc.)
    don't pollute the markup-level <div> balance count."""
    html = re.sub(r"<style\b[^>]*>.*?</style>", "", html, flags=re.S | re.I)
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    return html


def check_div_balance(html):
    markup = strip_non_markup(html)
    opens = len(re.findall(r"<div\b", markup))
    closes = len(re.findall(r"</div\s*>", markup))
    page = len(re.findall(r'<div\s+class="[^"]*\bpage\b', markup))
    return opens, closes, page


def check_leaflet(html):
    problems = []
    if "leaflet" not in html.lower():
        problems.append("Leaflet CDN not found (need leaflet.js + leaflet.css from unpkg/jsdelivr)")
    else:
        if not re.search(r"leaflet@[\d.]+/dist/leaflet\.js", html):
            problems.append("leaflet.js script tag not found")
        if not re.search(r"leaflet@[\d.]+/dist/leaflet\.css", html):
            problems.append("leaflet.css link tag not found")
    if not re.search(r'id\s*=\s*"map"', html):
        problems.append('no <div id="map"> container')
    if not re.search(r"\bvar\s+TRIP\s*=", html):
        problems.append("no `var TRIP = {...}` map-data object")
    if "tile.openstreetmap.org" not in html:
        problems.append("OSM tile URL (tile.openstreetmap.org) not found")
    return problems


# Pull out the TRIP = { ... }; object literal (best-effort brace matching).
def extract_trip(html):
    m = re.search(r"\bvar\s+TRIP\s*=\s*\{", html)
    if not m:
        return None
    i = m.end() - 1  # at the '{'
    depth, j = 0, i
    while j < len(html):
        c = html[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return html[i:j + 1]
        j += 1
    return None


def check_coords(html):
    """Every stop object that names a place should carry numeric lat & lng."""
    trip = extract_trip(html)
    problems = []
    if trip is None:
        return ["could not isolate the TRIP object to check coordinates"]
    stops = re.findall(r"\{[^{}]*\bname\s*:[^{}]*\}", trip)
    if not stops:
        problems.append("TRIP has no stop objects with a `name:` field")
        return problems
    for idx, s in enumerate(stops, 1):
        lat = re.search(r"\blat\s*:\s*(-?\d+(?:\.\d+)?)", s)
        lng = re.search(r"\blng\s*:\s*(-?\d+(?:\.\d+)?)", s)
        nm = re.search(r"name\s*:\s*['\"]([^'\"]*)", s)
        label = (nm.group(1) if nm else f"#{idx}")
        if not lat or not lng:
            problems.append(f"stop '{label}' is missing numeric lat/lng")
        else:
            la, lo = float(lat.group(1)), float(lng.group(1))
            if not (-90 <= la <= 90 and -180 <= lo <= 180):
                problems.append(f"stop '{label}' has out-of-range coords ({la}, {lo})")
    return problems


def check_no_katex(html):
    problems = []
    if "katex" in html.lower():
        problems.append("KaTeX reference found — remove it (trip-planner has no math)")
    # display-math delimiters that survived from the study-notes template
    dollars = [line_of(html, m.start()) for m in re.finditer(r"\$\$", html)]
    if dollars:
        problems.append(f"stray '$$' math delimiters at line(s) {', '.join(map(str, dollars[:20]))}")
    return problems


def check_travel_components(html):
    problems = []
    hotels = len(re.findall(r'class\s*=\s*"[^"]*\bhotel\b', html))
    user_booked = re.search(r'data-hotels\s*=\s*"user-booked"', html)
    if user_booked:
        pass  # deliberate omission: user already has accommodation
    elif hotels == 0:
        problems.append('住宿备选 missing: no .hotel cards and no data-hotels="user-booked" marker '
                        "— Step 5 was silently dropped")
    elif hotels < 3:
        problems.append(f"only {hotels} .hotel card(s) — Step 5 requires >=3 options (备选, not one)")
    if not re.search(r'class\s*=\s*"[^"]*\bbudget\b', html):
        problems.append("no .budget table found")
    if not re.search(r'class\s*=\s*"[^"]*\bchecklist\b', html):
        problems.append("no .checklist section found")
    elif "localStorage" not in html:
        problems.append(".checklist present but no localStorage persistence in the page")
    return problems


def check_mobile(html):
    problems = []
    if not re.search(r'<meta\s+name="viewport"', html):
        problems.append('no <meta name="viewport"> tag — phones will render the desktop layout zoomed out')
    m = re.search(r"@media\s*\(\s*max-width\s*:\s*6\d{2}px\s*\)\s*\{(.*?)\n\}", html, re.S)
    if not m:
        problems.append("no phone-breakpoint @media (max-width:6xxpx) block — page is not adapted "
                        "for narrow screens (the design system ships a canonical 640px block)")
    elif m.group(1).count("{") < 10:
        problems.append("the max-width @media block is too thin (<10 rules) — copy the full mobile "
                        "block from references/design-system.md")
    return problems


def check_self_contained(html):
    problems = []
    for m in re.finditer(r'<img\b[^>]*\bsrc\s*=\s*"(https?://[^"]+)"', html, re.I):
        problems.append(f"remote <img src> at line {line_of(html, m.start())}: "
                        f"{m.group(1)[:60]}… (inline as base64 instead)")
    return problems


# ── Fabrication backstops (structural; a determined fabricator can still evade —
#    the load-bearing fix is the 数据诚信契约 in SKILL.md; these catch the lazy
#    default path that fills rating/verdict fields without ever browsing). ──

def _hotel_cards(html):
    """Best-effort split into per-.hotel-card chunks (card start → next card start)."""
    starts = [m.start() for m in re.finditer(r'<div\s+class="hotel"', html)]
    if not starts:
        return []
    bounds = starts + [len(html)]
    return [html[bounds[i]:bounds[i + 1]] for i in range(len(starts))]


def check_review_provenance(html):
    """Inverted, NOT confession-gated: a hotel card that ASSERTS a rating, a
    review count, or a review-area verdict must carry a date-anchored browse
    provenance marker in the SAME card. Omitting the honesty token no longer
    disables detection — a no-browser card must simply not assert these."""
    problems = []
    # a numeric star rating in the .h-rating <b>, e.g. <b>4.8</b> / <b>约4.6</b>
    rating = re.compile(r'class="h-rating">[^<]*<b>\s*约?\s*[1-5]\.\d', re.I)
    count = re.compile(r'\d[\d,]+\s*条点评')
    verdict = re.compile(r'已核|可信|实测|分布正常|不像刷分|好评(具体|集中)|口碑稳|水军')
    # provenance must be date-anchored so a bare decoy word won't satisfy it
    prov = re.compile(r'实查于\s*\d{4}-\d{2}-\d{2}|浏览器实读[^。]{0,30}\d{4}-\d{2}-\d{2}'
                      r'|浏览器实查[^。]{0,30}\d{4}-\d{2}-\d{2}')
    for i, c in enumerate(_hotel_cards(html), 1):
        nm = re.search(r'class="h-name">([^<]*)', c)
        label = nm.group(1) if nm else f"#{i}"
        signal = rating.search(c) or count.search(c) or verdict.search(c)
        if signal and not prov.search(c):
            problems.append(f"hotel '{label}': asserts a rating/点评数/评论结论 but the card has no "
                            f"dated browse-provenance (实查于 YYYY-MM-DD / 浏览器实读…日期) — "
                            f"either browser-read it for real, or drop the number/verdict "
                            f"(写「评分以 App 为准」)")
    return problems


def check_fake_cheapest(html):
    """A price row tagged .cheapest (✓最低) that is itself an estimate (（估）/估价),
    or any defunct platform used as a hotel price row, is a fabricated comparison."""
    problems = []
    for m in re.finditer(r'class="pc-row[^"]*cheapest[^"]*"[^>]*>(.*?)</div>\s*(?=<div|</div)', html, re.S):
        if re.search(r'（估）|估价|≈|约¥', m.group(1)):
            problems.append("a .cheapest (最低) row is itself an estimate (（估）/约¥) — "
                            "you cannot crown a 最低 without real compared prices (fake comparison)")
            break
    for m in re.finditer(r'class="pc-plat">([^<]*)', html):
        if re.search(r'美团|去哪儿|同程|艺龙', m.group(1)):
            problems.append(f"defunct platform in a price row (.pc-plat: {m.group(1).strip()[:20]}) — "
                            f"去哪儿/美团/同程/艺龙 are dead (see platform truth table); never a price source")
            break
    return problems


def check_hotel_price_second_source(html):
    """Each hotel card that quotes a price must engage a SECOND price platform
    (飞猪 domestic, or Booking/Agoda international) — either a real price or an
    honest note (验证码墙/未读). 携程-only hotel pricing = single-source. 高德 is a
    REVIEW source (no room prices) and does NOT satisfy this. 成都-safe: all three
    成都 cards mention 飞猪 (two as a price, 如家 as a captcha-wall note)."""
    problems = []
    # 飞猪 must be ENGAGED: followed (within ~35 chars, tags stripped) by a real ¥
    # price OR a genuine-unavailability marker. A bare 飞猪-defer ("订前再比价 / 我未核")
    # does NOT count — that is exactly the lazy single-source skip this catches.
    engaged = re.compile(r'(飞猪|Booking|Agoda|缤客)[^¥]{0,35}?'
                         r'(¥|验证码|登录|拦截|滑块|人机|墙|未读|连不上|超时|售罄|无可比|查无)', re.I)
    for i, c in enumerate(_hotel_cards(html), 1):
        pc = c[c.find('price-compare'):] if 'price-compare' in c else ""
        if "¥" not in pc:
            continue  # no priced hotel row → nothing to cross-source
        text = re.sub(r'<[^>]+>', '', c)  # strip tags so the window is reliable
        if not engaged.search(text):
            nm = re.search(r'class="h-name">([^<]*)', c)
            label = nm.group(1) if nm else f"#{i}"
            problems.append(f"hotel '{label}': 携程-only price — 飞猪 is missing or only deferred to the "
                            f"user (\"订前再比价\"), not actually engaged. Query 飞猪 for a real ¥, or note a "
                            f"genuine wall (验证码/未读); 高德 has no room prices and doesn't count.")
    return problems


def check_duplicate_forecast(html):
    """The same specific slash-format temperature string repeated across day cards,
    with no 气候典型/非当日预报 qualifier, is a fabricated per-day forecast (you cannot
    know a specific daily temp for dates outside the ~14-day window)."""
    problems = []
    temps = re.findall(r'约?\s*\d{2}\s*°\s*/\s*\d{2}\s*°', html)
    for t in set(temps):
        if temps.count(t) >= 2:
            # exempt only if every occurrence is qualified as climatology
            occ = [m.start() for m in re.finditer(re.escape(t), html)]
            if not all(re.search(r'气候典型|非当日预报|典型', html[max(0, p - 4):p + 40]) for p in occ):
                problems.append(f"temperature '{t.strip()}' repeated on {temps.count(t)} day-cards with no "
                                f"「气候典型/非当日预报」 qualifier — looks like a fabricated forecast, "
                                f"not per-day data (use a range or label it climatology)")
    return problems


def run(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"FAIL: file not found: {path}")
        return False

    fails = 0
    print(f"=== checking {path} ({len(html)} chars) ===")

    opens, closes, page = check_div_balance(html)
    if opens != closes:
        fails += 1
        print(f"[FAIL] <div> imbalance: {opens} '<div>' vs {closes} '</div>' (diff {opens - closes:+d})")
    else:
        print(f"[ok]  <div> balanced ({opens} open / {closes} close)")
    if page != 1:
        print(f"[warn] found {page} '.page' wrappers (expected exactly 1)")

    for label, probs in [
        ("Leaflet/map wiring", check_leaflet(html)),
        ("map coordinates", check_coords(html)),
        ("no leftover KaTeX", check_no_katex(html)),
        ("self-contained", check_self_contained(html)),
        ("travel components (hotel/budget/checklist)", check_travel_components(html)),
        ("mobile adaptation (viewport + media query)", check_mobile(html)),
        ("hotel review provenance (no fabricated ratings/verdicts)", check_review_provenance(html)),
        ("price comparison honesty (no fake 最低 / dead platforms)", check_fake_cheapest(html)),
        ("hotel price second source (飞猪, not just 携程)", check_hotel_price_second_source(html)),
        ("weather not fabricated (no repeated per-day forecast)", check_duplicate_forecast(html)),
    ]:
        if probs:
            fails += 1
            print(f"[FAIL] {label}:")
            for p in probs[:30]:
                print(f"        - {p}")
            if len(probs) > 30:
                print(f"        … and {len(probs) - 30} more")
        else:
            print(f"[ok]  {label}")

    print()
    if fails:
        print(f"RESULT: {fails} FAIL-level check(s). Fix and re-run.")
        return False
    print("RESULT: all checks passed.")
    return True


def main():
    # The output mixes Chinese + symbols; force UTF-8 so a GBK Windows console
    # doesn't crash on chars like ° or — mid-report.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    if len(sys.argv) != 2:
        sys.exit("usage: python3 check_html.py <output>.html")
    sys.exit(0 if run(sys.argv[1]) else 1)


if __name__ == "__main__":
    main()
