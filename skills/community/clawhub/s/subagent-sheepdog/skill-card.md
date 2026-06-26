## Description: <br>
Launch verification and watchdog discipline for delegated, backgrounded, browser-driven, and long-running tasks that prevents false "running" claims, clarifies failed_to_start vs failed_after_work_started, and treats heartbeat as a watchdog rather than the main progress loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike-alford](https://clawhub.ai/user/mike-alford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to verify that delegated, backgrounded, browser-driven, or long-running agent work has actually started before reporting it as running. It helps distinguish startup failures from later execution failures and encourages concise, truthful progress updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add unnecessary reporting overhead when applied to tiny direct tasks. <br>
Mitigation: Apply it only to delegated, backgrounded, browser-driven, or long-running work where startup verification matters. <br>
Risk: An agent could still report work as running based only on a handle rather than verified startup evidence. <br>
Mitigation: Require direct checks that the process, child session, or browser workflow exists and reached a usable state before using the running status. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mike-alford/subagent-sheepdog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with status labels and concise progress messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or data collection; the skill guides launch verification, status classification, retry posture, and user-facing communication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
