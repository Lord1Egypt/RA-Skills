## Description:

Burns LLM tokens toward a target count for AI usage KPI scenarios across OpenAI, Claude, Gemini, and OpenAI-compatible APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neardws](https://clawhub.ai/user/neardws)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a bundled CLI that deliberately consumes LLM token quota against a selected provider and target count. It is intended for cases where the user explicitly wants token usage generated and can accept the resulting provider cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live external API calls that spend paid provider quota or money.

Mitigation: Use dry-run first, choose limited test keys, and set conservative token targets before live execution.

Risk: API keys and custom base URLs can expose credentials or traffic if handled unsafely.

Mitigation: Prefer environment variables over command-line API keys, and use custom base URLs only for endpoints the user fully trusts.

Risk: The security summary notes live API use without strong confirmation, caps, or credential-safety controls.

Mitigation: Review the target, provider, model, and maximum tokens before execution, and interrupt the run if usage exceeds the intended scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neardws/skills/token-sisyphus)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger live provider API calls unless dry-run mode is used.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
