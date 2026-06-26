# Crystal Capture: Architecture Feedback from GPT

**Source:** GPT follow-up analysis (2026-03-04)
**Context:** After reviewing v0.6.0 releases and learning about existing capture hooks

---

## Key Insight: We Already Built the Hard Part

GPT's observation: the core capture abstraction already exists.

```
event ... normalize ... store ... embed ... memory
```

This pipeline is live in:
- `cc-hook.ts` (Claude Code hook)
- `cc-poller.ts` (file system watcher)
- `openclaw.ts` agent_end hook

The architecture is:

```
Adapters
    |
Capture hooks
    |
Memory Crystal store
    |
Dream Weaver consolidation
```

"The missing work is mostly integration surfaces, not core infrastructure."

---

## The Adapter List is Finite

Only ~5 adapters to cover 90% of AI developer workflows:

1. Claude Code CLI (done)
2. ChatGPT Desktop
3. Claude Desktop
4. Cursor
5. Browser extension

Everything else (Perplexity, Copilot, etc.) is incremental after that.

---

## Proposed CaptureEvent Interface

GPT suggested formalizing what adapters send:

```typescript
interface CaptureEvent {
  source: string
  timestamp: number
  user_input: string
  assistant_output: string
  tools?: ToolCall[]
  metadata?: Record<string, any>
}
```

Adapters convert their environment to this format. Memory Crystal stays clean.

**Note:** Our existing `ExtractedMessage` interface in cc-poller.ts and oc-backfill.ts is close:
```typescript
interface ExtractedMessage {
  role: string
  text: string
  timestamp: string
  sessionId: string
}
```

CaptureEvent is a superset. Could be the public adapter API.

---

## Repo Structure Signal

Suggested directory:

```
/adapters
   chatgpt-desktop/
   claude-desktop/
   cursor/
   browser/
   terminal/
```

"It signals immediately to developers: this system captures cognition."

---

## The Category Shift

"The moment capture becomes automatic, the system shifts from tool to infrastructure."

- Tools get opened occasionally
- Infrastructure runs all the time

That's the adoption inflection point.

---

## Longitudinal Cognition Data

With automatic capture + Dream Weaver, Memory Crystal eventually accumulates:

- How ideas evolved over time
- What conversations led to decisions
- What insights repeat across sessions
- What knowledge stabilizes vs. changes

"That's effectively machine-assisted reflection."

---

## The Four-Layer Narrative

GPT suggested explicitly describing the stack as:

```
Capture         ... record everything
Memory          ... store and search
Reflection      ... consolidate what matters
Communication   ... agents talk to each other
```

Maps to our components:
- Capture = Crystal Capture (cc-hook, cc-poller, adapters)
- Memory = Memory Crystal (crystal.db, vector search, relay)
- Reflection = Dream Weaver Protocol (narrative consolidation)
- Communication = Bridge (agent-to-agent)

This is cleaner than our current five-layer model for external communication.

---

## Design Validation

"The fact that you already had cc-hook and agent_end hooks built before this discussion is a good signal. It suggests the design was converging toward this architecture naturally rather than being forced."

GPT's read: "When someone can reverse-engineer the vision, it usually means the primitives are aligned."

---

## Action Items

1. Formalize `CaptureEvent` interface as the public adapter API
2. Create `/adapters` directory structure
3. Build ChatGPT Desktop adapter first (largest user base, file-system based)
4. Consider the four-layer narrative (Capture / Memory / Reflection / Communication) for README and marketing
5. Add "30-second mental model" to top of README per earlier feedback
