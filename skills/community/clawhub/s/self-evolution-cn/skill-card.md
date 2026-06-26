## Description: <br>
多 agent 自我进化系统，自动记录学习、错误和功能需求，支持多 agent 统计和自动提升 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheney87](https://clawhub.ai/user/cheney87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, knowledge gaps, command failures, and feature requests across OpenClaw agents. It writes shared learning records and can promote repeated patterns into future agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning records may capture chat or tool output that contains sensitive information. <br>
Mitigation: Use a private SHARED_LEARNING_DIR, avoid enabling the skill in sessions that may expose secrets, and periodically inspect or purge LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md, and SOUL.md. <br>
Risk: Automatic promotion can change future agent behavior based on repeated patterns. <br>
Mitigation: Review setup.sh and daily_review.sh before enabling the skill, and set AUTO_PROMOTE_ENABLED=false when promotion should require manual review. <br>
Risk: Shared multi-agent persistence can spread incorrect or unwanted lessons across agents. <br>
Mitigation: Limit shared learning directories to trusted agents and review promoted entries before using them as durable behavior guidance. <br>


## Reference(s): <br>
- [Self Evolution Cn on ClawHub](https://clawhub.ai/skills/self-evolution-cn) <br>
- [Record format](artifact/references/format.md) <br>
- [Promotion mechanism](artifact/references/promotion.md) <br>
- [Hook setup](artifact/references/hooks-setup.md) <br>
- [OpenClaw integration](artifact/references/openclaw-integration.md) <br>
- [Multi-agent support](artifact/references/multi-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown records, hook messages, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent learning, error, feature request, state, and log files in the configured learning directory.] <br>

## Skill Version(s): <br>
2.1.1 (source: SKILL.md frontmatter and server release metadata, released 2026-04-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
