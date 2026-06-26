## Description: <br>
Vigil provides AI agent safety guardrails that validate proposed tool calls before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RobinOppenstam](https://clawhub.ai/user/RobinOppenstam) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent builders use Vigil to check shell commands, file operations, API calls, and other proposed tool calls for common safety risks before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external npm package vigil-agent-safety, so unpinned dependency updates could change the guardrail behavior. <br>
Mitigation: Review and preferably pin the npm package version before installing or deploying the skill. <br>
Risk: The artifact includes dangerous command examples to demonstrate blocked inputs. <br>
Mitigation: Use those examples only as checker inputs and do not execute them directly in a shell or other live tool. <br>
Risk: The wrapper reports ALLOW, BLOCK, or ESCALATE decisions but does not replace review for high-risk tool use. <br>
Mitigation: Configure the package mode deliberately and require human review or stricter controls for ESCALATE results and sensitive tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RobinOppenstam/vigil) <br>
- [Vigil source link](https://github.com/hexitlabs/vigil) <br>
- [vigil-agent-safety npm package](https://www.npmjs.com/package/vigil-agent-safety) <br>
- [Vigil documentation](https://hexitlabs.com/vigil) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-line wrapper returns ALLOW, BLOCK, or ESCALATE decisions with reasons and exit codes.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
