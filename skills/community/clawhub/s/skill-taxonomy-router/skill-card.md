## Description: <br>
Routes user tasks to the most relevant skills using a layered taxonomy, risk model, and minimum-necessary-loading strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzk332266](https://clawhub.ai/user/wzk332266) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify available skills, choose the most specific skill for a task, and avoid loading higher-risk or higher-context tools when a narrower option is enough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad routing policy can over-select powerful or action-capable skills when the task is ambiguous. <br>
Mitigation: Prefer the single most specific relevant skill, choose the lowest sufficient risk level, and ask one clarifying question when ambiguity affects safety. <br>
Risk: Newly downloaded or overlapping skills may be treated as trusted before review. <br>
Mitigation: Classify new skills before use, keep risky operations blocked by default, and prefer canonical skills over overlapping variants. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/wzk332266/skill-taxonomy-router) <br>
- [Change log](artifact/references/change-log.md) <br>
- [Session layer](artifact/references/session-layer.md) <br>
- [Skill classification schema](artifact/references/skill-classification-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with compact routing summaries and optional shell commands for local router maintenance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are policy and routing recommendations; the public artifact is policy-only and host-agnostic.] <br>

## Skill Version(s): <br>
1.5.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
