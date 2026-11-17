## Description:

Guides agents through authenticated Knowledge Planet operations with zsxq-cli, including community and content management, moderation workflows, reports, poster and video generation, and Skill Pay payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxq](https://clawhub.ai/user/zsxq)

### License/Terms of Use:

MIT-0

## Use Case:

External community operators, support staff, and developers use this skill to manage Knowledge Planet groups, posts, comments, notes, members, tags, columns, scheduled jobs, and payment-related workflows from an authenticated zsxq-cli session. It also supports operational reporting, risk monitoring, content curation, and local poster or video generation from group content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates an authenticated Knowledge Planet account and can initiate write, delete, payment, bulk tag/archive, and migration actions.

Mitigation: Require explicit user confirmation before those actions and verify group, topic, comment, note, payment object, and price identifiers before execution.

Risk: Local poster and video workflows include script execution and generated HTML preview behavior that the security summary flags for review.

Mitigation: Install only from a trusted publisher, avoid externally supplied output paths, do not preview generated HTML from untrusted post content until reviewed, and prefer pinned audited package versions.

Risk: AI-generated summaries, posters, and videos may change the tone or emphasis of source posts.

Mitigation: Show generated scripts or summaries to the user for approval before rendering or sharing derived content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zsxq/skills/zsxq)
- [Authentication and Error Handling](references/auth-errors.md)
- [CLI Exploration](references/cli-exploration.md)
- [Group List](references/group-list.md)
- [Topic Create](references/topic-create.md)
- [Topic Edit](references/topic-edit.md)
- [Topic Delete](references/topic-delete.md)
- [WeChat Order Create](references/wechat-order-create.md)
- [Daily Patrol Scenario](references/scenarios/daily-patrol.md)
- [Operations Report Scenario](references/scenarios/compose-operations-report.md)
- [Daily Poster Scenario](references/scenarios/generate-daily-poster.md)
- [Video Generation Scenario](references/scenarios/generate-video.md)
- [Risk Monitoring Scenario](references/scenarios/monitor-risky-content.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PNG, HTML, or MP4 files for poster and video workflows when required dependencies are available.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
