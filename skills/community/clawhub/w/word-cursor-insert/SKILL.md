---
name: word-cursor-insert
description: 写报告时，把选中的一段话或 Excel/CSV 文件等内容，直接插进当前打开的 Word 光标处。文本和表格都能插，我会根据光标处语境判断该填成数字、文字还是表格，一次就插到位，重复执行也不会多插，几乎瞬间完成。告别手动复制粘贴。
---

# Word Cursor Insert

> ⚡ 手写报告利器：把一段话、一个 Excel/CSV 表格，精准塞进 Word 光标所在位置。连接你正在编辑的 Word，读懂光标处语境，单调用完成插入，重复执行也不会多插——快、准、稳。

## 最快用法（默认就这么跑，一条 Bash 调用）
用 managed venv 的 python 直接跑脚本，文本走 `--text`，表格走文件路径：
- 文本：`~/.workbuddy/binaries/python/envs/default/Scripts/python.exe scripts/word_cursor_insert.py --text "要插的内容" [--newline]`
- 长文本怕命令行乱码：写到 utf-8 文件后 `--file 路径.txt`
- 表格：`... word_cursor_insert.py 表.xlsx [--no-title]`（或 `.csv`）
- 强制插入（绕过就近判重）：加 `--no-idempotent`

**一条命令插完，信任返回即停。不要先读脚本、不要插完另跑校验、不要为长中文额外写临时 py——那都是多出来的往返。**

## Overview
Insert data into the cursor of the Word document the user currently has open.
Two modes: (1) a CSV/list becomes a formatted Word table (title + bold header +
borders + autofit); (2) a short value becomes inline plain text (e.g. filling a
blank inside a sentence). The workflow is context-aware (it inspects the cursor
surroundings before inserting) and fast (Python + pywin32, bounded-window
context read, single tool call).

## When to use
- "把这份清单 / 表 / CSV 写到 Word 光标处"
- "人数统计一下 插到 Word 光标" / "把统计结果填到 Word 里"
- Any request to place a spreadsheet / list / computed value at the Word
  insertion point.

## Critical environment rules (see references/gotchas.md)
- NEVER use PowerShell for Word COM here: its stdout is garbled and results are
  lost. Always use Python + pywin32. Python stdout is clean.
- Read cursor context with a BOUNDED window (~300 chars), never
  `doc.Range(0, sel.Start)`. Cost must stay O(window), independent of doc size.
- Do NOT re-run a COM call because the terminal looked garbled — that duplicates
  the insertion. Judge success from stdout/result only.
- 默认直接 `--text "中文内容"` 走命令行（managed python 在 Windows 下吃中文 argv 没问题）。**临时文件只是中文万一乱码的兜底**（用 `--file 路径.txt`），非必做步骤——别为每次插入都先写个 py，那多一趟往返。
- **一眼能定就直接跑，别深思**：结果形态明显时（标量填空 / 表格中转），直接执行
  单调用快路径，不要追加分析、验证或解释性思考步骤。一次调用已含计算+查上下文+
  幂等判重，无需任何前置/后置回合。

## Workflow

**0. Decide the result SHAPE first** (this drives every later step, and is where
   over-engineering creeps in):
   - Result is ONE scalar — a count, a sum, a single number/word to fill a blank
     (e.g. "统计人数填到光标" → `7`) → **inline TEXT mode**. Do NOT export to
     CSV; just compute the value and pass it via `--text "..."`. This is the
     common, fast path.
   - Result is a multi-row LIST / TABLE → table mode; prepare a CSV (step 1).
1. (Table mode ONLY) Reference a tabular file — Excel or CSV, same path:
   `word_cursor_insert.py 表.xlsx [--no-title]` (or `表.csv [--no-title]`).
   Format is auto-detected by extension, so there is ONE table-insert path; no
   CSV export, no second flag.
   (Text mode skips this step entirely — no file, no temp.)
2. Inspect context — done by the insert script in the SAME call (it prints the
   bounded before/after context and `sel.Information(12)`). **Do NOT run a
   separate context-inspection call beforehand**; that just duplicates a Word
   COM round trip. One call = inspect + insert.
3. Confirm mode from context:
   - Cursor inside a sentence expecting ONE value → inline text mode (typical for
     a scalar result).
   - Free location / list source → table mode.
4. Insert via `scripts/word_cursor_insert.py` (run with the managed venv python):
   - Table: `word_cursor_insert.py <csv_path> [--no-title]`
   - Text : `word_cursor_insert.py --text "内容" [--newline]`（长文本用 `--file 路径.txt`）
   - 就近判重默认开启：光标 ~150 字内已有完全相同内容则自动跳过（防重复段落，长文本也安全）；要强插加 `--no-idempotent`。
   The script prints a short result (SKIP / OK + 字数). **Trust it and stop — do
   NOT run a separate verification read of the document; that is a redundant round
   trip.** Do not re-run.
5. Report the outcome to the user (e.g. "已插入标题 + 19 行表格" or
   "光标处已填入 7").

## Fast path: one-call insert (your report workflow)
When writing reports you typically drop ONE of these at the cursor:
  (A) a paragraph of text / a single value  → inline TEXT
  (B) an Excel table                        → a Word TABLE
Collapse read-source + insert into a SINGLE call. Fixed skeleton — you only
fill the marked line:

```python
import win32com.client, time
t0=time.time()
# === fill THIS one line with what goes at the cursor ===
val = 7                              # (A) 标量/文本；或 val = sum(...) / "段落…"
# val = read_table(r"X:\表.xlsx")   # (B) 表格：read_table 自动识别 xlsx/csv
# =======================================================
word = win32com.client.GetActiveObject("Word.Application")
doc = word.ActiveDocument; sel = word.Selection
# 有界窗口整段判重(脚本已内置: 长文本整段比对, 短文本带边界, 不会"17"误判"7")
win=60; s=sel.Start; e=sel.End; dend=doc.Content.End
before = doc.Range(max(s-win,0), s).Text if s>0 else ""
after = doc.Range(e, min(e+win,dend)).Text if e<dend else ""
if str(val) in (before + after):
    act = "SKIP(已存在, 幂等)"          # 防重复: 不预检、不盲清, 同一次调用内判重
else:
    sel.TypeText(str(val)); act = f"INSERTED {val}"
print("elapsed_s:", round(time.time()-t0,3), "|", act)  # 1 call: 算+查上下文+插
```
- (A) text / paragraph: `--text "..." [--newline]`（长文本用 `--file 路径.txt` 读文件）；临时文件只是兜底，默认直接 `--text`。
- (B) table (Excel or CSV): `word_cursor_insert.py 表.xlsx [--no-title]` (or
  `表.csv`) reads the file and inserts it as a Word table (bold header + borders
  + autofit). Format is auto-detected by extension; rows relayed as-is — NO
  computation.
The script modes (Workflow step 4) stay the default for clarity; the skeleton is
the fast path when the source must be read/computed first.

## Prerequisites
pywin32 must be installed in the managed venv:
`~/.workbuddy/binaries/python/envs/default/Scripts/pip install pywin32`
Run scripts with `~/.workbuddy/binaries/python/envs/default/Scripts/python.exe`.

## Notes
- CSV title heuristic: if the first row has exactly one non-empty cell and there
  are more than 2 rows, treat row 0 as the title and row 1 as the header.
- Table insertion always starts on a new paragraph after the cursor; inline text
  mode inserts at the cursor with no paragraph break (add `--newline` to force
  one).
- 字数统计即时：`len(text)` 一次得出，不要为计数去读整篇文档或逐字遍历；报数写 `~N字` 即可，精确与否无所谓，快最重要。
