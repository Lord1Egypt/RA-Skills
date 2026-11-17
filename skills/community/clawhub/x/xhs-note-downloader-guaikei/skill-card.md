## Description:

Retrieves public Xiaohongshu note details, comments, creator posts, and interaction metrics through guaikei.com for KOL screening, content trend research, and campaign decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, analysts, and agents use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator posts for content research, KOL screening, competitor monitoring, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, note/profile URLs, and retrieved public data are sent to guaikei.com.

Mitigation: Use the skill only when data sharing with guaikei.com is authorized, and avoid passing links with sensitive xsec_token parameters unless needed.

Risk: The GUAIKEI_API_TOKEN credential is required for API access.

Mitigation: Store the token as a secret environment variable and use a scoped or disposable token where possible.

Risk: Retrieved results are automatically written to a local logs directory.

Mitigation: Review and periodically delete generated logs, especially when they contain campaign data, URLs, or retrieved comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-note-downloader-guaikei)
- [Guaikei API service site](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results are saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
