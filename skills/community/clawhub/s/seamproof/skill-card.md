## Description:

Make a texture or a whole PBR texture set tile seamlessly, with a measured seam score. Use when asked to make a texture seamless or tileable, fix visible seams or a repeating grid on a game texture, or process PBR maps (albedo/basecolor, normal, roughness, height, metallic/AO) so the whole set stays in register — for example "make this texture tile", "fix the seams on these maps", "why does my texture show a grid when tiled", or "score how seamless this texture is". Not for finding 9-slice borders in UI panels (that is patchproof) or recovering the grid of damaged pixel art (that is snapgrid).

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and artists use SeamProof to repair visible seams in individual textures or aligned PBR map sets and review measured before-and-after seam scores before using the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign but had medium confidence and partial coverage; installing from the Git-based package reference carries unassessed risk.

Mitigation: Review the package source and install only if you trust it; the scan does not establish that the package is risk-free.

Risk: Alpha-channel seams are not fixed, and images smaller than 8x8 are copied unchanged.

Mitigation: Check alpha separately and inspect small images before relying on the processed result.

Risk: Colour-map detrending can flatten intentional broad shading.

Mitigation: Use --no-detrend when preserving an intentional gradient matters.

## Reference(s):

- [SeamProof on ClawHub](https://clawhub.ai/raktikoo/skills/seamproof)
- [Project link in installation instructions](https://github.com/RakTikoo/seamproof)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Processed texture image files and a per-map plain-text report with seam scores, tiled re-scores, and verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A shared correction keeps maps in a set aligned. Results may remain poor for strong edge features; alpha seams pass through unchanged.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
