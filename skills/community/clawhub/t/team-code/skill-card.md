## Description: <br>
Coordinate multiple AI agents as a development team for complex coding projects using isolated workspaces, structured delegation, integration, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multiple coding agents on multi-file features, complex refactors, library implementations, and research reproductions. It helps a lead agent plan dependencies, assign isolated work, integrate changes, and verify the final result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository-wide agent coordination can cause unintended edits, merge conflicts, or data loss when agents are not isolated. <br>
Mitigation: Use separate git worktrees for each subagent, verify each agent is confined to its assigned workspace, and review all changes before integration. <br>
Risk: The workflow includes examples involving pushes, merges, resets, and worktree deletion that can affect project history or local work. <br>
Mitigation: Require explicit user confirmation before destructive or remote-affecting operations, and start from a clean git status or a backup. <br>
Risk: Weak guardrails around delegated coding tasks can allow subagents to modify files outside their intended scope. <br>
Mitigation: Provide each subagent with target files, restricted files, and verification commands, then inspect diffs and run tests before accepting the work. <br>


## Reference(s): <br>
- [Team Code Examples](references/examples.md) <br>
- [Effective Strategies for Asynchronous Software Engineering Agents](https://arxiv.org/abs/2603.21489) <br>
- [async-swe-agents GitHub repository](https://github.com/JiayiGeng/async-swe-agents) <br>
- [ClawHub Team Code release](https://clawhub.ai/simoncatbot/team-code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON task specifications, and workflow patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no API keys or MCP tools are declared in the supplied evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
