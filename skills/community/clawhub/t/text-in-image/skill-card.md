## Description:

Helps agents generate images with exact visible text for posters, packaging, ads, social graphics, UI mockups, menus, signage, and infographics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent builders use this skill when an image must contain exact copy, such as a product label, poster headline, ad tagline, UI mockup label, menu item, or sign. It guides model choice, prompt structure, generation parameters, and full-resolution verification so visible text matches the supplied wording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text and provided reference images may be sent to external image-generation providers through Runware.

Mitigation: Avoid sensitive images or private copy unless that provider flow is approved for the use case.

Risk: Generated images can contain misspelled, omitted, or extra characters even when exact text is requested.

Mitigation: Inspect every required string at full resolution and edit or regenerate before returning the image.

## Reference(s):

- [Worked recipes](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON imageInference request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, structured prompt JSON, generation settings, and verification steps for exact on-image text.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
