## Description:

Assists clinical research authors by turning supplied section details and notes into Chinese or English IMRaD-style manuscript draft paragraphs with reporting-guideline reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical research authors and medical writing teams use this skill to draft manuscript sections from factual notes they provide. It is intended for language organization and writing self-check reminders, not for creating undisclosed data or unverified conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical research notes may contain patient identifiers, protected health information, unpublished research data, or institution-confidential details.

Mitigation: Use only data authorized for the external model service and prefer de-identified notes.

Risk: API keys passed directly on the command line can be exposed through shell history or process listings.

Mitigation: Avoid putting a real API key directly on the command line when possible.

Risk: Generated draft text could be mistaken for verified scientific conclusions.

Mitigation: Require author review and modification before use, and do not submit model output as an unverified conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-paper-writing-assist)
- [Hivoice MAAS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [JSON containing metadata and Markdown draft text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output includes the requested manuscript section, language, note count, draft text, and writing self-check reminders.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
