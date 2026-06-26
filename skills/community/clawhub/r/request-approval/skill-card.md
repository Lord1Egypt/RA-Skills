## Description: <br>
Use Preloop's request_approval tool to get human approval before risky operations like deletions, production changes, or external modifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yconst](https://clawhub.ai/user/yconst) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add human approval checkpoints before destructive, production, external, security, financial, or otherwise sensitive operations. It helps agents gather context, request approval through Preloop, and stop when approval is denied or unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval requests may fail or be bypassed if the Preloop MCP endpoint, token, or approval policy is misconfigured. <br>
Mitigation: Verify the configured Preloop endpoint or package, store a least-privilege token securely, and test that the request_approval tool appears and sends notifications before relying on the skill. <br>
Risk: Sensitive or destructive operations could proceed without adequate human review if approval rules are too permissive. <br>
Mitigation: Set approval policies so destructive, production, external, security, financial, and bulk-change operations require approval in all relevant environments. <br>
Risk: A denied, errored, or timed-out approval response could be misread as permission to continue. <br>
Mitigation: Treat denial, errors, and timeouts as stop conditions, report the result to the user, and only retry when circumstances materially change. <br>


## Reference(s): <br>
- [Setup & Configuration](references/SETUP.md) <br>
- [Detailed Examples](references/EXAMPLES.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Preloop Documentation](https://docs.preloop.ai) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with tool parameters, configuration examples, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Preloop MCP server and approval policy before the request_approval tool can be used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
