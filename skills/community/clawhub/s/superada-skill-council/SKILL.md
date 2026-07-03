---
name: council
version: 0.1.0
description: Topic-aware multi-agent council for structured debate, challenge, and synthesis across engineering, sales, support, product, ops, and strategy topics.
metadata: {"emoji":"🏛️","category":"thinking","supports_topic_personas":true}
---

# Council

Topic-aware multi-agent debate for OpenClaw.

This is a retooled version of the fixed-persona Council pattern, adapted for our stack:
- built for **OpenClaw / Clawdbot agents**
- optimized for **`sessions_spawn`** and isolated sub-agents
- personas change based on the **topic/domain**
- usable by **any agent** that can read and follow a skill

## When to Use

Use this skill when the request needs:
- multiple specialist viewpoints
- deliberate tradeoff analysis
- stress-testing a plan before execution
- a visible debate instead of one-shot advice
- topic-specific councils like engineering, sales, support, product, GTM, risk

Good triggers:
- “council this”
- “give me multiple perspectives”
- “stress test this plan”
- “run an engineering council”
- “use sales personas on this”
- “debate this before we build/sell/ship it”

Do **not** use this for:
- trivial factual lookups
- simple edits
- low-stakes yes/no questions
- tasks where one specialist is clearly enough

## Core Idea

The value is not “five opinions.”
The value is **interaction**:
1. specialists take initial positions
2. specialists challenge each other’s assumptions
3. the council converges on a recommendation with clear tensions called out

Parallel within each round. Sequential across rounds.

## Council Modes

### 1) Quick Council
Use for fast sanity checks.
- 1 round
- 3 to 5 personas
- short outputs
- final recommendation

### 2) Full Council
Use for important decisions.
- 3 rounds
- 4 to 6 personas
- explicit cross-response in later rounds
- synthesis with convergence, disagreement, and next step

### 3) Custom Council
Use when the user specifies a domain or mix.
Examples:
- engineering council
- sales council
- support council
- product + engineering council
- security-heavy council

## Topic Routing

Before running the council, classify the topic.

Default routing:
- **Engineering** → architecture, implementation, infra, APIs, code quality, security engineering
- **Sales** → outbound, enterprise deals, discovery, objections, pricing, pipeline strategy
- **Support / Success** → ticket handling, escalation, SLA, retention, onboarding, support ops
- **Product** → roadmap, UX, requirements, prioritization, customer value, scope
- **Growth / Marketing** → positioning, campaigns, funnel, content, attribution, experiments
- **Ops / Leadership** → workflow design, hiring process, coordination, team structure, execution risk
- **General / Strategy** → use mixed council if no single domain dominates

If ambiguous:
- pick the dominant domain
- or run a mixed council with 1 persona from each relevant area

See `Personas.md` for topic packs.

## Standard Process

### Quick Council
1. Identify topic/domain
2. Select 3-5 personas from `Personas.md`
3. Ask each persona for a short position in parallel
4. Synthesize:
   - consensus
   - biggest concern
   - recommendation
   - whether a full council is needed

### Full Council
1. Identify topic/domain
2. Select 4-6 personas from `Personas.md`
3. Run **Round 1: Initial Positions** in parallel
4. Aggregate transcript
5. Run **Round 2: Responses & Challenges** in parallel
6. Aggregate transcript
7. Run **Round 3: Final Position / Convergence** in parallel
8. Produce synthesis using `OutputFormat.md`

## OpenClaw Execution Pattern

Preferred implementation pattern:
- use **`sessions_spawn`** to launch one isolated sub-agent per persona
- give each sub-agent only:
  - the user’s topic/problem
  - the persona brief
  - the round instructions
  - prior transcript where needed
- keep outputs concise and structured
- aggregate results in the parent agent
- use **light self-healing** for higher-stakes councils:
  - fallback model chain
  - checkpoint file
  - proof requirement

See `SelfHealing.md` for the resilience layer.

### Suggested sub-agent contract
For each persona spawn, give:
- persona name
- mission
- what to optimize for
- what to distrust
- output length target
- exact round objective

### Good operational defaults
- model: use default unless the task is very high stakes
- quick council: 3-5 personas
- full council: 4-6 personas
- avoid councils >6 personas unless the decision is unusually load-bearing

## Rules for Persona Selection

1. Pick personas that create **useful friction**, not redundant agreement.
2. Include at least one persona grounded in execution reality.
3. Include at least one persona grounded in user/customer reality when relevant.
4. Include risk/compliance/security when the topic touches sensitive systems.
5. Avoid “the same brain in five hats.” Each persona must optimize for a distinct concern.

## Rules for Good Debate

- Round 2 and later must reference **specific** points from other personas.
- Personas should challenge assumptions, not just restate preferences.
- The synthesis must preserve unresolved tensions.
- If the council lacks key information, say so directly.
- Recommendation should be actionable, not poetic.

## Output Requirements

Always end with:
- **Recommended path**
- **Key tradeoffs**
- **Open questions**
- **Next action**

See `OutputFormat.md`.

## Example Invocations

- “Run an engineering council on this API design.”
- “Quick council: should we ship this pricing page copy?”
- “Use a support council to redesign our escalation flow.”
- “Run a sales council on this outbound strategy for TPAs.”
- “Council this product spec before Scotty builds it.”

## Recommended Domain Packs

- Engineering: 5 personas
- Sales: 5 personas
- Support: 5 personas
- Product: 5 personas
- Growth: 5 personas
- Mixed strategy: 4-6 personas

See `Personas.md`.

## Notes

- This skill is deliberately **topic-aware**, unlike the original fixed Architect/Designer/Engineer/Researcher quartet.
- For pure attack-mode, use a red-team pattern instead.
- For single-model self-critique, `3pass` is cheaper. Council is for higher-stakes calls.

## Enhancements and Examples

This skill has been upgraded for better AI executor ergonomics and output quality:

- **Add-ons**: You can now apply constraints like "Budget Hawk" or "Devil's Advocate" from `Personas.md` to dynamically shift a persona's perspective.
- **Ergonomics**: See `ExecutorPrompt.md` for instructions on how to comfortably use `sessions_spawn` and pass add-ons to sub-agents.
- **Transcripts**: See `examples/engineering-council.md` for a model output of productive disagreement and synthesis.
- **Benchmarking**: Use `benchmarks/output-benchmarking.md` to self-evaluate the council output (target score > 70) before presenting it to the user.
