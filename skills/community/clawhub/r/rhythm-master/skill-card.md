## Description:

Rhythm Master is a browser-based keyboard rhythm game skill where players press arrow keys and the spacebar in time with falling notes, with difficulty levels, combo scoring, judgment ratings, and local or optional online leaderboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dletter2](https://clawhub.ai/user/dletter2)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to play a keyboard rhythm game and test reflexes in a browser. Developers can use its bundled documentation to run the local HTML game or configure an optional online leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player names and scores are stored in the browser for the local leaderboard.

Mitigation: Tell users what is stored locally and avoid collecting sensitive player information.

Risk: The optional online leaderboard guidance can allow unsafe public score submission and remote leaderboard rendering.

Mitigation: Do not deploy the online leaderboard as written; require authenticated or server-mediated score submission, deny public database writes by default, validate all fields, render leaderboard values as text, and add a privacy notice before publishing player data.

## Reference(s):

- [Game Mechanics](references/game_mechanics.md)
- [Leaderboard System](references/leaderboard_system.md)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Cloud Functions Documentation](https://firebase.google.com/docs/functions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and bundled HTML game files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local game stores scores in browser LocalStorage; online leaderboard use requires additional Firebase or server configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
