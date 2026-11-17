## Description:

RFC Document Assistant helps agents look up, list, search, read, and summarize RFC documents for Internet protocol standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunrenyi](https://clawhub.ai/user/lunrenyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and technical users use this skill to find RFCs by number or keyword, review protocol standards, and request AI-assisted summaries of RFC search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guide includes a remote installer path that can execute mutable code before manual review.

Mitigation: Prefer Homebrew installation or a download-review-execute workflow, and avoid curl-pipe-shell installation on machines with credentials or sensitive files.

Risk: The skill depends on the x-cmd framework being installed and trusted before its RFC commands can run.

Mitigation: Confirm the installation method explicitly and verify the x-cmd loader and binary after installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lunrenyi/skills/x-rfc)
- [Source Repository](https://github.com/x-cmd/skill)
- [x-cmd Installation Guide](data/install.md)
- [x-cmd Release Downloads](https://github.com/x-cmd/release)
- [x-cmd Installer](https://get.x-cmd.com)
- [Conda Package Source](https://conda.prefix.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires x-cmd to be installed and loaded before RFC commands can run.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
