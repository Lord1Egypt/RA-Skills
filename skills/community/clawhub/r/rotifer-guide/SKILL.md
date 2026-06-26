---
name: rotifer-guide
description: >-
  Unified user-facing entry point for Rotifer Protocol: interactive onboarding, natural-language
  scaffolding, diagnostics, ecosystem search, and fidelity upgrade.
  Use when the user mentions "how to use Rotifer", "getting started", "tutorial", "beginner",
  "create gene", "make a", "init", "score is 0", "publish failed", "diagnose", "check",
  "find a gene", "recommend", "search", "upgrade", "Wrapped to Native", "fidelity", "evolve".
---

# Rotifer Guide — User Entry Point

> This Skill handles intent recognition and workflow routing. Deep technical details are delegated to specialized Skills.

## Prerequisites

Before using this Skill, ensure the Rotifer CLI is available:

```bash
npx @rotifer/playground --version
```

If you prefer MCP integration instead of CLI, add this to your MCP config:

```json
{
  "mcpServers": {
    "rotifer": {
      "command": "npx",
      "args": ["@rotifer/mcp-server"]
    }
  }
}
```

No version pinning needed — both packages resolve to the latest release automatically.

---

## Intent Router

| User signal | Sub-capability | Action |
|-------------|---------------|--------|
| How to / getting started / tutorial / beginner / what is a Gene | **onboarding** | Interactive walkthrough |
| Create / make a XX / new / init / I want a | **scaffold** | Natural-language scaffolding |
| Score is 0 / publish failed / something's wrong / why / diagnose / check | **doctor** | Diagnostics & repair |
| Any gene for / recommend / search / find one that does XX | **explorer** | Ecosystem search |
| Upgrade / Wrapped to Native / fidelity / evolve / rewrite | **upgrade** | Fidelity evolution |

When intent is unclear, list all five sub-capabilities and let the user choose.

## Related Skills

| Skill | Relationship | When to route |
|-------|-------------|---------------|
| `gene-dev/SKILL.md` | Deep technical manual for scaffold / onboarding | User needs full development workflow details |
| `gene-migration/SKILL.md` | Deep migration manual for upgrade | After user confirms migration plan |
| `rotifer-arena/SKILL.md` | Comparison & evaluation entry | User wants to compare Genes / run Arena |
| `genome/SKILL.md` | Gene composition | User wants to combine multiple Genes into an Agent |

---

## 1. onboarding — Interactive Walkthrough

### Phase 1: Environment Check

```bash
cd rotifer-playground
node dist/index.js --version
node dist/index.js list
```

If not installed, guide: `git clone` → `npm install` → `npm run build`.

### Phase 2: Core Concepts

| Concept | One-liner | Analogy |
|---------|-----------|---------|
| Gene | Self-contained logic unit: `express(input) → output` | Function |
| Fidelity | Native > Hybrid > Wrapped — higher = more secure | Compiler optimization level |
| Arena | Genes compete for ranking via F(g) fitness score | Leaderboard |
| Domain | Two-level category like `content.grammar` | Namespace |
| phenotype.json | Gene metadata | package.json |
| R(g) / V(g) | Reputation score / Security score | Credit rating |

### Phase 3: Hands-on Experience

Walk the user through a Gene's complete lifecycle:

```bash
rotifer init hello-world --domain content.greeting --fidelity Wrapped
rotifer test hello-world
rotifer compile hello-world
rotifer arena submit hello-world
rotifer arena list --domain content.greeting
```

After each step, explain the output and confirm the user understands before proceeding.

### Phase 4: Next Steps

Recommend based on user background:
- Has an existing SKILL.md → scaffold (`rotifer wrap`)
- Wants to browse the ecosystem → explorer
- Wants to dive deeper → route to `gene-dev/SKILL.md`

---

## 2. scaffold — Natural-Language Scaffolding

### Phase 1: Intent Extraction

Extract from the user's natural-language description:

| Parameter | Extraction method | Default |
|-----------|------------------|---------|
| name | Generate kebab-case from description | Must confirm |
| domain | Infer two-level domain from functionality | Must confirm |
| fidelity | Needs external API → Hybrid, pure computation → Native, quick prototype → Wrapped | Wrapped |

### Phase 2: Confirm Parameters

Present inferred results to the user, wait for confirmation before executing.

### Phase 3: Scaffold Generation

**From scratch:**

```bash
rotifer init <name> --domain <domain> --fidelity <fidelity>
```

**From an existing SKILL.md:**

```bash
rotifer scan --skills
rotifer wrap <name> --from-skill <path>
```

**From ClawHub:**

```bash
rotifer wrap <name> --from-clawhub <slug>
```

### Phase 4: Verification

```bash
rotifer test <name>
rotifer compile <name>
```

After compilation passes, prompt: publish to Cloud (`rotifer publish`) or submit to Arena (`rotifer arena submit`).

For deeper development details (inputSchema design, express function implementation) → route to `gene-dev/SKILL.md`.

---

## 3. doctor — Diagnostics & Repair

### Decision Tree

```text
User reports a problem
 |
 +-- F(g) = 0 or abnormally low score
 |   +-- Does rotifer test <name> pass?
 |   |   +-- Fails → Check if express() return value matches outputSchema
 |   |   +-- Passes → Check if phenotype.json domain is reasonable
 |   +-- Are there competitors in the same domain?
 |       +-- Yes → Analyze competitor strengths, suggest optimizations
 |
 +-- Publish failed
 |   +-- Does rotifer compile <name> succeed?
 |   |   +-- Fails → Check for syntax errors, missing dependencies
 |   |   +-- Succeeds → Check network connection, Cloud credentials
 |   +-- Is phenotype.json format valid?
 |
 +-- Compilation failed
 |   +-- Check the exported express function signature in index.ts
 |   +-- Check inputSchema / outputSchema in phenotype.json
 |   +-- Check if fidelity declaration matches actual code
 |       +-- Declared Native but has fetch calls → Change to Hybrid or remove network calls
 |
 +-- Runtime error
     +-- rotifer test <name> --verbose
     +-- Check if input conforms to inputSchema
     +-- Check if express() handles edge cases correctly
```

### Common Diagnostic Commands

```bash
rotifer test <name>
rotifer list
rotifer arena list --domain <domain>
```

### Quick Reference

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| F(g) = 0 | express() returns empty or format mismatch | Fix return value to match outputSchema |
| Compilation failed | TypeScript type error | Check express function signature |
| Publish timeout | Cloud credentials expired | Refresh Cloud credentials |
| Arena ranking dropped | Stronger competitor appeared in same domain | Optimize algorithm or upgrade fidelity |
| Fidelity mismatch | Native declared but has fetch calls | Remove network calls or change declaration to Hybrid |

---

## 4. explorer — Ecosystem Search

### Phase 1: Understand the Need

Extract from user description: functionality keywords, target domain, fidelity preference.

### Phase 2: Search

```bash
rotifer arena list
rotifer arena list --domain <domain>
rotifer list
```

### Phase 3: Result Analysis

Display search results in a table:

| Field | Description |
|-------|-------------|
| name | Gene name |
| domain | Category |
| fidelity | Native / Hybrid / Wrapped |
| F(g) | Fitness score |
| R(g) | Reputation score |

### Phase 4: Recommendation

- Found a matching Gene → suggest install: `rotifer install <name>`
- Found a partial match → suggest fork and modify, or submit an Arena challenge (route to `rotifer-arena/SKILL.md`)
- Nothing found → suggest creating a new Gene (route to scaffold)

---

## 5. upgrade — Fidelity Evolution

### Phase 1: Assess Current State

```bash
rotifer list
```

Check the target Gene's phenotype.json — confirm current fidelity and express() implementation.

### Phase 2: Migration Path Decision

| Current | Target | Condition | Path |
|---------|--------|-----------|------|
| Wrapped | Native | Functionality can be implemented as pure computation | Rewrite express(), remove all external calls |
| Wrapped | Hybrid | Must call external APIs | Add WASM shell + allowedDomains whitelist |
| Hybrid | Native | Can internalize API dependencies | Replace API calls with local algorithms |

### Phase 3: Execute Migration

After confirming the migration plan, route to `gene-migration/SKILL.md` for the full migration workflow.

### Phase 4: Verification

```bash
rotifer test <name>
rotifer compile <name>
rotifer arena submit <name>
```

Compare F(g) scores before and after migration to confirm ranking continuity.
