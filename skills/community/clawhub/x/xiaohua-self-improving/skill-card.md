## Description: <br>
小花专用自我迭代技能 - 基于 self-improving-agent 增强，集成 OpenClaw 工作流、MEMORY.md、百度千帆、看想做找四部曲。专为国内部署优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aroooooy](https://clawhub.ai/user/Aroooooy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agent operators use this skill to capture learnings, errors, corrections, and reusable workflow patterns across OpenClaw-oriented sessions. It helps maintain .learnings files, promote durable knowledge into MEMORY.md, SOUL.md, TOOLS.md, or AGENTS.md, and configure reminder hooks for future sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to persist and reuse session learnings broadly, which can unintentionally retain sensitive, personal, or confidential information. <br>
Mitigation: Restrict use to trusted projects and review .learnings, MEMORY.md, SOUL.md, TOOLS.md, AGENTS.md, and daily memory files before allowing persisted content to influence later sessions. <br>
Risk: Bootstrap hooks can re-inject durable notes into future agent context without enough scoping or consent guidance. <br>
Mitigation: Enable hooks only in workspaces where persistent reminders are expected, and disable or narrow hook use for projects involving secrets, credentials, regulated data, or confidential business details. <br>
Risk: Error and learning templates may encourage storing raw command output or operational details. <br>
Mitigation: Redact credentials, tokens, personal data, customer data, and private system details before writing learning entries or promoting them into long-term memory files. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/Aroooooy/xiaohua-self-improving) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Entry Examples](artifact/references/examples.md) <br>
- [Learnings Format](artifact/assets/LEARNINGS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update local learning and memory files when the agent follows the skill guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
