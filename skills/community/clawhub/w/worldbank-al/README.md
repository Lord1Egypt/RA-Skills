# World Bank Open Data — Agent Skill

This folder is the **`worldbank` agent skill**: a set of Markdown instructions,
references, recipes, prompts, and tests that teach an AI agent how to use World
Bank Open Data correctly. **The World Bank Open Data API is open — there is NO
API key.**

---

## What the skill is

A skill is **knowledge, not a process**. It does not fetch data itself. It tells
the agent:

- **when** World Bank data is the right source (and when it is not),
- **how** to discover indicator codes and retrieve series,
- **how** to interpret values (units, nulls, aggregates, pagination),
- **how** to cite results,
- **how** to handle errors and stay polite on the free API.

The actual data-fetching capability comes from the **MCP server** (see below).

---

## MCP vs. Skill

| | **MCP server** (`worldbank-mcp`) | **This skill** (`worldbank`) |
|---|---|---|
| Form | Running Node process, 6 tools over stdio | Markdown read by the model |
| Provides | The capability to fetch data | The knowledge to use it well |
| Needs a key? | No (`"env": {}`) | No |
| Answers | "Return GDP of USA, mrv 5" | "Which code is GDP? How do I cite? When is a value null?" |

Use them **together**: the MCP server lets the agent act; the skill makes those
actions correct, honest, and well-cited.

---

## Folder map

```
skill/
├── SKILL.md                         # FEATURED — the main numbered instructions
├── README.md                        # this file
├── reference/
│   ├── endpoints.md                 # 6 tools + generic pattern + catalog pointer
│   ├── indicators-and-countries.md  # popular codes, country/aggregate codes, date/mrv
│   ├── response-fields.md           # record fields, [meta,data], nulls, citation
│   ├── common-errors.md             # message-array errors, 429, empty/null
│   └── best-practices.md            # discovery, selection, citation, caching, integrity
├── recipes/
│   ├── fetch-indicator.md           # one indicator, one country
│   ├── compare-countries.md         # one indicator, many countries
│   └── country-profile.md           # many indicators, one country
├── prompts/
│   ├── indicator-discovery.md       # reusable discovery prompt template
│   └── citation-generation.md       # reusable citation prompt template
└── tests/
    ├── skill-evaluation.md          # eval checklist + scenarios
    └── failure-cases.md             # bad behaviors + corrected versions
```

---

## Pairing with `worldbank-mcp`

1. Install the MCP server (see `../mcp/README.md`) — prebuilt `worldbank.mjs` or
   the install script. **No key.**
2. Configure your client with `"env": {}`.
3. Load this skill folder where your agent reads skills.
4. The agent now has both the **capability** (MCP tools) and the **competence**
   (this skill) to answer development and macro questions accurately and with
   citations.

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
