## Description:

Extracts shopping and payment intent from the current conversation and returns a structured JSON summary, either by calling an optional local payment-intent summarizer with a session ID or by analyzing the conversation context directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhc1111](https://clawhub.ai/user/xhc1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents handling shopping-related conversations use this skill to determine whether the current conversation contains shopping or payment intent and summarize product, amount, platform, status, and a short Chinese-language summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may summarize shopping or payment-related details from the current conversation.

Mitigation: Confirm users are comfortable with this conversation-level summarization before installing or invoking the skill.

Risk: When the optional payment-intent command path is used, unsafe command construction could expose the session ID or alter the intended command.

Mitigation: Run payment-intent through a trusted executable path, validate the session ID, and avoid shell string interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhc1111/skills/shopping-intent-extractor)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain JSON object without a Markdown code fence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON includes hasIntent, intentType, product, amount, platform, status, and a concise Chinese summary; analysis is limited to the current conversation.]

## Skill Version(s):

1.0.3 (source: server release metadata, released 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
