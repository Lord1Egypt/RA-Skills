## Description: <br>
Classifies tasks by safety and complexity to route safe, negligible queries to gpt-5.1-codex-mini and escalate critical or executable tasks to gpt-5.3-codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacks3tr](https://clawhub.ai/user/jacks3tr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to conserve Codex oAuth usage by routing only safe, low-impact interactions to a mini model and escalating executable, uncertain, or high-impact work to a stronger Codex model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic escalation may pass the full user prompt to a stronger-model session. <br>
Mitigation: Avoid unnecessary secrets in prompts and require approval or disclosure before escalation in sensitive workflows. <br>
Risk: Model switches may not be announced unless the user asks. <br>
Mitigation: Add a local requirement for explicit escalation disclosure when users need auditability or cost visibility. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jacks3tr/save-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger model escalation for executable, uncertain, or high-impact tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
