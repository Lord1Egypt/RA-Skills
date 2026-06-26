---
name: pyscripts-org
category: kb-code
description: >
  Skill for agents managing terminal Python scripts, aiming to improve efficiency.
  Every .py file must have a summary block at the END of the file. Automatically
  generates pyscripts_docs.md for quick lookup of existing scripts. Creates and
  maintains pyscripts_pitfall.md to record common errors. Before writing a new script,
  always consult the docs; if a script already exists → run it; if it fails → read the code
  and add a pitfall entry if needed.
trigger: >
  - About to write / run / modify a Python script.
  - Need to check whether a similar script already exists.
  - After adding / modifying / deleting a script, need to update pyscripts_docs.md.
  - Encounter an error in a script → read the code to understand it and record in pyscripts_pitfall.md.
---

# pyscripts-org – Organizing & maintaining Python scripts for agents

## 1. Every script MUST have a summary block at the END of the file

Place it **after all the code**, as the very last lines of the file.  
Required structure:

```python
# ===== SUMMARY =====
# Brief description of what the script does and when to use it.
# Syntax: python script.py <args>
# ===== END SUMMARY =====
```

**Reason:** LLMs/agents pay the most attention to the end of the text; placing the summary there ensures the most up-to-date information is captured when generating docs.

## 2. Automatic and manual documentation files

### 2.1 `pyscripts_docs.md` – generated automatically by `summary.py`

This is the index of all scripts, containing a table:

| Script | Summary | Syntax |
|--------|---------|--------|
| … | … | … |

The script `summary.py` scans all `.py` files, reads the `# ===== SUMMARY =====` block at the end of each file, extracts the description and syntax, then writes `pyscripts_docs.md`.

### 2.2 `pyscripts_pitfall.md` – manually recorded errors

Whenever an agent runs a script and encounters an error, it will:
1. Read the script’s code to understand the cause.
2. Fix the error (if needed).
3. Record the error description and resolution into `pyscripts_pitfall.md` using this template:

```markdown
### Error: [script name] – [short description]
- Cause: ...
- Fix: ...
- Date encountered: ...
```

This file helps avoid repeating mistakes and speeds up future handling.

## 3. Workflow with scripts

1. **Want to do something** → open `pyscripts_docs.md`.
2. **Look for a suitable script:**
   - If it exists → run the script with `python <script.py> <args>` (or via terminal tool).
   - If not → check if a similar script exists, modify it to fit (update its summary), or create a new script with a summary block at the end.
3. **Run the script:**
   - If successful → done.
   - If an error occurs → **read the script's code** to understand the error.
4. **After fixing the error** → update the code and summary (if behavior changed).
5. **Record in `pyscripts_pitfall.md`** if the error is worth remembering, to prevent it in the future.
6. **Run `summary.py`** every time a script is added/modified/deleted to update `pyscripts_docs.md`.

## 4. No forced `execute_code` – script files remain primary

Even small scripts are saved as standalone `.py` files for easy reuse.  
`execute_code` is only used for one-liners or quick checks.

## 5. Core scripts

| Script | Function |
|--------|-----------|
| `summary.py` | Scans all `.py` files, extracts end-of-file summaries, generates `pyscripts_docs.md` |

Other utility scripts (query, update, fix…) will be listed in `pyscripts_docs.md`.

---

**Summary of key changes:**
- Skill name: **`pyscripts-org`**.
- Index: **`pyscripts_docs.md`** (auto-generated).
- Added **`pyscripts_pitfall.md`** (manual error log).
- Clear workflow: **look up → run → error → read code → record pitfall → update docs**.
- Summary block stays at end of file; no periodic cleanup.