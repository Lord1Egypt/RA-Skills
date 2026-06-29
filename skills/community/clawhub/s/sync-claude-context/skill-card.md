## Description: <br>
Syncs Claude Code project context at the start of a new session or after significant project changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit and refresh Claude Code project guidance, skills, memory, and settings suggestions after repository changes or time away from a project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local Claude project guidance, rules, skills, or memory files, which could introduce inaccurate or stale instructions. <br>
Mitigation: Use it intentionally and review the resulting git diff before relying on or committing the updated context files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Claude project context files and suggest settings changes for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
