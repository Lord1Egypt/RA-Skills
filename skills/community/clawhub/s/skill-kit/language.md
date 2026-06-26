# Language — Skill language = SKILL.md frontmatter `description` language (HARD STOP)

**Every skill file (SKILL.md, topic .md, resources/*) is written in the same language as the SKILL.md frontmatter `description` field.** If description is English, all topic and resource files are English; if Korean, all are Korean. No per-Edit publish-target matching needed — the frontmatter description line alone decides.

**`description` field itself must be a single language (HARD STOP)**. English skills allow **zero Korean keywords** in description (including trigger keywords). Korean skills may include English technical terms (Vault, ArgoCD, K3s, etc.) but the main description prose is Korean. No "mixed" exception.

| Skill language (per description first sentence) | description body | description trigger keywords |
|------|------|------|
| English skill | English only | English only (zero Korean keywords) |
| Korean skill | Korean only | Korean primary + English allowed only for proper nouns/technical terms (e.g., "Vault", "ArgoCD") |

## Don't / Do table (description itself)

| # | Don't | Do |
|---|-------|-----|
| A | Add any non-English trigger keyword to an English skill's description (e.g., adding a Korean translation/synonym of an existing English keyword) | Use English-only trigger keywords. Non-English users can still match via the English keywords |
| B | "Adding just one Korean keyword lets Korean users trigger the skill" thinking | The system reminder exposes the full description to English speakers too. Even one Korean keyword breaks description consistency + wastes the truncate budget |
| C | locale-duplicate with "core nouns are OK" (the previous weak lint.md rule) | English skill = zero Korean. Even a core noun applicable to both locales gets one English keyword only |
| D | Korean skill description lists English trigger keywords with equal weight | Korean skills keep Korean keywords as primary. English is restricted to proper nouns/technical terms |

## Don't / Do table (skill body)

| # | Don't | Do |
|---|-------|-----|
| 1 | Match against publish target / LICENSE presence / skill catalog before Edit | Check the SKILL.md first line `description:` language → write in that language |
| 2 | "It's a mixed file, so it's ambiguous" thinking | frontmatter description is the primary criterion. Even if Korean sections exist in the body, the description language is the enforced answer |
| 3 | "Existing Korean is there, so new additions can be Korean too" | If description is English, existing Korean is a mistake. Write new additions in English + queue existing Korean for a separate English conversion task |

## Self-check (every time before editing a skill file)

1. Confirm the description line with `head -5 <SKILL.md>` or `Grep "^description:" <SKILL.md>`
2. description in English → write English. In Korean → write Korean
3. If the body is mixed, the description language is the source of truth (mixed = partial stale signal)
4. **Prior-task language ≠ skill description language — self-check (HARD STOP — prevents recurrence)**: Even if the prior N actions (e.g., posting a Korean PR correction comment / updating a Korean fix_plan / posting a Korean inline review) were all in Korean, if the skill file's description language is English, write in English. "Context inertia" is the most common bypass pattern

## Context inertia trap (HARD STOP)

| # | Don't | Do |
|---|-------|-----|
| 1 | Write the new skill section in the same language as the prior N actions | Re-check the description before any skill Edit → reset every Edit (prior task language is irrelevant) |
| 2 | "PR comment was Korean, fix_plan was Korean, inline review was Korean → skill addition is Korean too" mapping | Per-medium language rules are independent: medium language (PR / fix_plan / inline) is decided separately from skill file language |
| 3 | "Body has one Korean section already, so mixing is fine" rationalization | A Korean section in the body = stale signal. description language is the answer. New additions follow description language |
| 4 | "Just this one section in Korean, will convert to English later" deferral | Write in English at addition time. Deferral = permanent mix + higher cleanup cost |

**Self-check trigger keywords** (re-check description before every skill Edit if any of these apply):

- The prior response wrote/posted Korean text (PR comment, fix_plan entry, inline review body, etc.)
- The prior response wrote/posted English text (GitHub PUBLIC repo issue/PR body, etc.)
- The Edit target file path contains "skills/", `~/.claude/skills/`, or `~/.agents/skills/`
- new_string contains a markdown section (`###`, `####`, `|` table)

## Exceptions

- Korean skill description's **proper nouns / technical terms** (Vault, ArgoCD, K3s, Authentik, etc.) — keep English as-is
- English skill description's **proper nouns / product names** (no Korean transliteration/translation added)
- description must be single-language (mixing deprecated)
- If a description language change is needed, decide separately (per skill publish policy)

## Hook installed

- Script: `~/.claude/skills/hook/resources/block-skill-language-mismatch.sh` (sole source of truth)
- Install location: `~/.claude/hooks/block-skill-language-mismatch.sh` (copy, executable bit set)
- Matchers: `PreToolUse:Edit` and `PreToolUse:Write` in `~/.claude/settings.json`
- Scope: only `.md` files under `*/skills/<name>/`. Code/data files unaffected
- Detection: zero Hangul in SKILL.md `description` → strict mode (any Hangul in new content → DENY exit 2). Hangul in description → permissive (Korean skills may include English technical terms)
- Quote handling: user quotes must be paraphrased into English before pasting into English skill files. The hook does not distinguish quote vs body content
