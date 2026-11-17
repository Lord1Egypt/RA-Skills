## Description:

Finds new upcoming IT events worldwide based on user-selected interests and location, avoids duplicates, and helps return official registration or payment links on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankyjo](https://clawhub.ai/user/frankyjo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find upcoming IT events by interest and location, receive concise digests of new events, and retrieve official registration or payment links for previously surfaced events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The weekly setup helper can create a persistent OpenClaw cron job.

Mitigation: Run setup only after confirming recurring delivery is intended, and review the cron schedule, message, timezone, and deletion command before enabling it.

Risk: Helper scripts in the artifact hard-code Ukraine and Ukrainian in their OpenClaw prompts instead of honoring the documented location and language behavior.

Mitigation: Verify the intended location and response language before using the scripts; use manual search behavior when the requested scope differs from the script prompt.

Risk: The skill writes event history under the OpenClaw workspace for deduplication.

Mitigation: Confirm that storing event names, dates, locations, and links in memory/it-events-sent.json is acceptable for the user's workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankyjo/skills/searchitevents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Concise Markdown event digests and short follow-up responses, with optional shell commands for one-time searches or weekly digest setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains event deduplication state in memory/it-events-sent.json when used through the helper scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
