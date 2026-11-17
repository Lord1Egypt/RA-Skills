## Description:

Claude终端复用工具 is an instruction-only tmux helper for managing local tmux sessions and windows through agent-guided commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to manage local tmux sessions and windows, plan work, track progress, and coordinate terminal workflows in Chinese or English. It is not intended for complex human performance evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell and file authority for tmux-oriented tasks.

Mitigation: Use it only for explicit tmux session or window operations, and confirm before allowing session closure, terminal paste actions, file writes, or arbitrary shell commands.

Risk: The security summary notes inconsistent scope and API-key disclosures.

Mitigation: Do not provide API keys unless the publisher explains which service is called and why, and prefer environment-scoped credentials when credentials are truly required.

Risk: The artifact describes broad project-management activation alongside terminal control.

Mitigation: Avoid broad autonomous activation; constrain use to local tmux workflow management and review proposed commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tmux-session-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe tmux session state, window operations, execution results, and setup steps.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
