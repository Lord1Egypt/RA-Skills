## Description:

Generates Markdown release notes from git commit history using Conventional Commits, with category grouping, date or version filters, and optional file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to generate categorized release notes or changelog drafts from a repository's git history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated release notes may include misleading or untrusted commit text before publication.

Mitigation: Review and sanitize generated Markdown before publishing, especially for repositories with untrusted contributors.

Risk: The output option writes release notes to a user-supplied path.

Mitigation: Choose output paths deliberately and review generated files before committing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/releasenotes)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown release notes and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Release notes may include commit hashes, authors, generated timestamp, and optional file output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
