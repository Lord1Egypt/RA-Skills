## Description:

Unified audit logging, policy enforcement, and input sanitization for the entire VMware MCP skill family.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VMware administrators use this skill to review audit activity, inspect or configure policy rules, export audit records, and integrate policy checks and input sanitization into VMware skill tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged policy baseline denies no operations, and a user rules file replaces the baseline.

Mitigation: Back up existing rules, configure explicit deny rules, and use `vmware-audit policy` to confirm the effective rules before production use.

Risk: The security scan was partial because some referenced local paths were missing.

Mitigation: Review the production setup instructions and all referenced local files before installation.

Risk: Audit records and exports can include infrastructure identifiers, configuration, and operation results.

Mitigation: Restrict access to the audit database and review exports before sharing them.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [CLI Reference](references/cli-reference.md)
- [Capabilities](references/capabilities.md)
- [Agent Guardrails](references/agent-guardrails.md)
- [Project Homepage](https://github.com/vmware-skills/VMware-Policy)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Audit summaries, JSON audit exports, CLI commands, YAML policy examples, and Python integration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit records may contain infrastructure names, addresses, configuration, and operation results.]

## Skill Version(s):

1.25.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
