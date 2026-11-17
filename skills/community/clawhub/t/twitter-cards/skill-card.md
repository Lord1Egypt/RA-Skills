## Description:

Guides agents to add or optimize Twitter Card metadata for X/Twitter link previews, including card type, title, description, image, handle, and accessibility tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site maintainers use this skill to generate or review Twitter/X card metadata so shared links display accurate titles, descriptions, images, and account attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated metadata can publish inaccurate titles, descriptions, handles, image URLs, or alt text.

Mitigation: Review generated Twitter Card fields and public image links before publishing changes.

Risk: Public preview images may fail if URLs are relative, inaccessible, too small, too large, or in an unsupported format.

Mitigation: Use absolute HTTPS image URLs and validate previews with the X Card Validator before release.

## Reference(s):

- [X Card Validator](https://cards-dev.twitter.com/validator)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with HTML and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended image dimensions, tag length limits, absolute image URL requirements, and testing guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
