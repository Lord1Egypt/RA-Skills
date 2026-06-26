## Description: <br>
Semantically optimizes conversation history and large text blocks through the Trunkate AI API, including optional OpenClaw hooks for proactive context management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[titus-choi](https://clawhub.ai/user/titus-choi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to compress long agent histories, large logs, and oversized text blocks while preserving task-relevant context for continued work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation history and project context may be sent to the Trunkate API, especially when the always-on PreRequest hook is enabled. <br>
Mitigation: Prefer manual CLI use or disable the PreRequest hook unless the workspace is appropriate for third-party processing; avoid sensitive or regulated sessions. <br>
Risk: The hook can replace agent memory with optimized text without clear per-use control. <br>
Mitigation: Review or disable automatic history replacement, set conservative thresholds and budgets, and keep raw-history fallback available when exact context matters. <br>
Risk: The skill requires a TRUNKATE_API_KEY for a third-party service. <br>
Mitigation: Scope, rotate, and store the API key only in trusted environments; do not commit it to project files. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/titus-choi/trunkate-ai) <br>
- [Optimization examples](references/examples.md) <br>
- [Hooks setup](references/hooks-setup.md) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Proactive context hook](hooks/openclaw/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; optimized history text from the CLI or hook output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When OpenClaw hooks are enabled, the skill may emit OPENCLAW_ACTION:SET_HISTORY to replace session history with optimized text.] <br>

## Skill Version(s): <br>
0.20.0 (source: server release metadata and version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
