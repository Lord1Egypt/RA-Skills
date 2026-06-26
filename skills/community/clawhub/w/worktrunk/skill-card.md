## Description: <br>
Git worktree manager for parallel AI agent workflows. Use when the user needs to manage multiple working directories for parallel development, create feature branches with isolated environments, or run multiple AI agents concurrently. Covers `vx worktrunk` and `vx wt` commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to create, switch, list, merge, and clean up isolated Git worktrees for parallel development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merge and remove workflows can delete local worktrees or branches, including work that has not been preserved elsewhere. <br>
Mitigation: Check `git status`, confirm needed local work is saved, and use keep or dry-run-style options where available before running merge or remove commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/worktrunk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Git worktree commands, vx command examples, and hook configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
