## Description:

Processes local venue scene images by blending a person reference into a user-provided store, restaurant, cafe, mall, or similar setting with Replicate gpt-image-2 editing followed by SeedVR2 upscaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turkyden](https://clawhub.ai/user/turkyden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate local-business visit images by placing a selected or preset person reference into a venue scene and returning an upscaled result. It is intended for workflows where the user provides an authorized scene image or URL, configures Replicate credentials, and needs reproducible shell-command guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled local paths may upload arbitrary readable files to Replicate or SeedVR2.

Mitigation: Run the skill in a sandbox limited to dedicated input and output folders, and use only non-sensitive images the user is authorized to process.

Risk: User-controlled image URLs may point to internal, private, or unauthorized resources.

Mitigation: Allow only trusted public HTTPS image URLs and reject internal URLs or arbitrary local network locations.

Risk: User-controlled output paths may overwrite files writable by the execution environment.

Mitigation: Constrain outputs to a dedicated output directory and review the resolved path before execution.

Risk: Generated images may involve identifiable people or private business interiors.

Mitigation: Use only images with appropriate consent and avoid private interiors or identifiable people unless the user confirms authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turkyden/skills/tandian-image-skills)
- [Publisher profile](https://clawhub.ai/user/turkyden)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local output file paths; runtime output is a WebP image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REPLICATE_API_TOKEN, an accessible scene image path or URL, and a writable output path.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
