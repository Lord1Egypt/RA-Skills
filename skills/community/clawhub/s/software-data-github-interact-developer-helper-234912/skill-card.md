## Description:

Helps agent users, skill authors, maintainers, and teams plan and implement GitHub-style workflows on ClawHub, including bug fixes, setup hardening, reliability improvements, and adjacent workflow artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and AI-agent teams use this skill to turn GitHub-style workflow requests into concrete plans, code or documentation artifacts, checklists, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad GitHub, CLI, issue, run, or API wording.

Mitigation: Review the agent's interpreted task and planned actions before allowing repository changes or external GitHub operations.

Risk: Generated workflow or implementation guidance can be incorrect or mismatched to the user's repository constraints.

Mitigation: Require the agent to state assumptions, provide verification commands, and list remaining risks before treating the output as complete.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-234912)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [Guided arqctl connect --auto issue](https://github.com/Elevarq/Arq-Signals/issues/99)
- [Add issue-template config.yml issue](https://github.com/DataDave-Dev/weftmap/issues/70)
- [OpenClaw Ecosystem Digest issue](https://github.com/kakapez/agents-radar/issues/376)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, visible limits, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
