## Description: <br>
Dispatch tasks to ThinkForce AI agents through its REST API, manage missions and subtasks, and poll for results without server setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ade5791](https://clawhub.ai/user/ade5791) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, decompose, schedule, trigger, monitor, pause, resume, cancel, share, and collaborate on ThinkForce missions and subtasks through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook-triggered subtasks can run agents from external input without documented validation or approval controls. <br>
Mitigation: Keep webhook URLs private, validate senders and payloads before use, and avoid granting webhook-triggered agents sensitive connectors, credentials, or destructive tools without separate approval controls. <br>
Risk: The skill requires an API key that can operate the user's ThinkForce workspace. <br>
Mitigation: Install only when workspace automation is intended, store the API key securely, and review mission actions before allowing high-impact or unattended runs. <br>
Risk: Scheduled or auto-dispatched work can run unattended and may execute subtasks in parallel when sequencing is required. <br>
Mitigation: Use the granular mission and subtask flow for dependent work, verify DAG dependencies before running, and set budget or human-review checkpoints for high-stakes missions. <br>


## Reference(s): <br>
- [ClawHub ThinkForce listing](https://clawhub.ai/ade5791/thinkforce) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mission plans, status summaries, API request examples, and error reports for ThinkForce workflows.] <br>

## Skill Version(s): <br>
2.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
