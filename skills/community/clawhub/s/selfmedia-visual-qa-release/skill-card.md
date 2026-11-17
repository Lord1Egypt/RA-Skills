## Description:

Validate a rendered media delivery package against an explicit file and media contract, including video streams, image sizes, and subtitle timing; report failures without promoting or overwriting files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Creators and media production teams can check a finished delivery package against the actual handoff requirements and use the reported fields to address failures. The included five-file Douyin contract is a project example, not a universal platform requirement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included Douyin example contract could be mistaken for a universal platform requirement.

Mitigation: Confirm the user's actual requirements and adjust the contract before validation.

Risk: A passing metadata check could be mistaken for proof of visual quality or platform acceptance.

Mitigation: Inspect images at their intended display size and review the video visually; treat a pass as compliance with the selected local contract only.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text validation findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only checks against the selected local contract; a pass does not establish visual quality or platform acceptance.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
