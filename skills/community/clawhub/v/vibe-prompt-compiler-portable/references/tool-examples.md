# Tool-Specific Examples

## Cursor Example

### Workflow

1. Run:

```bash
python3 scripts/compile_prompt.py --request "Build an event registration admin panel MVP" --stack "Next.js, Supabase, Tailwind"
```

2. Paste the output into Cursor Chat.
3. Add this short instruction after the compiled prompt:

```text
Use this as the source of truth. Plan briefly first, then implement only the first useful slice. Do not modify unrelated files.
```

### Better for broad tasks

For larger requests, run:

```bash
python3 scripts/create_handoff.py --request "Build an event registration admin panel MVP" --mode plan-only --output handoff
```

Then paste the handoff into Cursor Chat.

## Claude Code Example

### Workflow

Run:

```bash
python3 scripts/create_handoff.py --request "Fix the login API 500 error" --mode bugfix --output handoff
```

Then pass the handoff into Claude Code with an extra instruction like:

```text
Use the handoff as the source of truth. Start with root-cause analysis, then apply the smallest safe fix.
```

### Good fit

- bugfixes
- refactors
- broad implementation tasks where drift is a risk
- codebase work where you want stronger planning before editing

## Codex CLI Example

### Workflow

Run:

```bash
python3 scripts/create_handoff.py --request "Build a lightweight CRM MVP" --mode plan-only --output handoff > /tmp/crm-handoff.txt
```

Then either:

- paste `/tmp/crm-handoff.txt` into Codex CLI
- or use it as the main task text in your coding session

### Short task variant

For a focused request:

```bash
python3 scripts/compile_prompt.py --request "Refactor the profile settings form" > /tmp/refactor-prompt.txt
```

Then feed that prompt to Codex CLI.

### Better prompt wrapper for Codex CLI

Append this after the compiled prompt:

```text
Work surgically. Prefer minimal diffs, preserve existing conventions, and verify the current slice before moving on.
```

## Gemini CLI Example

### Workflow

Run:

```bash
python3 scripts/create_handoff.py --request "Design a multi-tenant isolation approach for our React + FastAPI app" --mode plan-only --output handoff > /tmp/tenant-brief.txt
```

Then paste the brief into Gemini CLI with:

```text
Use this brief as the source of truth. First compare 2-3 practical architecture options, then recommend the smallest robust path for the current stack.
```

### Good fit

- architecture exploration
- alternative comparison
- implementation planning before coding
- turning vague product requests into executable engineering tasks

## Generic IDE Chat Example

### Workflow

Use `compile_prompt.py` for quick work:

```bash
python3 scripts/compile_prompt.py --request "Add bulk delete to the users table with confirmation" --task crud-feature
```

Then paste the output into your IDE chat and add:

```text
Implement only the current slice. Keep the patch small and explain how to verify it.
```

## Complex Request Example: Architecture

### Input request

```text
We have one testing system and want to support two products with isolated data but identical features.
```

### Better handoff move

Use:

```bash
python3 scripts/create_handoff.py --request "We have one testing system and want to support two products with isolated data but identical features" --task architecture-review --output handoff
```

Then ask the coding tool:

```text
Use this handoff as the source of truth. Recommend the best near-term architecture for the current stack, explain trade-offs, and avoid over-engineering.
```

## Complex Request Example: Automation

### Input request

```text
Set up a workflow that watches inbound files, parses them, stores records, and alerts us when processing fails.
```

### Better handoff move

Use:

```bash
python3 scripts/create_handoff.py --request "Set up a workflow that watches inbound files, parses them, stores records, and alerts us when processing fails" --task automation-workflow --output handoff
```

Then ask the tool:

```text
Use this handoff as the source of truth. Design the workflow with retries, idempotency, and observability, then implement the smallest reliable slice.
Respect the non-goals and deliver exactly the listed deliverables.
```

## Rule of Thumb

- use `compile_prompt.py` for shorter, clearer tasks
- use `create_handoff.py` for bigger, riskier, or more ambiguous tasks
- prefer `architecture-review` when the user is really asking for system shape, trade-offs, or rollout strategy
- prefer `automation-workflow` when the core problem is triggers, background execution, retries, or operations
- prefer `integration` when third-party systems and failure semantics are central
