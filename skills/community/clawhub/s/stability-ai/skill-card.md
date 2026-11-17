## Description:

Generate high-quality images via Stability AI API (SDXL, SD3, Stable Image Core).

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Digital artists, developers, and content creators use this skill to generate Stability AI images from text prompts with model, style, aspect ratio, seed, and output-format controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API credentials may be sent to a configured API_HOST.

Mitigation: Use the default Stability AI HTTPS endpoint or only trusted HTTPS API_HOST values, and do not configure untrusted custom hosts.

Risk: The cleanup routine can delete older image files and same-basename JSON files in the selected output directory.

Mitigation: Use a dedicated empty output directory for generated assets instead of a directory containing unrelated images.

Risk: Generated metadata stores prompts and settings that may be sensitive.

Mitigation: Review metadata before sharing outputs and avoid including confidential information in prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1999azzar/skills/stability-ai)
- [Publisher profile](https://clawhub.ai/user/1999azzar)
- [Stability AI API Reference](artifact/references/models.md)

## Skill Output:

**Output Type(s):** [Files, JSON metadata, Shell commands, Configuration guidance]

**Output Format:** [Local image files with JSON metadata and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PNG, JPG, and WebP outputs; metadata stores prompt and generation settings; cleanup keeps the most recent 20 generated images.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
