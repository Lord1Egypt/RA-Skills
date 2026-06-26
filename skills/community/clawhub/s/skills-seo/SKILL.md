---
name: skill-seo
description: Analyze and optimize a skill for discoverability on ClawHub, skills.sh, and similar skill directories. Use when you need to improve naming, slug choice, SKILL.md descriptions, query coverage, examples, listing conversion, or search visibility before publication, while keeping the skill broadly compatible with OpenClaw, Claude Code, Codex, and Cursor.
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["python3"] } } }
---

Audit and improve the target skill for discovery, search recall, and click-through across skill directories.

Prioritize ClawHub and skills.sh. Treat OpenClaw, Claude Code, Codex, and Cursor as compatibility constraints, not primary optimization surfaces.

## Quick Start

Use this workflow when you need a fast audit before publication:

1. Run `python3 {baseDir}/scripts/analyze_skill_seo.py <skill-path>`.
2. Read the target skill's `name`, `description`, first screen, and example prompts.
3. Check whether the skill is easy to understand on a listing page in under 10 seconds.
4. Rewrite the highest-impact metadata and first-screen copy first.
5. Re-run the analyzer and compare the result against the baseline.

## When to Use This Skill

Use this skill when the goal is to make a skill easier to discover, understand, and trust on ClawHub, skills.sh, or similar directories.

Typical use cases:

- Rewrite `name`, slug, or `description` for better search recall
- Improve `SKILL.md` first-screen copy for higher click-through
- Expand keyword, synonym, and user-intent coverage before publication
- Audit whether a skill is ready for ClawHub or skills.sh submission
- Compare a listing against directory ranking signals and identify weak spots

## When Not to Use This Skill

Do not use this skill when the problem is primarily implementation quality rather than listing discoverability.

Use a different workflow when you need to:

- Debug runtime failures inside the target skill
- Test whether the skill actually works end-to-end
- Add new product capabilities unrelated to discovery or listing quality
- Build platform-specific adapters unless the user explicitly asks for them

## If the Audit Is Inconclusive

If the static audit is not enough, say exactly what is still uncertain and what evidence is missing.

Common next steps:

- Read the target skill's full references and scripts for hidden terminology
- Inspect the public listing page to compare displayed copy against the local `SKILL.md`
- Ask for real search terms, target audience, or competitor listings
- Run a follow-up quality pass with `skill-test` if the issue may be implementation rather than SEO

## Example Prompts

- `Audit this skill for ClawHub search visibility and rewrite the description for better recall.`
- `Why is this skill hard to discover on skills.sh, and what copy should I change first?`
- `Optimize this new skill's slug, name, and top-of-file wording before I publish it.`
- `Compare this skill against ClawHub and skills.sh ranking signals and give me a prioritized fix list.`

## Audit Checklist

Review the target skill against this checklist before making changes:

- Is the slug literal, searchable, and stable?
- Does the frontmatter `description` state the job, object, outcome, and `Use when ...` trigger?
- Does the first screen show realistic example prompts early?
- Are exact task phrases, synonyms, and user-intent phrases all present?
- Are prerequisites, constraints, and trust signals visible?
- Does the skill look credible and maintained rather than generic or template-like?
- Does the copy still match the actual capability boundary of the skill?
- Are any optional extras, such as `eval.yaml` or UI metadata, actually relevant to the user's goal before recommending them?

## Workflow

1. Identify the target skill folder and inspect `SKILL.md` first.
2. Run `python3 {baseDir}/scripts/analyze_skill_seo.py <skill-path>` to get a baseline report.
3. Read [references/platform-signals.md](references/platform-signals.md) and [references/optimization-patterns.md](references/optimization-patterns.md) before making recommendations.
4. If present, inspect `README.md`, example files, and any public listing metadata that affects display.
5. Separate recommendations by platform:
   - `ClawHub`: prioritize semantic recall, exact slug or name matches, examples, and popularity signals.
   - `skills.sh`: prioritize clear category fit, high-conversion listing copy, trust signals, and install-friendly presentation.
6. Check that the skill remains broadly usable in OpenClaw, Claude Code, Codex, and Cursor without adding platform-specific optimization unless the user asks for it.
7. Rewrite only what improves discovery or trigger quality. Preserve the skill's actual capability boundaries.
8. If the user asks for implementation, edit the target skill and re-run the analyzer to confirm improvement.

## Definition of Done

- The analyzer has run and a baseline report exists.
- All `high` severity findings have been addressed or explicitly justified.
- The `description` covers at least 3 query classes: exact task phrase, synonyms, and user-intent language.
- Example prompts in SKILL.md reflect realistic user phrasing.
- Target platform compatibility status is explicit: `verified` where evidence exists, otherwise `unverified`.
- Re-running the analyzer shows improvement over the baseline.

## Output Requirements

Produce a concise report with:

- Current strengths and weaknesses
- Platform-specific findings for `ClawHub` and `skills.sh`
- Compatibility notes for `OpenClaw`, `Claude Code`, `Codex`, and `Cursor` using `verified` / `unverified` language only when relevant
- Missing keywords, synonyms, and user-phrased queries
- Recommended rewrites for `name`, slug, `description`, and first-screen content
- Trust and conversion gaps such as missing prerequisites, examples, screenshots, badges, stars, or install guidance
- A prioritized action list with `high`, `medium`, and `low` impact items

## Optimization Heuristics

- Prefer concrete, searchable names over abstract brand names.
- Put the problem, object, and action into the first 1 to 2 sentences.
- Include realistic user phrasings and close synonyms in `description` and the top of `SKILL.md`.
- Make the skill's boundary explicit so retrieval stays precise.
- Keep frontmatter concise but query-dense.
- Put examples near the top; examples improve both semantic recall and click-through.
- Add references only when they deepen a repeated workflow or expose non-obvious domain language.
- Avoid generic filler such as "powerful", "seamless", or "all-in-one" unless backed by specifics.
- Treat `eval.yaml` and UI metadata as optional enhancements, not baseline listing requirements.

## Rewrite Formula

Use this pattern when rewriting a weak listing:

`<Action> <object/system> for <outcome>. Use when you need to <job 1>, <job 2>, <job 3>, or when the user asks about <common phrasing>.`

Then reinforce it with:

- 3 to 5 example prompts using realistic user language
- A first-screen summary that repeats the main task phrase once
- One or two trust signals such as prerequisites, constraints, or costs

## Competitor Comparison

When a user asks for a market-aware rewrite:

1. Identify 2 or 3 comparable skills on the same directory.
2. Compare names, descriptions, example prompts, and first-screen structure.
3. Note what the target skill is missing, not just what competitors include.
4. Recommend changes that improve clarity and trust without copying competitors' wording.

## Anti-Patterns

Do not do any of the following:

- Suggest fake installs, fake stars, fake usage, or other manipulative ranking tactics
- Recommend version bumps or metadata churn without a real content change
- State platform behavior as a guaranteed fact when it is only an observed heuristic
- Stuff unrelated keywords into the description or examples
- Broaden a skill's positioning beyond what the implementation can actually do
- Flag missing `eval.yaml` or `agents/openai.yaml` as if they were mandatory for ClawHub or skills.sh publication

## When Editing a Skill

- Preserve the existing capability surface unless the user asks to expand it.
- Prefer improving `description`, top-of-file wording, and usage examples before adding large new references.
- If the folder name is weak for search, recommend a slug rename explicitly instead of renaming silently.
- If the target platform has already indexed the old name, explain the migration tradeoff.

## Resources

- Platform ranking and retrieval notes: [references/platform-signals.md](references/platform-signals.md)
- Rewrite patterns and keyword coverage rules: [references/optimization-patterns.md](references/optimization-patterns.md)

## Commands

```sh
# Audit a skill folder with default heuristics
python3 {baseDir}/scripts/analyze_skill_seo.py /path/to/skill

# Audit with explicit target keywords
python3 {baseDir}/scripts/analyze_skill_seo.py /path/to/skill --keywords "postgres backup, disaster recovery, wal archiving"

# Emit JSON for downstream processing
python3 {baseDir}/scripts/analyze_skill_seo.py /path/to/skill --json
```
