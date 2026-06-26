## Description: <br>
Create or update recurring chat cron jobs that choose exactly one @ID from a configured list on each run, avoid repeating the previous target, persist the last-picked target in a workspace state file, and post one single-target message to chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakullla](https://clawhub.ai/user/sakullla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and chat administrators use this skill to create or update recurring chat jobs that rotate through a roster and mention one person per run. It helps configure the schedule, target roster, state file, and message constraints for single-target recurring posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring job could post to the wrong chat, run at the wrong time, or use an incorrect roster. <br>
Mitigation: Confirm the delivery target, roster, schedule, timezone, and message style before enabling or updating the job. <br>
Risk: A live test advances the rotation state and posts publicly to the active chat. <br>
Mitigation: Run live tests only when explicitly requested, warn before testing, and reset the memory state file if the rotation needs repair. <br>
Risk: The rotation can repeat or mention unintended IDs if its state file or roster is stale. <br>
Mitigation: Keep the state file under a relative memory path, validate its single-line value against the roster, and reset invalid state to none. <br>


## Reference(s): <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompt skeletons and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cron-job settings, a relative memory state-file path, roster rules, and final-message constraints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence, released 2026-03-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
