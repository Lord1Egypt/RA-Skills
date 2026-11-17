## Description:

Extract clean, transparent-background signature ink from photos and scanned documents, including workflows to remove light backgrounds or red stamps, darken ink, and upscale the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anhao6170](https://clawhub.ai/user/anhao6170)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to extract handwritten black or gray signature strokes from an image, produce a transparent PNG, optionally upscale the result, and report output dimensions and ink pixel count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing very large untrusted images or extreme scale values may create dependency and input-size hygiene issues.

Mitigation: Install dependencies in a virtual environment and avoid very large dimensions or extreme scale values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anhao6170/skills/signature-extractor)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown response with shell command usage and generated RGBA PNG file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script reports output dimensions and ink pixel count after processing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
