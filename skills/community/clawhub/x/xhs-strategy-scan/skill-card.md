## Description:

xhs-strategy-scan helps agents collect public Xiaohongshu notes, note details, comments, and creator posts for content research, competitor analysis, KOL screening, and trend insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, creators, and analysts use this skill to gather public Xiaohongshu data for topic research, competitor monitoring, comment analysis, creator post tracking, KOL screening, and trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GUAIKEI_API_TOKEN in URL query strings.

Mitigation: Keep the token private, avoid sharing command traces that may expose it, and rotate the token if exposure is suspected.

Risk: Retrieved data and Xiaohongshu URLs with xsec_token values may be saved to plaintext local logs.

Mitigation: Treat the logs directory as sensitive, restrict access to it, and redact or remove logs before sharing workspaces or outputs.

Risk: The skill is intended for public Xiaohongshu data and may return comments, profile details, and research history.

Mitigation: Use it only for public data the user is allowed to process and review outputs before redistribution or use in reports.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/xhs-strategy-scan)
- [Guaikei token and API service](https://www.guaikei.com)
- [Options and calling guide](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output from the CLI tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and GUAIKEI_API_TOKEN; command outputs may include Xiaohongshu URLs, comments, profile details, and retrieved content.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
