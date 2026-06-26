## Description: <br>
Manage Cursor CLI tasks via tmux with security hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucezhu888](https://clawhub.ai/user/brucezhu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to start, monitor, guide, and stop Cursor CLI coding tasks in tmux sessions. It supports long-running development work, status checks, follow-up instructions, and environment diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run trusted background agent commands through a shell and keep authenticated tmux sessions alive. <br>
Mitigation: Install it only on trusted development machines and repositories where Cursor is allowed to access code, review task text and session names carefully, and clean up tmux sessions when finished. <br>
Risk: Use on production systems, shared machines, or secret-heavy workspaces may expose sensitive code or credentials through agent execution or captured tmux output. <br>
Mitigation: Avoid those environments for normal use; prefer a container or another isolated environment for sensitive work. <br>


## Reference(s): <br>
- [ClawHub Use Cursor release page](https://clawhub.ai/brucezhu888/use-cursor) <br>
- [OpenClaw skills homepage](https://github.com/openclaw/skills) <br>
- [Cursor documentation](https://cursor.com/docs) <br>
- [tmux usage guide](https://github.com/tmux/tmux/wiki) <br>
- [OpenClaw ACP documentation](https://docs.openclaw.ai/cli/acp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured tool responses and captured tmux text, often with shell command snippets or status data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session names, task status, command output, and redacted diagnostic text.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata; artifact frontmatter and package metadata report 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
