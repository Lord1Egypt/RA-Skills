## Description:

Spawns a specialized sub-agent to monitor Reddit and optimize for GEO. Runs on a scheduled cron job (9 AM/6 PM default) to deliver lead drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muhammedilyasy](https://clawhub.ai/user/muhammedilyasy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to monitor recent Reddit discussions, generate verified lead digests, and draft brand-aware replies for human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent scheduled agent with broad web and browser access may run outside the user's expected operating window or permissions.

Mitigation: Confirm the cron schedule and timezone before enabling the skill, restrict browser or posting tools where possible, and keep a clear pause or delete path for the background job.

Risk: Public Reddit posting can affect brand reputation if drafts are posted without review.

Mitigation: Require explicit approval for every post and schedule change before using browser automation.

## Reference(s):

- [Reddit Marketing and GEO Skill on ClawHub](https://clawhub.ai/muhammedilyasy/skills/reddit-marketing-geo)
- [Publisher website](https://ilyasy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown digest with verified Reddit URLs, fetched titles, comment counts, and draft replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before posting; recurring schedule defaults to 9 AM and 6 PM.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
