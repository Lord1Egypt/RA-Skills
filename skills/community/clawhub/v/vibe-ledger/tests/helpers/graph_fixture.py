"""A three-file project with one paid service: app/page.tsx -> lib/ai.ts -> OpenAI, plus a lone lib/util.ts."""
import graph

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_project(root, purpose="把文字发给 OpenAI 总结。"):
    write(root, "app/page.tsx", 'import { summarize } from "../lib/ai";\nexport default function Page() {}\n')
    write(root, "lib/ai.ts", 'import OpenAI from "openai";\nexport async function summarize(t) {\n  return t;\n}\n')
    write(root, "lib/util.ts", "export const x = 1;\n")
    write(root, "package.json", '{"dependencies": {"next": "15.0.0", "openai": "4.60.0"}}\n')
    g = graph.build(root, [], {"findings": []})
    ledger = {"evidence": {
                  "E1": {"kind": "code", "path": "lib/ai.ts", "line": 2, "snippet": "export async function summarize(t) {", "ok": True},
                  "Q1": {"kind": "transcript", "ok": True, "ts": "2026-09-12T09:00:00Z", "role": "user",
                         "quote": "不要让陌生人花我的钱", "msg_id": "m", "session": "s"}},
              "promises": [{"id": "P1", "type": "user_requirement", "question": "what_costs", "plain": "不要让陌生人花我的钱",
                            "source": ["Q1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["E1"]}],
              "compromises": [], "map": {"nodes": [], "edges": []}, "access": {"resources": []}, "paths": []}
    probes = {"findings": [{"id": "secrets_exposed:lib/util.ts:1", "probe": "secrets_exposed", "level": "hint",
                            "path": "lib/util.ts", "line": 1, "snippet": "export const x = 1;", "message": "A thing", "implies": []}]}
    explained = {"evidence": {}, "rejected": [], "files": {"lib/ai.ts": {
        "purpose_plain": purpose, "purpose_dev": "dev", "ok": True, "dropped_functions": [], "purpose_unverified": False,
        "missing_identifiers": [], "history": [], "functions": [{"name": "summarize", "line": 2, "plain": "发请求", "line_corrected": False}]}}}
    return root, g, explained, ledger, probes
