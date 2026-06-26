## Description: <br>
Plan-first workflow for non-trivial work: plan with done criteria, create a tracking issue, package context as documents on the issue, decide where code lives, hand off to an executing agent, verify completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to plan, track, package, route, hand off, execute, and verify non-trivial engineering work. It is intended for tasks with multiple steps, architecture or strategy decisions, risky edits, or iterative bug fixing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plans, design notes, context documents, or tracker comments could expose secrets or sensitive project details. <br>
Mitigation: Do not place secrets in workflow documents or comments; review context before attaching it to an issue or local plan file. <br>
Risk: Tracker updates can target the wrong company, project, repository, or issue if identifiers are stale or copied incorrectly. <br>
Mitigation: Verify target company, project, repository, and issue identifiers before creating or updating tracker records. <br>
Risk: Updating an existing Paperclip document without revision checks could overwrite prior workflow context. <br>
Mitigation: Use the current base revision when updating Paperclip documents and retry after reading the latest document if there is a conflict. <br>


## Reference(s): <br>
- [Workflow Execution Skill](SKILL.md) <br>
- [README](README.md) <br>
- [Tracker Reference: Paperclip](references/tracker-paperclip.md) <br>
- [Tracker Reference: GitHub Issues](references/tracker-github.md) <br>
- [Tracker Reference: None (Local Files)](references/tracker-none.md) <br>
- [Paperclip](https://paperclip.ing) <br>
- [ClawHub Skill Page](https://clawhub.ai/levineam/workflow-execution) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline command and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow plans, tracker updates, handoff instructions, verification summaries, and optional local plan files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
