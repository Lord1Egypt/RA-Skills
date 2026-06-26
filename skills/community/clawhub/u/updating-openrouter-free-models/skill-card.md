## Description: <br>
Use when needing to fetch, test, and update OpenRouter free model lists in Claude Code or OpenClaw configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youshu3008](https://clawhub.ai/user/youshu3008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to fetch OpenRouter free model IDs, test model availability, and update Claude Code or OpenClaw model configuration with verified models and fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use sensitive local API tokens for authenticated OpenRouter calls. <br>
Mitigation: Use a dedicated OPENROUTER_API_KEY and unset ANTHROPIC_AUTH_TOKEN unless you intentionally want that token source used. <br>
Risk: The update scripts can change live Claude Code and OpenClaw model configuration. <br>
Mitigation: Back up ~/.claude/settings.json and ~/.openclaw/openclaw.json before running update or test commands. <br>
Risk: The full test workflow may restart OpenClaw and should not be treated as a dry run. <br>
Mitigation: Review commands before execution and run step by step when service interruption or configuration changes need approval. <br>


## Reference(s): <br>
- [OpenRouter API documentation](https://openrouter.ai/docs) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>
- [ClawHub skill page](https://clawhub.ai/youshu3008/updating-openrouter-free-models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary model list files and update local Claude Code or OpenClaw configuration when its scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
