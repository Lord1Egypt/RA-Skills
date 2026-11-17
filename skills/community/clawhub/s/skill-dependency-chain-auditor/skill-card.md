## Description:

Helps audit transitive skill dependency chains in agent compositions, catching cases where indirect dependencies introduce vulnerabilities that propagate through the chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to audit an agent skill's direct and transitive dependencies, assess trust gradients and version pinning, identify graph anomalies, and summarize dependency-chain risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit results can be incomplete when dependency metadata is missing, inaccurate, or unavailable across the full transitive chain.

Mitigation: Confirm dependency declarations and registry metadata before relying on the audit verdict for deployment decisions.

Risk: The skill may guide use of dependency metadata or registries during an audit, even though the artifact itself has no executable behavior.

Mitigation: Review proposed data sources and commands before use, and limit registry access to approved environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/skill-dependency-chain-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report may include dependency inventory, trust-gradient analysis, version-pinning assessment, graph anomalies, capability aggregation, a chain integrity verdict, and recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
