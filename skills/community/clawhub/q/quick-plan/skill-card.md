## Description: <br>
Quick Plan turns an implementation discussion into a concise, TDD-driven markdown plan when no finalized spec exists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use Quick Plan to reconstruct intent from the current conversation, inspect relevant project conventions, and draft an implementation plan before any code execution begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during casual planning requests and read project files to prepare a draft. <br>
Mitigation: Use it when an implementation plan is intended, and review the reconstructed intent before relying on the draft. <br>
Risk: The generated plan could encode incorrect assumptions about the user's intent or project conventions. <br>
Mitigation: Review the plan before approving any save to `.beagle/plans/`, and revise unclear scope or acceptance criteria before execution. <br>


## Reference(s): <br>
- [Quick Plan on ClawHub](https://clawhub.ai/anderskev/skills/quick-plan) <br>
- [Fanout exploration brief](artifact/references/fanout-brief.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown implementation plan with task checklists, tests, commands, assumptions, and handoff guidance] <br>
**Output Parameters:** [Conversation context, target slug or path, repository conventions, and explicit approval before saving the plan] <br>
**Other Properties Related to Output:** [Writes a plan only after approval and does not execute the implementation tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
