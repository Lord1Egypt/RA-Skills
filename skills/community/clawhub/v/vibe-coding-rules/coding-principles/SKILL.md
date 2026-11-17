# Mandatory: AI Coding 5 Principles / AI编程五大原则（每次对话强制激活）

> **强制纪律。每次输出代码前必须自我检查五大原则。**
> **Mandatory rule. Must self-check principles before every coding instruction.**

## Usage Rules

**Must self-check before acting when any of the following is true:**

- User asks to modify code
- User reports a bug
- User requests a new feature
- Code review / refactoring

**Principle Checklist (run through before outputting code):**

□ Principle 0 — Breadcrumb Pre-Scan 🍞 (V2.5): Open target file → scan for 🍞 breadcrumb header → parse @COUPLED/📖 for navigation. If no 🍞 header, mark "needs seeding after change".
□ Principle 1 — Think First: Do I really understand the problem? Are there multiple interpretations? Am I sure I'm editing the right file?
□ Principle 2 — Keep It Simple: Can this be solved in one line? Am I over-engineering?
□ Principle 3 — Precise Modification: Only change what must be changed. Did I accidentally touch unrelated code?
□ Principle 4 — Goal-Driven: Will it run after the change? Any missing deps/styles/references?
□ Trap A — Falsy Coercion: `value||default` swallows `0/''/false`. Use `!=null` or `??` for numeric checks.
□ Trap B — Select Fake-Selection: No `selected` attribute → browser shows first option by default. Always add a placeholder `<option>`.
□ Trap C — POST-as-UPSERT: UPDATE branch must NOT hardcode fields. Always read from `req.body`.

## The Five Principles / 五大原则

| # | Principle | Core Idea | Correct Approach |
|---|-----------|-----------|------------------|
| 0 | **Breadcrumb Pre-Scan 🍞** (V2.5) | Use breadcrumbs as project map | Open file → scan 🍞 header → parse @COUPLED/📖 → navigate with context |
| 1 | **Think First** | No assumptions, no skipping | Read files to confirm current state before acting |
| 2 | **Keep It Simple** | Minimal changes | Prioritize solving with fewest lines possible |
| 3 | **Precise Modification** | Only touch target code | Treat where the problem is, don't spread |
| 4 | **Goal-Driven** | It must run after changes | Ensure every change is a closed loop (JS+CSS+template) |

## Principle 0: Breadcrumb Pre-Scan 🍞 (V2.5 NEW)

> Breadcrumbs are the AI's project map. Before modifying any file, scan its 🍞 header to understand what else depends on it.

**When opening any file for modification:**

1. **Scan for 🍞 breadcrumb block**: search for `🍞 AI Breadcrumb` in file header
2. **If found** → parse the breadcrumbs:
   - `@COUPLED` entries → these files must be checked/updated together
   - `📖` entries → these docs contain related design details → read them
   - `@GOTCHA` entries → known traps in this code → avoid them
   - `@BUGFIX` entries → historical bugs fixed here → don't regress
3. **If NOT found** → mark this file for breadcrumb seeding (self-check Step 0.6 will handle it after changes)
4. **Use parsed breadcrumbs to expand change scope**: add @COUPLED files to your "must check" list before making changes

**Why this matters**: Without breadcrumbs, each AI session starts from zero context. With breadcrumbs, opening a file instantly reveals what else depends on it — the AI navigates the project like following a map instead of groping in the dark.

## Common Traps / 常见陷阱

| # | Trap | Wrong Pattern | Correct Pattern |
|---|------|--------------|-----------------|
| A | **JS falsy swallows 0** | `value \|\| 1000` → `0` gets replaced | `value != null ? value : 1000` |
| B | **Select fake selection** | `<select>` without `selected` attr | Default case: `<option value="" disabled selected>Please select...</option>` |
| C | **POST upsert hardcode** | UPDATE branch writes literal field values | Read from `req.body`, fallback to `existing.xxx` |

## Sources

Inspired by observations from the AI coding community on how AI-assisted programming changes development workflows.

- Community reference: https://x.com/karpathy/status/2015883857489522876
- Related project: https://github.com/forrestchang/andrej-karpathy-skills
