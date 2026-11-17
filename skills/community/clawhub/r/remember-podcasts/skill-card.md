## Description:

Remember Podcasts helps an agent store and search podcast episodes, timestamps, takeaways, and quotable ideas using the BlueColumn API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to log podcast notes with episode details, timestamps, and takeaways, then recall relevant moments later by topic. It is suited for maintaining a searchable listening history and queueing clips or episodes to revisit or share.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast notes, timestamps, queue items, and search queries are sent to BlueColumn's remote service.

Mitigation: Install only when that service is approved for the data involved, and avoid storing secrets, regulated data, or confidential internal notes unless approved.

Risk: The skill requires a BlueColumn API key for remote API calls.

Mitigation: Keep the API key in a secure environment variable or secret manager and avoid embedding it in prompts, notes, or source files.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-podcasts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash examples and API request fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key supplied through a secure environment variable or secret manager.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
