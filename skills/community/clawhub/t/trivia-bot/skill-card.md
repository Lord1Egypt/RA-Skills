## Description:

Daily trivia questions with scoring, streaks, and category selection. Learn something new every day. Competitive mode for group chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to run daily trivia quizzes, answer multiple-choice questions, and track local scores and streaks across casual quiz sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update a local trivia score JSON file.

Mitigation: Use a dedicated data file path for trivia progress and keep backups of any important local data in the same working area.

Risk: Advertised category, difficulty, group, and leaderboard behavior may not be fully implemented in the artifact.

Mitigation: Validate the installed behavior before relying on those features for group play, scoring workflows, or user-facing quiz sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/trivia-bot)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [Skill README](artifact/README.md)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and plain text responses with JavaScript module behavior for trivia questions, answers, facts, and local score updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores score, total answers, streak, and best streak in a local JSON file when used through the bundled JavaScript module.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
