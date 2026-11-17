## Description:

Skill Publish Adapter Real helps developers validate, repair, and publish ClawHub/OpenClaw skill packages with guidance and shell-command workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to check skill package quality, repair common packaging issues, and prepare publishing workflows for ClawHub or GitHub. It is intended for normal ClawHub release workflows, with additional review required before using it in real projects or CI jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users and CI jobs to run an unverified GitHub script.

Mitigation: Review the script before use, or require a bundled script pinned to an immutable commit with checksum or signature verification.

Risk: The packaged metadata does not match the described adapter behavior.

Mitigation: Compare the packaged files with the intended adapter before installation or release use.

Risk: Publishing automation can accidentally package or expose sensitive files.

Mitigation: Review the exact release package contents and exclude secrets, credentials, and local-only files before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/skills/skill-publish-adapter-real)
- [Publisher profile](https://clawhub.ai/user/puppetcat-fire)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and release workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, jq, tar, and git according to server-resolved ClawHub metadata.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
