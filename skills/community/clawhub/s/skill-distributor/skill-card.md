## Description:

Generates multi-platform distribution materials for agent skills, including marketplace listings, social promotion copy, GitHub README content, validation guidance, and optional publishing commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmf515](https://clawhub.ai/user/gmf515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill creators use this skill to prepare distribution assets for publishing an agent skill across ClawHub, GitHub, domestic skill marketplaces, and social platforms. It helps validate skill metadata, generate platform-specific copy, and provide publish or push commands when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub publishing flows can expose credentials if tokens are pasted into chat, logs, or remote URLs.

Mitigation: Use GitHub CLI or a credential helper, and do not store tokens in generated commands or repository remotes.

Risk: Generated distribution files and publishing commands can overwrite README content or publish externally before review.

Mitigation: Review diffs before writing or pushing files, confirm target platforms, and pin or preinstall the ClawHub CLI before validation or publishing.

## Reference(s):

- [Platform format reference](artifact/references/platform-formats.md)
- [ClawHub skill listing](https://clawhub.ai/gmf515/skills/skill-distributor)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown files and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes distribution materials under distro/ and may provide publishing commands for GitHub or ClawHub.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
