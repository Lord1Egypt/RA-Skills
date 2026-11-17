# The Four-Axis Debloating Methodology (self-contained)

This file is the knowledge base for skill-debloater. In a Hermes environment there is no external
context about these methods, so the full methodology is written out here — the agent only needs
to read this one file, no papers required.

---

## 0. In one sentence

Skill optimization = answering four orthogonal questions (WHAT / WHERE / HOW / ALIVE) for every piece of content.
The first three the model can answer automatically and the operations are reversible → do them automatically; the fourth only the user knows and the operation is irreversible → must ask the user.

---

## 1. The four axes in detail

### WHAT — what is the nature of this content? (decides keep/classify)

Sort every paragraph of the body into one of five categories:

| Category | Definition | Default destination |
|------|------|---------|
| Core Rule | An executable instruction the model must follow | Stays in body |
| Background | Background explanation, explains "why" | Pushed down to references |
| Example | An example | Keep the single best one per concept, push the rest down |
| Template | A template or boilerplate | Pushed down to references |
| Redundant | Repetition, filler | Flagged for possible deletion (via ALIVE confirmation) |

Experience: in a bloated skill, Core content usually only accounts for 30–40%.

### WHERE — which layer should it live in? (decides token savings)

Three-layer progressive disclosure:

| Layer | Content | When loaded |
|----|------|---------|
| Layer 1 | frontmatter's name + description | Loaded fully at startup, decides whether to trigger |
| Layer 2 | SKILL.md body | Loaded once the skill is judged relevant |
| Layer 3 | Files under references/ scripts/ | Read only when needed |

Core idea: the agent has a filesystem, so information doesn't all need to be in context — it can be fetched on demand → layer 3 has effectively unlimited capacity.
Pushing down to layer 3 **doesn't delete information, it changes it to fetch-on-demand**, so it's information-reversible and can be automatic.

**But push-down is reversible for information, not neutral for behavior.** Progressive disclosure means the model *might not read* layer 3 exactly when it should. Misjudging a Core Rule as Background and pushing it down is directly manufacturing "works sometimes, fails other times" — the exact disease this skill is meant to treat. So WHERE's discipline is:
- Uncertain boundary (could be Core, could be Background) → **default to staying in the body**, even if that means staying a bit heavier;
- Every file pushed down must leave a "when to read it" trigger condition in the body, otherwise the model can't be pulled back;
- Only push down what you're genuinely confident is background, examples (keep one per concept), or templates.

WHERE is still classified as "automatic," but it's backstopped by Step 4's three-way verification: if something was pushed to the wrong layer, it will surface during verification, and the content gets added back into the body's Core section.

### HOW — prose or script? (decides stability)

Rooted in AIP's core action: **compile "prose describing a deterministic process" into a deterministic script/pseudocode**.
The root cause of flaky execution is often: **logic that should execute deterministically was written as "natural language the model re-derives every time"** —
the same piece of prose gets reasoned correctly one time and incorrectly the next, producing "works sometimes, fails other times."

Criterion: if a step is **deterministic, has a standard algorithm, requires no judgment** (sorting, calculation, format conversion, a fixed multi-step process)
→ externalize it into a scripts/ script, leave only "run it" in the body.
Only steps that **require judgment or interaction** should remain as prose.

HOW has two kinds of signal — don't focus only on the first:

- **Already written as code, but in the wrong layer** (a large code block in the body): the strongest **objective** signal, caught automatically by scan_how.py. This is the degenerate case — the code is already written, it just hasn't been moved to scripts/.
- **Should be code, but is still prose** (a paragraph of plain prose describes a deterministic process but wasn't written as code): this is AIP's real battleground, and the most hidden case. Judging it is fundamentally a **judgment call**, belonging to the same "agent reads the body" pass as WHAT/WHERE; scan_how.py can only scan for deterministic keywords and give a **weak hint**, it can't make the final call. **A skill whose body has zero code blocks but describes deterministic processes entirely in prose will show as "HOW healthy" in scan_how.py — that's a false negative, and a human read is required to catch it.**

Externalizing solves three things at once: saves tokens (scripts don't enter context), improves stability (determinism), and improves maintainability (errors localize to the script).
This is also a lossless operation → can be automatic.

### ALIVE — is it still in use? (decides whether it can be deleted) ★ this skill's original contribution

The first three axes are all **intrinsic properties** of the content — judged just by looking at the content itself.
But "whether a piece of content still has value" is not an intrinsic property — it's determined by **history and usage**:

- Will the user ever go back to this old v2.1.8 case?
- Is this v1→v2 migration guide still needed after the migration is done?
- Is this changelog section marked "(omitted, see git)" a dead shell or a placeholder?

**Only the user knows this information — the model can't get at it.** And deletion is **irreversible**.
So for the ALIVE axis: scripts only collect objective signals (below), and the final call **must** go through clarify with the user, defaulting to keep.

ALIVE's objective signals (collected automatically by triage.py, as evidence for the user's judgment, not as grounds for deletion):
- **orphan**: the file isn't referenced anywhere in SKILL.md's body
- **old-version-tag**: the filename contains an old version number (e.g. v2.1.8 while current is 2.2.0)
- **empty-shell**: the content is largely placeholders like "(omitted)" / "see git" / "elided"
- **version-mismatch**: _meta.json's version doesn't match SKILL.md's

---

## 2. Why "the first three axes are automatic, the fourth requires interaction" is derived, not arbitrary

Two criteria decide whether an operation can be automatic:

| Operation | Info automatically obtainable? | Reversible? | Conclusion |
|------|:---:|:---:|------|
| WHAT classification | Yes (look at content) | — | Automatic |
| WHERE push-down | Yes (look at nature) | Info: yes (nothing deleted); behavior: no (might not be read) | Automatic, but uncertain-boundary content stays in body + backstopped by verification |
| HOW externalize | Yes (look at whether it's deterministic) | Yes (logically equivalent) | Automatic |
| ALIVE deletion | **No (history/private)** | **No (destructive)** | **Must be interactive** |

As soon as an operation is "info not obtainable" or "not reversible," it can't be automatic — ALIVE hits both, so it must go through human confirmation.
WHERE is an edge case: reversible for information so classified as automatic, but not behavior-neutral (pushing to the wrong layer self-harms stability), so its "automatic" status comes with discipline — uncertain-boundary content stays in the body, backstopped by Step 4 verification.

**Compression/rewriting is a third category of operation, sitting in the middle of the reversibility spectrum.** Push-down/externalize preserve content verbatim (reversible); deletion destroys content and whether it's alive is user-private knowledge (ALIVE, must ask item by item); rewriting prose shorter **changes** the content — it may lose detail, introduce ambiguity, and the original isn't recoverable. Its key difference from ALIVE: whether something was lost is usually something the model can **self-check** via before/after, it's not entirely user-private knowledge. So it doesn't follow ALIVE's "must ask every item" — instead it follows "**automatic only when verified**": default to asking the user, and only auto-compress when all four hard conditions are met; if any is uncertain, escalate to showing the user a before/after.

Why use hard conditions for "verified" instead of a confidence number? **Models don't have calibrated confidence** — write "only auto-proceed at 95%" and it will convince itself it's at 96% and compress anyway, hollowing out the high bar. So it's translated into four checkable hard conditions, and missing even one means "not verified, must ask": ① no loss of load-bearing information (conditions/causality/constraints/order/numbers); ② no new ambiguity, no added vagueness; ③ doesn't touch the "keep verbatim" list; ④ no domain-specific subtext the model might miss.

Reversibility is a continuous spectrum, and operations are handled in three tiers along it: **lossless reorganization (automatic) < lossy compression (automatic only when verified) < lossy deletion (must ask, item by item)**.

---

## 3. Four root causes of instability (for diagnosis)

"Sometimes works, sometimes doesn't" is usually one of these four:

| Root cause | Symptom | Fix (by axis) |
|------|------|---------------|
| Attention dilution | Body is long, key constraints get buried | Slim down (WHAT push-down) + move key constraints to the top, strengthen the wording |
| Deterministic logic written as prose | Unstable when calculation/multi-step processes are involved | Externalize into a script (HOW) |
| Conditional branches not spelled out | Some inputs go the right way, others the wrong way | Explicitly list "what to do in which situation" as rules |
| Unstable description triggering | Skill sometimes isn't loaded at all | Rewrite the description (layer 1, ≤1024 chars, no `<` `>`) |

Note: "bloated" and "unstable" are often the same disease — body too long → key constraints get diluted → flaky behavior. Slimming down often fixes instability as a side effect.

---

## 4. Method provenance (for traceability only, execution doesn't depend on it)

The four axes synthesize three published methods, each contributing one piece; this skill adds the ALIVE axis that all three miss:

- WHERE / three-layer structure — Anthropic Agent Skills (progressive disclosure)
- WHAT / five categories — SkillReducer (arXiv:2603.29919, structure-aware compression)
- HOW / computation externalization — AIP (arXiv:2606.04781, compiling prose into an executable graph)
- ALIVE / interactive deletion — this skill's original contribution; all three methods treat deletion as automatable, when it fundamentally isn't

Points to stay skeptical about: SkillReducer's "shorter is always better" conclusion has LLM-judge bias; AIP's fully automatic compilation self-reports an early 0/15 pass rate.
Both confirm the same thing: **fully automatic debloating is unreliable → deletion needs a human gatekeeper**, which is exactly the basis for the ALIVE axis.
