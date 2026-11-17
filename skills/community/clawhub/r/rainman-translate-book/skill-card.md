## Description:

This deprecated skill tells users that rainman-translate-book has been renamed to translate-book and provides migration commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this deprecated package as a migration notice for replacing rainman-translate-book with translate-book. It provides uninstall and install commands rather than active translation functionality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated skill instructs users to install a mutable replacement skill globally without pinning or verification.

Mitigation: Install only after reviewing the replacement skill, and prefer a pinned ClawHub version or a specific reviewed Git commit.

Risk: Users may assume the deprecated package verifies or includes the replacement contents.

Mitigation: Treat this package as a migration notice only and review translate-book separately before migrating.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deusyu/skills/rainman-translate-book)
- [Publisher profile](https://clawhub.ai/user/deusyu)
- [Replacement translate-book repository](https://github.com/deusyu/translate-book)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Migration notice only; this deprecated package does not include or verify the replacement skill contents.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
