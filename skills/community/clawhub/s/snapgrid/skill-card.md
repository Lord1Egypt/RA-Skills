## Description:

Recover the pixel grid from damaged "fake pixel art" — sprites upscaled with smoothing, AI-generated, or blur/JPEG-damaged — and snap them back to pixel art. Use when asked to fix smoothed or blurry pixel art, recover a sprite's original resolution and palette, or clean up a sprite sheet or animation frames — for example "this pixel art was upscaled with smoothing, snap it back", "recover the original grid of this sprite", or "fix these animation frames so they share one grid and palette". Not for making textures tile seamlessly (that is seamproof) or finding 9-slice borders in UI panels (that is patchproof). A sheet or folder of frames is processed jointly, with one shared grid and one shared palette.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and digital artists use SnapGrid to recover a consistent pixel grid and palette from smoothed or damaged pixel art, including sprite sheets and animation frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged an install-command signature as unexpected for the stated purpose.

Mitigation: Review the Git-based install source and command before installing.

Risk: Security analysis was partial because palette sidecar references could not be resolved.

Mitigation: Review the palette sidecar behavior before relying on generated files.

## Reference(s):

- [Repository named in the install instructions](https://github.com/RakTikoo/snapgrid)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands; repaired image files and GPL/JSON palette sidecars when run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A successful run writes repaired PNG image(s) and shared palette sidecars; an abstention writes nothing.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
