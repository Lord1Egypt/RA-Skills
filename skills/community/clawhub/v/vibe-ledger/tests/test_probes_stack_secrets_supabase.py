import base64
import json
import subprocess

import probes
from probes import secrets_exposed, supabase_rls
from probes.util import is_client_file, local_imports

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def jwt(role):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256"}) + "." + enc({"role": role, "iss": "supabase"}) + "." + "s1gnatureS1gnature"


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_detect_stack_from_package_json_and_files(tmp_path):
    write(tmp_path, "package.json", json.dumps({"dependencies": {"next": "15", "@supabase/supabase-js": "2"},
                                                "devDependencies": {"vite": "5"}}))
    write(tmp_path, "firestore.rules", "rules_version = '2';")
    write(tmp_path, "api/requirements.txt", "flask==3.0\n")
    st = probes.detect_stack(tmp_path)
    assert st["stacks"] == ["firebase", "flask", "nextjs", "supabase", "vite"]
    assert st["unsupported"] == ["flask"] and st["covered"] is True


def test_detect_stack_unknown_project(tmp_path):
    write(tmp_path, "main.go", "package main")
    write(tmp_path, "go.mod", "module x")
    st = probes.detect_stack(tmp_path)
    assert st == {"stacks": ["go"], "unsupported": ["go"], "covered": False}


def test_client_prefixed_secret_in_env_is_certain(tmp_path):
    write(tmp_path, ".env.local", f"NEXT_PUBLIC_SUPABASE_ANON_KEY={jwt('anon')}\nNEXT_PUBLIC_OPENAI_API_KEY={OPENAI}\n"
                                  "OPENAI_API_KEY_SERVER=fine-on-server\nVITE_ADMIN_SECRET=x\n")
    write(tmp_path, ".env.example", f"NEXT_PUBLIC_OPENAI_API_KEY={OPENAI}\n")
    found = secrets_exposed.run(tmp_path, {"stacks": ["nextjs"]})
    got = sorted((f.path, f.line, f.level) for f in found)
    assert got == [(".env.local", 2, "certain"), (".env.local", 4, "certain")]


def test_hardcoded_secret_in_code_but_not_anon_jwt(tmp_path):
    write(tmp_path, "src/ai.ts", f'const key = "{OPENAI}";\nconst anon = "{jwt("anon")}";\n'
                                 f'const admin = "{jwt("service_role")}";\n')
    found = secrets_exposed.run(tmp_path, {"stacks": []})
    assert sorted(f.line for f in found) == [1, 3]


def test_tracked_env_file_is_reported(tmp_path):
    write(tmp_path, ".env", "A=1\n")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", ".env"], check=True)
    found = secrets_exposed.run(tmp_path, {"stacks": []})
    assert [(f.path, f.line, f.snippet) for f in found] == [(".env", 1, "A=1")]


def test_secrets_probe_without_git(tmp_path):
    write(tmp_path, "src/a.ts", "export const a = 1;\n")
    assert secrets_exposed.run(tmp_path, {"stacks": []}) == []


MIGRATION = """create table notes (
  id uuid primary key,
  user_id uuid not null
);

alter table notes disable row level security;

create table profiles (id uuid primary key);
alter table profiles enable row level security;
create policy "everyone reads" on profiles for select using (true);

create table todos (id bigint primary key);
"""


def test_supabase_rls_findings_and_implications(tmp_path):
    write(tmp_path, "supabase/migrations/001_init.sql", MIGRATION)
    write(tmp_path, "lib/db.ts", 'const r = await supabase.from("notes").select();\n'
                                 'const s = await supabase.from("payments").select();\n'
                                 'const b = Buffer.from("hello");\n')
    found = {(f.message.split(" ")[0], f.path, f.line): f for f in supabase_rls.run(tmp_path, {"stacks": ["supabase"]})}
    by_line = {(f.path, f.line): f for f in found.values()}
    off = by_line[("supabase/migrations/001_init.sql", 6)]
    assert off.level == "certain" and "notes" in off.message
    assert {"resource": "notes", "subject": "anonymous", "perm": "read", "value": "allow"} in off.implies
    pol = by_line[("supabase/migrations/001_init.sql", 10)]
    assert {(i["subject"], i["perm"]) for i in pol.implies} == {("anonymous", "read"), ("signed_in", "read")}
    never = by_line[("supabase/migrations/001_init.sql", 12)]
    assert "todos" in never.message and never.implies == []
    unknown = by_line[("lib/db.ts", 2)]
    assert unknown.level == "hint" and "payments" in unknown.message
    assert ("lib/db.ts", 3) not in by_line
    assert ("supabase/migrations/001_init.sql", 9) not in by_line  # profiles has RLS on


def test_service_role_in_client_code(tmp_path):
    write(tmp_path, "components/Admin.tsx", '"use client";\nconst k = process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY;\n')
    write(tmp_path, "app/api/admin/route.ts", "const k = process.env.SUPABASE_SERVICE_ROLE_KEY;\n")
    found = supabase_rls.run(tmp_path, {"stacks": ["supabase", "nextjs"]})
    assert [(f.path, f.line, f.level) for f in found] == [("components/Admin.tsx", 2, "certain")]


def test_is_client_file():
    assert is_client_file("app/page.tsx", '"use client";', ["nextjs"]) is True
    assert is_client_file("app/api/x/route.ts", "", ["nextjs"]) is False
    assert is_client_file("src/App.tsx", "", ["vite"]) is True
    assert is_client_file("lib/util.ts", "", ["nextjs"]) is None


def test_local_imports_resolve_relative_and_alias(tmp_path):
    write(tmp_path, "lib/ai.ts", "export {}")
    route = write(tmp_path, "app/api/chat/route.ts", 'import { ask } from "@/lib/ai";\nimport x from "../../util";\n')
    write(tmp_path, "app/util/index.ts", "export {}")
    got = sorted(p.relative_to(tmp_path.resolve()).as_posix() for p in local_imports(tmp_path, route, route.read_text()))
    assert got == ["app/util/index.ts", "lib/ai.ts"]


def test_run_all_ids_and_skips(tmp_path):
    write(tmp_path, "package.json", json.dumps({"dependencies": {"react": "18"}}))
    write(tmp_path, ".env", f"VITE_KEY={OPENAI}\nVITE_OTHER={OPENAI}\n")
    out = probes.run_all(tmp_path)
    assert "secrets_exposed" in out["ran"]
    assert any(s["probe"] == "supabase_rls" for s in out["skipped"])
    ids = [f["id"] for f in out["findings"]]
    assert len(ids) == len(set(ids))
    assert "secrets_exposed:.env:1" in ids


def test_a_crashing_probe_is_reported_not_hidden(tmp_path, monkeypatch):
    def boom(root, stack):
        raise RuntimeError("bad regex")
    monkeypatch.setattr(secrets_exposed, "run", boom)
    out = probes.run_all(tmp_path)
    assert {"probe": "secrets_exposed", "reason": "crashed: RuntimeError('bad regex')"} in out["skipped"]


def test_run_all_masks_secrets_in_finding_snippets(tmp_path):
    write(tmp_path, ".env", f"VITE_KEY={OPENAI}\n")
    out = probes.run_all(tmp_path)
    snippets = " ".join(f["snippet"] for f in out["findings"])
    assert OPENAI not in snippets and "sk-proj-…" in snippets


def test_skipped_probes_say_which_stack_they_need(tmp_path):
    out = probes.run_all(tmp_path)
    skip = next(s for s in out["skipped"] if s["probe"] == "supabase_rls")
    assert skip["needs"] == ["supabase"]


def test_task_class_names_are_not_reported_as_secrets(tmp_path):
    write(tmp_path, "src/App.tsx", '<div className="taREDACTED-SECRET" />\n')
    assert secrets_exposed.run(tmp_path, {"stacks": []}) == []


def test_secrets_in_test_files_are_hints_not_certain(tmp_path):
    write(tmp_path, "tests/api.test.mjs", f'assert.equal(auth, "Bearer {OPENAI}");\n')
    write(tmp_path, "src/api.js", f'const key = "{OPENAI}";\n')
    found = {f.path: f for f in secrets_exposed.run(tmp_path, {"stacks": []})}
    assert found["tests/api.test.mjs"].level == "hint" and "test file" in found["tests/api.test.mjs"].message
    assert found["src/api.js"].level == "certain"


def test_chrome_extension_is_named_as_not_covered(tmp_path):
    write(tmp_path, "manifest.json", json.dumps({"manifest_version": 3, "name": "x", "permissions": ["storage"]}))
    st = probes.detect_stack(tmp_path)
    assert st["stacks"] == ["chrome-extension"] and st["unsupported"] == ["chrome-extension"]


def test_a_bundled_browser_component_manifest_is_not_an_extension(tmp_path):
    # Remotion/Puppeteer download headless Chrome into the project; its component
    # manifests carry manifest_version but declare nothing an extension does
    write(tmp_path, ".remotion/chrome/PrivacySandbox/manifest.json", json.dumps(
        {"manifest_version": 2, "name": "Privacy Sandbox Attestations", "version": "1", "pre_installed": True}))
    write(tmp_path, "broken/manifest.json", '{"manifest_version": 3, ')
    assert probes.detect_stack(tmp_path)["stacks"] == []
    write(tmp_path, "ext/manifest.json", json.dumps({"manifest_version": 3, "action": {"default_popup": "p.html"}}))
    assert probes.detect_stack(tmp_path)["stacks"] == ["chrome-extension"]
