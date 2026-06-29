# SADC Subagent Delegation Template

This file contains the detailed SADC subagent delegation pattern. Read this when:
- Task tier is Standard or Complex
- You need to launch a `Task` subagent for SADC research
- You need the example Task invocation prompt structure

## Mandate

For Standard/Complex tier tasks, delegate SADC research to a `Task` subagent (subagent_type: `general-purpose`) BEFORE writing the problem specification.

## Subagent Workflow

1. **`Skill(command="web-search")`** — search for existing packages, libraries, or patterns matching the task domain. Examples:
   - "Python library for PDF text extraction"
   - "Next.js 16 authentication middleware patterns"
   - "matplotlib Chinese font configuration"

2. **`Skill(command="web-reader")`** — extract full content from the top 3-5 most relevant URLs returned by web-search. Focus on: official docs, README, getting-started guides.

3. **Return to main agent**: a concise summary (≤500 words) covering:
   - Existing solutions found (name + URL + 1-line description)
   - Recommended approach based on official docs
   - Any gotchas or anti-patterns noted in the docs
   - If no existing solution: explicit statement "searched <sources>, no existing package found"

## Why Subagent (Not Inline)

- Subagent runs in its own context window — doesn't pollute main agent's context with raw search results
- Main agent can begin drafting problem-spec.md while subagent researches (parallel work)
- Subagent's research output becomes part of the problem-spec's "Sources checked" section
- If subagent finds an existing library that solves the task, the main agent can pivot BEFORE writing any code — saves hours of wasted implementation

## Example Task Invocation

```
Task(
  description: "SADC research for <task>",
  subagent_type: "general-purpose",
  prompt: "Research existing solutions for <task description>.
    1. Invoke Skill(command='web-search') with query: '<domain-specific query>'
    2. From the top 5 results, invoke Skill(command='web-reader') on the 3 most relevant URLs
    3. Return a summary (≤500 words): existing solutions found, recommended approach, gotchas.
    If no existing solution, state explicitly: 'searched <sources>, no existing package found'.
    Pass Task ID: SADC-001. Read /home/z/my-project/worklog.md before starting.
    Append your work record to /home/z/my-project/worklog.md when done."
)
```

## Simple / Minimal Tier

Skip subagent delegation. Inline research is fine for these tiers — the task is small enough that context pollution is minimal.
