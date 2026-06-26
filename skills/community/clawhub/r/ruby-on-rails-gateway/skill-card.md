## Description: <br>
Configure and operate a Ruby On Rails Agent Gateway integration from the OpenClaw side for briefing pull workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessewaites](https://clawhub.ai/user/jessewaites) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw to read briefing data from a Rails app through the agent_gateway briefing endpoint. It supports setup checks, scoped read-only pulls, result summarization, and reusable command patterns for reporting or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live bearer tokens and path secrets may be exposed through logs or pasted commands. <br>
Mitigation: Use dedicated read-only tokens where possible, redact secrets in user-visible output, and keep token values out of logs. <br>
Risk: Broad pulls such as full history can retrieve more application data than intended. <br>
Mitigation: Start with narrow resource, period, and latest filters before expanding the query scope. <br>
Risk: A local helper script may run with the user's environment and credentials. <br>
Mitigation: Verify the helper script before running it and prefer non-destructive briefing requests. <br>


## Reference(s): <br>
- [Rails Agent Gateway Usage Reference](references/usage.md) <br>
- [agent_gateway Ruby gem](https://github.com/jessewaites/agent-gateway) <br>
- [ClawHub skill page](https://clawhub.ai/jessewaites/ruby-on-rails-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize JSON briefing responses and redact live secrets in user-visible output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
