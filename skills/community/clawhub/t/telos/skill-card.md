## Description:

TELOS (Telic Evolution and Life Operating System) reads, updates, and backs up a user's local personal life OS so an agent can use missions, goals, beliefs, challenges, and wisdom as context for life-aligned assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sauldataman](https://clawhub.ai/user/sauldataman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use TELOS to initialize and maintain a local personal context system, then let an assistant draw on that context for onboarding, life planning, career decisions, relationship questions, investment choices, and other personal strategy conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive personal material may be stored locally and loaded into assistant context, including through optional persistent hook injection.

Mitigation: Install only if comfortable with local storage and context loading; avoid recording secrets, explicit trauma details, or third-party text without careful review; install the optional hook only after explicit consent and audit review.

Risk: Restore and update workflows operate on local files and can be risky when invoked with arbitrary names or paths.

Mitigation: Review commands before execution, use known backup names and allowed TELOS files, and keep backups plus the update log available for recovery.

## Reference(s):

- [TELOS on ClawHub](https://clawhub.ai/sauldataman/skills/telos)
- [TELOS onboarding workflow](references/onboarding.md)
- [TELOS update workflow](references/update-workflow.md)
- [Daniel Miessler Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- [OpenClaw](https://openclaw.ai)
- [Claude Code](https://claude.com/claude-code)
- [Agent Skills specification](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local TELOS markdown files and may propose or run Bun/Node commands for initialization, updates, backups, restore, history, and optional hook installation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
