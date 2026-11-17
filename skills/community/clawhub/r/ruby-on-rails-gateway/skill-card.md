## Description:

Configure and operate a Ruby On Rails Agent Gateway integration from the OpenClaw side for briefing pull workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessewaites](https://clawhub.ai/user/jessewaites)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure OpenClaw to query a Rails agent_gateway briefing endpoint, validate authentication settings, and generate scoped read-only data summaries for reports or automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can pull sensitive Rails application data broadly when configured with gateway credentials.

Mitigation: Use least-scope resources and periods, avoid period=all unless needed, and keep briefing pulls read-only.

Risk: Bearer tokens and secret-bearing gateway URLs can be exposed through logs, shell history, pasted commands, or shared output.

Mitigation: Redact live credentials, avoid printing tokens, and keep secret-bearing URLs out of user-visible output and logs.

Risk: The local helper script path may point to unaudited code while receiving Rails gateway credentials.

Mitigation: Prefer direct curl or a verified trusted helper, and avoid running the absolute-path helper unless its source and contents are known.

## Reference(s):

- [Rails Agent Gateway Usage Reference](references/usage.md)
- [agent_gateway Ruby gem](https://github.com/jessewaites/agent-gateway)
- [Ruby On Rails Gateway on ClawHub](https://clawhub.ai/jessewaites/skills/ruby-on-rails-gateway)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and concise data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, helper-script command patterns, environment-variable checks, troubleshooting notes, and summarized briefing counts or latest records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
