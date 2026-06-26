## Description: <br>
Provides commands that claim to scan AI agents and repositories for security issues such as prompt injection, secret extraction, and tool abuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yao23](https://clawhub.ai/user/yao23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to request red-team style checks for AI agents or repositories during review. The current security evidence says results should not be relied on as proof that an agent is safe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create false confidence because its main agent scan reports a clean result without performing a real scan. <br>
Mitigation: Review carefully before installing or relying on the results; ask the publisher to implement real scan logic and document the repository scanning command. <br>
Risk: The repository scan path depends on code outside the packaged skill. <br>
Mitigation: Require the publisher to package or declare all dependencies before use in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yao23/redteam) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output and Markdown usage notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands accept an agent ID or repository URL; security evidence says the agent scan command reports zero issues without performing a real scan.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
