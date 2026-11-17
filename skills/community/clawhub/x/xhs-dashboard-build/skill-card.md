## Description:

Retrieves public Xiaohongshu notes, note details, note comments, and creator post lists so an agent can support content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, content operators, marketing teams, and analysts use this skill to collect public Xiaohongshu search, note, comment, and creator-post data for downstream summarization, comparison, reporting, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GuaiKei API token that may carry paid quota or account value.

Mitigation: Use a dedicated low-privilege token, avoid shared workspaces, and rotate or revoke the token if exposure is suspected.

Risk: Queried Xiaohongshu URLs and returned datasets are sent to www.guaikei.com and saved locally.

Mitigation: Confirm data-sharing permissions before use, protect the local logs directory, and delete saved results when they are no longer needed.

Risk: The skill is intended for public Xiaohongshu data and does not support private, hidden, or login-gated content.

Mitigation: Use it only for public data collection and keep redistributed or externally shared outputs within applicable platform, legal, and organizational rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-dashboard-build)
- [GuaiKei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and structured JSON results from the CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; task results are saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
