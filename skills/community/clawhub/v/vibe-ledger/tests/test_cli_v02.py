import json
import re
from pathlib import Path

import pytest

import shot
import vl
from common import load_json
from helpers.fake_logs import ClaudeSession

LEDGER = {"evidence": {}, "promises": []}
EXPLAIN = {"evidence": {}, "files": {"lib/ai.ts": {
    "purpose_plain": "把文字发给 OpenAI 总结。", "purpose_dev": "Wraps `summarize` around the OpenAI client.",
    "functions": [{"name": "summarize", "line": 3, "plain": "把文字发出去，取回总结"},
                  {"name": "sendEmail", "line": 9, "plain": "发邮件"}]}}}
OVERLAP_DOM = ('<body data-layout="done"><svg><g class="vlg-node" data-id="app/page.tsx" data-x="0" data-y="0" '
               'data-w="236" data-h="58" data-dim="0"></g><g class="vlg-node sel" data-id="lib/ai.ts" data-x="100" '
               'data-y="20" data-w="236" data-h="58" data-dim="0"></g></svg></body>')


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    return tmp_path


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_app(tmp_path, name="app"):
    """app/page.tsx (Next.js entry) and lib/util.ts both use lib/ai.ts, which calls OpenAI."""
    app = tmp_path / name
    write(app, "app/page.tsx", 'import { summarize } from "../lib/ai";\nexport default function Page() {\n  return summarize("x");\n}\n')
    write(app, "lib/ai.ts", 'import OpenAI from "openai";\nconst client = new OpenAI();\n'
                            'export async function summarize(text) {\n  return client.responses.create({ input: text });\n}\n')
    write(app, "lib/util.ts", 'import { summarize } from "./ai";\nexport const twice = (t) => summarize(t + t);\n')
    write(app, "package.json", json.dumps({"dependencies": {"next": "14", "openai": "4"}}))
    s = ClaudeSession(app, "s1")
    s.user("帮我做一个把文字总结成一句话的网页")
    s.edit(app / "lib/ai.ts", "return text;", "return client.responses.create({ input: text });")
    s.save(tmp_path / "claude" / "projects")
    return app


def start(app):
    assert vl.main(["start", "--project", str(app)]) == 0
    return vl.latest_run(app)


def put(run, name, doc):
    (run / name).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def through_render(app):
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", EXPLAIN)
    put(run, "requirements.json", {"evidence": {}, "requirements": []})
    assert vl.main(["check", "--project", str(app)]) == 0
    assert vl.main(["render", "--project", str(app)]) == 0
    return run


def test_start_writes_graph_and_explain_pack(env, capsys):
    run = start(make_app(env))
    out = capsys.readouterr().out
    g = load_json(run / "graph.json")
    assert {n["id"] for n in g["nodes"]} == {"app/page.tsx", "lib/ai.ts", "lib/util.ts"}
    assert [x["id"] for x in g["externals"]] == ["ext:openai"]
    assert "### lib/ai.ts" in (run / "explain_pack.md").read_text(encoding="utf-8")
    stats = load_json(run / "run.json")["graph"]
    assert stats["files"] == 3 and stats["externals"] == 1 and stats["explain_groups"] == 1
    assert "File graph: 3 files" in out and str(run / "explain.json") in out and "explain-guide.md" in out
    assert vl.top_file(g) == "lib/ai.ts"


def test_start_with_many_files_asks_for_explain_parts(env, capsys):
    app = env / "many"
    write(app, "src/main.ts", "".join(f'import "./m{i}";\n' for i in range(10)))
    for i in range(10):
        write(app, f"src/m{i}.ts", f"export function f{i}() {{}}\n")
    run = start(app)
    out = capsys.readouterr().out
    assert load_json(run / "run.json")["graph"]["explain_groups"] == 2
    assert "explain_NN.json" in out and "merge --project" in out and "check --project" in out


def test_merge_combines_explanation_parts(env, capsys):
    run = start(make_app(env))
    parts = run / "parts"
    parts.mkdir()
    put(parts, "explain_01.json", EXPLAIN)
    put(parts, "explain_02.json", {"evidence": {}, "files": {
        "lib/ai.ts": {"purpose_plain": "第二份，应被跳过"},
        "app/page.tsx": {"purpose_plain": "首页，调用总结功能。"}}})
    capsys.readouterr()
    assert vl.main(["merge", "--project", str(env / "app")]) == 0
    merged = load_json(run / "explain.json")
    assert set(merged["files"]) == {"lib/ai.ts", "app/page.tsx"} and merged["duplicates"] == ["lib/ai.ts"]
    assert merged["files"]["lib/ai.ts"]["purpose_plain"] == "把文字发给 OpenAI 总结。"
    out = capsys.readouterr().out
    assert "Merged 2 explanation parts" in out and "check --project" in out
    assert not (run / "ledger.json").exists()


def test_merge_reports_bad_explanation_parts(env, capsys):
    run = start(make_app(env))
    (run / "parts").mkdir()
    put(run / "parts", "explain_01.json", {"files": {"lib/ai.ts": {}}})
    capsys.readouterr()
    assert vl.main(["merge", "--project", str(env / "app")]) == 2
    assert "purpose_plain must be a non-empty string" in capsys.readouterr().out


def test_check_lists_explain_problems_then_drops_invented_functions(env, capsys):
    app = make_app(env)
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", {"files": {"lib/ai.ts": {"functions": []}}})
    put(run, "requirements.json", {"evidence": {}, "requirements": []})
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    assert "purpose_plain must be a non-empty string" in capsys.readouterr().out
    put(run, "explain.json", EXPLAIN)
    put(run, "requirements.json", {"evidence": {}, "requirements": []})
    assert vl.main(["check", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    assert "Functions dropped: 1" in out and "sendEmail — not defined in this file" in out and "render --project" in out
    kept = load_json(run / "explain.verified.json")["files"]["lib/ai.ts"]["functions"]
    assert [f["name"] for f in kept] == ["summarize"]


def test_check_needs_explain_json_and_render_needs_a_passing_check(env, capsys):
    app = make_app(env)
    run = through_render(app)
    (run / "explain.json").unlink()
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    out = capsys.readouterr().out
    assert "explain.json does not exist yet" in out and "explain_pack.md" in out
    assert not (run / "explain.verified.json").exists()
    assert vl.main(["render", "--project", str(app)]) == 2


def test_check_on_a_run_without_graph_asks_to_start_again(env, capsys):
    app = make_app(env)
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", EXPLAIN)
    put(run, "requirements.json", {"evidence": {}, "requirements": []})
    (run / "graph.json").unlink()
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    out = capsys.readouterr().out
    assert "older version" in out and "start --project" in out
    assert str(run / "ledger.json") in out and "copy" in out  # the user is told their ledger is not lost


def test_render_builds_the_flowchart_page(env, capsys):
    run = through_render(make_app(env))
    html = (run / "report.html").read_text(encoding="utf-8")
    assert 'class="vl-tabs"' in html and 'id="vl-data"' in html and html.count("var dagre=") == 1
    assert "把文字发给 OpenAI 总结。" in html
    data = json.loads(re.search(r'id="vl-data">(.*?)</script>', html, re.S).group(1))
    card = {n["id"]: n for n in data["nodes"]}["lib/ai.ts"]["card"]
    assert [f["name"] for f in card["functions"]] == ["summarize"]  # the invented name never reaches the panel
    assert "lib/ai.ts · sendEmail" in html  # it is listed, with its reason, under what the report could not verify


def test_project_without_code_files_still_renders(env, capsys):
    app = env / "bare"
    write(app, "index.html", "<h1>hi</h1>")
    run = start(app)
    assert "File graph: 0 files" in capsys.readouterr().out
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", {"evidence": {}, "files": {}})
    put(run, "requirements.json", {"evidence": {}, "requirements": []})
    assert vl.main(["check", "--project", str(app)]) == 0
    assert vl.main(["render", "--project", str(app)]) == 0
    assert '"g_no_files"' in (run / "report.html").read_text(encoding="utf-8")


def test_shot_passes_the_top_file_and_reports_overlaps(env, capsys, monkeypatch):
    app = make_app(env)
    through_render(app)
    seen = {}

    def fake_shots(report, out_dir, chrome, select=None, journey=None, requirements=False, dataflow=False):
        seen["select"], seen["journey"], seen["requirements"] = select, journey, requirements
        return [Path(out_dir) / "desktop.png"]
    monkeypatch.setattr(shot, "find_chrome", lambda: "/fake/chrome")
    monkeypatch.setattr(shot, "take_shots", fake_shots)
    monkeypatch.setattr(shot, "dump_dom", lambda chrome, url, timeout=90: OVERLAP_DOM)
    capsys.readouterr()
    assert vl.main(["shot", "--project", str(app)]) == 1
    out = capsys.readouterr().out
    assert seen["select"] == "lib/ai.ts" and seen["journey"] is None and seen["requirements"] is True
    assert "Layout check FAILED" in out and "app/page.tsx ↔ lib/ai.ts" in out
    monkeypatch.setattr(shot, "dump_dom", lambda chrome, url, timeout=90: "")
    assert vl.main(["shot", "--project", str(app)]) == 1
    assert "did not finish drawing" in capsys.readouterr().out


def test_shots_in_a_real_browser(env, capsys):
    if not shot.find_chrome():
        pytest.skip("Chrome/Chromium not available")
    app = make_app(env)
    through_render(app)
    capsys.readouterr()
    assert vl.main(["shot", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    names = {Path(m.strip()).name for m in re.findall(r"Screenshot: (.+)", out)}
    assert names == {"desktop.png", "desktop-dark.png", "phone-390.png", "selected.png", "overview.png",
                     "requirements.png"}
    assert "none overlap; selected lib/ai.ts" in out


def test_shot_includes_the_first_journey(env, capsys, monkeypatch):
    app = make_app(env)
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", {**EXPLAIN, "journeys": [{"title": "你点「总结」时", "steps": [
        {"file": "app/page.tsx", "plain": "页面交出文字"}, {"file": "lib/ai.ts", "plain": "发给 OpenAI"}]}]})
    put(run, "requirements.json", {"evidence": {}, "requirements": []})
    assert vl.main(["check", "--project", str(app)]) == 0
    assert "Journeys: 1 kept" in capsys.readouterr().out
    assert vl.main(["render", "--project", str(app)]) == 0
    seen = {}

    def fake_shots(report, out_dir, chrome, select=None, journey=None, requirements=False, dataflow=False):
        seen["journey"] = journey
        return [Path(out_dir) / "desktop.png"]
    monkeypatch.setattr(shot, "find_chrome", lambda: "/fake/chrome")
    monkeypatch.setattr(shot, "take_shots", fake_shots)
    monkeypatch.setattr(shot, "dump_dom", lambda chrome, url, timeout=90: "")
    vl.main(["shot", "--project", str(app)])
    assert seen["journey"] == "J1"


def test_render_compares_with_the_previous_run(env, capsys):
    app = make_app(env)
    through_render(app)
    first = capsys.readouterr().out
    assert "没有可比的上一次运行" in first  # the line follows the report language (this app's is Chinese)
    write(app, "lib/extra.ts", 'export const extra = 1;\n')
    write(app, "lib/util.ts", 'import { summarize } from "./ai";\nimport { extra } from "./extra";\nexport const twice = (t) => summarize(t + t);\n')
    run = through_render(app)
    out = capsys.readouterr().out
    assert "的运行相比" in out and "1 个新文件，1 个改过，0 个删掉" in out
    html = (run / "report.html").read_text(encoding="utf-8")
    data = json.loads(re.search(r'id="vl-data">(.*?)</script>', html, re.S).group(1))
    assert {n["id"]: n["diff"] for n in data["nodes"]}["lib/extra.ts"] == "new"
    assert vl.main(["render", "--project", str(app), "--no-compare"]) == 0
    assert "的运行相比" not in capsys.readouterr().out


def test_compare_refuses_a_run_that_cannot_be_compared(env, capsys):
    app = make_app(env)
    first = through_render(app)
    run = through_render(app)
    capsys.readouterr()
    assert vl.main(["render", "--project", str(app), "--compare", str(run)]) == 2
    assert "is this run" in capsys.readouterr().out
    other = make_app(env, name="other")
    other_run = through_render(other)
    capsys.readouterr()
    assert vl.main(["render", "--project", str(app), "--compare", str(other_run)]) == 2
    assert "another project" in capsys.readouterr().out
    (first / "graph.json").write_text("{broken", encoding="utf-8")
    assert vl.main(["render", "--project", str(app), "--compare", str(first)]) == 2
    assert "graph.json" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        vl.main(["render", "--project", str(app), "--compare", str(first), "--no-compare"])
