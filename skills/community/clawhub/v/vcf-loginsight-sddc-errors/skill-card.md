## Description:

Extract recent critical SDDC Manager and vCenter error logs from Aria Operations for Logs to assist with VCF troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasture-rohit](https://clawhub.ai/user/kasture-rohit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to retrieve recent critical SDDC Manager and vCenter error logs from Aria Operations for Logs and assess likely VCF troubleshooting context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer-token access could expose or over-permit access to operational logs.

Mitigation: Use a least-privilege, read-only Log Insight token and limit environment access to agents that need this skill.

Risk: Unsafe TLS settings may weaken trust in the Log Insight connection.

Mitigation: Remove the TLS bypass or configure a trusted CA before production use.

Risk: The broad error query may retrieve more SDDC Manager or vCenter logs than the user intended.

Mitigation: Narrow the query or activation language and run it only after clear user intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasture-rohit/skills/vcf-loginsight-sddc-errors)
- [Publisher profile](https://clawhub.ai/user/kasture-rohit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with log fields, shell command context, and brief troubleshooting assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses LOGINSIGHT_HOST, LOGINSIGHT_API_TOKEN, curl, and jq; queries up to 10 recent error events.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
