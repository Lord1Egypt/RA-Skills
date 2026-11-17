## Description:

Automates Xiaohongshu (XHS/RED) content publishing, browser login checks, content search and detail retrieval, comments, notification mentions, and creator metrics through Chrome DevTools Protocol.

This skill is for research and development only.

## Publisher:

[white0dew](https://clawhub.ai/user/white0dew)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators evaluating Xiaohongshu automation use this skill to run agent-assisted publishing, search, engagement, notification, and creator-metrics workflows. The skill expects review of post and comment content before live actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Xiaohongshu browser profile and perform account actions.

Mitigation: Use a dedicated account and browser profile, and install only when this level of account access is acceptable.

Risk: Public posts or comments may be published from generated or user-supplied text and media.

Mitigation: Review final titles, body text, comments, images, and videos before allowing live posting or commenting.

Risk: Remote CDP access can expose browser control to an untrusted host.

Mitigation: Use local CDP by default and connect to a remote CDP endpoint only when the host and network path are fully trusted.

Risk: Untrusted webpage content or media URLs may be downloaded or used in publishing workflows.

Mitigation: Avoid feeding the skill untrusted pages or media URLs, and verify media sources before use.

Risk: Notification, analytics, and CSV outputs can contain private account or performance data.

Mitigation: Treat these outputs as private account data and store or share them only in trusted locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/white0dew/skills/xiaohongshuskills)
- [ClawHub publisher profile](https://clawhub.ai/user/white0dew)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger browser-controlled posting, commenting, content retrieval, notification capture, or CSV export when the user runs the generated commands.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
