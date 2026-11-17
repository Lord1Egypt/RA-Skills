## Description:

Wechat Content Studio helps agents research topics, draft WeChat Official Account articles, generate cover-image guidance, publish drafts through wenyan, verify Sogou indexing, and monitor article status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to produce WeChat Official Account articles from topic research through drafting, style self-checks, draft publishing, search-index verification, and article monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat publishing credentials may be exposed if secrets are entered on the command line or appear in logs.

Mitigation: Store credentials only in the expected local secrets file or environment configuration, avoid command-line secrets, and rotate any credential that appears in transcripts or logs.

Risk: The publish workflow can install the wenyan CLI globally if it is missing.

Mitigation: Review and approve package installation manually, pin or preinstall the CLI in controlled environments, and run the skill in a workspace where global package changes are acceptable.

Risk: Generated articles can be published to a WeChat draft workflow and may contain inaccurate, unsuitable, or off-brand content.

Mitigation: Require human editorial review before publishing drafts, especially for factual claims, style, copyright, and brand fit.

## Reference(s):

- [Wechat Content Studio on ClawHub](https://clawhub.ai/luis1213899/skills/wechat-studio-kh)
- [Content Methodology](artifact/references/content_methodology.md)
- [HV Analysis Methodology](artifact/references/hv-analysis-methodology.md)
- [Style Examples](artifact/references/style_examples.md)
- [Writing Techniques](artifact/references/写作技巧.md)
- [Humanized Writing Guide](artifact/references/去AI味指南.md)
- [Viral Content Methodology](artifact/references/爆款方法论.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated article drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Python scripts and the wenyan CLI to publish and verify WeChat drafts when credentials are configured.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
