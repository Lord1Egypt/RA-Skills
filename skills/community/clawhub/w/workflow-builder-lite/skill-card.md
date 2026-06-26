## Description: <br>
Build and execute multi-step workflows with conditional logic, chaining API calls, agent actions, and shell commands into reusable sequences with if/else branching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to plan, save, edit, and execute multi-step workflows that combine API calls, agent actions, shell commands, file writes, and conditional branching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved workflows may include API calls, agent actions, shell commands, or file writes that change external systems or local files. <br>
Mitigation: Review each workflow before approval, and confirm shell commands or file writes only when the exact command or content is expected and trusted. <br>
Risk: Workflow steps can encode incorrect assumptions or unsafe branching logic. <br>
Mitigation: Show workflow steps before execution and report progress after each step so users can inspect behavior and stop or edit the workflow. <br>


## Reference(s): <br>
- [Workflow Builder Lite on ClawHub](https://clawhub.ai/tommot2/workflow-builder-lite) <br>
- [Workflow Builder Lite homepage](https://clawhub.ai/skills/workflow-builder-lite) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with workflow steps, progress reports, and inline shell or file-write proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saved workflows are represented as Markdown files under memory/workflows when approved.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
