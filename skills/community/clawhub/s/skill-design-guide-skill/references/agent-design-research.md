# How to Build a Good Skill / Agent: Industry Design Principles Research

> Research date: 2026-04-14
> Sources: Anthropic / OpenAI / Google / LangChain official docs and engineering blogs

---

## Research Scope

| Source | Document | Published | Core Perspective |
|--------|----------|-----------|-----------------|
| **Anthropic** | "Building Effective Agents" | 2024.12 | Workflow pattern taxonomy + when to use Agents |
| **Anthropic** | "The Complete Guide to Building Skills for Claude" (33pp) | 2026.02 | Skill structure spec + progressive disclosure |
| **Anthropic** | "Scaling Managed Agents: Decoupling Brain from Hands" | 2026.04 | Production-grade Agent architecture + interface design |
| **OpenAI** | "A Practical Guide to Building Agents" | 2025.04 | Tool design + guardrails + evaluation |
| **LangChain** | "State of Agent Engineering 2025" + Agent Engineering blog | 2025.12 | Quality vs latency + observability + multi-model routing |

---

## 1. The Single Most Important Principle

> **Start simple. Add complexity only when simpler solutions fall short.**
> — Anthropic + OpenAI + LangChain consensus

Anthropic: "The most successful implementations aren't using complex frameworks or specialized libraries — they use **simple, composable patterns**."

OpenAI: "Start simple, add complexity gradually. Define clear responsibility boundaries for agents."

---

## 2. Workflow vs Agent: Know Which One You Need

Anthropic draws a clear distinction:

| Type | Definition | When to use |
|------|-----------|-------------|
| **Workflow** | Orchestrated via predefined code paths | Task steps are clear, predictable |
| **Agent** | LLM dynamically plans flow and tool use | Flexibility needed, can't predefine the path |

**Decision criterion**: If steps are predetermined (e.g., "read knowledge base → write article from template → save to directory"), it's a workflow — no need for Agent's dynamic planning.

---

## 3. Anthropic's Five Workflow Patterns

### 1. Prompt Chaining
Task decomposed into sequential steps, each processing previous output, with programmatic checkpoints.
- Best for: fixed subtask decomposition
- Example: generate outline → check compliance → write body from outline

### 2. Routing
Classify input, route to specialized processing flows.
- Best for: tasks with clear input categories needing different handling
- Example: article type → corresponding template and rules

### 3. Parallelization
Multiple independent subtasks run simultaneously, results merged.
- Best for: independent subtasks that benefit from parallel speedup
- Example: core article → simultaneously generate blog, social, newsletter versions

### 4. Orchestrator-Workers
Central LLM dynamically decomposes tasks, delegates to workers.
- Best for: complex tasks where subtasks can't be predefined

### 5. Evaluator-Optimizer
One LLM generates, another evaluates with feedback, iterating until pass.
- Best for: clear evaluation criteria, iteration yields measurable improvement
- Example: draft → review Agent checks facts/compliance → feedback → revision

---

## 4. Skill Structure Design (Anthropic Official Spec)

### Four Components

| Component | Purpose | Required |
|-----------|---------|----------|
| **SKILL.md** | Core definition: triggers, workflow, rule constraints | Yes |
| **scripts/** | Executable scripts (Python/JS, etc.) | As needed |
| **reference/** | Reference docs (for Agent to read and understand context) | Strongly recommended |
| **assets/** | Templates, configs, and supporting resources | As needed |

### Progressive Disclosure

**Key design principle**: Don't stuff all information into context at once.

- YAML front matter determines when to load the Skill
- Full instructions load only when Skill is triggered
- References load on demand, not pre-loaded

**Solves**: context window overload (too much info degrades quality) + token waste

---

## 5. Tool Design (OpenAI + Anthropic Consensus)

### Anthropic's Three Core Recommendations

1. **Think from the Agent's perspective**: Write tool descriptions like documentation for a junior developer — include examples, edge cases, input formats, differences from other tools
2. **Test and iterate**: Observe what errors the model makes; improving tool descriptions is often more effective than improving prompts
3. **Error-proof design (Poka-yoke)**: Make parameters harder to misuse (e.g., require absolute paths instead of relative)

### Anthropic's Field Experience

> "When building the SWE-bench Agent, we spent **more time optimizing tools than optimizing the overall prompt**. For example, we found the model made errors with relative file paths — switching to always requiring absolute paths made it work perfectly."

---

## 6. Four Gates for Production-Grade Agents (LangChain + OpenAI)

### Gate 1: Quality vs Latency
LangChain survey's **#1 concern** for agent engineers:
- High accuracy → multi-round reasoning/self-reflection → token cost explosion + long wait
- Low latency → fewer reasoning steps → potential quality drop
- **Resolution**: Find the sweet spot of "smart enough and fast enough"

### Gate 2: Observability
> "Agent bugs aren't crashes (visible) — they're fluent-sounding but entirely fabricated content (hallucinations)."

**Must track**: what materials the Agent read at each step, which knowledge base entries it cited, what decisions it made.

### Gate 3: Guardrails (OpenAI's Four Layers)

| Layer | Content |
|-------|---------|
| Input validation | Is the topic within knowledge base coverage? |
| Output filtering | Contains internal codenames / unreleased features / customer names? |
| Tool call limits | Prevent Agent from accessing unauthorized files |
| Human-in-the-loop | Which steps require human confirmation? |

### Gate 4: Evaluation Methods
- End-to-end: overall article quality (requires human judgment)
- Component-level: factual accuracy (can be auto-verified against knowledge base)
- Continuous monitoring: adoption rate and edit volume per article

---

## 7. Anthropic's Latest Architecture: Brain-Hands Separation

From Anthropic's April 2026 engineering blog — while targeting large-scale managed Agent scenarios, the core idea guides Skill design:

**Core idea**: Agent = Brain (reasoning + decisions) + Hands (execution) + Session (event log)

The three should be **decoupled** — Brain doesn't depend on specific Hands implementation, Session exists independently.

**Implications for Skill design**:
- **Skill = Brain** (SKILL.md defines reasoning logic and rules)
- **Tools/scripts = Hands** (file I/O, search, specific operations)
- **Knowledge base/directories = Session** (persistent state and data)

Separation means: modify Skill logic without touching the knowledge base; update knowledge base without rewriting the Skill; change directory structure without redesigning the Skill.

---

*Research: Ali | 2026-04-14*
