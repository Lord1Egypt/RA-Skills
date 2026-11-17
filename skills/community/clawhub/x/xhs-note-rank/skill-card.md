## Description:

xhs-note-rank retrieves public Xiaohongshu note search results, note details and comments, and creator post lists for content research, competitor analysis, KOL screening, and trend insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, brand marketers, analysts, and MCN teams use this skill to gather public Xiaohongshu data for topic research, competitor monitoring, comment analysis, creator review, and reporting. It requires a GUAIKEI_API_TOKEN and sends keywords or Xiaohongshu URLs to the Guaikei API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note URLs, profile URLs, and related request data to www.guaikei.com using GUAIKEI_API_TOKEN.

Mitigation: Install and run it only when that third-party API use is acceptable, and avoid submitting private, sensitive, or unauthorized URLs or queries.

Risk: GUAIKEI_API_TOKEN is required and should be treated as sensitive.

Mitigation: Store the token in the environment, restrict access to the runtime environment, and rotate or revoke the token if it may have been exposed.

Risk: The skill automatically saves fetched results locally, and logs may contain xsec_token URLs, comments, profile data, and research queries.

Mitigation: Review, protect, redact, or delete generated logs after use according to the user's data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-note-rank)
- [Guaikei API service](https://www.guaikei.com)
- [Options and usage reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON command output with optional Markdown guidance and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include Xiaohongshu note URLs, user profile URLs, comments, interaction metrics, request metadata, and saved logs under logs/.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
