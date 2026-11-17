## Description:

Create a Gmail filter to automatically label, star, or categorize incoming messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this recipe to have an agent prepare Gmail label and filter commands for organizing incoming messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Gmail filter action could remove messages from the inbox or apply unintended labels if the criteria or action JSON is wrong.

Mitigation: Review the proposed filter criteria and actions before running the create command, then verify the resulting filter list.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the gws command-line tool and the gws-gmail skill to list labels, create labels, create filters, and verify filter settings.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
