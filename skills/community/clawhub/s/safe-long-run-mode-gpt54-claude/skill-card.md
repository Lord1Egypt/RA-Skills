## Description: <br>
Operate long-running AI tasks safely across GPT-5.4 and Claude by using model selection rules, phased execution, checkpoints, resumable workflows, API throttling discipline, and subagent isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwiley1989](https://clawhub.ai/user/bwiley1989) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to manage long-running tasks that may touch multiple files, systems, external APIs, browser automation, Azure, Orgo, or subagents. It helps the agent plan work in phases, preserve resumable checkpoints, choose between GPT-5.4 and Claude, and control API usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint notes, local artifacts, or screenshots created during long tasks may accidentally capture sensitive information. <br>
Mitigation: Tell the agent where checkpoint files may be saved, avoid storing secrets in notes or screenshots, and review saved artifacts before sharing them. <br>
Risk: Subagents or external-system actions can make changes that are hard to inspect during a long autonomous run. <br>
Mitigation: Review subagent plans and external-system actions before they make changes, serialize risky writes, and keep each phase resumable. <br>


## Reference(s): <br>
- [Safe Long-Run Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with checklists and routing matrices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for phased execution, checkpointing, model routing, subagent isolation, API throttling, and resume handoff.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
