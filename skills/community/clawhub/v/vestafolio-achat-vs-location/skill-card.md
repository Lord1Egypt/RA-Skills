## Description:

Compare final net wealth between buying a primary residence with a mortgage and renting while investing savings, over a chosen horizon, using Vestafolio's simulator API, after asking the simulator's questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-planning assistants use this skill to compare a French primary-residence purchase against renting while investing savings. The skill gathers scenario assumptions, obtains consent, calls Vestafolio's simulator API, and explains the returned buy-versus-rent result and limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends financial scenario inputs to Vestafolio's external API after user approval.

Mitigation: Summarize the exact fields and values before transmission and proceed only after the user agrees.

Risk: Over-sharing could expose sensitive personal or account information that the simulator does not need.

Mitigation: Send only relevant simulator fields and omit names, addresses, account identifiers, credentials, files, and conversation history.

Risk: Buy-versus-rent recommendations can change materially when assumptions such as appreciation, investment return, rent growth, or horizon change.

Mitigation: Ground conclusions in the API result, state assumptions and limits, and present the output as an estimate rather than financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-achat-vs-location)
- [Vestafolio simulator API schema](https://www.vestafolio.com/api/tools/v1/achat-vs-location)
- [Vestafolio interactive simulator](https://www.vestafolio.com/simulateurs/achat-vs-location)
- [Vestafolio website](https://www.vestafolio.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell commands for API execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before transmitting summarized simulator inputs to Vestafolio.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
