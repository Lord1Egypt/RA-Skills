## Description: <br>
Operate Slack Web API through UXC with a curated OpenAPI schema, bearer-token auth, and messaging-core guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure bearer-token access and execute Slack messaging-core operations through UXC, including auth checks, channel inspection, conversation and thread reads, message posting, reactions, and limited Socket Mode event intake. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to read from or write to Slack using provided tokens. <br>
Mitigation: Install it only for intended Slack automation and use least-privileged bot tokens by default. <br>
Risk: Writes such as messages and reactions can affect Slack conversations. <br>
Mitigation: Confirm the target channel or thread and message content before executing write operations. <br>
Risk: User-token and Socket Mode access can broaden what the agent can read or receive. <br>
Mitigation: Reserve user-token access for explicit cases and stop Socket Mode subscriptions when finished. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated Slack Web API OpenAPI Schema](references/slack-web.openapi.json) <br>
- [Slack Web API Docs](https://docs.slack.dev/apis/web-api) <br>
- [Slack chat.postMessage](https://docs.slack.dev/reference/methods/chat.postMessage) <br>
- [Slack conversations.history](https://docs.slack.dev/reference/methods/conversations.history) <br>
- [Slack conversations.replies](https://docs.slack.dev/reference/methods/conversations.replies/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Slack Web API operation guidance and UXC command patterns; command results are Slack JSON envelopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
