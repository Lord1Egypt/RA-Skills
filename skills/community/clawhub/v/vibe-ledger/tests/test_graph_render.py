import pytest

import render
import shot
from helpers.graph_fixture import make_project
from helpers.verified import PROBES, RUN, sample
from ledger_report import graph_page


def page(tmp_path, lang="zh", **kw):
    root, g, explained, ledger, probes = make_project(tmp_path, **kw)
    data = graph_page.page_data(g, explained, ledger, probes, root, lang, True)
    return render.render_html(sample(), RUN, PROBES, lang, graph_data=data)


def test_tabbed_page_structure(tmp_path):
    html = page(tmp_path)
    assert html.count("<h1>") == 1 and 'class="vl-tabs"' in html and 'data-tab="overview"' in html
    assert 'id="vl-data"' in html and html.count("var dagre=") == 1 and "vlg-viewport" in html
    assert '<section id="tab-overview" class="vl-tabpanel" hidden>' in html and "对账表" in html
    assert html.index('id="vl-data"') < html.index("var dagre=") < html.index("function computeLayout")
    assert "<!--VL_DAGRE-->" not in html
    assert render.find_secrets(html.replace(graph_page.dagre_source(), "")) == []


def test_untabbed_page_is_unchanged():
    html = render.render_html(sample(), RUN, PROBES, "zh")
    assert "vl-tabs" not in html and "var dagre=" not in html and html.count("<h1>") == 1


def test_overview_coverage_lists_graph_gaps(tmp_path):
    root, g, explained, ledger, probes = make_project(tmp_path)
    g["unresolved"] = [{"from": "lib/ai.ts", "spec": "./gone", "line": 9}]
    g["excluded"] = {"tests": 2, "config": 1}
    explained["files"]["lib/ai.ts"]["dropped_functions"] = [{"name": "sendEmail", "reason": "not defined in this file"}]
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    overview = render.render_html(sample(), RUN, PROBES, "zh", graph_data=data).split('id="vl-data"')[0]
    assert "流程图没有画 2 个测试文件和 1 个配置文件" in overview
    assert "lib/ai.ts:9" in overview and "./gone" in overview and "lib/ai.ts · sendEmail" in overview


def test_dagre_has_no_script_breaking_text():
    assert "</script" not in graph_page.dagre_source().lower()


def _browser_or_skip():
    chrome = shot.find_chrome()
    if not chrome:
        pytest.skip("Chrome/Chromium not available")
    return chrome


def test_layout_and_selection_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    out = tmp_path / "report.html"
    out.write_text(page(tmp_path / "proj"), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?select=lib/ai.ts")
    rep = shot.layout_report(dom)
    assert rep["done"] and rep["overlaps"] == []
    ids = {n["id"]: n for n in rep["nodes"]}
    assert set(ids) == {"app/page.tsx", "lib/ai.ts", "lib/util.ts", "ext:openai"}
    assert ids["ext:openai"]["x"] > ids["app/page.tsx"]["x"]
    assert ids["lib/util.ts"]["x"] > ids["app/page.tsx"]["x"]  # an unimported non-entry file is not drawn left of the entry
    assert rep["selected"] == ["lib/ai.ts"]
    assert ids["app/page.tsx"]["dim"] == "0" and ids["lib/util.ts"]["dim"] == "1"
    assert "把文字发给 OpenAI 总结。" in dom


def test_large_graph_collapses_without_overlaps_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    root = tmp_path / "big"
    for d in ("src/ai", "src/ui", "src/db", "src/util"):
        for i in range(40):
            p = root / d / f"f{i}.ts"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f'import "../util/f{(i + 1) % 40}";\n' if d != "src/util" else "", encoding="utf-8")
    (root / "src" / "main.ts").write_text('import "./ai/f0";\nimport "./ui/f0";\nimport "./db/f0";\n', encoding="utf-8")
    import graph
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    out = tmp_path / "big.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    rep = shot.layout_report(shot.dump_dom(chrome, out.as_uri()))
    assert rep["done"] and rep["overlaps"] == []
    assert {n["id"] for n in rep["nodes"]} == {"folder:src/ai", "folder:src/ui", "folder:src/db", "folder:src/util", "src/main.ts"}


def test_layout_report_parses_nodes_and_finds_overlaps():
    dom = ('<body data-layout="done"><svg><g class="vlg-node r-logic s-ok sel" data-id="a" data-x="0" data-y="0" '
           'data-w="100" data-h="50" data-dim="0"></g><g class="vlg-node r-logic s-ok" data-id="b" data-x="90" '
           'data-y="10" data-w="100" data-h="50" data-dim="1"></g><g class="vlg-node" data-id="c" data-x="300" '
           'data-y="0" data-w="100" data-h="50" data-dim="1"></g></svg></body>')
    rep = shot.layout_report(dom)
    assert rep["done"] and rep["selected"] == ["a"] and rep["overlaps"] == [["a", "b"]] and len(rep["nodes"]) == 3


def test_wide_graph_opens_readable_at_the_entries_in_a_real_browser(tmp_path):
    import re

    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "chain"
    root.mkdir()
    (root / "index.html").write_text('<script type="module" src="/src/m0.ts"></script>', encoding="utf-8")
    for i in range(12):  # twelve columns: far wider than the canvas at a fitted scale
        (root / "src").mkdir(exist_ok=True)
        (root / "src" / f"m{i}.ts").write_text(f'import "./m{i + 1}";\n' if i < 11 else "", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    out = tmp_path / "chain.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri())
    m = re.search(r'id="vlg-viewport" transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([\d.]+)\)"', dom)
    assert m, "viewport transform not found"
    tx, scale = float(m.group(1)), float(m.group(3))
    entry = {n["id"]: n for n in shot.layout_report(dom)["nodes"]}["src/m0.ts"]
    assert scale >= 0.7  # cards readable on first sight
    assert 0 <= tx + entry["x"] * scale <= 200  # and the view starts where the reading starts
    resized = tmp_path / "chain-resized.html"  # screenshot mode resizes the window after load; the selection must survive
    resized.write_text(out.read_text(encoding="utf-8").replace(
        "</body>", "<script>setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 50);</script></body>"),
        encoding="utf-8")
    dom = shot.dump_dom(chrome, resized.as_uri() + "?select=src/m11.ts")
    m = re.search(r'id="vlg-viewport" transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([\d.]+)\)"', dom)
    tx, scale = float(m.group(1)), float(m.group(3))
    last = {n["id"]: n for n in shot.layout_report(dom)["nodes"]}["src/m11.ts"]
    assert 0 <= tx + last["x"] * scale <= 880 - last["w"] * scale  # a selected file is brought into view


def test_journey_route_and_positions_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    root, g, explained, ledger, probes = make_project(tmp_path / "proj")
    explained["journeys"] = [
        {"id": "J1", "title": "你点「总结」时", "outcome": "总结出现在页面上", "dropped_steps": [],
         "steps": [{"file": "app/page.tsx", "plain": "页面把文字交出去"}, {"file": "lib/ai.ts", "plain": "发给 OpenAI", "linked": True}]},
        {"id": "J2", "title": "工具函数", "outcome": "", "dropped_steps": [],
         "steps": [{"file": "lib/util.ts", "plain": "算一个数"}, {"file": "lib/ai.ts", "plain": "用上它", "linked": False}]}]
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    out = tmp_path / "report.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data), encoding="utf-8")
    home = shot.dump_dom(chrome, out.as_uri())
    assert home.count('class="vlg-journey-btn"') == 2
    dom = shot.dump_dom(chrome, out.as_uri() + "?journey=J1")
    ids = {n["id"]: n for n in shot.layout_report(dom)["nodes"]}
    assert ids["app/page.tsx"]["dim"] == "0" and ids["lib/ai.ts"]["dim"] == "0" and ids["lib/util.ts"]["dim"] == "1"
    assert dom.count('class="vlg-jbadge"') == 2 and "页面把文字交出去" in dom and "最后：总结出现在页面上" in dom
    assert 'class="vlg-jlink unlinked"' not in dom  # page.tsx imports ai.ts, so the real arrow carries the route
    dom2 = shot.dump_dom(chrome, out.as_uri() + "?journey=J2")
    assert dom2.count('class="vlg-jlink unlinked"') == 1 and "代码里没找到这一步和上一步之间的直接引用" in dom2
    card = shot.dump_dom(chrome, out.as_uri() + "?select=app/page.tsx")
    assert "在整体里的位置" in card and "你点「总结」时，第 1/2 步：页面把文字交出去" in card


def test_journey_draws_each_step_from_the_step_that_calls_it_in_a_real_browser(tmp_path):
    import re

    import explain
    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "hub"
    (root / "src").mkdir(parents=True)
    (root / "index.html").write_text('<script type="module" src="/src/hub.js"></script>', encoding="utf-8")
    (root / "src" / "hub.js").write_text('import "./a";\nimport "./b";\n', encoding="utf-8")
    (root / "src" / "a.js").write_text("export const a = 1;\n", encoding="utf-8")
    (root / "src" / "b.js").write_text("export const b = 1;\n", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    explained = explain.verify({"evidence": {}, "files": {}, "journeys": [{"title": "t", "steps": [
        {"file": "src/hub.js", "plain": "page"}, {"file": "src/a.js", "plain": "a"}, {"file": "src/b.js", "plain": "b"}]}]},
        g, root, {})
    data = graph_page.page_data(g, explained, sample(), {"findings": []}, root, "en", False)
    assert [s.get("from") for s in data["journeys"][0]["steps"]] == [None, 0, 0]
    out = tmp_path / "hub.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?journey=J1")
    hot = re.findall(r'<path[^>]*class="vlg-edge hot( flow)?"[^>]*data-from="([^"]+)" data-to="([^"]+)"', dom)
    assert all(flow for flow, _, _ in hot)  # a route's arrows carry the moving dashes
    hot = [(a, b) for _, a, b in hot]
    assert sorted(hot) == [("src/hub.js", "src/a.js"), ("src/hub.js", "src/b.js")]
    assert 'class="vlg-jlink' not in dom  # both steps ride real import arrows; no invented a → b line


def test_arrows_enter_cards_horizontally_from_the_left_in_a_real_browser(tmp_path):
    import re

    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "web"
    (root / "src").mkdir(parents=True)
    (root / "index.html").write_text('<script type="module" src="/src/main.ts"></script>', encoding="utf-8")
    (root / "src" / "main.ts").write_text('import "./a";\nimport "./b";\nimport "./c";\nimport "./d";\n', encoding="utf-8")
    for name, deps in (("a", "b"), ("b", "d"), ("c", "d"), ("d", "")):
        (root / "src" / f"{name}.ts").write_text(f'import "./{deps}";\n' if deps else "", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    out = tmp_path / "web.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri())
    boxes = {n["id"]: n for n in shot.layout_report(dom)["nodes"]}
    paths = re.findall(r'<path d="([^"]+)" class="vlg-edge[^"]*" data-from="([^"]+)" data-to="([^"]+)"', dom)
    assert len(paths) == 7
    for d, a, b in paths:
        nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", d)]
        end, last_ctrl, target = (nums[-2], nums[-1]), (nums[-4], nums[-3]), boxes[b]
        assert abs(end[0] - target["x"]) < 0.6, (a, b, d)  # on the card's left edge…
        assert target["y"] + 10 <= end[1] <= target["y"] + target["h"] - 10, (a, b, d)  # …at one of its ports
        assert abs(last_ctrl[1] - end[1]) < 0.6 and last_ctrl[0] < end[0], (a, b, d)  # arrives level, moving right


def _path_samples(d):
    """Points along an SVG path made of M, L and C commands (what graph.js draws)."""
    import re
    tokens = re.findall(r"[MLC]|-?\d+(?:\.\d+)?", d)
    pts, cur, i = [], None, 0
    while i < len(tokens):
        cmd = tokens[i]
        if cmd == "M":
            cur = (float(tokens[i + 1]), float(tokens[i + 2])); pts.append(cur); i += 3
        elif cmd == "L":
            nxt = (float(tokens[i + 1]), float(tokens[i + 2]))
            pts += [(cur[0] + (nxt[0] - cur[0]) * t / 20, cur[1] + (nxt[1] - cur[1]) * t / 20) for t in range(1, 21)]
            cur = nxt; i += 3
        elif cmd == "C":
            c1 = (float(tokens[i + 1]), float(tokens[i + 2])); c2 = (float(tokens[i + 3]), float(tokens[i + 4]))
            nxt = (float(tokens[i + 5]), float(tokens[i + 6]))
            for k in range(1, 21):
                t = k / 20
                pts.append(tuple((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3
                                 for p0, p1, p2, p3 in zip(cur, c1, c2, nxt)))
            cur = nxt; i += 7
        else:
            i += 1
    return pts


def test_links_go_around_cards_in_a_real_browser(tmp_path):
    import re

    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "chain"
    (root / "src").mkdir(parents=True)
    (root / "index.html").write_text('<script type="module" src="/src/m0.ts"></script>', encoding="utf-8")
    (root / "src" / "m0.ts").write_text('import "./m1";\nimport "./m3";\nimport OpenAI from "openai";\n', encoding="utf-8")
    (root / "src" / "m1.ts").write_text('import "./m2";\n', encoding="utf-8")
    (root / "src" / "m2.ts").write_text('import "./m3";\n', encoding="utf-8")
    (root / "src" / "m3.ts").write_text("export const x = 1;\n", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    out = tmp_path / "chain.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri())
    boxes = {n["id"]: n for n in shot.layout_report(dom)["nodes"]}
    paths = re.findall(r'<path d="([^"]+)" class="vlg-edge[^"]*" data-from="([^"]+)" data-to="([^"]+)"', dom)
    assert {(a, b) for _, a, b in paths} >= {("src/m0.ts", "src/m3.ts"), ("src/m0.ts", "ext:openai")}
    for d, a, b in paths:
        for x, y in _path_samples(d):
            for cid, c in boxes.items():
                if cid in (a, b):
                    continue
                inside = c["x"] + 2 < x < c["x"] + c["w"] - 2 and c["y"] + 2 < y < c["y"] + c["h"] - 2
                assert not inside, f"{a} → {b} passes through {cid} at ({x:.0f}, {y:.0f})"


def test_expanding_a_hovered_folder_leaves_nothing_dimmed_in_a_real_browser(tmp_path):
    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "big"
    for d in ("src/ai", "src/ui", "src/db", "src/util"):
        for i in range(25):
            p = root / d / f"f{i}.ts"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f'import "../util/f{i}";\n' if d != "src/util" else "", encoding="utf-8")
    (root / "src" / "main.ts").write_text('import "./ai/f0";\n', encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    html = render.render_html(sample(), RUN, PROBES, "en", graph_data=data).replace("</body>", (
        "<script>setTimeout(function () { var n = document.querySelector('.vlg-node.r-folder');"
        " n.dispatchEvent(new MouseEvent('mouseenter')); n.dispatchEvent(new MouseEvent('click', {bubbles: true})); }, 50);"
        "</script></body>"))
    out = tmp_path / "big.html"
    out.write_text(html, encoding="utf-8")
    rep = shot.layout_report(shot.dump_dom(chrome, out.as_uri()))
    assert len(rep["nodes"]) > 5  # the folder opened
    assert [n["id"] for n in rep["nodes"] if n["dim"] == "1"] == []


def test_keyboard_esc_in_search_keeps_the_file_and_space_opens_one_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    root, g, explained, ledger, probes = make_project(tmp_path / "proj")
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    script = ("<script>setTimeout(function () {"
              " var s = document.getElementById('vlg-search');"
              " s.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));"
              " var u = document.querySelector('.vlg-node[data-id=\"lib/util.ts\"]');"
              " if (location.hash === '#space') u.dispatchEvent(new KeyboardEvent('keydown', {key: ' ', bubbles: true}));"
              "}, 50);</script></body>")
    out = tmp_path / "report.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data).replace("</body>", script), encoding="utf-8")
    kept = shot.layout_report(shot.dump_dom(chrome, out.as_uri() + "?select=lib/ai.ts"))
    assert kept["selected"] == ["lib/ai.ts"]  # Esc in the search box only leaves the search box
    spaced = shot.layout_report(shot.dump_dom(chrome, out.as_uri() + "#space"))
    assert spaced["selected"] == ["lib/util.ts"]


def test_developer_view_shows_names_only_around_the_focus_in_a_real_browser(tmp_path):
    import re

    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "dev"
    (root / "src").mkdir(parents=True)
    (root / "index.html").write_text('<script type="module" src="/src/main.ts"></script>', encoding="utf-8")
    (root / "src" / "main.ts").write_text('import { alpha, beta, gamma, delta } from "./lib";\nimport { one } from "./other";\n',
                                          encoding="utf-8")
    (root / "src" / "lib.ts").write_text("export const alpha = 1;\nexport const beta = 2;\nexport const gamma = 3;\n"
                                         "export const delta = 4;\nexport function helper() {\n  return 1;\n}\n", encoding="utf-8")
    (root / "src" / "other.ts").write_text("export const one = 1;\n", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    explained = {"evidence": {}, "rejected": [], "files": {"src/lib.ts": {
        "purpose_plain": "放几个常量。", "purpose_dev": "Exports `alpha` and friends.", "ok": True, "dropped_functions": [],
        "purpose_unverified": False, "missing_identifiers": [], "history": [],
        "functions": [{"name": "helper", "line": 5, "plain": "返回 1", "line_corrected": False}]}}}
    data = graph_page.page_data(g, explained, sample(), {"findings": []}, root, "zh", False)
    out = tmp_path / "dev.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data), encoding="utf-8")
    rest = shot.dump_dom(chrome, out.as_uri() + "?view=dev")
    labels = re.findall(r'<text[^>]*class="(vlg-edge-label names[^"]*)"', rest)
    assert labels and not any("hot" in c for c in labels)  # nothing at rest: CSS hides every label that is not hot
    sel = shot.dump_dom(chrome, out.as_uri() + "?view=dev&select=src/lib.ts")
    hot = re.findall(r'<text[^>]*class="vlg-edge-label names[^"]*hot[^"]*"[^>]*>([^<]*)</text>', sel)
    assert hot == ["alpha, beta +2"]  # only lib.ts's own link, two names and a count
    assert 'class="vlg-devmeta"' in sel and "src/lib.ts · 8 行 · 5 个导出" in sel
    assert re.search(r'class="vlg-namerow"><button[^>]*>main\.ts</button><span class="vlg-names">alpha, beta, gamma, delta</span>', sel)
    assert re.search(r'<details class="vlg-fn"><summary><code>helper:5</code>', sel) and "<details open" not in sel
    assert 'class="vlg-devnote"' in sel


def test_long_name_labels_are_shortened_in_a_real_browser(tmp_path):
    import re

    import graph
    chrome = _browser_or_skip()
    root = tmp_path / "long"
    (root / "src").mkdir(parents=True)
    (root / "index.html").write_text('<script type="module" src="/src/main.ts"></script>', encoding="utf-8")
    (root / "src" / "main.ts").write_text(
        'import { extractAnthropicJsonPayload, extractOpenAiJsonPayload } from "./payload";\n'
        'import { theVeryLongestPossibleExportedHelperName } from "./helpers";\n', encoding="utf-8")
    (root / "src" / "payload.ts").write_text("export const extractAnthropicJsonPayload = 1;\n"
                                             "export const extractOpenAiJsonPayload = 2;\n", encoding="utf-8")
    (root / "src" / "helpers.ts").write_text("export const theVeryLongestPossibleExportedHelperName = 1;\n", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    out = tmp_path / "long.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?view=dev&select=src/main.ts")
    hot = sorted(re.findall(r'<text[^>]*class="vlg-edge-label names[^"]*hot[^"]*"[^>]*>([^<]*)</text>', dom))
    assert hot == ["extractAnthropicJsonPayload +1", "theVeryLongestPossibleExpor…"]


def test_compare_view_marks_what_changed_in_a_real_browser(tmp_path):
    import re

    from ledger_report import diff
    from test_diff import make_run, write
    chrome = _browser_or_skip()
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "index.html", '<script type="module" src="/main.ts"></script>')
    write(project, "main.ts", 'import "./old";\nimport "./keep";\nimport "./side";\n')
    write(project, "old.ts", "export const o = 1;\n")
    write(project, "keep.ts", 'import "./side";\nexport const k = 1;\n')
    write(project, "side.ts", "export const s = 1;\n")
    prev, _ = make_run(runs, "20261010-090000", project)
    (project / "old.ts").unlink()
    write(project, "main.ts", 'import "./keep";\nimport "./side";\nimport "./fresh";\n')
    write(project, "keep.ts", "export const k = 2;\n")  # no longer imports side.ts: a link that is gone, both ends remain
    write(project, "fresh.ts", "export const f = 1;\n")
    cur, g = make_run(runs, "20261012-090000", project)
    d = diff.compare(prev, cur, "zh")
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, project, "zh", False, diff=d)
    out = tmp_path / "cmp.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?compare=1")
    cls = {n["id"]: n["cls"].split() for n in shot.layout_report(dom)["nodes"]}
    assert "d-new" in cls["fresh.ts"] and "d-changed" in cls["main.ts"] and "d-changed" in cls["keep.ts"]
    assert "dim" in cls["side.ts"]
    assert re.search(r'<path[^>]*class="vlg-dgone"', dom)  # keep.ts → side.ts is gone
    assert re.search(r'class="vlg-edge[^"]*d-new[^"]*" data-from="main.ts" data-to="fresh.ts"', dom)
    assert "和上次比（2026-10-10）" in dom and "1 个新文件，2 个改过，1 个删掉" in dom and "old.ts" in dom
    assert 'id="vlg-legend-diff"' in dom  # the legend says what green, blue and red dashes mean
    card = shot.dump_dom(chrome, out.as_uri() + "?select=keep.ts")
    assert "比上次：内容改过" in card and "比上次：不再调用 side.ts" in card


def test_export_builds_a_standalone_svg_and_a_png_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    root, g, explained, ledger, probes = make_project(tmp_path / "proj")
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    probe = ("<script>setTimeout(function () {"
             " var s = window.vibeLedger.exportSvg();"
             " document.body.setAttribute('data-svg-head', s.slice(0, 40));"
             " document.body.setAttribute('data-svg-ok', [s.indexOf('viewBox') > 0, s.indexOf('ai.ts') > 0, s.indexOf('<style') > 0,"
             "   s.indexOf('vlg-bg') > 0, s.indexOf('font-family') > 0].join(','));"
             " document.body.setAttribute('data-name', window.vibeLedger.fileName('png'));"
             " window.vibeLedger.exportPng(function (blob) { document.body.setAttribute('data-png', blob.type + ':' + blob.size); });"
             "}, 50);</script></body>")
    out = tmp_path / "report.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data).replace("</body>", probe), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?select=lib/ai.ts")
    import re
    attrs = dict(re.findall(r'data-(svg-head|svg-ok|name|png)="([^"]*)"', dom))
    assert attrs["svg-head"].startswith("&lt;svg") and attrs["svg-ok"] == "true,true,true,true,true"
    assert attrs["name"] == "proj-流程图.png"  # named after the project folder
    kind, size = attrs["png"].split(":")
    assert kind == "image/png" and int(size) > 2000
    assert 'data-act="export"' in dom


def test_module_and_data_views_in_a_real_browser(tmp_path):
    import re

    from test_graph_page import _views_project
    chrome = _browser_or_skip()
    root = tmp_path / "views"
    g = _views_project(root)
    ledger = {"evidence": {"E1": {"kind": "code", "path": "src/ai/client.js", "line": 1, "snippet": "x", "ok": True}},
              "promises": [], "compromises": [],
              "map": {"nodes": [{"id": "panel", "lane": "browser", "kind": "page", "label": "面板", "holds": [], "paid": False, "evidence": []},
                                {"id": "oa", "lane": "storage", "kind": "third_party", "label": "OpenAI", "holds": [], "paid": True,
                                 "evidence": ["E1"]}],
                      "edges": [{"from": "panel", "to": "oa", "carries": "简历和职位", "risk": None, "evidence": ["E1"]}]}}
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, ledger, {"findings": []}, root, "zh", False)
    out = tmp_path / "views.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data), encoding="utf-8")
    mods = shot.layout_report(shot.dump_dom(chrome, out.as_uri() + "?mode=modules"))
    assert {n["id"] for n in mods["nodes"]} == {"folder:src/ai", "folder:src/ui", "folder:src/store", "folder:scripts",
                                                "src/background.js", "ext:openai", "ext:local-storage"}
    assert mods["overlaps"] == []
    dom = shot.dump_dom(chrome, out.as_uri() + "?mode=data")
    flow = shot.layout_report(dom)
    assert {n["id"] for n in flow["nodes"]} == {"src/background.js", "src/ui/panel.js", "src/ai/client.js", "ext:openai"}
    assert re.search(r'class="vlg-edge-label carries"[^>]*>简历和职位<', dom)


def test_sequence_view_of_a_journey_in_a_real_browser(tmp_path):
    import re
    chrome = _browser_or_skip()
    root, g, explained, ledger, probes = make_project(tmp_path / "proj")
    explained["journeys"] = [{"id": "J1", "title": "你点「总结」时", "outcome": "总结出现在页面上", "dropped_steps": [],
                              "steps": [{"file": "app/page.tsx", "plain": "页面把文字交出去"},
                                        {"file": "lib/ai.ts", "plain": "发给 OpenAI", "linked": True, "from": 0},
                                        {"file": "app/page.tsx", "plain": "显示总结", "linked": True, "from": 1}]}]
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    out = tmp_path / "seq.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "zh", graph_data=data), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?journey=J1&seq=1")
    assert 'data-layout="done"' in dom and 'class="vlg-seq"' in dom
    assert len(re.findall(r'<g class="vlg-seq-actor[ "]', dom)) == 3  # you, page.tsx, ai.ts
    assert len(re.findall(r'<g class="vlg-msg(?: [^"]*)?"', dom)) == 4  # three steps and the outcome coming back to you
    assert "总结出现在页面上" in dom and 'class="vlg-node' not in dom


def _interactive(tmp_path, data, script, query=""):
    """Render `data`, run `script` in the page after it settles, and return the DOM."""
    out = tmp_path / "interactive.html"
    html = render.render_html(sample(), RUN, PROBES, "zh", graph_data=data)
    out.write_text(html.replace("</body>", "<script>setTimeout(function () {" + script + "}, 60);</script></body>"), encoding="utf-8")
    return shot.dump_dom(_browser_or_skip(), out.as_uri() + query)


def _journey_data(tmp_path, steps=None):
    root, g, explained, ledger, probes = make_project(tmp_path / "proj")
    steps = steps or [{"file": "app/page.tsx", "plain": "页面交出文字"}, {"file": "lib/ai.ts", "plain": "发给 OpenAI", "linked": True, "from": 0}]
    explained["journeys"] = [{"id": "J1", "title": "你点「总结」时", "outcome": "总结出现", "dropped_steps": [], "steps": steps}]
    return graph_page.page_data(g, explained, ledger, probes, root, "zh", True)


_SEARCH = ("var s = document.getElementById('vlg-search'); s.value = '{q}';"
           " s.dispatchEvent(new Event('change', {{bubbles: true}}));")


def test_searching_from_the_sequence_view_returns_to_the_flowchart_in_a_real_browser(tmp_path):
    dom = _interactive(tmp_path, _journey_data(tmp_path), _SEARCH.format(q="lib/ai.ts"), "?journey=J1&seq=1")
    assert 'class="vlg-seq"' not in dom and shot.layout_report(dom)["selected"] == ["lib/ai.ts"]


def test_clicking_a_lifeline_opens_that_file_in_a_real_browser(tmp_path):
    click = ("var r = document.querySelector('.vlg-seq-actor[data-id=\"lib/ai.ts\"] rect');"
             " r.dispatchEvent(new MouseEvent('click', {bubbles: true}));")
    dom = _interactive(tmp_path, _journey_data(tmp_path), click, "?journey=J1&seq=1")
    assert shot.layout_report(dom)["selected"] == ["lib/ai.ts"] and 'class="vlg-seq"' not in dom


def test_a_file_hidden_by_the_data_view_opens_in_the_files_view_in_a_real_browser(tmp_path):
    dom = _interactive(tmp_path, _journey_data(tmp_path), _SEARCH.format(q="lib/util.ts"), "?mode=data")
    rep = shot.layout_report(dom)
    assert rep["selected"] == ["lib/util.ts"]
    assert '<button type="button" data-mode="files" class="on">' in dom


def test_a_long_sequence_opens_at_its_top_in_a_real_browser(tmp_path):
    import re
    import graph
    root, _, explained, ledger, probes = make_project(tmp_path / "proj")
    for i in range(30):  # thirty entries: the flowchart's entries sit far down, where the sequence must not be centred
        (root / "app" / f"p{i}").mkdir(parents=True)
        (root / "app" / f"p{i}" / "page.tsx").write_text("export default function P() {}\n", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    steps = [{"file": "app/page.tsx" if k % 2 == 0 else "lib/ai.ts", "plain": f"第 {k + 1} 步", "linked": True,
              **({"from": k - 1} if k else {})} for k in range(16)]
    explained["journeys"] = [{"id": "J1", "title": "长路线", "outcome": "", "dropped_steps": [], "steps": steps}]
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    dom = _interactive(tmp_path, data, "", "?journey=J1&seq=1")
    ty = float(re.search(r'id="vlg-viewport" transform="translate\([-\d.]+,([-\d.]+)\)', dom).group(1))
    assert 0 <= ty <= 80  # the lifeline heads (at y = 0) are on screen


def test_service_names_are_normalised_by_whole_words():
    assert graph_page._norm_service("OpenAI API") == "openai"
    assert graph_page._norm_service("rapid") == "rapid" and graph_page._norm_service("API") == ""


def test_quiet_comparison_hides_the_toggle_in_a_real_browser(tmp_path):
    from ledger_report import diff
    from test_diff import make_run, write
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts", "export const a = 1;\n")
    prev, _ = make_run(runs, "20261010-090000", project)
    cur, g = make_run(runs, "20261012-090000", project)
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, project, "zh", False,
                                diff=diff.compare(prev, cur, "zh"))
    dom = _interactive(tmp_path, data, "")
    assert '<button type="button" data-act="compare" hidden="">' in dom


def test_data_view_folders_count_only_the_files_drawn_in_a_real_browser(tmp_path):
    import re

    import graph
    from e2e.medium import make_medium
    root = make_medium(tmp_path / "medium")
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "zh", False)
    dom = _interactive(tmp_path, data, "", "?mode=data")
    lib = re.search(r'data-id="folder:src/lib"(.*?)</g>', dom, re.S).group(1)
    assert "12 个文件" in lib  # l12…l19 lead nowhere from the entry, so the data view leaves them out
