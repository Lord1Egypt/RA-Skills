## Description:

Helps volunteer-run recreational leagues plan round-robin fixtures, adjust for absences, track standings, and print match-day schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Volunteer organizers and coaches use this skill to manage fixtures, attendance, fair playing time, match results, and standings for recreational leagues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local league records include player names, absences, and scores.

Mitigation: Protect the local league.json file and share it only with appropriate league organizers.

Risk: The --db option can write league data to a user-provided path.

Mitigation: Check the selected path before running commands that save league data.

Risk: Fairness and call-up features do not replace full league management.

Mitigation: Review schedules and attendance decisions before sharing them with players.

## Reference(s):

- [Rec League Scheduler on ClawHub](https://clawhub.ai/voronindenis5/skills/rec-league-scheduler)
- [Round-Robin Math, Bye Rotation & the Night Re-Flow](references/round-robin-math.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Printable fixtures, match-day sheets, fairness reports, and standings.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
