## Description:

Retrieve and review responses from a Google Form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this recipe to retrieve Google Forms response data through configured Google Workspace tooling for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can expose Google Forms responses, which may contain sensitive data.

Mitigation: Run it only with the intended Google Workspace account and confirm the target form before retrieving responses.

Risk: Commands depend on local Google Workspace tooling and configured access.

Mitigation: Verify the gws command-line tool, Google Workspace authentication, and required gws-forms skill are available before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-collect-form-responses)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Google Workspace access and the gws command-line tool.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
