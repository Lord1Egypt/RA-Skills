## Description: <br>
An MCP server that provides native tools to dynamically search VMware Aria Operations for Logs (Log Insight). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasture-rohit](https://clawhub.ai/user/kasture-rohit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to let an agent query VMware Aria Operations for Logs through an MCP tool for keyword-based VCF log investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Log Insight API token can expose sensitive log access if leaked. <br>
Mitigation: Use a least-privilege token, keep it out of source control and logs, and rotate it if exposure is suspected. <br>
Risk: Returned log messages may contain sensitive or untrusted content. <br>
Mitigation: Install only for agents allowed to access Log Insight data and treat returned log text as untrusted. <br>
Risk: TLS verification behavior may rely on disabled certificate checks. <br>
Mitigation: Prefer proper TLS verification or a trusted CA bundle when deploying this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kasture-rohit/vcf-loginsight-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/kasture-rohit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON configuration examples; MCP tool responses are plain text log summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOGINSIGHT_HOST and LOGINSIGHT_API_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
