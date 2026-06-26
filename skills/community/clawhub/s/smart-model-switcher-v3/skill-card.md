## Description: <br>
Smart Model Switcher V3 helps OpenClaw agents choose and switch among configured third-party model providers based on task type, model availability, fallback behavior, and cost preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure multi-provider model routing for OpenClaw workflows, including task-based model selection, provider fallback, API key validation, and cost-aware selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for multiple paid model-provider API keys and describes automatic external account checks. <br>
Mitigation: Use restricted provider keys with billing caps and review provider permissions before enabling validation or monitoring. <br>
Risk: Automatic fallback routing and model availability checks may send prompts or account metadata to multiple third-party providers. <br>
Mitigation: Avoid sensitive data unless routing is constrained to approved providers and inspect any referenced runtime scripts from a trusted pinned source before running them. <br>
Risk: The security summary notes limited user control and included implementation detail for external validation, fallback routing, monitoring, and periodic checks. <br>
Mitigation: Treat the artifact as requiring review before deployment, and confirm the installed implementation matches the documented behavior before using it in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/davidme6/smart-model-switcher-v3) <br>
- [Project homepage from ClawHub metadata](https://github.com/davidme6/openclaw/tree/main/skills/smart-model-switcher-v3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, shell, and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require configured third-party provider API keys and provider account access.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
