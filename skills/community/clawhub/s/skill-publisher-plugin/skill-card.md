## Description:

Helps agents upload and publish local skills to the ClawHub marketplace, including login checks, release/version decisions, and CLI command references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivian8725118](https://clawhub.ai/user/vivian8725118)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to prepare, version, and publish local skills to ClawHub with CLI-based checks and commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned `npx clawhub` commands may execute an unexpected CLI version.

Mitigation: Use a pinned or vetted ClawHub CLI invocation and review proposed commands before execution.

Risk: Publishing a local skill can unintentionally expose sensitive files or incorrect marketplace metadata.

Mitigation: Verify the local skill path, slug, name, version, tags, and changelog before publishing, and keep secrets out of the skill directory.

Risk: Shell command templates can be unsafe when placeholders are filled from untrusted metadata.

Mitigation: Treat placeholder values as reviewed inputs and quote or reject unsafe values before running generated commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vivian8725118/skills/skill-publisher-plugin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI command templates and publishing status output examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
