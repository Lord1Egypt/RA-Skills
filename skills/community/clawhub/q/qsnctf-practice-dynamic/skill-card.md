## Description:

Fetches QSNCTF leaderboard standings and recent solve activity from public QSNCTF APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, CTF participants, and security training users use this skill to check QSNCTF leaderboard rankings and recent solve activity from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts www.qsnctf.com and prints returned leaderboard or activity data.

Mitigation: Run it only when outbound access to QSNCTF is expected, and review terminal output handling if remote fields need sanitization.

Risk: Dependency installation may introduce environment or supply-chain risk.

Mitigation: Use a virtual environment, avoid elevated privileges, and consider pinning the requests dependency before installation.

## Reference(s):

- [QSNCTF leaderboard API](https://www.qsnctf.com/api/5dboard/playlist)
- [QSNCTF solve activity API](https://www.qsnctf.com/api/5dboard/viewlist)
- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/qsnctf-practice-dynamic)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs QSNCTF leaderboard rows and solve activity returned by the remote APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
