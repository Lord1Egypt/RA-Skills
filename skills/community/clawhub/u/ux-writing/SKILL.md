---
name: ux-writing
description: Deep UX writing workflow—voice, clarity, error and empty states, forms, accessibility of text, localization hooks, and collaboration with design. Use when polishing UI copy, reducing support burden, or establishing product voice.
---

# UX Writing (Deep Workflow)

UX writing is **interface design** with words: **reduce cognitive load**, **prevent errors**, and **build trust**. It is not marketing polish bolted on at the end.

## When to Offer This Workflow

**Trigger conditions:**

- Confusing errors, high drop-off flows, empty states that feel broken
- Inconsistent terminology across product
- Accessibility review flags **unclear** labels or **verbose** instructions
- Preparing **voice & tone** guidelines for a design system

**Initial offer:**

Use **six stages**: (1) context & users, (2) voice & tone, (3) clarity & structure, (4) errors & recovery, (5) forms & validation, (6) a11y & localization. Ask for **screenshots**, **current copy**, and **metrics** (support tickets, drop-off).

---

## Stage 1: Context & Users

**Goal:** Copy matches **mental model** and **emotional state**.

### Questions

1. **User goal** on this screen—primary action?
2. **Stress level**: billing, security, health—tone adjusts
3. **Expertise**: first-time vs power user—**progressive disclosure**

### Constraints

- **Character limits** in UI components; **legal** must-review text

**Exit condition:** **Scenario brief** per screen or flow—not generic “friendly.”

---

## Stage 2: Voice & Tone

**Goal:** **Consistent** personality with **flexible** tone by context.

### Voice (stable)

- Principles: e.g., **clear**, **respectful**, **confident**, **human**—pick 3–4 and **define** anti-patterns

### Tone (situational)

- **Success**: brief affirmation
- **Error**: calm, **no blame**; **next step** forward
- **Empty state**: **invite** action without condescension

### Terminology

- **Glossary**: “Workspace” vs “Project”—**one term** per concept; align with **engineering** names users see in API/docs

**Exit condition:** **Before/after** examples for **three** contexts (success, error, empty).

---

## Stage 3: Clarity & Structure

**Goal:** **Scannable** text—**front-load** meaning.

### Practices

- **Titles** specific: “Payment failed” not “Something went wrong” (unless generic is truly unknown)
- **Buttons** use **verbs**: “Save address” not “OK”
- **Sentence case** per style guide; **avoid** ALL CAPS except acronyms
- **Numbers/dates**: user locale; **relative** time when helpful (“Updated 2 min ago”)

### Microcopy hierarchy

- **Primary** message → **secondary** detail → **tertiary** learn more

**Exit condition:** **Redundant** words cut; **one idea** per sentence in critical paths.

---

## Stage 4: Errors & Recovery

**Goal:** Users **understand** what happened and **what to do next**.

### Structure

- **What happened** (plain language, no codes alone)
- **Why** (if known and helpful—not stack traces)
- **What to do** (steps, link to support, retry)
- **Support** path when stuck

### Security

- **Don’t** leak whether an **email exists** on login if policy requires ambiguity—coordinate with security

**Exit condition:** **Top 10** error states have **rewritten** copy + **engineering** alignment on **truth** of messages.

---

## Stage 5: Forms & Validation

**Goal:** **Inline** help and **validation** text **accessible** and **timely**.

### Practices

- **Label** every input; **don’t** rely on placeholder alone as label
- **Errors** associated programmatically (`aria-describedby`); **announce** on submit failure
- **Password rules** visible **before** typing when complex
- **Success** confirmation for destructive actions

### Tone on errors

- **Avoid** shame (“Invalid input”) → **neutral** (“Enter a date after Jan 1, 2024”)

**Exit condition:** **Form** review checklist applied to **highest-traffic** form.

---

## Stage 6: Accessibility & Localization

**Goal:** Text works for **screen readers** and **translation**.

### Accessibility

- **Alt text** for meaningful images; **decorative** marked so
- **Instructions** not color-only; **error** identification not by color alone

### Localization (i18n)

- **No** concatenated strings with **word order** assumptions across languages
- **Punctuation** and **formality** per locale—**pseudolocale** QA for overflow

**Exit condition:** **String extraction** friendly; **no** embedded HTML in strings without plan.

---

## Final Review Checklist

- [ ] Voice/tone documented with examples
- [ ] Critical paths scannable; verbs on CTAs
- [ ] Errors: cause + next step + support path
- [ ] Forms: labels, validation, a11y association
- [ ] i18n-safe string patterns

## Tips for Effective Guidance

- **Read aloud**—if awkward, revise.
- Pair with **design**: copy length affects **layout**; **don’t** fight the grid blindly.
- For **AI products**, clarify **machine** vs **human** responsibility in copy.

## Handling Deviations

- **Dense enterprise UIs**: prioritize **task** **efficiency** over personality.
- **Regulated** industries: **legal** review loop—suggest **plain** alternatives, not legal advice.
