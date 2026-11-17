## Description:

AI-powered multisport coaching - get personalized workouts, training plans, and performance analytics for running, cycling, swimming, and triathlon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nftechie](https://clawhub.ai/user/nftechie)

### License/Terms of Use:

MIT

## Use Case:

External users, athletes, developers, and MCP-compatible agent clients use this skill to retrieve workouts, adapt training plans, review performance metrics, chat with an AI endurance coach, and generate quick standalone workouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send workout history, profile details, performance metrics, coach-chat messages, and health-related details to Transition endpoints.

Mitigation: Install only if you trust Transition with that data and review what information the agent will request before using authenticated endpoints.

Risk: TRANSITION_API_KEY grants access to personalized training data and actions.

Mitigation: Keep the API key private, provide it only through trusted environment configuration, and rotate it if it may have been exposed.

Risk: TRANSITION_API_URL can route requests away from the default Transition API if set.

Mitigation: Leave TRANSITION_API_URL unset unless you intentionally configured a trusted endpoint.

Risk: Plan adaptation and third-party pushes such as Garmin can change or export training plan data.

Mitigation: Require explicit user approval before adapting a plan or pushing workouts to external services.

## Reference(s):

- [Transition homepage](https://www.transition.fun)
- [Transition API base URL](https://api.transition.fun)
- [ClawHub skill listing](https://clawhub.ai/nftechie/skills/transition-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses, MCP text results, curl examples, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated features require TRANSITION_API_KEY; the free workout-of-the-day endpoint does not require authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata and MCP server implementation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
