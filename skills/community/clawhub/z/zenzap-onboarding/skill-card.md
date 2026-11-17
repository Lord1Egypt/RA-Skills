## Description:

Bootstrap a complete Zenzap workspace for a human user - create the organization, install the agent as a bot, and invite the human - all via a single API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurdoron-zz](https://clawhub.ai/user/zurdoron-zz)

### License/Terms of Use:


## Use Case:

Agents and their users use this skill to create a Zenzap workspace, install the agent as a bot, invite a human user, configure OpenClaw integration when applicable, and begin initial workspace operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party plugin code.

Mitigation: Verify the Zenzap plugin publisher and version before installation.

Risk: The skill handles API keys and API secrets that could be exposed through shell history, logs, or copied tokens.

Mitigation: Avoid putting API secrets in shell history or logs; prefer a secure secret store or interactive credential entry when available.

Risk: The skill starts ongoing workspace operations such as topic creation, polling, and message-state changes.

Mitigation: Keep human confirmation around topic creation, polling duration, and any message read-state updates.

Risk: The skill tells the agent to load remote API documentation after setup.

Mitigation: Treat remote API documentation as reference material only.

## Reference(s):

- [Zenzap full API reference](https://docs.zenzap.co/llms-full.txt)
- [Zenzap create organization API endpoint](https://api.zenzap.co/v2/agentic/organization/create)
- [Zenzap app](https://app.zenzap.co)
- [ClawHub skill page](https://clawhub.ai/zurdoron-zz/skills/zenzap-onboarding)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown instructions with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes human-confirmation steps, rate-limit information, API request and response examples, plugin configuration guidance, and event-polling instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
