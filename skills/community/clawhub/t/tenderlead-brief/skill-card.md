## Description:

Reads a user's TenderLead matched UK tender brief and explains saved BID or SKIP recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlucwright](https://clawhub.ai/user/jlucwright)

### License/Terms of Use:

MIT-0

## Use Case:

TenderLead account holders use this skill to review matched UK procurement opportunities and understand existing BID or SKIP guidance before checking the original notice and eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TenderLead API token could be exposed through chat, files, URLs, or command arguments.

Mitigation: Store the token in protected secret configuration and grant only the documented read scopes.

Risk: Installing an unexpected CLI package could introduce unwanted software into the workflow.

Mitigation: Confirm the pinned TenderLead CLI package and account are expected before installation.

Risk: A saved BID or SKIP recommendation might be mistaken for an eligibility decision.

Mitigation: Check the original tender notice and eligibility before acting on the recommendation.

## Reference(s):

- [TenderLead](https://tenderlead.co.uk)
- [TenderLead brief on ClawHub](https://clawhub.ai/jlucwright/skills/tenderlead-brief)

## Skill Output:

**Output Type(s):** [Guidance, Analysis]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only summaries of existing brief results; missing values remain unknown.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
