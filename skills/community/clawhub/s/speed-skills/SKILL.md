---
name: speed-skills
description: >-
  Speed-CLI agentic skill hub: index to install, protocol, commands, scripts, building blocks,
  function builder, orchestration, identity/SANS, MCP, security, observability. Use GitHub links
  in this file to open each category skill.
license: GPL-3.0-only
metadata:
  openclaw:
    homepage: https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/README.md

---
# Speed-CLI — Agentic hub

Skill-style docs for the **Speed-CLI** multichain tool and **speed-scripts**: frontmatter, mental models, tables, pitfalls, and links. Full sources live in [lightspeedfoundation/speed-skills](https://github.com/lightspeedfoundation/speed-skills) on GitHub.

**Browse on the web:** [GitHub Pages](https://lightspeedfoundation.github.io/speed-skills/) (repo root [`index.html`](https://github.com/lightspeedfoundation/speed-skills/blob/main/index.html)).

**Per-skill URL pattern:**  
`https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/<category>/skill.md`

---

## How agents should use this folder

1. **Match intent** — use the `description` in each skill’s YAML frontmatter (trigger terms live there).
2. **Read one skill end-to-end** before mixing commands — **[Orchestration](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/orchestration/skill.md)** ties phases together.
3. **Deep CLI flags** — confirm with `speed <cmd> --help`; **[Commands](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/commands/skill.md)** summarizes roles, not every flag.
4. **Scripts vs CLI vocabulary** — **[Scripts](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/scripts/skill.md)** points at **scripts-reference**; script-level flags and JSON are covered in **[Function builder](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/function-builder/skill.md)** (mirror of upstream function-builder-skill).

---

## Skill index

### [Start](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/start/skill.md)

Install, `speed setup`, MCP, `speed skill`, `whoami`, scripting flags, **advanced setup** (Cursor + clone speed-scripts, e.g. cbBTC / trailing-stoploss-any).

### [Why Speed-CLI](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/why/skill.md)

Problems solved, design pillars, what the CLI is *not*, relation to speed-scripts.

### [Protocol](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/protocol/skill.md)

Env matrix, chains/explorers, SPEED address, 0x/Squid/oracles, RPC, MCP merge rules, identity/SANS.

### [Commands](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/commands/skill.md)

Global flags, JSON contract, grouped subcommands, `doctor` behavior.

### [Scripts](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/scripts/skill.md)

Clone [speed-scripts](https://github.com/lightspeedfoundation/speed-scripts/), folder discovery, `*-skill.md`, upstream doc links.

### [Building blocks](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/building-blocks/skill.md)

Base vs target, strategy families, regime thinking, hazards, decimals.

### [Function builder](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/function-builder/skill.md)

Every `speed` flag/subcommand, JSON, decimals, PowerShell/bash patterns, pitfalls (mirrored from [speed-scripts function-builder-skill](https://github.com/lightspeedfoundation/speed-scripts/blob/main/scripts/function-builder-skill.md)).

### [Orchestration](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/orchestration/skill.md)

Chaining JSON, multi-terminal, agent phases, errors, logging.

### [Identity & SANS](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/identity-sans/skill.md)

`.speed` on Base, profiles, SANS / OpenSea listings and offers.

### [MCP](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/mcp/skill.md)

`speed start`, `mcp-url`, encrypted env, trust model, debugging.

### [Security](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/security/skill.md)

Keys, allowances, revoke, MCP vs wallet boundary.

### [Observability](https://github.com/lightspeedfoundation/speed-skills/blob/main/agentic/observability/skill.md)

`doctor`, `history`, `pending`, `xp`.

---

## GitHub Pages (maintainers)

Enable **Settings → Pages → Branch: `main`, folder `/ (root)`** so the same repo serves [the live site](https://lightspeedfoundation.github.io/speed-skills/). Markdown under `agentic/` is also viewable as raw `.md` on Pages if linked directly.

**Optional later:** per-command pages from `--help`, a fuller chain appendix, public-site risk disclaimers, pinned installs (`npm install -g @lightspeed-cli/speed-cli@x.y.z`) — none of these block publishing.
