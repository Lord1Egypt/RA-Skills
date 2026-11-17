## Description:

Prepare and publish an OpenClaw AgentSkill to ClawHub. Use when a skill directory is ready and needs to be published, or when upgrading an already-published skill to a new version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ham-5on](https://clawhub.ai/user/ham-5on)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to prepare, publish, upgrade, and verify OpenClaw AgentSkill releases on ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install the clawhub CLI globally without pinning a reviewed package version.

Mitigation: Verify the npm package name and publisher, consider pinning to a reviewed version, and avoid elevated privileges unless the installation impact is understood.

Risk: Publishing parameters can update an existing skill owned by the user.

Mitigation: Review the slug, name, version, tags, and changelog before running publish commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ham-5on/skills/publish-guide)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI; publishing commands can update an existing owned skill.]

## Skill Version(s):

1.1.0 (source: _meta.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
