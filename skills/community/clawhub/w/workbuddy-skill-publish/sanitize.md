
**Run this BEFORE any publish.** Public skills are permanent.

## Release Type Gate (run first)

Before starting, classify the release — the pipeline strictness differs:

| Type | Definition | Required stages |
|---|---|---|
| **New skill publish** | Slug not yet on ClawHub | **Full 5 stages**: Understand → Transform → Sanitize → Verify (user approval message) → Publish + Install-check |
| **Content update** | New references / new sections / scope change | Sanitize → Verify (user approval) → Publish |
| **Patch (wording / metadata)** | Description tweak, frontmatter fix, version bump only | Sanitize → Publish (user approval is still required — show the diff or content before publishing) |

**New-skill extra checks (mandatory):**
1. `clawhub inspect <slug>` — must return "Skill not found" (not AMBIGUOUS) before publish. A slug collision creates an unfixable ghost record.
2. Structure completeness per skill-design-guide: Hard Rules, Failure Handling, Output Format, steps tagged `[Deterministic]`/`[LLM]`.
3. Optional discoverability add-on: a Chinese summary + trigger keywords can be appended to the description (skillhub search indexes description only, not description_zh). This broadens public search visibility beyond what the user may expect — ask the user and proceed only after explicit consent. Never add these by default.

**Frozen skills (do not update unless necessary):**
- `social-persona-profiling` — any update risks re-triggering SkillSpector alerts (its third-party-profiling capability sits on the policy line). If an update is unavoidable, keep frontmatter minimal and change body only.

## Personal Data

Remove or genericize:
- [ ] Names (your name, team members, company)
- [ ] Email addresses
- [ ] Usernames, handles, IDs
- [ ] Phone numbers
- [ ] Addresses, locations
- [ ] URLs to private resources
- [ ] Internal project names
- [ ] Client/customer references

## Credentials & Secrets

**NEVER include:**
- [ ] API keys, tokens, passwords
- [ ] Environment variable VALUES (names are ok)
- [ ] Private URLs with auth params
- [ ] Database connection strings
- [ ] SSH keys, certificates

## Model-Specific References

Remove references to specific models that won't apply to all users:
- [ ] "Claude" → "the agent" or "the model"
- [ ] "GPT" → generic term
- [ ] Specific model versions
- [ ] Provider-specific features

## Internal References

Remove:
- [ ] References to your specific file paths
- [ ] Your workspace structure
- [ ] Your tool configurations
- [ ] Internal documentation links
- [ ] Team-specific workflows

## Dangerous Patterns

Check for:
- [ ] Commands that could damage systems
- [ ] Patterns that encourage unsafe behavior
- [ ] Hardcoded paths that won't work elsewhere
- [ ] Assumptions about user's environment

## Genericize Examples

Replace specific with generic:
- `~/my-company/project` → `~/projects/example`
- `john@company.com` → `user@example.com`
- `api.mycompany.com` → `api.example.com`
- Internal tool names → generic descriptions

## Final Check

Before publishing, read entire skill asking:
- "Would I be comfortable if this were public forever?"
- "Could this expose anything about me/my company?"
- "Would this work for someone with zero context about me?"

## If Unsure

**Ask the user:**
> "I found [X] which might be personal/internal. Should I remove, genericize, or keep it?"

Better to ask than to publish something private.

## Post-publish Finding Diagnosis (if SkillSpector or similar scanner reports findings)

When a security/policy scanner reports findings AFTER publish, diagnose the finding's layer before fixing. **Do not reflexively add disclaimers or narrow triggers — that often makes things worse.**

### Step 1: Read the "Finding" text

Findings quote specific lines. Identify what the scanner actually objects to:
- Is it quoting **frontmatter** (trigger keywords, description text)? → L1
- Is it quoting **body steps** but the issue is wording mismatch with description? → L2
- Is it quoting **body steps** and the issue is the capability itself (e.g. "actionable interpersonal advice", "third-party profiling", "consequential decision automation")? → L3

### Step 2: Match to layer

| Layer | Signal | Fix approach |
|---|---|---|
| **L1 Surface** | Finding quotes frontmatter trigger keywords or description phrasing | Narrow trigger words, add data preconditions, move hidden-style content to separate fields |
| **L2 Behavior mismatch** | Finding quotes body steps, but the root cause is description saying one thing while body does another | Align description to match actual body behavior (or change body to match description) |
| **L3 Scope** | Finding quotes body steps and the issue is the skill's core capability itself | This is a design decision, not a wording fix. Ask the user: keep the capability and accept the finding, or restructure the skill's scope? |

### Step 3: Anti-patterns

- **Do not add "NOT a decision-support system" disclaimers to fix L3 findings.** The scanner reads the body, not just the disclaimer. If the body provides actionable guidance, a disclaimer creates a *new* mismatch (L2).
- **Do not reflexively narrow trigger keywords for L2/L3 findings.** Narrow triggers only fixes L1. If the finding quotes body steps, trigger wording is not the issue.
- **Do not bump versions repeatedly trying to fix the same finding.** If the same finding persists after 2 patch attempts, the issue is L3 (scope), not L1 (wording). Stop and escalate to the user with the scope-level tradeoff.

### Step 4: When to stop fixing

If ClawHub moderation shows `CLEAN` but SkillSpector (or similar third-party scanner) still reports findings, **the skill is already live and installable**. SkillSpector findings are informational — they do not block ClawHub moderation. Ask the user whether to:
1. Accept the findings (skill is live, moderation is CLEAN)
2. Continue fixing (only worthwhile if findings indicate real risk to users)

### Step 5: Rollback strategy (when fixes make things worse)

If 2+ patch attempts have been made and findings are **increasing**, stop and reassess: the last edits may have made behavior worse, but a lower finding count is **not** the goal — demonstrated risk reduction is. Re-read each new finding on its own merits and classify it as a genuine risk or a false positive with evidence.

**Revision procedure:**
1. Diagnose each finding by layer (Steps 1–3 above) and decide, with written evidence, whether the underlying behavior is actually unsafe. Never remove a field just because it triggered a finding.
2. **Preserve accurate capability disclosures and necessary usage restrictions** — `not_for`, `read_when`, scope limits, and safety-related metadata stay unless they are factually wrong. Removing them to shorten the scanner's surface is not remediation; it hides real constraints from reviewers.
3. Fix unsafe **behavior** directly, or if a finding is a false positive, document why with evidence rather than deleting the disclosure.
4. Publish as a new version with a changelog that names each finding, its classification, and the evidence for any false-positive determination.

**Key insight:** A minimal frontmatter is fine, but stripping accurate restrictions to make a scanner quiet trades a finding for a real safety gap. Pass again by fixing behavior and documenting evidence, not by deleting safety metadata.

**Real example (social-persona-profiling):**
- 1.0.4: passed SkillSpector (no findings)
- 1.0.5-1.0.10: added trigger keywords, read_when, not_for, disclaimers, Chinese triggers → findings **increased** to 10+
- 1.0.11: rolled back frontmatter to 1.0.4 original + retained 1.0.8 body scope fix → **passed**
