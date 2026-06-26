## Description: <br>
Captures learnings, errors, corrections, and feature requests so coding agents can improve future workflows and promote durable knowledge to workspace memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record command failures, user corrections, missing capabilities, and reusable lessons, then promote proven patterns into workspace memory or new skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs and promoted prompt files may capture sensitive workspace, user, or command context. <br>
Mitigation: Set explicit log locations, review entries before saving or promotion, and redact secrets, personal data, customer data, raw prompts, command arguments, and environment details. <br>
Risk: Broad hooks or cross-session sharing may spread unreviewed guidance across agent sessions. <br>
Mitigation: Avoid global empty-match hooks, enable hooks only in intended workspaces, and require human review before shared or promoted learnings become durable instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bingze00000/self-improving-agent-jarvis) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Self-Improvement Examples](references/examples.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace learning logs and skill scaffolds when an agent follows the guidance.] <br>

## Skill Version(s): <br>
3.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
