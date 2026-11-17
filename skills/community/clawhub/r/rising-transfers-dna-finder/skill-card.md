## Description:

Find cheaper, style-matched footballer alternatives using Rising Transfers vector DNA search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeleon](https://clawhub.ai/user/leeleon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and football recruitment analysts use this skill to find lower-value players with similar playing styles to a named footballer. The skill queries the Rising Transfers Intelligence API and presents ranked alternatives with similarity, club, value, and savings information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player name queries and the RT_API_KEY authentication header are sent to Rising Transfers.

Mitigation: Install and use the skill only if sharing searched player names with Rising Transfers is acceptable, and manage the API key through the agent environment rather than chat text.

Risk: Eligible DNA searches may consume Rising Transfers account credits.

Mitigation: Confirm credit-sensitive searches before use and monitor account usage in Rising Transfers.

## Reference(s):

- [Rising Transfers API](https://api.risingtransfers.com)
- [Rising Transfers API Documentation](https://api.risingtransfers.com/docs)
- [Rising Transfers Pricing](https://api.risingtransfers.com/pricing)
- [ClawHub Skill Page](https://clawhub.ai/leeleon/skills/rising-transfers-dna-finder)
- [Publisher Profile](https://clawhub.ai/user/leeleon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown ranked table with concise follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RT_API_KEY and network access to api.risingtransfers.com; eligible searches may consume Rising Transfers account credits.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
