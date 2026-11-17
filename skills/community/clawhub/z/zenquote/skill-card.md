## Description:

Daily inspirational quotes from ZenQuotes.io. Get daily wisdom, random quotes, quote images. Supports automated daily delivery via cron scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisluo5311](https://clawhub.ai/user/chrisluo5311)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch daily, random, multiple, or image-based inspirational quotes from ZenQuotes.io and optionally configure daily delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily delivery setup persists chat_id and account_id values into an automated agent job without identifier validation.

Mitigation: Run setup only with trusted identifiers, inspect ~/.openclaw/cron after setup, and prefer validation and JSON-safe escaping before deployment.

Risk: Quote image mode writes to a fixed temporary path.

Mitigation: Use a private temporary image path and remove generated image files after delivery.

## Reference(s):

- [ZenQuote skill page](https://clawhub.ai/chrisluo5311/skills/zenquote)
- [ZenQuotes API documentation](https://docs.zenquotes.io/)
- [ZenQuotes website](https://zenquotes.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown text, JSON status objects, and local cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote image mode returns a local image path and caption; setup mode writes a daily delivery configuration.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
