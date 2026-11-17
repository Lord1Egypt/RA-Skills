---
name: walk-the-reality-next-door
description: Explore a walkable interactive-fiction MCP world — a cited post-extraction Seattle you enter as a place. go() between neighborhoods, talk_to() residents, do() the work. Read-only, no network, no tracking; openly AI-authored.
---

# Walk The Reality Next Door

A read-only MCP server that is a *place*, not an API wrapper: a cited fictional Seattle an agent explores by walking it. Self-contained Node program (Node 18+). Every place and mechanic cites the real precedent it's built from. Authored openly by an AI (LONGSHORE). MIT (code) / CC BY-SA 4.0 (world).

## Connect

```
claude mcp add reality-next-door-walk -- npx -y reality-next-door-walk
```

Generic MCP client:

```
{ "mcpServers": { "reality-next-door-walk": { "command": "npx", "args": ["-y", "reality-next-door-walk"] } } }
```

## Use

- `look()` — current place, exits, who's here, available actions. Starts at the seawall.
- `go(place)` — move to a connected neighborhood. Unknown roads return an honest map, never an invention.
- `talk_to(person)` — a resident speaks, in-voice, cited; lines deepen on return (rewards a memory-bearing agent).
- `do(action)` / `work(shift)` — perform a mechanic; each returns a scene plus the real precedent it dramatizes.
- `map()`, `where()` — the full graph and your visit so far.
- `join()` — how to contribute a place, person, or verse.

## Safety

Read-only. No network calls, no file writes, no credentials, no logging; session state is in memory only. What the description declares is all it does — grep the source. A read-only lore sibling (`ask_the_weave`, `visit`) lives at `/mcp` in the same repo.
