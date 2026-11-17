## Description:

Remove image backgrounds with Yaps and save a transparent, solid-background, or outlined-sticker PNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People editing images locally use this skill to remove a background and export a transparent PNG, a solid-color image, or an outlined sticker through Yaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged runtime can access broader Yaps media and account functions than background removal alone.

Mitigation: Review before installation and approve only the intended background-removal operation in a trusted local session.

Risk: Account checks or refresh may trigger unexpected credential prompts.

Mitigation: Do not approve unexpected credential prompts; manage sign-in directly in Yaps.

Risk: Processing the wrong image or replacing an existing export could expose or destroy files.

Mitigation: Choose input files explicitly, write to a new destination, and preserve sources and prior exports.

## Reference(s):

- [Yaps Background Removal on ClawHub](https://clawhub.ai/yaps/skills/yaps-background-removal)
- [Yaps local runtime guide](references/runtime.md)
- [Download or open Yaps](https://yaps.ai/download)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PNG image and concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transparent, solid-background, or outlined-sticker output; report dimensions and mask coverage when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
