## Description:

This skill helps agents retrieve public Xiaohongshu data for keyword trend tracking, note details, comment review, and creator post monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, analysts, and agent developers use this skill to collect and summarize public Xiaohongshu search results, note details, comments, and creator posts for social listening, content planning, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and retrieved public-data requests may be sent to Guaikei's API.

Mitigation: Use the skill only when third-party API processing is acceptable and the requested data-sharing scope is authorized.

Risk: The GUAIKEI_API_TOKEN is sensitive and command results may be saved in local logs.

Mitigation: Protect the token, avoid shared or archived workspaces for sensitive runs, clean generated logs when needed, and rotate the token if exposure is suspected.

Risk: Results intended to be recent may be misleading if recency options are left implicit.

Mitigation: Set --sort and --time explicitly when the task depends on current or recent Xiaohongshu activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-comment-sentiment-guaikei)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may write retrieved results to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
