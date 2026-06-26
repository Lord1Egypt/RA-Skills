## Description: <br>
Superpowers-Openclaw provides a 12-skill OpenClaw development workflow for design-before-code, test-driven development, systematic debugging, verification, and structured code review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fenccerece](https://clawhub.ai/user/fenccerece) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill collection to apply a rigorous OpenClaw workflow from idea exploration through planning, implementation, verification, code review, and branch completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collection can broadly shape agent behavior across development tasks. <br>
Mitigation: Review the package before deployment and enable it only in repositories and workflows where this strict development methodology is desired. <br>
Risk: The workflow can lead an agent to run dependency installs, builds, tests, git commits, merges, pushes, and PR commands. <br>
Mitigation: Require explicit user confirmation before package-manager commands or git operations that mutate branches, history, remotes, or pull requests. <br>
Risk: Automatic setup commands may execute project code in the target repository. <br>
Mitigation: Use the skill only in trusted repositories and review setup commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fenccerece/superpowers-openclaw) <br>
- [SuperpowersOpen homepage](https://github.com/superpowers-open/superpowers-open) <br>
- [Original Superpowers methodology](https://github.com/obra/superpowers) <br>
- [README](README.md) <br>
- [Anthropic best practices for writing skills](writing-skills/anthropic-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, checklists, plans, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include design notes, implementation plans, verification evidence, review checklists, git commands, and setup instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
