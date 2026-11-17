## Description:

Stop Slop Zh helps agents draft, rewrite, and review Chinese prose to reduce common AI-writing patterns such as cliches, formulaic structure, nominalized verbs, abstract subjects, punctuation fingerprints, and inflated endings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, content teams, and developers use this skill when an agent is producing or polishing Chinese text for human readers. It guides the agent to remove formulaic AI style, preserve facts and stance, and flag places where real details must be supplied by the author.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The style rules may remove wording that is intentionally formal, precise, or required in legal, contractual, academic, policy, or exact-preservation text.

Mitigation: Use the skill as editorial guidance in those contexts, review changes against the source text, and preserve required wording when precision matters.

Risk: Requests to make prose more concrete can lead an agent to add unsupported numbers, names, or scenarios.

Mitigation: Require any new concrete detail to come from supplied evidence; otherwise keep a plain statement, leave an author-fill placeholder, or delete the unsupported claim.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/leeguooooo/stop-slop-zh)
- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/stop-slop-zh)
- [Chinese AI cliche phrase blacklist](references/phrases.md)
- [Chinese AI sentence-structure blacklist](references/structures.md)
- [Chinese AI punctuation fingerprints](references/punctuation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language Chinese prose, editorial guidance, rewrite suggestions, and checklist-style review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quality scores or author-fill placeholders for missing factual details.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
