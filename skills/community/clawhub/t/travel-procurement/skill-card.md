## Description:

Source, compare, and recommend travel transport options (bus/train/shuttle/taxi/private transfer) from user-provided trip constraints for route planning, quote comparison, and decision-ready recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austineyapp](https://clawhub.ai/user/austineyapp)

### License/Terms of Use:


## Use Case:

Travel planners and assistants use this skill to collect trip constraints, compare public and private transport options, and produce concise recommendations with a fallback option.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A transport comparison may be used to initiate booking, payment, or account-based actions without enough user review.

Mitigation: Require explicit user confirmation before any booking, payment, or account-based action.

Risk: Travel quote requests may expose more personal trip detail than needed.

Mitigation: Provide only the travel details needed to obtain and compare the requested options.

## Reference(s):

- [Option Format](references/option-format.md)
- [Travel Procurement on ClawHub](https://clawhub.ai/austineyapp/skills/travel-procurement)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendations with normalized option details and a decision prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes total price, practical caveat, risk note, and fallback option for each comparison set.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
