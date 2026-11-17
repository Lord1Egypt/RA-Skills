import json

import graph
from ledger_report import diff, graph_page


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def make_run(runs, name, project, ledger=None, probes=None, complete=True):
    run = runs / name
    run.mkdir(parents=True)
    g = graph.build(project, [], probes or {"findings": []})
    (run / "graph.json").write_text(json.dumps(g), encoding="utf-8")
    (run / "probes.json").write_text(json.dumps(probes or {"findings": []}), encoding="utf-8")
    (run / "run.json").write_text(json.dumps({"created": f"2026-10-{name[6:8]}T09:00:00+00:00"}), encoding="utf-8")
    if complete:
        (run / "ledger.verified.json").write_text(json.dumps(ledger or {"evidence": {}, "promises": [], "compromises": []}),
                                                  encoding="utf-8")
        (run / "explain.verified.json").write_text(json.dumps({"evidence": {}, "files": {}}), encoding="utf-8")
    return run, g


def finding(path, message, level="certain", probe="secrets_exposed"):
    return {"id": f"{probe}:{path}:1", "probe": probe, "level": level, "path": path, "line": 1,
            "snippet": "x", "message": message, "implies": []}


def promise(plain, status):
    return {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": plain, "status": status,
            "source": [], "verdict_plain": "v", "verdict_dev": "d", "evidence": []}


def test_nodes_carry_a_content_fingerprint(tmp_path):
    write(tmp_path, "a.ts", "export const a = 1;\n")
    write(tmp_path, "b.ts", "export const a = 1;\n")
    nodes = {n["id"]: n for n in graph.build(tmp_path, [], {"findings": []})["nodes"]}
    assert nodes["a.ts"]["sha"] == nodes["b.ts"]["sha"] and len(nodes["a.ts"]["sha"]) == 12


def test_previous_run_is_the_latest_earlier_complete_one(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts")
    make_run(runs, "20261010-090000", project)
    make_run(runs, "20261011-090000", project, complete=False)  # check never passed: not comparable
    cur, _ = make_run(runs, "20261012-090000", project)
    make_run(runs, "20261013-090000", project)  # later than the current run: never the "previous" one
    assert diff.previous_run(cur).name == "20261010-090000"
    assert diff.previous_run(runs / "20261010-090000") is None


def test_compare_files_links_services_risks_and_promises(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "main.ts", 'import "./old";\nimport "./keep";\n')
    write(project, "old.ts", "export const o = 1;\n")
    write(project, "keep.ts", "export const k = 1;\n")
    prev, _ = make_run(runs, "20261010-090000", project,
                       ledger={"evidence": {}, "compromises": [], "promises": [promise("只有我能看到", "broken")]},
                       probes={"findings": [finding("keep.ts", "A OpenAI secret is written directly in the code")]})
    (project / "old.ts").unlink()
    write(project, "main.ts", 'import "./keep";\nimport "./fresh";\n')
    write(project, "keep.ts", 'import OpenAI from "openai";\nexport const k = 2;\n')
    write(project, "fresh.ts", "export const f = 1;\n")
    cur, _ = make_run(runs, "20261012-090000", project,
                      ledger={"evidence": {}, "compromises": [], "promises": [promise("只有我能看到", "kept")]},
                      probes={"findings": [finding("fresh.ts", "This environment file is tracked by git; pushing the repository publishes it", "hint")]})
    d = diff.compare(prev, cur, "zh")
    assert d["since"] == "2026-10-10T09:00:00+00:00" and d["sha_known"] is True
    assert d["files"] == {"added": ["fresh.ts"], "removed": ["old.ts"], "changed": ["keep.ts", "main.ts"]}
    assert d["links"]["added"] == [["keep.ts", "ext:openai"], ["main.ts", "fresh.ts"]]
    assert d["links"]["removed"] == [["main.ts", "old.ts"]]
    assert d["services"] == {"added": ["ext:openai"], "removed": []}
    assert d["risks"]["new"] == [{"path": "fresh.ts", "level": "warn", "text": "这个环境变量文件被 git 记录了，推送仓库就会把它公开"}]
    assert d["risks"]["resolved"] == [{"path": "keep.ts", "level": "bad", "text": "代码里直接写着一个 OpenAI 密钥"}]
    assert d["promises"] == {"changed": [{"plain": "只有我能看到", "before": "broken", "after": "kept"}], "new": [], "gone": []}


def test_a_run_without_fingerprints_compares_only_added_and_removed(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts", "export const a = 1;\n")
    prev, g = make_run(runs, "20261010-090000", project)
    for n in g["nodes"]:
        del n["sha"]  # a v0.2 run
    (prev / "graph.json").write_text(json.dumps(g), encoding="utf-8")
    write(project, "a.ts", "export const a = 2;\n")
    cur, _ = make_run(runs, "20261012-090000", project)
    d = diff.compare(prev, cur, "en")
    assert d["sha_known"] is False and d["files"]["changed"] == []


def test_page_data_marks_new_and_changed_files(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "main.ts", 'import "./keep";\n')
    write(project, "keep.ts", "export const k = 1;\n")
    prev, _ = make_run(runs, "20261010-090000", project)
    write(project, "main.ts", 'import "./keep";\nimport "./fresh";\n')
    write(project, "fresh.ts", "export const f = 1;\n")
    cur, g = make_run(runs, "20261012-090000", project)
    d = diff.compare(prev, cur, "zh")
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, {"evidence": {}, "promises": []}, {"findings": []},
                                project, "zh", False, diff=d)
    nodes = {n["id"]: n for n in data["nodes"]}
    assert nodes["fresh.ts"]["diff"] == "new" and nodes["main.ts"]["diff"] == "changed" and nodes["keep.ts"]["diff"] is None
    assert nodes["main.ts"]["card"]["diff_notes"] == ["比上次：内容改过", "比上次：新增调用 fresh.ts"]
    assert data["diff"]["counts"] == {"added": 1, "changed": 1, "removed": 0}


def test_previous_run_orders_same_second_runs_by_number_and_ignores_other_folders(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts")
    for name in ("20261022-170000", "20261022-170000-2", "20261022-170000-9"):
        make_run(runs, name, project)
    (runs / "notes").mkdir()  # not a run
    cur, _ = make_run(runs, "20261022-170000-10", project)
    assert diff.previous_run(cur).name == "20261022-170000-9"
    assert diff.previous_run(tmp_path / "missing" / "20261022-170000") is None


def test_identical_promises_are_compared_one_by_one(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts")
    prev, _ = make_run(runs, "20261010-090000", project, ledger={"evidence": {}, "compromises": [],
                       "promises": [promise("登录后才能用", "broken"), promise("登录后才能用", "broken")]})
    cur, _ = make_run(runs, "20261012-090000", project, ledger={"evidence": {}, "compromises": [],
                      "promises": [promise("登录后才能用", "kept"), promise("登录后才能用", "broken")]})
    assert diff.compare(prev, cur, "zh")["promises"]["changed"] == [{"plain": "登录后才能用", "before": "broken", "after": "kept"}]


def test_summary_line_follows_the_report_language(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts")
    prev, _ = make_run(runs, "20261010-090000", project)
    write(project, "b.ts")
    cur, _ = make_run(runs, "20261012-090000", project)
    d = diff.compare(prev, cur, "zh")
    assert diff.summary_line(d, "zh") == "和 2026-10-10 的运行相比：1 个新文件，0 个改过，0 个删掉；新风险 0 个，已解决 0 个"
    assert diff.summary_line(d, "en").startswith("Compared with the run of 2026-10-10: 1 new, 0 changed, 0 removed files")


def test_a_quiet_comparison_is_marked_quiet(tmp_path):
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts", "export const a = 1;\n")
    prev, _ = make_run(runs, "20261010-090000", project)
    cur, g = make_run(runs, "20261012-090000", project)
    d = diff.compare(prev, cur, "zh")
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, {"evidence": {}, "promises": []}, {"findings": []},
                                project, "zh", False, diff=d)
    assert data["diff"]["quiet"] is True


def test_a_reworded_promise_from_the_same_message_is_the_same_promise(tmp_path):
    """Each run's agent words a promise its own way; the message it came from does not change."""
    project, runs = tmp_path / "app", tmp_path / "runs"
    write(project, "a.ts")
    ev = {"E1": {"kind": "transcript", "msg_id": "u-7", "quote": "只有我能看到", "ok": True}}

    def said(plain, status):
        return {**promise(plain, status), "source": ["E1"]}
    prev, _ = make_run(runs, "20261010-090000", project, ledger={"evidence": ev, "compromises": [],
                       "promises": [said("只有我自己能看到我的笔记", "broken")]})
    cur, _ = make_run(runs, "20261012-090000", project, ledger={"evidence": ev, "compromises": [],
                      "promises": [said("笔记只给我自己看", "kept")]})
    assert diff.compare(prev, cur, "zh")["promises"] == {
        "changed": [{"plain": "笔记只给我自己看", "before": "broken", "after": "kept"}], "new": [], "gone": []}


def test_promises_pair_by_a_shared_message_whatever_question_or_extra_sources():
    old = [{"plain": "导出的全部记录可以直接当备份", "status": "kept", "type": "ai_claim", "msgs": {"a1"}},
           {"plain": "登录以后再做", "status": "pending", "type": "deferred", "msgs": {"u6"}}]
    new = [{"plain": "登录功能以后再做", "status": "kept", "type": "deferred", "msgs": {"u6", "a9"}},
           {"plain": "导出的 JSON 文件可以当备份用", "status": "kept", "type": "ai_claim", "msgs": {"a1"}},
           {"plain": "数据存在 data.json", "status": "kept", "type": "ai_claim", "msgs": {"a2"}}]
    pairs, fresh, gone = diff._pair_promises(old, new)
    assert {(a["plain"], b["plain"]) for a, b in pairs} == {("导出的全部记录可以直接当备份", "导出的 JSON 文件可以当备份用"),
                                                         ("登录以后再做", "登录功能以后再做")}
    assert [n["plain"] for n in fresh] == ["数据存在 data.json"] and gone == []
