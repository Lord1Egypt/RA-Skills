## Description:

Enable or disable a strict engineering workflow for coding tasks enforcing goal clarification, specs, planning, test-driven small steps, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiceman161](https://clawhub.ai/user/spiceman161)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to opt into a structured coding workflow that clarifies goals, writes specs and plans, executes changes in small verified steps, and summarizes outcomes. It is intended for coding, build, and debugging tasks rather than general chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling the mode changes coding-task behavior until it is turned off.

Mitigation: Use the status or disable command when the structured workflow is no longer wanted.

Risk: The trigger examples are bilingual and may be read as exhaustive.

Mitigation: Confirm acceptable equivalent enable, disable, and status phrasing before relying on the mode in a workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spiceman161/skills/superpowers-mode)
- [Plan template](references/plan-template.md)
- [Spec template](references/spec-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local mode-state file when the user enables, disables, or checks the mode.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
