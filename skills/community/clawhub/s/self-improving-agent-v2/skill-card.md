## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanghuaqi](https://clawhub.ai/user/fanghuaqi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, user corrections, feature requests, and reusable lessons in project learning files. It also guides promotion of durable learnings into agent memory or instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files and promoted prompt files can retain sensitive session content. <br>
Mitigation: Keep learning storage project-scoped and redact secrets, customer data, raw prompts, credentials, and unrelated session content before saving or sharing. <br>
Risk: Optional hooks can run broadly and inject reminders into agent sessions. <br>
Mitigation: Review the hook scripts before enabling them and prefer project-level activation over global activation unless broad behavior is intended. <br>
Risk: Incorrect or overly broad learnings can be promoted into future agent instructions. <br>
Mitigation: Review promoted entries for accuracy, scope, and relevance before adding them to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or similar prompt files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fanghuaqi/self-improving-agent-v2) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent learning entries and optional hook reminders; no model or API output is generated directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
