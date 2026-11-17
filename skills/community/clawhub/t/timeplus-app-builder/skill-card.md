## Description:

Use when creating, packaging, or installing a Timeplus app (.tpapp), including converting SQL resources and dashboards into an installable app package, writing manifests, applying template variables, building dashboard JSON, and debugging install failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtao](https://clawhub.ai/user/gangtao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, package, install, and troubleshoot Timeplus .tpapp bundles that provision DDL resources and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted app packages or install-time configuration can lead to unsafe Timeplus resource definitions or installs.

Mitigation: Use only trusted packages and trusted install-time config, and review generated manifests, DDL, dashboards, and install commands before deployment.

Risk: Secrets can be exposed through plaintext endpoints or queryable resource definitions.

Mitigation: Prefer HTTPS for non-local endpoints, avoid embedding secrets in DDL or dashboard queries, and keep sensitive values out of queryable resource definitions.

Risk: Mutable Python dependencies and broad network listeners can increase deployment risk.

Mitigation: Pin Python dependencies and bind inputs to 0.0.0.0 only when network access is explicitly restricted.

Risk: Template values can change SQL, JSON, or shell behavior when inserted without context-aware quoting.

Mitigation: Validate install-time values and quote template variables according to the target context before packaging or installing an app.

## Reference(s):

- [Dashboard JSON Specification](artifact/references/dashboard-spec.md)
- [Timeplus Documentation](https://docs.timeplus.com)
- [Timeplus Proton GitHub Repository](https://github.com/timeplus-io/proton)
- [Sprig Template Functions](https://masterminds.github.io/sprig/)
- [Timeplus SQL Guide](https://github.com/timeplus-io/AgentSkills/tree/main/timeplus-sql-guide)
- [ClawHub Skill Page](https://clawhub.ai/gangtao/skills/timeplus-app-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, SQL, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces app package structure, manifest guidance, dashboard specifications, DDL patterns, install commands, and troubleshooting guidance for Timeplus .tpapp releases.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
