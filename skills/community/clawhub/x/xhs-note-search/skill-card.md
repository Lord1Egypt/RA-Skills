## Description:

XHS Note Search helps agents search public Xiaohongshu notes, retrieve note details and comments, and list public posts from a creator profile for content research, competitor analysis, KOL screening, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External marketers, content creators, analysts, and developers use this skill to collect public Xiaohongshu note, comment, and creator-post data through Guaikei APIs for topic discovery, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu search terms, note URLs, profile URLs, and the Guaikei API token to a third-party service.

Mitigation: Install and run it only when that data sharing is acceptable; avoid submitting sensitive targets and manage the API token as a credential.

Risk: Fetched results are automatically saved locally in plaintext logs that may contain research history, comments, profile data, and token-bearing URLs.

Mitigation: Keep generated logs out of source control, shared workspaces, backups, and support bundles unless they have been reviewed and redacted.

## Reference(s):

- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei API Service](https://www.guaikei.com)
- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/xhs-note-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance and shell commands; command results are structured JSON and JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may be saved under logs/ and can include search targets, comments, profile data, and token-bearing URLs.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, package.json, release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
