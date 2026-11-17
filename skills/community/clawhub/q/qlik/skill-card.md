## Description:

Complete Qlik Cloud analytics platform integration with 37 tools for health checks, search, app management, reloads, natural language Insight Advisor queries, automations, AutoML, Qlik Answers AI, data alerts, spaces, users, licenses, data files, and lineage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fianabates1](https://clawhub.ai/user/fianabates1)

### License/Terms of Use:

MIT

## Use Case:

Developers, data engineers, and BI operators use this skill to inspect and operate Qlik Cloud tenants, apps, reloads, analytics queries, automations, AutoML, Qlik Answers, alerts, users, spaces, data files, and lineage from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or tenant settings may be exposed or misused if stored insecurely or provided to unsafe scripts.

Mitigation: Use a minimally scoped Qlik API key, set QLIK_TENANT only to the exact HTTPS tenant you control, and avoid storing long-lived keys in broadly readable files.

Risk: Unsafe inputs or tenant settings may allow unintended local code execution or unsafe API requests.

Mitigation: Review and harden the shell scripts before installation, and do not expose them to untrusted queries or IDs until Python interpolation and temporary-file handling are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fianabates1/skills/qlik)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON-producing shell tool invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts generally return JSON objects containing success status, data or error details, and timestamps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
