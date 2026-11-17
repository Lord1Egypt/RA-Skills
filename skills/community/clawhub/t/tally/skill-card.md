## Description:

Create and edit Tally forms via API for building surveys, feedback forms, and questionnaires programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujesyoga](https://clawhub.ai/user/yujesyoga)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create, inspect, update, and back up Tally forms through the Tally API when building surveys, feedback forms, or questionnaires.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Tally API key that may grant access to account forms.

Mitigation: Keep the key least-privileged where possible, store it privately, and install the skill only when the agent should work with the Tally account.

Risk: The skill can retrieve submissions or update live forms.

Mitigation: Access submissions only when authorized, duplicate or back up forms before PATCH updates, and verify form state after changes.

Risk: Example commands use fixed /tmp file paths for backup and form JSON files.

Mitigation: Replace fixed /tmp paths with private files controlled by the user or deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujesyoga/skills/tally)
- [Tally forms API endpoint](https://api.tally.so/forms)
- [Tally form detail and update endpoint](https://api.tally.so/forms/{id})
- [Tally form submissions endpoint](https://api.tally.so/forms/{id}/submissions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Tally API block structures, endpoint examples, and update workflow guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
