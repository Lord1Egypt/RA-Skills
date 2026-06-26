## Description: <br>
Records OpenClaw closed-loop events and reactions for duplicate-skipped and proposal-created stale-missions outcomes, and updates trigger fire metadata when appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EcosincronIA](https://clawhub.ai/user/EcosincronIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to log real OpenClaw stale-missions workflow outcomes into event and reaction history. It supports duplicate-skipped and proposal-created records for the stale_missions_alert flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent OpenClaw workflow history to a local Supabase/Postgres database. <br>
Mitigation: Run it only when the local supabase-db container is the intended target and the operator wants real workflow records written. <br>
Risk: Mission titles are stored in persistent event and reaction records. <br>
Mitigation: Avoid using sensitive information in mission titles before running the recording commands. <br>
Risk: The proposal-created command updates trigger fire metadata for the stale_missions_alert flow. <br>
Mitigation: Use the command only for the intended stale_missions_alert workflow and review trigger state before recording production outcomes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against the local supabase-db Postgres container and writes persistent OpenClaw event, reaction, and trigger metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
