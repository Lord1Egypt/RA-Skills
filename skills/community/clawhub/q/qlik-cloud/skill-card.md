## Description:

Complete Qlik Cloud analytics platform integration with 37 tools for health checks, search, app management, reloads, natural language queries, automations, AutoML, Qlik Answers AI, data alerts, spaces, users, licenses, data files, and lineage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[undsoul](https://clawhub.ai/user/undsoul)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and operators use this skill to inspect and operate Qlik Cloud tenants, apps, reloads, automations, users, spaces, lineage, alerts, AutoML resources, and Qlik Answers assistants. It also helps agents query business data through Qlik Insight Advisor using natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Qlik API credentials to perform tenant reads and tenant-changing actions.

Mitigation: Use a least-privilege Qlik API key, store it in a secret manager or runtime environment, and review commands before execution.

Risk: Unsafe shell and Python interpolation patterns can increase exposure when questions, IDs, or tenant endpoints are untrusted.

Mitigation: Avoid untrusted inputs until the interpolation issues are fixed, and require an https:// Qlik tenant endpoint.

## Reference(s):

- [ClawHub Qlik Cloud skill page](https://clawhub.ai/undsoul/skills/qlik-cloud)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [JSON responses from bash tools, with Markdown setup and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QLIK_TENANT and QLIK_API_KEY at runtime.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
