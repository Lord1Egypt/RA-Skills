## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to capture command failures, user corrections, missing capabilities, knowledge gaps, and reusable best practices, then review or promote important learnings into project or agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived information into future agent context and cross-session workflows. <br>
Mitigation: Keep learning files project-scoped, redact secrets, personal data, proprietary content, raw transcripts, and untrusted user text, and only install it when durable agent memory is intended. <br>
Risk: Promoting learnings into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions can make incorrect or untrusted guidance durable. <br>
Mitigation: Require human review before promotion and scan the resulting guidance before deployment. <br>
Risk: Optional global hooks can add persistent self-improvement behavior across sessions. <br>
Mitigation: Avoid global hooks unless the hook scripts have been reviewed and the behavior is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/yuyonghao-self-improving) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-scoped learning files and optional hook configuration when the user enables that workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
