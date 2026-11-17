## Description:

Use when the user encounters VolcEngine errors or needs local troubleshooting for OpenAPI, Python SDK, CLI, IAM, billing, compute, networking, storage, database, CDN, media, AI, security, or VKE cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to triage VolcEngine service errors, local CLI or SDK failures, identity and permission issues, billing and quota problems, networking, storage, media, AI, security, and VKE incidents without modifying cloud resources by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use VolcEngine read credentials and summarize account, infrastructure, billing, or resource details during troubleshooting.

Mitigation: Use temporary least-privilege credentials, avoid sharing raw outputs, and share only the minimum troubleshooting summary needed.

Risk: Security evidence notes that one ALB backend collector can collect infrastructure details outside the selected load balancer.

Mitigation: Be careful with the ALB backend collector and review collected scope before sharing results until its query scope is narrowed.

## Reference(s):

- [Getting Started](references/getting-started.md)
- [OpenAPI Quick Check](references/openapi-quick-check.md)
- [Domain Troubleshooting Guides](references/domain-guides/README.md)
- [Billing Troubleshooting Scripts](references/domain-guides/billing-quota/scripts/README.md)
- [Compute, Container, and Network Scripts](references/domain-guides/compute-container-network/scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, diagnostic checklists, and JSON summaries from helper scripts when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only troubleshooting posture by default; sensitive credentials and full access keys should be masked.]

## Skill Version(s):

1.0.2 (source: server release evidence, released 2026-09-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
