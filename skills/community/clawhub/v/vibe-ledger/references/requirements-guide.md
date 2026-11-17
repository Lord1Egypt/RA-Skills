# Writing requirements.json (the 需求对照 / Your asks tab)

The tab answers the user's question "did the AI build what I asked for?". You turn `requests_NN.md` (every message the user typed, oldest first) and the project code into `<run>/requirements.json`. `vl.py check` verifies every quote and snippet, re-runs your searches, and lists every user message you did not account for.

This is not the ledger. The ledger keeps only the five safety questions; here **every** request about the project counts — features, behaviour, looks, wording, docs, file layout, defaults.

## 1. Read

1. The request pack(s), top to bottom. "AI before this" is the end of the AI message the user answered: a short reply ("yes, do 2 and 3", "选 paper-dossier") gets its meaning from it.
2. For each request, the code that should carry it. Open the files; do not guess. When a short reply needs more than the 400 characters shown, find its ID in the reading packs (`reading_pack_NN.md`) for the full AI message.

## 2. What is a requirement

A requirement is something the user asked **the project** to do or be: "字幕要跟着语音走", "README 只留名字", "默认走 codex 订阅", "make the button blue". One per distinct ask: a message with three asks is three requirements with the same `source`; the same ask repeated later is one requirement with both messages in `source`.

An approved proposal counts: when the AI listed options and the user answered "先把 2，3，4 修复下", write one requirement per approved item, with `plain` saying what item 2 was, and the user's reply as `source` (add the AI's message too if you want the list on record — at least one source must be the user's).

Not requirements — list their IDs under `skipped` instead:

| reason | examples |
|---|---|
| `ack` | "继续", "好的", "可以" with nothing approved that changes the project, "ok" |
| `process` | "push", "检查一下", "进行的如何了", "尽量省 token", "先别评审" — how to work this session, not what the project does |
| `question` | "你觉得还有什么可以优化的", "why did it fail?" |
| `not_project` | a request about another project, the user's own files, or a one-off output that is not kept in this project ("make me two videos about X") |

Every `[ID]` in the packs must end up either in some requirement's `source` (or `agreed_in` / `superseded_by`) or under `skipped`. The report lists the rest as "unaccounted", which reads as "a requirement may be missing here".

## 3. Status — from the code, not from the conversation

| The code shows… | status | needs |
|---|---|---|
| it is there and works as asked | `done` | code or probe `evidence` |
| some of it (one of two cases, only the default path) | `partial` | code or probe `evidence`; a `fix_prompt` |
| it is not there | `missing` | code `evidence` of where it should be, **or** `searched`: words that would be in the project if it were built (≥ 4 characters each; `check` searches every tracked text file, case-insensitively, and drops the verdict to ❓ if any is found); a `fix_prompt` |
| it was built another way than asked | `changed` | code `evidence`; `changed_to` (what was built instead); `agreed_in` with the user's message accepting it, when there is one |
| the user later asked for something else instead | `superseded` | `superseded_by`: the transcript evidence of the user's **later** message |
| you cannot tell | `unknown` | — |

A transcript quote proves something was *said*, never that it is in the code. The AI saying "已实现" is not evidence. When unsure, write `unknown`.

`changed` vs `superseded`: if the user changed their mind, it is `superseded` (not a problem). If the AI decided on its own, it is `changed` — say so in `verdict_plain`, and the report shows whether the user agreed.

## 4. Fields

`requirements.json` is `{"evidence": {...}, "requirements": [...], "skipped": {...}}`.

- `evidence` — exactly as in the ledger (references/ledger-schema.md): `transcript` (`session`, `msg_id`, `quote`), `code` (`path`, `line`, `snippet`), `probe` (`finding_id`).
- each requirement: `id` (`R1` …), `area` (a short feature name to group under, e.g. "配音", "字幕", "README", "登录"; use the user's words; 4–10 areas for a whole project), `plain` (the ask in one short sentence, in the run's language), `source` (transcript ids), `status`, `verdict_plain` (one sentence a non-programmer understands), `verdict_dev` (file, line, mechanism), `evidence` (code/probe ids), and as the table says `searched`, `changed_to`, `agreed_in`, `superseded_by`, `fix_prompt` (what to change, where, how to confirm — pasteable to an AI; never a secret).
- `skipped` — `{"ack": [msg ids], "process": [...], "question": [...], "not_project": [...]}`. Message ids, not evidence ids.

Write in the run's language (`lang` in `run.json`).

## 5. Several request packs

Each subagent takes one `requests_NN.md` and writes `<run>/parts/req_NN.json` in the same format (ids only need to be unique inside the part). `vl.py merge` combines them into `requirements.json`. A `superseded_by` must point at a message in the same pack; when the later message is in another pack, add it to that part's evidence anyway (quote it from the reading pack) or write `unknown`.

## 6. A worked example

The pack shows `[u1] USER … 字幕要按语音时长计时，另外 README 清空只留名字` and later `[u9] USER … 仿照 slides_maker 写一个完整的 README`; the code has `scripts/captions.py` with `def cue_times(durations):` and no `say` fallback anywhere.

```json
{
  "evidence": {
    "E1": {"kind": "transcript", "session": "s1", "msg_id": "u1", "quote": "字幕要按语音时长计时"},
    "E2": {"kind": "code", "path": "scripts/captions.py", "line": 12, "snippet": "def cue_times(durations):"},
    "E3": {"kind": "transcript", "session": "s1", "msg_id": "u1", "quote": "README 清空只留名字"},
    "E4": {"kind": "transcript", "session": "s1", "msg_id": "u9", "quote": "仿照 slides_maker 写一个完整的 README"},
    "E5": {"kind": "transcript", "session": "s1", "msg_id": "u4", "quote": "网络断了就用 Mac 的 say 配音"}
  },
  "requirements": [
    {"id": "R1", "area": "字幕", "plain": "字幕按每段语音的实际时长计时", "source": ["E1"], "status": "done",
     "verdict_plain": "字幕的出现时间是按配音文件的时长算出来的。",
     "verdict_dev": "scripts/captions.py:12 cue_times() builds cue starts from the measured audio durations.",
     "evidence": ["E2"]},
    {"id": "R2", "area": "README", "plain": "README 清空，只留项目名", "source": ["E3"], "status": "superseded",
     "superseded_by": "E4", "verdict_plain": "你后来要了一份完整的 README，这条不再适用。",
     "verdict_dev": "Replaced by the later request in u9.", "evidence": []},
    {"id": "R3", "area": "配音", "plain": "网络断了时改用 Mac 自带的 say 配音", "source": ["E5"], "status": "missing",
     "searched": ["say -v", "subprocess.run([\"say\""],
     "verdict_plain": "项目里没有调用 Mac 的 say，网络断了配音会直接失败。",
     "verdict_dev": "No call to the macOS `say` command anywhere in the tracked files.",
     "evidence": [],
     "fix_prompt": "In the TTS step, when the online voice fails after retries, fall back to the macOS `say` command and print a warning. Confirm by turning the network off and generating one page."}
  ],
  "skipped": {"ack": ["u2", "u3"], "process": ["u5"], "question": ["u6"], "not_project": []}
}
```
