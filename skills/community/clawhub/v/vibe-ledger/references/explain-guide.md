# Writing the explanations

`start` picks the files that matter most — entry points, files with check findings, files many others use; at most 30 — and lists them in `<run>/explain_pack.md`. You write `<run>/explain.json`: what each of those files does, its main functions, and, when the conversations show it, how it came to be. Every other file gets an automatic summary. The flowchart's side panel shows what you write, after `check` has verified it.

## 1. Read

For each file in the pack, read its lines in the pack (role, exports, what it uses, who uses it, check findings) and then **the whole file**. Never explain a file you have not opened.

## 2. Write one entry per file

- `purpose_plain` — one or two sentences for someone who cannot read code: what the file does for the person using the app, and where data goes (which store, which outside service). Say "your notes", "the AI service", "the database" — not function names. Write in the run's language (`lang` in `run.json`).
- `purpose_dev` — one sentence for a developer naming the mechanism, with identifiers in backticks (`createClient`, `lib/supabase.ts`). **Every backticked name must exist in the project.** If one does not, the purpose is shown as unverified.
- `functions` — the 2–5 functions a reader most needs, each `{"name", "line", "plain"}`:
  - `name` exactly as this file defines it: a function, an arrow function or function expression assigned to a name, a class, a class method or an object method. Not something the file only imports or calls.
  - `line` — the line where that definition starts. `check` accepts ±3 lines, corrects the line of a name defined only once in the file, and drops any other name with the reason.
  - `plain` — one sentence in plain words.
  - A file with no functions of its own (markup, a config object, one exported client) gets `"functions": []`.
- `history` (optional) — only when the reading packs show how the file came about: `{"plain": "…", "evidence": ["H1"]}`. Each id points to a transcript quote in the top-level `evidence` map, copied word for word from a reading pack under the same rules as the ledger (references/extraction-guide.md): `msg_id` is the `[ID]` in the pack's header line and the quote is at least 4 characters. Items whose quotes fail are dropped. With no conversations, leave `history` out.

Do not write risks here. They come from the probes and the verified ledger and are attached to each file automatically.

## 3. Journeys: what happens when the user does something

Files explained one by one do not show how they work together. Also write 2–4 `journeys` for the whole project — the things a user actually does (open the page, press the main button, save, pay, sign in) — each as the files it passes through, in order:

- `title` — what the user does, in the run's language: "你点「分析这个职位」时".
- `steps` — 2–8 steps, in the order things happen. Each step is `{"file", "plain"}`, optionally with `"function"` and `"line"` (the same rules as above). Start at an entry point listed under "Journeys" in `explain_pack.md`, follow the imports, and end where the user sees the result. The same file may appear twice when the flow comes back to it.
- `outcome` (optional) — what the user sees at the end: "你在侧边栏看到分析结果".

`check` drops a step whose file is not in the graph, rejects a journey left with fewer than 2 steps, and marks a step that no import connects to the one before it (an event or a message, say): the page draws that link dashed and says the code shows no direct link. Write only steps you read in the code.

With several explanation groups, journeys span the groups: write them once, in `explain.json`, after `vl.py merge`.

## 4. The function map: areas, data, flows

The flowchart opens on the project's parts, not its folders, so write these three once for the whole project (with several explanation groups: in `explain.json`, once the parts are merged). The end of `explain_pack.md` lists every file by folder and the lines where the code names a data file.

- `areas` — 2–10 parts of the project as its user would name them: "配音", "渲染", "交付检查", "行程页面", "日历". Each is `{"id", "name", "plain", "match"}`: `plain` is one sentence on what the part does for the user; `match` lists what it covers — a folder ending in `/` (`scripts/qa/`), a glob (`scripts/*_qa.py`) or an exact path. Order matters: **a file goes to the first area that matches it**, so list narrow areas before broad ones and end with a catch-all only if it is a real part. A file no area matches is drawn under "Other" — few is fine; many means the areas are wrong. Group by what a part does, not by where it sits: when everything is in one folder, use globs and paths.
- `items` — the data and outputs that move between the parts: inputs the user gives, working files, outputs, stores. `{"id", "name", "plain", "kind", "match"}`; `kind` is `input`, `file`, `output` or `store`; `match` lists the spellings the code uses for it (`["storyboard.json"]`, `["out.mp4", "out.nobgm.mp4"]`). Outside services (APIs) are added from the imports; do not write them.
- `flows` — who reads or writes each item: `{"area", "item", "op", "path", "line", "snippet"}`; `op` is `read` or `write`; `path`, `line` and `snippet` are one line of code that does it, copied exactly (the candidates in the pack are a good start). `check` keeps a flow only when the line is in the file (±3 lines), the file belongs to that area, and the line names the item (one of its `match` spellings). Write the one line that decides it, not a comment.

A part that writes an item and another that reads it are joined on the map by a link that says what passes ("storyboard.json"), dashed when no import joins them. The 数据流 / Data flow view draws the parts, the items between them and the outside services.

## 5. Paths, groups and empty packs

- Use paths exactly as the pack prints them (relative to the project, forward slashes). An entry whose path is not in the graph is rejected as a whole.
- When the pack lists more than 8 files it splits them into groups. Each group writes `<run>/parts/explain_NN.json` in this same format (give each group to its own subagent, or do them one by one); evidence ids only need to be unique within one part. `vl.py merge` combines the parts into `explain.json`; a file explained twice keeps the first explanation.
- When the pack lists no files, write `{"evidence": {}, "files": {}}` — `check` needs the file to exist.

## 6. Example

```json
{
  "evidence": {
    "H1": {"kind": "transcript", "session": "s1", "msg_id": "u-3", "quote": "帮我加一个总结按钮，用 OpenAI"}
  },
  "files": {
    "app/api/summarize/route.ts": {
      "purpose_plain": "你点“总结”时，这个文件把你的笔记发给 OpenAI，再把它写的总结送回页面。",
      "purpose_dev": "Next.js route handler: `POST` reads `notes` from the request body and asks OpenAI for a summary.",
      "functions": [{"name": "POST", "line": 5, "plain": "收到页面发来的笔记，请 OpenAI 写总结并返回"}],
      "history": [{"plain": "你要求加一个用 OpenAI 的总结按钮，AI 随后写了这个文件。", "evidence": ["H1"]}]
    },
    "lib/supabase.ts": {
      "purpose_plain": "连接存放笔记的数据库（Supabase），其他文件都通过它读写笔记。",
      "purpose_dev": "Creates the shared client with `createClient` from the public URL and anon key.",
      "functions": []
    }
  },
  "journeys": [
    {
      "title": "你点「总结」时",
      "steps": [
        {"file": "app/page.tsx", "plain": "页面把你的笔记交给总结接口"},
        {"file": "app/api/summarize/route.ts", "plain": "接口把笔记发给 OpenAI，等它写好总结", "function": "POST", "line": 5},
        {"file": "app/page.tsx", "plain": "页面把总结显示在笔记下面"}
      ],
      "outcome": "总结出现在笔记下面"
    }
  ],
  "areas": [
    {"id": "page", "name": "笔记页面", "plain": "你看到和操作的页面", "match": ["app/page.tsx"]},
    {"id": "api", "name": "总结接口", "plain": "把笔记交给 OpenAI，取回总结", "match": ["app/api/"]},
    {"id": "store", "name": "数据库连接", "plain": "读写你的笔记", "match": ["lib/"]}
  ],
  "items": [
    {"id": "notes", "name": "笔记", "plain": "你写的笔记", "kind": "store", "match": ["notes"]}
  ],
  "flows": [
    {"area": "api", "item": "notes", "op": "read", "path": "app/api/summarize/route.ts", "line": 6,
     "snippet": "const { notes } = await req.json();"}
  ]
}
```

## 7. What `check` does with it

- A format problem (missing `purpose_plain`, a line that is not a number, an unknown evidence id) is listed and `check` exits with code 2. Fix it and run `check` again.
- Areas: every file goes to the first area that matches it; an area that ends up with no file is dropped, and a pattern that matches nothing is listed. A flow whose line is missing, sits in another area's file, or does not name its item is dropped with the reason; an item left without flows is dropped.
- Function names are looked up in the file: kept, line-corrected or dropped. Backticked names are looked up in the project. History quotes are looked up in the conversations.
- The result goes to `explain.verified.json`, which `render` uses. Fix a mis-copied line or quote only by copying from the real file or message; a dropped name is the honest result, not something to work around.
