---
title: Use Case 2 — Research Collection (v2.0)
canvas_side: workflow_example
use_case: user_has_no_data
pattern: data_collection_plan_then_v2_pipeline
skill: value-proposition-canvas
version: 2.0
created: 2026-07-09
---

# Use Case 2: Research Collection — "No data yet, what should I gather?"

## Scenario

You are a product designer with a vague product idea. You have not done any user research yet. You have a feeling that there is a real problem to solve, but you do not know who has the problem, what they say about it, or what they have tried.

You come to the workshop with:
- A product idea (or a feeling that there might be one).
- No transcripts, no interviews, no quantitative data.
- The recognition that you should not build anything until you have talked to real users.

You want the agent to:
1. Help you decide **what to research** (which persona or segment, what questions, what methods).
2. Help you run the research or run it for you (depending on tooling).
3. After you have the data, run the **v2.0 pipeline** (Phase 1 → Phase 2 → Phase 2.5 → done).

The skill treats the **no-data-yet** case as a research-planning problem, not a VPC problem. The VPC starts once you have evidence.

---

## Step 1 — First clarifying question (HARD WAIT)

The agent asks:

> *"Are we designing for a specific persona (one user type, named like Pat) or for a whole segment (a category of users like 'indie designers building SaaS')?"*

The agent **does nothing** until the user answers.

You answer: **"Persona. Pat — an indie designer, 3 years experience, ships one product at a time, uses Figma and shadcn, talks to 2-3 engineers per release."**

The agent now has a **target persona**, but no data yet.

---

## Step 2 — Persona sharpening (HARD GATE before research)

The agent does not accept the persona as given. It applies the **persona quality check**:

> *"Pat is a plausible persona, but 'indie designer with 3 years experience' is a demographic, not a behavioral profile. Before we go collect data, let me make sure we are defining Pat the right way."*

The agent asks 3-5 sharpening questions:

1. *"What does Pat do in a typical day, in their own workflow?"*
2. *"What tool does Pat reach for first when they sit down to design?"*
3. *"What does Pat wish was different about their work, even if they have never said it out loud?"*
4. *"Who else does Pat talk to about their work (peers, communities, mentors)?"*
5. *"What is Pat not doing, that they would do if their life were easier?"*

You answer. The agent refines the persona:

> **Pat (refined)**: A product designer who ships one product at a time, alone or with 2-3 engineers. Uses Figma for design, shadcn for components, and Slack for everything else. Spends ~40% of their time in the design tool, ~30% explaining the design to engineers, ~20% in meetings about the design, and ~10% on everything else. The 30% "explaining" time is the suspected pain. The 20% "meetings" time is the suspected undiscovered pain. Pat has never written a design spec; the spec is implicit in the Figma file.

The agent now has a **persona with a behavioral profile**, not just demographics. This is the input to the research plan.

---

## Step 3 — The agent produces a research plan

The agent does **not** start the VPC. The agent outputs a research plan — a checklist the user can execute over the next 1-2 weeks. The plan has 5 components.

### 3.1 What to research (the questions you need to answer)

| # | Question | Why it matters for the VPC |
|---|---|---|
| Q1 | What is Pat's daily workflow, hour by hour? | You cannot write a Job without knowing the workflow. |
| Q2 | What does Pat do when the design hits an edge case (empty state, error, loading)? | Edge cases are the source of most Pains. |
| Q3 | What does Pat do *after* the design is "done"? | Handoff is where most Pains live. |
| Q4 | What has Pat tried that did not work? | Failed attempts are Pains with a paper trail. |
| Q5 | What would Pat pay for? (Or: what has Pat paid for, in adjacent tools?) | Pains with a payment trail are the dominant ones. |
| Q6 | Who else has this problem? | Tests whether the persona is a real segment or an edge case. |
| Q7 | What does Pat say when they describe their work to a non-designer? | Surfaces Jobs the persona would never name explicitly. |

### 3.2 What methods to use

| Method | When to use | What it gives you |
|---|---|---|
| **Semi-structured interviews (5-8)** | Always start here. | The raw material — Jobs, Pains, Gains in Pat's own words. |
| **Shadowing / observation (1-2 sessions)** | After 3-4 interviews, if you can. | The Pains the persona does not say out loud. |
| **Card sorting (5-8 participants)** | Once you have a candidate list of Pains. | The rank order of Pains. |
| **Survey (n ≥ 30)** | Once you have a hypothesis. | Validation, not discovery. |
| **Forum / community mining** | In parallel with interviews. | Unprompted Pains, the "venting" signal. |

**Minimum evidence base:** 5-8 interviews + 1-2 shadowing sessions + 30 minutes of forum mining. The agent does not let the user proceed to the VPC on less.

### 3.3 Who to recruit (recruiting spec for "Pat")

> **Recruiting spec for "Pat"**
>
> - Has shipped at least one product (any size) in the last 12 months.
> - Uses Figma as the primary design tool.
> - Works alone or with a small team (≤ 3 engineers).
> - Has handed off at least one design to engineering in the last 6 months.
> - Is willing to do a 30-minute video call in the next 2 weeks.
>
> **Out of scope for Pat**: design leads managing 5+ designers, designers who work exclusively in code, designers who have never handed off a design.
>
> **Recruiting channels**: Pat's Twitter / X followers, design Slack communities (e.g., Design Buddies, Figma Community), your own network, User Interviews / Respondent.io if you can pay.

### 3.4 The interview script (the 7 questions, expanded)

The agent outputs a **semi-structured interview script** for Pat. Each question is open-ended, behaviorally anchored, and Socratically tested (i.e., the agent has checked that the question does not lead the witness).

```text
1. Walk me through the last time you sat down to design a screen.
   (Listen for: tools, sequence, interruptions, switching costs.)

2. What's the most frustrating part of designing right now, even if it's small?
   (Listen for: small frustrations that point to big Pains. Probe "tell me more".)

3. Tell me about the last time you handed off a design to an engineer.
   - What did the handoff look like?
   - What went well? What went wrong?
   - How long did it take end-to-end (design done → implementation in production)?

4. When the implementation came back different from your design, what happened?
   - How did you find out?
   - What did you do?
   - How much rework was needed?

5. Have you ever written a design spec or handoff document?
   - If yes: what format? Who read it? What was the result?
   - If no: why not? What do you do instead?

6. Have you ever used an AI coding tool (Cursor, Copilot, v0, etc.) on your designs?
   - If yes: what worked? What didn't?
   - If no: why not?

7. If you could wave a magic wand and change one thing about how you hand off designs,
   what would it be?
   (Listen for: the dominant Gain. Probe "what would that change for you?")

8. Who else do you know who has this problem?
   (Tests whether the segment is real.)
```

### 3.5 What to listen for (the signal taxonomy, mapped to v2.0 Customer Profile fields)

The agent provides a **listening guide** — what to listen for, organized by v2.0 Customer Profile fields (Jobs, Pains, Gains). This is what the user captures in the interview and what the agent will extract from later.

| VPC field | What to listen for | Verbatim signals |
|---|---|---|
| **Job (functional)** | What the persona is trying to accomplish. | "I need to...", "My job is to...", "I'm trying to..." |
| **Job (social)** | How the persona wants to be perceived. | "I want my team to see me as...", "I want to be known for..." |
| **Job (emotional)** | How the persona wants to feel. | "I want to feel...", "I hate feeling like..." |
| **Pain (operational)** | Frustrations, time waste, broken workflows. | "I waste X hours on...", "Every time I do X, I have to..." |
| **Pain (strategic)** | Fears, risks, missed opportunities. | "I'm worried that...", "What if..." |
| **Pain (social)** | Embarrassment, status loss. | "It's embarrassing when...", "I don't want my team to think I..." |
| **Gain (functional)** | Capabilities the persona wishes they had. | "I wish I could...", "It would be great if..." |
| **Gain (emotional)** | Feelings the persona wishes they felt. | "I want to feel in control of...", "I want to sleep at night knowing..." |
| **Gain (social)** | Status the persona wishes they had. | "I want to be seen as...", "I want my work to be recognized as..." |

**Number targets** (what the agent will aim for in Phase 1):
- 1-2 main Jobs + 3-5 supporting Jobs.
- 3-5 Pains.
- 3-5 Gains.

If the transcripts yield more, the agent will cluster and prune with the user. If they yield fewer, the agent will probe with follow-up interviews.

### 3.6 What to capture (the capture template)

The agent provides a **capture template** for each interview. The user fills it in during or right after the interview, before memory fades.

```markdown
## Interview #[N] — [Date]
### Persona: [Pat-equivalent or other]
### Time: [30 min target]
### Channel: [Zoom / in-person / async]

### Verbatim quotes (paraphrased is OK, but flag paraphrases):
- Q1: "[quote]" — context
- Q2: "[quote]" — context
- Q3: "[quote]" — context
...

### My observations (the things they said between the lines):
- [observation 1]
- [observation 2]

### Artifacts the persona showed me (screenshots, Figma files, Slack threads):
- [attachment or link]

### My read on the dominant Job / Pain / Gain from this interview:
- Dominant Job: [one sentence]
- Dominant Pain: [one sentence]
- Dominant Gain: [one sentence]

### Open questions for the next interview:
- [question 1]
- [question 2]
```

---

## Step 4 — You go do the research

You spend 1-2 weeks executing the plan. You talk to 5-8 Pats. You capture 5-8 capture templates. You have 5-8 transcripts in your project folder.

The skill has nothing to do during this period. The skill is not an interviewing tool; it is a structuring tool. Use a different tool (a notebook, a recorder, Otter.ai, your own memory) to collect the data.

---

## Step 5 — You come back with the data

You give the agent the 5-8 capture templates + transcripts (or links to them). The agent then runs the **v2.0 pipeline** (see `examples/research-ingestion.md` for the full worked example):

1. **Persona/segment question** — already answered (Pat). Continue.
2. **Phase 1 (Customer Profile)** — extract Jobs (1-2 main + 3-5 supporting), Pains (3-5), Gains (3-5). Sort by frequency/importance. Verbatim source quotes. User accepts each table.
3. **Phase 1 gate** — user explicitly accepts the Customer Profile Lock.
4. **Phase 2.1 (Pain Relievers)** — agent proposes one PR per locked Pain. 1:1 mapping, no orphans. User accepts.
5. **Phase 2.1 gate** — user accepts the Pain Relievers table.
6. **Phase 2.3 (Gain Creators)** — agent proposes one GC per locked Gain. 1:1 mapping, multi-tag allowed. User accepts.
7. **Phase 2.3 gate** — user accepts the Gain Creators table.
8. **Phase 2.5 (Products & Services)** — agent proposes 1-3 bundle items (the offering shape, not features). User accepts.
9. **Phase 2.5 gate** — user accepts the Products & Services table.
10. **Phase 2.7 (Framework Selection)** — agent asks which framework the user wants for prioritization. Proposes **Kano Model Strategist** as the default and explains how it works. User confirms.
11. **Phase 2.7 gate** — user confirms the framework. The skill ends.

The pipeline is identical to Use Case 1 from Step 3 onward. The only difference is the input — in Use Case 1 you brought the data; in Use Case 2 you built the data-collection infrastructure first and then brought the data.

---

## What the agent did NOT do (and why this matters)

- **The agent did not generate the persona from scratch.** The persona is a name the user gave. The agent's job is to sharpen the persona, not invent it.
- **The agent did not skip the research.** The skill is honest that you cannot write a VPC without evidence. The agent's first response to "I have an idea but no data" is "let's plan the research," not "let's hallucinate a VPC."
- **The agent did not promise that the research would be fast.** 5-8 interviews + shadowing + forum mining is 1-2 weeks of work. The skill is explicit about the cost. There is no "30-minute VPC."
- **The agent did not provide a "synthetic" persona as a substitute for real research.** Some tools offer to generate a fake persona to feed the canvas. The agent refuses. A fake persona is a hallucination with a name.

---

## Lessons for the agent

1. **The first clarifying question is the same in both use cases.** Persona or segment? Always ask. The answer changes everything downstream.
2. **A persona is a behavioral profile, not a demographic.** The agent pushes back on "indie designer, 3 years exp" until the persona has a workflow, a tool stack, and a suspected pain.
3. **The research plan is a deliverable, not a step.** The user should be able to execute the plan without further agent input. The skill produces a checklist, not a chat.
4. **The interview script is Socratically tested.** Each question has been checked for leading-the-witness. The user can use it as-is.
5. **The capture template is a forcing function.** Without a template, the user will forget half the interview by the time they get back to the canvas. The template makes the data ingestion possible.
6. **The number targets in the listening guide match the v2.0 number rules.** The user is told upfront: aim for 1-2 main Jobs, 3-5 Pains, 3-5 Gains. The agent will cluster and prune if the transcripts yield more.
7. **The pipeline converges.** Both use cases end at the same artifact: a fully-mapped VPC table with a selected prioritization framework. The only difference is the input.
8. **The agent explains concepts to the user.** When the research plan is delivered, the agent explains why each method is recommended, what to listen for, and how the captured data maps to the v2.0 Customer Profile fields. The skill is educational, not just procedural.

---

## References

- Osterwalder, A., Pigneur, Y., Smith, A. (2014). *Value Proposition Design.* Wiley.
- Interaction Design Foundation (2024). *The Value Proposition Canvas.* — Pain and Gain category taxonomies, two rules for gains.
- Blank, S. (2013). *The Four Steps to the Epiphany.* — Customer Development, GOOB.
- Patton, J. (2014). *User Story Mapping.* O'Reilly. — Behavioral persona framing.
- `research-ingestion.md` in this folder — The v2.0 pipeline that Use Case 2 feeds into.
- `kano-model-strategist` skill in this playbook — The next step after the v2.0 skill finishes.
