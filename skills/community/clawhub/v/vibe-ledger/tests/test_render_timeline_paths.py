import re

from helpers.verified import sample
from ledger_report import paths_svg, timeline_svg


def test_build_items_order_and_compromise_status():
    items, overflow = timeline_svg.build_items(sample())
    assert [it["key"] for it in items] == ["P1", "C1", "P2", "P3", "P4"]
    c1 = items[1]
    assert c1["compromise"] and c1["status"] == "broken" and [e[1] for e in c1["events"]] == ["error", "ai_changed"]
    assert items[2]["lane"] == "deferred" and items[3]["lane"] == "ai_changed" and overflow == []


def test_timeline_svg_contents():
    html = timeline_svg.render_timeline(sample(), "zh", True)
    for word in ("你说的", "报错", "AI 改的", "以后再说", "今天", "09-12", "09-13"):
        assert word in html
    assert html.count('<g class="tl-pill') == 5
    assert html.count('class="mk s-') == 6
    assert html.count('class="arc s-') == 5 and html.count('class="tl-link s-') == 1
    assert "妥协: RLS · 仍在代码里" in html
    assert "<title>只有我自己能看到我的笔记</title>" in html


def test_timeline_without_transcripts_or_items():
    assert "没找到对话记录" in timeline_svg.render_timeline(sample(), "zh", False)
    led = sample()
    for e in led["evidence"].values():
        if e["kind"] == "transcript":
            e["ok"] = False
    assert "能核实的事件" in timeline_svg.render_timeline(led, "zh", True)


def test_timeline_overflow_note():
    led = sample()
    base = led["promises"][3]
    led["promises"] += [{**base, "id": f"X{i}"} for i in range(20)]
    items, overflow = timeline_svg.build_items(led)
    assert len(items) == timeline_svg.MAX_ITEMS and overflow
    assert "放不下" in timeline_svg.render_timeline(led, "zh", True)


def test_timeline_dimensions_are_numbers():
    html = timeline_svg.render_timeline(sample(), "en", True)
    w, h = re.search(r'viewBox="0 0 (\d+) (\d+(?:\.\d+)?)"', html).groups()
    assert int(w) > 400 and float(h) > 200


def test_paths_steps_warnings_and_unverified():
    html = paths_svg.render_paths(sample(), "zh")
    assert html.count('<g class="step') == 3
    assert 'class="step warn"' in html and "⚠ 没有登录检查" in html
    assert 'class="step unverified"' in html and "未核实" in html
    assert "app/api/summarize/route.ts:3" in html and "点“AI 总结”" in html
    assert html.count('class="flow"') == 2


def test_paths_wrap_rows():
    led = sample()
    step = led["paths"][0]["steps"][0]
    led["paths"] = [{"action": "long", "steps": [{**step, "label": f"s{i}"} for i in range(6)]}]
    html = paths_svg.render_paths(led, "en")
    assert html.count('<g class="step') == 6 and html.count('class="flow"') == 5


def test_paths_empty():
    led = sample()
    led["paths"] = []
    assert "没有可展示的操作路径" in paths_svg.render_paths(led, "zh")


def _same_day_ledger(extra):
    led = sample()
    base = led["promises"][3]
    for i in range(extra):
        e = dict(led["evidence"]["E1"], ts=f"2026-09-12T1{i % 10}:0{i % 6}:00Z", quote="只有我自己能看到我的笔记")
        led["evidence"][f"T{i}"] = e
        led["promises"].append({**base, "id": f"T{i}", "source": [f"T{i}"]})
    led["evidence"]["E4"]["ts"] = "2026-09-12T10:00:00Z"
    return led


def test_timeline_fits_the_page_for_an_ordinary_history():
    html = timeline_svg.render_timeline(_same_day_ledger(3), "zh", True)
    width = int(re.search(r'viewBox="0 0 (\d+) ', html).group(1))
    assert width <= timeline_svg.MAX_WIDTH


def test_timeline_labels_times_within_one_day():
    html = timeline_svg.render_timeline(_same_day_ledger(6), "zh", True)
    assert len(re.findall(r'class="tl-date"[^>]*>\d\d:\d\d<', html)) >= 1


def test_timeline_pill_text_fits_its_box():
    from ledger_report import bits
    led = sample()
    led["promises"][0]["plain"] = "不要让陌生人随便调用 AI 花我的钱，也不要让他们看到我的笔记"
    html = timeline_svg.render_timeline(led, "zh", True)
    pills = re.findall(r'<g class="tl-pill[^"]*">.*?<text[^>]*>(.*?)</text>', html)
    assert pills and all(bits.width(p) <= timeline_svg.PILL_UNITS for p in pills)


def test_pill_css_does_not_wrap():
    from pathlib import Path
    css = (Path(__file__).resolve().parents[1] / "scripts/ledger_report/assets/report.css").read_text()
    assert re.search(r"\.pill\{[^}]*white-space:nowrap", css)
