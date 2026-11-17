## Description:

Helps agents connect to Typeform through Maton to manage forms, retrieve responses, and access insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams working with Typeform use this skill to inspect forms and responses, create or update forms with approval, and set up approved automated Typeform actions through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account connections and writes can change Typeform data.

Mitigation: Get explicit approval for each new connection or write; verify the account, target, and intended change first.

Risk: Hosted functions, triggers, and destinations can create ongoing automated data flows.

Mitigation: Review the function, schedule, destination URL, and data shared; approve each automation and destination separately.

Risk: Raw API-key use may expose account credentials or response data.

Mitigation: Prefer managed login; handle API keys securely and share only the response fields needed for the task.

## Reference(s):

- [Typeform API overview](https://www.typeform.com/developers/get-started)
- [Typeform forms API](https://www.typeform.com/developers/create/reference/retrieve-forms)
- [Typeform responses API](https://www.typeform.com/developers/responses/reference/retrieve-responses)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [Typeform skill release](https://clawhub.ai/byungkyu/skills/typeform)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands, code, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a Maton account with an authorized Typeform connection.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
