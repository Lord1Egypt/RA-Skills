## Description: <br>
Use when the user wants to create, inspect, update, or run scheduled remote agents in the cloud rather than local cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, inspect, update, or run scheduled remote agent jobs in isolated cloud environments while keeping repository, environment, connector, cron, and prompt details explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scheduled remote trigger can persist and run with cloud account, repository, environment, connector, schedule, and prompt settings. <br>
Mitigation: Confirm the final trigger details and expected side effects before creating, updating, or running the trigger. <br>
Risk: Missing authentication, repository access, or connector assumptions can cause failed or unintended remote runs. <br>
Mitigation: Verify authentication, repository access, environment, and connector assumptions before scheduling or executing a run. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wimi321/remote-agent-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trigger definitions, run or update confirmations, and operational notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
