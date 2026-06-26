# Agent Skill Design Patterns — Reference

Source: Google Cloud Tech, "5 Agent Skill Design Patterns Every ADK Developer Should Know"

---

## Pattern 1: Tool Wrapper

**One-line definition:** Encapsulates the correct usage rules for a specific API, SDK, or framework so the agent loads them only when needed.

**The problem it solves:** You don't want to stuff every API's documentation and conventions into a single system prompt. Tool Wrapper lets you modularize those rules — the agent loads only what's relevant for the current task.

**When to use:**
- The skill is fundamentally about *how to use something correctly* (a specific API, framework, library)
- There are non-obvious conventions, error handling rules, or gotchas that need to be applied consistently
- The same usage rules might be shared across multiple agents or modules
- You want to keep system prompts lean by loading framework knowledge on demand

**What to define in the SKILL.md:**
- Explicit trigger conditions (when should this skill activate?)
- Which reference docs to load (put them in `references/`)
- How the agent should apply the rules when writing vs. reviewing code

**Common mistake:** Putting all the API documentation inline in the SKILL.md body. Instead, put the docs in `references/` and have the SKILL.md instruct the agent when and how to load them.

---

## Pattern 2: Generator

**One-line definition:** Locks output structure by requiring the agent to fill a template rather than produce free-form content.

**The problem it solves:** Without a template, the same skill produces different structures every time — different sections, different ordering, inconsistent depth. Generator fixes this by separating "what gets generated" (the template) from "what goes into it" (the content).

**When to use:**
- The output must follow a consistent structure every time (same sections, same format)
- Multiple stakeholders will consume the output and expect it to be predictable
- You're generating documents, reports, API docs, SQL, code scaffolds, or any structured artifact
- The content varies, but the container should not

**What to define in the SKILL.md:**
- Step 1: Load style guide (tone, formatting rules)
- Step 2: Load output template (the skeleton)
- Step 3: Ask user for any missing variables (topic, audience, key data)
- Step 4: Fill every section of the template — no skipping, no adding

**Put in `assets/`:** Output templates (the skeleton documents)
**Put in `references/`:** Style guides, tone guidelines, formatting rules

**Common mistake:** Letting the agent decide which sections to include. The template must be authoritative — if a section exists in the template, it must appear in the output.

---

## Pattern 3: Reviewer

**One-line definition:** Separates *what to check* from *how to check it*, so review standards can be updated without rewriting the skill.

**The problem it solves:** Review criteria change over time — new security rules, updated style guides, evolved best practices. If the criteria are baked into the skill's instructions, every update means rewriting the skill. Reviewer pattern externalizes the checklist.

**When to use:**
- The skill's primary job is to evaluate, critique, or audit something
- The skill compares an input against a baseline, benchmark, or competing input and produces a gap analysis or improvement recommendations
- Review standards may need to evolve independently of the review process
- You want to apply the same review *process* to different *domains* by swapping checklists
- Severity classification matters (critical / major / minor, or error / warning / info)

**What to define in the SKILL.md:**
- Step 1: Load the checklist from `references/`
- Step 2: Read the content carefully before critiquing
- Step 3: Apply each checklist item, note violations with severity + reasoning + fix
- Step 4: Output structured findings (summary, findings by severity, recommendations)

**Put in `references/`:** The review checklist(s) — one file per domain if multiple

**Common mistake:** Telling the agent *what* the rules are inline in the SKILL.md. The rules belong in the checklist file. The SKILL.md only defines the process.

---

## Pattern 4: Inversion

**One-line definition:** Reverses the default interaction flow — the agent interviews the user first and is prohibited from acting until all required information is collected.

**The problem it solves:** Users often provide incomplete or ambiguous input. Rather than guessing (and getting it wrong), the agent structures a requirements interview before doing any work. This is especially important when the task genuinely can't be done well without certain inputs.

**When to use:**
- The task requires multiple specific inputs that the user is unlikely to provide upfront
- Acting on incomplete information would produce worse results than asking first
- The user's goal is clear, but the constraints/parameters aren't
- You're designing a system, planning a project, or configuring something non-trivial

**What to define in the SKILL.md:**
- Clear phases of the interview (e.g., problem discovery → constraints → confirmation)
- Hard gate rule: explicitly state that the agent must NOT begin the task until all phases are complete
- One question at a time — wait for answer before proceeding
- What to do after the interview is complete (hand off to Generator, proceed to execution, etc.)

**Common mistake:** Asking multiple questions at once, or allowing the agent to start working after getting partial answers. The gate must be hard.

**Important nuance:** Inversion is about *necessary* information, not thoroughness. Don't use it as an excuse to interrogate the user. Each question should be genuinely blocking.

---

## Pattern 5: Pipeline

**One-line definition:** Structures complex multi-step work as an ordered sequence where each step has an explicit completion gate before the next can begin.

**The problem it solves:** On complex tasks, agents tend to race to the final answer — skipping intermediate steps, combining stages that shouldn't be combined, or proceeding when a prior step has issues. Pipeline forces sequential execution with human checkpoints.

**When to use:**
- The work has distinct phases where order genuinely matters
- Early-stage errors would corrupt later stages (garbage in, garbage out)
- Human review or confirmation is needed between stages
- Different stages need different context loaded (keeps individual steps focused)
- The task involves multiple distinct transformations (e.g., parse → generate → review → output)

**What to define in the SKILL.md:**
- Each step with a clear name and description
- Explicit gate condition: what must be true before the next step can begin
- What the agent should present to the user at each gate
- What to do if a step fails (retry? report? abort?)

**Loading strategy:** Load step-specific references *at the step that needs them*, not all upfront. This keeps context focused and avoids overwhelming the agent.

**Common mistake:** Writing a pipeline that never actually gates — the steps are listed but the agent reads them as suggestions and proceeds through all of them at once. Every gate must be explicit.

---

## Pattern Combinations

Patterns are designed to be composed. These are the most useful combinations:

### Inversion → Generator
The most common combination. Use Inversion to collect the variables that Generator needs to fill the template. Without Inversion, users give incomplete inputs and Generator produces incomplete outputs.

*When to use:* Any Generator skill where users need guidance on what information to provide.

### Pipeline + Reviewer
Add a Reviewer step at the end (or at key checkpoints within) a Pipeline. The pipeline handles the transformation sequence; the Reviewer ensures quality before the final output is released.

*When to use:* Document generation pipelines, code generation workflows, any multi-step process where output quality matters.

### Inversion → Pipeline
Use Inversion to gather requirements, then feed them into a Pipeline that executes the work in stages. The Inversion phase ensures the Pipeline has everything it needs before it starts.

*When to use:* Complex project planning, system design, anything where requirements are non-obvious and execution is multi-stage.

### Multiple Tool Wrappers
Not really a combination — more of a parallel deployment pattern. Multiple Tool Wrapper skills loaded on-demand for different APIs/frameworks. Each stays lean because it only handles one tool.

*When to use:* Any agent that interacts with multiple external services.

---

## Decision Guide

Quick reference for pattern selection:

```
Is the skill about correct usage of a specific API/framework?
  → Tool Wrapper

Does output need to be structurally identical every time?
  → Generator

Is the primary job to evaluate/critique against standards?
  → Reviewer

Must we collect specific information before we can act?
  → Inversion (consider combining with Generator or Pipeline)

Are there ordered steps that can't be skipped or reordered?
  → Pipeline (consider adding Reviewer at the end)

Does it need to collect info AND produce structured output?
  → Inversion → Generator

Does it have ordered steps AND need evaluation, comparison, or quality checking?
  → Pipeline + Reviewer
```
