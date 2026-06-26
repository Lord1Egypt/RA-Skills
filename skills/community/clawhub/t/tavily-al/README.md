# Tavily Web Search Skill

A portable **agent skill** that teaches an AI agent how to use **Tavily** well: when to search the live web, which operation to use, how to design queries, how to evaluate and cite sources, how to handle errors, how to control cost, and how to stay secure against prompt injection.

This package is **instructional knowledge**, not running software.

---

## Skill vs. MCP server — the critical distinction

These are two different things that work together:

- **An MCP server (e.g. `tavily-mcp`) is executable infrastructure.** It is a running process that exposes *tools* the agent can call — `tavily_search`, `tavily_extract`, `tavily_crawl`, `tavily_map`. It holds the `TAVILY_API_KEY`, makes the actual HTTP requests to Tavily, and returns results. It is **how** the agent physically reaches Tavily.

- **This skill is instructional knowledge.** It contains no executable code and makes no network calls. It teaches the agent **when and how** to use Tavily — operation choice, query planning, source evaluation, citation, error handling, cost control, and security. It is **judgment**, not plumbing.

Analogy: the MCP server is the **telephone**; this skill is the **training on who to call, what to ask, how to verify the answer, and how to write it down with sources.**

The skill assumes Tavily is reachable either through MCP tools (`tavily_*`) or through a direct HTTP client against `https://api.tavily.com` using `Authorization: Bearer <TAVILY_API_KEY>`. It does not require the MCP server specifically — any transport that provides equivalent operations works.

## Folder map

```
tavily-skill/
├── SKILL.md          # AUTHORITATIVE. The full agent playbook (read this first).
├── README.md         # This file: what the skill is, skill-vs-MCP, how to load it.
├── CLAUDE.md         # Instructions for an AI agent maintaining this skill.
├── skill.json        # Machine-readable manifest (name, version, ops, safety rules).
├── reference/        # Deep-dive reference docs (elaborate on SKILL.md).
│   ├── endpoints.md          # Each endpoint: purpose, params, response, cost.
│   ├── parameters.md         # All parameters across endpoints + when to change them.
│   ├── response-fields.md    # Every response field + how the agent should use it.
│   ├── common-errors.md      # 401/422/429/timeout/empty + correct reactions.
│   ├── best-practices.md     # Distilled checklist.
│   └── safety-and-security.md# Key safety, untrusted content, prompt injection, robots.
├── examples/         # (Optional) Worked end-to-end agent workflows.
├── recipes/          # (Optional) Reusable task patterns (query + params + handling).
├── prompts/          # (Optional) Reusable prompt fragments for invoking the skill.
└── tests/            # (Optional) Behavioral checks for the skill's guidance.
```

> `examples/`, `recipes/`, `prompts/`, and `tests/` are part of the intended layout. Add content to them following the conventions in `CLAUDE.md`. They may be empty until populated.

## How an agent / host loads this skill

1. **Discovery.** The host (Claude Code, an agent framework, or a custom runtime) registers this directory as a skill and reads `skill.json` for metadata: `name`, `version`, `entrypoint`, `required_environment_variables`, `operations`, `expected_tools`, and `safety_rules`.
2. **Activation.** When a task matches the skill's purpose (web research / lookup / verification / citation), the host loads the `entrypoint` (`SKILL.md`) into the agent's working context so the agent follows its rules.
3. **Tool availability.** The host ensures the `expected_tools` (`tavily_search`, `tavily_extract`, `tavily_crawl`, `tavily_map`) are available — typically by running the `tavily-mcp` server — and that `TAVILY_API_KEY` is set in the environment.
4. **Reference on demand.** The agent consults `reference/*` for parameter/field/error details as needed; `SKILL.md` remains authoritative if anything conflicts.

## How it pairs with the `tavily-mcp` server

- Run/connect the `tavily-mcp` server so its `tavily_*` tools are exposed to the agent.
- Set `TAVILY_API_KEY` in the server's environment (the server injects auth; the agent never handles the raw key).
- Load this skill so the agent uses those tools **correctly** — right operation, lean parameters, source evaluation, citations, error handling, cost control, and prompt-injection safety.
- If the MCP server is unavailable, the same guidance applies to a direct HTTP client against `https://api.tavily.com`.

## Keeping it updated

- Treat `SKILL.md` as the single source of truth; update it first, then align `reference/*`.
- Tavily's API evolves and **crawl/map are beta** — re-verify endpoints, parameters, response fields, limits, and credit costs against the official docs.
- Anything not confirmed must be marked `> Verification needed: confirm with https://docs.tavily.com`.
- Bump `version` in `skill.json` on meaningful changes.
- Never commit real API keys or secrets.
- Official documentation: https://docs.tavily.com
