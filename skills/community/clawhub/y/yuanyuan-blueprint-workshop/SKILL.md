---
name: yuanyuan-blueprint-workshop
description: Turn a person's tacit know-how into a testable Agent Blueprint through a structured 5-step workshop: scenario discovery, SOP extraction, dependency mapping, blueprint generation, and skill sourcing. Use when helping someone discover whether they have a reusable method and transform it into a buildable lobster-agent blueprint.
---

# Yuanyuan Blueprint Workshop

## Purpose

This skill packages the full **Yuanyuan** workflow into one reusable workshop.

Its job is not to magically generate a finished product from one vague sentence.
Its job is to help a user:
1. discover a real scenario worth turning into an agent,
2. extract their implicit know-how,
3. map the required knowledge and tools,
4. produce a real Agent Blueprint,
5. plan how the missing skills should be sourced.

---

## Use this skill when

Use it when the user says things like:
- “I think I have some experience, but I don't know if it can become an agent.”
- “Help me turn my know-how into a lobster agent.”
- “I want to productize my method.”
- “Help me figure out whether this workflow is structured enough.”
- “Take me from idea → blueprint → skill gap plan.”

---

## Do NOT use this skill when

- The user only wants a small factual answer.
- The user already has a finished blueprint and only needs implementation.
- The user asks for direct coding or deployment without discovery.
- The task is only to install/publish one isolated skill.

---

## Core promise

This workshop should produce two feelings for the user:
1. **“The AI actually understands what I'm good at.”**
2. **“Aha — I really do have a reusable method.”**

If the interaction feels like a cold questionnaire or generic encouragement, the skill is failing.

---

## Hard rules

1. Do **not** jump straight into full product generation before structure is clear.
2. Do **not** confuse domain knowledge with decision logic.
3. Do **not** overpromise that every idea deserves to become an agent.
4. Do **not** replace user delivery with a file path.
   - Save files internally if useful.
   - But when delivering a blueprint or structured result, send the **full content directly in the chat**.
5. Do **not** install many skills blindly.
   - First reuse local capabilities.
   - Then search ClawHub.
   - Then vet/scan.
   - Only then install or write new skills.

---

## The 5-step workshop

### Step 1 — Scenario Discovery
Goal: narrow a vague direction into one concrete, testable scenario.

Questions to drive:
- What are you consistently better at than most people?
- What do people repeatedly come to you for?
- If we only productize one scenario first, which one should it be?

Judging standard:
- Input can be defined
- Judgment can be structured
- Output can be verified

Output:
- scenario definition
- target user
- core task
- initial verdict: suitable / not yet suitable

### Step 2 — SOP Extraction
Goal: extract the actual method, not just abstract knowledge.

Methods:
- Ask “When someone comes to you for this, how do you usually handle it?”
- Continuously restate structure back to the user
- Push on judgment criteria, branches, exceptions, and mistakes

Output:
- step list
- judgment points
- branch logic
- common pitfalls
- unclear gaps that still need follow-up

### Step 3 — Knowledge & Tools Mapping
Goal: identify what this future agent needs in order to really work.

Distinguish:
- public knowledge layer
- skill-private references
- real tools / APIs / automation dependencies

Output:
- knowledge sources
- tool dependencies
- priority of dependencies
- minimal viable dependency set

### Step 4 — Agent Blueprint Generation
Goal: turn the findings into a buildable blueprint.

The blueprint should at minimum include:
1. scenario definition
2. target user
3. core task
4. SOP flow
5. judgment rules
6. knowledge requirements
7. skill/tool requirements
8. risks and boundaries
9. test suggestions
10. next build steps

Delivery rule:
- Give the user the **full blueprint directly in chat**.
- Saving a file is optional internal archiving, not the deliverable itself.

### Step 5 — Skill Sourcing Plan
Goal: connect the blueprint to the platform layer.

Use this order:
```text
reuse local
→ search ClawHub
→ vet/scan
→ install if suitable
→ otherwise write the missing skill
```

Output:
- capability gaps
- locally reusable skills
- ClawHub search targets
- likely self-built skills
- fill order

---

## Recommended final deliverables

By the end of this workshop, aim to produce:
1. a **Scenario Definition**,
2. a **Structured SOP**,
3. a **Dependency Map**,
4. a **Full Agent Blueprint**,
5. a **Skill Sourcing Plan**.

---

## Success criteria

The workshop is working if the user says things like:
- “Yes, that's exactly my real value.”
- “I didn't realize my process was this clear.”
- “Now I can actually imagine this becoming an agent.”

The workshop is failing if it turns into:
- generic praise,
- shallow summarization,
- premature system design,
- or path-only delivery.

---

## References

Use the files under `references/` and `templates/` for deeper context and output scaffolds.
