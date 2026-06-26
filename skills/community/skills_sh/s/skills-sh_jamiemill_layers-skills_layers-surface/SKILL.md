---
name: layers-surface
description: Techniques for auditing and deciding the surface against the layers below — vocabulary, object consistency, completeness, feedback, hierarchy, accessibility
---

# /layers-surface

*Assumes `/layers-intro` has been loaded. This skill is a library of techniques, not a script — see "How to use these skills" there.*

The surface layer is where everything decided below becomes something a person actually encounters: words, sounds, visuals, physical affordances, motion, feedback. It's the most medium-specific layer, but the decisions that matter most first are universal — they hold whether the surface is a screen, voice interface, physical device, or service touchpoint.

Surface problems are often symptoms of deeper ones. The central discipline here is telling apart issues you can fix at the surface from issues that need a lower layer revisited.

---

## The decisions this layer makes

- Whether the surface honours the vocabulary and objects from the conceptual model
- Whether every affordance from the breadboard is present — and whether any surface element has no model behind it
- Whether the emotional register fits the jobs users are doing
- How the user knows what happened, what's in progress, and what went wrong
- What's most prominent, and whether it should be
- Whether everything is accessible to the users who need it

---

## Disciplines — what keeps the surface honest

- **Surface fix vs deeper-layer issue.** The key judgement: is this something to fix in the copy/layout, or a symptom whose root is in the conceptual model or interaction flow? Wrong vocabulary may be a rewrite — or a model that never settled the term. Route deeper issues back to the relevant skill rather than patching the symptom.
- **Terms match the ubiquitous language.** Flag direct violations (a model term used inconsistently), unlisted terms (surface words not in the model — add to model, or remove as noise), and tone misalignments.
- **Object consistency.** No shapeshifters (same object in significantly different forms across contexts), no masked objects (a form where the user can't recognise the object type).
- **Completeness both ways.** Every breadboard affordance is present; no surface element exists with no model or flow behind it (those are interaction decisions that slipped through — route to `/layers-interaction-flow`).
- **Errors diagnose, explain, recover.** "Something went wrong" fails all three. Flag every error state that doesn't do all three.
- **Prominence reflects importance.** What the flow needs the user to notice is what stands out; nothing prominent that shouldn't be.
- **Accessibility is decided, not defaulted.**
- **Emotional register matches the emotional and social jobs** from user needs — not the product's benefit framed as the user's.

---

## Techniques

Two kinds of work live here: auditing existing surface against the layers below, and working through open surface decisions. Use whichever the situation calls for.

| Technique | Use it to |
|---|---|
| **Vocabulary check** | Take the ubiquitous language list; check every label, heading, button, error, notification, help string against it. |
| **Object-consistency check** | For each model object: where does it appear, in how many forms? Catch shapeshifters and masked objects. |
| **Completeness check** | Walk the breadboard against the surface in both directions — missing affordances, and surface with no model behind it. |
| **Emotional-register check** | Return to the emotional and social jobs; find where tone, framing, or emphasis misaligns. |
| **Feedback & error inventory** | For each action and state transition: how does the user know it worked, is in progress, or failed — and what to do next? |
| **Hierarchy review** | Per key place: what must the user notice or act on, and does the surface make that most prominent? Decide what's primary before how to signal it. |
| **Accessibility pass** | Per medium — screen (contrast, sizing, touch targets, keyboard, screen-reader labels, focus), voice (everything conveyed verbally, recovery without visual context), physical (reach, tactile differentiation, lighting, no fine-motor requirement). |
| **Consistency pass** | Similar things treated similarly, different things differently; medium conventions honoured or deliberately broken. |
| **Make it (real medium, mockups, style tiles, prototypes, design system, copy-first)** | When producing surface rather than auditing it. Work in code for real interaction feedback; mockups for layout/hierarchy; style tiles for early tone; prototypes for timing and motion; extend (don't contradict) an existing design system; write copy first when language is the primary material. |

---

## Working with the designer

Establish the medium and what exists from below — conceptual model (objects + ubiquitous language), breadboard, job stories including emotional/social jobs. If surface exists, audit it; if not, work the open decisions.

Offer the technique that fits the live concern — a vocabulary check when terms feel off, a feedback inventory when users don't know what happened, an accessibility pass when it's been left to defaults. Don't run all ten.

Capture only the residue: audit findings (each tagged surface-fix or deeper-layer issue), the open surface decisions grouped and prioritised (with options and constraints), the cross-layer issues to resolve first, and what's already working well so it isn't lost in revision.

The surface either honours what's decided below or undermines it. Revisit after any significant change to the conceptual model or interaction structure.
