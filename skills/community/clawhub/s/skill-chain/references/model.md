# SkillChain Ontology Model

Full type definitions, relation semantics, and constraint rationale for the SkillChain knowledge graph.

---

## Overview

The graph has four node types and six edge types. Everything revolves around the `Skill` entity; the other types exist to describe its supply chain.

```
SkillCategory ◄─ belongs_to_category ─ Skill ─ uses_tool ──────► Tool
                                         │                          │
                                         │ requires_package         │ backed_by_package
                                         ▼                          ▼
                                   SoftwarePackage ◄────────── SoftwarePackage
                                         
                        Skill ─ depends_on_skill ──► Skill
```

---

## Types

### Skill

The central entity. One instance per discovered skill directory.

| Property | Type | Required | Source |
|----------|------|----------|--------|
| `slug` | string | — | `_meta.json`, `.clawhub/origin.json`, or dirname |
| `name` | string | **yes** | SKILL.md frontmatter `name:` |
| `description` | string | — | SKILL.md frontmatter `description:` (truncated to 500 chars) |
| `source` | enum | **yes** | `clawhub` if registry metadata exists, else `local` |
| `status` | enum | — | defaults to `active` |
| `version` | string | — | `_meta.json` or `.clawhub/origin.json` |
| `license` | string | — | SKILL.md frontmatter `license:` |
| `local_path` | string | — | absolute path to skill directory |
| `last_scanned` | ISO datetime | — | set by ingest on each scan |
| `stars` | int | — | clawhub API (enrich only) |
| `downloads` | int | — | clawhub API (enrich only) |
| `installs_current` | int | — | clawhub API (enrich only) |
| `owner_handle` | string | — | clawhub API (enrich only) |
| `moderation` | enum | — | clawhub API (enrich only) |

**`source` enum:** `clawhub` · `local` · `github` · `system` · `other`

**`status` enum:** `active` · `deprecated` · `experimental` · `unknown`

**`moderation` enum:** `safe` · `suspicious` · `blocked` · `unreviewed`

---

### SkillCategory

A functional grouping inferred from keyword analysis of skill names and descriptions. Not manually curated — auto-assigned during ingest.

| Property | Type | Required |
|----------|------|----------|
| `name` | string | **yes** |
| `description` | string | — |

**Built-in categories** (keyword-driven):

| Category | Representative keywords |
|----------|------------------------|
| `crypto-finance` | crypto, trading, exchange, market, blockchain |
| `media-creation` | video, audio, image, music, diagram, slide |
| `communication` | email, wechat, slack, telegram, gmail |
| `data-analysis` | data, report, dashboard, sql, spreadsheet |
| `web-automation` | browser, playwright, scraper, search |
| `productivity` | memory, task, note, calendar, knowledge |
| `development` | code, github, docker, mcp, api, debug |
| `ai-models` | llm, gemini, qwen, gpt, openai, siliconflow |
| `automation` | bot, workflow, recipe, rpa, pipeline |
| `research` | research, medical, scientific, ncbi, paper |
| `iot-hardware` | device, iot, camera, sensor, hardware |
| `security` | security, antivirus, auth, credential, encrypt |
| `uncategorized` | fallback when no keywords match |

---

### Tool

A runtime capability used by a skill: an MCP server, a CLI program, a Python helper script bundle, a browser automation engine, etc.

| Property | Type | Required |
|----------|------|----------|
| `name` | string | **yes** |
| `kind` | enum | **yes** |
| `description` | string | — |
| `provider` | string | — |

**`kind` enum:** `mcp` · `cli` · `python_script` · `playwright` · `http_api` · `db` · `filesystem` · `other`

Tools are detected from SKILL.md content by pattern matching (e.g. mention of "playwright", "mcp server", "ffmpeg") and from the presence of a `scripts/` directory in the skill.

---

### SoftwarePackage

A versioned software artifact declared as a dependency: a PyPI package, an npm module, etc.

| Property | Type | Required |
|----------|------|----------|
| `name` | string | **yes** |
| `ecosystem` | enum | **yes** |
| `spec` | string | — | full requirement spec, e.g. `patchright==1.55.2` |
| `version` | string | — | extracted version if pinned |

**`ecosystem` enum:** `pypi` · `npm` · `system` · `other`

Packages are extracted directly from `requirements.txt` (Python) and `package.json` (Node). All subdirectory requirement files are also scanned.

---

## Relations

### `belongs_to_category`  `Skill → SkillCategory`

Cardinality: **many-to-many** (a skill can belong to multiple categories).

Auto-assigned during ingest via keyword matching. A skill with no matching keywords gets the `uncategorized` category.

---

### `subcategory_of`  `SkillCategory → SkillCategory`

Cardinality: **many-to-one**.  
Constraint: **acyclic** (enforced by validate).

Reserved for future manual hierarchy (e.g. `crypto-defi` is a subcategory of `crypto-finance`). Not auto-populated.

---

### `depends_on_skill`  `Skill → Skill`

Cardinality: **many-to-many**.  
Constraint: **cycles detected and reported**, not blocked.

Inferred by searching a skill's SKILL.md text for references to the slug or name of any other skill in the graph. This is heuristic — a false positive is possible if a skill slug is a common word. Manual curation may be needed.

This is the most analysis-rich relation: it lets you compute skill dependency depth, find "central" skills (high in/out degree), and detect circular dependencies that may indicate design issues.

---

### `uses_tool`  `Skill → Tool`

Cardinality: **many-to-many**.

Detected from SKILL.md via pattern matching. Expresses that a skill invokes this tool at runtime.

---

### `requires_package`  `Skill → SoftwarePackage`

Cardinality: **many-to-many**.

Parsed directly from `requirements.txt` / `package.json`. This is the primary software supply chain edge: it tells you what third-party code a skill depends on.

---

### `backed_by_package`  `Tool → SoftwarePackage`

Cardinality: **many-to-many**.

Expresses that a Tool is implemented by a SoftwarePackage (e.g. the `playwright` Tool is backed by the `patchright` PyPI package). Not auto-populated — populated manually or via future deep analysis of scripts.

---

## Constraints

| Constraint | Enforcement | Rationale |
|------------|-------------|-----------|
| `Skill.name` required | validate | Every skill must be identifiable |
| `Skill.source` enum | validate | Prevents free-text source values |
| `Skill.moderation` enum | validate | Normalizes security verdict vocabulary |
| `SoftwarePackage.ecosystem` enum | validate | Consistent package ecosystem labels |
| `subcategory_of` acyclic | validate | Category hierarchy must be a DAG |
| `depends_on_skill` cycle detection | analyze | Reported, not blocked — circular deps are data |

**On purposeful leniency:** `depends_on_skill` is not forced acyclic because a cycle may be a real finding worth surfacing (e.g. two skills that reference each other in integration patterns). The `analyze stats` and `analyze report` commands flag cycles explicitly.

---

## Storage

- Graph: `memory/skillchain/graph.jsonl` — append-only JSONL op log
- Schema: `schema/skillchain.yaml` — machine-readable constraint definitions
- Format: identical to the `ontology` skill; `scripts/ontology.py` from that skill is reused for low-level ops when available, with a self-contained fallback otherwise.

## Analysis Queries

| Question | Command |
|----------|---------|
| How many skills, categories, packages? | `analyze stats` |
| Which categories have the most skills? | `analyze categories` |
| What are the most popular skills? | `analyze top --by stars` |
| What does skill X depend on? | `analyze supply-chain --skill X` |
| Which skills use package patchright? | `analyze find-users --package patchright` |
| What packages are most widely used? | `analyze packages --top 20` |
| Full snapshot report | `analyze report --out report.md` |
