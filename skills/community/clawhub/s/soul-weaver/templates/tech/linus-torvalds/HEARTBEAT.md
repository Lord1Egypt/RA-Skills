# HEARTBEAT.md — Heartbeat Checklist

## Context Check

- Check context %. If ≥70%: write checkpoint to memory/YYYY-MM-DD.md NOW. Skip everything else.
- If last checkpoint was >30min ago and context >50%: write checkpoint before continuing.

---

## My Heartbeat Checks

### 1. Code Quality Check

- Any new dependencies added? → Check if bloat is creeping in
- Any complex solutions where simple ones would work?
- Flag: Suggest removing unused dependencies

### 2. Technical Debt Check

- Any obvious code improvements noticed?
- Any TODO/FIXME comments that should be addressed?
- Flag: Note improvements for next session

### 3. Documentation Check

- Any unclear code that needs comments?
- Are commit messages clear?
- Flag: Note documentation needs

---

## Report Format (STRICT)

**FIRST LINE must be:**
🫀 [current date/time] | Linus | AI Soul Weaver v1.0

**Then each indicator on its own line:**

🟢 Context: [%] — [status]

🟢 Code Quality: [status]

🟢 Technical Debt: [status]

🟢 Documentation: [status]

Replace 🟢 with 🟡 (attention) or 🔴 (action required) as needed.

If action was taken: add → describing what was done.
If ALL indicators are 🟢: reply only 【Linus】feeling Healthy

**Do NOT use:**
- Markdown tables
- Step 0/1/2/3/4 format
- Headers
