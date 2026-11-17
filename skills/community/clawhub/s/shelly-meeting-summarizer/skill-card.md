## Description:

Generates concise meeting summaries highlighting key decisions, action items with owners, follow-up dates, and a brief 3-sentence overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudiodrusus](https://clawhub.ai/user/claudiodrusus)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers can use this skill to turn raw meeting transcripts into concise Markdown summaries with decisions, action items, owners, deadlines, and follow-up dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts are sent to Anthropic for processing.

Mitigation: Use only with transcripts your organization permits sharing with Anthropic; avoid confidential, regulated, customer, legal, HR, or security-sensitive meetings unless approved.

Risk: The skill requires an Anthropic API key for outbound API calls.

Mitigation: Use a dedicated key with spending limits, rotate it regularly, and store it in the ANTHROPIC_API_KEY environment variable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/claudiodrusus/skills/shelly-meeting-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown with sections for Summary, Key Decisions, Action Items, and Follow-up Dates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires transcript input and an ANTHROPIC_API_KEY; API response length is configured for concise summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
