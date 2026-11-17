## Description:

Vets AI skills for security by checking source, code for red flags, permissions, and risks before installation to ensure safe usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavi296](https://clawhub.ai/user/xavi296)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before installing or running third-party skills to review source, permissions, suspicious patterns, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checklist could be applied too rigidly and reject benign inspection behavior such as decoding encoded content solely for review.

Mitigation: Treat the checklist as conservative guidance and confirm findings against the skill's actual behavior before making the final install decision.

Risk: A vetting report may miss issues if only part of a skill is reviewed.

Mitigation: Review all files in the skill and use the server security summary as the authoritative release risk source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xavi296/skills/test-skill-vetter2)
- [Publisher profile](https://clawhub.ai/user/xavi296)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with checklist sections and optional bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a security vetting report with source, metrics, red flags, permissions, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
