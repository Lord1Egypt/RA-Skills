# Anti-Patterns: Domain Context Management

Common mistakes to avoid when building and using a DOMAIN.md.

---

## ❌ AI Anti-Patterns

### 1. Inventing Domain Facts
**Problem:** The AI guesses at what a term means or how entities relate, and acts on that guess without flagging it.
**Fix:** Any unknown term or relationship must be marked `[UNKNOWN: ...]` or `[RELATIONSHIP UNCLEAR: ...]`. Never assume.

### 2. Silently Updating the Knowledge Base
**Problem:** The AI directly edits DOMAIN.md without human review, introducing errors or hallucinated facts.
**Fix:** The AI always *proposes* updates in the `## 📋 Proposed Domain Updates` section. Humans apply them.

### 3. Using Generic Names Instead of Domain Names
**Problem:** The AI calls an entity a "customer" when the business calls it an "account", or "order" instead of "ticket".
**Fix:** Always use the exact terminology from the Glossary and Entity Registry. Mirror the user's language.

### 4. Ignoring the DOMAIN.md at Session Start
**Problem:** The AI jumps into work without loading domain context, producing output that conflicts with existing conventions.
**Fix:** Reading DOMAIN.md is the first step of every session, always. Confirm to the user that it was loaded.

### 5. Overloading Open Questions
**Problem:** Every ambiguity gets added to Open Questions but they never get resolved, making the list useless.
**Fix:** Review and clear Open Questions regularly. If something stays unresolved for more than 2-3 sessions, escalate it explicitly.

### 6. Loading Everything in Split Mode
**Problem:** The domain has been split into Tier 1/2/3 files, but the AI reads every file at session start regardless of the task. This wastes context budget and adds noise.
**Fix:** Load Tier 1 (root DOMAIN.md) always. Load Tier 2 files only when the session touches that entity or flow. Load Tier 3 only on explicit request. If unsure whether a detail file is relevant, check the entity name in the Tier 1 index first — if it's not mentioned in the current task, don't load it.

### 7. Proposing Updates Without Specifying the Target File
**Problem:** In split mode, the AI proposes domain updates but doesn't say which file they belong to. The human has to figure out where each update goes.
**Fix:** In the Proposed Domain Updates section, always specify the target file: "Update: `docs/domain/entities/quote.md`" or "Update: `DOMAIN.md` (Tier 1 — core)." Make it copy-paste ready.

---

## ❌ Human Anti-Patterns

### 8. Never Updating the File
**Problem:** The AI proposes updates, but the human never applies them — the DOMAIN.md stays stale.
**Fix:** Treat domain updates like code review. They don't need to be applied immediately, but they should be reviewed within the same sprint/cycle.

### 9. Writing It All Upfront
**Problem:** Trying to document the entire domain before starting development — leads to bloat and inaccuracy.
**Fix:** Start with just the 3-5 core entities and 1-2 flows. Let it grow organically. Premature completeness is worse than incomplete-but-accurate.

### 10. Using Technical Language in Business Sections
**Problem:** DOMAIN.md becomes a database schema or API spec instead of business domain documentation.
**Fix:** Keep entity descriptions in business language. Technical implementations go in code/specs, not DOMAIN.md. The file should make sense to a business user who isn't a developer.

### 11. One Giant Flat File for a Complex System
**Problem:** As the project grows, a single DOMAIN.md becomes hard to navigate and maintain. The AI spends context budget on knowledge that isn't relevant to the current task.
**Fix:** Once you have ~200+ lines or 10+ entities, split into the tiered structure. Keep DOMAIN.md as a Tier 1 index with entity names and business rules. Move full descriptions, flows, and history into Tier 2/3 files. See SKILL.md § Progressive Disclosure.

### 12. Treating DOMAIN.md as Immutable
**Problem:** Hesitation to change existing entries because "we wrote it that way."
**Fix:** Businesses evolve. Terminology changes. Relationships shift. DOMAIN.md should reflect current reality, not history. Use the Changelog section to record what changed and why.

### 13. Splitting Too Early
**Problem:** The domain file has 90 lines and 4 entities, but gets split into 8 files because "we should be organized." The overhead of managing multiple files outweighs the benefit.
**Fix:** Don't split until the file crosses ~200 lines. Below that, a single file is simpler to read, edit, and maintain. The AI can load the whole thing without context budget concerns.

---

## ✅ Healthy Patterns

- Domain updates happen at the **end** of every meaningful session — even small ones
- The file is **version controlled** alongside the codebase
- New developers are asked to **read DOMAIN.md before touching code**
- When requirements conflict with DOMAIN.md, the team **discusses and resolves** before proceeding
- The AI **references specific DOMAIN.md entries** when making decisions (e.g., "Per the Business Rules section, a Generator in `maintenance` status cannot be assigned to a Rental")
- In split mode, the AI **names the files it loaded** at session start so the human knows what context is active
- The **~200 line threshold** is treated as a guideline, not a hard rule — split when it feels heavy, not when a counter trips

