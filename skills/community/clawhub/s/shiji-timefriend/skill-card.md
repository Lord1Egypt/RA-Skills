## Description:

时迹 lets an agent record TimeFriend activity, append review journal entries, create and query todos and inbox items, and summarize today's time records through natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masir1128](https://clawhub.ai/user/masir1128)

### License/Terms of Use:

MIT-0

## Use Case:

External TimeFriend users and agent operators use this skill to capture daily activity, diary notes, todos, inbox items, and same-day statistics in TimeFriend without switching out of the agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad conversational triggers may unintentionally send or change personal TimeFriend data such as diary text, todos, inbox items, and time records.

Mitigation: Use explicit TimeFriend commands, review sensitive diary or task content before sending, and confirm write operations when the request is ambiguous.

Risk: The TIMEFRIEND_TOKEN grants authenticated access to the remote TimeFriend service.

Mitigation: Keep the token secret, store it only in the configured environment variable, and rotate it from timefriend.xin if exposure is suspected.

Risk: Records and diary entries may be permanently changed on the remote service.

Mitigation: Verify dates, time ranges, categories, and appended diary text before creating or updating remote TimeFriend data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/masir1128/skills/shiji-timefriend)
- [Publisher profile](https://clawhub.ai/user/masir1128)
- [TimeFriend service](https://timefriend.xin)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown and natural-language responses with authenticated TimeFriend API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TIMEFRIEND_TOKEN environment variable and uses Beijing time (UTC+8) when parsing conversational time expressions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
