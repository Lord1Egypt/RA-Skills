#!/usr/bin/env python3
"""Regression tests for scripts/fetch_plan_imagery.py and scripts/plan_visuals.py.

Network-free by construction: every case here exercises the decision logic, which is where all
four of this feature's real defects lived. Whether Wikipedia is reachable is not something a test
suite should assert, but whether a photograph is allowed onto the page is, and that is decided
entirely offline.

The rule these tests defend is that the feature fails CLOSED. A page with three good photographs
and two gaps is honest; a page with five photographs where two are wrong teaches the traveller
that none of the pictures mean anything, and that is worse than the text-only page it replaced.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

# A real 1x1 PNG. The renderer only asks whether `data_uri` is truthy, but a payload that is not
# actually an image is a fixture that would keep passing after the renderer started decoding one.
PIXEL = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
         "z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def photo(label: str, page: str) -> dict:
    """One imagery slot, shaped the way fetch_plan_imagery.py writes it."""
    return {"label": label, "page": page, "page_url": f"https://en.wikipedia.org/wiki/{page}",
            "file": f"{page}.png", "file_url": f"https://commons.wikimedia.org/wiki/File:{page}.png",
            "license": "CC BY-SA 4.0", "artist": "A Photographer", "bytes": 68,
            "data_uri": PIXEL}


def run_fetch(module, plan_path: Path, verified: dict, *args: str) -> tuple[int, str]:
    """fetch_plan_imagery.main() with the network step replaced by a fixed result.

    In-process and stubbed at fetch(), because what is under test is the decision main() makes
    AFTER a run comes back -- whether the file on disk is replaced or merged. Driving it through
    the CLI would make every case depend on Wikipedia being reachable, and the interesting result
    is the one where it is NOT: eight of eight concurrent lookups returning HTTP 429 is a measured
    figure in the module's own MAX_CONCURRENCY note, and one slot resolving out of seven is what
    that looks like from here.
    """
    original_fetch, original_argv = module.fetch, sys.argv
    buffer = io.StringIO()
    try:
        module.fetch = lambda plan, limit, dry_run=False: (dict(verified), [])
        sys.argv = ["fetch_plan_imagery.py", str(plan_path), *args]
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            code = module.main()
    finally:
        module.fetch, sys.argv = original_fetch, original_argv
    return code, buffer.getvalue()


def render_page(plan_path: Path) -> tuple[int, str]:
    """Render through the CLI, because the sidecar is found by main() and not by render().

    Calling render(plan) directly would test the templating and skip the entire mechanism under
    test -- which is exactly how a plan could stop finding its photographs while every test that
    imports render() stayed green.
    """
    out = plan_path.with_suffix(".html")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render_final_trip_html.py"),
         str(plan_path), str(out)],
        capture_output=True, text=True)
    if result.returncode != 0:
        return result.returncode, result.stdout + result.stderr
    return 0, out.read_text(encoding="utf-8")


def main() -> int:
    imagery = load("fetch_plan_imagery")
    visuals = load("plan_visuals")
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    # --- what may be labelled as what ----------------------------------------------------
    # Measured against the live API while building this: "Alicante Central Market" matched the
    # article *Bombing of Alicante*. Its coordinate is 400 m away so every proximity rule passes,
    # and its lead image really is the market -- but the provenance would have been printed under
    # the photograph on somebody's holiday itinerary.
    check("an article near the place but not about it is refused",
          not imagery._relevant("Alicante Central Market", "Bombing of Alicante", "Alicante"), "")
    check("an article about the thing asked for is accepted",
          imagery._relevant("Castillo de Santa Bárbara", "Santa Bàrbara Castle", "Alicante"), "")

    # The destination's own photo has no narrower subject, so the rule inverts: the article must
    # be about the place and may introduce nothing new. Without this the search for 阿利坎特
    # returned 阿利坎特-埃爾切機場 -- the airport, sharing the city's name, four kilometres out --
    # and it would have opened the page.
    check("the destination hero accepts the place's own article",
          imagery._relevant("阿利坎特", "阿利坎特", "阿利坎特（西班牙，瓦伦西亚自治区）"), "")
    check("the destination hero refuses something merely located there",
          not imagery._relevant("阿利坎特", "阿利坎特-埃爾切機場",
                                "阿利坎特（西班牙，瓦伦西亚自治区）"), "")

    # --- the fall-through guard, across scripts and past the stopword list ----------------
    # Forms are built here rather than by destination_forms(), which asks Wikipedia for the
    # Latin title; the rule itself is what this file is allowed to assert.
    zh_forms = [imagery._tokens_raw("拉纳卡"), imagery._tokens_raw("Larnaca")]
    en_forms = [imagery._tokens_raw("Chengdu")]
    # Measured on a delivered zh plan: the anchor 拉纳卡市政市场 has no article of its own, fell
    # through to *Larnaca*, and was captioned with a photograph of the Finikoudes promenade --
    # a different place, under the market's heading. The guard existed and could not fire,
    # because a Latin title is never a subset of a Chinese one.
    check("a zh plan refuses its own destination article",
          imagery.is_destination_article("Larnaca", zh_forms), "")
    check("a zh plan refuses the destination article in its own script",
          imagery.is_destination_article("拉纳卡", zh_forms), "")
    # And the repair must not swallow real articles. `castle`, `church`, `museum`, `market` and
    # `beach` are all stopwords, so a stopword-stripped comparison collapses every "<City> <Type>"
    # article to the bare city and drops its photograph -- which it did, to Larnaca Castle.
    for title in ("Larnaca Castle", "Larnaca Salt Lake", "Larnaca Municipal Market"):
        check(f"'{title}' is its own subject, not the destination",
              not imagery.is_destination_article(title, zh_forms), "")
    check("an en plan still refuses its own destination article",
          imagery.is_destination_article("Chengdu", en_forms), "")
    check("an en plan keeps a '<City> <Type>' article",
          not imagery.is_destination_article("Chengdu Museum", en_forms), "")
    check("an empty title is not treated as a fall-through",
          not imagery.is_destination_article("", zh_forms), "")

    # The forms themselves, with the one network call stubbed. Asserting the guard while
    # hand-building its input tests the consumer and leaves the producer uncovered -- and the
    # producer is where the fix lives: without the Latin form the guard cannot fire on a zh plan
    # at all. Verified by mutation: deleting the latin_title branch keeps every check above green.
    original_latin_title = imagery.latin_title
    try:
        imagery.latin_title = lambda title, lang: "Larnaca" if title == "拉纳卡" else None
        forms = imagery.destination_forms("拉纳卡")
        check("destination_forms yields the plan's script and the Latin one",
              {"拉纳卡"} in forms and {"larnaca"} in forms, repr(forms))
        check("the guard fires on a Latin article through the real forms",
              imagery.is_destination_article("Larnaca", forms), repr(forms))
        check("...and still spares a '<City> <Type>' article",
              not imagery.is_destination_article("Larnaca Castle", forms), repr(forms))
        imagery.latin_title = lambda title, lang: None
        offline = imagery.destination_forms("拉纳卡")
        check("an unreachable Wikipedia degrades to one form instead of raising",
              offline == [{"拉纳卡"}], repr(offline))
        check("a destination that is only whitespace yields no forms at all",
              imagery.destination_forms("   ") == [], "")
    finally:
        imagery.latin_title = original_latin_title

    # --- what may open the page ----------------------------------------------------------
    # A hero is a photograph OF a place. "Larnaca 01-2017 img37 LCA Airport.jpg" names the city
    # first, passes the position rule, and was selected as a real trip's cover photograph.
    larnaca = imagery._tokens("Larnaca")
    alicante = imagery._tokens("Alicante")
    check("a hero refuses a terminal that names the city first",
          not imagery.file_names_the_subject("Larnaca 01-2017 img37 LCA Airport.jpg",
                                             larnaca, is_hero=True), "")
    check("a hero refuses a single monument",
          not imagery.file_names_the_subject("Larnaca 01-2017 img01 Larnaca Fort.jpg",
                                             larnaca, is_hero=True), "")
    # The repair must stay narrower than "no other word may appear". That version rejected the
    # España case below too, which turns the Quality-image upgrade off for every destination and
    # silently returns the feature to the plain lead images it was built to replace.
    check("a hero still accepts a country-qualified view of the place",
          imagery.file_names_the_subject("Vista de Alicante, España, 2014-07-04, DD 49.JPG",
                                         alicante, is_hero=True), "")
    check("a hero accepts a named quarter of the place",
          imagery.file_names_the_subject("Larnaca 01-2017 img14 Finikoudes.jpg",
                                         larnaca, is_hero=True), "")
    # An anchor's subject IS a facility, so the same file is fine under a fort's own heading.
    check("an anchor accepts the facility a hero refused",
          imagery.file_names_the_subject("Larnaca 01-2017 img01 Larnaca Fort.jpg",
                                         imagery._tokens("Larnaca Castle"), is_hero=False), "")
    check("position still separates a church one town over",
          not imagery.file_names_the_subject("Iglesia de San Miguel Arcángel, Altea, Alicante.jpg",
                                             alicante, is_hero=False), "")

    # --- names a human wrote, made searchable -------------------------------------------
    # Plans name places for a reader: "圣巴巴拉城堡（Castillo de Santa Bárbara）". Searching that
    # whole string finds nothing in any Wikipedia, which is why the first real run verified zero
    # images while the same five places resolved perfectly from their bracketed names.
    variants = imagery.name_variants("圣巴巴拉城堡（Castillo de Santa Bárbara）")
    check("the local name inside brackets is tried",
          "Castillo de Santa Bárbara" in variants, str(variants))
    check("the traveller-facing name is tried too", "圣巴巴拉城堡" in variants, str(variants))
    # A bracket holding a region is context, not an alias, and searching for it would match the
    # region rather than the city.
    region = imagery.name_variants("阿利坎特（西班牙，瓦伦西亚自治区）")
    check("a bracketed region is not treated as an alias",
          "西班牙，瓦伦西亚自治区" not in region, str(region))
    check("the bare place name survives", "阿利坎特" in region, str(region))

    check("a Chinese plan asks the Chinese Wikipedia first",
          imagery.wiki_languages("Chinese")[0] == "zh", "")
    check("European languages are tried as a fallback",
          "es" in imagery.wiki_languages("English"), "")

    # --- the download step -----------------------------------------------------------------
    # Wikimedia appends analytics parameters to thumbnail URLs, so splitting the whole string on
    # its last dot yielded "org&utm_campaign=imageinfo&utm_content=thumbnail" instead of "jpg".
    # Every download succeeded, every file was inside the size cap, and all five were discarded as
    # an unsupported format -- the dry run reported five photographs and the real run wrote none.
    import urllib.parse  # noqa: PLC0415
    thumb = ("https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/X.jpg/800px-X.jpg"
             "?utm_source=en.wikipedia.org&utm_campaign=imageinfo&utm_content=thumbnail")
    path = urllib.parse.urlparse(thumb).path
    check("the format is read from the path, not the query string",
          path.rsplit(".", 1)[-1].casefold() == "jpg", path)

    # --- figures degrade to nothing, never to a lie ---------------------------------------
    check("a day with no coordinates draws no map",
          visuals.day_map({"stops_in_order": ["A", "B"], "segments": []}, "t", "c") == "", "")
    check("an empty walking series draws no chart", visuals.walking_bars([], 30, "t", "c", "l") == "", "")
    check("a zero budget draws no bar", visuals.budget_bar([("flight", 10)], 0, None, "t", "c") == "", "")
    check("a day with no clock times draws no timeline",
          visuals.day_timeline([("act", None, "Flexible")], "t", "c") == "", "")

    # Coordinates come out of the map URLs, in each provider's own dialect. Reading one as the
    # other moves a point thousands of kilometres and would draw a meaningless scatter -- silently,
    # because a wrong map renders exactly as well as a right one.
    google = {"stops_in_order": ["A", "B"], "segments": [{
        "verified_map_url": "https://www.google.com/maps/dir/?api=1&origin=38.345200%2C-0.481500"
                            "&destination=38.348100%2C-0.486100&travelmode=transit"}]}
    points = visuals.stop_coordinates(google)
    check("a Google URL reads as lat,lon",
          len(points) == 2 and abs(points[0][1] - 38.3452) < 1e-4
          and abs(points[0][2] + 0.4815) < 1e-4, str(points))
    # The first version split on the character class [,%2C], which also matches inside a number:
    # 38.345200 became 38.345 and 00, so every longitude came out 0.0.
    check("a coordinate containing the digit 2 is not split apart",
          points and abs(points[0][2]) > 0.1, str(points))

    amap = {"stops_in_order": ["A", "B"], "segments": [{
        "verified_map_url": "https://uri.amap.com/navigation?from=116.4470,39.9510,Hotel"
                            "&to=116.4030,39.9240,Park&mode=bus"}]}
    points = visuals.stop_coordinates(amap)
    check("an Amap URL reads as lon,lat",
          len(points) == 2 and abs(points[0][1] - 39.9510) < 1e-4
          and abs(points[0][2] - 116.4470) < 1e-4, str(points))

    # --- generalization: everything above was built against one Spanish coastal city ---------
    # A day that crosses the 180th meridian put two stops 215 km apart at opposite ends of a
    # 320px drawing, because longitude was interpolated raw. The distance caption stayed correct
    # -- haversine does not care -- so the map rendered perfectly and was inside out. Fiji,
    # Kiribati, Chukotka and the Chatham Islands all live there.
    import re as _re  # noqa: PLC0415

    def x_positions(points: list[tuple[float, float]]) -> list[float]:
        segments = [{"verified_map_url":
                     f"https://www.google.com/maps/dir/?api=1&origin={a[0]},{a[1]}"
                     f"&destination={b[0]},{b[1]}&travelmode=transit"}
                    for a, b in zip(points, points[1:])]
        drawing = visuals.day_map(
            {"stops_in_order": [f"S{i}" for i in range(len(points))], "segments": segments},
            "t", "c")
        return [float(m) for m in _re.findall(r'<circle cx="([\d.]+)"', drawing)]

    across = x_positions([(-17.7134, 178.0650), (-17.7500, -179.9000), (-17.7300, 179.9500)])
    check("a day crossing the antimeridian is not drawn inside out",
          len(across) == 3 and abs(across[0] - across[1]) > abs(across[1] - across[2]),
          f"215 km apart drew closer than 27 km apart: {across}")

    # The southern hemisphere, the equator and 69°N are all ordinary cases the one test city
    # never exercised.
    for label, points in (("equator", [(-0.18, -78.47), (-0.22, -78.51)]),
                          ("69 north", [(69.6492, 18.9553), (69.6800, 18.9900)]),
                          ("southern", [(-41.2866, 174.7756), (-41.2924, 174.7787)])):
        check(f"a day at {label} still draws", len(x_positions(points)) == 2, label)

    # A single stop has no segment, so no coordinates, so no map -- rather than a figure with one
    # dot and an invented scale.
    check("a one-stop day draws nothing",
          visuals.day_map({"stops_in_order": ["A"], "segments": []}, "t", "c") == "", "")

    # Names arrive in whatever scripts the traveller and the destination use.
    for name, expected in (
            ("サンタバルバラ城（Castillo de Santa Bárbara）", "Castillo de Santa Bárbara"),
            ("Санкт-Петербург (Saint Petersburg)", "Saint Petersburg"),
            ("Castillo de Santa Bárbara (Santa Bàrbara Castle)", "Santa Bàrbara Castle")):
        check(f"the bracketed local name is extracted from {name[:12]}",
              expected in imagery.name_variants(name), str(imagery.name_variants(name)))

    # Rows are unpacked defensively: a malformed row must cost a figure, never a traceback.
    for builder, argument in ((visuals.walking_bars, [None]),
                              (visuals.budget_bar, [None]),
                              (visuals.day_timeline, [None])):
        try:
            builder(argument, *(([30, "t", "c", "l"]) if builder is visuals.walking_bars
                                else ([1, None, "t", "c"]) if builder is visuals.budget_bar
                                else (["t", "c"])))
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{builder.__name__} raised on a malformed row: {exc}")

    # --- the sidecar: where the photographs live, and what happens when they are not there ----
    # This script used to write the base64 INTO the plan, in place and non-atomically. Measured
    # on a delivered plan: 2,047,677 of its 2,132,252 bytes were plan["imagery"] -- 96% of the one
    # file SKILL.md schedules this run against during the verification stage, that
    # references/verification.md hands to seven parallel agents, and that the gate loop sends the
    # reader back to after every finding. One read of it costs ~576k tokens instead of ~42k.
    #
    # The split is only safe if losing the payload is LOUD, and nothing else in this repo would
    # notice: `imagery` appears zero times in check_plan_consistency.py and validate_trip_html.py,
    # no gate counts <img> tags, and a page with no photographs is structurally valid. So these
    # cases assert two things -- the rendered page is unchanged by where the bytes live, and every
    # way of losing them exits non-zero naming the path.
    Sidecar = imagery.ImagerySidecarError

    def raises(name: str, call, expect: str) -> None:
        try:
            call()
        except Sidecar as exc:
            check(name, expect in str(exc), f"message did not mention {expect!r}: {exc}")
        except Exception as exc:  # noqa: BLE001
            check(name, False, f"raised {type(exc).__name__} instead of ImagerySidecarError: {exc}")
        else:
            check(name, False, "returned instead of raising -- a lost payload was made silent")

    check("the sidecar is named after the plan, beside the plan",
          imagery.sidecar_path_for(Path("/w/plans/2026-11-16-larnaca.json"))
          == Path("/w/plans/2026-11-16-larnaca-imagery.json"), "")
    # The workspace names plans in the traveller's language, so a CJK stem is the normal case
    # rather than the exotic one -- five of the eleven plans in a real workspace are CJK.
    check("a CJK plan name yields a CJK sidecar name",
          imagery.sidecar_path_for(Path("/w/plans/2026-11-16-拉纳卡-5-天.json")).name
          == "2026-11-16-拉纳卡-5-天-imagery.json", "")
    # A plan read from standard input has no directory to sit beside, and Path("-").stem would
    # quietly invent "--imagery.json" in whatever directory the command happened to run from.
    raises("a plan on standard input refuses to name a sidecar",
           lambda: imagery.sidecar_path_for("-"), "standard input")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload = {"hero": photo("Chengdu", "Chengdu"),
                   "anchor:0": photo("Central-city rhythm", "Jinli")}

        # 1. The page must not be able to tell where the bytes came from.
        inline_path = tmp / "inline.json"
        inline_path.write_text(json.dumps({**fixture, "imagery": payload}, ensure_ascii=False),
                               encoding="utf-8")
        split_path = tmp / "split.json"
        split_path.write_text(
            json.dumps({**fixture, "imagery_sidecar": "split-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        (tmp / "split-imagery.json").write_text(json.dumps(payload, ensure_ascii=False),
                                                encoding="utf-8")
        inline_code, inline_html = render_page(inline_path)
        split_code, split_html = render_page(split_path)
        check("the inline shape still renders", inline_code == 0, inline_html)
        check("the sidecar shape renders", split_code == 0, split_html)
        # Two images, not "some": a count that could be zero would pass this comparison while the
        # feature was entirely dead.
        check("both shapes render the same photographs",
              inline_code == split_code == 0
              and inline_html.count("<img") == split_html.count("<img") == 2,
              f"inline={inline_html.count('<img')} split={split_html.count('<img')}")
        check("the pages are byte-identical, not merely equal in count",
              inline_code == split_code == 0 and inline_html == split_html, "")
        check("the split plan carries no image bytes at all",
              PIXEL in inline_path.read_text(encoding="utf-8")
              and "base64" not in split_path.read_text(encoding="utf-8"), "")
        # The size claim, on a payload the size of a real one. The fixture's own photographs are
        # one-pixel PNGs, so a plan carrying them is small either way and would let this pass
        # while the defect was untouched. A real hero alone is ~880KB of base64.
        heavy = {"hero": {**photo("Chengdu", "Chengdu"),
                          "data_uri": "data:image/png;base64," + "A" * 880_000}}
        heavy_inline = tmp / "heavy-inline.json"
        heavy_inline.write_text(json.dumps({**fixture, "imagery": heavy}, ensure_ascii=False),
                                encoding="utf-8")
        heavy_split = tmp / "heavy-split.json"
        heavy_split.write_text(
            json.dumps({**fixture, "imagery_sidecar": "heavy-split-imagery.json"},
                       ensure_ascii=False), encoding="utf-8")
        (tmp / "heavy-split-imagery.json").write_text(json.dumps(heavy), encoding="utf-8")
        check("moving the bytes out shrinks the plan a reader has to load",
              heavy_split.stat().st_size * 10 < heavy_inline.stat().st_size,
              f"inline={heavy_inline.stat().st_size} split={heavy_split.stat().st_size}")
        heavy_code, heavy_html = render_page(heavy_split)
        check("and the heavy payload still reaches the page from its sidecar",
              heavy_code == 0 and heavy_html.count("<img") == 1, heavy_html[:400])

        # 2. Found by name with no key at all -- a plan copied by hand, or rewritten by a tool
        #    that did not know about imagery_sidecar, still finds its photographs.
        found_path = tmp / "found.json"
        found_path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        (tmp / "found-imagery.json").write_text(json.dumps(payload, ensure_ascii=False),
                                                encoding="utf-8")
        found_code, found_html = render_page(found_path)
        check("a sidecar beside the plan is found with no key naming it",
              found_code == 0 and found_html.count("<img") == 2, found_html[:400])

        # 3. A plan that genuinely has no photographs is still a plan.
        bare_path = tmp / "bare.json"
        bare_path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        bare_code, bare_html = render_page(bare_path)
        check("a plan with no imagery anywhere renders without photographs",
              bare_code == 0 and bare_html.count("<img") == 0, bare_html[:400])

        # 4. Every way of losing the payload, through the CLI a person actually runs.
        gone_path = tmp / "gone.json"
        gone_path.write_text(
            json.dumps({**fixture, "imagery_sidecar": "not-here-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        gone_code, gone_out = render_page(gone_path)
        check("a plan naming a sidecar that is not there refuses to render",
              gone_code != 0 and "not-here-imagery.json" in gone_out and "Traceback" not in gone_out,
              gone_out[:600])

        torn_path = tmp / "torn.json"
        torn_path.write_text(
            json.dumps({**fixture, "imagery_sidecar": "torn-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        (tmp / "torn-imagery.json").write_text("{not json", encoding="utf-8")
        torn_code, torn_out = render_page(torn_path)
        check("a sidecar that will not parse refuses to render",
              torn_code != 0 and "torn-imagery.json" in torn_out and "Traceback" not in torn_out,
              torn_out[:600])

        # 5. The resolver's own contract, where the shapes are easier to state than through a CLI.
        resolve = imagery.resolve_plan_imagery
        merged, source = resolve({"imagery": payload}, str(bare_path))
        check("an inline payload with no sidecar is returned as it is",
              merged == payload and source is None, repr(source))
        merged, source = resolve({"imagery_sidecar": "split-imagery.json"}, str(split_path))
        check("a sidecar payload is returned and its path reported",
              merged == payload and source == tmp / "split-imagery.json", repr(source))
        # Precedence, on a plan carrying both: the sidecar is the payload written most recently
        # and by the only script that verifies provenance, so it wins per key -- while an inline
        # slot the sidecar does not mention survives rather than being dropped.
        legacy = {"hero": photo("Old hero", "Old"), "anchor:9": photo("Only inline", "Solo")}
        merged, _ = resolve({"imagery": legacy, "imagery_sidecar": "split-imagery.json"},
                            str(split_path))
        check("the sidecar wins per key and inline-only slots survive",
              merged["hero"] == payload["hero"] and merged["anchor:9"] == legacy["anchor:9"]
              and merged["anchor:0"] == payload["anchor:0"], repr(sorted(merged)))
        check("resolving does not mutate the plan it was handed",
              resolve({"imagery": dict(payload)}, str(bare_path))[0] is not payload, "")

        raises("a key naming nothing refuses",
               lambda: resolve({"imagery_sidecar": "   "}, str(bare_path)), "names no file")
        raises("a non-string key refuses",
               lambda: resolve({"imagery_sidecar": 12}, str(bare_path)), "names no file")
        # The renderer tolerates a non-dict by drawing nothing, which is how a broken writer
        # upstream would stay invisible until somebody compared the page against the plan.
        raises("an inline imagery that is not an object refuses",
               lambda: resolve({"imagery": ["a list"]}, str(bare_path)), "not an object")
        (tmp / "list-imagery.json").write_text("[1, 2]", encoding="utf-8")
        raises("a sidecar holding a list refuses",
               lambda: resolve({"imagery_sidecar": "list-imagery.json"}, str(bare_path)),
               "not an object")

        # 6. A plan is a portable document: the pair must survive being moved together, which is
        #    the whole reason the key is relative rather than absolute.
        moved = tmp / "moved"
        moved.mkdir()
        (moved / "split.json").write_text(split_path.read_text(encoding="utf-8"), encoding="utf-8")
        (moved / "split-imagery.json").write_text(
            (tmp / "split-imagery.json").read_text(encoding="utf-8"), encoding="utf-8")
        moved_code, moved_html = render_page(moved / "split.json")
        check("a moved plan still finds the sidecar moved with it",
              moved_code == 0 and moved_html.count("<img") == 2, moved_html[:400])

        # 7. The aggregate ceiling, which nothing enforced before: every earlier cap is per image.
        cap = imagery.MAX_IMAGERY_TOTAL_BYTES
        check("a payload at the ceiling is accepted",
              imagery.aggregate_refusal(cap, "x") is None, "")
        over = imagery.aggregate_refusal(cap + 1, "the imagery sidecar /w/p-imagery.json")
        check("one byte over is refused, and the message names the figure and the file",
              over is not None and f"{cap + 1:,}" in over and "/w/p-imagery.json" in over,
              repr(over))
        # Enforced on the payload as it sits on disk, before it is parsed into memory.
        huge_path = tmp / "huge.json"
        huge_path.write_text(
            json.dumps({**fixture, "imagery_sidecar": "huge-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        (tmp / "huge-imagery.json").write_text(
            json.dumps({"hero": {**photo("x", "X"), "data_uri": "d" * (cap + 10)}}),
            encoding="utf-8")
        huge_code, huge_out = render_page(huge_path)
        check("an over-ceiling sidecar refuses to render rather than loading it",
              huge_code != 0 and "ceiling" in huge_out and "Traceback" not in huge_out,
              huge_out[:400])

        # 8. Atomic writes. The version this replaced was Path.write_text, which truncates first
        #    and writes after -- and SKILL.md schedules this script while seven verification
        #    agents hold the same plan path. Measured here with a 400KB payload, 40 rewrites and
        #    one concurrent reader: the naive write produced 31 torn reads, os.replace produces
        #    none. A reader seeing a prefix of a plan reports a JSONDecodeError on a file that is
        #    valid a millisecond later, which is the shape of a bug nobody reproduces.
        target = tmp / "atomic.json"
        blob = {"hero": {"data_uri": "A" * 400_000}}
        imagery.write_json_atomic(target, blob)
        torn_reads = [0]
        stop = threading.Event()

        def reader() -> None:
            while not stop.is_set():
                try:
                    json.loads(target.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    torn_reads[0] += 1

        watcher = threading.Thread(target=reader)
        watcher.start()
        try:
            for _ in range(40):
                imagery.write_json_atomic(target, blob)
        finally:
            stop.set()
            watcher.join()
        check("a concurrent reader never sees a half-written plan",
              torn_reads[0] == 0, f"{torn_reads[0]} torn read(s)")
        check("the atomic write leaves no temporary file behind",
              sorted(p.name for p in tmp.glob("*atomic*")) == ["atomic.json"],
              repr(sorted(p.name for p in tmp.glob(".*"))))
        check("the atomic write actually wrote the payload",
              json.loads(target.read_text(encoding="utf-8")) == blob, "")
        # It must also create the directory it was pointed at: save_trip_deliverables.py writes a
        # sidecar into a workspace that may not exist yet.
        imagery.write_json_atomic(tmp / "new" / "deep" / "s.json", {"ok": True})
        check("the atomic write creates the directory it needs",
              (tmp / "new" / "deep" / "s.json").is_file(), "")

        # 9. A re-run may ADD what it verified. It may never DELETE what it did not re-verify.
        #
        # The guard that existed only fired on a run that verified ZERO photographs, and zero is
        # not the shape a bad network has. This module's own MAX_CONCURRENCY note records eight of
        # eight concurrent lookups returning HTTP 429; one slot out of seven is what flaky hotel
        # wifi actually produces. Measured on a sidecar holding seven verified photographs with
        # fetch() returning one: the file went from 7 slots to 1, the run printed "1 image(s)
        # verified" and exited 0, and six photographs that had passed every provenance rule in this
        # file were gone with no note. Nothing downstream counts images, so the first person to
        # find out would have been the traveller standing in the city.
        def seeded(name: str, anchors: list[str], payload: dict) -> tuple[Path, Path]:
            """A plan naming `anchors` and a sidecar holding `payload`, on disk, ready for a re-run."""
            directory = tmp / name
            directory.mkdir()
            plan_file = directory / "trip.json"
            plan_file.write_text(json.dumps(
                {**fixture, "imagery_sidecar": "trip-imagery.json",
                 "destination_experience_anchors": [{"name": label} for label in anchors]},
                ensure_ascii=False), encoding="utf-8")
            side = directory / "trip-imagery.json"
            side.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            return plan_file, side

        six = [f"Anchor {index}" for index in range(6)]
        seven = {"hero": photo("Chengdu", "Chengdu")}
        for index, label in enumerate(six):
            seven[f"anchor:{index}"] = photo(label, f"Page{index}")
        one_slot = {"hero": photo("Chengdu", "Chengdu")}

        plan_file, side = seeded("partial", six, seven)
        code, out = run_fetch(imagery, plan_file, one_slot)
        after = json.loads(side.read_text(encoding="utf-8"))
        check("a re-run that verified one slot of seven keeps the other six",
              code == 0 and len(after) == 7, f"rc={code} keys={sorted(after)}\n{out}")
        check("the carried slots are the stored photographs, unaltered",
              all(after.get(key) == seven[key] for key in seven if key != "hero"),
              f"keys={sorted(after)}")
        check("a carry-forward is announced rather than passed off as verification",
              out.count("carried forward") >= 6, out)
        # "1 image(s) verified" is a true sentence about the run and a wholly misleading one about
        # the file, which is how nobody noticed the erasure. The line naming the file must count
        # the file.
        check("the sidecar line reports what landed on disk, not what the run verified",
              "7 image(s)" in out, out)

        # Removal still works, and is the documented way to drop a slot: take the anchor out of
        # the plan and re-run. Slots the plan no longer names are dropped -- with a note, because
        # a photograph disappearing silently is the defect above wearing a different hat.
        plan_file, side = seeded("removed", six[:3], seven)
        code, out = run_fetch(imagery, plan_file, one_slot)
        after = json.loads(side.read_text(encoding="utf-8"))
        check("dropping three anchors from the plan drops their three photographs",
              code == 0 and sorted(after) == ["anchor:0", "anchor:1", "anchor:2", "hero"],
              f"rc={code} keys={sorted(after)}\n{out}")
        check("each dropped slot is named in a note",
              all(f"anchor:{index}" in out for index in (3, 4, 5)), out)

        # The reason the merge is not a blind dict update. Slot keys are POSITIONAL, so deleting
        # the first anchor shifts every later one up a slot: a blind carry-forward would file the
        # photograph of "Anchor 1" under the heading now occupied by "Anchor 2". That is the exact
        # accuracy failure this whole module exists to refuse -- and unlike a missing photograph it
        # renders perfectly.
        plan_file, side = seeded("shifted", six[1:], seven)
        before = side.read_text(encoding="utf-8")
        code, out = run_fetch(imagery, plan_file, one_slot)
        check("a shifted anchor list refuses rather than re-filing photographs by position",
              code != 0 and "Anchor 1" in out, f"rc={code}\n{out}")
        check("a refused merge leaves the stored photographs exactly as they were",
              side.read_text(encoding="utf-8") == before, "the sidecar was rewritten anyway")
        check("a refused merge leaves the plan alone too",
              json.loads(plan_file.read_text(encoding="utf-8"))
              .get("destination_experience_anchors")[0]["name"] == "Anchor 1", "")

        # --max-images is the other way a run comes back with fewer slots than the plan names, and
        # it is not a failure at all -- it is the operator asking for a smaller payload. The slots
        # beyond the limit were never attempted, so they are exactly the slots that must survive.
        plan_file, side = seeded("limited", six, seven)
        code, out = run_fetch(imagery, plan_file,
                              {"hero": photo("Chengdu", "Chengdu"),
                               "anchor:0": photo("Anchor 0", "Page0")},
                              "--max-images", "2")
        after = json.loads(side.read_text(encoding="utf-8"))
        check("a --max-images run does not delete the slots it never looked at",
              code == 0 and len(after) == 7, f"rc={code} keys={sorted(after)}\n{out}")

        # Half the plans in a real workspace are CJK, so the label comparison that decides all of
        # the above has to hold in the script the traveller reads. Nothing here may depend on a
        # label being ASCII, casefoldable, or splittable on spaces.
        zh_dir = tmp / "zh"
        zh_dir.mkdir()
        zh_plan = zh_dir / "trip.json"
        zh_anchors = ["拉纳卡城堡", "拉纳卡市政市场"]
        zh_plan.write_text(json.dumps(
            {**fixture, "imagery_sidecar": "trip-imagery.json",
             "trip": {**fixture["trip"], "destination": "拉纳卡", "language": "Chinese"},
             "destination_experience_anchors": [{"name": label} for label in zh_anchors]},
            ensure_ascii=False), encoding="utf-8")
        zh_payload = {"hero": photo("拉纳卡", "Larnaca"),
                      "anchor:0": photo("拉纳卡城堡", "Larnaca Castle"),
                      "anchor:1": photo("拉纳卡市政市场", "Larnaca Municipal Market")}
        zh_side = zh_dir / "trip-imagery.json"
        zh_side.write_text(json.dumps(zh_payload, ensure_ascii=False), encoding="utf-8")
        code, out = run_fetch(imagery, zh_plan, {"hero": photo("拉纳卡", "Larnaca")})
        after = json.loads(zh_side.read_text(encoding="utf-8"))
        check("a CJK plan carries its unverified slots forward like any other",
              code == 0 and len(after) == 3 and after["anchor:1"]["label"] == "拉纳卡市政市场",
              f"rc={code} keys={sorted(after)}\n{out}")

        # An unreadable payload is not an absent one. The over-ceiling case is a file full of real
        # photographs this script refuses to parse, so clobbering it "because it could not be read"
        # would destroy more than any partial run could.
        torn_dir = tmp / "unreadable"
        torn_dir.mkdir()
        torn_plan = torn_dir / "trip.json"
        torn_plan.write_text(json.dumps({**fixture, "imagery_sidecar": "trip-imagery.json"},
                                        ensure_ascii=False), encoding="utf-8")
        (torn_dir / "trip-imagery.json").write_text("{not json", encoding="utf-8")
        code, out = run_fetch(imagery, torn_plan, one_slot)
        check("a run refuses to overwrite a payload it could not read",
              code != 0 and "trip-imagery.json" in out, f"rc={code}\n{out}")
        check("and the unreadable bytes are still there to be recovered",
              (torn_dir / "trip-imagery.json").read_text(encoding="utf-8") == "{not json", "")

        # ...but where the plan points at a payload that is simply GONE, there is nothing to lose
        # and the re-run must be able to rebuild. Refusing everywhere would mean a deleted sidecar
        # could only be repaired by hand-editing the plan first.
        gone_dir = tmp / "pointing-nowhere"
        gone_dir.mkdir()
        gone_plan = gone_dir / "trip.json"
        gone_plan.write_text(json.dumps({**fixture, "imagery_sidecar": "vanished-imagery.json"},
                                        ensure_ascii=False), encoding="utf-8")
        code, out = run_fetch(imagery, gone_plan, one_slot)
        check("a plan pointing at a payload that no longer exists can be rebuilt",
              code == 0 and (gone_dir / "trip-imagery.json").is_file(), f"rc={code}\n{out}")

        # 10. A sidecar found by NAME must prove it belongs to this plan.
        #
        # The key's original argument was "a flag is a thing to forget, so derive the name". The
        # missing half is that a filename guess is a thing to get WRONG, and it was measured on
        # this repo's own working filename: a Chengdu plan with no imagery key sat beside a
        # leftover trip-imagery.json from a Larnaca trip, and the delivered page opened with a
        # photograph of Larnaca, credited to Larnaca's photographer, under the Chengdu heading --
        # after which save_trip_deliverables.py stamped the foreign file in as this trip's payload
        # of record.
        foreign = {"hero": {**photo("Larnaca", "Larnaca"), "artist": "Another Trip's Photographer"}}
        stray = tmp / "stray"
        stray.mkdir()
        stray_plan = stray / "trip.json"
        stray_plan.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        (stray / "trip-imagery.json").write_text(json.dumps(foreign, ensure_ascii=False),
                                                 encoding="utf-8")
        stray_code, stray_out = render_page(stray_plan)
        check("a leftover sidecar from another trip does not reach the page",
              stray_code != 0 and "Traceback" not in stray_out, stray_out[:400])
        check("and the refusal shows the mismatch rather than only complaining",
              "'Larnaca'" in stray_out and "'Chengdu'" in stray_out, stray_out[:400])
        # Neither silently used NOR silently ignored: rendering a photo-less page here would be the
        # same silence the sidecar split was built to make impossible.
        check("the refusal names the way to adopt the file deliberately",
              "imagery_sidecar" in stray_out, stray_out[:400])

        # The declared key is authoritative and is asked for no proof: the plan said which file,
        # and a plan saying so is exactly the provenance a filename lacks. This is also what keeps
        # a legitimately renamed anchor from bricking its own plan.
        adopted = tmp / "adopted"
        adopted.mkdir()
        adopted_plan = adopted / "trip.json"
        adopted_plan.write_text(
            json.dumps({**fixture, "imagery_sidecar": "trip-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        (adopted / "trip-imagery.json").write_text(json.dumps(foreign, ensure_ascii=False),
                                                   encoding="utf-8")
        adopted_code, adopted_html = render_page(adopted_plan)
        check("a declared sidecar is used without being asked to prove itself",
              adopted_code == 0 and adopted_html.count("<img") == 1, adopted_html[:300])

        # An empty leftover carries no photograph, so it can attach nothing to the wrong trip and
        # refusing it would be a refusal about nothing.
        blank = tmp / "blank"
        blank.mkdir()
        blank_plan = blank / "trip.json"
        blank_plan.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        (blank / "trip-imagery.json").write_text("{}", encoding="utf-8")
        blank_code, blank_html = render_page(blank_plan)
        check("an empty leftover sidecar is not an error",
              blank_code == 0 and blank_html.count("<img") == 0, blank_html[:300])

        # The evidence rule itself, where the shapes are easier to state than through a CLI.
        check("a payload naming this plan's own slots vouches for itself",
              imagery.foreign_sidecar_slots(fixture, payload) == [],
              repr(imagery.foreign_sidecar_slots(fixture, payload)))
        check("a payload naming another trip's places does not",
              imagery.foreign_sidecar_slots(fixture, foreign) != [], "")
        check("a slot the plan does not have at all is foreign",
              imagery.foreign_sidecar_slots(fixture, {"anchor:7": photo("X", "X")}) != [], "")
        # A hand-written entry with no label proves nothing, and "no evidence" must not read as
        # "evidence of belonging" -- that inversion is how the whole class of bug starts.
        check("an entry with no label proves nothing",
              imagery.foreign_sidecar_slots(fixture, {"hero": {"data_uri": PIXEL}}) != [], "")
        raises("a plan too malformed to walk raises instead of crashing three frames down",
               lambda: imagery.plan_slot_labels({"trip": ["not", "an", "object"]}),
               "cannot be read")

        # 11. Standard input, which save_trip_deliverables.py documents in its own usage line.
        #
        # A piped plan has no directory, so `imagery_sidecar` -- a name relative to the plan -- was
        # resolved against whatever directory the command ran from. Measured both ways: the pipe
        # exited 2 for EVERY photographed plan from an ordinary cwd, and delivered a DIFFERENT
        # trip's photograph when that cwd happened to hold a file of the same name.
        def render_stdin(plan: dict, cwd: Path) -> tuple[int, str]:
            out = cwd / "piped.html"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "render_final_trip_html.py"),
                 "-", str(out)],
                input=json.dumps(plan, ensure_ascii=False), capture_output=True, text=True,
                cwd=str(cwd))
            if result.returncode != 0:
                return result.returncode, result.stdout + result.stderr
            return 0, out.read_text(encoding="utf-8")

        piped = {**fixture, "imagery_sidecar": "plan-imagery.json"}
        wrong_cwd = tmp / "wrong-cwd"
        wrong_cwd.mkdir()
        (wrong_cwd / "plan-imagery.json").write_text(json.dumps(foreign, ensure_ascii=False),
                                                     encoding="utf-8")
        code, out = render_stdin(piped, wrong_cwd)
        check("a piped plan does not adopt a same-named file from the current directory",
              code != 0 and "Another Trip's Photographer" not in out, out[:400])

        right_cwd = tmp / "right-cwd"
        right_cwd.mkdir()
        (right_cwd / "plan-imagery.json").write_text(json.dumps(payload, ensure_ascii=False),
                                                     encoding="utf-8")
        code, out = render_stdin(piped, right_cwd)
        check("a piped plan still works where the payload is provably its own",
              code == 0 and out.count("<img") == 2, out[:400])

        empty_cwd = tmp / "empty-cwd"
        empty_cwd.mkdir()
        code, out = render_stdin(piped, empty_cwd)
        check("a piped plan whose payload is nowhere refuses with the remedy, not a shrug",
              code != 0 and "instead of `-`" in out, out[:500])
        check("a piped plan with no photographs at all is unaffected",
              render_stdin(fixture, empty_cwd) == (0, (empty_cwd / "piped.html")
                                                   .read_text(encoding="utf-8")), "")

        # 12. The documented date-shift flow, which produced a plan neither consumer could open.
        #
        # The fixture's dates are fixed and replan_trip.py refuses a window before today, so the
        # shifts below pin today; unpinned, this block started failing once the calendar passed
        # the fixture (2026-10-09) for a reason that has nothing to do with photographs.
        REPLAN_TODAY = "2026-09-01"
        # `replan_trip.py <plan.json> --shift-days N --out <new.json>` copied `imagery_sidecar`
        # verbatim, so a plan shifted into any other directory named a file that was not beside it
        # and both render_final_trip_html.py and save_trip_deliverables.py exited 2 on it. The
        # photographs are still OF the same places -- a delta moves no venues -- so they travel
        # with the plan and what is no longer true about them goes into must_reverify.
        shift_from, shift_to = tmp / "shift-from", tmp / "shift-to"
        shift_from.mkdir()
        shift_to.mkdir()
        source_plan = shift_from / "trip.json"
        source_plan.write_text(
            json.dumps({**fixture, "imagery_sidecar": "trip-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        (shift_from / "trip-imagery.json").write_text(json.dumps(payload, ensure_ascii=False),
                                                      encoding="utf-8")
        shifted_plan = shift_to / "trip-shifted.json"
        replan = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "replan_trip.py"), str(source_plan),
             "--shift-days", "5", "--today", REPLAN_TODAY, "--out", str(shifted_plan)], capture_output=True, text=True)
        replan_out = replan.stdout + replan.stderr
        check("a date shift into another directory succeeds", replan.returncode == 0,
              replan_out[:400])
        shifted_code, shifted_html = render_page(shifted_plan) if shifted_plan.exists() else (9, "")
        check("and the shifted plan is one the renderer can still open, with its photographs",
              shifted_code == 0 and shifted_html.count("<img") == 2, shifted_html[:300])
        moved = json.loads(shifted_plan.read_text(encoding="utf-8")) if shifted_plan.exists() else {}
        check("the key names a file that is actually beside the new plan",
              (shift_to / str(moved.get("imagery_sidecar"))).is_file(),
              repr(moved.get("imagery_sidecar")))
        check("the source plan and its payload are left untouched",
              json.loads(source_plan.read_text(encoding="utf-8"))["imagery_sidecar"]
              == "trip-imagery.json" and (shift_from / "trip-imagery.json").is_file(), "")
        # What is no longer true is recorded rather than assumed away: a frame shot in one season
        # shows light, foliage and crowds the traveller will not meet in another, and slot keys are
        # positional, so re-verification that reorders an anchor moves every later photograph.
        flagged = [entry for entry in (moved.get("replan_context") or {}).get("must_reverify", [])
                   if entry.get("path") == "imagery_sidecar"]
        check("carrying the photographs is flagged, not silently accepted",
              len(flagged) == 1 and "season" in flagged[0]["reason"], repr(flagged))

        # stdout mode has no directory to put them in, so it refuses instead of writing a plan that
        # names a file relative to nowhere.
        piped_replan = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "replan_trip.py"), str(source_plan),
             "--shift-days", "5", "--today", REPLAN_TODAY], capture_output=True, text=True)
        check("a date shift to stdout refuses a plan whose photographs are in a sidecar",
              piped_replan.returncode != 0 and "--out" in piped_replan.stderr
              and not piped_replan.stdout.strip(),
              (piped_replan.stdout + piped_replan.stderr)[:400])

        # And a payload it cannot read is a refusal, not a plan written with the key copied over.
        broken_source = shift_from / "broken.json"
        broken_source.write_text(
            json.dumps({**fixture, "imagery_sidecar": "not-here-imagery.json"}, ensure_ascii=False),
            encoding="utf-8")
        broken_target = shift_to / "broken-shifted.json"
        broken_replan = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "replan_trip.py"), str(broken_source),
             "--shift-days", "5", "--today", REPLAN_TODAY, "--out", str(broken_target)], capture_output=True, text=True)
        check("a date shift refuses a plan whose photographs cannot be read",
              broken_replan.returncode != 0 and not broken_target.exists(),
              (broken_replan.stdout + broken_replan.stderr)[:400])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all imagery and visual regression cases passed")
    return 0


def test_plan_imagery() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
