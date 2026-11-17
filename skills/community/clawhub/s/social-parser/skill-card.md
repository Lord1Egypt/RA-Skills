## Description:

Parses Douyin videos and Xiaohongshu notes to extract titles, covers, descriptions, tags, creator details, media URLs, and related content metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyi9531](https://clawhub.ai/user/huyi9531)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and developers use this skill to inspect Douyin or Xiaohongshu links, retrieve structured metadata, and prepare content-analysis summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send Douyin or Xiaohongshu links to a remote parser through the gnomic CLI.

Mitigation: Use only public or non-sensitive links and disclose remote parsing before execution.

Risk: The install guidance uses an unpinned global npm installation for gnomic-cli.

Mitigation: Prefer a pinned, reviewed CLI version and avoid elevated privileges for global installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huyi9531/skills/social-parser)
- [gnomic-cli repository referenced by the skill](https://github.com/huyi9531/gnomic_cli)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON parser output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote media URLs and social-media metadata returned by the gnomic CLI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
