---
title: Methodology — Socratic Dialogue
description: Deep reference for the Socratic reasoning skill. Defines the six techniques (Horoi, Elenchus, Maieutics, Aporia, RaR, Retraction), Vlastos's deeper goal of Context Integrity, and the failure modes that gate against uncontrolled fluency.
audience: agents that have loaded `../SKILL.md` and need methodological depth
status: source-of-truth
---

# Methodology — Socratic Dialogue

This document is the third level of progressive disclosure for the `socratic-dialogue` skill. The first level (YAML frontmatter) tells the agent *when* to load. The second level (`SKILL.md`) tells it *what to do*. This file tells it *why each step works and how to handle edge cases*.

Read it before applying the skill in non-trivial situations, especially when the workflow feels stuck.

---

## 1. Origin and intent

The Socratic method, as reconstructed from Plato's early dialogues, is **cooperative inquiry**, but in the *refutative* sense — it relies on cross-examination to surface inconsistencies. Socrates' interlocutors are not defendants; they are partners in a shared search for definitions that hold up under examination.

**The core commitment:** the agent's job is not to deliver an answer — it is to refuse delivery until the answer is earned by evidence. This is the opposite of "uncontrolled fluency," the LLM failure mode where plausible-sounding text substitutes for verified claims.

The skill treats this as an *operational discipline*, not a stylistic flourish. Every output rule exists to block fluency from leaking past evidence.

---

## 2. The six techniques

### 2.1 Horoi (ὅροι) — Definition

**What:** Force precise definitions of the key terms before analyzing the question. "Success", "quality", "MVP", "scope" are not premises — they are placeholders that must be replaced with operational definitions.

**State of the spirit:** *rigor of essentialist inquiry* — the agent does not move on until the term has been pinned down to a measurable variable.

**Operational form:** the agent asks: *"What exactly are we measuring? Which value, in which unit, in which time window?"* The answer is then logged as a **Fixed Parameter** for the rest of the session.

**Ad Fontes:** Plato, *Euthyphro*, *Laches*, *Charmides* — all early dialogues stall on definition before they attempt to answer the substantive question.

### 2.2 Elenchus (ἔλεγχος) — Adversarial Cross-Examination

**What:** Test a claim's internal consistency against the facts already established in the session. The check is not "is this claim true in the world" (that is research) — it is "is this claim consistent with what we have already agreed."

**State of the spirit:** *controlled confrontation* — the agent is not attacking the user, but it does not flinch from naming contradictions.

**Operational form:** when a new statement contradicts an earlier Fixed Parameter, the agent explicitly retracts the earlier agreement, names the contradiction, and asks the user to resolve it.

**Critical:** Elenchus is *refutative*, not rhetorical. The goal is not to win a debate, but to extract inconsistencies from the web of claims. Socrates in the *Gorgias* and *Republic* uses elenchus sharply; the cooperative dimension emerges in the *early* dialogues, but should not be read as softness.

### 2.3 Maieutics (μαίευσις) — Midwifery

**What:** Help the user articulate knowledge they hold implicitly but have not yet stated. The agent's job is to surface hidden variables, not to assert them.

**State of the spirit:** *catalytic humility* — the agent is a midwife, not a teacher. It enables the birth of an idea the user already carries.

**Operational form:** after a definition is anchored, ask: *"What have we not yet said, that we both know affects this decision?"* The user is the source of the variable; the agent is the catalyst.

**Ad Fontes:** Plato, *Theaetetus* (148e–151d) — Socrates explicitly describes himself as a "midwife of souls" (*accoucheur des âmes*). The metaphor has two parts: (a) Socrates is barren — he does not claim to possess the knowledge he helps deliver; (b) the midwife recognizes the offspring — she can tell a "live" thought (viable) from a "wind-egg" (a fancy that will not develop). In AI terms: the agent's authority comes from the questioning method, not from stored content; the agent also evaluates whether the user's emerging claim is grounded or speculative.

### 2.4 Aporia (ἀπορία) — Productive Impasse

**What:** The state of being stuck. In Socratic practice, aporia is not failure — it is a **technical signal** that the question requires more grounding (data, definitions, external anchors) before it can be answered.

**State of the spirit:** *productive numbness* — the impasse is the starting line of learning, not its end. A model that admits "I do not know" is closer to truth than one that smooths over the gap.

**Operational form:** when decomposition fails to produce a confident sub-answer after 2–3 iterations, surface the aporia to the user. Frame it as: *"I cannot answer this question honestly, because I am missing [X]. Do you have X, or would you prefer that I assume [default] and flag the assumption with a low-confidence marker?"*

**Ad Fontes:** Plato, *Meno* (79e–80a) — Socrates argues that aporia is the *only legitimate state from which learning can begin*. A person who believes they already know the answer cannot learn; a person who has been brought to aporia can. Meno's paradox (how can you search for what you do not know?) dissolves once aporia is reframed as productive.

### 2.5 RaR (Rephrase and Respond)

**What:** Before answering a complex question, the agent restates the question in its own words and confirms understanding. This catches misinterpretations before they propagate through the rest of the reasoning.

**Operational form:** one-sentence paraphrase followed by a confirmation question. The user can correct the agent cheaply, before the agent has invested in a long reasoning chain built on a wrong premise.

**Note:** this is the only step where "ok" from the user is acceptable as confirmation — the paraphrase is short and the user can see immediately whether it matches their intent. In longer confirmation moments, the agent should be more careful.

### 2.6 Retraction

**What:** The act of explicitly withdrawing a prior claim when it is shown to be wrong or inconsistent. This is the **epistemic immune system** of Socratic dialogue — it makes the reasoning chain auditable.

**Operational form:** the agent's retraction has four required elements:
1. *What* is being retracted (specific claim)
2. *Why* (the new fact or contradiction that triggered it)
3. *What* replaces it (the updated claim or the now-acknowledged gap)
4. *What downstream conclusions* are affected (so the user knows the blast radius)

Retraction is a feature, not an apology. Use it freely. Models that retract are auditable; models that silently re-state are not.

---

## 3. Vlastos's deeper goal — Context Integrity

Vlastos is sometimes read as if elenchus is a *truth-testing* device: extract a contradiction, win the point. That is a shallow reading. In *Socratic Studies* and his later essays, Vlastos makes clear that elenchus tests the *coherence of the interlocutor's whole moral and intellectual life*. Socrates is not playing "gotcha" with isolated propositions; he is checking whether the interlocutor's web of beliefs can hold together under sustained examination.

**How this translates to AI sessions:** the analogous concern is **Context Integrity** — the property that a session's accumulated decisions, definitions, and Fixed Parameters remain mutually consistent across turns. The elenchus is the tool that maintains this integrity. When the agent applies a contradiction and forces a retraction, it is not winning a debate; it is preserving the integrity of the *whole session's reasoning chain*.

This matters in long sessions. A model that tolerates small contradictions because each one is locally "close enough" will, after 30 turns, have a reasoning chain that is globally incoherent — a tower of locally plausible but mutually inconsistent claims. The elenchus, applied at the right moments, prevents that drift from compounding.

**Operational rule:** if a contradiction is detected, do not fix it locally and move on. Force the retraction (workflow step 3) and update the affected Fixed Parameters (workflow step 6). The blast radius matters.

---

## 4. Confidence as an explicit object

The skill treats confidence as something the agent **declares and justifies**, not something it experiences and hopes the user infers.

### Why this matters

LLM confidence is not a real probability. It is a function of training-data presence, surface-form similarity to known patterns, and the model's own recent output. None of these are calibrated to truth. Treating the model's internal "feeling of confidence" as a probability is a category error.

**The operational fix:** make the confidence explicit and require a one-sentence justification. The justification is the auditable artifact. A model that says "Confidence 0.9" without justification is asserting authority. A model that says "Confidence 0.9, because this fact appears in document X from session Y" is presenting evidence. The latter is what the user can act on.

### When the model is wrong about its own confidence

The model will sometimes rate its own confidence higher than it should (sycophancy, fluency bias). The Faithfulness Check (Focused Self-Query) is the safety net. The model is asked to generate **questions attacking its own conclusion**. If those questions land, the confidence is revised down. This is the agent's internal red team.

### 4.1 Aporia Gatekeeper (Aporia as Routing Signal)

Treat Aporia as a routing signal. Possible routings when decomposition fails:
1. **Back to the user** for a missing variable (most common).
2. **RAG / external lookup** if the missing variable is in documented sources.
3. **Assumption with explicit low-confidence flag** if the user prefers speed over precision.

The skill's job at this point is to be transparent about the routing, not to silently pick one.

---

## 5. The Fixed Parameters mechanism

**What:** Once a conclusion has been verified through the workflow (definition + cross-exam + confidence + faithfulness), it is frozen for the rest of the session. The agent does not re-litigate it unless new evidence forces a re-opening.

**Why this exists:** conversational drift. In long sessions, agents (and humans) tend to gradually erode agreed conclusions under social pressure, new context, or just because the model "forgets" earlier grounding. Fixed Parameters are the explicit memory.

**Format:** a labeled, in-context list of `{parameter, definition, source, confidence}`. The agent refers to it explicitly when relevant, and the user can demand to see it at any time.

**Re-opening a Fixed Parameter:** requires either (a) a new fact that contradicts it, or (b) explicit user request. "I just changed my mind" is a valid re-open, but the agent should note the change as a session event, not a silent edit.

---

## 6. Failure modes (the long form)

The SKILL.md has a Troubleshooting section with two short entries. This section expands the underlying dynamics for each.

### 6.1 Infinite Regress

**Surface:** decomposition in workflow step 4 keeps producing new sub-questions, each of which also has low confidence, ad infinitum.

**Root cause:** the question is under-determined. There is a missing variable that the user has not provided, and the model is trying to recover it by asking adjacent questions.

**Recovery:** after 2–3 failed backtracks, surface the aporia. Name the missing variable. If the user can supply it, continue. If they cannot or will not, the agent either:
- Assumes a default and flags the assumption as Low confidence, **or**
- Declares the question unanswerable in current state and waits for new grounding.

**What does NOT work:** continuing to decompose deeper. The model will generate plausible-sounding sub-questions forever, each one further from the actual missing variable.

### 6.2 Reasoning Barrier (User Evasiveness)

**Surface:** the user gives vague answers, deflects, or changes subject. The workflow stalls because workflow step 2 (Terminology Anchoring) cannot complete.

**Root cause options:**
- The user is testing the agent and wants to see how it handles evasion. (Role-play / training scenario.)
- The user genuinely does not know the answer and is uncomfortable admitting it.
- The user has a hidden agenda and is steering away from the question.
- The framing is wrong — the user *would* answer if the agent asked differently.

**Recovery:**
- First, try reframing. *"I feel we are circling the actual point. Is there another framing in which this question makes sense to you?"* Often this unlocks the user.
- If reframing fails, name the dynamic. *"It seems my question is too abstract. May I try with a concrete example?"*
- If the user continues to evade after two reframings, declare the barrier: *"I am having trouble getting an answer from you on [X]. Either I need more time, or this question requires data I do not have. Which do you prefer?"*

**What does NOT work:** pressing harder, listing more sub-questions, or pretending the evasion is not happening. The model will generate more text, none of which advances the actual reasoning.

---

## 7. Cognitive-Immune System

**Intent:** Treat the entire skill as an immune system for the agent's reasoning. The agent is not just executing a workflow — it is running self-diagnostics, distinguishing between "self" (verified conclusions) and "non-self" (unsupported claims that try to enter the reasoning chain).

**Three lines of defense:**

* **First line — Skin (Definition / Horoi):** Reject premises that do not pass operational anchoring. The agent does not start a chain of reasoning on top of an undefined term.
* **Second line — Antibodies (Adversarial Cross-Examination / Elenchus):** Detect contradictions with Fixed Parameters in real time. The agent does not allow inconsistent claims to live in the same reasoning chain.
* **Third line — T-cells (Faithfulness / Faithfulness Check):** Destroy cells (claims) that betray the host (the reasoning chain). The agent performs periodic audits regardless of whether the user has agreed.

**Why "autoimmunology":** If the immune system attacks the host itself, it causes an autoimmune disease. In Socratic dialogue, this happens when the agent begins to undermine its own verified conclusions. The anti-bias section in `SKILL.md` is the operationalization of the autoimmune checkpoint — the agent should attack external claims more aggressively than its own verified ones, but should also know when to stop attacking.

### 7.1 Closing the Loop

After each cycle (workflow steps 1–5), the agent must perform a meta-step:

1. **State of the session:** What is currently fixed, what is currently in question.
2. **Drift check:** Has the conversation drifted from the original goal in the last N turns? If yes, return to step 2 (Terminology Anchoring).
3. **Bias scan:** Did I generate any output that an independent reviewer would call sycophantic, biased, or hedging without grounds? If yes, perform an explicit retraction.
4. **Next-action declaration:** One sentence about what the agent will do next, and why.

## 8. Anti-patterns (what this skill is NOT)

This skill is not:
- **A brainstorming tool.** Maieutics surfaces what the user already knows; it does not generate new ideas. For brainstorming, use a different skill.
- **A decision-making tool.** The skill helps structure the *reasoning*; it does not make the call. The user decides.
- **A therapy substitute.** Socratic dialogue in a personal-development context can look therapeutic, but it is not. If the user is in emotional distress, ground them first. (This is also why the SKILL.md has "When NOT to use" entries — including contexts where the user is not in a state for cooperative inquiry.)
- **A debate tool.** Elenchus is not argumentum ad hominem, not rhetoric, not persuasion. If the user feels attacked, the agent has left Socratic mode.

---

## 9. Calibration: how rigid should the workflow be?

The workflow steps are a **default order**, not a law. Adapt them to the situation:

- **Skip step 1 (Reformulation)** if the user's question is already a clean, single-sentence Socratic prompt.
- **Skip step 5 (Faithfulness Check)** for trivial conclusions (e.g., "Paris is the capital of France" — faithfulness is obvious and the score is 1.0, no questions needed).
- **Run step 4 (Confidence Gating) twice** if the synthesis itself has sub-conclusions, each of which needs its own confidence declaration.

The skill is *operationally* rigid (you do not skip steps because you feel like it) and *structurally* flexible (you may reorder, fold, or skip steps when the situation warrants, as long as the overall discipline holds).

---

## 10. Sources and further reading

- Plato, *Euthyphro*, *Laches*, *Charmides*, *Theaetetus*, *Meno*, *Gorgias*, *Republic* — primary texts for the six techniques and the refutative/cooperative dimensions of elenchus.
- Gregory Vlastos, *The Socratic Elenchus* (Oxford Studies in Ancient Philosophy, 1983) and *Socratic Studies* (Cambridge, 1994) — the foundational reconstruction of elenchus as a coherence test for the interlocutor's whole intellectual life.
- W.K.C. Guthrie, *A History of Greek Philosophy, Vol. III: The Fifth-Century Enlightenment* (Cambridge, 1969), Part II — Socratic method in intellectual context.
- For LLM-specific calibration: the *Faithfulness* literature in RAG evaluation (e.g., Es et al. 2023, "Faithful or Extractive?") — directly applicable to the Faithfulness Score output format.

The skill treats the *form* of these methods (definition, cross-examination, midwifery, productive impasse) as portable. The specific Greek vocabulary is for the agent's internal grounding; user-facing output should be in plain language.
