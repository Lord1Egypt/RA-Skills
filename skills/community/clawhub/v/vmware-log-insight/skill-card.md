## Description:

Search and aggregate VMware VCF Operations for Logs data to investigate events, discover fields, detect spikes, and inspect alerts; all tools are read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VMware operations engineers use this skill to investigate centralized VMware logs, find relevant events and spikes, discover searchable fields, and inspect alert history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be exposed if password files are readable by other users; the documented base64 storage is obfuscation, not encryption.

Mitigation: Restrict credential file permissions and prefer injecting passwords from a secret manager; use a least-privilege read-only service account.

Risk: A benign scan is not a guarantee of zero risk, and Skillspector coverage was partial.

Mitigation: Review credential setup and the optional `--skip-auth` behavior before installation, following the supplied security guidance.

## Reference(s):

- [Capabilities](artifact/references/capabilities.md)
- [CLI Reference](artifact/references/cli-reference.md)
- [Setup Guide](artifact/references/setup-guide.md)
- [Agent Guardrails](artifact/references/agent-guardrails.md)
- [ClawHub Release](https://clawhub.ai/zw008/skills/vmware-log-insight)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Markdown]

**Output Format:** [Structured JSON query results with concise text or Markdown summaries for the agent's answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results subject to the appliance response and documented query limits]

## Skill Version(s):

2.4.4 (source: server-resolved release metadata, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
