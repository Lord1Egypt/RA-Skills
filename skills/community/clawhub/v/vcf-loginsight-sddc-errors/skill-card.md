## Description: <br>
Extract recent critical SDDC Manager and vCenter error logs from Aria Operations for Logs to assist with VCF troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasture-rohit](https://clawhub.ai/user/kasture-rohit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to fetch and summarize recent VCF, SDDC Manager, and vCenter error logs from a configured Aria Operations for Logs endpoint during troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Log Insight bearer token to retrieve logs that may expose sensitive infrastructure details. <br>
Mitigation: Use a least-privileged, read-only token and review returned log text before sharing it outside the troubleshooting context. <br>
Risk: The provided curl command disables TLS certificate verification with -k. <br>
Mitigation: Remove -k where possible and configure trusted certificates for the Log Insight endpoint. <br>
Risk: The query scope is broad and may fetch unrelated or excessive error records. <br>
Mitigation: Add explicit SDDC Manager, vCenter, source, severity, and time-window filters before running in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kasture-rohit/vcf-loginsight-sddc-errors) <br>
- [Project homepage](https://github.com/kasture-rohit/vcf-openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized log findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOGINSIGHT_HOST and LOGINSIGHT_API_TOKEN, plus curl and jq. The command returns up to 10 recent error events from the configured Log Insight endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
