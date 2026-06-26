## Description: <br>
Agent Harness guides AI coding agents through disciplined engineering workflows for planning, execution, verification, review, checkpointing, and multi-agent coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianye](https://clawhub.ai/user/christianye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to make coding agents plan, implement, verify, and review work with explicit quality gates and checkpointing, especially for multi-step or multi-agent tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to launch nested reviewer tools over a repository, which may expose local code or diffs to external review tools. <br>
Mitigation: Use --no-yolo or AUTOREVIEW_YOLO=0 for sensitive repositories, and set --fallback-reviewer none when diffs should not be sent to other reviewer CLIs. <br>
Risk: Automated helper execution with broad local access can affect sensitive codebases if allowed without review. <br>
Mitigation: Review helper commands before allowing an agent to run them automatically and install only when this review posture is acceptable. <br>


## Reference(s): <br>
- [Checkpoint Patterns for Agent Systems](references/checkpoint-patterns.md) <br>
- [MAST Failure Taxonomy for Multi-Agent Systems](references/mast-failure-taxonomy.md) <br>
- [Agent Harness on ClawHub](https://clawhub.ai/christianye/trinity-harness) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with task plans, review notes, code changes, shell commands, and configuration details as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary with the engineering task and should include concrete verification evidence for deliverables.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
