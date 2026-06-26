## Description: <br>
Coordinates implementer and reviewer subagents to execute independent implementation-plan tasks in the current session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to execute mostly independent tasks from an implementation plan while keeping work in the current session. It guides agents through implementer, spec-compliance review, and code-quality review loops before moving to the next task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can result in automated code edits, test runs, and commits in the active workspace. <br>
Mitigation: Use it on a branch or workspace where automated changes are acceptable, and review resulting commits before merging or releasing. <br>
Risk: Incomplete task context can cause subagents to implement the wrong scope or miss requirements. <br>
Mitigation: Provide full task text and scene-setting context to implementer subagents, then require spec-compliance and code-quality review loops before marking tasks complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with prompt templates and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can lead agents to make code changes, run tests, create commits, and coordinate reviewer subagents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
