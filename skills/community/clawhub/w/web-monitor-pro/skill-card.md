## Description:

Monitor web pages for content changes, price drops, stock availability, and custom conditions, including change summaries, visual diffs, templates, JavaScript rendering, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakes420](https://clawhub.ai/user/jakes420)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to create and manage local web monitors for price, stock, and content changes, then check dashboards, diffs, reports, and webhook notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated monitor imports or configurations may introduce unsafe URLs, webhooks, or unexpected local state.

Mitigation: Use only trusted monitor JSON and review imported monitors before running checks.

Risk: Monitoring local, private, or internal URLs can expose sensitive network or page data through stored snapshots, reports, or webhooks.

Mitigation: Restrict monitors to intended public URLs and avoid local, private, or internal resources.

Risk: Webhook destinations receive event payloads that may contain sensitive page, price, or availability details.

Mitigation: Use trusted webhook endpoints and review payload sensitivity before enabling notifications.

Risk: Optional browser or Cloudflare engines add dependency and execution surface beyond the default curl path.

Mitigation: Enable optional engines only in a virtual environment with reviewed and pinned dependencies.

Risk: Generated dashboard and diff files write local HTML derived from monitored page content.

Mitigation: Open generated HTML only from trusted monitor content and review outputs before sharing them.

## Reference(s):

- [Web Monitor Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/jakes420/skills/web-monitor-pro)
- [Publisher Profile](https://clawhub.ai/user/jakes420)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with CLI commands, JSON exports/imports, generated HTML diffs, and dashboard/report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores monitor data, snapshots, screenshots, and generated dashboard files under the configured local web-monitor directory.]

## Skill Version(s):

3.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
