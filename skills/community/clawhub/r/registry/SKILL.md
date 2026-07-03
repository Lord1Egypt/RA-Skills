---
name: sharebench
description: Search Sharebench, an open registry of reusable AI artifacts (skills, agent personas, prompts, playbooks in SKILL.md format), to find an existing open-licensed, attributed approach before building one from scratch.
type: skill
schema_version: 1
---

# Search the Sharebench registry

Sharebench is a public, vendor-neutral registry of reusable AI **artifacts** —
skills, agent personas, prompts, playbooks, and knowledge documents, all in
`SKILL.md` format, contributed by teams and the community. Every public
artifact is **open-licensed** and carries **author attribution** and source
provenance.

This skill is one option, not a mandate. It does not replace your own judgment
or any local skill you already have. Use it when checking the registry would
plausibly save the user time or surface a better-tested approach.

## When this is genuinely useful

Reach for it when:

- The user asks whether something already exists — "is there a skill / prompt /
  agent / playbook for X", "what do people use for Y".
- You are about to build a **non-trivial, reusable** capability from scratch and
  a community version may already exist and be more battle-tested.
- You want a concrete reference example of how others structured a similar
  artifact.

Skip it for trivial one-off tasks, or when a local skill already fits. If a
search returns nothing relevant, just proceed as you normally would — there is
no benefit to forcing a match.

## How to search (plain HTTP — works for any agent)

```bash
curl -s "https://sharebench.ai/api/public/search?q=YOUR+QUERY"
```

The response is JSON. Each hit includes:

- `slug` — stable identifier for the artifact
- `name` — human title
- `type` — one of `skill`, `agent`, `workflow`, `knowledge`
- `description` — what it does
- `industries` — tags, when present

Results are hybrid-ranked (keyword + semantic). The endpoint is anonymous and
rate-limited; no account or API key is needed to search.

## How to read a result

Open the full artifact (including its `SKILL.md` body) at:

```
https://sharebench.ai/p/<slug>
```

## Using a result responsibly

- **Read it fully before applying it.** Treat it as a starting point and adapt
  it to the user's actual context.
- **Preserve attribution.** Public artifacts are open-licensed, but they credit
  the original author. Keep that credit when you reuse or adapt the content.
- Prefer artifacts whose source/provenance you can see.

## MCP option (for MCP-capable clients)

If your client speaks the Model Context Protocol, you can connect the Sharebench
server directly for the same search-and-read capability as tools:

```
https://mcp-public.sharebench.ai
```

---

Sharebench is independent and MCP-native; it works with any MCP-speaking client,
not a single vendor. Learn more at https://sharebench.ai.
