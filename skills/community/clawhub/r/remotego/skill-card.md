## Description:

Expose any CLI tool as a public web terminal via tunnel. Mirror bash, vim, python, node, or any command in a browser for remote access and collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topcheer](https://clawhub.ai/user/topcheer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose a local CLI session through a browser-accessible public tunnel for remote access or collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local terminal can become reachable from the internet through a public link.

Mitigation: Use only in least-privileged, non-sensitive sessions; avoid privileged shells, production hosts, sensitive repositories, and environments with secrets.

Risk: The skill instructions do not add enough safeguards for public terminal access.

Mitigation: Review the package and command before running, prefer a pinned reviewed package version, and run under a sandboxed or least-privileged account.

## Reference(s):

- [Project homepage](https://github.com/topcheer/claude-remoting)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes npm or npx commands, CLI options, and operational cautions for macOS and Linux systems with Node.js.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
