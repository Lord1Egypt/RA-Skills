## Description:

Converts an explicitly named Simplified Chinese article into its Traditional Chinese twin and keeps both files synchronized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and article authors use this skill to create or update a Traditional Chinese companion for a named Simplified Chinese article, with reciprocal links between the files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write files and invoke a shell command; runtime permission limits were not verified, so an unintended target or existing twin could be affected.

Mitigation: Name the source and output explicitly, check whether the Traditional twin already exists, and review all file changes after conversion.

Risk: Traditional conversion can choose the wrong form for ambiguous characters or alter wording inside quoted text.

Mitigation: Review the script's ambiguous-form warnings and compare quoted text with its cited edition before accepting the generated file.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/j3ffyang/skills/simplified-to-traditional)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Traditional Chinese Markdown article with reciprocal cross-links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one explicitly named article per run; does not run automatically.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
