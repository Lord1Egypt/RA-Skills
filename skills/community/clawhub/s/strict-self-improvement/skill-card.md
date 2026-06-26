## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayv29](https://clawhub.ai/user/jayv29) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture recurring errors, corrections, feature requests, and useful discoveries as structured memory before promoting durable guidance through human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable learning notes can persist sensitive session context too broadly. <br>
Mitigation: Use project-level setup where possible, keep summaries sanitized, and do not store secrets, customer data, raw prompts, tokens, or full command outputs. <br>
Risk: Global hooks can increase the scope of captured context and reminders. <br>
Mitigation: Prefer explicit project-level hook configuration, avoid global hooks unless reviewed, and disable hooks when they are not needed. <br>
Risk: Promoting unreviewed notes into core agent instructions can introduce incorrect or misleading behavior. <br>
Mitigation: Require human review before promoting anything into SOUL.md, AGENTS.md, TOOLS.md, Copilot instructions, or new skills. <br>
Risk: Hook scripts run with the same permissions as the configured agent environment. <br>
Mitigation: Review scripts before enabling them and install only in environments where the operator accepts that execution posture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayv29/strict-self-improvement) <br>
- [Entry Examples](references/examples.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning, error, feature request, promotion review, and skill scaffold files when the user or configured hooks apply the workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
