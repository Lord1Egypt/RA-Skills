## Description:

Analyzes a product's recent Xiaohongshu search trends and popular posts to recommend a promotion direction and examples to learn from.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and marketers use this skill before publishing a Xiaohongshu product post to gauge two-week interest, choose a promotion angle, and study relevant high-engagement posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An obfuscated helper forwards prompts to an LLM service, making its behavior difficult to inspect.

Mitigation: Review or replace the helper before use; keep the LLM endpoint local unless remote forwarding is intentional.

Risk: The skill operates through a logged-in Xiaohongshu browser session.

Mitigation: Install only if you trust the publisher and are comfortable granting access to that session.

Risk: User-specified input paths and output directories affect files read and written locally.

Mitigation: Provide only trusted product-image paths and output directories.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fatmind/skills/xhs-product-trend-fit)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Readable analysis in data.md and structured results in res.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trend assessment, suggested promotion direction, and breakdowns of example posts; HTML can be rendered separately from the JSON results.]

## Skill Version(s):

1.1.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
