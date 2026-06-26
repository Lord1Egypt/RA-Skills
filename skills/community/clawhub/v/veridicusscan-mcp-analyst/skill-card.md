## Description: <br>
Guides agents through VeridicusScan MCP scans of prompts, local files, public HTTPS URLs, and runtime-defense workflows such as memory ingestion, selective disclosure, tool scoping, plan guarding, and action gating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabaaziz991-hash](https://clawhub.ai/user/sabaaziz991-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, IT, recruiting, compliance, and developer users can use this skill to scan selected prompts, files, websites, and agent-runtime flows through a trusted VeridicusScan MCP bridge. The skill helps summarize risk bands, findings, coverage limits, redaction behavior, and runtime-defense decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected URLs, files, prompts, or runtime data to a VeridicusScan MCP bridge for analysis. <br>
Mitigation: Connect only a trusted bridge and scan only the specific inputs the user intends to share. <br>
Risk: Memory ingestion and selective-disclosure test inputs may contain sensitive information. <br>
Mitigation: Treat memory and disclosure inputs as sensitive, and summarize redaction or sanitized-only behavior when it appears in results. <br>
Risk: Public URL scans are intentionally limited to public HTTPS destinations and can reject private, loopback, local, or internally resolved targets. <br>
Mitigation: Report exact MCP error codes such as non_public_network_url and explain that these blocks are intentional network boundaries. <br>


## Reference(s): <br>
- [VeridicusScan MCP methods](references/mcp-methods.md) <br>
- [AI job application screening](https://veridicuscan.app/ai-job-application-screening) <br>
- [Local MCP automation for AI agents](https://veridicuscan.app/mcp-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, API Calls] <br>
**Output Format:** [Markdown summaries with MCP method names, risk fields, findings, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exact MCP error codes, redaction notes, coverage limits, and exported report guidance when relevant.] <br>

## Skill Version(s): <br>
0.1.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
