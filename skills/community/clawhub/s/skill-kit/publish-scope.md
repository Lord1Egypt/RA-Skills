# Publish-Scope — scope review before extending published skills (HARD STOP)

**Before adding a new topic, script, or feature to a published skill (`~/.claude/skills/es6kr/data/published.json` registered + git tracked), review whether the addition's scope falls within the general-use range of that skill.** Narrow-scope (specific infrastructure / specific model / specific environment) features must not be added to a published skill — separate them into a local-only skill or a new independent skill.

## Why

- Published skills are distributed to general users via `clawhub publish` / `context7 install` — adding a dependency absent in the user's environment (a specific RAG instance, a specific internal host, a specific external API key) produces meaningless noise for users and consumes the 1024-character description budget
- `skill-kit/upgrade.md` Step 5.5 performs scope **classification** (published vs. local-only) **immediately before commit**. The **pre-addition** scope **review** is a separate up-front gate that avoids the cost of reverting work after the fact

## Criteria for narrow scope

A feature has **narrow scope** (unsuitable for publishing) if any of the following apply:

| # | Criterion | Examples |
|---|-----------|---------|
| 1 | Tied to a specific host / IP / domain | Internal IP, internal domain, specific cluster alias |
| 2 | Tied to a specific external service instance / account | Specific organization, specific workspace |
| 3 | Requires a specific ML model / version | Specific embedding model ID hardcoded |
| 4 | Tied to a specific infrastructure tool / MCP instance | Specific MCP server + specific collection name |
| 5 | Troubleshooting procedure specific to one environment's debugging session | Procedure specialized for "error Y occurring in environment X" |
| 6 | Examples / Don't-Do / self-check body contains real user identifiers (GitHub login, full name, company name, email, employee ID, IP owner name, etc.) | Replace with placeholders: `@reviewer-login`, `@octocat`, `<reviewer-login>`, etc. |

## Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Add a topic tied to internal hosts or specific infrastructure to a published skill | If narrow scope, separate into a local-only skill. Add only generalized-domain topics to published skills |
| 2 | Think "it's related to this skill, so just add one topic" | Run the six-criterion self-check to confirm it can be generalized → separate if even one criterion matches |
| 3 | Add narrow-scope trigger keywords (specific hostname, specific ML model name) to a published skill | Allocate description budget only to keywords meaningful to general users |
| 4 | Write a narrow-scope topic, then discover the scope problem during the commit-time classification step → revert | Use the criteria self-check in this topic **before adding** to block the problem up front |
| 5 | Assume "users will ignore it on their own" | Users of published skills infer meaning solely from the description and Topics table. Internal-dependency topics only cause confusion |

## Procedure

1. **Entry trigger** — when starting to add a new topic, script, or feature to a published skill
2. **Confirm published status**:
   ```bash
   jq -r --arg slug "<skill-name>" '.skills[] | select(.slug == $slug or .local == $slug) | .slug' \
     ~/.claude/skills/es6kr/data/published.json
   ```
   - Result found = published → this rule applies
   - No result = local-only → this rule does not apply (add freely)
3. **Scope self-check** (six criteria above):
   - Any criterion matches → forbidden to add to published skill; must be separated
   - No criterion matches → can be generalized; OK to add to published skill
4. **Decide on a separation alternative** (if one or more criteria match):
   - If an existing local-only skill covers the domain, add it there
   - Otherwise, create a new local-only skill (`~/.claude/skills/<new-slug>/`, not registered in `published.json`, kept untracked)
5. **User confirmation** — if the self-check result is ambiguous, ask via AskUserQuestion: "add to `{published-skill}` vs. separate into `{local-only-skill}` vs. create a new skill"

## Exceptions

- The user has explicitly instructed "add to the published skill" (report the self-check result first, then defer to the user's decision)
- The narrow-scope item appears only as an **example/case study** within the topic body, and the topic itself describes a generalized procedure

## Related

- `skill-kit/upgrade.md` Step 5.5 — scope classification immediately before commit (this topic = pre-addition review)
- `skill-kit/portability.md` — vendor-specific reference forbidden in shared skills
