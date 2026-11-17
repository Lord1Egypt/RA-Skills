## Description:

Routes Claude tasks across Haiku, Sonnet, and Opus tiers based on task complexity to reduce API cost while preserving quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[millibus](https://clawhub.ai/user/millibus)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to choose the lowest-cost Claude model tier that is appropriate for the current task, escalating from Haiku to Sonnet or Opus when complexity warrants it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claude-specific routing guidance may bias agents toward cheaper models for simple tasks where model quality still matters.

Mitigation: Review important, high-stakes, or quality-sensitive tasks and escalate to a stronger model when the task requires deeper reasoning or nuanced judgment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/millibus/skills/smart-model-switching)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with model-routing examples and decision rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Claude-specific guidance for Haiku, Sonnet, and Opus tier selection.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
