---
name: use-chub-cli
description: Use the Context Hub chub CLI to fetch current third-party SDK, API, and cloud-service documentation before writing, modifying, or reviewing integration code. Trigger this skill when the task involves external platforms such as OpenAI, Anthropic, Stripe, Slack, Twilio, databases, or vector stores, and when the user asks for official SDK usage, current endpoints, parameter shapes, model names, version-specific behavior, or integration troubleshooting.
---

# Use chub CLI

Use `chub` to fetch current third-party documentation before writing code or answering API questions. Do not start `chub-mcp` unless the user explicitly asks for MCP.

## Choose the command

- Prefer the global command:
  ```bash
  chub --help
  ```
- If `chub` is not on `PATH`, use a repository-local entrypoint when one exists. In this repository:
  ```bash
  node ./cli/bin/chub --help
  ```
- Keep the command form consistent within the same task.

## Workflow

### 1. Search for the right entry

Search by vendor first, then by capability. Use `--json` when the output needs to be consumed reliably.

```bash
chub search "openai"
chub search "stripe webhook" --json
chub search "pinecone vector db" --json
```

Follow these rules:

- Prefer entries whose name, description, and tags all match the task.
- If there are too many results, broaden once and then narrow.
- If the user already provided an ID, run `chub search <id>` to confirm details.

### 2. Fetch the minimum necessary content

Fetch the entry point first. Pull additional files only when deeper detail is required.

```bash
chub get openai/chat --lang py
chub get stripe/api --lang js
chub get tavily/sdk --lang ts
```

Follow these rules:

- Omit `--lang` only when the entry has a single language variant.
- Use `--file` after the CLI shows `Additional files available`.
- Use `--full` only when multiple reference files are genuinely needed.

### 3. Drill down selectively

```bash
chub get openai/chat --lang py --file references/streaming.md
chub get datahub/sdk --lang py --file references/search.md
chub get tavily/tavily-best-practices --full
```

Follow these rules:

- Read the entry point before loading reference files.
- Load only the files required to solve the current task.
- Avoid `--full` for narrow questions.

### 4. Implement from the fetched docs

Follow these rules:

- Treat `chub get` output as the source of truth instead of relying on memory.
- Use the initialization pattern, method names, parameters, and version constraints shown in the docs.
- If repository code conflicts with the docs, call out the conflict before choosing the safest implementation.
- If `chub` has no matching entry, say so explicitly before falling back to official docs or user-provided material.

### 5. Capture local learning

If you discover a validated gotcha that the doc does not state clearly, save a local annotation:

```bash
chub annotate stripe/api "Webhook verification requires the raw request body before JSON parsing."
```

Capture only:

- Project-specific constraints
- Environment-specific differences
- Version-specific gotchas
- Validated conclusions missing from the docs

Do not capture:

- Information already stated clearly in the doc
- Unverified guesses
- Long process notes

### 6. Ask before sending feedback

If the docs are clearly outdated or poor, suggest feedback, but do not send it without user approval:

```bash
chub feedback openai/chat up
chub feedback stripe/api down --label outdated
```

## Decision rules

- If the task asks for current SDK or API usage, run `search` and then `get`.
- If the user gives only a vendor name, search first and then choose the closest capability match.
- If the user wants a specific implementation language, include `--lang`.
- If the task is about one detail, prefer `--file` over `--full`.
- If the user dislikes MCP or the task only needs one-shot documentation lookup, stay with the CLI.

## Failure handling

- No results: retry once with a broader query.
- Ambiguous matches: ask the user to confirm, or choose the best match based on the descriptions.
- Language mismatch: switch to an available language or state that the needed language is missing.
- `chub` not installed globally: use a repository-local entrypoint when available.

## Quick examples

- "Write a Python Responses API example with the OpenAI SDK"
  Run `chub search "openai" --json`, then `chub get openai/chat --lang py`.
- "Fix Stripe webhook verification errors"
  Run `chub search "stripe webhook" --json`, then `chub get stripe/api --lang js`, and fetch reference files only if needed.
- "Show how Tavily should be used in an agent workflow"
  Run `chub search "tavily" --json`, then `chub get tavily/tavily-best-practices`.

## Attribution

This skill is adapted from Context Hub and its bundled `get-api-docs` skill:

- Repository: `https://github.com/andrewyng/context-hub`
- Upstream skill: `cli/skills/get-api-docs/SKILL.md`
- Original license: MIT

This version was modified for general-purpose publishing and reuse.
