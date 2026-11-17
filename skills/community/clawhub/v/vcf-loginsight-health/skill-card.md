## Description:

Check the health, uptime, and node status of Aria Operations for Logs (Log Insight) in a VCF environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasture-rohit](https://clawhub.ai/user/kasture-rohit)

### License/Terms of Use:

MIT-0

## Use Case:

VCF platform operators and SREs use this skill to check Aria Operations for Logs cluster health, node status, and uptime, then summarize errors or disconnected nodes for operational follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health-check commands send a bearer token while disabling TLS certificate verification.

Mitigation: Prefer removing -k, configuring a trusted CA bundle for private certificates, and using a read-only token limited to health and node-status endpoints.

Risk: A misconfigured or untrusted LOGINSIGHT_HOST could receive the configured API token.

Mitigation: Confirm LOGINSIGHT_HOST before execution and store LOGINSIGHT_API_TOKEN in a protected environment secret rather than in files or shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasture-rohit/skills/vcf-loginsight-health)
- [Skill homepage](https://github.com/kasture-rohit/vcf-openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summary table with shell commands and JSON-derived status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOGINSIGHT_HOST, LOGINSIGHT_API_TOKEN, curl, and jq.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
