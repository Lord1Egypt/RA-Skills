## Description: <br>
Windsurf AI IDE guide for Cascade Agent, AI Flow, rules configuration, keyboard shortcuts, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as practical guidance for working with Windsurf's Cascade Agent, AI Flow completion, inline edits, chat panel, rules files, and shortcuts. It supports scaffolding, refactoring, rapid prototyping, and exploring unfamiliar technology stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Windsurf Cascade can modify files and run terminal commands when used in Write mode. <br>
Mitigation: Prefer Chat mode or scoped @file/@folder context for sensitive work, and review diffs plus dependency, terminal, and git changes before accepting them. <br>
Risk: Global Windsurf rules can affect AI behavior across future projects. <br>
Mitigation: Keep global rules minimal, review them periodically, and place project-specific requirements in local .windsurfrules files. <br>
Risk: Sensitive files or secrets could be exposed through broad project context. <br>
Mitigation: Exclude secrets from the workspace context, keep sensitive files in .gitignore where appropriate, and avoid giving the agent unnecessary project-wide access. <br>


## Reference(s): <br>
- [ClawHub Windsurf skill page](https://clawhub.ai/zhangifonly/windsurf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with tables and inline code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Windsurf rules examples, keyboard shortcuts, feature comparisons, and best-practice checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
