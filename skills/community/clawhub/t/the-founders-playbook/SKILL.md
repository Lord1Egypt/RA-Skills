---
name: The Founder's Playbook
slug: the-founders-playbook
description: Convert Anthropic's AI-native startup playbook into reusable agent skills — validate, build, launch, and scale your startup with AI across 4 stages. No platform lock-in, any agent can use it.
license: MIT-0
compatibility: Works with any AI agent, any coding assistant. No platform-specific dependencies.
metadata:
  author: casvian
  version: "1.0.0"
  repository: https://github.com/casvian/the-founders-playbook
---

# The Founder's Playbook 📖

> Based on "The Founder's Playbook: Building an AI-Native Startup" — adapted for any AI agent, any platform.

This skill converts the AI-native startup lifecycle framework into reusable, stage-aware workflows. It covers all four stages of building an AI-native company: **Idea → MVP → Launch → Scale**.

Each stage has:
- **Goals & exit criteria** — know when you're done
- **Challenges** — traps the framework flags before you fall in
- **Exercises** — concrete things to do with your AI agent
- **Trigger conditions** — detected from what you say

No Claude-specific references. Designed for any AI agent, any coding assistant, any platform.

---

## Stage Detection

The skill activates based on what you say. Stage transitions are detected from context:

| Trigger Phrases | Stage Activated |
|----------------|-----------------|
| "I have an idea", "validate this", "market research", "is this worth building" | **Idea** |
| "build the MVP", "start prototyping", "write the code", "create the first version" | **MVP** |
| "launch", "go to market", "get first customers", "fundraising", "investors" | **Launch** |
| "scale", "enterprise", "growing fast", "hire", "expand", "institutional" | **Scale** |

When uncertain, the agent should ask: *"What stage is your startup at? Idea (validating), MVP (building), Launch (first customers), or Scale (growing)?"*

---

## Stage 1: Idea Stage

### Goal
Research-oriented validation: assemble solid evidence that a real problem exists and your proposed solution effectively addresses it — before committing resources to building.

### Key Questions (in order)
1. **Is this problem real, specific, and frequent enough to build around?**
2. **Who exactly has it, and is that a market?**
3. **Is anyone else solving it, and how well?**
4. **What would a solution actually need to do — and does my idea do that?**
5. **Is this worth building?**

**Testable hypothesis format:** ❌ "People struggle with expense reporting" → ✅ "Finance managers at mid-market companies spend 4+ hours a week reconciling submissions because their current tools don't integrate with their accounting software."

### Exit Criteria
You're ready to leave the Idea stage when you can answer **yes** to all three:
1. **Is the problem real and specific?** — You can name exactly who experiences it, how often, how severely, and what they currently do about it.
2. **Does your solution address the actual problem?** — Not the problem you assumed, but the one validation revealed.
3. **Do you have enough signal to justify building?** — Enough qualitative evidence that committing to an MVP is a reasoned decision, not an act of faith.

### Challenges to Watch For

**❌ Mistaking building for validating**
When technical blockers are lifted, you risk skipping validation entirely. A working prototype is NOT evidence — it's a prop for conversations with potential users. The conversations are the evidence.

**❌ Premature scaling**
Agentic coding can scale execution far ahead of problem-solution fit. The AI will generate, test, debug, and refactor a codebase around a fundamentally flawed premise with exactly the same enthusiasm as a great one. **Keep your sense-making ahead of your building.**

**❌ Loss of objectivity**
Ask any AI for evidence supporting what you already believe, and it will find it. Confirmation bias now comes with a research engine. The antidote: use the same tools to make the adversarial case against your own idea.

### Exercises

**Exercise 1: Problem pressure test**
```
Feed your AI agent your raw idea and ask for an adversarial analysis:
- "What would have to be true for this idea to fail?"
- "Who would disagree with my assumptions and why?"
- "What's the weakest link in this reasoning?"
```

**Exercise 2: Competitive landscape**
```
Ask your AI agent to map four layers:
1. Direct competitors (same problem, same solution type)
2. Indirect competitors (same problem, different approach)
3. Potential acquirers (who would buy a solution in this space?)
4. Adjacent players (could enter your space)

For each: what proprietary advantage do you have?
```

**Exercise 3: Customer discovery interview brief**
```
Ask your AI agent to design a customer discovery interview protocol:
- Who to interview (segment criteria, minimum 10-15)
- What questions to ask (open-ended, avoid leading)
- How to analyze responses (themes, signal vs noise)
- What disconfirming evidence looks like
```

**Exercise 4: TAM/SAM/SOM with adversarial review**
```
Ask your AI agent to build a TAM/SAM/SOM model, then immediately
ask it to tear it apart: "Now make the case that these numbers
are too optimistic. What assumptions am I hiding?"
```

---

## Stage 2: MVP Stage

### Goal
Turn your validated idea into a real product that real users interact with. Build only what's necessary to test product-market fit, and build it with the architectural hygiene that keeps AI-generated code maintainable.

### Exit Criteria
The MVP stage ends when you have **genuine evidence of product-market fit**, not when the product feels "finished." Key litmus tests:
- **Sean Ellis test:** >40% of active users say they'd be "very disappointed" without your product
- **Retention signals:** Users return without you pushing them
- **Effort shift:** The product starts pulling users in, instead of you pushing them out

### Challenges to Watch For

**❌ AI technical debt (compounds like interest)**
Agentic coding tools generate functional code, not architecturally coherent code. Without specs and constraints written down where the AI can read them, each session re-derives foundational decisions from scratch — and those decisions drift. Unlike traditional tech debt (linear, manageable), **AI tech debt compounds exponentially.** The codebase becomes functional but structurally incoherent, and eventually collapses.

**❌ Falling for false product-market fit**
Early traction is not PMF. Launch energy comes from ephemeral forces — friends, investor intros, a Hacker News spike. None of these predict week six or week twelve. **Set your retention benchmarks before the first user arrives.**

**❌ Zero-friction scope creep**
Adding a feature takes an afternoon instead of a sprint, so every addition feels defensible. The antidote: a written scope definition created **before building begins** that specifies what evidence from real users would justify adding something new.

**❌ Insecure by inexperience**
Agentic coding tools generate code that *works*, not code that's *secure*. Vulnerabilities are invisible until exploited. Ships a security review before any user touches your product.

### Exercises

**Exercise 1: Define your architecture before you build**
```
Before a single line of production code, have your AI agent help you define:
- Core architectural principles (patterns to follow, dependencies to avoid)
- Tradeoffs you're consciously accepting at this stage
- Scale expectations for the next 6 months

Save this as a context file (e.g., AGENTS.md, project SKILL.md, or equivalent).
This is your architectural context document. Every build session starts here.
```

**Exercise 2: Scope definition document**
```
Create a written scope document before building:
- What the MVP does (specific, measurable)
- What it deliberately does NOT do (equally important)
- Feature amendment criteria: what evidence justifies adding something?

When new feature ideas surface, pressure-test them:
"Is this genuine user signal or founder enthusiasm?"
```

**Exercise 3: Session hygiene**
```
For every build session with your coding agent:
1. START: Share scope document + architectural context file
2. DURING: Keep the task specific (one feature, one fix)
3. END: Write a brief log — what was built, what decisions were made,
   what assumptions were introduced (5 min saves hours of drift)
```

**Exercise 4: Pre-launch security review**
```
Before deploying to real users, have your AI agent audit:
- Authentication and session handling
- Data exposure in API responses
- Input validation and injection risks
- Dependencies with known vulnerabilities
Treat findings seriously. Get human review for anything touching
auth, secrets, or data handling.
```

**Exercise 5: Measurement framework**
```
Define before launch:
- Which metrics matter (retention, activation, Day 7/30 targets)
- What constitutes product-market fit (specific benchmarks)
- What a FALSE POSITIVE looks like (signups without activation,
  revenue without retention, enthusiasm without repeat usage)

Then ask your AI to make the adversarial case against your own data.
```

### Pivot Decision Framework
If 3+ iteration cycles show no meaningful movement toward PMF:
```
Feed your AI agent: retention data + user feedback + original problem hypothesis
Ask three questions:
1. Is there a segment responding differently than the rest?
2. Is the gap a positioning problem or a product problem?
3. What would have to be true for the current product to find PMF?

Let the answers determine: adjust, pivot, or return to Idea stage.
```

---

## Stage 3: Launch Stage

### Goal
Turn early traction into a repeatable, sustainable growth engine. Make the product production-ready, harden the infrastructure underneath it, and build an actual company around it.

### Exit Criteria
1. **Revenue is real and growing** — not just MRR, but gross retention >80% and net retention >100%
2. **Acquisition is repeatable** — you know your CAC by channel and can spend to acquire predictably
3. **Operations run without founder bottlenecks** — processes exist, automation is in place. You are no longer personally handling support, triage, sprint planning, or reporting.

### Challenges to Watch For

**❌ The founder bottleneck**
When a single-person company succeeds, the founder becomes the critical path for everything. The system that got you here won't get you there. You need to systematize yourself out of the loop.

**❌ Treating security as optional**
At launch, you have real users with real data. A breach isn't just a technical problem — it's an existential one. Security is now a business requirement, not an engineering preference.

**❌ Premature optimization**
Some things only become problems at scale — and some never do. The Launch stage challenge is knowing the difference. Use data to decide what to fix now vs. what to monitor.

### Exercises

**Exercise 1: Founder bottleneck audit**
```
Map every workflow, decision, and approval currently routed through you.
Then ask: "What happens to each one if I'm unavailable for a week?"

The workflows that stall are where you're still hands-on enough to derail progress.
For each: delegate, automate, or document handoff criteria.
```

**Exercise 2: Technical debt sprint planning**
```
Ask your AI agent to audit the codebase and categorize debt:
What's blocking new features? → Fix this sprint
What's annoying but not blocking? → Schedule for later
What's cosmetic? → Never fix

Then: run a focused debt sprint. Each improvement must unblock
a specific product or business capability.
```

**Exercise 3: Compliance and security baseline**
```
Ask your AI agent to map:
- What data do you store? (PII, financial, health, etc.)
- What regulations apply? (SOC2, GDPR, HIPAA, CCPA, etc.)
- What documentation would an enterprise buyer request?
- What audit trail exists?

Build compliance into your workflow now — retrofitting is 10x harder.
```

**Exercise 4: GTM engine**
```
Ask your AI agent to build:
1. Market segmentation (who, where, why now)
2. Messaging architecture (value prop per segment)
3. Sales playbook (objection handling, demo script, pricing FAQ)
4. Content pipeline (what to publish, where, at what cadence)
5. Outbound sequence (who to contact, how, when to follow up)

Run the GTM motion with your AI agent driving the operational layer:
CRM hygiene, pipeline reporting, content publishing, and outreach sequencing.
```

**Exercise 5: Fundraising (if applicable)**
```
Ask your AI agent to prepare:
- Investor memo (problem, solution, traction, team, ask)
- Financial model (revenue projections, burn, unit economics)
- Competitive positioning (why now, why you, why not them)
- Data room checklist (cap table, IP, contracts, compliance)

Your agent can't pitch for you, but it can prepare everything
so you walk in knowing your numbers cold.
```

---

## Stage 4: Scale Stage

### Goal
Turn a working product into a durable company. Enterprise customers, institutional processes, organizational infrastructure — all without losing the speed that got you here.

### Exit Criteria
- Enterprise contracts are closing predictably
- You can step away for a week without the company stalling
- Data network effects and workflow lock-in are creating defensible moats
- Operational systems run on automation, not founder heroics

### Challenges to Watch For

**❌ Founder bottleneck at scale**
What worked at 10 users doesn't work at 1000. At this stage, you're no longer the person who should be in every loop. The goal is to make yourself replaceable in operations so you can focus on the decisions only you can make.

**❌ Losing the speed advantage**
Process is necessary at scale, but it's also the enemy of speed. The challenge is building institutional infrastructure without institutional bureaucracy.

**❌ Underestimating enterprise sales cycles**
Enterprise buyers evaluate differently — procurement, security reviews, legal, compliance. A Loom video and a sales deck don't cut it. You need demo environments, integration docs, SLAs, and security posture documentation.

### Exercises

**Exercise 1: Bottleneck map (scaled)**
```
Ask your AI agent to produce a map of current operational workflows.
For each: what happens when you're gone for a week?
The workflows that stall reveal where you're still the single point of failure.
Delegate, automate, or document escalation paths.
```

**Exercise 2: Enterprise infrastructure audit**
```
For your top 3 dream enterprise customers, ask your AI agent to produce
a gap analysis: what documentation, SLAs, and support infrastructure
would their procurement team expect before signing?

Common requirements:
- Security review documentation (SOC2, penetration tests)
- Uptime SLA (99.9%+)
- Incident response runbook
- Data retention/deletion policy
- Integration documentation
- Multi-tenant isolation architecture
Build what's missing.
```

**Exercise 3: Data moat analysis**
```
Feed your AI agent your interaction data and ask:
1. What behavioral patterns are in the data?
2. What feedback loop turns usage into systematic improvement?
3. Draft a moat narrative: how your data flywheel works,
   how long it's been spinning, and why a well-resourced
   competitor couldn't replicate it in under 2 years.
```

**Exercise 4: Workflow integration audit**
```
For your top 10 customers:
- What automations have they built on top of your product?
- What integrations do they depend on?
- What's their estimated switching cost?

Patterns to look for: what type of integration creates
the deepest lock-in for YOUR specific product?
```

**Exercise 5: Domain knowledge → AI context**
```
Convert your domain expertise into structured context:
1. Industry jargon and terminology
2. Regulatory edge cases and gotchas
3. Workflow patterns (e.g., "how to audit a commercial lease")
4. Competitive intelligence (why obvious solutions don't work)

Save as reusable context files or skills. Over months, this becomes
a proprietary knowledge substrate no generalist AI can match.
```

---

## Stage Transition Rules

When you reach a stage's exit criteria, the agent should recommend transitioning:

| From | To | Trigger |
|------|----|---------|
| Idea | MVP | "You've validated the problem, found real users who need this, and have enough signal. Ready to build?" |
| MVP | Launch | "You have genuine PMF signals — retention, user pull, the effort shift. Ready to build a company around this?" |
| Launch | Scale | "Revenue is predictable, acquisition is repeatable, operations don't need you daily. Ready to scale?" |
| Any | Earlier | "The data says pivot. Let's go back to validation with what we now know." |

---

## Companion Resources

This skill pairs well with:
- **`startup`** — stage-aware execution orchestration (spawn specialist agents per function)
- **`cofounder`** — balance your blind spots with adaptive counterweight across technical, strategic, and behavioral dimensions
- **`business`** — general business strategy and planning

---

## License: MIT-0 (Free to use, modify, and redistribute. No attribution required.)

Based on "The Founder's Playbook: Building an AI-Native Startup" — adapted for general agent use.
