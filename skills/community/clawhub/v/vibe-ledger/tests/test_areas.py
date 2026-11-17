import json
import re

import pytest

import areas
import explain
from ledger_report import graph_page
from ledger_report.graph_page import render_graph_tab


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def graph(paths, edges=(), externals=()):
    return {"nodes": [{"id": p, "label": p.rsplit("/", 1)[-1]} for p in paths], "edges": [{"from": a, "to": b} for a, b in edges],
            "externals": list(externals)}


PATHS = ["scripts/tts.py", "scripts/render.py", "scripts/a_qa.py", "scripts/b_qa.py", ".remotion/x.js", "lib/util.py"]


def test_first_area_that_matches_a_file_owns_it():
    owner, unmatched = areas.assign([
        {"id": "checks", "match": ["scripts/*_qa.py"]},
        {"id": "voice", "match": ["scripts/tts.py", "scripts/nope.py"]},
        {"id": "engine", "match": ["./.remotion/"]},  # "./" goes, the folder's own dot stays
        {"id": "rest", "match": ["scripts/"]},
    ], PATHS)
    assert owner["scripts/a_qa.py"] == owner["scripts/b_qa.py"] == "checks"
    assert owner["scripts/tts.py"] == "voice" and owner["scripts/render.py"] == "rest"
    assert owner[".remotion/x.js"] == "engine" and owner["lib/util.py"] == areas.OTHER
    assert unmatched == {"voice": ["scripts/nope.py"]}


@pytest.mark.parametrize("change, problem", [
    (lambda d: d.update(areas=d["areas"][:1]), "write 2–10 areas"),
    (lambda d: d["areas"][0].update(match=[]), "match must list"),
    (lambda d: d["areas"][1].update(id="voice"), "id missing or duplicated"),
    (lambda d: d["items"][0].update(kind="blob"), "kind must be one of"),
    (lambda d: d["flows"][0].update(op="send"), "op must be one of"),
    (lambda d: d["flows"][0].update(area="nowhere"), "unknown area"),
    (lambda d: d["flows"][0].pop("line"), "needs path, line"),
])
def test_format_problems_are_named(change, problem):
    d = doc()
    change(d)
    assert any(problem in p for p in areas.problems(d)), areas.problems(d)
    with pytest.raises(explain.ExplainError):
        explain.validate(d)


def doc():
    return {"evidence": {}, "files": {},
            "areas": [{"id": "voice", "name": "配音", "plain": "念旁白", "match": ["scripts/tts.py"]},
                      {"id": "render", "name": "渲染", "plain": "出片", "match": ["scripts/render.py"]},
                      {"id": "checks", "name": "检查", "plain": "查成片", "match": ["scripts/*_qa.py"]}],
            "items": [{"id": "words", "name": "逐词时间", "kind": "file", "match": ["words.json"]},
                      {"id": "film", "name": "成片", "kind": "output", "match": ["out.mp4"]}],
            "flows": [{"area": "voice", "item": "words", "op": "write", "path": "scripts/tts.py", "line": 2,
                       "snippet": 'open(base + ".words.json", "w").write(data)'},
                      {"area": "render", "item": "words", "op": "read", "path": "scripts/render.py", "line": 1,
                       "snippet": 'words = json.load(open("audio/01.words.json"))'},
                      {"area": "render", "item": "film", "op": "write", "path": "scripts/render.py", "line": 3,
                       "snippet": 'dst = os.path.join(out_dir, "out.mp4")'}]}


@pytest.fixture
def project(tmp_path):
    write(tmp_path, "scripts/tts.py", 'import json\nopen(base + ".words.json", "w").write(data)\n')
    write(tmp_path, "scripts/render.py", 'words = json.load(open("audio/01.words.json"))\nimport os\n'
                                         'dst = os.path.join(out_dir, "out.mp4")\n')
    write(tmp_path, "scripts/a_qa.py", 'film = os.path.join(out_dir, "out.mp4")\n')
    write(tmp_path, "lib/util.py", "x = 1\n")
    return tmp_path


G = graph(["scripts/tts.py", "scripts/render.py", "scripts/a_qa.py", "lib/util.py"],
          edges=[("scripts/render.py", "scripts/tts.py"), ("scripts/tts.py", "ext:openai")],
          externals=[{"id": "ext:openai", "label": "OpenAI API", "kind": "paid", "evidence": []}])


def test_verify_keeps_flows_the_code_shows(project):
    m = areas.verify(doc(), G, project)
    assert [a["id"] for a in m["areas"]] == ["voice", "render", "checks"] and m["other"] == ["lib/util.py"]
    assert len(m["flows"]) == 3 and m["rejected_flows"] == [] and {i["id"] for i in m["items"]} == {"words", "film"}


def test_verify_rejects_flows_with_the_reason(project):
    d = doc()
    d["flows"] += [
        {"area": "voice", "item": "film", "op": "read", "path": "scripts/a_qa.py", "line": 1,
         "snippet": 'film = os.path.join(out_dir, "out.mp4")'},  # a checks file, not a voice file
        {"area": "checks", "item": "words", "op": "read", "path": "scripts/a_qa.py", "line": 1,
         "snippet": 'film = os.path.join(out_dir, "out.mp4")'},  # does not name words.json
        {"area": "checks", "item": "film", "op": "read", "path": "scripts/a_qa.py", "line": 1,
         "snippet": "this line is not in the file"},
    ]
    d["areas"].append({"id": "ghost", "name": "空", "plain": "无", "match": ["nowhere/"]})
    m = areas.verify(d, G, project)
    reasons = [r["reason"] for r in m["rejected_flows"]]
    assert "belongs to area checks, not voice" in reasons[0]
    assert "does not name 逐词时间" in reasons[1]
    assert "not found" in reasons[2]
    assert m["dropped_areas"][0]["id"] == "ghost" and "matches a file" in m["dropped_areas"][0]["reason"]
    lines = "\n".join(areas.summary_lines(m))
    assert "3 rejected" in lines and "in no area" in lines


def test_page_data_links_the_writer_area_to_the_reader_area(project):
    m = areas.verify(doc(), G, project)
    fm = graph_page._function_map(m, G, {}, "zh")
    assert [a["id"] for a in fm["areas"]] == ["voice", "render", "checks", "__other"]
    assert fm["area_links"] == [{"from": "scripts/tts.py", "to": "scripts/render.py", "carries": ["逐词时间"]}]
    edges = {(e["from"], e["to"]) for e in fm["flow"]["edges"]}
    assert ("scripts/tts.py", "item:words") in edges and ("item:words", "scripts/render.py") in edges
    assert ("scripts/tts.py", "ext:openai") in edges  # outside services come from the imports
    assert fm["area_io"]["voice"] == {"reads": [], "writes": ["逐词时间"], "calls": ["OpenAI API"]}
    film = next(i for i in fm["flow"]["items"] if i["id"] == "item:film")
    assert film["writes"][0]["where"] == "scripts/render.py:3" and film["reads"] == []


def test_without_areas_the_page_keeps_the_folder_views():
    assert graph_page._function_map(None, G, {}, "en") == {"areas": None, "area_links": [], "flow": None}
    folder_tabs = re.findall(r'data-mode="(\w+)"', render_graph_tab("en"))
    assert folder_tabs == ["files", "modules", "data"]
    assert re.findall(r'data-mode="(\w+)"', render_graph_tab("en", True)) == ["map", "data"]


def test_pack_lists_every_file_and_the_data_the_code_names(project):
    pack = areas.pack_section(G, project)
    assert "`scripts/` (3)" in pack and "`lib/` (1)" in pack
    assert "**out.mp4**" in pack and "scripts/render.py:3" in pack


def test_explain_check_carries_the_function_map(project):
    out = explain.verify(doc(), G, project, {})
    assert out["function_map"]["areas"][0]["files"] == ["scripts/tts.py"]
    assert "Function map: 3 areas" in "\n".join(explain.summary_lines(out))
    bare = explain.verify({"evidence": {}, "files": {}}, G, project, {})
    assert bare["function_map"] is None


def test_guide_names_the_function_map_vocabulary():
    from pathlib import Path
    guide = (Path(__file__).resolve().parents[1] / "references" / "explain-guide.md").read_text(encoding="utf-8")
    block = re.search(r"`{3}json\n(.+?)\n`{3}", guide, re.S).group(1)
    assert json.loads(block)["areas"] and not areas.problems(json.loads(block))
    missing = [w for w in areas.OPS + areas.ITEM_KINDS if f"`{w}`" not in guide]
    assert not missing, missing


def test_a_page_calling_its_server_is_a_labelled_link_on_the_map(project):
    write(project, "web/index.html", "x")
    g = graph(["scripts/tts.py", "scripts/render.py", "scripts/a_qa.py", "web/index.html"])
    g["edges"] = [{"from": "web/index.html", "to": "scripts/render.py", "names": ["/api/film"]}]
    d = doc()
    d["areas"].insert(0, {"id": "page", "name": "页面", "plain": "你看到的页面", "match": ["web/"]})
    m = areas.verify(d, g, project)
    links = graph_page._function_map(m, g, {}, "zh")["area_links"]
    assert {"from": "web/index.html", "to": "scripts/render.py", "carries": ["/api/film"]} in links
