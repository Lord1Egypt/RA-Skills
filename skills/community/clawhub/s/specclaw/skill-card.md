## Description: <br>
Spec-driven development framework for OpenClaw. Propose features, generate specs, spawn coding agents, validate implementations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chanbistec](https://clawhub.ai/user/chanbistec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use SpecClaw to manage spec-driven code changes from proposal through planning, delegated implementation, verification, status tracking, and archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change code, run shell commands, create branches or worktrees, and spawn implementation agents with broad authority. <br>
Mitigation: Use it only in trusted repositories, review .specclaw task files and target paths before build or verify actions, and require explicit human approval for code-changing phases. <br>
Risk: Configured test, lint, build, and verification commands execute as shell actions. <br>
Mitigation: Review config.yaml and task-provided commands as executable code before running them, especially in autonomous or scheduled workflows. <br>
Risk: GitHub synchronization can publish proposal, task, and verification content and may use repository credentials. <br>
Mitigation: Keep github.sync disabled unless publication is intended, and use least-privilege GitHub credentials when enabling it. <br>


## Reference(s): <br>
- [SpecClaw ClawHub Page](https://clawhub.ai/chanbistec/specclaw) <br>
- [Agent Prompt Templates](references/agent-prompts.md) <br>
- [Build Engine](references/build-engine.md) <br>
- [Workflow Examples](references/workflow-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown workflow files, shell command sequences, JSON task/config summaries, and agent prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project workflow files under .specclaw and may spawn task-specific coding or verification agents.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
