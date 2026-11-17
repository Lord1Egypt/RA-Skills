import json
import re

import graph
from helpers.graph_fixture import OPENAI, make_project, write
from ledger_report import graph_page, i18n
from ledger_report.bits import width


def setup(tmp_path, purpose="把文字发给 OpenAI 总结。"):
    root, g, explained, ledger, probes = make_project(tmp_path, purpose=purpose)
    return graph_page.page_data(g, explained, ledger, probes, root, "zh", True)


def test_nodes_roles_states_badges_and_edges(tmp_path):
    data = setup(tmp_path)
    nodes = {n["id"]: n for n in data["nodes"]}
    assert set(nodes) == {"app/page.tsx", "lib/ai.ts", "lib/util.ts", "ext:openai"}
    assert nodes["ext:openai"]["role"] == "paid" and nodes["lib/ai.ts"]["role"] == "logic"
    assert nodes["lib/ai.ts"]["state"] == "bad" and nodes["lib/ai.ts"]["badge"] == "1 个问题"
    assert nodes["lib/util.ts"]["state"] == "warn" and nodes["lib/util.ts"]["badge"] == "1 个提示"
    assert nodes["app/page.tsx"]["state"] == "ok" and nodes["app/page.tsx"]["badge"] == ""
    edges = {(e["from"], e["to"]): e for e in data["edges"]}
    assert edges[("app/page.tsx", "lib/ai.ts")]["risky"] is True and edges[("app/page.tsx", "lib/ai.ts")]["names"] == ["summarize"]
    assert data["summary"] == "3 个文件，1 个入口，连到 1 个外部服务（其中 1 个按次收费）。"  # app/page.tsx is a Next.js entry
    assert data["top"] == ["lib/ai.ts", "lib/util.ts"] and len(data["howto"]) == 3
    assert data["strings"]["g_tab_graph"] == "文件流程图"


def test_explained_and_automatic_cards(tmp_path):
    data = setup(tmp_path)
    cards = {n["id"]: n["card"] for n in data["nodes"]}
    ai = cards["lib/ai.ts"]
    assert ai["explained"] and ai["purpose_plain"] == "把文字发给 OpenAI 总结。"
    assert [f["name"] for f in ai["functions"]] == ["summarize"]
    assert ai["snippets"][0]["code"].startswith("export async function summarize(t) {")
    assert ai["promises"] == [{"id": "P1", "status": "broken", "glyph": "❌", "plain": "不要让陌生人花我的钱"}]
    assert ai["risks"][0]["level"] == "bad" and ai["called_by"] == ["app/page.tsx"] and ai["calls"] == ["ext:openai"]
    util = cards["lib/util.ts"]
    assert not util["explained"] and "对外提供 1 个名字：x。" in util["auto"]
    ext = cards["ext:openai"]
    assert "OpenAI API：项目里有 1 个文件连到它。" == ext["auto"] and ext["evidence"][0]["where"] == "lib/ai.ts:1"
    assert ai["history_note"] == "对话里没找到和这个文件有关的记录"


def test_page_data_masks_secrets_and_escapes_script_close(tmp_path):
    data = setup(tmp_path, purpose=f"注意 </script><b>x</b> 密钥 {OPENAI}")
    script = graph_page.data_script(data)
    assert OPENAI not in script and "</script><b>" not in script and "\\u003c/script>" in script
    inner = re.search(r'<script type="application/json" id="vl-data">(.*)</script>$', script, re.S).group(1)
    back = json.loads(inner)
    purpose = {n["id"]: n for n in back["nodes"]}["lib/ai.ts"]["card"]["purpose_plain"]
    assert purpose.startswith("注意 </script><b>x</b>") and "sk-proj-…" in purpose


def test_card_text_is_fitted_but_full_text_is_kept(tmp_path):
    write(tmp_path, "components/SubscriptionCheckoutConfirmationDialog.tsx", "export const a = 1;\n")
    data = setup(tmp_path, purpose="这个文件负责把用户输入的长文本切成小段，再逐段发给模型总结")
    nodes = {n["id"]: n for n in data["nodes"]}
    long = nodes["components/SubscriptionCheckoutConfirmationDialog.tsx"]
    assert long["label"] == "SubscriptionCheckoutConfirmationDialog.tsx"
    assert long["short"].endswith("…") and width(long["short"]) <= graph_page.LABEL_UNITS
    ai = nodes["lib/ai.ts"]
    assert ai["short"] == "ai.ts" and ai["sub"].endswith("…") and width(ai["sub"]) <= graph_page.SUB_UNITS
    assert ai["card"]["purpose_plain"].endswith("总结")  # the panel keeps the whole sentence


def test_coverage_lists_what_the_flowchart_left_out(tmp_path):
    root, g, explained, ledger, probes = make_project(tmp_path)
    g["unresolved"] = [{"from": "lib/ai.ts", "spec": "./gone", "line": 9}]
    g["excluded"] = {"tests": 2, "config": 1}
    explained["rejected"] = [{"path": "lib/nope.ts", "reason": "not a file in the graph"}]
    explained["files"]["lib/ai.ts"]["dropped_functions"] = [{"name": "sendEmail", "reason": "not defined in this file"}]
    cov = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)["coverage"]
    assert cov["excluded"] == {"tests": 2, "config": 1} and cov["unresolved"][0]["spec"] == "./gone"
    assert cov["rejected"] == [{"path": "lib/nope.ts", "reason": "not a file in the graph"}]
    assert cov["dropped"] == [{"path": "lib/ai.ts", "name": "sendEmail", "reason": "not defined in this file"}]


def test_render_graph_tab_skeleton():
    html = graph_page.render_graph_tab("zh")
    for needle in ('id="vlg-svg"', 'id="vlg-viewport"', 'id="vlg-panel"', 'data-act="fit"', "红框 = 有问题", "✦ = 按次收费"):
        assert needle in html


def test_dagre_source_is_vendored_and_stripped():
    src = graph_page.dagre_source()
    assert src.startswith('"use strict";var dagre=') and "sourceMappingURL" not in src
    assert (graph_page.VENDOR_DIR / "LICENSE-dagre").read_text(encoding="utf-8").startswith("Copyright")


def test_graph_strings_exist_in_both_languages():
    zh = {k for k in i18n.STR["zh"] if k.startswith("g_")}
    en = {k for k in i18n.STR["en"] if k.startswith("g_")}
    assert zh == en and len(zh) >= 50


def test_probe_messages_are_translated_for_chinese_pages():
    from ledger_report.i18n import probe_message
    cases = {
        "This server endpoint calls a paid service (OpenAI API) and no login check was found in the file":
            "这个服务器接口会调用付费服务（OpenAI API），但文件里没找到登录检查",
        "Row level security is switched off for table notes: anyone with the public anon key can read and change every row":
            "表 notes 关掉了行级访问规则（RLS）：拿到公开 anon key 的人都能读、改每一行",
        "cors() with no options allows every website to call this server, and it also accepts the visitor's cookies and credentials":
            "cors() 没有设置限制，任何网站都能调用这个服务器，而且会带上访问者的 cookie 和登录凭据",
        "A policy on table read lets everyone read/write every row (using true)": "表 read 的一条规则让所有人都能读、改每一行（using true）",
    }
    for en, zh in cases.items():
        assert probe_message(en, "zh") == zh
        assert probe_message(en, "en") == en
    assert probe_message("A message no rule knows", "zh") == "A message no rule knows"


def test_panel_risks_use_the_page_language(tmp_path):
    root, g, explained, ledger, probes = make_project(tmp_path)
    probes["findings"][0]["message"] = "A OpenAI secret is written directly in the code"
    util = {n["id"]: n for n in graph_page.page_data(g, explained, ledger, probes, root, "zh", True)["nodes"]}["lib/util.ts"]
    assert util["card"]["risks"][0]["text"] == "代码里直接写着一个 OpenAI 密钥"


def test_every_fixture_probe_message_has_a_chinese_version():
    from pathlib import Path

    import probes as probe_mod
    from ledger_report.i18n import probe_message
    apps = Path(__file__).resolve().parent / "fixtures" / "apps"
    seen = []
    for app in sorted(apps.iterdir()):
        for f in probe_mod.run_all(app)["findings"]:
            if f["level"] in ("certain", "hint"):
                seen.append(f["message"])
                assert probe_message(f["message"], "zh") != f["message"], f["message"]
    assert len(seen) >= 5


def journey_data(tmp_path, lang="zh"):
    root, g, explained, ledger, probes = make_project(tmp_path)
    explained["journeys"] = [{"id": "J1", "title": "你点「总结」时", "outcome": "总结出现在页面上", "dropped_steps": [],
                              "steps": [{"file": "app/page.tsx", "plain": "页面把文字交出去"},
                                        {"file": "lib/ai.ts", "plain": "发给 OpenAI", "function": "summarize", "line": 2,
                                         "line_corrected": False, "linked": True},
                                        {"file": "lib/ai.ts", "plain": "拿回总结", "linked": True}]}]
    explained["rejected_journeys"] = [{"title": "编的路线", "reason": "fewer than 2 steps are files in the graph"}]
    return graph_page.page_data(g, explained, ledger, probes, root, lang, True)


def test_journeys_and_each_files_place_in_them(tmp_path):
    data = journey_data(tmp_path)
    assert [j["title"] for j in data["journeys"]] == ["你点「总结」时"]
    assert [s["file"] for s in data["journeys"][0]["steps"]] == ["app/page.tsx", "lib/ai.ts", "lib/ai.ts"]
    cards = {n["id"]: n["card"] for n in data["nodes"]}
    assert cards["lib/ai.ts"]["positions"] == [
        {"journey": "J1", "text": "你点「总结」时，第 2/3 步：发给 OpenAI"},
        {"journey": "J1", "text": "你点「总结」时，第 3/3 步：拿回总结"}]
    assert cards["lib/util.ts"]["positions"] == []
    assert data["strings"]["g_position_none"] and data["has_journeys"] is True
    assert data["coverage"]["dropped"][-1] == {"path": "编的路线", "name": "", "reason": "fewer than 2 steps are files in the graph"}


def test_no_journeys_means_no_position_section(tmp_path):
    root, g, explained, ledger, probes = make_project(tmp_path)
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    assert data["journeys"] == [] and data["has_journeys"] is False


def test_page_data_cannot_open_a_script_double_escape(tmp_path):
    data = setup(tmp_path, purpose="before <!--<script> after </script> end")
    script = graph_page.data_script(data)
    inner = re.search(r'<script type="application/json" id="vl-data">(.*)</script>$', script, re.S).group(1)
    assert "<" not in inner  # no "<!--", "<script" or "</" can reach the HTML tokenizer
    back = json.loads(inner)
    assert {n["id"]: n for n in back["nodes"]}["lib/ai.ts"]["card"]["purpose_plain"] == "before <!--<script> after </script> end"


def test_graph_tab_has_a_skip_link_to_the_panel():
    html = graph_page.render_graph_tab("zh")
    assert 'class="vlg-skip" href="#vlg-panel"' in html and "跳到讲解面板" in html
    assert 'id="vlg-panel" tabindex="-1"' in html


def test_cards_carry_the_names_each_link_imports(tmp_path):
    data = setup(tmp_path)
    cards = {n["id"]: n["card"] for n in data["nodes"]}
    assert cards["lib/ai.ts"]["caller_names"] == {"app/page.tsx": ["summarize"]}
    assert cards["app/page.tsx"]["call_names"] == {"lib/ai.ts": ["summarize"]}


def _views_project(tmp_path):
    write(tmp_path, "manifest.json", '{"manifest_version": 3, "background": {"service_worker": "src/background.js"}}')
    write(tmp_path, "src/background.js", 'import "./ui/panel";\n')
    write(tmp_path, "src/ui/panel.js", 'import "./view";\nimport "../ai/client";\n')
    write(tmp_path, "src/ui/view.js", "export const v = 1;\n")
    write(tmp_path, "src/ai/client.js", 'import OpenAI from "openai";\nimport "./prompts";\n')
    write(tmp_path, "src/ai/prompts.js", "export const p = 1;\n")
    write(tmp_path, "src/store/save.js", 'localStorage.setItem("k", "v");\n')
    write(tmp_path, "src/store/load.js", "export const l = 1;\n")
    write(tmp_path, "scripts/a.mjs", 'import "../src/ai/client.js";\n')
    write(tmp_path, "scripts/b.mjs", "export const b = 1;\n")
    return graph.build(tmp_path, [], {"findings": []})


def test_every_file_gets_a_module(tmp_path):
    g = _views_project(tmp_path)
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, {"evidence": {}, "promises": []}, {"findings": []},
                                tmp_path, "zh", False)
    mods = {m["id"]: m["files"] for m in data["modules"]}
    assert mods == {"src/ai": ["src/ai/client.js", "src/ai/prompts.js"], "src/store": ["src/store/load.js", "src/store/save.js"],
                    "src/ui": ["src/ui/panel.js", "src/ui/view.js"], "scripts": ["scripts/a.mjs", "scripts/b.mjs"]}
    assert {m["id"]: m["sub"] for m in data["modules"]}["scripts"] == "2 个文件 · 点开展开"  # background.js stays a single card


def test_data_flow_keeps_the_paths_from_entries_to_data_and_labels_them(tmp_path):
    g = _views_project(tmp_path)
    ledger = {"evidence": {"E1": {"kind": "code", "path": "src/ai/client.js", "line": 1, "snippet": "x", "ok": True}},
              "promises": [], "compromises": [],
              "map": {"nodes": [{"id": "panel", "lane": "browser", "kind": "page", "label": "面板", "holds": [], "paid": False, "evidence": []},
                                {"id": "oa", "lane": "storage", "kind": "third_party", "label": "OpenAI", "holds": [], "paid": True,
                                 "evidence": ["E1"]}],
                      "edges": [{"from": "panel", "to": "oa", "carries": "简历和职位", "risk": None, "evidence": ["E1"]}]}}
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, ledger, {"findings": []}, tmp_path, "zh", False)
    flow = data["data_flow"]
    assert flow["files"] == ["src/ai/client.js", "src/background.js", "src/ui/panel.js"]  # save.js is not on an entry's path
    assert flow["labels"] == {"src/ai/client.js\u0001ext:openai": "简历和职位"}


def test_data_flow_labels_a_store_named_differently_through_its_evidence(tmp_path):
    g = _views_project(tmp_path)
    ledger = {"evidence": {"E2": {"kind": "code", "path": "src/store/save.js", "line": 1, "snippet": "x", "ok": True}},
              "promises": [], "compromises": [],
              "map": {"nodes": [{"id": "page", "lane": "browser", "kind": "page", "label": "页面", "holds": [], "paid": False, "evidence": []},
                                {"id": "ls", "lane": "storage", "kind": "storage", "label": "浏览器本地存储", "holds": ["笔记"],
                                 "paid": False, "evidence": ["E2"]}],
                      "edges": [{"from": "page", "to": "ls", "carries": "笔记", "risk": None, "evidence": ["E2"]}]}}
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, ledger, {"findings": []}, tmp_path, "zh", False)
    assert data["data_flow"]["labels"] == {"src/store/save.js\u0001ext:local-storage": "笔记"}
