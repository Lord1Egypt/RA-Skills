"""A hand-built verified ledger (the shape verify.verify_ledger returns)."""
import copy

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"

_SAMPLE = {
    "evidence": {
        "E1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "只有我自己能看到我的笔记",
               "ok": True, "ts": "2026-09-12T09:01:00Z", "role": "user", "msg_kind": "text"},
        "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 3,
               "snippet": "alter table notes disable row level security;", "ok": True, "line_corrected": False},
        "E3": {"kind": "probe", "finding_id": "secrets_exposed:.env.local:2", "ok": True, "probe": "secrets_exposed",
               "level": "certain", "path": ".env.local", "line": 2,
               "snippet": "NEXT_PUBLIC_OPENAI_API_KEY=" + OPENAI, "message": "bundled into the browser"},
        "E4": {"kind": "transcript", "session": "s1", "msg_id": "m4", "quote": "暂时先把 key 放前端",
               "ok": True, "ts": "2026-09-13T10:00:00Z", "role": "assistant", "msg_kind": "text"},
        "E5": {"kind": "transcript", "session": "s1", "msg_id": "m5", "quote": "violates row-level security",
               "ok": True, "ts": "2026-09-12T09:20:00Z", "role": "tool", "msg_kind": "error"},
        "E6": {"kind": "transcript", "session": "s1", "msg_id": "m6", "quote": "disable row level security",
               "ok": True, "ts": "2026-09-12T09:21:00Z", "role": "assistant", "msg_kind": "edit"},
        "E7": {"kind": "code", "path": "app/api/summarize/route.ts", "line": 3,
               "snippet": "export async function POST(req: Request) {", "ok": True, "line_corrected": True},
        "BAD": {"kind": "code", "path": "app/pay.ts", "line": 1, "snippet": "stripe()", "ok": False,
                "reason": "file not found"},
    },
    "promises": [
        {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "只有我自己能看到我的笔记",
         "source": ["E1"], "status": "broken", "verdict_plain": "前门锁了，后窗一直开着",
         "verdict_dev": "notes 表关闭了 RLS（supabase/migrations/001.sql:3）", "evidence": ["E2"],
         "fix_prompt": "Re-enable row level security on notes and add a policy using (auth.uid() = user_id)."},
        {"id": "P2", "type": "deferred", "question": "open_debts", "plain": "把 OpenAI key 移到服务端",
         "source": ["E4"], "status": "pending", "verdict_plain": "key 还在前端，任何人都能拿走",
         "verdict_dev": "NEXT_PUBLIC_OPENAI_API_KEY in .env.local", "evidence": ["E3"],
         "fix_prompt": "Rename NEXT_PUBLIC_OPENAI_API_KEY to OPENAI_API_KEY and read it only in route.ts."},
        {"id": "P3", "type": "ai_claim", "question": "what_costs", "plain": "接口已经加了登录保护",
         "source": ["E1"], "status": "unknown", "verdict_plain": "没找到能证明这一点的代码",
         "verdict_dev": "no auth check found", "evidence": ["BAD"], "downgraded_from": "kept",
         "downgrade_reason": "no code or probe evidence passed verification", "fix_prompt": "Add a login check."},
        {"id": "P4", "type": "user_requirement", "question": "where_data", "plain": "笔记要存到 Supabase",
         "source": ["E1"], "status": "kept", "verdict_plain": "笔记确实存在 Supabase 的 notes 表里",
         "verdict_dev": "supabase.from('notes')", "evidence": ["E2"]},
    ],
    "compromises": [{"id": "C1", "error": "E5", "change": ["E6"], "bypassed": "RLS", "still_present": True,
                     "now": ["E2"], "breaks": "P1"}],
    "rejected": [{"id": "P9", "plain": "made up", "reason": "none of its quotes could be found in the conversations"}],
    "map": {"nodes": [{"id": "web", "lane": "browser", "kind": "page", "label": "首页", "holds": [], "paid": False,
                       "evidence": ["E2"]},
                      {"id": "api", "lane": "server", "kind": "route", "label": "/api/summarize", "holds": [],
                       "paid": False, "evidence": ["E7"]},
                      {"id": "db", "lane": "storage", "kind": "database", "label": "Supabase", "holds": ["notes"],
                       "paid": False, "evidence": ["E2"]},
                      {"id": "ai", "lane": "storage", "kind": "third_party", "label": "OpenAI", "holds": [],
                       "paid": True, "evidence": ["E7"]}],
            "edges": [{"from": "web", "to": "db", "carries": "笔记", "risk": "陌生人也能读", "evidence": ["E2"]},
                      {"from": "web", "to": "api", "carries": "笔记内容", "risk": None, "evidence": ["E7"]},
                      {"from": "api", "to": "ai", "carries": "笔记内容", "risk": None, "evidence": ["E7"]}],
            "unverified_nodes": [{"id": "stripe", "lane": "storage", "kind": "third_party", "label": "Stripe",
                                  "holds": [], "paid": True, "evidence": ["BAD"]}],
            "unverified_edges": []},
    "access": {"resources": [
        {"name": "notes", "required_by": "P1", "cells": {
            "anonymous": {"read": "allow", "write": "allow", "evidence": ["E2"]},
            "signed_in": {"read": "allow", "write": "allow", "evidence": ["E2"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["E2"]}}},
        {"name": "profiles", "required_by": None, "cells": {
            "anonymous": {"read": "deny", "write": "deny", "evidence": ["E2"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["E2"]}}}]},
    "paths": [{"action": "点“AI 总结”", "steps": [
        {"label": "summarize()", "evidence": "E7", "warning": None, "unverified": False},
        {"label": "POST /api/summarize", "evidence": "E7", "warning": "没有登录检查", "unverified": False},
        {"label": "stripe.charge()", "evidence": "BAD", "warning": None, "unverified": True}]}],
    "verification": {"evidence_total": 8, "evidence_ok": 7, "failed": [{"id": "BAD", "reason": "file not found"}],
                     "downgraded": 1, "rejected": 1, "nodes_unverified": 1, "edges_unverified": 0,
                     "cells_unknown": 0, "conflicts": 0},
}

RUN = {"project_name": "notes", "lang": "zh", "unattributed": ["lib/legacy.ts"],
       "sessions": {"threads": 2, "records": 40, "earliest": "2026-09-12T09:00:00Z", "latest": "2026-09-13T11:00:00Z",
                    "by_agent": {"claude-code": 2}, "archived_threads": 1, "ignored_types": {"claude:mode": 3},
                    "bad_lines": 0, "warnings": ["x.jsonl: the log format may have changed"]}}
PROBES = {"ran": ["secrets_exposed", "supabase_rls"],
          "skipped": [{"probe": "firebase_rules", "reason": "not used by this project: firebase", "needs": ["firebase"]},
                      {"probe": "routes", "reason": "crashed: ValueError('x')"}],
          "stack": {"stacks": ["nextjs", "supabase", "flask"], "unsupported": ["flask"], "covered": True},
          "findings": []}


def sample():
    return copy.deepcopy(_SAMPLE)
