## Description: <br>
Orchestrate multiple AI coding agents (Claude Code, Codex, Aider) from a single config - launch teams, run workflows, track capacity, and manage handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nutt-adam](https://clawhub.ai/user/nutt-adam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multi-agent coding workflows, including launching agents, sending prompts, running verification workflows, managing handoffs, and landing agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate agents, copy context between workspaces, and run git-changing actions such as landing branches. <br>
Mitigation: Run preflight checks, review generated handoffs and branch-landing commands before use, and perform work in repositories where unintended merges, pushes, or file changes can be reviewed and reverted. <br>
Risk: Context handoff and output capture workflows may include sensitive repository or user information. <br>
Mitigation: Avoid secrets in captured context and inspect handoff packets before applying or sharing them. <br>


## Reference(s): <br>
- [Tutti homepage](https://github.com/nutthouse/tutti) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions return JSON envelopes with command, exit code, data, stdout, stderr, and optional parse or status notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, changelog, action contract, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
