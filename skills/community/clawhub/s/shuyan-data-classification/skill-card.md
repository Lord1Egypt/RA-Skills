## Description:

Classifies and assigns sensitivity levels to database field metadata in batch through the Shuyan API, returning labels, reasoning, confidence, and sensitivity levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianmo1997](https://clawhub.ai/user/jianmo1997)

### License/Terms of Use:

MIT

## Use Case:

Developers and data governance teams use this skill to submit database field metadata or batch JSON records to a Shuyan classification endpoint and receive sensitive-data labels and sensitivity levels for cataloging or policy workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive sample data or regulated records may be sent to the configured API endpoint.

Mitigation: Use only a trusted local service or an HTTPS endpoint you control, and send real PII, financial data, production samples, or regulated records only when policy allows.

Risk: Bearer credentials may be exposed or reused, especially if the default sk-secret-key credential is left in place.

Mitigation: Set a unique SHUYAN_API_KEY, manage it as a secret, and avoid relying on the default credential.

Risk: The default local HTTP API setting can transmit credentials and sample content insecurely outside a trusted local environment.

Mitigation: Configure SHUYAN_API_URL to a trusted local service or an HTTPS endpoint under your control before processing sensitive inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianmo1997/skills/shuyan-data-classification)
- [Publisher profile](https://clawhub.ai/user/jianmo1997)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash and Python command examples plus JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHUYAN_API_KEY and SHUYAN_API_URL; batch responses are synchronous JSON and may take longer for larger inputs.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
