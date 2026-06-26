## Description: <br>
Delegates longer user-facing text generation to Upstage Solar Pro3 while keeping the primary model responsible for planning and tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route long explanations, reports, summaries, and other user-facing drafts to Upstage Solar Pro3 while retaining the primary model for planning and tool orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long prompts, reports, summaries, or chat context may be sent to Upstage or OpenRouter during delegation. <br>
Mitigation: Use the skill only for content appropriate to share with the selected provider, and avoid delegating sensitive data unless that provider use is approved. <br>
Risk: Provider API keys are required for Upstage or OpenRouter access. <br>
Mitigation: Use dedicated provider keys with spending limits where possible, and keep real keys out of shared repositories, logs, screenshots, and generated configuration examples. <br>
Risk: Saved delegated outputs may remain on local disk when the skill writes files. <br>
Mitigation: Prefer inline responses for normal chat output, and save files only to approved paths with appropriate cleanup for sensitive content. <br>


## Reference(s): <br>
- [Solar Delegation Setup Guide](references/setup-guide.md) <br>
- [Upstage API endpoint](https://api.upstage.ai/v1) <br>
- [Upstage console](https://console.upstage.ai) <br>
- [OpenRouter Solar Pro3 model reference](https://openrouter.ai/upstage/solar-pro-3) <br>
- [ClawHub skill page](https://clawhub.ai/upstage-deployment/upstage-solar-delegation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/upstage-deployment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, configuration examples, and optional plain text or markdown files for delegated outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegation is controlled by enabled sessions and an estimated output-token threshold; delegated model outputs are passed through as-is.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
