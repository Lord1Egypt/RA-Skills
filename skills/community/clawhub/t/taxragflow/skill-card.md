## Description:

Taxragflow answers Chinese tax questions by querying a configured private RAGFlow knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxin139](https://clawhub.ai/user/zhaoxin139)

### License/Terms of Use:

MIT

## Use Case:

Developers, tax teams, and finance users use this skill to route questions about tax policies, VAT, corporate income tax, personal income tax, tax benefits, and tax filing processes to an enterprise RAGFlow knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tax, payroll, customer, or enterprise finance questions may be sent to a configurable external RAGFlow service.

Mitigation: Configure only a trusted HTTPS RAGFlow endpoint and avoid submitting personal or confidential details unless the deployment has approval to process that data.

Risk: The RAGFlow API key is sent as a bearer token to the configured service.

Mitigation: Use a least-privilege API key, store it only in environment configuration, rotate it regularly, and restrict it to the approved RAGFlow endpoint.

Risk: Dependency versions are not fully pinned, which can introduce package-version drift during installation.

Mitigation: Install from a reviewed lockfile or pin dependency versions before deploying in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxin139/skills/taxragflow)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Skill metadata](skill.yaml)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text answer or concise error message returned from the configured RAGFlow service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAGFLOW_API_URL, RAGFLOW_API_KEY, and RAGFLOW_CHAT_ID environment variables.]

## Skill Version(s):

1.0.0 (source: plugin.json, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
