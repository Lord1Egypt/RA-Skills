## Description:

Helps OpenClaw or Codex remember repeated multi-step work as reusable SOPs and workflows that can be matched, confirmed, reused, saved, or updated across tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn recurring multi-step tasks into local workflow memory, ask before reusing matched SOPs, and capture or update workflows after useful runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local editor can change persistent workflow instructions that may steer future agent behavior.

Mitigation: Run the editor only on localhost and inspect saved workflow steps before approving reuse.

Risk: Workflow JSON files may be overwritten or updated in ways that are hard to audit later.

Mitigation: Keep backups or version control for workflow files before using save or update flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangyuqi98/skills/workflowhub)
- [Workflow Schema](references/workflow-schema.md)
- [Runtime Behavior](references/runtime-behavior.md)
- [Local UI Spec](references/local-ui-spec.md)
- [Workflow Template](assets/workflow-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow JSON that can influence future agent task handling after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
