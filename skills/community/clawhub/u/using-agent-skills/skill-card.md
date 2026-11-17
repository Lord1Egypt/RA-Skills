## Description:

Check for applicable skills before responding to development tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to choose the applicable workflow skill before and during software development tasks, including planning, implementation, testing, review, and release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced workflow skills may be missing or untrusted in the running agent environment.

Mitigation: Confirm required downstream skills are installed from trusted sources before relying on the routing guidance.

Risk: The artifact text is partially mojibake-corrupted, which can make instructions harder to audit.

Mitigation: Review the skill text for readability and repair encoding issues before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/using-agent-skills)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with decision trees and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; output depends on installed and trusted downstream skills.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
