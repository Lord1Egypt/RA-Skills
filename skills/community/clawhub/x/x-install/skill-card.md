## Description:

Helps agents and users query x-cmd's install module for software installation methods, package-specific install commands, and supported package listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunrenyi](https://clawhub.ai/user/lunrenyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to look up installation commands for software packages and list packages supported by x-cmd before performing installations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users toward installer flows that download and execute live internet-sourced code.

Mitigation: Prefer Homebrew or a staged download-review-execute flow; avoid direct curl-to-shell installation in sensitive environments.

Risk: Running an installation in an environment with secrets or important local state can increase supply-chain impact.

Mitigation: Use disposable environments with no sensitive credentials for higher-risk install methods, or ask the user to install x-cmd manually.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lunrenyi/skills/x-install)
- [x-cmd Skill Repository](https://github.com/x-cmd/skill)
- [x-cmd Installation Guide](data/install.md)
- [x-cmd Release Binaries](https://github.com/x-cmd/release)
- [x-cmd Install Script Source](https://get.x-cmd.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation safety guidance and command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
