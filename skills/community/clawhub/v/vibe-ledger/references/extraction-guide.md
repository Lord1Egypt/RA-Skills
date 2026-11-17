# Writing the ledger

You turn a reading pack, `probes.json`, `candidates.json` and the project code into `<run>/ledger.json`. The scripts check everything you write; the report shows what passed.

## 1. Read in this order

1. `probes.json` — deterministic findings. Each has an `id`, `level` (`certain`, `hint`, `fact`), `path`, `line`, `message`. `fact` findings from `routes` list the pages and endpoints.
2. The reading pack — every user message, plus candidates: **K** (an error followed by a change), **D** (something put off), **A** (the AI saying it did something). Candidates are hints; judge each one.
3. The code the pack and probes point at. Open the files; do not guess what they contain.

## 2. Promises

Write one promise for each thing that matters to one of the five questions (references/five-questions.md):

- `user_requirement` — the user asked for it ("只有我自己能看到我的笔记").
- `ai_claim` — the AI said it was done ("接口已经加了登录保护"). Claims are worth checking because they are often only partly true.
- `deferred` — someone said it would be done later ("for now the key is in the frontend").

Pick the status from the code, not from the conversation:

| The code shows… | status |
|---|---|
| the promise holds | `kept` |
| the opposite | `broken` |
| some of it (one route protected, another not) | `partial` |
| a `deferred` item that was never done | `pending` |
| you cannot tell from the code | `unknown` |

Every status except `unknown` needs at least one `code` or `probe` evidence that shows it. A transcript quote proves something was *said*, never that it is *true*.

## 3. Evidence

- Transcript: `msg_id` is the `[ID]` in the pack header line; `quote` is copied exactly from the text under it (one sentence is enough; at least 4 characters). Never quote across a "not shown" marker.
- Code: `path` relative to the project, the `line` where the snippet starts, and a `snippet` of 1–3 lines copied from the file. Prefer the line that *decides* the behaviour (the `disable row level security`, the missing check, the `NEXT_PUBLIC_` variable).
- Probe: `finding_id` from `probes.json`. Use it when a probe already found the thing — it is the strongest evidence.
- An edit record in the pack shows `--- before` / `+++ after` (or `WRITE path` plus the new text). Quote a change from the after-part.
- Secrets: snippets in `probes.json` and the reading packs are masked (`sk-proj-…wXyZ`). A masked copy of a line verifies exactly like the original, so never copy a raw secret into the ledger, even if you saw it in a file.

## 4. Compromises (from K candidates)

A compromise is a change made to get past an error that **weakened a protection**: switching off row level security, setting CORS to `*`, silencing type checks, skipping verification, using the service key in the browser, swallowing an error, replacing real data with mock data. A correct fix (adding the missing policy, fixing the query) is not a compromise — skip it.

For each real compromise: `error` = the error's transcript evidence; `change` = the change's transcript evidence (quote from the edit record); `bypassed` = a few words; `still_present` = whether the weakening is in the code **now** (check the file; `now` lists the code/probe evidence); `breaks` = the promise it breaks, if any.

## 5. Map (diagram A)

Nodes go in three lanes: `browser` (pages, client code), `server` (routes, server functions), `storage` (databases, file storage and outside services). Kinds: `page`, `route`, `function`, `database`, `storage`, `third_party`, `client`. Set `paid: true` for services that charge per use (AI APIs, SMS, email, payments). Edges say what data moves (`carries`) and, when it is risky, why (`risk`, a few words). Every node and edge needs code or probe evidence — the route probe's `fact` findings are good evidence for route nodes. Keep it to the parts that matter: at most 12 nodes are drawn. When the project is not a web app (a command-line tool, a pipeline, a desktop app), set `lane_labels` so the lanes say what they are — e.g. `{"browser": "你运行的脚本", "server": "本机处理"}`; a lane called "browser" on a CLI misleads.

## 6. Access (diagram B)

One resource per table, collection or bucket that holds user data. When a promise is about who may *use* something rather than read data — "strangers must not run up my AI bill", "only I can reset" — the resource may be that action (name it plainly, e.g. "AI summary (/api/summarize)"): `read` = may call it, `write` = may change what it changes. For each of `anonymous`, `signed_in`, `owner`, write what the code allows for `read` and `write` (`allow`, `deny`, `unknown`) with evidence. Leave a subject's cell out when the code says nothing specific about that subject, and write `unknown` rather than guessing — for example, do not mark the owner `allow` when the code does not tell owners and other users apart. Link `required_by` to the promise that asked for privacy. Probe findings are merged in automatically: when a probe says "anyone can read", it fills unknown cells and flags cells that disagree — do not copy probe conclusions you cannot see in the code.

## 7. Paths (diagram E, developer view)

One to four key actions (save data, call the AI, pay, sign in). Each path is `{"action": "Summarize my notes", "steps": [...]}` — `action` names what the user does. Each step is a function or request with **one** code evidence id — a string, not a list: `{"label": "POST /api/summarize", "evidence": "E7", "warning": "no login check"}`; put a short `warning` on the step where the problem is (e.g. "no login check") and leave it out (or `null`) elsewhere.

## 8. Writing style

- `plain`: the promise as the user would say it, short.
- `verdict_plain`: one sentence a non-programmer understands. An analogy only if it is accurate ("the front door is locked but the back window is open" fits RLS off with a login page; it does not fit a slow page).
- `verdict_dev`: file, line and mechanism.
- `fix_prompt` (for `broken`, `partial`, `pending`): what to change, where, and how to confirm it — written so the user can paste it to their AI. No secrets.
- Write in the run's language (`lang` in `run.json`).

## 9. Several reading packs

Each subagent writes `<run>/parts/part_NN.json` holding `evidence`, `promises` and `compromises` for its pack (ids only need to be unique inside the part). `vl.py merge` renames ids, drops duplicates and flags promises two parts judged differently. You then add `map`, `access` and `paths` to the merged `ledger.json`, referring to the merged promise ids (`p1_P3` …).

## 10. A worked example

The pack shows `[s1-u1] USER … 只有我自己能看到我的笔记`, candidate K1 with `[s1-u3] TOOL-OUTPUT … new row violates row-level security policy` and `[s1-u4] AI … EDIT supabase/migrations/001.sql … disable row level security`; `probes.json` has `supabase_rls:supabase/migrations/001.sql:3`.

```json
{
  "evidence": {
    "E1": {"kind": "transcript", "session": "s1", "msg_id": "s1-u1", "quote": "只有我自己能看到我的笔记"},
    "E2": {"kind": "probe", "finding_id": "supabase_rls:supabase/migrations/001.sql:3"},
    "E3": {"kind": "transcript", "session": "s1", "msg_id": "s1-u3", "quote": "new row violates row-level security policy"},
    "E4": {"kind": "transcript", "session": "s1", "msg_id": "s1-u4", "quote": "disable row level security"},
    "E5": {"kind": "code", "path": "lib/supabase.ts", "line": 3, "snippet": "export const supabase = createClient("}
  },
  "promises": [{
    "id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "只有我自己能看到我的笔记",
    "source": ["E1"], "status": "broken",
    "verdict_plain": "笔记表的访问规则被关掉了：任何人拿到网页里公开的密钥，就能读到所有人的笔记。",
    "verdict_dev": "supabase/migrations/001.sql:3 disables RLS on notes; no policy limits rows to auth.uid().",
    "evidence": ["E2"],
    "fix_prompt": "In supabase/migrations, re-enable row level security on notes and add select/insert policies using (auth.uid() = user_id). Then sign in as a second user and confirm you cannot see the first user's notes."
  }],
  "compromises": [{"id": "C1", "error": "E3", "change": ["E4"], "bypassed": "RLS",
                   "still_present": true, "now": ["E2"], "breaks": "P1"}],
  "map": {"nodes": [
            {"id": "web", "lane": "browser", "kind": "page", "label": "笔记页", "holds": [], "paid": false, "evidence": ["E5"]},
            {"id": "db", "lane": "storage", "kind": "database", "label": "Supabase", "holds": ["notes"], "paid": false, "evidence": ["E2"]}],
          "edges": [{"from": "web", "to": "db", "carries": "笔记", "risk": "陌生人也能读", "evidence": ["E2"]}]},
  "access": {"resources": [{"name": "notes", "required_by": "P1", "cells": {
            "owner": {"read": "allow", "write": "allow", "evidence": ["E5"]}}}]},
  "paths": []
}
```

The anonymous and signed-in cells are left out on purpose: the probe fills them.
