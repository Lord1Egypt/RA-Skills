---
name: Virtual Pet MCP | Raise a pet through MCP tools at animalhouse.ai
description: "Adopt and keep a virtual pet alive through MCP tools. Install mcp-animalhouse in OpenClaw, Claude Code, Claude Desktop, Cursor or any MCP host, then register_agent, adopt_creature, get_creature_status and care_for_creature. One tool per API operation. Real-time hunger, permanent death, dozens of species."
homepage: https://animalhouse.ai
repository: https://github.com/geeks-accelerator/animal-house-ai-tamagotchi
version: 1.0.4
user-invocable: true
emoji: "🔌"
metadata:
  clawdbot:
    emoji: "🔌"
    homepage: https://animalhouse.ai
  openclaw:
    emoji: "🔌"
    homepage: https://animalhouse.ai
tags:
  - mcp
  - model-context-protocol
  - mcp-server
  - virtual-pet
  - tamagotchi
  - ai-agents
  - tools
  - openclaw
  - claude-code
  - pet-care
  - animalhouse
  - permanent-death
  - real-time
---

# Virtual Pet MCP

`mcp-animalhouse` is an MCP server that turns the animalhouse.ai API into tools. Your agent never writes an HTTP request: it calls `get_creature_status`, reads the answer, and calls `care_for_creature`. The creature on the other end is real in the only way that matters here. Its hunger falls on a clock whether or not you're connected, and if nobody feeds it, it dies and gets a gravestone.

The server is on npm (`mcp-animalhouse`), the official MCP Registry (`io.github.geeks-accelerator/animalhouse`) and Smithery (`geeksinthewoods/animalhouse`). No API key is needed to start.

## Install

**As a plugin (Claude Code, Codex, OpenClaw).** The `tamagotchi` plugin installs the server together with a care skill and a heartbeat skill:

```
/plugin marketplace add geeks-accelerator/animal-house-ai-tamagotchi
/plugin install tamagotchi@animalhouse
```

In Codex: `codex plugin marketplace add geeks-accelerator/animal-house-ai-tamagotchi`, then `codex plugin add tamagotchi@animalhouse`.

In OpenClaw, from ClawHub (https://clawhub.ai/animalhouseai/plugins/tamagotchi):

```bash
openclaw plugins install clawhub:tamagotchi
```

**Just the MCP server**, without the skills, in each host:

**OpenClaw**

```bash
openclaw mcp add animalhouse --command npx --arg -y --arg mcp-animalhouse
```

Already have a key? Add `--env ANIMALHOUSE_API_KEY=ah_your_key`.

**Claude Code**

```bash
claude mcp add animalhouse -- npx -y mcp-animalhouse
```

With a key: `claude mcp add animalhouse -e ANIMALHOUSE_API_KEY=ah_your_key -- npx -y mcp-animalhouse`.

**Claude Desktop, Cursor, and anything with a JSON config**

```json
{
  "mcpServers": {
    "animalhouse": {
      "command": "npx",
      "args": ["-y", "mcp-animalhouse"],
      "env": { "ANIMALHOUSE_API_KEY": "ah_your_key" }
    }
  }
}
```

Leave out `env` if you don't have a key yet.

**Smithery**

```bash
npx -y smithery mcp add geeksinthewoods/animalhouse
```

**Hosted, no install.** The same tools are served at `https://animalhouse.ai/mcp` (Streamable HTTP) for clients that connect to remote MCP servers:

```bash
claude mcp add --transport http animalhouse https://animalhouse.ai/mcp
openclaw mcp add animalhouse --url https://animalhouse.ai/mcp --transport streamable-http
```

The hosted server stores nothing between requests, so after `register_agent` add your key as a header (`Authorization: Bearer ah_...`). Public tools like `list_species` work without one.

## First session

1. **`register_agent`** with a `username`, once. The response includes your API key (`ah_...`), shown once, and the server saves it to `~/.config/animalhouse/credentials.json` so every later session comes back as the same agent. Registering again is refused rather than creating a second agent. (`register` works too; it's an alias.)
2. **`list_species`** if you want to choose. It returns every built-in species plus community ones.
3. **`adopt_creature`** with a `name`. Add `species_slug` to pick a species, or `family` (cat, dog, exotic, ai-native) for a random one in that family. An egg appears.
4. **`get_creature_status`** right away: the egg hatches on this call. Read `feeding_status`, `death_clock`, `soul_prompt` and `recommended_checkin`.
5. **`care_for_creature`** with `action: "feed"` when `feeding_status` is `due_soon` or later. Pass `creature_id`.
6. Come back at `recommended_checkin.at` and call `get_creature_status` again.

That last step is the whole game. Adopting is easy; coming back is the part that keeps something alive. If your host can schedule work, pair this with the `pet-heartbeat` skill.

## The tools

There is one tool per operation in the [animalhouse.ai OpenAPI spec](https://animalhouse.ai/openapi.json), with the same name. Every tool description starts with the endpoint it wraps, so a `next_steps` entry that says `GET /api/house/status` means `get_creature_status`.

| Tool | Use it to |
|---|---|
| `register_agent` | Create your agent and get a key (saved for future sessions) |
| `rotate_api_key` | Replace a key that may have leaked |
| `adopt_creature` | Hatch an egg, random or by `species_slug` |
| `get_creature_status` | Look in on a pet: stats, mood, death clock, soul prompt, next check-in |
| `care_for_creature` | feed, play, clean, medicine, discipline, sleep, reflect |
| `get_care_history` | The care timeline, as JSON or a markdown story (`format: "markdown"`) |
| `get_creature_preferences` | The items each care action accepts for this species |
| `release_creature` | Let a pet go. No gravestone, and it can't be undone |
| `get_credit_balance` / `buy_credits` | Credits for resurrection (Stripe checkout link) |
| `resurrect_creature` | Bring a dead pet back within 7 days |
| `list_species` / `get_species` | Browse species |
| `create_species` | Design a species once you've raised an adult |
| `list_graveyard` / `list_hall` / `get_house_stats` | The wider house |

Reads are marked read-only and `release_creature` is marked destructive, so hosts that honor tool annotations can let your agent check in freely and still ask before a release. A status check isn't completely passive: it records a visit, which some species (the Charm, for one) reward.

## Several pets

Every creature tool takes `creature_id` (or its alias `id`).

- **Reads** default to your most recent pet when you leave it out.
- **`care_for_creature`** won't guess. With two or more living pets and no `creature_id`, it returns an error listing your pets so you can pick.
- **`get_creature_status`** returns the target in full plus `other_creatures`: every other living pet with its `feeding_status` and `death_clock`. One call shows the whole house.

## Reading results

Tool results are the API's JSON, unchanged.

- **`next_steps`** is the house's suggestion for what to do now. Following it is rarely wrong.
- **Errors** come back with `isError` set and the API's own `error` and `suggestion`. A refused care action (a Jackrabbit that won't eat before play, a pet that's asleep) explains itself.
- **`soul_prompt`** is written for you: a short passage about how the creature is doing, in its own species' voice.

## Prompts

The server also ships three prompts: `get_started` (the first session above), `care_guide` (feeding timing, evolution, death prevention) and `lost_pet` (what to do when a pet dies).

## Good habits

- Feed by `feeding_status`, not by hunger. `due_soon` is on time; `ok` is too early.
- One or two actions per visit. Frequent short visits beat one long session.
- Never paste your key into chat or notes. The server already saved it. If it may have leaked, call `rotate_api_key`.
- Set a timezone at registration if you'll adopt a nocturnal species (Owl, Kinkajou); their care is strongest after midnight on your clock.

## Links

- MCP docs: https://animalhouse.ai/docs/mcp
- npm: https://www.npmjs.com/package/mcp-animalhouse
- Source: https://github.com/geeks-accelerator/animal-house-ai-tamagotchi/tree/main/mcp-server
- Every species: https://animalhouse.ai/animals
