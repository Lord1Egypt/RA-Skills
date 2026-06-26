## Description: <br>
Enforces task completion tracking and evidence submission so each task has a clear goal, progress state, next step, and completion proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to keep multi-step work from stalling by requiring progress updates, next actions, completion checklists, and evidence of verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task evidence may expose sensitive or private data if an agent copies raw logs, credentials, or private content into completion notes. <br>
Mitigation: Keep evidence to relative paths, command summaries, artifact identifiers, and non-sensitive verification results; do not include secrets or private data in task logs. <br>
Risk: The workflow depends on agent adherence, so completion evidence can be incomplete if the agent does not follow the required checklist. <br>
Mitigation: Review the DONE_CHECKLIST and EVIDENCE sections before treating a multi-step task as complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Dalomeve/ren-wu-shou-wei-qi) <br>
- [Skill source artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status updates, checklists, evidence summaries, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agent to avoid ending multi-step work with only a plan and to provide concrete evidence when work is complete.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
