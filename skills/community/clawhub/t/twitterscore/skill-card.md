## Description:

Research, analyze, and track Twitter influence with TwitterScore.io API. Get scores, analyze followers, track growth, and compare accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolaybohdanov](https://clawhub.ai/user/nikolaybohdanov)

### License/Terms of Use:


## Use Case:

External developers and analysts use this skill to query TwitterScore.io for Twitter/X account scores, follower analysis, growth history, bulk account comparisons, and API usage limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried Twitter/X account identifiers and related API usage are sent to the third-party TwitterScore.io API.

Mitigation: Use the skill only for approved targets and confirm that third-party API data sharing is acceptable for the investigation or workflow.

Risk: The TwitterScore API key may persist locally when stored in OpenClaw configuration.

Mitigation: Use a dedicated API key, keep it out of committed files, store it with approved secret-management practices, and rotate it if exposure is suspected.

Risk: Bulk and repeated queries can hit TwitterScore.io rate or plan limits.

Mitigation: Use bulk operations, pagination, caching for repeated lookups, and the limits command to monitor quota before high-volume use.

## Reference(s):

- [TwitterScore ClawHub skill page](https://clawhub.ai/nikolaybohdanov/skills/twitterscore)
- [TwitterScore API Documentation](https://twitterscore.gitbook.io/twitterscore/developers/api-documentation)
- [TwitterScore API pricing](https://twitterscore.io/api/prices?i=9720)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON, CSV]

**Output Format:** [Markdown guidance with shell command examples and text, JSON, or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TwitterScore API key; supports pagination, filtering, bulk checks up to 50 accounts, and CSV exports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
