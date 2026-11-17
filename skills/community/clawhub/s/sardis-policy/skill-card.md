## Description:

Natural language spending policy creation and management for Sardis agent wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create, inspect, test, and version Sardis spending policies for agent wallets, including limits, vendor restrictions, category controls, and approval thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make durable spending-policy changes when used with a Sardis API key.

Mitigation: Use a least-privileged SARDIS_API_KEY and review every policy before creation or replacement.

Risk: Permissive policy templates or natural-language descriptions may allow broader spending than intended.

Mitigation: Prefer explicit limits, vendor allowlists, approval thresholds, and dry-run policy checks before relying on a policy.

Risk: The shell examples include JSON bodies assembled in shell commands.

Mitigation: Use pinned dependencies and safer jq-built JSON request bodies before copying examples into automation.

## Reference(s):

- [Sardis Website](https://sardis.sh)
- [Sardis Policy Documentation](https://sardis.sh/docs/policies)
- [Sardis API Reference](https://api.sardis.sh/v2/docs)
- [ClawHub Skill Page](https://clawhub.ai/efedurmaz16/skills/sardis-policy)
- [Publisher Profile](https://clawhub.ai/user/efedurmaz16)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Sardis API key plus curl and jq for the documented command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
