## Description:

Publishes or updates ClawhHub skills by guiding an agent through skill selection, versioning, changelog collection, confirmation, and `clawhub publish` CLI execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingke2023](https://clawhub.ai/user/xingke2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish or update ClawhHub skills with an explicit version, changelog, slug, display name, and latest tag. It is intended for release workflows that need guided confirmation before running the publish command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish command template can mishandle untrusted folder, slug, name, version, or changelog values and may lead to unintended local command execution.

Mitigation: Review the skill folder, slug, version, and changelog before publishing, and avoid metadata containing shell metacharacters until safer argument handling is used.

Risk: The workflow can publish the wrong skill or version if the selected folder, slug, or current release state is mistaken.

Mitigation: Run inspection first, confirm the release summary with the user, and verify the final published slug and version from CLI output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xingke2023/skills/xingke-clawhub-publish)
- [Publisher profile](https://clawhub.ai/user/xingke2023)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command output summaries, version recommendations, changelog text, and publish status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
