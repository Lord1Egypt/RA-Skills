## Description:

Build practical AI image generation and editing workflows inspired by Nano Banana Pro demand, including prompt packs, reference planning, retry rules, and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External designers, marketers, agent users, and skill authors use this skill to turn AI image generation or editing goals into prompt packs, reference plans, QA checks, retry rules, and deployment checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to respond to image workflow requests where a narrower specialist skill would be more appropriate.

Mitigation: Review invocation routing and tighten trigger wording when deploying alongside overlapping image generation or workflow skills.

Risk: Prompt packs and workflow advice can still produce unusable or misleading image outputs because some model and tool limits cannot be solved by prompting alone.

Mitigation: Use the skill's visual QA checklist, bounded retry plan, and explicit model-limit notes before publishing or handing off generated images.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Nano Banana Pro demand signal](https://clawhub.ai/skills/nano-banana-pro)
- [Skill release page](https://clawhub.ai/kyro-ma/skills/work-productivity-nano-banana-workflow-helper-040526)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with prompts, checklists, workflow plans, and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt packs, visual QA checklists, retry frameworks, iteration logs, and deployment or configuration checklists.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
