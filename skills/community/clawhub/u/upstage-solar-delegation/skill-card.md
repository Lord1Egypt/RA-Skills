## Description:

Delegates longer user-facing text generation to Upstage Solar Pro3 while keeping the primary model for planning and tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route long explanations, reports, summaries, and drafts to Upstage Solar Pro3 while retaining primary-model planning and tool orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-form prompts and context may be sent to Upstage or OpenRouter during delegation.

Mitigation: Enable delegation only for sessions whose users understand the external provider route, and avoid use with private, regulated, customer, or multi-user chat content unless reviewed.

Risk: Broad delegation policy changes can affect shared or sensitive sessions.

Mitigation: Keep output-token thresholds conservative, use per-session enablement, and restrict who can change persistent delegation policy.

Risk: Provider API keys could be exposed if stored in checked-in configuration files.

Mitigation: Store Upstage and OpenRouter keys in environment variables or a secrets manager.

## Reference(s):

- [Solar Delegation Setup Guide](references/setup-guide.md)
- [OpenRouter Solar Pro3 Model Reference](https://openrouter.ai/upstage/solar-pro-3)
- [Upstage Console](https://console.upstage.ai)
- [ClawHub Skill Release](https://clawhub.ai/upstage-deployment/skills/upstage-solar-delegation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write markdown or text files when the user asks for saved output; otherwise returns delegated text inline.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
