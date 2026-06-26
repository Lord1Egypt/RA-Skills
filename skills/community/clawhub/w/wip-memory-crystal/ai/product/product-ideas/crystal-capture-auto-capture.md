# Crystal Capture: Automatic Conversation Capture

**Source:** GPT feedback on v0.6.0 release (2026-03-04)
**Priority:** High (adoption driver)

## The Insight

GPT's exact framing: "The single killer feature is auto-capture every AI conversation."

Right now Memory Crystal requires either:
- An agent hook (OpenClaw plugin, Claude Code hook) ... which means the AI platform has to support it
- Manual `crystal_remember` calls ... which means the user has to think about it

If instead it silently captured everything from every AI tool, it becomes indispensable. Once someone installs it, they never uninstall it because their entire AI history lives there.

## What We Already Have

- `cc-hook.ts` ... Claude Code hook (captures after every conversation turn)
- `cc-poller.ts` ... continuous capture via cron (scans JSONL files)
- `openclaw.ts` ... OpenClaw plugin (agent_end hook)
- `crystal backfill` ... retroactive import of existing sessions
- `crystal init` ... discovers existing session files

These cover Claude Code CLI and OpenClaw. The gap is everything else.

## What We Need

Three adapters to cover the rest of the AI landscape:

### 1. Desktop App Watchers (file system)

Watch for conversation files from:
- `~/Library/Application Support/ChatGPT/` (ChatGPT desktop)
- `~/Library/Application Support/Claude/` (Claude desktop)
- Cursor chat logs
- Other MCP-compatible tools

Implementation: `fswatch` or `chokidar` on known paths. When files change, extract messages and ingest. Similar to how `cc-poller.ts` already works for Claude Code.

### 2. Terminal Wrapper

```bash
mc run claude
mc run openclaw
mc run python agent.py
```

Wraps any terminal AI session, captures stdin/stdout, and pipes to Memory Crystal. Like `script` but with semantic chunking.

### 3. Browser Extension

Capture conversations from:
- chat.openai.com
- claude.ai
- perplexity.ai

Send to local Memory Crystal via localhost endpoint (`crystal serve`).

## The Complete Loop

GPT nailed the architecture:

```
Capture ... Memory ... Dream

Which is:

experience ... memory ... learning
```

Or in our stack:

```
Crystal Capture (auto-capture)
    |
Memory Crystal (storage + vector index)
    |
Dream Weaver (narrative consolidation)
    |
Boot Sequence (warm start)
```

## Why This Matters for Adoption

GPT's argument: "AI conversations are currently disposable. Developers lose insights constantly. Memory Crystal would turn AI into persistent collaborators instead of temporary chats."

The pain is real. Every developer has had the experience of asking Claude something six months ago and having no way to find it again. Memory Crystal solves this, but only if capture is automatic.

## Naming

GPT suggested:
- **Crystal Capture** (fits the naming convention)
- **Memory Crystal Recorder**

We already use "capture" in the codebase (`cc-hook.ts` capture state, `captureCount`). Crystal Capture is natural.

CLI: `crystal capture on` / `crystal capture off`

## The Bigger Picture

GPT also called Memory Crystal "the Git for cognition." The analogy:
- Git = version control for code
- Memory Crystal = version control for AI conversations and knowledge
- Both are local-first, distributed, content-addressable

## Implementation Priority

1. **Desktop app watchers** ... highest impact, covers ChatGPT + Claude desktop (largest user bases)
2. **Browser extension** ... covers web interfaces (chat.openai.com, claude.ai)
3. **Terminal wrapper** ... covers CLI tools and custom agents

The desktop watcher could ship as a LaunchAgent, similar to how wip-healthcheck works.
