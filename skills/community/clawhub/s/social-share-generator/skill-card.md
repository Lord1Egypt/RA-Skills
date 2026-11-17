## Description:

Helps agents add, optimize, or audit social share buttons, including placement, platform selection, share URLs, icon guidance, accessibility, and native Web Share API fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to guide agents that implement share buttons for articles, posts, products, and other web pages. It helps choose appropriate placements, platforms, share intent URLs, icon handling, and accessibility requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated share URLs may encode the wrong destination, message, or tracking parameters.

Mitigation: Review generated URLs before release and confirm that encoded text, destinations, and tracking parameters match privacy and analytics expectations.

Risk: Generated icon recommendations may drift from current platform brand requirements.

Mitigation: Use official platform brand assets and verify icon sizes, colors, and naming before publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with URL examples and inline JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces placement, platform, share URL, icon, and accessibility recommendations; no files are written by the skill itself.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
