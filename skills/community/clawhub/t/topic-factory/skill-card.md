## Description:

自媒体选题日报系统 generates daily Chinese self-media topic reports by collecting public trend data, matching a keyword library, using an LLM for hooks and titles, writing Markdown reports, and optionally sending Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seairteng](https://clawhub.ai/user/seairteng)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and self-media teams use this skill to produce a daily shortlist of data-informed topics for Douyin short videos and WeChat public-account articles. It is intended to help schedule topic discovery, drafting prompts, Markdown report creation, notification, and archiving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires an Anthropic API key and may encourage persistent shell startup configuration.

Mitigation: Use a scoped credential from a trusted HTTPS Anthropic endpoint, prefer a secret manager or temporary environment injection, and avoid committing or sharing shell profile files.

Risk: Feishu notifications send generated topic content to a user-configured webhook destination.

Mitigation: Configure only trusted Feishu groups or bots, rotate leaked webhook tokens, and review notification contents before enabling scheduled delivery.

Risk: The scheduled wrapper depends on an external alert script outside the skill package.

Mitigation: Inspect, replace, or remove the external send_alert.py dependency before enabling cron jobs.

Risk: LLM-generated hooks, titles, and data points may be inaccurate or misleading.

Mitigation: Treat generated topics as drafts and manually verify facts, sources, and investment-sensitive claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seairteng/skills/topic-factory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces daily topic files, Feishu notification text, fallback messages, logs, and short-lived archive files for unused topics.]

## Skill Version(s):

1.0.1 (source: server release evidence and changelog; artifact frontmatter and _meta.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
