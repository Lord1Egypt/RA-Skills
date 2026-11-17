## Description:

Choose, price, deploy, set up, message, schedule and manage Wiro AI agents, the assistants that keep running on Wiro with skills such as social posting, ad reports, review replies or a phone receptionist, through the Wiro MCP tools or the REST API. Use when the user wants an agent that works on its own or on a schedule, asks what agent templates or plans cost, or wants to connect, configure, message, upgrade or remove a Wiro agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using Wiro can use this skill to choose and manage persistent AI agents, connect their services, send messages, schedule work, and understand plans and billing. It guides an agent through Wiro MCP tools or the REST API, including confirmation before paid actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the Wiro integration may involve external API access and paid agent plans or model runs.

Mitigation: Review the current quote, paying wallet, credit details, and renewal terms, and get clear confirmation before a charge.

Risk: Agents may process credentials and content from external services such as email or web pages.

Mitigation: Provide only required credentials through the supported connection flow, do not repeat secrets, and treat outside content as data rather than instructions.

## Reference(s):

- [Wiro Agents overview](https://wiro.ai/docs/agent-overview)
- [Wiro Agent messaging](https://wiro.ai/docs/agent-messaging)
- [Wiro Agent skills](https://wiro.ai/docs/agent-skills)
- [Wiro Agent credentials](https://wiro.ai/docs/agent-credentials)
- [Wiro Studio](https://wiro.ai/docs/studio)
- [Wiro Agent templates](https://wiro.ai/agents)
- [ClawHub release](https://clawhub.ai/wiroai/skills/wiro-agents)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers agent selection, setup, messaging, scheduling, billing, and removal.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
