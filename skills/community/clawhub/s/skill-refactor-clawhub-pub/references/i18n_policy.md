# i18n / Natural-Language Policy

This file is the load-on-demand home for the skill's i18n decisions (mirrors the
design doc §6). The body keeps only the three-state picker (it must survive
compaction); the policy detail, layering rules, and non-Chinese-user checklist
live here.

## 1. The policy that actually fires

ClawHub's scanner (SkillSpector / A.I.G) enforces a **Natural-Language Policy**.
Observed hits on published skills:

| Hit shape | Why it fires | Severity | Sample |
|---|---|---|---|
| frontmatter sets `language: en` (or an equivalent locale lock) with **no nearby note offering a language choice or justifying the locale restriction** | restriction without a choice or stated reason | Low (89%) | `read-it-reframe-it-own-it` |
| all user-facing instructions are a **single language** (e.g. all Chinese) with **no opt-in choice and no clear justification** | language forced without user consent / validity | Medium (92%) | `daily-security-check` |

**Compliant fix — pick one; default to A:**
- **A (default): offer a language choice** — do not lock `language`; expose
  `auto/zh/en` three states (below).
- **B: justify a restriction** — when a region/regulation genuinely pins a locale,
  state it nearby: why it is restricted and how the user exits it.

Conclusion: do **not** write `language: <single value>` in frontmatter without a
reason; do **not** lock user-facing instructions to one language.

## 2. Language layering (which field in which language)

| Location | Language | Why |
|---|---|---|
| frontmatter `description` (trigger text) | **English primary** (Chinese keywords optional) | ClawHub convention: frontmatter `description` is English; English triggers reach non-Chinese users |
| frontmatter `name` / `slug` / `tags` | **English slug** | naming rule `^[a-z0-9]+(-…)$` is naturally English |
| body: hard constraints / criteria / 5-step / routing | **bilingual** (EN + `EN:` or `中文` mirror lines) | serves both; the policy only flags *locking* to one language, not bilingual |
| code examples / commands / paths | as-is | any language fine |
| report artifacts (audit md / changelog) | **follows the user's language** (§3 picker) | user-facing, decided by choice |

## 3. The three-state picker (keep in the body's first ~3000 tokens)

This exact block belongs in the main file (near H9 or as its own section) so the
scanner reads "a language choice is offered":

```markdown
## Language / 语言选择 (Natural-Language Policy: offer a choice)

This skill serves multilingual users; artifact language is decided by three states,
fixed for the whole run (no mid-run switch):

- **auto (default):** follow the language you use with the agent — English in →
  English out; Chinese in → Chinese out; mixed → your dominant language; pure
  code/paths with no natural language → ask "Chinese or English report?"
- **zh:** force Chinese; every artifact Chinese, ignoring the exchange language.
- **en:** force English; every artifact English, ignoring the exchange language.

Priority: your explicit zh/en > inferred auto > ask as a fallback.
(No locale is hard-set, so this is not a "single-language lock". If you must pin a
locale, state the reason and an exit here.)
```

This block is the landing spot for policy "A" (a choice is offered); the last line
covers "B" (a restriction, if any, must be documented with reason + exit). Both
in the body → the scanner no longer flags Natural-Language Policy.

## 4. Non-Chinese-user checklist (beyond language)

| Dimension | Requirement |
|---|---|
| trigger words | `description` English primary includes "optimise/refactor/trim SKILL.md", "body too long", "hard constraints lost", "split into references" |
| paths / commands | forward slashes, relative-path examples; never assume one OS separator |
| default assumptions | when `context`/permission fields are missing, state the inferred default in **both EN and 中文** |
| artifact naming | `skillmd_audit_<name>.md`, changelog headings bilingual |
| failure fallback | the "3-step self-check" is given in English too (spelling / relative path / list dir) |
| numerics | decimal integers for tokens/lines/chars; no full-width digit mixing |

## 5. Acceptance (confirm i18n will not trip)

1. Run `scripts/check_skillmd.py <SKILL.md> --platform clawhub` — expect **no**
   Natural-Language / locale hit (the linter does not check this item; cross-check
   the §1 table by hand).
2. Self-check against the two §1 hit shapes: ① any unjustified `language:` in
   frontmatter? ② is the body locked to one language with no opt-in? Both "no" =
   compliant.
3. Run `skill-publish-gate` (`--platform clawhub`) as a publish preflight; confirm
   no new blocker.
