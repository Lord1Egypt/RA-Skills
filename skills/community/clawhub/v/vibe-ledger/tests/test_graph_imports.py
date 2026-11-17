import graph


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


JS = '''import React from "react";
import {
  runA,
  runB as other,
} from "./ai/client";
import "./styles.css";
export { helper } from "../shared/helper.js";
export * from "./types";
// import ghost from "./ghost";
/* import alsoGhost from "./ghost2"; */
const lazy = import("./lazy");
const fs = require("fs");
const local = require("./local.cjs");
export const notAnImport = "from here";
'''


def test_es_cjs_dynamic_and_reexport_imports():
    got = graph.js_imports(JS)
    specs = [(s, line) for s, line, _ in got]
    assert specs == [("react", 1), ("./ai/client", 2), ("./styles.css", 6), ("../shared/helper.js", 7),
                     ("./types", 8), ("./lazy", 11), ("fs", 12), ("./local.cjs", 13)]
    names = dict((s, n) for s, _, n in got)
    assert names["./ai/client"] == ["runA", "runB", "other"] and names["react"] == ["React"]


def test_comment_blanking_keeps_line_numbers():
    text = "/* a\nb */\nimport x from './x';\n"
    assert graph.js_imports(text) == [("./x", 3, ["x"])]
    assert graph.strip_comments(text, "js").count("\n") == text.count("\n")


def test_python_imports():
    text = "import os, app.db\nfrom . import views, models\nfrom ..core.auth import login  # comment\n# import ghost\nfrom flask import Flask\n"
    assert graph.py_imports(text) == [
        ("", "os", 1, []), ("", "app.db", 1, []), (".", "", 2, ["views", "models"]),
        ("..", "core.auth", 3, ["login"]), ("", "flask", 5, ["Flask"])]


def test_relative_index_and_extension_resolution(tmp_path):
    write(tmp_path, "src/ai/client.ts")
    write(tmp_path, "src/ui/index.tsx")
    write(tmp_path, "src/app.ts")
    assert graph.resolve_js("./ai/client", "src/app.ts", tmp_path, []) == ("file", "src/ai/client.ts")
    assert graph.resolve_js("./ui", "src/app.ts", tmp_path, []) == ("file", "src/ui/index.tsx")
    assert graph.resolve_js("./nope", "src/app.ts", tmp_path, []) == ("missing", None)
    assert graph.resolve_js("react", "src/app.ts", tmp_path, []) == ("package", "react")
    assert graph.resolve_js("@supabase/supabase-js", "src/app.ts", tmp_path, []) == ("package", "@supabase/supabase-js")


def test_js_extension_import_resolves_to_ts_source(tmp_path):
    write(tmp_path, "src/util.ts")
    assert graph.resolve_js("./util.js", "src/main.ts", tmp_path, []) == ("file", "src/util.ts")


def test_tsconfig_with_comments_and_trailing_commas(tmp_path):
    write(tmp_path, "tsconfig.json", '''{
      // editor settings
      "compilerOptions": {
        "baseUrl": ".",
        /* aliases */
        "paths": { "@lib/*": ["./src/lib/*"], "@cfg": ["./src/config.ts"], },
        "url": "http://example.com/not-a-comment",
      },
    }''')
    write(tmp_path, "src/lib/db.ts")
    write(tmp_path, "src/config.ts")
    aliases = graph.load_aliases(tmp_path)
    assert ("@lib/", ["src/lib"], True) in aliases and ("@cfg", ["src/config.ts"], False) in aliases
    assert graph.resolve_js("@lib/db", "src/app.ts", tmp_path, aliases) == ("file", "src/lib/db.ts")
    assert graph.resolve_js("@cfg", "src/app.ts", tmp_path, aliases) == ("file", "src/config.ts")


def test_at_alias_falls_back_to_src_then_root_and_vite_absolute(tmp_path):
    write(tmp_path, "src/lib/a.ts")
    write(tmp_path, "lib/b.ts")
    assert graph.resolve_js("@/lib/a", "app/page.tsx", tmp_path, []) == ("file", "src/lib/a.ts")
    assert graph.resolve_js("@/lib/b", "app/page.tsx", tmp_path, []) == ("file", "lib/b.ts")
    assert graph.resolve_js("~/lib/b", "app/page.tsx", tmp_path, []) == ("file", "lib/b.ts")
    assert graph.resolve_js("/src/lib/a.ts", "index.html", tmp_path, []) == ("file", "src/lib/a.ts")


def test_resolution_never_leaves_the_project(tmp_path):
    root = tmp_path / "app"
    write(root, "src/a.ts")
    write(tmp_path, "outside.ts")
    assert graph.resolve_js("../../outside", "src/a.ts", root, []) == ("missing", None)


def test_resolve_py_relative_and_absolute(tmp_path):
    write(tmp_path, "app/__init__.py")
    write(tmp_path, "app/views.py")
    write(tmp_path, "app/core/auth.py")
    write(tmp_path, "app/api/routes.py")
    assert graph.resolve_py(".", "missing_mod", "app/views.py", tmp_path) == ("missing", None)
    assert graph.resolve_py("..", "core.auth", "app/api/routes.py", tmp_path) == ("file", "app/core/auth.py")
    assert graph.resolve_py("", "app.views", "main.py", tmp_path) == ("file", "app/views.py")
    assert graph.resolve_py("", "app", "main.py", tmp_path) == ("file", "app/__init__.py")
    assert graph.resolve_py("", "flask", "main.py", tmp_path) == ("package", "flask")


def test_resolve_py_finds_sibling_modules_of_a_script_folder(tmp_path):
    # a script run directly has its own folder first on sys.path: `import workshop` in
    # scripts/render.py loads scripts/workshop.py, even if the root has one too
    write(tmp_path, "scripts/render.py")
    write(tmp_path, "scripts/workshop.py")
    write(tmp_path, "scripts/pkg/__init__.py")
    write(tmp_path, "workshop.py")
    write(tmp_path, "tools/run.py")
    assert graph.resolve_py("", "workshop", "scripts/render.py", tmp_path) == ("file", "scripts/workshop.py")
    assert graph.resolve_py("", "pkg", "scripts/render.py", tmp_path) == ("file", "scripts/pkg/__init__.py")
    assert graph.resolve_py("", "workshop", "tools/run.py", tmp_path) == ("file", "workshop.py")
    assert graph.resolve_py("", "numpy", "scripts/render.py", tmp_path) == ("package", "numpy")


def test_resolve_py_inside_a_package_does_not_take_siblings(tmp_path):
    # inside a package an absolute import is absolute: app/views.py's `import auth`
    # does not mean app/auth.py
    write(tmp_path, "app/__init__.py")
    write(tmp_path, "app/views.py")
    write(tmp_path, "app/auth.py")
    assert graph.resolve_py("", "auth", "app/views.py", tmp_path) == ("package", "auth")


def test_indented_sibling_imports_become_links(tmp_path):
    write(tmp_path, "scripts/render.py", "import os\n\ndef go():\n    import workshop as _ws\n    from stage import run\n")
    write(tmp_path, "scripts/workshop.py")
    write(tmp_path, "scripts/stage.py")
    g = graph.build(tmp_path, [], {"findings": []})
    assert {(e["from"], e["to"]) for e in g["edges"]} == {
        ("scripts/render.py", "scripts/workshop.py"), ("scripts/render.py", "scripts/stage.py")}


def test_collect_files_excludes_tests_and_config(tmp_path):
    for rel in ("src/a.ts", "src/b.test.ts", "tests/c.py", "vite.config.ts", "src/__tests__/d.js",
                "src/styles.css", "node_modules/x/index.js", "app/main.py"):
        write(tmp_path, rel)
    files, excluded = graph.collect_files(tmp_path)
    assert sorted(files) == ["app/main.py", "src/a.ts"]
    assert excluded == {"tests": 3, "config": 1}


def test_comment_markers_inside_strings_are_not_comments():
    text = ('const MATCH = ["*://*/*"];\nimport { a } from "./a";\nconst url = "http://x"; // trailing note\n'
            "export function later() {}\n/** Docs. */\nimport b from './b';\n")
    assert [s for s, _, _ in graph.js_imports(text)] == ["./a", "./b"]
    clean = graph.strip_comments(text, "js")
    assert "later" in clean and "trailing note" not in clean and clean.count("\n") == text.count("\n")
    assert [e["name"] for e in graph.exports(text, "js")] == ["later"]


def test_monorepo_tsconfigs_extend_a_base_and_apply_to_their_own_package(tmp_path):
    import json as _json
    write(tmp_path, "tsconfig.base.json", _json.dumps(
        {"compilerOptions": {"baseUrl": ".", "paths": {"@shared/*": ["packages/shared/src/*"]}}}))
    write(tmp_path, "packages/web/tsconfig.json", '{ "extends": "../../tsconfig.base.json", }')
    write(tmp_path, "packages/api/tsconfig.json", _json.dumps(
        {"extends": "../../tsconfig.base.json", "compilerOptions": {"baseUrl": ".", "paths": {"@/*": ["./src/*"]}}}))
    write(tmp_path, "packages/shared/src/util.ts", "export const u = 1;\n")
    write(tmp_path, "packages/web/src/page.ts", 'import { u } from "@shared/util";\n')
    write(tmp_path, "packages/api/src/handler.ts", 'import { db } from "@/db";\n')
    write(tmp_path, "packages/api/src/db.ts", "export const db = 1;\n")
    g = graph.build(tmp_path, [], {"findings": []})
    edges = {(e["from"], e["to"]) for e in g["edges"]}
    assert ("packages/web/src/page.ts", "packages/shared/src/util.ts") in edges
    assert ("packages/api/src/handler.ts", "packages/api/src/db.ts") in edges
    assert g["unresolved"] == []
