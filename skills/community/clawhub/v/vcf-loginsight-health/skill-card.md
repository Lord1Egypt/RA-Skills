## Description: <br>
Check the health, uptime, and node status of Aria Operations for Logs (Log Insight) in a VCF environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasture-rohit](https://clawhub.ai/user/kasture-rohit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform operators use this skill to query Log Insight cluster health and node status, then summarize the results into a readable table that highlights unhealthy or disconnected nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Log Insight API token to query a configured service endpoint. <br>
Mitigation: Set LOGINSIGHT_HOST only to a trusted internal endpoint and use a least-privilege or read-only API token where possible. <br>
Risk: The provided curl commands disable TLS certificate verification. <br>
Mitigation: Review the endpoint and certificate handling before use, and enable certificate verification when the environment supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kasture-rohit/vcf-loginsight-health) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance] <br>
**Output Format:** [Markdown summary table with JSON-derived cluster and node status details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOGINSIGHT_HOST, LOGINSIGHT_API_TOKEN, curl, and jq.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
