## Description:

Mirror a Claude Code terminal in a browser for remote viewing and real-time interaction through a public localhost.run web terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topcheer](https://clawhub.ai/user/topcheer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and collaborators use this skill to share a live Claude Code terminal session in a browser so another person can watch or interact with the session remotely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public interactive terminal session can expose workspace contents or allow remote interaction by anyone who obtains the session URL.

Mitigation: Use the skill only when public remote access is intentional, keep the URL narrowly shared, and stop the session as soon as collaboration is complete.

Risk: Mutable npm or npx package execution can change behavior if the package version is not pinned and reviewed.

Mitigation: Prefer a pinned, reviewed @remotego/remotego version before use.

Risk: Cached terminal output may reveal secrets or sensitive history to new viewers during the session.

Mitigation: Run from a sanitized workspace and avoid displaying secrets before or during the mirrored session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/topcheer/skills/remoting)
- [Project homepage](https://github.com/topcheer/claude-remoting)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes npm or npx commands, optional port/domain/cwd flags, and operational guidance for starting and stopping the mirrored terminal.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
