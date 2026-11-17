## Description:

YYClaw helps an agent check account balance and usage, list available models, and make OpenAI-compatible chat completion calls through the YYClaw API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geniustimee](https://clawhub.ai/user/geniustimee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route model requests through YYClaw, inspect prepaid credit, review usage, and call supported Claude and Gemini models from an OpenAI-compatible client or shell command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid external API and may spend prepaid or on-chain credit when model calls are made.

Mitigation: Confirm with the user before billable model calls and check balance or usage when cost exposure is relevant.

Risk: The security assessment says the skill mishandles API keys and uses broad activation for paid external calls.

Mitigation: Configure YYCLAW_API_KEY as a private environment secret and do not print or paste the key into chat or logs.

Risk: Prompts, account queries, and usage data are sent to YYClaw.

Mitigation: Use the skill only when sending the requested data to YYClaw is acceptable for the user's workflow.

## Reference(s):

- [YYClaw Skill Page](https://clawhub.ai/geniustimee/skills/yyclaw)
- [YYClaw API and Dashboard](https://crypto.yyclaw.cc)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls]

**Output Format:** [Markdown with inline bash, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for external API calls that may consume prepaid or on-chain credit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
