## Description:

Publishes a local skill to ClawHub using specified slug, name, version, path, and optional changelog parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to publish a local skill directory to ClawHub from the command line or from Python code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled bearer token could allow unintended use of a publisher credential if the skill is run as-is.

Mitigation: Revoke the bundled token and require each user to authenticate with their own scoped credential before publishing.

Risk: The publishing workflow can upload unintended local files from the selected skill directory.

Mitigation: Review the target directory and generated file list before executing the publisher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/test-slug)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue network API calls and upload files when executed by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
