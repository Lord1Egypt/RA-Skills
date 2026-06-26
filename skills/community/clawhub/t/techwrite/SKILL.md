---
name: techwrite
description: Deep workflow for technical prose—audience, purpose, structure, precision, examples, diagrams, review, and iteration. Use when drafting developer docs, design notes, internal guides, RFCs, or public technical articles.
---

# Technical Writing (Deep Workflow)

Technical writing succeeds when **readers can act** or **decide** with less confusion. Optimize for **clarity**, **correctness**, and **appropriate depth**—not word count.

## When to Offer This Workflow

**Trigger conditions:**

- New feature docs, migration guides, API references
- RFCs, ADRs, architecture summaries
- Runbooks, onboarding docs, postmortems (writing-heavy)
- “Make this clearer” edits on existing pages

**Initial offer:**

Use **six stages**: (1) define audience & goal, (2) outline & scope, (3) draft core content, (4) examples & edge cases, (5) review for clarity, (6) ship & maintain. Ask for **template** or **style guide** if org has one.

---

## Stage 1: Audience & Goal

**Goal:** One primary reader persona; one **outcome**.

### Questions

1. **Who** reads (new hire, partner engineer, SRE, end user of API)?
2. **Job-to-be-done**: debug issue? integrate API? approve design?
3. **Constraints**: word limit, legal review, localization later?

### Anti-goals

- “Everyone” audience → usually **nobody** satisfied—prefer layered docs (overview + deep dive links)

**Exit condition:** **Success sentence**: “After reading, the reader can ___.”

---

## Stage 2: Outline & Scope

**Goal:** **BLUF** + **sections** that match mental model.

### Practices

- **Top**: context + outcome + prerequisites
- **Middle**: procedural steps OR conceptual model—pick one primary mode per doc
- **Bottom**: troubleshooting, FAQ, links, changelog

### Scope control

- **In scope / out of scope** box for ambiguous topics
- **Version** and **last reviewed** metadata for fast-moving products

**Exit condition:** Outline reviewed; **order** matches reader journey (often happy path first).

---

## Stage 3: Draft Core Content

**Goal:** **Precise**, **scannable**, **honest**.

### Style

- **Short sentences**; **active voice** for procedures (“Click…”, “Run…”)
- **Define terms** on first use; **glossary** for large docs
- **Avoid** vague adjectives (“robust”, “seamless”) without criteria

### Structure signals

- **Headings** that describe content; **lists** for sequences and parallel items
- **Numbered steps** for order-sensitive actions

**Exit condition:** First full pass complete—**ugly OK**, precision matters more than polish.

---

## Stage 4: Examples & Edge Cases

**Goal:** Examples **reduce tickets**; edge cases **build trust**.

### Examples

- **Minimal complete** snippet; **realistic** names; **expected output**
- Show **failure** example when errors are common—include **how to fix**

### Edge cases

- Permissions, rate limits, idempotency, backward compatibility
- **“If you see X, do Y”** troubleshooting table when helpful

**Exit condition:** At least one **end-to-end** path works on fresh machine (when procedural).

---

## Stage 5: Review for Clarity

**Goal:** Remove **ambiguity** and **hidden assumptions**.

### Checklist

- **Ambiguous pronouns** (“it”, “this”)—replace with nouns
- **Implied steps**—make explicit
- **Diagrams**: labeled arrows; **alt text** for accessibility
- **Links**: avoid broken anchors; prefer **stable** URLs

### Reviews

- **Peer review** for technical accuracy; **non-expert** read for onboarding docs

**Exit condition:** Another reader can follow without asking clarifying questions—or questions are **FAQ’d**.

---

## Stage 6: Ship & Maintain

**Goal:** Docs **decay**—plan updates.

### Practices

- **Owner** field; **review cadence** for critical paths
- **Changelog** or **page history** when platform changes often
- **Deprecate** old pages with redirects

---

## Final Review Checklist

- [ ] Audience and success outcome explicit
- [ ] Outline matches reader journey
- [ ] Procedures numbered; concepts separated from steps
- [ ] Examples + failures where needed
- [ ] Reviewed for ambiguity; diagrams accessible

## Tips for Effective Guidance

- Prefer **concrete nouns** over abstractions (“the database primary” vs “the system”).
- When user pastes draft, do **surgical** edits—preserve voice unless clarity suffers.
- For **non-native readers**, avoid idioms and culture-specific jokes.

## Handling Deviations

- **Marketing-heavy request**: separate **facts** from positioning; flag risky claims.
- **Legal-sensitive**: suggest expert review; avoid drafting binding language unless qualified.
