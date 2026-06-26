# Portability — ensuring portability of public/published skills (HARD STOP)

Published skill bodies (`clawhub publish` / `context7 install` / plugin marketplace) must not embed **user-private global rule cross-refs** or **vendor-specific instance references** directly. Dependencies absent on the target machine become dead references, and the skill stops working in other environments.

## Rule A — Global rule cross-ref forbidden

In public/published skill topics and SKILL.md bodies, **cross-referencing user-private global rules such as `~/.agents/rules/*.md` is forbidden**. A published skill runs on machines where the user's private global rules do not exist, so any global rule reference becomes a dead reference.

This rule refines the general "layer structure" table in `common.md` at the **distribution boundary**: local-only skills may reference global rules, but published public skills must resolve all references within their own distribution unit (plugin).

### Reference permission matrix

| Referencing party | Reference target | Allowed? |
|------------------|-----------------|----------|
| Local-only skill (not published) | `~/.agents/rules/*.md` global rule | ✅ (guaranteed to exist on local machine) |
| **Public/published skill** | **`~/.agents/rules/*.md` global rule** | ❌ **Forbidden (absent on target machine → dead ref)** |
| Skill within the same plugin | Rules bundled in the same plugin | ✅ (same distribution unit — resolve guaranteed) |
| Public skill | Rules/skills in a different plugin or external distribution unit | ❌ Forbidden (outside distribution unit) |

### If a cross-ref is truly necessary → bundle as a plugin

If a public skill genuinely needs to reference a rule, bundle that rule inside the same plugin so the distribution unit matches. Only intra-plugin rules↔skills cross-refs remain resolvable after deployment. If plugin bundling is not feasible, inline the referenced content as self-contained prose in the skill body.

| # | Don't | Do |
|---|-------|-----|
| 1 | Write `~/.agents/rules/<file>.md "..." reference` in a public skill body | (a) Inline the referenced content as self-contained prose in the skill body, or (b) bundle the rule in the same plugin and reference it by its intra-plugin path |
| 2 | Treat an existing public skill → global rule cross-ref as "a dependency to maintain" | It is an anti-pattern and a **removal target**. Removing it is not a cost — it is a publishability cleanup |
| 3 | Frame "N cross-ref locations need updating" as a downside/cost in a decompose/refactor option | Cross-ref removal = publishability improvement (the goal). State it as a benefit, not a cost, in option descriptions |
| 4 | Keep the global rule in place and reference it from the public skill when a reference is needed | Bundle rule + skill in the same plugin → convert to intra-plugin reference |

### Self-check (before every Edit of a public skill topic or SKILL.md)

1. Is the skill being edited public/published? (`published.json` registered or targeting a plugin marketplace)
2. Does the new or existing body contain a reference to `~/.agents/rules/*.md` or `.claude/rules/*.md` of a different distribution unit?
3. If yes → (a) self-contained inline or (b) convert to intra-plugin reference after bundling the rule in the same plugin
4. "Keep the reference" is not an option — it is a dead ref on the target machine and must always be removed, inlined, or bundled

### Exceptions

- Local-only skills (not published, not registered in `published.json`): global rule references are allowed
- Intra-plugin rules↔skills cross-refs: allowed (same distribution unit)
- A rule file that is bundled inside the plugin and deployed together: intra-plugin path reference is allowed

## Rule B — No vendor-specific hardcoding in generic (shared) skills

Generic skill topic bodies must not **hardcode specific vendor instances (URLs, internal IPs, specific MCP server names, specific vendor-skill calls)**. A generic skill **declares only an abstract dispatch interface** and delegates implementation to vendor-specific skills.

This rule operates on a different axis from Rule A: A prevents dead references at distribution time; B ensures the skill works across diverse environments.

### Criteria for generic vs. vendor-specific

| Skill category | This rule applies? |
|---------------|-------------------|
| Generic (shared) — general behavior, multi-environment | ✅ Applies |
| Vendor-specific (scoped to a particular use case) — the author is the vendor implementor | ❌ Does not apply |

**Definition of generic**: a skill is generic if at least one of the following is true:
- The description describes general behavior without naming a specific tool, domain, or environment
- Any user can invoke it regardless of environment (no dependency on a specific internal cluster or account)
- Other generic skills list it under `depends-on` or call it

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Hardcode internal URLs/IPs directly in a generic skill topic body | Declare only an abstract dispatch flag (`--rag=<skill>:<topic>`). Keep URLs inside the vendor skill |
| 2 | Explicitly call a vendor skill from a generic skill (e.g., `Skill("<vendor>", "...")`) | Accept it as a call-site parameter (e.g., `--rag=<skill>:<topic>` — the caller specifies the vendor) |
| 3 | Add a vendor-specific verification procedure to a generic skill | Declare only the abstract contract (let the receiver own its healthcheck); put actual verification in the vendor skill |
| 4 | "Write vendor-specific code inside the generic skill and have the vendor call it" | Reverse the direction: the generic skill declares the interface, the vendor skill implements the receiver. Coupling belongs only in the call-site flag |
| 5 | Write a new implementation in the generic skill when an existing dispatch pattern already exists in a vendor skill | Grep for existing dispatch patterns before editing — if found, follow that pattern |

### Trigger points — all generic skill body changes

| Point in time | Self-check required? | Notes |
|--------------|---------------------|-------|
| Before invoking Edit / Write tool | ✅ Mandatory | Writing new content |
| Importing a generic skill file from another worktree/branch | ✅ Mandatory | Import = decision point for introducing new content |
| Baseline copy commit | ✅ Mandatory | "Baseline = exempt" exemption is forbidden |
| Copy-pasting text from another generic skill | ✅ Mandatory | Regardless of source, self-check is required at the destination |
| Auto-generated files | ✅ Mandatory | Self-check immediately after generation |

### Self-check (before every Edit/Write or import of a generic skill)

1. **Is the skill being edited generic?** — Check against the criteria above. If yes, this rule applies.
2. **Does the content being added contain any of the following patterns?**
   - Internal hostname / IP / domain
   - A specific vendor skill name (`Skill("<vendor>", ...)`)
   - A specific MCP server (`mcp__<vendor>__*`)
   - A specific external service instance (specific API endpoint, specific collection name)
3. **If yes, immediately convert to an abstraction**:
   - Vendor reference → call-site parameter (`--<verb>=<skill>:<topic>` abstract flag)
   - Verification procedure → delegate to the vendor receiver
   - URL/host → abstract as an environment-variable contract
4. **Check whether an existing dispatch design exists in the vendor skill** → if so, follow that pattern and expose only the contract on the generic side

### Dispatch pattern standard

Recommended pattern when a generic skill exposes an external service integration:

```text
<generic-command> ... --<verb>=<skill>:<topic>
```

- `<verb>` — action category (rag, sync, notify, export, etc.)
- `<skill>:<topic>` — caller-specified vendor designation
- If omitted, skip dispatch (default behavior only)

The call-site knows the vendor skill name, so the generic skill has no need to enumerate vendors.

### Extension to author-facing media

This rule applies not only to the generic skill body text itself but also to **all author-facing media used when presenting work on a generic skill to the user**:

| Author-facing medium | This rule applies? |
|---------------------|-------------------|
| Chat response text (plans/suggestions/recommendations) | ✅ |
| `AskUserQuestion` question / option label / description | ✅ |
| `TodoWrite` / `TaskCreate` subject/description | ✅ |
| Plan/research artifacts (`.md`) | ✅ |
| Abstract contract flag (`--<verb>=<skill>:<topic>`) citations | ❌ (abstract contract — not vendor-dependent) |
| Case history body (failed-attempts, etc.) | ❌ (preserve vendor names for recurrence verification) |

#### Don't / Do (Author-facing)

| # | Don't | Do |
|---|-------|-----|
| 1 | Recommend "add a specific-vendor-tool-first rule to fix.md" | Recommend by abstract behavior name ("semantic search first"). The caller decides the concrete tool |
| 2 | Use a vendor product name directly in an AskUserQuestion option label | Write option labels using abstract behavior names |
| 3 | Say "must store to a specific vendor" in a chat response | Say "must store to the RAG receiver" or "store using the available store tool" |
| 4 | Present a specific backend name as a user option | Use abstract terminology. Environment-registered tools determine the vendor choice |

### Exceptions

- Vendor names may be cited in **examples/case studies** within the skill body (SKILL.md / topic `.md` prose, NOT inside `AskUserQuestion` option descriptions — Rule B still forbids those)
- The generic skill itself implements **meta-dispatch auto-detection**
- The user explicitly requests a vendor comparison/selection (user intent takes first priority)

## Related

- `skill-kit/publish-scope.md` — scope review before extending published skills
- `skill-kit/upgrade.md` — apply this rule when adding topics
- Violation case details: cleanup/data/failed-attempts.md "vendor-specific reference in shared skill" keyword entries
