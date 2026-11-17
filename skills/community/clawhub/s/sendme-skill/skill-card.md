## Description:

Send and receive files peer-to-peer using the sendme protocol from iroh.computer, for sharing files or folders between machines with resumable downloads, integrity verification, and direct peer-to-peer connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muninn-huginn](https://clawhub.ai/user/muninn-huginn)

### License/Terms of Use:


## Use Case:

Developers, operators, and external users use this skill when they need an agent to help send or receive explicit files and folders with the sendme command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the sendme tool from an untrusted source could expose users to supply-chain risk.

Mitigation: Install only from a trusted source, preferably a reviewed or package-manager version.

Risk: Sendme tickets grant access to the shared transfer and can expose files if sent to the wrong recipient.

Mitigation: Treat tickets as access tokens, verify the recipient, and share only files or folders the user explicitly chose.

Risk: Receiving large folders can consume substantial local disk space.

Mitigation: Check available disk space before receiving large folders.

## Reference(s):

- [Sendme on ClawHub](https://clawhub.ai/muninn-huginn/skills/sendme-skill)
- [sendme protocol documentation](https://www.iroh.computer/sendme)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and optional Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sendme tickets and command guidance; tickets should be treated as access tokens.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
