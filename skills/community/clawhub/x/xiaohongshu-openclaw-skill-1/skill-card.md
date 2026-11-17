## Description:

Provides command-line access to structured public Xiaohongshu data for keyword search, note details, creator post monitoring, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, marketers, and analysts use this skill to retrieve public Xiaohongshu data for content planning, competitor monitoring, KOL screening, and comment insight workflows. It supplies data for downstream analysis rather than making marketing strategy decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, links, and the Guaikei API token are sent to the Guaikei service.

Mitigation: Use the skill only when that data sharing is acceptable, scope inputs to necessary public data, and rotate the API token if exposure is suspected.

Risk: Generated local logs may contain sensitive research inputs or retrieved content.

Mitigation: Treat the logs directory as sensitive and avoid committing, publishing, or sharing it outside the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xiaohongshu-openclaw-skill-1)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can write result logs locally and require GUAIKEI_API_TOKEN for authenticated API access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
