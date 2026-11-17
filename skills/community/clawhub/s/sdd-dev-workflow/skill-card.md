## Description:

A specification-driven development workflow for complex software projects using SDD, Speckit, Claude Code, and OpenClaw autonomous agent patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydearzsy](https://clawhub.ai/user/mydearzsy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a structured SDD workflow for complex application work, from project initialization through specification, planning, implementation, acceptance checks, Git commits, and PR handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill grants agents broad authority to approve prompts, install software, and publish code with insufficient safeguards.

Mitigation: Run it only in a VM or container with test credentials, review every shell installer, avoid bypassPermissions, and require manual confirmation before Git push or PR creation.

Risk: The artifact describes automatic apt, pip, and npm dependency installation during development.

Mitigation: Disable or avoid automatic installs from error text and manually review dependency changes before allowing package installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mydearzsy/skills/sdd-dev-workflow)
- [Installation guide](references/installation.md)
- [Autonomous agent guide](references/autonomous-agent.md)
- [Acceptance protocol](references/acceptance-protocol.md)
- [Git version control guide](references/git-version-control.md)
- [Dependency installation guide](references/dependency-installation.md)
- [Constitution guide](references/constitution-guide.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Spec Kit](https://github.com/github/spec-kit.git)
- [Zhipu Claude Code configuration](https://docs.bigmodel.cn/cn/coding-plan/tool/claude.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create or update project files, run shell commands, install dependencies, perform acceptance checks, and prepare Git commits or pull requests.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
