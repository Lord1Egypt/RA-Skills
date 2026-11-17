## Description:

Story generation pipeline skill that supports multi-episode continuous generation, graph management, AI quality checks, human confirmation, and relationship tracking for characters, scenes, and hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexidyg](https://clawhub.ai/user/hexidyg)

### License/Terms of Use:


## Use Case:

External creators and developers use this skill to run a multi-episode story pipeline that drafts episode content, reviews quality, tracks narrative state, and waits for human approval before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted pipeline IDs can make the skill read, write, or delete JSON files outside its intended storage area.

Mitigation: Use only in a constrained workspace until pipeline_id path validation is fixed and destructive graph deletion is removed or explicitly scoped.

Risk: Story inputs and generated episode content are persisted locally in pipeline and graph state files.

Mitigation: Avoid sensitive story material unless local retention is acceptable, and define clear retention and cleanup controls before deployment.

Risk: AI review results drive retry and approval flow.

Mitigation: Require stricter review-result validation and keep human confirmation in the loop before storing graph state or continuing generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexidyg/skills/story-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/hexidyg)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and JSON-like structured text for episode prompts, review prompts, status results, and pipeline state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are designed for iterative episode generation with AI review and human confirmation checkpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
