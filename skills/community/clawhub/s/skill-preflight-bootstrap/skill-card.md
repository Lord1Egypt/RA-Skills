## Description: <br>
Initializes a repository-level skill preflight workflow so agents check available skills before starting tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sysundy](https://clawhub.ai/user/sysundy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent maintainers use this skill to bootstrap project-level preflight scripts, hooks, learning logs, and team guidance for repositories that should check reusable skills before work begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bootstrap changes can affect repository-level agent behavior by adding settings, hooks, scripts, documentation, learning files, and an AGENTS.md section. <br>
Mitigation: Run the bootstrap script with --dry-run first, then review the generated .codex/settings.json, .claude/settings.json, AGENTS.md, and hook scripts before applying changes. <br>
Risk: Remote skill search runs an external npx command and may send the task description to that tool. <br>
Mitigation: Avoid including secrets in task descriptions used for remote search or in .learnings notes. <br>


## Reference(s): <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated repository files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write project-level settings, hook scripts, learning files, documentation, and an AGENTS.md section when the bootstrap script is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
