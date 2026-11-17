## Description:

Assesses task difficulty, estimated time, resource cost, and required skills, while adding clarification and confirmation gates for ambiguous or higher-risk requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq16685283172](https://clawhub.ai/user/qq16685283172)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and users use this skill to estimate the complexity, time, cost, and skill needs of requested work before execution. It is also used to clarify underspecified requests and ask for confirmation before complex or high-risk operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may act as a broad clarification and confirmation gate beyond simple task assessment.

Mitigation: Enable it only where that workflow is desired, and scope interception behavior narrowly before deployment.

Risk: The skill stores original prompts and learned defaults in a local OpenClaw cache.

Mitigation: Review cache contents and retention behavior before use, and avoid storing sensitive prompts unless local storage is acceptable.

Risk: Deletion whitelist and global interception behavior can reduce user review of potentially destructive actions.

Mitigation: Keep destructive operations behind explicit confirmation and avoid enabling broad whitelists without reset and audit controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq16685283172/skills/task-assessor)
- [Assessment methodology](references/assessment-methodology.md)
- [Assessment template](references/assessment-template.md)
- [Task benchmarks](references/task-benchmarks.md)
- [Intent detection logic](references/intent-detection-logic.md)
- [Response parser](references/response-parser.md)
- [Risk whitelist](references/risk-whitelist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown task assessment reports, clarification questions, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request missing details before continuing and may ask for confirmation before L3+ or high-risk tasks.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
