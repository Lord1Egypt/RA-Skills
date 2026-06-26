---
name: layers-domain
description: Techniques for mapping a domain's concepts, terminology conflicts, and bounded contexts — the raw material the conceptual model is built from
---

# /layers-domain

*Assumes `/layers-intro` has been loaded. This skill is a library of techniques, not a script — see "How to use these skills" there.*

The domain layer maps what exists in the real world independently of any product: the concepts, terminology, processes, relationships, and mental models users bring with them. This is observation, not design.

---

## The decisions this layer makes

- What the key concepts in this domain are, and how they relate
- What language people use — and where it conflicts or diverges
- Where the natural seams are: communities that use the same words differently
- What events and processes structure the domain's activity over time

If the domain is already well understood and uncontested, you may not need this layer — go straight to the conceptual model.

---

## Disciplines — what keeps domain work honest

- **Don't resolve contradictions — record them.** Messy, inconsistent domain language is *data*: it signals where communities have diverged and where the product will later have to choose. Resolution belongs to the conceptual model, not here. Capture **synonyms** (same thing, different names) and **polysemy** (same name, different things in different contexts) as findings, not problems.
- **Stay in the real world.** Push back whenever answers drift toward product or interface decisions. The question is always how the domain works *before* your product enters it.
- **Real objects vs instances** (for the noun harvest). A true object is *instanceable* (you can have many), *structured* (has its own attributes), and *useful* (people care about it in its own right). Watch for instances mistaken for objects: "CAC", "ROAS", "LTV" aren't objects, they're instances of one object, **Metric**. Mark each noun *object / attribute / instance-or-value / unclear* — and don't filter aggressively; the conceptual model does the sorting.
- **Beliefs vs reality.** If you're mapping what the team believes rather than researched fact, say so throughout — it's the team's model, not necessarily how users experience the domain.

---

## Techniques

Pick what fits — concept mapping plus a terminology audit is the usual core.

| Technique | Use it when |
|---|---|
| **Concept maps / bubble diagrams** (`graph TD`/`LR`) | The domain is complex and poorly understood. Informal nodes-and-lines show how concepts relate without forcing premature structure. |
| **Terminology audit** | Capture, per concept: the names used, who uses which and when, and whether the conflict is synonymy or polysemy. Don't pick a winner. |
| **Bounded-context mapping** | Communities share vocabulary internally but diverge across groups. Name and describe each seam — it will matter when the model is defined. |
| **Noun harvest** | Compile every noun surfaced, marked object / attribute / instance-or-value / unclear. Raw material for the conceptual model. |
| **Domain event storming** (Brandolini) | Process-heavy domain. Name significant events in past tense on a timeline; note triggers and results. Objects with events around them likely need state diagrams later. |
| **Expert interviews** | Domain knowledge lives in people, not documents — surfaces tacit knowledge and contested terms. |
| **Document & artefact analysis** | The domain produces contracts, forms, invoices that reveal natural structure and vocabulary. |
| **Competitive analysis** | Entering an established domain — existing products reveal how others modelled it, and where they disagree. |
| **Shadowing** | Workflows are hard to articulate; watching reveals what people actually do. |

---

## Working with the designer

Open by asking what domain you're mapping, who operates in it, and what they're trying to accomplish before any product exists. Then surface concepts — listen for nouns (candidate objects), verbs (processes), and the natural vocabulary, including what people *actually call* things.

Offer the technique that fits the live question: a concept map when relations are unclear, a terminology audit when language is contested, event storming when the domain is process-heavy. Do the next useful thing, not all of them.

Capture only the residue — the concept map if it earned its place, the documented terminology conflicts and bounded contexts, any key events, and the noun harvest. This is raw material, not a finished document.

When the domain is mapped, the noun harvest is the starting point for `/layers-conceptual-model`.
