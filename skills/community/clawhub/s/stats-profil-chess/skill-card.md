## Description:

Fetches public Chess.com ratings and records for a player across rapid, blitz, bullet, and puzzles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugoramon](https://clawhub.ai/user/hugoramon)

### License/Terms of Use:


## Use Case:

Chess players, coaches, and agents use this skill to look up a public Chess.com username and return a concise ratings and record summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Chess.com's public API with the supplied username.

Mitigation: Use only public Chess.com usernames and avoid entering passwords, tokens, or private account data.

Risk: A missing, private, or unreachable profile can produce lookup errors instead of statistics.

Mitigation: Validate the username format before execution and present API or network errors clearly to the user.

## Reference(s):

- [Chess.com public player stats API](https://api.chess.com/pub/player/{username}/stats)
- [ClawHub skill page](https://clawhub.ai/hugoramon/skills/stats-profil-chess)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text summary with rating, record, and error sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a single user-provided Chess.com username and returns only public profile statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
