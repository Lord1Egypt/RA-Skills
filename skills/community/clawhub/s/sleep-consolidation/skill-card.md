## Description: <br>
Sleep Consolidation helps agents consolidate daily experiences and learnings into structured long-term Markdown memory through micro-rest, NREM, and REM-style workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cshiaa](https://clawhub.ai/user/cshiaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist useful session learnings, preferences, decisions, and synthesized insights across agent sessions. It supports quick daily-log capture, end-of-session consolidation, and memory loading at the start of later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores conversation memory in Markdown files. <br>
Mitigation: Use a constrained workspace, avoid storing secrets or private enterprise data, and review generated MEMORY.md, daily logs, and bank files. <br>
Risk: Claude-backed consolidation modes can send session content to Anthropic. <br>
Mitigation: Prefer manual runs for sensitive sessions and review context before using flush, NREM, or REM modes. <br>
Risk: The current evidence notes missing consent prompts, redaction, retention controls, and safe path validation. <br>
Mitigation: Add explicit consent, redaction, retention, and path-validation controls before broad deployment. <br>


## Reference(s): <br>
- [Memory Schema Reference](references/memory_schema.md) <br>
- [Workspace Layout Reference](references/workspace_layout.md) <br>
- [ClawHub skill page](https://clawhub.ai/cshiaa/sleep-consolidation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown files, JSON responses, Python helper output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes long-term memory, daily logs, and bank files under the configured workspace; Claude-backed modes require ANTHROPIC_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
