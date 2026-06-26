## Description: <br>
Use when the user wants a prompt or command to run on a recurring interval, such as checking deploys, polling status, or repeating a slash-command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to schedule a recurring prompt or command, run it once immediately, and receive confirmation of the cadence, identifier, expiry behavior, and cancellation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring task could run more often, longer, or differently than intended if the cadence, expiry, or target command is unclear. <br>
Mitigation: Confirm the exact cadence, command or prompt, expiry behavior, and cancellation path before scheduling. <br>
Risk: Repeated execution of sensitive or high-impact commands can amplify mistakes. <br>
Mitigation: Avoid scheduling sensitive or high-impact commands unless the agent platform provides clear permission and rate controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/recurring-loop-runner) <br>
- [Publisher profile](https://clawhub.ai/user/wimi321) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the scheduled cadence, recurring task identifier, expiry behavior, immediate first execution result, and cancellation details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
