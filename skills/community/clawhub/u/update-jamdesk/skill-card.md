## Description:

Guides an agent through updating Jamdesk customer-facing documentation for user-facing API, CLI, UI, configuration, and component changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbourne1](https://clawhub.ai/user/gbourne1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to plan, write, verify, and optionally commit Jamdesk documentation updates after user-facing product changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit a configured external Jamdesk documentation repository.

Mitigation: Review the proposed scope, branch choice, generated diff, and any commit or push prompt before approving changes.

Risk: Broad documentation requests may activate the workflow.

Mitigation: Confirm that the requested change affects user-facing documentation before allowing file edits.

## Reference(s):

- [Jamdesk homepage](http://www.jamdesk.com)
- [Jamdesk documentation](https://jamdesk.com/docs)
- [Jamdesk components documentation](https://jamdesk.com/docs/components)
- [ClawHub skill page](https://clawhub.ai/gbourne1/skills/update-jamdesk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update documentation files and project configuration when the user approves the workflow.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
