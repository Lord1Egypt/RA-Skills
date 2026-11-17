import re

from helpers.verified import sample
from ledger_report import access_html, map_svg


def svg_part(html):
    return html[html.index("<svg"):html.index("</svg>")]


def test_map_lanes_nodes_edges_and_legend():
    html = map_svg.render_map(sample(), "zh")
    svg = svg_part(html)
    for label in ("浏览器", "你的服务器", "存储与第三方服务", "首页", "/api/summarize", "Supabase", "OpenAI"):
        assert label in svg
    assert svg.count('<g class="node') == 4
    assert svg.count("<path class=\"edge") == 3
    assert svg.count('class="edge risk"') == 1 and "陌生人也能读" in svg
    assert svg.count("💰") == 2  # the OpenAI node and the legend
    assert 'class="node-ref dev-only"' in svg and "supabase/migrations/001.sql:3" in svg


def test_unverified_nodes_are_listed_not_drawn():
    html = map_svg.render_map(sample(), "zh")
    assert "Stripe" not in svg_part(html)
    assert "未核实，没画进图里" in html and "Stripe" in html


def test_map_caps_nodes_and_lists_overflow():
    led = sample()
    led["map"]["nodes"] = [{"id": f"n{i}", "lane": "server", "kind": "function", "label": f"fn{i}", "holds": [],
                            "paid": False, "evidence": ["E2"]} for i in range(15)]
    led["map"]["edges"] = []
    html = map_svg.render_map(led, "en")
    assert svg_part(html).count('<g class="node') == map_svg.MAX_NODES
    assert "Others (no room on the map)" in html and "fn14" in html


def test_select_nodes_puts_risky_and_paid_first():
    m = sample()["map"]
    shown, overflow = map_svg.select_nodes(m)
    assert [n["id"] for n in shown][:2] == ["web", "db"] and shown[2]["id"] == "ai" and overflow == []


def test_empty_map():
    led = sample()
    led["map"] = {"nodes": [], "edges": [], "unverified_nodes": [], "unverified_edges": []}
    assert "没能从代码里确认任何数据去向" in map_svg.render_map(led, "zh")


def test_map_svg_coordinates_are_finite_numbers():
    svg = svg_part(map_svg.render_map(sample(), "zh"))
    for num in re.findall(r'\b(?:x|y|width|height)="([^"]+)"', svg):
        float(num)


def test_access_matrix_rows_cells_and_frames():
    html = access_html.render_access(sample(), "zh")
    main = html.split('<details class="ok-rows">')[0]
    assert "notes" in main and "陌生人" in main and "其他登录用户" in main and "本人" in main
    assert main.count('class="cell frame') == 2  # anonymous + signed_in on a broken requirement
    assert "只有我自己能看到我的笔记" in main and "❌" in main
    assert '<details class="ok-rows">' in html and "其余 1 类数据" in html and "profiles" in html.split("ok-rows")[1]


def test_access_conflicts_unknown_and_probe_notes():
    led = sample()
    cells = led["access"]["resources"][0]["cells"]
    cells["anonymous"] = {"read": "deny", "write": "unknown", "evidence": ["E2"], "from_probe": ["secrets_exposed:.env.local:2"],
                          "conflicts": [{"perm": "read", "probe": "p", "probe_says": "allow", "ledger_says": "deny",
                                         "message": "RLS is off for notes"}]}
    html = access_html.render_access(led, "zh")
    assert "说法冲突" in html and "RLS is off for notes" in html
    assert 'class="unknown"' in html and 'class="probe-note dev-only"' in html


def test_star_resource_and_empty():
    led = sample()
    led["access"]["resources"] = [{"name": "*", "required_by": None, "cells": {
        "anonymous": {"read": "allow", "write": "allow", "evidence": []}}}]
    assert "所有数据" in access_html.render_access(led, "zh")
    led["access"]["resources"] = []
    assert "没有检测到数据库" in access_html.render_access(led, "zh")


def test_is_problem():
    statuses = {"P1": "broken", "P4": "kept"}
    ok = {"name": "x", "required_by": "P4", "cells": {"anonymous": {"read": "deny", "write": "deny"}}}
    assert not access_html.is_problem(ok, statuses)
    assert access_html.is_problem({**ok, "required_by": "P1"}, statuses)
    assert access_html.is_problem({"name": "y", "cells": {"anonymous": {"read": "allow", "write": "deny"}}}, statuses)


def test_edge_labels_sit_in_the_gaps_on_top_of_the_nodes():
    svg = svg_part(map_svg.render_map(sample(), "zh"))
    assert svg.rindex('<g class="node') < svg.index('class="edge-label')
    boxes = [(x, x + map_svg.LANE_W) for x in map_svg.LANE_X]
    xs = re.findall(r'class="edge-label[^"]*" x="([\d.]+)"', svg)
    assert xs
    for x in xs:
        assert not any(a < float(x) < b for a, b in boxes), x
        assert 0 < float(x) < map_svg.WIDTH
    assert 'class="node risky"' not in svg
    assert "<title>⚠ 笔记 — 陌生人也能读</title>" in svg


def test_edges_that_skip_a_lane_go_below_its_boxes():
    svg = svg_part(map_svg.render_map(sample(), "zh"))
    # sample: web (browser) -> db (storage) skips the server lane, whose only box ends at y = TOP + NODE_H
    d = re.search(r'<path class="edge risk" d="([^"]+)"', svg).group(1)
    ys = [float(v) for v in re.findall(r",(-?[\d.]+)", d)]
    assert max(ys) > map_svg.TOP + map_svg.NODE_H


def test_edge_label_text_sits_above_its_line():
    svg = svg_part(map_svg.render_map(sample(), "zh"))
    label_ys = [float(y) for y in re.findall(r'class="edge-label[^"]*" x="[\d.]+" y="([\d.]+)"', svg)]
    node_centres = {map_svg.TOP + map_svg.NODE_H / 2 + i * (map_svg.NODE_H + map_svg.GAP) for i in range(3)}
    for y in label_ys:
        assert all(not (c - 4 < y < c + 12) for c in node_centres), y


def test_map_lane_labels_replace_the_web_app_titles():
    led = sample()
    led["map"]["lane_labels"] = {"browser": "你运行的脚本", "server": "本机处理"}
    svg = svg_part(map_svg.render_map(led, "zh"))
    assert "你运行的脚本" in svg and "本机处理" in svg and "存储与第三方服务" in svg
    assert "浏览器" not in svg and "你的服务器" not in svg
