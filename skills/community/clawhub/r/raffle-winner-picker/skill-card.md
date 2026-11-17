## Description:

Picks random winners from lists, spreadsheets, or Google Sheets for giveaways, raffles, and contests. Ensures fair, unbiased selection with transparency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javotillo](https://clawhub.ai/user/javotillo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to select raffle, giveaway, contest, survey, event, or team-assignment winners from lists, CSV files, Excel files, or Google Sheets. It supports single or multiple winners, duplicate prevention, runner-ups, exclusions, weighted draws, and timestamped result records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Participant spreadsheets and Google Sheets may contain personal data such as names, email addresses, entry dates, or comments.

Mitigation: Provide only the columns needed to select and contact winners, avoid sharing full emails or comments publicly, and retain exported winner records only as long as necessary.

Risk: Incorrect eligibility rules, exclusions, duplicate handling, or weighting could produce an invalid or disputed draw.

Mitigation: Review the entrant list, contest rules, exclusions, and weight columns before selection, then save the timestamped result record for auditability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javotillo/skills/raffle-winner-picker)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown or plain text winner-selection summary, with optional exported winner records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include winner details, runner-ups, exclusions, weights, selection method, and timestamped audit notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
