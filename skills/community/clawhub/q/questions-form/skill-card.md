## Description:

Present multiple clarifying questions as an interactive Telegram form using inline buttons, selectable options, and an optional free-text escape hatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edonadei](https://clawhub.ai/user/edonadei)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to collect two or more Telegram-based clarifying answers before continuing a task. It is suited for structured requirements gathering, onboarding flows, preference collection, and similar multi-question interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-text answers in Telegram may include sensitive information if users provide it.

Mitigation: Prefer enumerated answer options and avoid asking for passwords, payment data, government IDs, or confidential business secrets.

Risk: Callback payloads can become invalid or ambiguous if question IDs and option values are too long or inconsistent.

Mitigation: Use the documented form:<question_id>:<value> convention, keep question IDs short, and use compact underscore-separated values.

## Reference(s):

- [Form Patterns Reference](references/form-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/edonadei/skills/questions-form)
- [Publisher Profile](https://clawhub.ai/user/edonadei)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON-style Telegram message and button payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram form structure, callback_data conventions, state handling guidance, and collected-answer summaries.]

## Skill Version(s):

1.0.0 (source: server evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
