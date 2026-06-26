## Description: <br>
Reviewer Agent provides an independent review perspective for projects, checking completion, quality, communication, efficiency, maintainability, and concrete improvement actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to perform independent post-completion reviews of OpenClaw skills or projects. It compares claimed work against evidence, scores review dimensions, and produces actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw skill files and writes review reports, which may expose confidential project details in generated review output. <br>
Mitigation: Run it only against intended projects and review generated reports before sharing or retaining them. <br>
Risk: The skill may send a short conclusion through Feishu when notification behavior is configured. <br>
Mitigation: Confirm the notification recipient and project confidentiality before enabling or using notification delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/reviewer-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review reports and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write review reports to /tmp/review-result-{project}.md and workspace review logs; may send a short Feishu notification when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
