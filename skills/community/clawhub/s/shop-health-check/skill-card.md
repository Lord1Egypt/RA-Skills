## Description:

Shop Health Check helps agents run automated health checks for cross-border e-commerce stores, including site availability, response time, SSL certificate status, key-page 404s, missing content, and Feishu alert delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzhimin](https://clawhub.ai/user/zzhimin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and e-commerce teams use this skill to configure recurring health checks for one or more storefronts and receive concise reports or Feishu alerts when availability, SSL, product page, or content checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured shop URLs can cause broad outbound network requests, including to sensitive internal services if untrusted configuration is used.

Mitigation: Use only trusted shop URLs, allowlist expected domains, and restrict outbound network access where possible.

Risk: Report posting can send operational details to a Feishu webhook when reporting is enabled.

Mitigation: Validate or allowlist Feishu webhook domains and use --no-feishu unless external reporting is intended.

Risk: Unpinned Python dependencies may change behavior across environments.

Mitigation: Install dependencies in a virtual environment and pin dependency versions for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzhimin/skills/shop-health-check)
- [Publisher profile](https://clawhub.ai/user/zzhimin)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Console text, Feishu markdown card payload, or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured shop domains and paths; Feishu delivery is controlled by webhook configuration or --no-feishu.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
