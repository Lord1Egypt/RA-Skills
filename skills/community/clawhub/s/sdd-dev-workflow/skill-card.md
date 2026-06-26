## Description: <br>
Guides agents through a specification-driven development workflow using SDD, Speckit, Claude Code, project setup scripts, iterative implementation, Git checkpoints, and acceptance checks for complex software projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mydearzsy](https://clawhub.ai/user/mydearzsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run complex application work through specification, clarification, planning, implementation, verification, and release steps. It is intended for project initialization, iterative feature development, dependency setup, Git workflow enforcement, and optional autonomous-agent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may run with broad unattended authority, including long sessions and automatic prompt approval. <br>
Mitigation: Use acceptEdits for normal work and reserve bypassPermissions or dangerously-skip-permissions for disposable containers or virtual machines. <br>
Risk: Automatic dependency installation can execute pip, apt, npm, or remote installer commands in the development environment. <br>
Mitigation: Review or disable automatic installs, run the skill in a dedicated workspace, and inspect installation scripts before execution. <br>
Risk: The workflow can push branches or create pull requests after acceptance checks. <br>
Mitigation: Use least-privilege GitHub tokens and manually review diffs, remotes, secrets, and target branches before any push or PR. <br>
Risk: Required or optional API tokens may be exposed if used in shared or persistent environments. <br>
Mitigation: Scope tokens narrowly, keep them out of committed files and logs, and rotate credentials after sandbox or agent experiments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mydearzsy/sdd-dev-workflow) <br>
- [Installation guide](references/installation.md) <br>
- [Dependency installation guide](references/dependency-installation.md) <br>
- [Autonomous agent mode](references/autonomous-agent.md) <br>
- [Acceptance protocol](references/acceptance-protocol.md) <br>
- [Git version control guide](references/git-version-control.md) <br>
- [GitHub Spec Kit](https://github.com/github/spec-kit.git) <br>
- [Astral uv installer](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide file edits, package installation, Git commits, Git pushes, pull request creation, long-running agent sessions, and acceptance checks.] <br>

## Skill Version(s): <br>
1.4.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
