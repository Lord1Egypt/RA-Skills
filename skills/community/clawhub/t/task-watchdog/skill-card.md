## Description: <br>
Watches long-running screen tasks, closes nuisance pop-ups, and can alert a user-configured webhook if the task appears to fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnotherJ1](https://clawhub.ai/user/AnotherJ1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users running long desktop jobs use this skill to monitor progress, close disruptive pop-ups, and receive webhook alerts when a task appears stuck or failed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent watches the screen during long-running tasks and may observe private documents, chats, credentials, or unrelated work. <br>
Mitigation: Run it only in a workspace where sensitive or unrelated content is hidden before monitoring starts. <br>
Risk: Automatic pop-up dismissal can click the wrong control if a disruptive dialog is misidentified. <br>
Mitigation: Constrain use to low-risk unattended workflows and keep the skill's stated guardrails: do not terminate processes, do not click cancel on the target task, and avoid restart or install actions. <br>
Risk: Webhook alerts can disclose task state or screenshots to the configured endpoint. <br>
Mitigation: Configure webhook alerts only to an endpoint the user controls and expects to receive task-failure notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AnotherJ1/task-watchdog) <br>
- [Publisher profile](https://clawhub.ai/user/AnotherJ1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Screen observations, UI actions, Screenshots, Webhook notifications] <br>
**Output Format:** [Natural-language agent instructions with optional screenshot capture and webhook alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No shell commands are allowed by the skill artifact; network access may be used for configured webhook alerts.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
