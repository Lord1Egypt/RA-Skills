## Description:

Helps agents handle archive and compression tasks such as compressing, extracting, packaging, listing contents, and viewing archive files across formats including zip, tar, gz, 7z, rar, zst, xz, and bz2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunrenyi](https://clawhub.ai/user/lunrenyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users can use this skill when an agent needs to compress files, extract archives, list archive contents, or prepare backup packages with x-cmd archive commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guide includes an auto-install option that executes mutable remote shell code directly on the user's machine.

Mitigation: Prefer Homebrew or a download-review-verify workflow, and avoid the auto-install option on machines with credentials, source code, or other sensitive data.

Risk: The skill depends on x-cmd as an external tool before archive operations can be performed.

Mitigation: Install x-cmd only after confirming the install method and verifying that the environment is appropriate for the selected installation path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lunrenyi/skills/x-zuz)
- [x-cmd website](https://www.x-cmd.com)
- [x-cmd skill repository](https://github.com/x-cmd/skill)
- [x-cmd installation guide](data/install.md)
- [x-cmd releases](https://github.com/x-cmd/release)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces archive workflow guidance and x-cmd command suggestions; command execution depends on the hosting agent and user consent.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
