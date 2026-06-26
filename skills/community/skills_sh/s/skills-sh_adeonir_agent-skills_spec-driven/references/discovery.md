# Feature Discovery

Understand the feature before drafting the spec. Loaded by specify.md Step 7.

## When to Use

After scope assessment and project context check, before drafting spec.md.
Discovery is adaptive -- deepen based on the quality of answers, not a fixed
script. If input came from a file (@file.md), use extracted content as starting
context and skip questions already answered by the document.

## Discovery Topics

### Topic 1: Problem & Context

**Opening questions:**
- What problem does this feature solve?
- Who is affected and what's their current pain?
- How do you know this is a real problem? (evidence, feedback, observation)

**Deepen when:**
- User describes a solution, not a problem → "What problem does this solve? Let's start there."
- No evidence → "What would convince you this is real? Have you seen users struggle with this?"
- Multiple problems mixed → "These sound like separate issues. Which one is primary?"
- Vague audience → "Who specifically? Describe the person who hits this problem most."

**Sufficient when:**
- Problem can be stated in one clear sentence
- At least one concrete user/persona is identified
- Evidence exists or is explicitly marked as hypothesis

### Topic 2: Scope & Success

**Opening questions:**
- What needs to work first for this feature to be useful? (P1 core)
- What is explicitly out of scope?
- How will you know this feature succeeded? (measurable outcome)

**Deepen when:**
- No clear core → "What needs to work first for this feature to be useful?"
- Scope keeps expanding → "We started with X, now it's X+Y+Z. Should we narrow down?"
- No success criteria → "How would you demo this working? What does the user see?"
- User stories without user connection → "Which user needs this? What problem does it solve for them?"
- No priority order → "If you implement these one at a time, what order makes sense?"

**Sufficient when:**
- User stories are prioritized by implementation order (P1 core, P2 increment, P3 polish)
- P1 user stories form a working feature on their own
- At least one measurable success criterion exists
- Boundaries are defined (what is explicitly out of scope)

## Discovery Flow

1. Start each topic with its opening questions (2-3 per topic)
2. Evaluate answers against sufficiency criteria
3. If criteria not met, deepen -- ask follow-ups targeting the specific gap
4. If criteria met, summarize understanding and move to next topic
5. After both topics, present synthesis for user confirmation -- separate what the
   user **stated** from what was **assumed or inferred**; the assumed items go to the
   `## Assumptions` ledger

## Adaptive Deepening

Probe further when answers are:

- **Vague**: "users want something better" → ask for specifics
- **Assumed**: stated as fact without evidence → ask for evidence, or record in the Assumptions ledger as `user-hypothesis`
- **Conflated**: multiple concepts mixed → separate and explore each
- **Solution-first**: describes what to build before why → redirect to the problem
- **Overly broad**: "everyone", "all cases" → narrow to most important

Move on when:

- The topic's sufficiency criteria are met
- The user explicitly says "I don't know" (mark as TBD)
- Further questioning would not yield new information

## Question Principles

- Open-ended first, specific later
- Never suggest answers in the question (avoid leading questions)
- Build follow-ups on what the user actually said, not on a script
- Be specific: "Should password reset require email verification?" not "How should reset work?"
- Offer options when possible: "Should the timeout be (a) 30 minutes, (b) 1 hour, or (c) configurable?"

## Critical Posture

Discovery is not a formality. Challenge ideas with respect, but never be a yes-man.

| Situation | Passive Response | Critical Response |
|-----------|-----------------|-------------------|
| User describes vague problem | "Okay, let's proceed" | "Who specifically has this problem? How often?" |
| User jumps to solution | "Got it, I'll include that" | "Before we define the solution -- what problem does this solve?" |
| User adds scope mid-discovery | "I'll add that too" | "This changes the scope. Should we focus on the core first?" |
| User has no evidence | "Noted" | "Without evidence, this is an assumption -- I'll record it in the Assumptions ledger as `user-hypothesis`." |

## Recording Assumptions

Discovery surfaces premises the build will rest on. Both kinds go to the
`## Assumptions` ledger in spec.md, never silently into the spec body:

- `user-hypothesis` -- the user asserted it as fact without evidence (the "mark as
  hypothesis" above, now durable).
- `agent-assumed` -- a gap the human did not answer that you filled to proceed.

**Anti-fabrication:** never write an `agent-assumed` premise as a stated fact in the
problem, scope, or success synthesis -- record it as an assumption with how it gets
confirmed. A load-bearing assumption you cannot confirm without the user is also an
Open Question, not a quiet guess.

## Gray Area Detection

During discovery, watch for signals that indicate ambiguous areas needing deeper discussion:

- Contradictory requirements
- "It depends" answers without clear conditions
- Requirements that could be interpreted multiple ways
- Missing domain knowledge
- Trade-offs without clear preference
- Implementation forks the build would otherwise default — theme/skin, locale/routing, brand strings, runtime target

If detected and scope is **Complex**: note them as Open Questions (each tagged
`[blocking]` or `[deferrable]`) and suggest running [discuss.md](discuss.md) after spec
is created.

Implementation forks must be pinned into spec.md (`## Decisions` or `## Session
Context`) or explicitly marked TBD before drafting — never left to be defaulted
during design or implement.

## Quality Gate

Before proceeding to drafting, verify:

- [ ] Both topics met sufficiency criteria or gaps are marked as TBD
- [ ] Unknowns explicitly marked as TBD
- [ ] User confirmed the synthesis
- [ ] No critical ambiguity remains
- [ ] Problem is understood with evidence or recorded in the Assumptions ledger
- [ ] Each Open Question tagged `[blocking]` or `[deferrable]`
- [ ] `discovery:` provenance set — `human` if a person answered, `autonomous-assumed` if it ran without human answers (the ledger then carries `agent-assumed` rows)

Items unresolved after discovery go to "Open Questions" in spec.md, each tagged
`[blocking]` or `[deferrable]`. Spec creation is never blocked, but a `[blocking]`
question surfaces at approval and halts the phase it bears on.
