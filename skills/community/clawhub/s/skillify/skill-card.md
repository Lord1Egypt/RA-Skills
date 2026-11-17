## Description:

Part of the Overpowered skill suite, Skillify helps an agent turn a qualified or otherwise proven repeatable workflow into a portable Agent Skill with concise instructions, trigger-focused metadata, gotchas, and evals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-skill authors use this skill to package proven workflows into reusable, portable Agent Skills. It is intended for workflows with real execution or evaluation evidence, not for saving arbitrary conversations or permanently installing one-off procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills may preserve incorrect assumptions, project-specific details, or unsupported claims if the source workflow is not reviewed.

Mitigation: Review the generated skill package, confirm the workflow evidence, and verify that evals distinguish the intended reusable behavior before deployment.

Risk: A one-off procedure could be treated as a proven reusable skill without enough evidence.

Mitigation: Require Skill Academy qualification or equivalent reuse evidence before labeling the skill proven or graduated.

## Reference(s):

- [Overpowered skill suite](https://github.com/raguets/overpowered)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Agent Skill package guidance and file contents, typically including SKILL.md and evals.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before deployment and should not claim a workflow is proven unless evidence supports that status.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
