## Description:

Signal Pipeline gathers marketing signals from RSS, X/Twitter, Telegram, and Gmail newsletters to generate daily posts, weekly summaries, and monthly deep-dives for content creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mephistophelesbits](https://clawhub.ai/user/mephistophelesbits)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and market researchers use this skill to aggregate marketing and technology signals, track trends and competitors, and draft daily, weekly, or monthly content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail newsletter collection can expose email content beyond the intended marketing newsletters.

Mitigation: Run it only with a dedicated, least-privilege Gmail account or a tightly scoped newsletter label.

Risk: The newsletter monitor invokes the gog command through a shell, which increases command execution risk.

Mitigation: Audit the gog invocation before use and replace shell execution with an argument-vector subprocess call where possible.

Risk: The artifact includes WeChat/Sogou scraping behavior that is not disclosed in the main setup flow.

Mitigation: Remove that behavior or clearly disclose it before running the Telegram monitor in a real workspace.

Risk: Daily signal persistence uses a hard-coded agent-memory path.

Mitigation: Change storage to a project-local configurable directory before installing or scheduling the scripts.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before production or shared-workspace use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mephistophelesbits/skills/signal-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown and text reports printed to stdout, JSON daily signal files, and local SQLite data stores created by the included scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include daily draft posts, weekly theme summaries, monthly POV drafts, signal capsules with GDI scores, and source-specific monitoring reports.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
