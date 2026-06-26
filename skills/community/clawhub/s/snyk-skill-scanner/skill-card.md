## Description: <br>
Guides agents through scanning local skills, MCP servers, and agent tools for security issues using Snyk's agent scanner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SwiftKing100](https://clawhub.ai/user/SwiftKing100) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to run local scans of agent components and interpret scanner findings before installing or publishing skills, MCP servers, or tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented examples execute external tooling with uvx and may fetch the latest scanner package at runtime. <br>
Mitigation: Verify the snyk-agent-scan package source before use and pin a known scanner version instead of using @latest when reproducibility matters. <br>
Risk: Scanning broad local paths can expose more files to the scanner than intended. <br>
Mitigation: Run scans only against directories selected for audit, such as the specific skill or MCP server path under review. <br>


## Reference(s): <br>
- [Snyk agent-scan issue code reference](https://github.com/snyk/agent-scan/blob/main/docs/issue-codes.md) <br>
- [ClawHub release page](https://clawhub.ai/SwiftKing100/snyk-skill-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/SwiftKing100) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with bash command examples and result interpretation tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scanner output or JSON when the user runs the documented snyk-agent-scan commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
