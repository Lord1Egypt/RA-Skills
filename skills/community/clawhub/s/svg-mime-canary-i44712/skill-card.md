## Description:

Inert canary skill used during an authorized ClawHub assessment to observe the HTTP headers applied when a published skill ships an SVG file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playgod2023](https://clawhub.ai/user/playgod2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security assessors can use this inert canary to observe the HTTP headers served for a published SVG file during an authorized ClawHub assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked assets/icon.svg as executable, although the skill describes it as a static icon.

Mitigation: Confirm the SVG asset is expected and inspect it for active content before installing; the provided file contains only a static rectangle.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/playgod2023/skills/svg-mime-canary-i44712)
- [Publisher profile: playgod2023](https://clawhub.ai/user/playgod2023)

## Skill Output:

**Output Type(s):** [Guidance, Files]

**Output Format:** [Markdown documentation and a static SVG file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No runtime behavior; the included SVG is a static green rectangle.]

## Skill Version(s):

0.0.1 (source: frontmatter, consistent with server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
