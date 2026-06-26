## Description: <br>
Helps agents remember repeated ways of working as reusable local SOPs, workflows, and queues, then ask before reusing or saving them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture repeated multi-step work as editable local JSON workflows, match future requests against saved SOPs, and generate concise execution briefs. It is intended for local workflow management with explicit confirmation before reuse or save actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and edits user-chosen local JSON workflow files, so unintended directories or stale workflow content could affect future agent behavior. <br>
Mitigation: Use a dedicated workflow directory such as ./.openclaw/workflows, review saved workflows before reuse, and keep workflows concise and auditable. <br>
Risk: The bundled local UI is intended for local workflow editing and could expose workflow data if bound beyond localhost. <br>
Mitigation: Keep the UI bound to localhost unless network access is intentional and controlled. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zhangyuqi98/workflow-memory-skills) <br>
- [instruction.md](instruction.md) <br>
- [workflow-schema.md](references/workflow-schema.md) <br>
- [runtime-behavior.md](references/runtime-behavior.md) <br>
- [local-ui-spec.md](references/local-ui-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, shell commands, and JSON workflow files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workflow memories and execution briefs; workflow files are editable JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
