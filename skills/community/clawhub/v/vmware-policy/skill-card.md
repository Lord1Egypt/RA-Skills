## Description:

Provides shared audit logging, policy enforcement, and input sanitization for the VMware MCP skill family, with a CLI and Python library for querying logs and managing rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VMware administrators use this library and CLI to review audit activity, inspect policy decisions, configure deny rules and maintenance windows, and integrate audit and sanitization support into VMware skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs and rotated archives may contain tool parameters, results, user information, and timestamps.

Mitigation: Restrict access to the local audit database and its archives, and explicitly mark sensitive parameters and results for redaction.

Risk: The packaged policy baseline denies no operations, so calls are allowed unless operator rules are configured.

Mitigation: Configure deny rules or maintenance windows and use `vmware-audit policy` to confirm which rules are active.

Risk: Setting `VMWARE_POLICY_DISABLED=1` bypasses policy evaluation for the process.

Mitigation: Restrict who can set this environment variable and unset it after any intentional use.

Risk: The benign security verdict has medium confidence; some local references were unresolved and executable behavior was not checked.

Mitigation: Review unresolved references and assess the installed package before relying on it in a deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-policy)
- [Project homepage](https://github.com/vmware-skills/VMware-Policy)
- [Setup guide](artifact/references/setup-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [MCP result contract](artifact/references/mcp-result-contract.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Code, Guidance]

**Output Format:** [CLI audit summaries, JSON exports, YAML policy examples, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit results depend on selected filters and time ranges and may contain sensitive operational details.]

## Skill Version(s):

1.26.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
