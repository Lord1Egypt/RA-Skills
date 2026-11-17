import json

import graph

NO_PROBES = {"findings": []}


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_entries_for_each_stack(tmp_path):
    write(tmp_path, "app/page.tsx", "export default function P() {}")
    write(tmp_path, "app/api/chat/route.ts", "export async function POST() {}")
    write(tmp_path, "pages/_app.tsx")
    write(tmp_path, "pages/about.tsx")
    write(tmp_path, "manifest.json", json.dumps({
        "manifest_version": 3, "background": {"service_worker": "src/background.js"},
        "content_scripts": [{"js": ["src/content.js"]}], "side_panel": {"default_path": "src/panel/panel.html"}}))
    write(tmp_path, "src/background.js")
    write(tmp_path, "src/content.js")
    write(tmp_path, "src/panel/panel.html", '<script type="module" src="panel.js"></script>')
    write(tmp_path, "src/panel/panel.js")
    write(tmp_path, "index.html", '<script type="module" src="/src/main.ts"></script><script src="https://cdn.example/x.js"></script>')
    write(tmp_path, "src/main.ts")
    write(tmp_path, "package.json", json.dumps({"main": "./server/index.js", "bin": {"tool": "bin/cli.js"},
                                                "dependencies": {"next": "15.0.0"}}))
    write(tmp_path, "server/index.js", "app.listen(3000);")
    write(tmp_path, "bin/cli.js")
    write(tmp_path, "worker.js", "server.listen(8080);")
    write(tmp_path, "tools/run.py", 'if __name__ == "__main__":\n    main()\n')
    write(tmp_path, "app.py")
    files, _ = graph.collect_files(tmp_path)
    entries = graph.find_entries(tmp_path, files)
    assert set(entries) == {"app/page.tsx", "app/api/chat/route.ts", "pages/about.tsx", "src/background.js",
                            "src/content.js", "src/panel/panel.js", "src/main.ts", "server/index.js", "bin/cli.js",
                            "worker.js", "tools/run.py", "app.py"}
    assert entries["src/panel/panel.js"] == "manifest side panel → src/panel/panel.html"
    assert entries["server/index.js"] == "package.json main"
    assert entries["worker.js"] == "starts a server (.listen)"


def test_pages_folder_is_ordinary_code_outside_nextjs(tmp_path):
    write(tmp_path, "index.html", '<script type="module" src="/src/main.tsx"></script>')
    write(tmp_path, "src/main.tsx", 'import "./pages/home";\n')
    write(tmp_path, "src/pages/home.tsx", "export default function Home() {}\n")
    write(tmp_path, "app/page.tsx", "export default function P() {}\n")
    write(tmp_path, "package.json", json.dumps({"dependencies": {"react": "18.3.1"}}))
    files, _ = graph.collect_files(tmp_path)
    assert graph.find_entries(tmp_path, files) == {"src/main.tsx": "index.html script"}
    write(tmp_path, "next.config.mjs", "export default {};\n")
    assert set(graph.find_entries(tmp_path, files)) == {"src/main.tsx", "src/pages/home.tsx", "app/page.tsx"}


def test_build_edges_unresolved_and_fallback_entries(tmp_path):
    write(tmp_path, "src/a.ts", 'import { run } from "./b";\nimport x from "./missing";\n')
    write(tmp_path, "src/b.ts", "export function run() {}\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    assert g["edges"] == [{"from": "src/a.ts", "to": "src/b.ts", "line": 1, "names": ["run"]}]
    assert g["unresolved"] == [{"from": "src/a.ts", "spec": "./missing", "line": 2}]
    assert g["entries"] == [{"path": "src/a.ts", "reason": "not imported by any file"}]
    nodes = {n["id"]: n for n in g["nodes"]}
    assert nodes["src/a.ts"]["role"] == "entry" and nodes["src/b.ts"]["role"] == "logic"
    assert nodes["src/b.ts"]["exports"] == [{"name": "run", "line": 1}]
    assert g["languages"] == ["js"] and g["collapsed"] is False


def test_import_cycles_are_kept_and_self_imports_dropped(tmp_path):
    write(tmp_path, "src/a.ts", 'import { b } from "./b";\nexport const a = 1;\n')
    write(tmp_path, "src/b.ts", 'import { a } from "./a";\nexport const b = 2;\n')
    write(tmp_path, "src/self.ts", 'import "./self";\n')
    g = graph.build(tmp_path, [], NO_PROBES)
    assert {(e["from"], e["to"]) for e in g["edges"]} == {("src/a.ts", "src/b.ts"), ("src/b.ts", "src/a.ts")}
    assert g["entries"] == [{"path": "src/self.ts", "reason": "not imported by any file"}]


def test_externals_from_packages_urls_and_storage(tmp_path):
    write(tmp_path, "src/ai.ts", 'import OpenAI from "openai";\nimport { createClient } from "@supabase/supabase-js";\n'
                                 'import _ from "lodash";\nconst r = await fetch("https://api.anthropic.com/v1/messages");\n'
                                 'localStorage.setItem("k", "v");\nimport { getApp } from "firebase/app";\n')
    write(tmp_path, "src/db.py", "import sqlite3\nimport requests\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    ext = {e["id"]: e for e in g["externals"]}
    assert set(ext) == {"ext:openai", "ext:supabase", "ext:anthropic", "ext:local-storage", "ext:firebase", "ext:sqlite"}
    assert ext["ext:openai"]["kind"] == "paid" and ext["ext:supabase"]["kind"] == "data"
    assert ext["ext:anthropic"]["evidence"] == [
        {"path": "src/ai.ts", "line": 4, "snippet": 'const r = await fetch("https://api.anthropic.com/v1/messages");'}]
    edges = {(e["from"], e["to"]) for e in g["edges"]}
    assert ("src/ai.ts", "ext:openai") in edges and ("src/db.py", "ext:sqlite") in edges
    assert all(not e["to"].startswith("ext:lodash") for e in g["edges"])


def test_exports_js_and_python():
    js = ("export default function Home() {}\nexport async function load() {}\nexport const API = 1;\n"
          "export class Store {}\nconst a = 1, b = 2;\nexport { a, b as bee };\nexports.legacy = () => 1;\n"
          "module.exports = { one, two };\nexport { helper } from './helper';\n")
    assert [(e["name"], e["line"]) for e in graph.exports(js, "js")] == [
        ("Home", 1), ("load", 2), ("API", 3), ("Store", 4), ("a", 6), ("bee", 6), ("legacy", 7), ("one", 8), ("two", 8)]
    py = "def run():\n    pass\nclass Store:\n    def method(self): pass\ndef _private(): pass\nasync def fetch(): pass\n"
    assert [(e["name"], e["line"]) for e in graph.exports(py, "py")] == [("run", 1), ("Store", 3), ("fetch", 6)]


def test_large_project_collapses_into_folders(tmp_path):
    for d in ("src/ai", "src/ui", "src/db", "src/util"):
        for i in range(40):
            write(tmp_path, f"{d}/f{i}.ts")
    write(tmp_path, "src/main.ts")
    g = graph.build(tmp_path, [], NO_PROBES)
    assert g["collapsed"] is True
    assert [f["id"] for f in g["folders"]] == ["src/ai", "src/db", "src/ui", "src/util"]
    assert all(len(f["files"]) == 40 for f in g["folders"])
    assert "src/main.ts" not in {x for f in g["folders"] for x in f["files"]}


def test_folder_groups_skip_single_file_groups():
    paths = ["a/x.ts", "a/y.ts", "b/z.ts", "c/w.ts", "c/v.ts", "root.ts"]
    assert graph.folder_groups(paths) == [{"id": "a", "files": ["a/x.ts", "a/y.ts"]},
                                          {"id": "c", "files": ["c/v.ts", "c/w.ts"]}]


def test_scores_and_explain_selection(tmp_path):
    write(tmp_path, "index.html", '<script type="module" src="/src/main.ts"></script>')
    write(tmp_path, "src/main.ts", 'import "./ai";\nimport "./util";\n')
    write(tmp_path, "src/ai.ts", 'import OpenAI from "openai";\nimport "./util";\n')
    write(tmp_path, "src/util.ts")
    write(tmp_path, "src/lonely.ts")
    probes = {"findings": [{"path": "src/ai.ts", "level": "certain", "message": "m", "line": 1},
                           {"path": "src/util.ts", "level": "hint", "message": "m", "line": 1}]}
    recs = [{"kind": "edit", "files": [str(tmp_path / "src/util.ts")], "ts": f"2026-09-12T09:0{i}:00Z"} for i in range(6)]
    g = graph.build(tmp_path, recs, probes)
    nodes = {n["id"]: n for n in g["nodes"]}
    assert {k: v["score"] for k, v in nodes.items()} == {"src/main.ts": 3, "src/ai.ts": 6, "src/util.ts": 5, "src/lonely.ts": 0}
    assert {k for k, v in nodes.items() if v["explain"]} == {"src/main.ts", "src/ai.ts", "src/util.ts"}
    assert nodes["src/util.ts"]["edits"] == {"count": 6, "first": "2026-09-12T09:00:00Z", "last": "2026-09-12T09:05:00Z"}
    assert nodes["src/lonely.ts"]["edits"] is None


def test_explain_pack_lists_files_and_groups(tmp_path):
    write(tmp_path, "src/main.ts", "".join(f'import "./m{i}";\n' for i in range(10)))
    for i in range(10):
        write(tmp_path, f"src/m{i}.ts", f"export function f{i}() {{}}\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    pack = graph.explain_pack(g, tmp_path, NO_PROBES)
    assert "## Group 2 → parts/explain_02.json" in pack and "### src/main.ts" in pack
    assert "- exports: f3 (line 1)" in pack and "- used by: src/main.ts" in pack
    write(tmp_path / "small", "main.ts", 'import "./a";\n')
    write(tmp_path / "small", "a.ts", "export const a = 1;\n")
    small = graph.build(tmp_path / "small", [], NO_PROBES)
    assert "Group" not in graph.explain_pack(small, tmp_path / "small", NO_PROBES)


def test_explain_pack_asks_for_journeys_from_the_entry_points(tmp_path):
    write(tmp_path, "index.html", '<script type="module" src="/src/main.ts"></script>')
    write(tmp_path, "src/main.ts", 'import "./a";\n')
    write(tmp_path, "src/a.ts", "export const a = 1;\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    pack = graph.explain_pack(g, tmp_path, NO_PROBES)
    assert "## Journeys" in pack and "- src/main.ts (index.html script)" in pack and "after `vl.py merge`" not in pack
    write(tmp_path / "many", "src/main.ts", "".join(f'import "./m{i}";\n' for i in range(10)))
    for i in range(10):
        write(tmp_path / "many", f"src/m{i}.ts", f"export function f{i}() {{}}\n")
    many = graph.explain_pack(graph.build(tmp_path / "many", [], NO_PROBES), tmp_path / "many", NO_PROBES)
    assert "after `vl.py merge`" in many


def test_an_oversized_folder_group_is_split_further(tmp_path):
    for sub in ("a", "b", "c", "d"):
        for i in range(35):
            write(tmp_path, f"src/{sub}/f{i}.ts")
    write(tmp_path, "docs/x.ts")
    write(tmp_path, "scripts/y.ts")
    g = graph.build(tmp_path, [], NO_PROBES)
    assert g["collapsed"] is True
    assert [f["id"] for f in g["folders"]] == ["src/a", "src/b", "src/c", "src/d"]  # not one 140-file "src"
    flat = ["solo/f%d.ts" % i for i in range(60)] + ["one/x.ts", "two/y.ts"]
    assert [f["id"] for f in graph.folder_groups(flat)] == ["solo"]  # nothing below it to split into: kept whole


def _git_init(root):
    import subprocess
    subprocess.run(["git", "init", "-q", str(root)], check=True)


def test_git_ignored_files_are_left_out_and_counted(tmp_path):
    # generated output a tool writes into the project (here excluded through .git/info/exclude,
    # which a .gitignore-only check would miss) is not the project's code
    _git_init(tmp_path)
    (tmp_path / ".git" / "info").mkdir(exist_ok=True)
    (tmp_path / ".git" / "info" / "exclude").write_text(".superpowers/\n")
    write(tmp_path, ".gitignore", "gen/\n")
    write(tmp_path, "src/a.ts", 'import "./b";\n')
    write(tmp_path, "src/b.ts")
    write(tmp_path, "src/new.ts")  # untracked but not ignored: still the project's code
    write(tmp_path, ".superpowers/films/x/kit.ts", "// TODO: generated\n")
    write(tmp_path, "gen/out.py", "# TODO: generated\n")
    files, excluded = graph.collect_files(tmp_path)
    assert sorted(files) == ["src/a.ts", "src/b.ts", "src/new.ts"]
    assert excluded["ignored by git"] == 2
    import candidates
    assert candidates.scan_code_todos(tmp_path) == []


def test_collect_files_without_git_keeps_everything(tmp_path):
    write(tmp_path, ".gitignore", "gen/\n")
    write(tmp_path, "gen/out.py")
    files, excluded = graph.collect_files(tmp_path)
    assert sorted(files) == ["gen/out.py"] and not excluded["ignored by git"]


def test_explain_selection_breaks_score_ties_by_real_fan_in(tmp_path):
    # both hubs hit the capped score; the one more files depend on must win, not the one
    # earlier in the alphabet
    write(tmp_path, "src/a_minor.ts")
    write(tmp_path, "src/z_core.ts")
    for i in range(6):
        write(tmp_path, f"src/m{i}.ts", 'import "./a_minor";\nimport "./z_core";\n')
    for i in range(6, 12):
        write(tmp_path, f"src/m{i}.ts", 'import "./z_core";\n')
    import graph as gmod
    old = gmod.EXPLAIN_MAX
    gmod.EXPLAIN_MAX = 1
    try:
        g = graph.build(tmp_path, [], NO_PROBES)
    finally:
        gmod.EXPLAIN_MAX = old
    nodes = {n["id"]: n for n in g["nodes"]}
    assert nodes["src/a_minor.ts"]["score"] == nodes["src/z_core.ts"]["score"]
    assert [k for k, v in nodes.items() if v["explain"]] == ["src/z_core.ts"]


def test_explain_selection_keeps_one_folder_to_half_the_slots(tmp_path):
    # every script is an entry, so a scripts/ folder would take every slot; the
    # selection keeps room for the other half of the project
    for i in range(8):  # each script is an entry AND imported by the next: they outrank web/
        write(tmp_path, f"scripts/s{i}.py", f'import s{(i + 1) % 8}\nif __name__ == "__main__":\n    pass\n')
    write(tmp_path, "web/core.ts")
    write(tmp_path, "web/util.ts")
    for i in range(3):
        write(tmp_path, f"web/page{i}.ts", 'import "./core";\nimport "./util";\n')
    import graph as gmod
    old = gmod.EXPLAIN_MAX
    gmod.EXPLAIN_MAX = 4
    try:
        g = graph.build(tmp_path, [], NO_PROBES)
        chosen = [n["id"] for n in g["nodes"] if n["explain"]]
        assert sum(c.startswith("scripts/") for c in chosen) == 2 and len(chosen) == 4
        # with nothing else to pick, the cap gives the slots back
        for p in list(tmp_path.joinpath("web").iterdir()):
            p.unlink()
        g = graph.build(tmp_path, [], NO_PROBES)
        assert sum(n["explain"] for n in g["nodes"]) == 4
    finally:
        gmod.EXPLAIN_MAX = old


def test_paid_ai_hosts_beyond_the_us_majors(tmp_path):
    write(tmp_path, "tts.py", 'INTL = "https://api.minimax.io/v1/t2a_v2"\nCN = "https://api.minimax.chat/v1/t2a_v2"\n')
    write(tmp_path, "chat.py", 'URL = "https://api.moonshot.cn/v1/chat/completions"\n'
                              'QWEN = "https://dashscope.aliyuncs.com/api/v1"\n')
    write(tmp_path, "fast.ts", 'fetch("https://api.groq.com/openai/v1/chat/completions")\n'
                               'fetch("https://api.mistral.ai/v1/chat/completions")\n')
    g = graph.build(tmp_path, [], NO_PROBES)
    ext = {e["id"]: e["kind"] for e in g["externals"]}
    assert ext == {"ext:minimax": "paid", "ext:moonshot": "paid", "ext:dashscope": "paid",
                   "ext:groq": "paid", "ext:mistral": "paid"}
    tts = next(e for e in g["externals"] if e["id"] == "ext:minimax")
    assert [(ev["path"], ev["line"]) for ev in tts["evidence"]] == [("tts.py", 1)]  # first hit per file


def test_a_page_with_its_own_script_is_code_and_links_to_the_server_it_calls(tmp_path):
    code = "  const rows = [];\n" * 20  # real page logic, well over a one-liner
    write(tmp_path, "public/index.html",
          f'<link rel="stylesheet" href="/style.css"><script>\n{code}'
          "async function load(month) {\n  const url = '/api/expenses?month=' + month;\n"
          "  return (await fetch(url)).json();\n}\nfetch('/logo.png');\n</script>\n<p>'/api/not-in-a-script'</p>\n")
    write(tmp_path, "public/about.html", "<h1>About</h1><script>var x = 1;</script>")  # markup and a one-liner
    write(tmp_path, "server.js", "const http = require('http');\n"
          "http.createServer((q, s) => { if (q.url.startsWith('/api/expenses')) s.end('[]'); "
          "if (q.url === '/logo.png') s.end(); if (q.url === '/api/not-in-a-script') s.end(); }).listen(3000);\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    ids = {n["id"] for n in g["nodes"]}
    assert "public/index.html" in ids and "public/about.html" not in ids
    entries = {e["path"]: e["reason"] for e in g["entries"]}
    assert entries["public/index.html"] == "page with its own script"
    links = [(e["from"], e["to"], e["names"]) for e in g["edges"]]
    assert links == [("public/index.html", "server.js", ["/api/expenses"])]  # not the image, not text outside the script
