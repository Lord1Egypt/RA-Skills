# RAGFlow Custom Agent Guide

Read this file only when you need to author, debug, or review a RAGFlow Agent/Canvas DSL. For CLI syntax, read [COMMANDS.md](COMMANDS.md). For SDK request and response shapes, read [API.md](API.md). For failures and recovery steps, read [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

This guide distills the current RAGFlow v0.26.0 agent behavior into practical schema rules, minimal examples, and failure patterns you can use directly.

## Contents

- [Quick choice](#quick-choice)
- [Shortest path](#shortest-path)
- [Current schema checklist](#current-schema-checklist)
- [Components and graph must agree](#components-and-graph-must-agree)
- [Variable rules](#variable-rules)
- [Customize by node type](#customize-by-node-type)
- [Runtime conclusions](#runtime-conclusions)
- [Minimal example index](#minimal-example-index)
- [Common failures](#common-failures)

## Quick choice

| Goal | Read first | Start from |
|---|---|---|
| Build the smallest conversational agent | [Shortest path](#shortest-path) | `references/examples/agents/01-conversational-message.json` |
| Add knowledge-base retrieval | [Customize by node type](#customize-by-node-type) for `Retrieval` and `Agent` | `references/examples/agents/02-retrieval-message.json` or `03-tool-agent.json` |
| Build a tool-using LLM agent | [Customize by node type](#customize-by-node-type) for `Agent` | `references/examples/agents/03-tool-agent.json` |
| Build a loop or batch-processing agent | [Customize by node type](#customize-by-node-type) for `Iteration / IterationItem` | `references/examples/agents/04-iteration-agent.json` |
| Build a webhook agent | [Customize by node type](#customize-by-node-type) for `Webhook` | `references/examples/agents/05-webhook-message.json` |
| Debug `KeyError('path')`, broken variable resolution, or skipped nodes | [Current schema checklist](#current-schema-checklist) and [Common failures](#common-failures) | Compare against your DSL |

## Shortest path

Do not start from an empty JSON object.

1. Pick the closest file from `references/examples/agents/`.
2. Replace only deployment-specific values such as `llm_id`, `kb_ids`, tool credentials, and prompt text.
3. Keep the current runtime fields intact: `history`, `path`, `retrieval`, `variables`, `globals`, and `graph`.
4. Create the agent, look it up by title, create a session, and send a question.

```bash
node {baseDir}/scripts/ragflow.js create-agent \
  --title "My Agent" \
  --dsl @references/examples/agents/01-conversational-message.json \
  --json

node {baseDir}/scripts/ragflow.js list-agents --name "My Agent" --json
node {baseDir}/scripts/ragflow.js create-agent-session --agent <agent_id> --json
node {baseDir}/scripts/ragflow.js agent-chat --agent <agent_id> --session <session_id> --question "Hello" --json
```

`create-agent` currently returns `true` on success, not the new agent id.

## Current schema checklist

When you hand-author a DSL, keep this checklist:

- Top level includes `components`, `history`, `path`, `retrieval`, `variables`, `globals`, and `graph`
- `components` is the runtime structure and `graph` is the canvas structure; node ids must line up across both
- Every `graph.nodes[]` entry includes `data.name`
- `globals` explicitly keeps the system variables
- Every referenced `component_id` actually exists
- Loop flows define both `Iteration` and `IterationItem`
- Tool-enabled agents place tools under `Agent.params.tools`

Recommended skeleton:

```json
{
  "components": {},
  "history": [],
  "path": [],
  "retrieval": [],
  "variables": {},
  "globals": {
    "sys.query": "",
    "sys.user_id": "",
    "sys.conversation_turns": 0,
    "sys.files": [],
    "sys.history": [],
    "sys.date": ""
  },
  "graph": {
    "nodes": [],
    "edges": []
  }
}
```

Additional constraints:

- Keep `sys.date` even though runtime refreshes it
- `env.*` values come from top-level `variables`
- `component_id@output_name` values come from node outputs
- Prefer the current schema instead of relying on server-side migration from old DSL formats

## Components and graph must agree

RAGFlow agent DSL is not just an execution graph and not just a canvas export. `components` and `graph` must both be valid and must describe the same flow.

### `components`

Every component should at least look like this:

```json
{
  "begin": {
    "obj": {
      "component_name": "Begin",
      "params": {}
    },
    "downstream": ["message:0"],
    "upstream": []
  }
}
```

Key fields:

- `obj.component_name`: runtime component type
- `obj.params`: runtime parameters
- `downstream`: successor component ids
- `upstream`: predecessor component ids
- `parent_id`: needed only for nested nodes such as `IterationItem`

### `graph.nodes`

Every graph node should at least keep these fields:

```json
{
  "id": "begin",
  "type": "beginNode",
  "position": { "x": 50, "y": 200 },
  "data": {
    "label": "Begin",
    "name": "begin",
    "form": {
      "mode": "conversational",
      "prologue": "Hi! I'm your assistant."
    }
  }
}
```

Key constraints:

- `graph.nodes[].id` matches the `components` key
- `graph.nodes[].data.name` is required
- `graph.nodes[].data.form` should stay aligned with `obj.params`

### `graph.edges`

Each edge `source` and `target` must reference real component ids. Updating only `components.downstream` or only `graph.edges` leaves the runtime and canvas out of sync.

## Variable rules

Runtime variable resolution mainly supports three classes:

- System variables: `{sys.query}`, `{sys.user_id}`, `{sys.history}`
- Environment variables: `{env.foo}`
- Component outputs: `{retrieval:0@formalized_content}`, `{begin@body.message}`

Rules:

- Variables without `@` are read from `globals`
- Variables with `@` must use `component_id@output_name`
- Dot-path access is supported, for example `{begin@body.message}` or `{agent:0@structured.items.0.title}`

Most variable failures come from ids, output names, or top-level fields not lining up.

## Customize by node type

### Begin

`Begin.params.mode` currently supports:

- `conversational`
- `task`
- `Webhook`

`Webhook` is not an alias for ordinary chat mode. It triggers a separate webhook route and request-validation path.

### Message

`Message` most often emits the final answer:

```json
{
  "content": [
    "{agent:0@content}"
  ]
}
```

`content` is an array. Runtime selects one template at random, and templates can contain variable references.

### Retrieval

`Retrieval` can be either a canvas node or a tool definition inside `Agent.params.tools`. Common inputs are:

- `query`
- `kb_ids`
- `similarity_threshold`
- `top_n`
- `top_k`

If you want an explicit retrieval stage on the canvas, start from `02-retrieval-message.json`. If you want retrieval as an LLM tool, start from `03-tool-agent.json`.
As of v0.26.0, metadata filters are correctly reused across canvas executions even when node state is modified, fixing an issue where filters could be lost during iterative debugging.

### Agent

`Agent` is the tool-capable LLM node. In the current structure, tools live under `Agent.params.tools`:

```json
{
  "tools": [
    {
      "component_name": "Retrieval",
      "id": "Retrieval:tool0",
      "name": "Retrieval",
      "params": {}
    }
  ]
}
```

Do not model tools here as separate top-level `Tool` nodes. For this skill, prefer the embedded structure shown in `03-tool-agent.json`.
`Agent` nodes can emit structured JSON output directly into the `structured` field when a JSON schema is provided, allowing downstream nodes to access fields without manual string parsing.

### Iteration / IterationItem

Loops require at least:

- one `Iteration`
- one `IterationItem`
- `IterationItem.parent_id` pointing to its `Iteration`
- `Iteration.params.items_ref` pointing to the collection being iterated

Two practical constraints matter here:

- `items_ref` must resolve to a real list at runtime
- if the upstream value comes from an `Agent`, do not make the agent emit a top-level array schema directly; use an object schema such as `{"items": ["..."]}` and point `items_ref` at `agent:0@structured.items`

`04-iteration-agent.json` uses that pattern because it works against the current backend implementation.

### Webhook

When `Begin.mode = "Webhook"`, the server reads these extra fields:

### Browser

`Browser` is a component type that enables AI-driven browser automation within agent workflows. It allows agents to navigate web pages, extract content, and interact with browser elements programmatically. Use it when the agent needs to access live web data or perform web-based tasks as part of its workflow.

When `Begin.mode = "Webhook"`, the server reads these extra fields:

- `methods`
- `content_types`
- `schema`
- `security`
- `execution_mode`
- `response`

`schema` should follow the current exported JSON-schema-style object:

```json
{
  "body": {
    "type": "object",
    "required": ["message"],
    "properties": {
      "message": { "type": "string" }
    }
  }
}
```

Use `05-webhook-message.json` as the minimal reference.

## Runtime conclusions

Read this section only when you need to explain why a DSL can be created but still fails at session creation or runtime.

### Creation

`create-agent` calls `POST /api/v1/agents`. The server normalizes the DSL, which means:

- `--dsl` can be inline JSON
- `--dsl` can also be `@agent.json`
- old component names and old node types may be migrated, but migration should not be treated as the target schema

### Session

`create-agent-session` creates a new `Canvas` from the current agent DSL, resets runtime state, and stores the current DSL in the session. A session keeps more than chat messages; it also keeps runtime DSL state.

### Run

`agent-chat` calls `POST /api/v1/agents/chat/completions` with `agent_id` in the body. Runtime updates:

- `sys.query`
- `history`
- `sys.history`
- `sys.conversation_turns`
- `retrieval`

That is why removing these runtime-looking top-level fields can still let agent creation succeed while session creation or execution later fails.

## Minimal example index

All examples live in `references/examples/agents/` and can be used directly with `--dsl @...`:

| File | Best for | Usually replace |
|---|---|---|
| `01-conversational-message.json` | Smallest conversational agent, `Begin -> Message` | `prologue`, output template |
| `02-retrieval-message.json` | Explicit retrieval chain, `Begin -> Retrieval -> Message` | `kb_ids`, retrieval thresholds, output template |
| `03-tool-agent.json` | Tool-using LLM agent, `Begin -> Agent -> Message` | `llm_id`, `tools`, prompt |
| `04-iteration-agent.json` | Loop or batch-processing agent | `items_ref`, loop-body prompt, aggregate output |
| `05-webhook-message.json` | Webhook agent, `Begin(Webhook) -> Message` | `schema`, `security`, response definition |

These examples are structurally minimal, not production-minimal. Replace `llm_id`, `kb_ids`, API keys, webhook security settings, and any other deployment-specific values with real ones from your environment.

## Common failures

| Problem | Cause |
|---|---|
| `KeyError('path')` or session creation failure | Top-level runtime fields are incomplete |
| Agent creates successfully but runtime cannot resolve variables | `graph.nodes[].id`, `components` keys, and variable references do not line up |
| Logs or debugging output lose component names | `graph.nodes[].data.name` is missing |
| Agent appears to have tools but never calls them | Tools were not written into `Agent.params.tools` |
| Webhook agent creates successfully but endpoint behavior is broken | `Begin.mode`, `schema`, `security`, or `response` does not match the current implementation |
| Iteration agent creates successfully but crashes at execution time | `items_ref` resolved to `None` or a non-list, often because the upstream `Agent` did not produce a real `structured.items` array |
| Old DSL imports but behaves strangely | The server migrated it, but the final structure was not rewritten to the current schema |