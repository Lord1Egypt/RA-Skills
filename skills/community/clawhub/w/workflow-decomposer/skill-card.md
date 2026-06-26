## Description: <br>
Decomposes complex work into actionable steps, selects suitable models for each step, tracks workflow progress, and provides troubleshooting options when a step is blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lpj18337105261](https://clawhub.ai/user/lpj18337105261) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to break complex requests into executable workflows, assign an appropriate model to each step, and keep progress visible during multi-step work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow steps or model assignments may be inaccurate or unsuitable for sensitive file changes, deployments, account actions, or public-facing work. <br>
Mitigation: Review generated steps before execution and require human approval for actions that change files, deploy systems, affect accounts, or publish content. <br>
Risk: Optional progress tracking can save task context in local workflow-state JSON files. <br>
Mitigation: Delete local workflow-state files when saved task context is no longer needed. <br>


## Reference(s): <br>
- [Workflow Decomposer README](README.md) <br>
- [Model Capabilities Reference](references/model-capabilities.md) <br>
- [Model-Specific Prompt Guide](references/model-prompt-guide.md) <br>
- [Model Selection Guide](references/model-selection.md) <br>
- [Workflow Decomposition Template](references/workflow-template.md) <br>
- [Workflow Templates](references/workflow-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lpj18337105261/workflow-decomposer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown workflow reports with optional shell commands and JSON workflow-state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include decomposition model, current step, current step model, progress status, and blocker guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
