## Description:

A comprehensive skill for Tencent EdgeOne administration, covering edge acceleration, security, observability, API discovery, credential setup, site onboarding, cache operations, certificates, logs, and security reporting through Tencent Cloud CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and security engineers use this skill to administer Tencent EdgeOne zones, acceleration domains, cache tasks, certificates, logs, and security policies. It helps agents select the right reference workflow, call Tencent Cloud APIs with tccli, and produce operational reports or configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Tencent Cloud CLI credentials for EdgeOne administration.

Mitigation: Install and run it only where the user is comfortable granting agent access to the relevant Tencent Cloud account and credentials.

Risk: The skill can trigger high-impact cloud changes such as CAM service-linked role creation, purchases, site creation, DNS changes, security changes, and local tccli upgrades.

Mitigation: Require explicit user approval before local tool upgrades, permission changes, purchases, site creation, DNS/security changes, or other write operations.

Risk: Traffic, log, and security drill-downs may expose client IPs, user agents, URLs, or referers.

Mitigation: Confirm the need for sensitive drill-downs before use and limit disclosure of operational or personal data in reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/skills/tencent-edgeone-skill)
- [Tencent EdgeOne Homepage](https://edgeone.ai)
- [Tencent EdgeOne Documentation](https://edgeone.ai/document)
- [Tencent EdgeOne API Reference](https://edgeone.ai/document/50454)
- [Skill Definition](SKILL.md)
- [EdgeOne API Reference](references/api/README.md)
- [EdgeOne Site Acceleration Reference](references/acceleration/README.md)
- [Security Operations Reference](references/security/README.md)
- [Observability Reference](references/observability/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls, analysis]

**Output Format:** [Markdown with inline shell commands, tables, JSON snippets, and concise operational reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include tccli command plans, confirmation prompts, API-derived summaries, cache or certificate task status, security findings, and log or traffic reports.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
