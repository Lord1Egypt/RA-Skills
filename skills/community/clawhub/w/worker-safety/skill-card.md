## Description: <br>
Operations Safety Reference - Hard Limits apply unconditionally for OpenClaw agent operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yurken](https://clawhub.ai/user/yurken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to enforce rigid OpenClaw safety boundaries, refuse unsafe operations, and offer safer alternatives for workspace, network, runtime, plugin, and group-chat requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may refuse legitimate administrative or cleanup requests when they overlap with protected runtime, plugin, network, or workspace operations. <br>
Mitigation: Review the refusal context and choose a scoped safe alternative, such as workspace-internal paths, authenticated channel setup, explicit allowlist changes, or a smaller selected install set. <br>
Risk: Strict external-instruction rules may block requests to install or execute content from unknown URLs. <br>
Mitigation: Evaluate external material as reference information only and avoid blindly following, installing, or executing URL-provided instructions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown safety guidance and refusal criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install code, call tools, or request sensitive access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
