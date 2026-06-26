## Description: <br>
Use when the user wants OpenClaw or Codex to remember their way of working as reusable SOPs, workflows, queues, or "how I do things". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture repeated multi-step work as local SOP/workflow JSON files, match new tasks against saved workflows, and ask for confirmation before reusing or updating a workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved workflow files may contain sensitive process details or tool preferences. <br>
Mitigation: Keep the workflow directory scoped to a trusted project or personal folder and review saved workflows before sharing or reuse. <br>
Risk: A matched SOP could lead to writes, external calls, or other side effects if reused without review. <br>
Mitigation: Require explicit user confirmation before applying a matched workflow unless the current user turn already asks to use the previous SOP or usual process. <br>
Risk: The bundled UI edits local workflow files and should not be exposed unintentionally. <br>
Mitigation: Run the UI on localhost and expose it beyond the local machine only with deliberate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyuqi98/workflowhub) <br>
- [Workflow schema](references/workflow-schema.md) <br>
- [Runtime behavior](references/runtime-behavior.md) <br>
- [Local UI spec](references/local-ui-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text execution briefs, JSON workflow files, and shell commands for local workflow tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses concise local workflow records rather than full transcripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
