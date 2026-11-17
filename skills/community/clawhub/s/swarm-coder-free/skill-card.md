## Description: <br>
Swarm Coder Free coordinates an agent-assisted coding workflow that assigns a fresh subagent for each task and uses a two-stage specification and code-quality review loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to break a coding plan into tracked tasks, delegate each task to a fresh agent context, and require specification and quality review before moving on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may read project plans, modify repository files, run commands, and create local .swarm prompt files. <br>
Mitigation: Use it in a controlled workspace, inspect generated files and diffs, and review changes before committing or submitting code. <br>
Risk: Delegated implementation and review work can produce incorrect, incomplete, or over-broad code changes. <br>
Mitigation: Keep the two-stage review loop, rerun tests, and require human review for decisions that affect architecture, security, or release quality. <br>


## Reference(s): <br>
- [Detailed reference](references/detail.md) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/swarm-coder-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, prompt templates, task status updates, review findings, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .swarm prompt files and guide repository changes through delegated agent tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
