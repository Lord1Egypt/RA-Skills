## Description:

Connects and operates Zrise tasks through XML-RPC with approval-based AI workflows and result writeback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khoabd](https://clawhub.ai/user/khoabd)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Zrise can use this skill to fetch tasks, route work to AI agents, collect approvals, post comments or results, fill timesheets, and move task stages. It is intended for controlled task automation where Zrise credentials and workflow approvals are managed by the deploying team.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact task automation can modify Zrise task state, comments, and timesheets.

Mitigation: Install only in a controlled environment, use a least-privileged Zrise account, keep approval gates active, and test first against non-production Zrise tasks.

Risk: Weak network, credential, and permission safeguards could expose the workflow UI or credentials.

Mitigation: Require WORKFLOW_UI_TOKEN, bind the UI to 127.0.0.1, restore TLS certificate verification, and remove permission-bypass execution modes before operational use.

Risk: Mutable setup steps and dependencies can change behavior after installation.

Mitigation: Avoid installing executables from /tmp or using mutable latest dependencies; pin and verify dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khoabd/skills/zrise-connect-release)
- [Artifact README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Workflow templates guide](artifact/docs/WORKFLOW_TEMPLATES.md)
- [Workflow UI guide](artifact/docs/WORKFLOW_UI_COMPLETE.md)
- [Team onboarding guide](artifact/docs/TEAM_ONBOARDING.md)
- [Telegram integration guide](artifact/docs/TELEGRAM_INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML-formatted Zrise comments, JSON status objects, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Zrise tasks, comments, stages, timesheets, and local workflow state when run with configured credentials.]

## Skill Version(s):

3.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
