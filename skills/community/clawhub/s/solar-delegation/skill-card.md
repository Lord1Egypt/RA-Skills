## Description: <br>
Delegate longer user-facing text generation to Upstage Solar Pro3 while keeping the primary model for planning and tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to route substantial user-facing drafts, explanations, reports, and summaries to Upstage Solar Pro3 while retaining the primary model for planning and tool use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent model gateway configuration and service restarts can disrupt an existing OpenClaw setup. <br>
Mitigation: Back up existing configuration and require explicit user confirmation before applying persistent changes or restarting services. <br>
Risk: OpenRouter API keys may be exposed if copied into checked-in JSON or shared configuration. <br>
Mitigation: Store API keys through environment variables or a secret store rather than committing credentials. <br>


## Reference(s): <br>
- [Solar Delegation Setup Guide](references/setup-guide.md) <br>
- [Upstage Solar Pro3 model reference](https://openrouter.ai/upstage/solar-pro-3) <br>
- [ClawHub release page](https://clawhub.ai/upstage-deployment/solar-delegation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates only when the current session is enabled and the estimated output meets the configured token threshold; falls back to direct response if delegated generation is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
