## Description:

yan-watchman is a Rust-based multi-platform AI assistant message watchdog with intelligent importance scoring and adaptive monitoring frequency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eightroad](https://clawhub.ai/user/eightroad)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI assistant operators use this skill to work with a proposed Rust watchdog for monitoring AI assistant messages across Discord, Feishu, and WebChat, with importance scoring and adaptive polling. Reviewers should treat the release as documentation evidence because the claimed Rust implementation files are not present in the artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact claims implementation files that are not included in the source package.

Mitigation: Install only after reviewing the actual source package and confirming the claimed Rust, configuration, and documentation files are present.

Risk: The artifact includes build and workspace-copy commands that could modify a local skills workspace if run automatically.

Mitigation: Require explicit confirmation before running commands, and verify copied files and destination paths before deployment.

Risk: The described behavior involves monitoring messages across communication platforms.

Mitigation: Define privacy, consent, retention, and cleanup rules before using it to monitor messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eightroad/skills/yan-watchman)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package-creation guidance and command snippets; implementation source files claimed by the text are absent from the submitted artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
