## Description:

Generates brand-matched content by reading a local brand voice profile, matching relevant trend reports, and drafting posts, threads, newsletters, articles, and video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:


## Use Case:

Content creators, marketing teams, and operators use this skill to generate draft social, newsletter, article, and video content that follows a supplied brand voice profile and selected trend inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The brand voice profile may contain private examples or details that should not be reused in generated drafts.

Mitigation: Review and minimize the local brand voice profile before use, and avoid including sensitive examples or private information.

Risk: Generated content batches may contain inaccurate, off-brand, or unintended draft text.

Mitigation: Review `data/content-batch-{date}.json` before scheduling, publishing, or sharing generated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-brand-voice-writer)
- [Publisher profile](https://clawhub.ai/user/ryudi84)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Draft content for social posts, threads, newsletters, articles, and video scripts, with generated batches saved as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local brand voice and trend-report JSON files and writes generated draft batches to local JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
