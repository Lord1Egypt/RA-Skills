# Anthropic Tool Design Guide — Key Takeaways

> Source: Anthropic Engineering Blog — "Writing effective tools for agents — with agents" (2025.09)
> Original: https://www.anthropic.com/engineering/writing-tools-for-agents

---

## Core Insight

Tools are a **contract between deterministic systems and non-deterministic Agents**. Traditional APIs are system-to-system contracts (deterministic input → deterministic output), but Agents may use tools in unexpected ways. Design tools **from the Agent's perspective**, not the developer's.

---

## Five Core Principles

### 1. Choose the Right Tools (and choose NOT to build some)

**More tools ≠ better results.**

Common mistake: wrapping API endpoints 1:1 as tools, regardless of whether the Agent needs them.

Agents have limited context windows — they can't efficiently iterate through large datasets like programs can. Design tools to match the Agent's capability model.

**Correct approach:**
- Build `search_contacts` instead of `list_contacts` (Agents can't efficiently scan lists)
- Build `schedule_event` instead of separate `list_users` + `list_events` + `create_event`
- Build `get_customer_context` instead of `get_customer_by_id` + `list_transactions` + `list_notes`

**Principle**: Tools should consolidate multi-step operations, reducing the Agent's intermediate output overhead.

### 2. Namespace Your Tools

Agents may face hundreds of tools. Group by prefix to help Agents locate the right one:
- `asana_projects_search`, `asana_users_search`
- `jira_search`, `jira_create_issue`

### 3. Return Meaningful Context

- **Prefer**: name, image_url, file_type (directly useful)
- **Avoid**: uuid, 256px_image_url, mime_type (low-signal noise)
- Resolving UUIDs to human-readable names **significantly reduces hallucination rates**
- Provide a `response_format` parameter (concise / detailed) to control verbosity

### 4. Optimize for Token Efficiency

- Implement pagination, range selection, filtering, truncation
- Claude Code defaults to 25,000 token limit per tool response
- When truncating, include guidance ("Results truncated. Use filter parameters to narrow scope.")
- Error responses must be **specific and actionable**, not raw tracebacks

**Good error response:**
> "Parameter `start_date` has invalid format. Use YYYY-MM-DD, e.g., 2026-04-14."

**Bad error response:**
> "Error: Invalid input"

### 5. Prompt-Engineer Your Tool Descriptions

**One of the most effective optimization methods** — refining tool descriptions can yield dramatic improvements.

- Write tool descriptions like onboarding docs for a new team member: include examples, edge cases, format requirements
- Avoid ambiguity: use `user_id` not `user`
- Anthropic found Claude was appending "2025" to search queries — fixed by improving the tool description

**Anthropic quote:**
> "On the SWE-bench project, we spent more time optimizing tools than optimizing the overall prompt."

---

## Evaluation-Driven Iteration Process

1. **Build prototype** → quick setup, manual testing
2. **Build eval set** → prompt-response pairs grounded in real scenarios
3. **Run evaluation** → collect accuracy, runtime, token usage, error rates
4. **Analyze results** → read Agent reasoning chains, find tool usage issues
5. **Let Agent improve tools** → feed eval logs to Claude Code, let it optimize descriptions and implementations
6. **Hold out test set** → prevent overfitting

---

## Key Takeaways

| Principle | One-liner |
|-----------|-----------|
| Design for Agents, not developers | Agents' cognitive model differs from programs |
| Fewer, better tools beat many mediocre ones | Too many tools confuse Agents |
| Tool descriptions > prompt engineering | ROI of improving tool descriptions often exceeds system prompt changes |
| Absolute paths > relative paths | Prevents Agent path-reasoning errors |
| Evaluation-driven | You don't know if tools work until you test them |
| Specific errors > generic errors | Help Agents self-correct |

---

*Distilled by Ali | 2026-04-14*
