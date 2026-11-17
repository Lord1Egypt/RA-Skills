## Description:

Automates multi-platform ecommerce operations including product opportunity scanning, listing support, customer replies, order handling, and daily operations reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hnc87](https://clawhub.ai/user/hnc87)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and ecommerce automation developers use this skill to coordinate recurring storefront tasks across platforms such as Douyin, Taobao/Tmall, Pinduoduo, and JD. It can prepare local configuration and data files, run scheduled operational scripts, and generate markdown daily reports from store data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unattended live-store automation that can publish products, message customers, and process shipments.

Mitigation: Use dry-run testing, explicit approval gates, audit logs, scoped credentials, and a documented way to disable each scheduled task before connecting real store accounts.

Risk: Cron-based automation can repeatedly perform customer replies, product publishing, shipping, refunds, browser automation, or API-key-backed actions without review.

Mitigation: Keep live publishing, auto replies, auto shipping, refunds, browser automation, and API keys disabled until the operator has reviewed and approved the configured workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hnc87/skills/solo-ecommerce-agent)
- [Platform operation guide](references/platform_guides.md)
- [Taobao seller console](https://myseller.taobao.com)
- [Douyin store console](https://fxg.jinritemai.com)
- [Pinduoduo merchant console](https://mms.pinduoduo.com)
- [JD shop console](https://shop.jd.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, Python scripts, JSON configuration, cron schedules, logs, and markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON data and log/report files under the configured ecommerce data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
