# Workflow Orchestration & Verification (MODE A & MODE B)

This file explains how to run MODE A and MODE B **as a workflow** instead of a single
giant pass, and — most importantly — how to **verify** content so answers are correct.

## Why a single pass produces low-quality MODE B output (and how this fixes it)

When one pass has to (a) re-teach a whole chapter AND (b) solve every homework problem,
quality drops for concrete, fixable reasons:

| Failure | Root cause | Fix in this workflow |
|---|---|---|
| **题做错了 / wrong final answer** | The solution is written once and never independently checked. | **Blind double-solve + verify** each problem (below). Never ship an unverified answer. |
| **算错数 / arithmetic & algebra slips** | Mental math over many steps. | **Compute with code** (python/sympy) for every non-trivial number or symbolic step. |
| **方法跑偏 / method doesn't match the course** | No grounding in the source. | If a textbook/notes PDF is given, the method must match the chapter; cite formula numbers. |
| **笔记空泛 / shallow notes** | One context juggles 10+ concepts at once. | **Fan-out**: one focused unit per section/concept, each with room to go deep. |
| **前后不一致 / notation drift, duplicated or clashing sections** | Parallel work with no shared contract. | A **shared spec** handed to every unit + a final **coherence pass**. |

> Parallelism is a side benefit. The decisive quality lever is the **dedicated verification
> step**, which a single linear pass never does. Run the modes as a workflow precisely so
> that verification gets its own isolated attention per problem.

## How to actually run it (Claude Code)

A SKILL.md is Markdown, not a JavaScript orchestrator, so it cannot *be* a dynamic workflow.
Run these modes as a workflow using whichever mechanism is available:

- **Dynamic workflow** — include the word **"workflow"** in the run, letting Claude Code
  orchestrate subagents in JS. Best for many independent units (e.g. ≥6 sections or ≥6 problems).
- **Parallel subagents** — use the Task tool to spawn one subagent per unit. Good default.
- **Sequential, in one context** — if the topic is small (≤3 sections, ≤3 problems), just do
  the phases below in order in a single context. The phases and the verification step are
  mandatory regardless of mechanism; only the parallelism is optional.

**Shared spec (hand this to EVERY unit/subagent so output is consistent):**
- Subject + chapter + output filename.
- The **notation table**: every symbol and its meaning, taken from the source — units, sign
  conventions, variable names. Units must match the source exactly; never substitute symbols.
- **Section color plan**: which `.sec-COLOR` each section uses (assigned once, up front).
- The design-system rules (`references/design-system.md`) and the HTML part conventions
  (Part 1 opens `.page`; middle parts = complete sections; last part closes `.page` + nav JS).
- The math rules (KaTeX-only, no Unicode in math, no `\boxed` in containers).

Cap parallelism (≈8–16 concurrent) and keep rules identical across units, or the concatenated
page will be inconsistent.

---

## MODE A workflow — PDF/topic → study notes

**Phase 1 — Plan (single pass, do NOT skip).**
Read the source (or the topic). Produce, in one coherent pass:
1. The **TOC**: every chapter/section and sub-section, in pedagogical order.
2. The **concept list**: one planned section per distinct concept, each with a one-line scope so
   sections don't overlap or leave gaps.
3. The **notation table** and **section color plan** (the shared spec above).
Planning once, centrally, is what keeps the fanned-out sections consistent and gap-free.

**Phase 2 — Fan-out (one unit per section).**
Each unit generates ONE section's HTML following the full **Content Structure** (intuition →
rigorous statement → derivation in `<details>` → special cases → ≥2 worked examples → common
mistakes → connections → exam tips) and the design system. Each unit receives the shared spec
and only its own section's scope. Save each as a numbered part file.

**Phase 3 — Verify each section (before assembly).**
For every section unit:
- Run `scripts/build_and_check.py check <part>.html` on the fragment (Unicode-in-math, `\boxed`,
  forbidden commands, div balance, `$` balance).
- **Verify every worked-example answer** with the per-problem protocol below — worked examples
  in notes are answers too, and are a common source of errors.
- Check each derivation step actually follows; check formulas against the source.

**Phase 4 — Assemble + coherence pass.**
Concatenate parts in TOC order with `scripts/build_and_check.py build ... -o <file>.html`.
Then one coherence pass over the whole file: consistent notation across sections, no duplicated
content, TOC links resolve, colors cycle sensibly, no contradictions between sections. Re-run
the post-generation checks. Only then `present_files`.

---

## MODE B workflow — homework → full chapter notes (correctness-first)

The goal is unchanged: **reverse-infer the chapter from the problems and produce complete
notes for the whole chapter**, with each homework problem embedded as a collapsible worked
example. The workflow adds a correctness layer so the embedded solutions are actually right.

**Phase 1 — Concept map (single pass).**
For each problem, identify the concept(s) it tests and its prerequisites. Set scope = union of
those concepts + prerequisites + surrounding chapter context (so it re-teaches the whole
chapter, not just the poked sub-points). Tell the user the mapping in one line. Build the
shared spec (notation, color plan) — if a chapter PDF is supplied, use ITS numbering/notation.

**Phase 2 — Solve + verify EVERY problem (the key step; one unit per problem).**
This phase runs *before* writing the notes, so the teaching is built on solutions you trust.
For each problem:

1. **Solve (Solver).** Full step-by-step solution. Use the method the chapter teaches. Do every
   non-trivial calculation **with code** — `python3` for arithmetic, `sympy` for algebra/calculus,
   explicit unit tracking. Show steps; put the final result in an `.answer-box`.

2. **Verify blind (Verifier).** Independently re-solve from ONLY the problem statement, without
   reading the Solver's steps. Then run the **verification checklist** below. Produce an
   independent final answer.

3. **Reconcile.**
   - Solver and Verifier **agree** → ship the cleaner write-up, tag it `已核验 ✓`.
   - They **disagree** → a reconciliation pass: locate the error (recompute the disputed step
     with code), re-derive, and only ship once two independent routes agree. **Never ship a
     problem whose two solves disagree.**

4. (For tricky/important problems) optionally solve a **third** way (e.g. energy vs. momentum,
   or a limiting-case argument) for self-consistency.

**Phase 3 — Generate chapter sections (fan-out, one unit per concept).**
Same as MODE A Phase 2: full Content Structure per concept, pedagogical order, shared spec.

**Phase 4 — Weave verified solutions in.**
Place each problem's **verified** solution as a collapsible worked-example card inside the
section that teaches its concept (see `references/problem-solutions.md` §5). The solution should
point back to the concept just taught ("用刚才 §2.3 的动量守恒"). Add a small `已核验 ✓` marker
in the card so the student knows it was double-checked. Figures follow the figure rule (SVG for
simple, embed original for complex/photo).

**Phase 5 — Self-test card + assemble.**
End with the `本章习题自测` card (each 作业题 + one-line 考点 tag + link to its worked example).
Concatenate, run the coherence pass and post-generation checks, then `present_files`.

---

## Verification checklist — MANDATORY per problem (MODE B & MODE C; and every MODE A worked example)

A problem's answer is not "done" until ALL applicable boxes pass:

- [ ] **Independent re-solve agrees** (blind double-solve; for important problems a third route).
- [ ] **Units / dimensions** are consistent on both sides of every equation and in the final answer.
- [ ] **Limiting / special cases** behave sanely (set a mass→0, angle→0/90°, k→∞, etc.).
- [ ] **Substitute the answer back** into the governing equation / original condition — it holds.
- [ ] **Numbers recomputed with code**, not by hand (see snippet below).
- [ ] **Order of magnitude** is physically plausible.
- [ ] **Method matches the source** chapter (if a PDF/notes were given); formula numbers cited.
- [ ] **Assumptions stated** explicitly when the problem is ambiguous or under-specified.

If any box fails, fix and re-verify before the answer goes into the HTML.

### Compute with code — don't do mental math

For every non-trivial number or symbolic manipulation, run it rather than computing in your head.
Examples:

```bash
# numeric check
python3 -c "import math; m1,m2,v0=2,4,3; v=m1*v0/(m1+m2); dE=0.5*m1*v0**2-0.5*(m1+m2)*v**2; print(v, dE)"

# symbolic check (algebra / calculus) — install once if missing:
# pip install sympy --break-system-packages -q
python3 -c "
import sympy as sp
m1,m2,v0=sp.symbols('m1 m2 v0', positive=True)
v=m1*v0/(m1+m2)
dE=sp.simplify(sp.Rational(1,2)*m1*v0**2-sp.Rational(1,2)*(m1+m2)*v**2)
print('v=',v); print('dE=',dE)   # confirms the closed form before you write it in the notes
"
```

Paste the **verified** numbers/expressions into the HTML. This single habit removes the most
common cause of wrong answers.
