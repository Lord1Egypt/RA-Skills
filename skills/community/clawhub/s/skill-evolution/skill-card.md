## Description:

Skill Evolution helps an agent interactively improve other skills through targeted evolution or fusion of selected external skills, documents, and conversation-derived patterns, with backup and rollback safeguards before edits are applied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pillar-wang](https://clawhub.ai/user/pillar-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this meta-skill to revise installed skills in a controlled workflow: choose an evolution direction, review proposed changes, apply confirmed diffs, test the result, and keep or roll back the edit. It is also used to incorporate reusable guidance from another skill, an external document, or prior conversation feedback into a target skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify other installed skills and persist new behavior into future agent runs.

Mitigation: Use it only for intended skill-editing workflows, inspect the source material and final diff before applying changes, and test the edited skill before keeping the result.

Risk: Document or conversation-derived content can introduce private, incorrect, or unwanted instructions into a skill.

Mitigation: Avoid sensitive inputs, review selected fusion items before insertion, and remove backup logs if they may contain private material.

Risk: A failed or unsuitable edit can leave a target skill in an undesired state.

Mitigation: Rely on the documented backup, rollback, byte comparison, and user-confirmation workflow before retaining edits.

## Reference(s):

- [Evolution Directions](references/evolution-directions.md)
- [Rollback and Fusion Resources](references/resources.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with proposed diffs, tables, inline shell commands, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create backup files and evolution or fusion logs when used to edit a target skill.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
