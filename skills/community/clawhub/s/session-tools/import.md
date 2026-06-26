# Session Import

Delivers session data to other agents/skills via pipeline.

## Quick Start

```
/session import --hookify          # Fetch session and deliver to hookify
/session import --analyze          # Session analysis pipeline
/session import --to <agent>       # Deliver to a specific agent
```

## Prerequisites

### 0. Verify claude-sessions-mcp tool registration

Call `mcp__code-mode__list_tools` to check whether `claude-sessions-mcp` tools are available:

```
mcp__code-mode__list_tools
```

If `mcp__claude-sessions-mcp__list_projects` is **not** in the results, register via the utcp skill first:

```
/utcp register
```

Verify registration before proceeding.

### 1. Fetch Session Data

First, fetch session data using `/session summarize`.
Alternatively, you can specify the project/session ID directly in the prompt.

## Pipeline Targets

Check for the following keywords in the prompt:

| Keyword | Target | Description |
|---------|--------|-------------|
| `hookify` | hookify:conversation-analyzer | Analyze patterns and generate hooks |
| `analyze` | general-purpose | Conversation analysis insights |
| `continue` | Parent agent | Return task context |

## Pipeline Examples

### hookify Pipeline

```
Task tool:
  subagent_type: "hookify:conversation-analyzer"
  prompt: |
    Find patterns to prevent from the following conversation and generate hooks:

    <conversation>
    {fetched session conversation content}
    </conversation>
```

### Analysis Pipeline

```
Task tool:
  subagent_type: "general-purpose"
  prompt: |
    Please analyze the following conversation:

    <conversation>
    {session data}
    </conversation>
```

### Custom Pipeline

When the user specifies a particular agent/skill:

```
Task tool:
  subagent_type: "{specified agent}"
  prompt: |
    Please work based on the following session context:

    <session_context>
    {fetched session data}
    </session_context>

    Request: {user's additional request}
```

## Full Workflow

1. Select project/session (`mcp__claude-sessions-mcp__list_*`)
2. Extract conversation content (`summarize-session.py`)
3. Identify pipeline target
4. Call agent via Task tool

## Notes

- If no pipeline target is found, return summarize results only
- hookify pipeline extracts user/assistant messages only
- Sensitive information is automatically filtered (API keys, tokens, etc.)
- Due to context limits, only the most recent 50 messages are delivered
