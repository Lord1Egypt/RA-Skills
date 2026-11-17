## Description:

Provides an agent skill for Toutiao account operations, including scheduled content posting, vegetable-price tracking, revenue-oriented content planning, and an operations knowledge base for food-price and local-livelihood creators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhhjwei](https://clawhub.ai/user/jhhjwei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to plan, generate, publish, and monitor Toutiao posts in the vegetable-price and local-livelihood niche. It is intended to support recurring account operations, pricing-data summaries, and revenue-focused content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags automated Toutiao posting and automatic account actions without clear per-post approval controls.

Mitigation: Require manual review and explicit approval before any generated post is published or location is added.

Risk: The server security guidance warns that package-authored memory is imported by the skill.

Mitigation: Inspect the bundled memory files before import and avoid loading them into active agent memory unless the operator intentionally wants that context.

Risk: The server security guidance advises caution before installation and points to restore.sh as a file to inspect.

Mitigation: Review restore.sh before running it, use a dedicated low-risk Toutiao account, and pin installer versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhhjwei/skills/toutiao-agent-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/jhhjwei)
- [Toutiao creator portal](https://mp.toutiao.com)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)
- [Publishing guide](artifact/knowledge/toutiao-publishing-guide.md)
- [Revenue strategy knowledge base](artifact/knowledge/toutiao-revenue-strategy.md)
- [Timing optimization knowledge base](artifact/knowledge/toutiao-timing-optimization.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated content drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduled posting plans, Toutiao content drafts, data summaries, and operational checklists.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
