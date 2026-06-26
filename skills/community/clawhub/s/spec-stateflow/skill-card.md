## Description: <br>
Structured software engineering workflow with state-driven execution for requirement analysis, technical design, task planning, implementation tracking, and session recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naozixu](https://clawhub.ai/user/naozixu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a structured workflow for new features, complex architecture work, multi-module integrations, and cross-module fixes. It guides agents through requirements, design, task breakdown, execution tracking, and recovery after interrupted sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated requirements, designs, or task plans can misstate scope or acceptance criteria if accepted without review. <br>
Mitigation: Review and confirm each workflow phase before proceeding, and inspect generated requirements.md, design.md, and tasks.md before relying on them. <br>
Risk: Continuous operation can advance through implementation tasks without per-task approval when explicitly authorized. <br>
Mitigation: Use continuous operation only with clear task boundaries and stop conditions, and inspect diffs and commits before accepting the result. <br>
Risk: Session recovery can resume from stale or incomplete task state after interruption. <br>
Mitigation: Re-read tasks.md, verify code state, and reconcile any mismatch before continuing work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naozixu/spec-stateflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown workflow documents, task tracker updates, concise guidance, code changes, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update requirements.md, design.md, and tasks.md under the user-defined spec path.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
